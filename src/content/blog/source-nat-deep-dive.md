---
title: "From Container to Internet: A Deep Dive into Source NAT"
description: "How source NAT carries container traffic to the internet: SNAT hooks, MASQUERADE rules, and experiments that break and then fix the path, step by step."
slug: "source-nat-deep-dive"
---

By Rao Shahzaib · DevOps

## Key Takeaway

> In this section, we’ll discuss the purpose of **Source NAT (SNAT)** and observe how SNAT affects our packets through three small experiments.

## Source NAT (SNAT)

### What is SNAT ?

In the previous section (@6. Understanding the Relationship Between iptables, Docker, and Linux Bridge), we mentioned that **`iptables`** is a **user-space tool** that allows users to configure and interact with the **Linux kernel’s** **`Netfilter`** **system**.

In common use cases, users employ iptables to define **`firewall rules`** or **`packet translation rules`**.

Among these, **`Source NAT (SNAT)`** is a feature implemented by Netfilter that modifies the **`source IP address or port`** of packets, allowing internal network hosts to communicate with external networks using a single public IP address.

In other words, ***iptables provides the configuration interface, while the Netfilter subsystem in the Linux kernel actually performs the SNAT operation and packet transformation.***

### Two Types of SNAT

In **iptables**, there are two built-in NAT targets used for **`Source NAT (SNAT)`**, but they differ in how the source IP is set:

#### Type 1: `SNAT`

- **Behavior**: Replaces the source IP of outgoing packets with a ***specific, static public IP address***.
- **When to use**:
- You have a stable, known public IP.
- Common in data centers, servers, or static ISP connections.
- **Performance**: Slightly more efficient than MASQUERADE (no extra lookups needed).
- **Example**
  ```bash
  $ iptables -t nat -A POSTROUTING -s 192.168.1.0/24 -o eth0 -j SNAT --to-source 203.0.113.5:8877
  ```

The above command demonstrates how to modify the **IP address** and **port number** using **iptables**.

When the source address is `192.168.1.0`, any packet sent out through the `eth0` interface will have its **source** rewritten to `203.0.113.5:8877`.

***Note:***

- If you specify a non-existent address in `-to-source`, iptables will still accept and apply the rule successfully. However, the returning packets will not be able to reach their destination.
- If no port number is specified in `-to-source`, the kernel will automatically assign a random port number from the range **1024–64512**.

#### Type 2: `MASQUERADE`

- **Behavior**: ***Dynamically uses the current IP of the outgoing interface*** as the NAT source.
- **When to use**:
- Your public IP is **dynamic** (e.g., typical home broadband or mobile networks).
- PPPoE or DHCP environments where the IP can change without notice.
- **Extra work**: Every time the interface’s IP changes, MASQUERADE automatically adapts.
- **Performance**: Slightly slower than SNAT because it must check the interface’s IP for each packet.
- **Example**
  ```bash
  iptables -t nat -A POSTROUTING -s 192.168.1.0/24 -o eth0 -j MASQUERADE
  ```

### Where does Source NAT take effect?

![Diagram: Where does Source NAT take effect?](/images/source-nat-deep-dive/01-source-nat-deep-dive.webp)
From the diagram left, we can observe that **`SNAT`** **is located in the** **`POSTROUTING`** **chain**.

However, if we take a closer look at the actual implementation inside the **`Linux kernel`** **(v6.16)**, we’ll notice something interesting.

In the **`Netfilter hooks`**, besides being able to modify the **source IP and port number** in the **`POSTROUTING`** **chain**, it’s also possible to perform such modifications in the **`INPUT`** **chain (** **`NF_INET_LOCAL_IN`** **)** — a detail that isn’t illustrated in the diagram on the left.


**The Hooks of `SNAT` in Linux Kernel**

