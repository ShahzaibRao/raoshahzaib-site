---
title: "Understanding iptables, Docker, and the Linux Bridge"
description: "How iptables and the Linux bridge work together, what Docker changes in the filter table, and hands-on experiments tracing the packet path step by step."
slug: "iptables-docker-linux-bridge"
---

By Rao Shahzaib · DevOps

## Key Takeaway

> In this chapter, we will explore the roles of netfilter and iptables, take a closer look at the iptables filter table, and conduct experiments to observe how Docker impacts iptables.

## Introduction

When we have a Linux machine connected to a network and want to perform certain actions on its packets, how should we proceed?

First, we need to understand that in the Linux environment, network packets arriving from outside to the user application generally follow the flow shown in the diagram below.

![Diagram: Introduction](/images/iptables-docker-linux-bridge/01-iptables-docker-linux-bridge.svg)

### What is netfiler ?

- **`Netfilter`** is a framework within the Linux kernel used for filtering, modifying, and forwarding network packets.
- It provides a low-level infrastructure that allows hooks at different stages of packet processing (such as receiving, forwarding, and sending) within the kernel.
- Netfilter itself is built into the Linux kernel and offers underlying packet handling capabilities but ***does not directly interact with users***.
- The main functions of netfilter include:
- Packet filtering
- Network Address Translation (NAT)
- Packet modification (e.g., altering headers or marking packets)
- Packet forwarding or dropping

