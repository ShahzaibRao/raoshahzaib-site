---
title: "Linux Routing System Part 2: Hands-On Routing Experiments"
description: "Two hands-on Linux routing experiments: route from a network namespace to the host and out to external DNS, and see why ARP and gateways behave as they do."
slug: "linux-routing-system-part-2"
---

By Rao Shahzaib · DevOps

## Key Takeaway

This is a follow-up to the previous article,  [4. Understand Linux Routing System](/blog/linux-routing-system) , presenting two interesting hands-on experiments. Through these experiments, we will attempt to interact with targets outside the Network Namespace, such as the **eth0** interface on the local host, or external network services like **Google DNS**.

## Experiment 2 - Direct route from a Network Namespace to Host eth0

In Experiment 2, we will initiate a ping command from the **`eth0`** interface inside the **`network namespace ns1`** to the **`Host eth0`** interface. Since these two interfaces belong to different subnets, they cannot communicate directly. Therefore, we will explore how, by interacting with the **`Routing` Table** and utilizing the **`bridge br0`**, we can eventually succeed in pinging the **`Host eth0`**.


During the experiment, we will observe two interesting issues, and we will leave one additional question for the reader to ponder.

In addition, this environment does not have any default routing rules and does not use a gateway. Instead, it adopts a **`Direct Routing`** approach.


The architectural diagram is shown below.

![Experiment 2 - Direct route from a Network Namespace to Host eth0 — diagram](/images/linux-routing-system-part-2/01-routing-table-2-drawio.svg)

### Experimental Environment Setup

This environment uses the **Ubuntu 24.04 server** provided by **iximiuz Labs**, which offers a fast and convenient online practice environment.