```c
//https://github.com/torvalds/linux/blob/v6.16/net/netfilter/xt_nat.c#L150-L225
static struct xt_target xt_nat_target_reg[] __read_mostly = {
	{
		.name		= "SNAT",
		.revision	= 0,
		.checkentry	= xt_nat_checkentry_v0,
		.destroy	= xt_nat_destroy,
		.target		= xt_snat_target_v0,
		.targetsize	= sizeof(struct nf_nat_ipv4_multi_range_compat),
		.family		= NFPROTO_IPV4,
		.table		= "nat",
		.hooks		= (1 << NF_INET_POST_ROUTING) |
							  (1 << NF_INET_LOCAL_IN),
		.me		= THIS_MODULE,
	},
	.
	.
	.
	{
		.name		= "SNAT",
		.revision	= 1,
		.checkentry	= xt_nat_checkentry,
		.destroy	= xt_nat_destroy,
		.target		= xt_snat_target_v1,
		.targetsize	= sizeof(struct nf_nat_range),
		.table		= "nat",
		.hooks		= (1 << NF_INET_POST_ROUTING) |
							  (1 << NF_INET_LOCAL_IN),
		.me		= THIS_MODULE,
	},
	.
	.
	
	{
		.name		= "SNAT",
		.revision	= 2,
		.checkentry	= xt_nat_checkentry,
		.destroy	= xt_nat_destroy,
		.target		= xt_snat_target_v2,
		.targetsize	= sizeof(struct nf_nat_range2),
		.table		= "nat",
		.hooks		= (1 << NF_INET_POST_ROUTING) |
							  (1 << NF_INET_LOCAL_IN),
		.me		= THIS_MODULE,
	},
	.
	.
	.
};

```

**The Hooks of `MASQUERADE` in Linux Kernel**

> The **`MASQUERADE`** target, on the other hand, is explicitly restricted to modifying the **IP address and port number** only within the **`POSTROUTING`** **chain**.

```c
https://github.com/torvalds/linux/blob/v6.16/net/netfilter/xt_MASQUERADE.c#L72-L96
static struct xt_target masquerade_tg_reg[] __read_mostly = {
	{
#if IS_ENABLED(CONFIG_IPV6)
		.name		= "MASQUERADE",
		.family		= NFPROTO_IPV6,
		.target		= masquerade_tg6,
		.targetsize	= sizeof(struct nf_nat_range),
		.table		= "nat",
		.hooks		= 1 << NF_INET_POST_ROUTING,
		.checkentry	= masquerade_tg6_checkentry,
		.destroy	= masquerade_tg_destroy,
		.me		= THIS_MODULE,
	}, {
#endif
		.name		= "MASQUERADE",
		.family		= NFPROTO_IPV4,
		.target		= masquerade_tg,
		.targetsize	= sizeof(struct nf_nat_ipv4_multi_range_compat),
		.table		= "nat",
		.hooks		= 1 << NF_INET_POST_ROUTING,
		.checkentry	= masquerade_tg_check,
		.destroy	= masquerade_tg_destroy,
		.me		= THIS_MODULE,
	}
};

```


## **Set Up the Experiment Environment**

Before conducting the experiment, we need to set up the environment as shown in the diagram below.

![Diagram: Set Up the Experiment Environment](/images/source-nat-deep-dive/02-source-nat-deep-dive.svg)

> This environment uses the **Ubuntu 24.04 server** provided by **iximiuz Labs**, which offers a fast and convenient online practice environment.