Reference: [netfilter/iptables project homepage<br />      -<br />    The netfilter.org project](https://www.netfilter.org/)

### What is iptables ?

- **`iptables`** is a user-space tool used to configure and manage rules within the netfilter framework, primarily operating at Layer 3 (the IP layer).
- It allows system administrators to define how network packets entering or leaving a Linux system should be handled—such as allowing, dropping, modifying, or forwarding packets.
- iptables interacts with netfilter via a command-line interface, passing user-defined rules to the kernel’s netfilter modules.
- iptables organizes its rules using **tables** and **chains**:
- **Tables**: such as `filter` (for filtering), `nat` (for network address translation), and `mangle` (for packet modification).
- **Chains**: such as `INPUT` (incoming packets), `OUTPUT` (outgoing packets), and `FORWARD` (forwarded packets).

### 5 Tables and 5 Chains in iptables

#### 5 Tables

- **`filter table`**
- **Purpose**: Used for packet filtering to decide whether to allow or drop packets.
- **Common Use Cases**: Setting firewall rules, such as blocking traffic from specific IPs or ports.
- **Default Table**: If no table is specified, iptables commands operate on the filter table by default.
- **`nat table`**
- **Purpose**: Used for Network Address Translation (NAT), including Source NAT (SNAT) and Destination NAT (DNAT).
- **Common Use Cases**: IP masquerading, port forwarding, or NAT routing.
- **Note**: The nat table only processes packets when they first enter certain chains (like PREROUTING or POSTROUTING).
- **`mangle table`**
- **Purpose**: Used to modify packet header information, such as TTL (Time To Live), TOS (Type of Service), or marking packets.
- **Common Use Cases**: Advanced traffic control or Quality of Service (QoS) management.
- **Feature**: Rules in the mangle table are executed before other tables.
- **`raw table`**
- **Purpose**: Used to mark packets to bypass connection tracking, e.g., setting NOTRACK.
- **Common Use Cases**: For high-performance needs or to avoid connection tracking.
- **Feature**: The raw table has the highest priority, with rules processed before other tables.
- **`security table`**
- **Purpose**:
- Handles packet processing related to Mandatory Access Control (MAC), especially for SELinux or other security modules.
- Allows filtering based on security contexts and is typically used in environments requiring higher security levels, such as enterprise servers or systems needing fine-grained security policies.
- Main functions include setting security markings on packets or interacting with SELinux security policies.
- **Common Use Cases**:
- Integrating with SELinux for security context–based firewall rules.
- Applying rules that distinguish network traffic by security level or role, restricting traffic based on security contexts.
- **Notes**:
- The security table is not enabled on all Linux systems and requires kernel support for SELinux or other MAC frameworks.
- It is generally processed after the filter and mangle tables, thus having lower priority than raw and mangle tables.

#### 5 Chains

iptables defines five built-in chains within the netfilter framework, representing `hooks` at different stages of packet processing:

1. **`PREROUTING`**
- **Trigger time**: When a packet just enters the system, before routing decisions are made.
- **Applicable tables**: nat, mangle, raw.
- **Common uses**: Destination NAT (DNAT), packet marking.
2. **`INPUT`**
- **Trigger time**: When the packet’s destination is the local machine.
- **Applicable tables**: filter, mangle, security.
- **Common uses**: Filtering incoming packets, e.g., restricting access from certain sources.
3. **`FORWARD`**
- **Trigger time**: When the packet is routed through the machine (the machine acts as a router).
- **Applicable tables**: filter, mangle.
- **Common uses**: Controlling traffic passing through the host, such as firewall rules on routers.
4. **`OUTPUT`**
- **Trigger time**: When locally generated packets are about to be sent out.
- **Applicable tables**: filter, nat, mangle, raw, security.
- **Common uses**: Filtering or modifying packets sent by the local machine.
5. **`POSTROUTING`**
- **Trigger time**: When the packet is about to leave the system, after routing decisions have been made.
- **Applicable tables**: nat, mangle, security.
- **Common uses**: Source NAT (SNAT), IP masquerading (MASQUERADE).

The diagram below illustrates the structure of Tables and Chains in iptables. (Reference: [https://gist.github.com/nerdalert/a1687ae4da1cc44a437d](https://gist.github.com/nerdalert/a1687ae4da1cc44a437d))

![Diagram: 5 Chains](/images/iptables-docker-linux-bridge/02-iptables-docker-linux-bridge.png)

## Further Understanding of the Filter Table

In most cases, the table we commonly use is the **Filter Table**, especially when using a Linux host as a router, where its intervention is necessary.

When only using the filter table, we focus on three chains: **`INPUT`**, **`FORWARD`**, and **`OUTPUT`**. Packet filtering can be performed based on the following three scenarios:

1. The packet’s destination is the local machine (**`INPUT`** chain).
2. The packet is being forwarded through the machine (**`FORWARD`** chain).
3. The packet’s destination is another address, originating locally (**`OUTPUT`** chain).

So how do we actually perform filtering? We simply add rules to the corresponding chains based on what we want to allow or block.

### **Useful Commands**

#### **Using the ****`iptables-save`**** Command**

![Diagram: Using the iptables-save Command](/images/iptables-docker-linux-bridge/03-iptables-docker-linux-bridge.png)

We can use the `iptables-save` command to display the contents of different tables. For example, using the command: `$ iptables-save -t filter` we can view the contents of the **filter** table.

From the output above, we can see that the filter table contains three chains: `INPUT`, `FORWARD`, and `OUTPUT`.

- `:INPUT ACCEPT [0:0]`
- This chain handles packets **coming into the local machine**.
- The default policy is `ACCEPT`, meaning all incoming packets are accepted by default.
- `:FORWARD ACCEPT [0:0]`
- This chain handles packets **being forwarded through the machine** (e.g., when the machine acts as a router).
- The default policy is also `ACCEPT`, allowing forwarded packets.
- `:OUTPUT ACCEPT [0:0]`
- This chain handles packets **originating from the local machine**.
- The default policy is `ACCEPT`.

The `[0:0]` after each chain represents `[packet count : byte count]`.

- Packet count (`0` here) indicates how many packets have been processed by this chain.
- Byte count (`0` here) indicates the total size in bytes of all processed packets.

#### **Using the ****`iptables`**** Command**

Besides using `iptables-save`, we can also use the `iptables` command with other options to view the rules. For example, the following command shows the filter table with detailed information: `$ iptables -L -t filter -v`

![Diagram: Using the iptables Command](/images/iptables-docker-linux-bridge/04-iptables-docker-linux-bridge.png)


Change the FORWARD chain policy in the filter table from ACCEPT to DROP

![Diagram: Using the iptables Command](/images/iptables-docker-linux-bridge/05-iptables-docker-linux-bridge.png)

### Examples of Adding and Deleting Rules

#### Adding

```bash
# Insert a rule into the INPUT chain of the filter table to accept packets coming from IP address 10.23.45.67 via the eth0 interface.
# Since the -I (insert) option is used, this rule will be placed at the top of the INPUT chain and take precedence over other rules. You can also use -A (append) to add the rule at the end.
$ iptables -t filter -I INPUT -i eth0 -s 10.23.45.67 -j ACCEPT
```

#### Deleting

```bash
# Delete a rule from the INPUT chain of the filter table that allows packets from IP address 10.23.45.67 coming through the eth0 interface to be ACCEPT.
$ iptables -t filter -D INPUT -i eth0 -s 10.23.45.67 -j ACCEPT
```

## Linux Bridge and iptables

### Quick Review of Linux Bridge

A **`bridge`** is a virtual network interface in the Linux kernel that implements Layer 2 (L2) network bridging, meaning:

- It connects multiple network interfaces together like a physical switch.
- It forwards packets between interfaces based on MAC addresses (similar to a switch).
- Common use cases include:
- Virtual networks for containers (e.g., Docker’s `docker0` bridge)
- Bridge mode networking for KVM/libvirt virtual machines
- Kubernetes networking (e.g., CNI plugins) for pod-to-pod communication

### What’s the relationship between bridge and iptables?

By default,* ****bridges only handle Layer 2 (MAC address) packet forwarding***, so bridged traffic (e.g., between VMs or containers) **does not necessarily pass through iptables**.

If you want to use iptables firewalls to control:

- Container traffic passing through bridges (like Docker bridges)
- Virtual machine bridge interface traffic

you **must enable** the kernel parameter `net.bridge.bridge-nf-call-iptables`. Otherwise, packets won’t enter iptables at all!

#### Linux kernel Config - `net.bridge.bridge-nf-call-iptables`

> We can use this kernel configuration to control whether packets passing through a bridge network interface should be processed by iptables’ filter table—especially the FORWARD chain.

- When `net.bridge.bridge-nf-call-iptables` is set to `1` (enabled), it means:
- **Packets received by the bridge interface will enter the iptables processing flow (especially the FORWARD chain).**
- Rules set in iptables can control packets passing through the bridge.
- Conversely, when `net.bridge.bridge-nf-call-iptables` is set to `0` (disabled):
- Packets passing through the bridge will **not** be processed by iptables.
- In other words, **your firewall rules will have no effect on traffic passing through the bridge.**

### Real-World Scenario

#### Docker Default Bridge (`docker0`)

- By default, Docker uses the `docker0` bridge (as shown in Experiment 1 of this note).
- If you want to control container inbound/outbound traffic with iptables (e.g., blocking certain ports), you need packets on the bridge to pass through iptables. This means `net.bridge.bridge-nf-call-iptables` must be set to `1`.

#### KVM Virtual Machines Using Bridge to Connect to External Network

- Suppose you connect a physical NIC and virtual NICs together using a bridge (e.g., `br0`).
- Traffic between virtual machines flows through the bridge.
- If `bridge-nf-call-iptables` is not enabled, iptables will **not see this traffic at all and therefore cannot filter it**.

## Experiment 1 – What Docker Did

> In Experiment 1, we will install Docker and gain a preliminary understanding of what changes it makes to the system’s iptables. In later articles, we will explore these topics in greater depth.

### Set Up the Experiment Environment

> This environment uses the **Ubuntu 24.04 server **provided by **iximiuz Labs**, which offers a fast and convenient online practice environment.

> Reference: [https://labs.iximiuz.com/](https://labs.iximiuz.com/)

#### Install Docker

- Install following the official guide: [Ubuntu](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository)
- After installation, the Docker service is not enabled by default, so we need to enable it using the following command:
  ```bash
  $ sudo systemctl status docker.service
  $ sudo systemctl start docker.service
  $ sudo systemctl enable docker.service
  ```

### Comparison of iptables Before and After Installing Docker

The following diagram provides a simple comparison of the iptables contents to help us understand what changes Docker has made.

![Diagram: Comparison of iptables Before and After Installing Docker](/images/iptables-docker-linux-bridge/06-iptables-docker-linux-bridge.png)

**iptales after installing Docker**

```bash
laborant@ubuntu-01:~$ sudo iptables-save -t filter
# Generated by iptables-save v1.8.10 (nf_tables) on Mon Aug 11 14:01:18 2025
*filter
:INPUT ACCEPT [0:0]
:FORWARD DROP [0:0]
:OUTPUT ACCEPT [0:0]
:DOCKER - [0:0]
:DOCKER-BRIDGE - [0:0]
:DOCKER-CT - [0:0]
:DOCKER-FORWARD - [0:0]
:DOCKER-ISOLATION-STAGE-1 - [0:0]
:DOCKER-ISOLATION-STAGE-2 - [0:0]
:DOCKER-USER - [0:0]
-A FORWARD -j DOCKER-USER
-A FORWARD -j DOCKER-FORWARD
-A DOCKER ! -i docker0 -o docker0 -j DROP
-A DOCKER-BRIDGE -o docker0 -j DOCKER
-A DOCKER-CT -o docker0 -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
-A DOCKER-FORWARD -j DOCKER-CT
-A DOCKER-FORWARD -j DOCKER-ISOLATION-STAGE-1
-A DOCKER-FORWARD -j DOCKER-BRIDGE
-A DOCKER-FORWARD -i docker0 -j ACCEPT
-A DOCKER-ISOLATION-STAGE-1 -i docker0 ! -o docker0 -j DOCKER-ISOLATION-STAGE-2
-A DOCKER-ISOLATION-STAGE-2 -o docker0 -j DROP
COMMIT
# Completed on Mon Aug 11 14:01:18 2025
```

#### **Main Differences (Brief Summary)**

**1\. The default policy of the `FORWARD` chain changes from **`ACCEPT`** to **`DROP`**

- **Impact**: This is the most significant change. The FORWARD chain, which originally allowed all forwarding traffic, now defaults to dropping all forwarded packets unless explicitly permitted by a rule. This may block non-Docker forwarding traffic, such as LXD, VPN, or other bridged networks.
- **Reason**: To ensure the security of container networks, Docker sets the default policy of the FORWARD chain to DROP and only allows traffic that matches its specific rules to pass through.

**2\. Several custom chains have been added**

- Docker added the following custom chains:
- **DOCKER**: Handles Docker container-specific forwarding rules.
- **DOCKER-BRIDGE**: Manages rules related to the bridge network (`docker0`).
- Docker uses the `docker0` bridge interface, and traffic passes through the FORWARD chain because `net.bridge.bridge-nf-call-iptables=1`.
- **DOCKER-CT**: Deals with connection tracking (conntrack) related rules.
- Rules allow traffic originating from containers (`i docker0 -j ACCEPT`) and established response traffic (via DOCKER-CT), while restricting direct external access to containers unless NAT rules are present.
- **DOCKER-FORWARD**: Coordinates Docker’s forwarding rules.
- **DOCKER-ISOLATION-STAGE-1** and **DOCKER-ISOLATION-STAGE-2**: Implement isolation between containers.
- **DOCKER-USER**: Allows users to insert custom rules that take precedence over Docker’s own rules.
- These chains form the core mechanism Docker uses to manage container networking, including NAT, port mapping, and isolation.

**3\. Jump rules added to the `FORWARD` chain**

- A FORWARD -j DOCKER-USER: All forwarded traffic first goes to the **DOCKER-USER** chain, allowing users to insert custom rules.
- A FORWARD -j DOCKER-FORWARD: If no match is found in **DOCKER-USER**, traffic proceeds to the **DOCKER-FORWARD** chain, where Docker’s own rules handle it.

**4\. No changes were made to the `INPUT` and `OUTPUT` chains**

- The default policies for the INPUT and OUTPUT chains remain ACCEPT, and no new rules have been added. This indicates that Docker only affects forwarding traffic (the FORWARD chain) and does not directly impact the host’s incoming or outgoing traffic.

## Experiment 2 – The Impact of iptables and Custom Bridges

> In Experiment 2, assuming Docker is already installed, we will create two Network Namespaces and a Linux Bridge. Using ping commands, we will explore how the iptables FORWARD chain affects the bridge.

> The experiment will be divided into three scenarios to examine different ways of adjusting iptables and the bridge to enable communication between the network namespaces.

> This experimental setup builds directly on the environment from Experiment 1.

### Set Up the Experiment Environment

#### Setup Network Namespaces and Bridge

**command**

```bash
# Create network namespaces ns1 & ns2
sudo ip netns add ns1
sudo ip netns add ns2
# Create bridge br0
sudo ip link add br0 type bridge
# Create virtual ethernet pairs
sudo ip link add veth1 type veth peer veth2
sudo ip link add veth3 type veth peer veth4
# Assign veth to ns
sudo ip link set netns ns1 veth1
sudo ip link set netns ns2 veth3
# Attach veth to br0
sudo ip link set veth2 master br0
sudo ip link set veth4 master br0
# Bring up interfaces
sudo ip link set up veth2
sudo ip link set up veth4
sudo ip link set up br0
sudo ip netns exec ns1 ip link set veth1 up
sudo ip netns exec ns2 ip link set veth3 up
# Assign IP address
sudo ip addr add 10.22.33.1/24 dev br0
sudo ip netns exec ns1 ip addr add 10.22.33.4/24 dev veth1
sudo ip netns exec ns2 ip addr add 10.22.33.5/24 dev veth3
```

The information after setup is shown in the two images below (the left image displays `Host` details, and the right image shows the information for network namespaces `ns1` and `ns2`).

![Diagram: command](/images/iptables-docker-linux-bridge/07-iptables-docker-linux-bridge.png)
![Diagram: command](/images/iptables-docker-linux-bridge/08-iptables-docker-linux-bridge.png)

### Let’s begin the experiment!

#### Scenario 1. `FORWARD` chain is `DROP`

![Diagram: Scenario 1. FORWARD chain is DROP](/images/iptables-docker-linux-bridge/09-iptables-docker-linux-bridge.png)
In Experiment 1, we clearly saw that Docker changes the iptables `FORWARD` chain policy to `DROP` and handles packet forwarding through the `docker0` bridge. Because of this, our self-created `br0` bridge cannot function properly.

- **Step 1****:** Use the command `$ iptables-save -t filter` to check the current iptables configuration.
- **Step 2****:** Monitor packets passing through the Host’s `br0` bridge interface.
- **Step 3****:** From `ns1`, ping `ns2`.

After these steps, we observe two key points:

- The `ping` command `fails`.
- ICMP echo reqest packets pass through the `br0` interface, but no ICMP echo reply packets are received.


![Diagram: Scenario 1. FORWARD chain is DROP](/images/iptables-docker-linux-bridge/10-iptables-docker-linux-bridge.png)
First, we change the FORWARD chain policy from DROP to ACCEPT using the command: `$ iptables -t filter -P FORWARD ACCEPT` .

Then, we ping from `ns1` to `ns2` again. This time, we observe that the two network namespaces can communicate successfully.

> `Conclusion`: From Scenario 1, we learned that the iptables FORWARD chain can effectively control the forwarding of packets passing through the br0 bridge


#### Scenario 2. `FORWARD` chain is `DROP`, disable `net.bridge.bridge-nf-call-iptables`

![Diagram: Scenario 2. FORWARD chain is DROP, disable net.bridge.bridge-nf-call-iptables](/images/iptables-docker-linux-bridge/11-iptables-docker-linux-bridge.png)
From Scenario 1, we learned that the state of the iptables FORWARD chain affects packet forwarding through the `br0` bridge. Is there a way to decouple iptables from our custom bridge so that the FORWARD chain doesn’t affect `br0`?

Yes, we can achieve this by adjusting the kernel parameter `net.bridge.bridge-nf-call-iptables` so that packets passing through the `br0` interface are not processed by iptables’ filter table.

- **Step 1****:** Use `$ iptables-save -t filter` to check the current iptables configuration.
- **Step 2****:** Set `net.bridge.bridge-nf-call-iptables` to `0` to prevent packets going through the `br0` bridge from being filtered by iptables.
- **Step 3****:** Ping from `ns1` to `ns2`.

> Conclusion: We can use the kernel parameter `net.bridge.bridge-nf-call-iptables` to control whether packets passing through a bridge bypass iptables’ filter table.

#### Scenario 3. `FORWARD` chain is `DROP`, enable `net.bridge.bridge-nf-call-iptables`, add custom rule

![Diagram: Scenario 3. FORWARD chain is DROP, enable net.bridge.bridge-nf-call-iptables, add custom rule](/images/iptables-docker-linux-bridge/12-iptables-docker-linux-bridge.png)


#### The count of packets
Besides the methods used in Scenario 1 and Scenario 2, are there any other ways to allow communication between ns1 and ns2 when the FORWARD chain policy is set to DROP and `net.bridge.bridge-nf-call-iptables` is enabled (set to 1)?

***Yes, we can add custom FORWARD rules ourselves!***

- Step 1，Add a FORWARD rule using the command `sudo iptables -t filter -I FORWARD 1 -j ACCEPT` This accepts all incoming packets and allows forwarding. The rule is inserted at the top, taking precedence over all Docker rules.
- Step 2，Set `net.bridge.bridge-nf-call-iptables` to `1` to ensure iptables affects packets passing through the `br0` bridge.
- Step 3，Check the current iptables configuration with `iptables-save -t filter`
- Step 4，Ping from `ns1` to `ns2`.

> `Conclusion`: Although the system’s default FORWARD chain policy is set to DROP, packet forwarding can still be enabled by adding custom FORWARD rules.


![Diagram: The count of packets](/images/iptables-docker-linux-bridge/13-iptables-docker-linux-bridge.png)
By the way, we can use the command `$ iptables-save -t filter -c` to view the packet and byte counters for each rule.


## Conclusion

In this chapter, we learned about the roles of netfilter and iptables, and observed that Docker modifies and adds many rules to the Filter Table. This causes our self-created bridge to be affected, preventing it from properly forwarding packets.

---