Reference: [https://labs.iximiuz.com/](https://labs.iximiuz.com/)

**commands - Create our environment**

```bash
# Create a network namepsace called ns1
sudo ip netns add ns1
# Create a virtual ethernet pair called veth1 & veth2
sudo ip link add veth1 type veth peer name veth2
# Attach veth2 to ns1
sudo ip link set veth2 netns ns1
# Create a linux bridge called br0
sudo ip link add br0 type bridge
# Attach veth1 to br0
sudo ip link set veth1 master br0
# Bring interfaces up
sudo ip link set veth1 up
sudo ip link set br0 up
sudo ip netns exec ns1 ip link set veth2 up
# Assign the IP address
sudo ip netns exec ns1 ip link set veth2 name eth0
sudo ip netns exec ns1 ip addr add 10.22.33.4/24 dev eth0
sudo ip addr add 10.22.33.1 dev br0
```

### Let’s begin the experiment!

#### 1. Ping `Host eth0` from `ns1`

![1. Ping Host eth0 from ns1 — screenshot](/images/linux-routing-system-part-2/02-screenshot-2025-08-01-8-50-39.png)

First, let’s check the routing table of `ns1`. At the moment, it contains only one entry:

`10.22.33.0/24 dev eth0 proto kernel scope link src 10.22.33.4`

Next, when we issue a `ping` command from `ns1` to the `Host`, we can observe that it results in a **“Network is unreachable”** status.


#### 2. Update `ns1`'s routing table

![2. Update ns1's routing table — screenshot](/images/linux-routing-system-part-2/03-screenshot-2025-08-01-8-57-17.png)

Since that’s the case, let’s try adding the `Host’s `**`eth0`** to `ns1`’s routing table.

- **Step 1:** Add the route with the command

  `ip route add 172.16.0.2/32 dev eth0`

- **Step 2:** Issue the `ping` command to the Host again

Result: We get a different outcome — it’s no longer **“Network is unreachable”**, but the `ping` command becomes stuck (hangs)…

Why is that? Let’s debug it step by step.


#### 3. Observe two questions

![3. Observe two questions — screenshot](/images/linux-routing-system-part-2/04-screenshot-2025-08-01-9-11-47.png)

- **Step 1:** Check the ARP table in `ns1`. We can observe an interesting phenomenon:
  - **Question 1:** Why does `ns1`’s ARP table show the **IP address** of the `Host’s eth0` interface, but the **MAC address** recorded is that of the `br0` interface?
- **Step 2:** On the Host side (bottom right), run `tcpdump` to listen for packets traversing the `br0` interface.
- **Step 3:** Return to `ns1` and issue the `ping` to the Host again.

**Question 2:** At this point we observe that `br0` receives the **ICMP Request** packets but no **ICMP Reply** packets. Why is that?

#### 4. Solve the Question 2

![4. Solve the Question 2 — screenshot](/images/linux-routing-system-part-2/05-screenshot-2025-08-01-9-29-47.png)

Let’s answer **Question 2** first.

- **Step 1:** Check the Host’s routing table.
  - We find only the `default` route and a `172.16.0.0/24 …` route. That means the Host does not know how to deliver packets to `ns1`.
- **Step 2:** Therefore, we manually add a route to `ns1`:

  `$ sudo ip route add 10.22.33.0/24 dev br0`


#### 5. Result of solving the Question 2

![5. Result of solving the Question 2 — screenshot](/images/linux-routing-system-part-2/06-screenshot-2025-08-01-9-30-15.png)

After adding the route, we issue the `ping` command again — and this time, it succeeds. We can also observe that the `br0` interface now carries both **`ICMP Request`** and **`ICMP Reply`** packets.

Through this small experiment, we learned that in order to successfully send and receive packets, every point the packet passes through must have the appropriate routing in place.


### Let’s return to **`Question 1`** once again.

#### The core issue

Why does the ARP table in `ns1` map the IP address `172.16.0.2` (Host eth0’s IP) to the MAC address of `br0` (`26:3b:a6:f0:d8:6a`), instead of the MAC address of Host eth0 (`62:c1:4b:74:54:6f`)?

![The core issue — screenshot](/images/linux-routing-system-part-2/07-screenshot-2025-08-01-11-07-53.png)

Let’s confirm the packet path when pinging `Host eth0` from `ns1`.

- **Step 1:** On the right side of the left diagram, we listen on the `Host eth0` interface (above) and on the `br0` interface (below).
- **Step 2:** From `ns1`, initiate a `ping` command to the `Host eth0` interface.


![The core issue — screenshot](/images/linux-routing-system-part-2/08-screenshot-2025-08-01-11-08-04.png)

Next, we observe an interesting phenomenon.

The packet reaches the `br0` interface and is returned back to `ns1`; it is not forwarded to the `Host eth0` interface.

So, why does this happen? And who allows `br0` to respond to ARP requests on behalf of `Host eth0`? Please continue reading to find out.


#### Analysis of the cause behind **`Question 1`**

Because we added `172.16.0.2/32 dev eth0` to `ns1`’s routing table, this tells the Linux kernel that packets destined for `172.16.0.2` can be sent directly without going through a gateway, using the `eth0` interface in `ns1`.

So, Linux considers `172.16.0.2` to be on the “local network” of `ns1`, and therefore it actively sends out an **ARP request** asking, “Who has 172.16.0.2?”

When the Host receives this ARP request, it notices:

- Although `172.16.0.2` is the IP address of `Host eth0`,
- The packet came in through the `veth` interface (which is connected to `br0`),
- If `ip_forward` is enabled and there are no other restrictions,
- Then the Linux kernel will **reply to the ARP request**, saying: “172.16.0.2 is me, my MAC address is \[MAC of br0\]. Send the packets to me, and I will forward them.”

This causes the ARP record we see in `ns1` to show `(Host eth0 IP address) at [br0 MAC address] on eth0`.

This also means that `br0` and `Host eth0` are in the same namespace (kernel), so `br0` can respond to ARP requests on behalf of `Host eth0`.

### A question left for you to ponder

After analyzing **Question 1**, we know that in this case, `br0` can respond to ICMP packets from `ns1` on behalf of `Host eth0`.

So, the question is: Did the packets actually get delivered to `Host eth0`, or were they returned as soon as they reached `br0`?

Feel free to try it out and find the answer yourself.

## Experiment 3 - Try to communicate to Google DNS from a Network Namespace

In Experiment 3, we will initiate a ping command from the **eth0** interface inside the network namespace `ns1` to an external network (Google DNS).

Compared to Experiment 2, in this experiment, we set the bridge `br0` as the **gateway** for `ns1`, allowing it to help forward packets. Please note the architectural diagram below.

Note that this experiment will **not successfully ping Google DNS**, but it still provides some interesting insights. In a future article, we will address and resolve this issue—stay tuned!

The architectural diagram is as follows.

![Experiment 3 - Try to communicate to Google DNS from a Network Namespace — diagram](/images/linux-routing-system-part-2/09-routing-table-3-drawio.svg)

### Experimental Environment Setup

This environment uses the **Ubuntu 24.04 server** provided by **iximiuz Labs**, which offers a fast and convenient online practice environment.

Reference: [https://labs.iximiuz.com/](https://labs.iximiuz.com/)

**commands - Create our environment**

```bash
# Create a network namepsace called ns1
sudo ip netns add ns1
# Create a virtual ethernet pair called veth1 & veth2
sudo ip link add veth1 type veth peer name veth2
# Attach veth2 to ns1
sudo ip link set veth2 netns ns1
# Create a linux bridge called br0
sudo ip link add br0 type bridge
# Attach veth1 to br0
sudo ip link set veth1 master br0
# Bring interfaces up
sudo ip link set veth1 up
sudo ip link set br0 up
sudo ip netns exec ns1 ip link set veth2 name eth0
# Assign the IP address
sudo ip netns exec ns1 ip link set eth0 up
sudo ip netns exec ns1 ip addr add 10.22.33.4/24 dev eth0
sudo ip addr add 10.22.33.1 dev br0
```

### Let’s begin the experiment!

#### 1. First check our environment

![1. First check our environment — screenshot](/images/linux-routing-system-part-2/10-screenshot-2025-08-06-12-30-49.png)

After setting up the environment, it will appear as shown in the left diagram.

In addition to displaying the network configuration, it also shows the routing tables of both the `Host` and `ns1` individually.


#### 2. Ping Google DNS from `ns1`

![2. Ping Google DNS from ns1 — screenshot](/images/linux-routing-system-part-2/11-screenshot-2025-08-06-12-39-53.png)

We confirm that in the Host environment, we can successfully ping Google DNS (8.8.8.8).

However, in the `ns1` environment, the result is **“Network is unreachable.”**

- This is because `ns1`’s routing table lacks a default route and has no specified route to the destination, so it does not know how to forward the packets.

#### 3. Direct routing to Google DNS in `ns1`

![3. Direct routing to Google DNS in ns1 — screenshot](/images/linux-routing-system-part-2/12-screenshot-2025-08-06-12-47-08.png)

- **Step 1:** On the Host side, monitor all packets passing through `br0`.
- **Step 2:** Manually add a direct route for Google DNS:

  `$ ip route add 8.8.8.8/32 dev eth0`

- **Step 3:** Attempt the `ping` command again.
  - At this point, the command hangs in `ns1`.
  - On the Host side (left), observe that the `br0` interface receives ARP Request packets asking “Who has IP address 8.8.8.8?”

However, since `8.8.8.8` belongs to an external network and is not part of any subnet on this machine, the Linux kernel responsible for the Host’s `br0` interface cannot respond to these ARP requests, resulting in no ARP Reply.

**Relation to Experiment 2**

In the previous Experiment 2, we pinged the Host’s eth0 interface from `ns1`. Although Host eth0 and `ns1` do not belong to the same subnet, because Host eth0 and Host br0 reside in the same network namespace and on the same machine, the Linux kernel can respond to ARP requests on behalf of Host br0.

#### 4. Turn `br0` as Gateway and monitor it

![4. Turn br0 as Gateway and monitor it — screenshot](/images/linux-routing-system-part-2/13-screenshot-2025-08-06-12-50-45.png)

How can we address the issue above?

- **Step 1:** Remove the previous direct route and add a new route with the command:

  `$ ip route add 8.8.8.8/32 via 10.22.33.1 dev eth0`


  - This sets `br0 (10.22.33.1)` as the gateway.
  - You will see `8.8.8.8 via 10.22.33.1 dev eth0` in `ns1`’s routing table.
- **Step 2:** Try pinging `8.8.8.8` again.
  - You will observe that the Host now receives ICMP echo request packets.

In this situation, all packet requests sent from `ns1` to `8.8.8.8` will pass through `br0` as the gateway (for `ns1`, `br0` now acts as its gateway) to forward the packets on behalf of `ns1`.


#### 5. Examine our ARP Table

![5. Examine our ARP Table — screenshot](/images/linux-routing-system-part-2/14-screenshot-2025-08-06-3-53-05.png)

So far, after checking `ns1`’s current Routing Table and ARP Table (using the command `$ arp -a`), we can analyze the following:

- `? (8.8.8.8) at <incomplete> on eth0`
  - `<incomplete>` means that `ns1` attempted to resolve the MAC address for `8.8.8.8` but failed. This is usually because `8.8.8.8` is not in the same network as `eth0` (which is in the `10.22.33.0/24` subnet).
  - ARP protocol only works for IP address resolution within the same subnet. Since `8.8.8.8` is an external network address, its MAC address cannot be obtained via ARP.
  - This situation usually indicates that `ns1` needs to access external networks via a gateway (for example, `10.22.33.1` may act as the gateway).
- `? (10.22.33.1) at 46:47:b7:ad:a6:90 [ether] on eth0`
  - Since `ns1`’s eth0 and `br0` are on the same network (`10.22.33.0/24`), `ns1` can communicate directly with `br0` using ARP.
  - This ARP entry shows that `ns1` successfully obtained the MAC address of `br0`, meaning that `ns1`’s eth0 and `br0` (IP `10.22.33.1`) are able to communicate at Layer 2 (data link layer).

Therefore, typically, packet forwarding between different subnets requires a gateway. The gateway is identified and communicated with via its MAC address, rather than by the destination IP address.

#### 5. Monitor `Host eth0` interface

![5. Monitor Host eth0 interface — screenshot](/images/linux-routing-system-part-2/15-screenshot-2025-08-06-3-57-49.png)

Earlier, we monitored the `br0` interface. Now, let’s switch to monitoring ICMP packets on the Host’s `eth0` interface.

- **Step 1:** Before starting, confirm whether IP forwarding is enabled. If it’s not set to 1, the host will not forward packets from `br0` to `Host eth0`.
- **Step 2:** Monitor ICMP packets on the `Host eth0` interface.
- **Step 3:** From `ns1`, initiate a ping command to `8.8.8.8`.

At this point, we can see that ICMP echo request packets successfully pass through the `Host eth0` interface towards the external network.


***However, we do not receive ICMP Echo Reply packets. This issue will be discussed in a future article.***


## Conclusion

In this article, we have summarized the following conclusions:

- In Experiment 2, we explored two interesting issues and understood that for packets to be correctly sent and received, every node along the path must have clear and proper routing.
- In Experiment 3, through communication with external services, we learned the concept of a gateway and gained a deeper understanding of routing.