> Reference: [https://labs.iximiuz.com/](https://labs.iximiuz.com/)

### **Install Docker**

Install following the official guide: [Docker Documentation](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository)[**Ubuntu**](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository)

After installation, the Docker service is not enabled by default, so we need to enable it using the following command:

```bash
$ sudo systemctl status docker.service
$ sudo systemctl start docker.service
$ sudo systemctl enable docker.service
```

### **Spin Up a Busybox Docker Container**

```bash
$ sudo docker run -d --name client busybox /bin/sh -c "sleep infinity"
```

![Diagram: Spin Up a Busybox Docker Container](/images/source-nat-deep-dive/03-source-nat-deep-dive.png)
After successfully creating a Docker container named `client`, we can use the command `$ ip -c a` to view the current **network interfaces** (highlighted in orange in the left diagram), and `$ sudo iptables-save -t nat -c` to inspect the **rules in the** **`nat`** **table**.

Among these, the **nat rules** we are particularly interested in are highlighted with a **blue underline** (`POSTROUTING`), which will be explained below.

#### nat table explanation

The explanation of the ***nat table*** **rules** is as follows:

- `PREROUTING`
  ```txt
  [2:104] -A PREROUTING -m addrtype --dst-type LOCAL -j DOCKER
  ```

- **Meaning**: All incoming packets (before routing decisions) with a **destination address of the local host (LOCAL)** are sent to the **DOCKER chain** for processing.
- **Counter** `[2:104]`: 2 packets (104 bytes) have matched this rule.
- **Purpose**: To intercept packets directed to the host’s IP. For **Docker port mappings** (e.g., `p 8080:80`), these packets are **DNATed (We will talk about it in the next post)** to the corresponding container within the **DOCKER chain**.
- **`OUTPUT`**
  ```txt
  [0:0] -A OUTPUT ! -d 127.0.0.0/8 -m addrtype --dst-type LOCAL -j DOCKER
  ```

- **Meaning**: Packets generated by the local host, as long as their **destination is not the loopback address (127.x.x.x)** and are of type `LOCAL`, are sent to the **DOCKER chain**.
- **Counter** `[0:0]`: No packets have matched this rule yet.
- **Purpose**: Supports access to Docker port mappings either **between containers** or from the **host itself**.
- **`POSTROUTING`**
  ```txt
  [3:192] -A POSTROUTING -s 172.17.0.0/16 ! -o docker0 -j MASQUERADE
  ```

- **Meaning**:
- Source IP is within the container subnet `172.17.0.0/16`
- Packet’s outgoing interface is **not** `docker0`
- Apply **`MASQUERADE (SNAT)`** to rewrite the source IP to the host’s external IP.
- **Counter** `[3:192]`: 3 packets (192 bytes) have already been **SNATed**.
- **Purpose**: *Allows containers to access external networks, making their traffic appear as if it originates from the host itself.*
- **`DOCKER`**
  ```txt
  [0:0] -A DOCKER -i docker0 -j RETURN
  ```

- **Meaning**: If a packet **comes from** `docker0`, it is returned immediately without applying **DNAT**.
- **Counter** `[0:0]`: No packets have triggered this rule yet.
- **Purpose**: Prevent Docker’s own bridge network traffic from being mistakenly subjected to **DNAT**.

## **Experiment 1 – Observing the Effect of Source NAT**

> In Experiment 1, we send packets from the container to the outside and observe their state as they pass through **`docker0`** and the `host’s `**`eth0`** interface, in order to verify the effect of **Source NAT**.

### 1.1 Use `nslookup` inside the container to query **google.com**

> If a packet is leaving the host to the public network, **NAT rewrites its source to the host’s public IP** (this is the role of SNAT).

> However, when observing the packet on **docker0**, you still see the container’s **private IP**.

![Diagram: 1.1 Use nslookup inside the container to query google.com](/images/source-nat-deep-dive/04-source-nat-deep-dive.png)
First, we use the `tcpdump` command to monitor the host’s **docker0** bridge and **eth0** interfaces.

Next, inside the container, we run `$ nslookup google.com` to query its IP address.

From the results, we can observe the following from different perspectives:

- **From the** **`docker0`** **bridge:**
- `172.17.0.2`: Source IP (the container’s IP on the docker0 network)
- `52739`: Source UDP ephemeral port used by the container to query the DNS server
- `203.0.113.157:53`: Destination DNS server IP and port 53
- **From host’s** **`eth0`** **:**
- The source IP is no longer `172.17.0.2`; it has been rewritten to `172.16.0.2`, which is the IP of the host’s `eth0` interface
- The port number remains the same (`52739`)

### 1.2 Run `nslookup google.com` **again inside the container**

![Diagram: 1.2 Run nslookup google.com again inside the container](/images/source-nat-deep-dive/05-source-nat-deep-dive.png)
When we run the same query again inside the container, we can observe that the **port number has changed**—from `52739` to `38851`. This happens because the new connection is assigned a **random port by the kernel**.

### 1.3 Ping `8.8.8.8` from the container

![Diagram: 1.3 Ping 8.8.8.8 from the container](/images/source-nat-deep-dive/06-source-nat-deep-dive.png)
Next, we use the **ping** command inside the container. Unlike `nslookup`, **ping does not rely on a specific port number**, as we will explain below.

#### `Ping` Uses ICMP, Not TCP/UDP

- `ping` uses **ICMP (Internet Control Message Protocol)**.
- ICMP operates at the **network layer (Layer 3)**, unlike TCP or UDP, which are transport layer protocols.
- Therefore, ICMP **does not have port numbers**. It only includes some basic fields:
- `Type` (e.g., Echo Request = 8, Echo Reply = 0)
- `Code` (provides more detailed classification)
- `Identifier` (id, used to distinguish different ping sessions)
- `Sequence number` (seq, used to track packet order)

In my packet capture (monitoring the **`docker0`** bridge):

```txt
ICMP echo request, id 20, seq 0, length 64
```

Here, `id=20` and `seq=0` are **ICMP’s own fields**, used to distinguish different requests, **not a port number**.

#### `nslookup` Uses DNS over UDP/TCP

- DNS queries usually use **`UDP/53`**, and sometimes **TCP/53** (especially for large responses or TCP fallback).
- UDP/TCP are **transport layer protocols**, which require **port numbers** to determine which application should receive the packet.
- On the server side, **destination port = 53** indicates a DNS service.
- On the client side, a **random source port** is chosen, e.g., `38851` in our case.

Thus, in `tcpdump` we see:

```txt
172.17.0.2.38851 > 203.0.113.157.53: ...
```

This shows **source port = 38851** and **destination port = 53**.

## Experiment 2 – Rules with a Specified Port Number Range

> In Experiment 2, we modify the original **POSTROUTING** rule to assign a fixed **range of port numbers**, and then observe the results.

### 2.1 Remove the original **POSTROUTING’s** rule

![Diagram: 2.1 Remove the original POSTROUTING’s rule](/images/source-nat-deep-dive/07-source-nat-deep-dive.png)
- **Step 1:** Check the current **iptables** **`nat`** **table** rules. Identify the **POSTROUTING** rule (highlighted with a blue underline) that we want to remove.
- **Step 2:** Use the `D` option to delete the **POSTROUTING** rule. Then verify that it has been successfully removed.


### 2.2 Use `nslookup` inside the container to query **google.com**.

![Diagram: 2.2 Use nslookup inside the container to query google.com.](/images/source-nat-deep-dive/08-source-nat-deep-dive.png)
After the **POSTROUTING** rule is removed, running `nslookup` will fail to retrieve information for **google.com**.

By observing the host’s **`docker0`** bridge and `host’s `**`eth0`** interface, we can see that all outgoing packets still have the source IP `172.17.0.2`, which is the container’s private IP.

This causes the packets to leave the host successfully, but the ***return traffic cannot reach the container***, resulting in failed responses.


### 2.3 Add a **POSTROUTING** rule with a **specified port number range**

![Diagram: 2.3 Add a POSTROUTING rule with a specified port number range](/images/source-nat-deep-dive/09-source-nat-deep-dive.png)
Next, we re-add the **POSTROUTING** rule, limiting the usable **port number range** to **55555–55600**.

- **Step 1:** Attempt to add the POSTROUTING rule.
- You may notice that the rule **cannot be added**, and `iptables` shows an error. The reason is:
- **MASQUERADE** is essentially a **SNAT** (Source NAT).
- When using the `-to-ports` option, `iptables` requires you to explicitly specify the **transport layer protocol** (TCP / UDP / SCTP / DCCP), because the concept of a "port" only exists for these protocols—not ICMP or others.
- Your current rule does **not include a protocol match** (`p tcp` or `p udp`), so `iptables` does not know how to apply `-to-ports`.
- **Step 2:** Re-add the POSTROUTING rule, specifying that it only applies to the **UDP protocol**.

### 2.4 Run `nslookup google.com` **again inside the container**

![Diagram: 2.4 Run nslookup google.com again inside the container](/images/source-nat-deep-dive/10-source-nat-deep-dive.png)
Next, we monitor the **docker0** bridge and the host’s **eth0** interface again, and run `nslookup` inside the container.

We can successfully retrieve information for **google.com**.

Observations:

- On the **`docker0 bridge`**, the packet uses **source port** `35077`.
- On `host’s `**`eth0`**, the packet shows **source port** `55600`, which falls within the **port range we specified**.

This demonstrates that when using **`MASQUERADE`** for ***dynamic port allocation***, the kernel correctly assigns a port that **respects the range we defined**.


### 2.5  Fail to ping `8.8.8.8` from the container

![Diagram: 2.5  Fail to ping 8.8.8.8 from the container](/images/source-nat-deep-dive/11-source-nat-deep-dive.png)
Now, let’s try the **ping** command.

The result fails, because the POSTROUTING rule we added earlier **only applies to UDP packets** and does **not apply to ICMP packets**.

### 2.6 Use `--random` option

![Diagram: 2.6 Use --random option](/images/source-nat-deep-dive/12-source-nat-deep-dive.png)
Next, we try using the `--random` option instead of specifying a fixed port number range, and observe the effect it produces.

![Diagram: 2.6 Use --random option](/images/source-nat-deep-dive/13-source-nat-deep-dive.png)
![Diagram: 2.6 Use --random option](/images/source-nat-deep-dive/14-source-nat-deep-dive.png)

The two images above both show the results when using `--random`.

- The **left image** corresponds to the **`first`** **nslookup** execution.
- The **right image** corresponds to the **`second`** **nslookup** execution.

We can see that when using `--random`, the **port numbers** observed on **`docker0`** and `host’s `**`eth0`** are completely randomized.

In contrast, in `Experiment 1`, since we did **not** use `--random`, the kernel tried to ***preserve the original port number***, which is why the source port appeared the same on both **`docker0`** and `host’s `**`eth0`**.

## **Experiment 3 – Using SNAT to Specify an IP Address**

> In the first two experiments, we explored how **MASQUERADE** dynamically modifies the **source IP and port** based on the host’s **eth0** interface.

> In Experiment 3, we will observe how **SNAT** can be used to **statically specify the source IP**.

### 3.1 Assign an **invalid source IP**

![Diagram: 3.1 Assign an invalid source IP](/images/source-nat-deep-dive/15-source-nat-deep-dive.png)
The advantage of **SNAT** is that when we have a **fixed IP address**, we can bind it so that outgoing packets can be correctly routed back to that specific IP.

First, we use the `-j SNAT` target with `--to-source 203.0.113.4` to bind an **invalid IP address**, `203.0.113.4`.

### 3.2 Use `nslookup` inside the container to query **google.com**.

![Diagram: 3.2 Use nslookup inside the container to query google.com.](/images/source-nat-deep-dive/16-source-nat-deep-dive.png)
By observing the packets on **docker0** and **eth0**, we can see that the **source IP** of packets leaving the `host’s `**`eth0`** interface has been changed to `203.0.113.4`.

However, since this IP address does **not belong to the host**, the outgoing packets cannot be routed back, causing the `nslookup` command to fail.

> If we change the source IP to someone else’s address, we can make that other machine receive packets that originally belonged to us. Sending a large volume of such spoofed packets can overload the victim host or congest its network; this technique is commonly used in `DDoS` and `reflection‑amplification` attacks.


### 3.3 Assign a valid and routable source IP

![Diagram: 3.3 Assign a valid and routable source IP](/images/source-nat-deep-dive/17-source-nat-deep-dive.png)
Next, we will assign the IP address of the `host’s eth0 `interface.

If you want to limit the range of port numbers, you can configure it using a command like the following.

```txt
--to-source 172.16.0.2:1000-1010
```

![Diagram: 3.3 Assign a valid and routable source IP](/images/source-nat-deep-dive/18-source-nat-deep-dive.png)
Finally, we can `successfully` query and retrieve information for **google.com**.


## **Conclusion**

In this chapter, we explored the concept of **Source NAT (SNAT)** and its practical applications. Through three experiments, we observed how:

1. **`MASQUERADE`** dynamically modifies the source IP and port based on the host’s interface, allowing containers to communicate with external networks.
2. Specifying **port ranges** enables control over which source ports can be used, and the kernel correctly enforces these limits.
3. **`SNAT`** allows static assignment of a source IP, ensuring that return traffic is correctly routed back to the intended host, while demonstrating the risks of IP spoofing.

These experiments provided a hands-on understanding of how Source NAT operates at different stages (docker0 bridge vs. host interface) and how it affects packet transmission.

In the next chapter, we will explore **`Destination NAT (DNAT)`** and discuss some interesting scenarios and use cases.

---
