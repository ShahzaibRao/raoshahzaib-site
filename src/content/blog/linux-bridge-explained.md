---
title: "Linux Bridge Explained: How a Virtual Switch Connects Namespaces"
description: "Learn how a Linux bridge forwards frames like a virtual switch: build a bridge lab, trace ARP and ICMP across namespaces, and watch the FDB learn MAC addresses."
slug: "linux-bridge-explained"
---

By Rao Shahzaib · DevOps

## Key Takeaway

In this article, we explore how multiple network namespaces can communicate with each other through a `Linux Bridge`, using visual guides and hands-on experiments (with the `ping` command).

With a Linux Bridge, communication becomes possible between isolated or independent environments without the need to establish point-to-point connections for each one.

## Linux Bridge

### Introduction

A **`Linux Bridge` **is a `virtual` network device implemented within the Linux kernel that enables Layer 2 (Data Link Layer) packet forwarding between multiple network interfaces on the same host—similar to a physical switch.

It is primarily used to bridge different network interfaces—such as virtual machines, containers, or physical network interfaces—allowing them to communicate within the same Layer 2 broadcast domain.

#### **How It Works**

- A **Linux Bridge** functions as a software-based switch and operates via the Linux kernel’s [bridge module](https://github.com/torvalds/linux/tree/master/net/bridge).
- When a packet arrives at the bridge, it checks the `destination MAC address` and consults its internal forwarding table:
  - If the destination MAC is known, the packet is forwarded to the corresponding interface.
  - If unknown, the packet is broadcast to all bridged interfaces (except the one it came from).
- The bridge supports the **`Spanning Tree Protocol (STP)`** to prevent network loops and ensure network stability.

#### **Practical Use Case**

Imagine you have a server running multiple virtual machines that need to communicate with the external network:

1. Create a Linux bridge (e.g., `br0`).
2. Add the host's physical network interface (`eth0`) and the virtual machines' network interfaces (`vnet0`, `vnet1`) to `br0`.
3. Assign an IP address to `br0` if Layer 3 communication is required.
4. Now, the virtual machines can communicate with the external network through `br0` and with each other directly.

#### **Userspace Tools**

- **bridge-utils**: Contains the legacy `brctl` tool. Source code is available in the [bridge-utils repository](https://www.linuxfromscratch.org/blfs/view/svn/basicnet/bridge-utils.html).
- **iproute2**: A modern network configuration suite. Source code can be found in the [iproute2 repository](https://git.kernel.org/pub/scm/network/iproute2/iproute2.git/).

### Forwarding Database (FDB)

#### Introduction

The **`Forwarding Database (FDB)`** plays a key role in a Linux Bridge by keeping track of each `connected device’s MAC address` and the `specific interface (port)` it is associated with. When the bridge receives an Ethernet frame, it consults the FDB to determine how to forward the packet:

- If the destination MAC address exists in the FDB, the packet is forwarded to the corresponding interface.
- If the destination MAC address is not found in the FDB, the packet is **`flooded`** to all bridged interfaces (except the source interface).
- The FDB also supports **`dynamic learning`** and **`aging`**, ensuring the table stays current and efficient.
**Aging Time**

  ## Aging Time

  ### Introduction

  In a **Linux Bridge**, the **ageing time** refers to the maximum duration that a dynamically learned MAC address entry remains in the **Forwarding Database (FDB)** without being used—i.e., without seeing any related traffic.

  If no packets are received from a particular MAC address within this ageing time, the bridge considers the entry stale and removes it from the FDB to keep the table accurate and efficient.

  - **How It Works:**
    - When a bridge device (e.g., `br0`) receives a packet from an interface (e.g., `veth6`), it records the **source MAC address** and the **associated interface**, creating a dynamic FDB entry (e.g., `c6:e9:9b:3e:43:4a dev veth6 master br0`).
    - Each dynamic entry has an **ageing timer**. If no packets are received from that MAC address within the ageing time, the entry is removed to prevent the FDB from being cluttered with stale data.
    - The **`default` ageing time** is usually **`300 seconds` (5 minutes)**, but this value can be customized.
  - **Why Ageing Time Matters**:
    - **`Resource Efficiency`**: The FDB has limited capacity. Removing outdated entries conserves memory and system resources.
    - **`Network Adaptability`**: Devices may change interfaces or MAC addresses (e.g., during a container restart). The ageing mechanism ensures the FDB reflects the current network topology.
    - **`Avoiding Incorrect Forwarding`**: Keeping stale MAC entries could cause packets to be misrouted to interfaces that no longer exist or are inactive.
  - **Impact**:
    - For example, the dynamic entry `c6:e9:9b:3e:43:4a dev veth6 master br0 `will be subject to ageing. If no packets are sent or received via `veth6` during the ageing period, the entry may be removed.
    - **Static entries** (marked as `permanent`, e.g., `e6:42:3e:0e:65:6b dev veth6 master br0 permanent`) are **not affected** by ageing time because they are manually configured or fixed by the system.

  ### **How to Prevent or Extend Ageing Time**

  1. **Increase the Ageing Time**
     1. Extend the duration before dynamic entries expire.
        1. `echo 60000 > /sys/class/net/br0/bridge/ageing_time`
        2. `ip link set br0 type bridge ageing_time 600`
  2. **Convert Dynamic Entries to Static (Permanent)**
     1. Prevent specific MAC entries from being aged out. Manually set a MAC address as **permanent**:
        1. `bridge fdb add c6:e9:9b:3e:43:4a dev veth6 master permanent`
           1. Note: If the entry already exists as dynamic, you may need to delete it first before adding it as permanent.
  3. **Maintain Network Activity**
     1. Keep sending traffic through the interface periodically to reset the ageing timer and keep dynamic entries active.
  4. **Disable the Ageing Mechanism**
     1. Stop ageing entirely by setting the ageing time to `0`.
        1. `echo 0 > /sys/class/net/br0/bridge/ageing_time`
        2. `ip link set br0 type bridge ageing_time 0`

#### **Structure of the FDB**

The FDB is typically organized as a table with the following key fields:

- **MAC Address**:

  The 48-bit Ethernet MAC address of the device.

- **Interface (Port):**

  The bridge interface through which the MAC address was learned (e.g., `eth0`, `vnet0`).

- **Flags**:

  Indicate the type and behavior of the entry:


  - `self`: The entry belongs to the bridge device itself (e.g., multicast or the bridge’s own address).
  - `permanent`: A statically configured entry that will **not age out**.
  - *(No flag)*: Implies a **`dynamically learned`** entry, which is subject to ageing and will expire if inactive.

**Real FDB case**

This example assumes a Linux host running a virtualization environment, where a bridge device (`br0`) connects multiple network interfaces, including physical NICs and virtual network interfaces of virtual machines.

**Case Background**

Suppose you have a server running a Linux Bridge `br0`, which bridges the following interfaces:

- `eth0`: Physical network interface connected to the external network.
- `vnet0`: Virtual network interface for the first virtual machine.
- `vnet1`: Virtual network interface for the second virtual machine.

These interfaces form a Layer 2 network segment. The bridge maintains an FDB that maps each device’s MAC address to its corresponding interface. Assume VLANs are configured in the environment and some entries are statically set.

**Sample FDB Table**

Below is an example output of the `bridge fdb show` command, simulating the FDB content:

```txt
00:16:3e:12:34:56 dev eth0 vlan 10 self static
00:16:3e:78:90:ab dev vnet0 vlan 10
00:16:3e:ab:cd:ef dev vnet1 vlan 10
33:33:00:00:00:01 dev br0 self permanent
```

| **MAC Address** | **Port** | **VLAN ID** | Type | State |
| --- | --- | --- | --- | --- |
| 00:16\:3e\:12:34:56 | eth0 | 10 | Static | Active |
| 00:16\:3e\:78:90:ab | vnet0 | 10 | Dynamic | Active |
| 00:16\:3e\:ab\:cd\:ef | vnet1 | 10 | Dynamic | Active |
| 33:33:00:00:00:01 | br0 | - | Permanent | Active |

## Setting Up a Linux Bridge Test Environment

We will create four network namespaces and one Linux Bridge inside a single Linux host, connecting them via virtual ethernet interfaces. After setup, the network topology will look like the diagram below.

![Setting Up a Linux Bridge Test Environment — diagram](/images/linux-bridge-explained/01-linux-bridge-0-drawio.svg)

### 1. vagrant + virtualbox + ubuntu-24.04


If you'd like to try this yourself, you can refer to my experimental setup using Vagrant + VirtualBox + Ubuntu 24.04: [Notion page](https://app.notion.com/p/2348a3a7d9d480b7adbec6d6b613f703)


Once the environment is set up, you should see network information similar to the following

**ip information**

```bash
2025-07-22 13:30:09 ⌚  network-lab in ~
○ → ip -c a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host noprefixroute
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:71:19:d8 brd ff:ff:ff:ff:ff:ff
    altname enp0s8
    inet 10.0.2.15/24 metric 100 brd 10.0.2.255 scope global dynamic eth0
       valid_lft 79812sec preferred_lft 79812sec
    inet6 fd17:625c:f037:2:a00:27ff:fe71:19d8/64 scope global dynamic mngtmpaddr noprefixroute
       valid_lft 86235sec preferred_lft 14235sec
    inet6 fe80::a00:27ff:fe71:19d8/64 scope link
       valid_lft forever preferred_lft forever
3: eth1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:e9:f4:bb brd ff:ff:ff:ff:ff:ff
    altname enp0s9
    inet 172.17.8.222/24 brd 172.17.8.255 scope global eth1
       valid_lft forever preferred_lft forever
    inet6 fe80::a00:27ff:fee9:f4bb/64 scope link
       valid_lft forever preferred_lft forever
4: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN group default
    link/ether e2:d4:6e:59:2f:3a brd ff:ff:ff:ff:ff:ff
    inet 172.18.0.1/16 brd 172.18.255.255 scope global docker0
       valid_lft forever preferred_lft forever
```

### 2. Network Namespace

#### Create four Network Namespaces

```bash
$ sudo ip netns add ns1
$ sudo ip netns add ns2
$ sudo ip netns add ns3
$ sudo ip netns add ns4
```

#### Create four pairs of VETH interfaces

```bash
$ sudo ip link add veth0 type veth peer veth1
$ sudo ip link add veth2 type veth peer veth3
$ sudo ip link add veth4 type veth peer veth5
$ sudo ip link add veth6 type veth peer veth7
```

#### Attach VETH to Network Namespace and Assign IP Address

```bash
# Configure ns1
$ sudo ip link set netns ns1 veth1
$ sudo ip netns exec ns1 ip link s dev veth1 up
$ sudo ip netns exec ns1 ip addr add 10.22.33.7/24 dev veth1

# Configure ns2
$ sudo ip link set netns ns2 veth3
$ sudo ip netns exec ns2 ip link s dev veth3 up
$ sudo ip netns exec ns2 ip addr add 10.22.33.8/24 dev veth3

# Configure ns3
$ sudo ip link set netns ns3 veth5
$ sudo ip netns exec ns3 ip link s dev veth5 up
$ sudo ip netns exec ns3 ip addr add 10.22.33.9/24 dev veth5

# Configure ns4
$ sudo ip link set netns ns4 veth7
$ sudo ip netns exec ns4 ip link s dev veth7 up
$ sudo ip netns exec ns4 ip addr add 10.22.33.10/24 dev veth7
```

### 3. Linux Bridge

#### Create a Linux Bridge

Create a bridge named `br0` on the host.

```bash
$ sudo ip link add br0 type bridge
```


![Create a Linux Bridge — screenshot](/images/linux-bridge-explained/02-screenshot-2025-07-22-8-22-38.png)

#### Connect the veth interfaces to the Linux Bridge.

Connect the host’s veth interfaces to the `br0` Linux Bridge using the `master` interface setting.

```bash
$ sudo ip link set master br0 dev veth0
$ sudo ip link set master br0 dev veth2
$ sudo ip link set master br0 dev veth4
$ sudo ip link set master br0 dev veth6
```

After completion, you’ll see something like the image on the right— each veth interface now shows the `master br0` attribute.


![Connect the veth interfaces to the Linux Bridge. — screenshot](/images/linux-bridge-explained/03-screenshot-2025-07-22-8-44-19.png)

By the way, you can also use the legacy `brctl` command or the `bridge` command to check the bridge status.


![Connect the veth interfaces to the Linux Bridge. — screenshot](/images/linux-bridge-explained/04-screenshot-2025-07-22-8-51-28.png)

#### Bring interfaces up

Enable (bring up) all veth interfaces and the `br0` interface on the host

```bash
$ sudo ip link set dev veth0 up
$ sudo ip link set dev veth2 up
$ sudo ip link set dev veth4 up
$ sudo ip link set dev veth6 up
$ sudo ip link set dev br0 up
```
![Bring interfaces up — screenshot](/images/linux-bridge-explained/05-screenshot-2025-07-22-8-56-47.png)

The diagram above shows that all links are in the **`forwarding`** state, which means communication can now begin.


## Experiment Walkthrough

### Introduction

![Introduction — diagram](/images/linux-bridge-explained/06-linux-bridge-layer-drawio.svg)

### What happens after you run the ping command?

#### 1. ARP Request from ns1
In this experiment, we will initiate a `ping` command from network namespace `ns1` to `ns4`, using the Linux Bridge as an intermediary to forward the packets.

The diagram on the left provides a high-level view to help understand how the packets, components, and commands correspond to the layers of the OSI model.

![1. ARP Request from ns1 — diagram](/images/linux-bridge-explained/07-linux-bridge-1-drawio.svg)

#### 2. Flood ARP Request


If `ns1`’s ARP table does not have an entry for `ns4`’s IP address, it will first send an **`ARP Request`** packet through the Linux Bridge. The bridge then handles forwarding this request so that `ns1` can learn `ns4`’s MAC address before sending actual data packets.


![2. Flood ARP Request — diagram](/images/linux-bridge-explained/08-linux-bridge-2-drawio.svg)

#### 3. ARP Reply
If the Linux Bridge’s FDB also lacks an entry for `ns4`’s MAC address, it will **`flood`** the ARP request —broadcasting it out to all other interfaces except the one it was received on—so that `ns4` can receive the request and respond.


![3. ARP Reply — diagram](/images/linux-bridge-explained/09-linux-bridge-3-drawio.svg)

#### 4. ICMP Request
`ns4` replies with an ARP Reply, so the Linux Bridge updates its FDB with `ns4`’s MAC address and interface mapping. It then forwards the ARP Reply back to the original requester, `ns1`.

![4. ICMP Request — diagram](/images/linux-bridge-explained/10-linux-bridge-4-drawio.svg)

#### 5. ICMP Reply
At this point, `ns1` has all the necessary information and can send the ICMP Echo Request packet to the Linux Bridge, which will forward it to `ns4`.


![5. ICMP Reply — diagram](/images/linux-bridge-explained/11-linux-bridge-5-drawio.svg)

Similarly, the ICMP Reply from `ns4` will be forwarded back to `ns1` through the Linux Bridge.


## Let’s get started with the real experiment!

We will use the `ping` command inside the `ns1` environment to send ICMP packets to `ns4` and observe the process and results.

Before starting the experiment, let’s review the current environment. As shown in the diagram below, each network namespace is configured as follows.

![Let’s get started with the real experiment! — screenshot](/images/linux-bridge-explained/12-screenshot-2025-07-22-9-20-32.png)

### Analyzing the Forwarding Database (FDB) of the Linux Bridge device `br0`.

After completing the setup steps, before running the `ping` command, let’s analyze the current Forwarding Database (FDB) on the host.

We start by checking the FDB of `br0`— the MAC address table—which records the MAC addresses learned on each interface of the bridge, along with their corresponding ports, VLAN IDs, and related details.

```txt
$ bridge fdb show br0
33:33:00:00:00:01 dev eth0 self permanent
01:00:5e:00:00:01 dev eth0 self permanent
33:33:ff:71:19:d8 dev eth0 self permanent
01:80:c2:00:00:00 dev eth0 self permanent
01:80:c2:00:00:03 dev eth0 self permanent
01:80:c2:00:00:0e dev eth0 self permanent
33:33:00:00:00:01 dev eth1 self permanent
01:00:5e:00:00:01 dev eth1 self permanent
33:33:ff:e9:f4:bb dev eth1 self permanent
01:80:c2:00:00:00 dev eth1 self permanent
01:80:c2:00:00:03 dev eth1 self permanent
01:80:c2:00:00:0e dev eth1 self permanent
33:33:00:00:00:01 dev docker0 self permanent
01:00:5e:00:00:6a dev docker0 self permanent
33:33:00:00:00:6a dev docker0 self permanent
01:00:5e:00:00:01 dev docker0 self permanent
e2:d4:6e:59:2f:3a dev docker0 vlan 1 master docker0 permanent
e2:d4:6e:59:2f:3a dev docker0 master docker0 permanent
42:a3:b1:71:35:5c dev veth0 vlan 1 master br0 permanent
42:a3:b1:71:35:5c dev veth0 master br0 permanent
33:33:00:00:00:01 dev veth0 self permanent
01:00:5e:00:00:01 dev veth0 self permanent
33:33:ff:71:35:5c dev veth0 self permanent
8a:0d:df:ba:d4:1f dev veth2 vlan 1 master br0 permanent
8a:0d:df:ba:d4:1f dev veth2 master br0 permanent
33:33:00:00:00:01 dev veth2 self permanent
01:00:5e:00:00:01 dev veth2 self permanent
33:33:ff:ba:d4:1f dev veth2 self permanent
a6:21:69:7e:aa:bd dev veth4 vlan 1 master br0 permanent
a6:21:69:7e:aa:bd dev veth4 master br0 permanent
33:33:00:00:00:01 dev veth4 self permanent
01:00:5e:00:00:01 dev veth4 self permanent
33:33:ff:7e:aa:bd dev veth4 self permanent
e6:42:3e:0e:65:6b dev veth6 vlan 1 master br0 permanent
e6:42:3e:0e:65:6b dev veth6 master br0 permanent
33:33:00:00:00:01 dev veth6 self permanent
01:00:5e:00:00:01 dev veth6 self permanent
33:33:ff:0e:65:6b dev veth6 self permanent
33:33:00:00:00:01 dev br0 self permanent
01:00:5e:00:00:6a dev br0 self permanent
33:33:00:00:00:6a dev br0 self permanent
01:00:5e:00:00:01 dev br0 self permanent
33:33:ff:dc:15:1c dev br0 self permanent
16:f0:f3:dc:15:1c dev br0 vlan 1 master br0 permanent
16:f0:f3:dc:15:1c dev br0 master br0 permanent
```
**Analyze `veth0`**

- **42\:a3\:b1:71:35:5c**：The statically configured MAC address appears twice:
  - Once associated with VLAN 1 (`vlan 1 master br0 permanent`).
  - Once without VLAN information (`master br0 permanent`).
  - This is likely the MAC address of the `veth0` device, statically bound to the bridge.
- **33:33:00:00:00:01**：The `IPv6` multicast address (all-nodes multicast) is marked as `self permanent`, indicating it is a fixed multicast address handled by the bridge device itself.
- **01:00:5e:00:00:01**：The `IPv4` multicast address (all-hosts multicast) is likewise marked as `self permanent`, indicating it is a fixed multicast address managed by the bridge device itself.
- **33:33:ff:71:35:5c**：The `IPv6` solicited-node multicast address (derived from the last part of `42:a3:b1:71:35:5c`) is marked as `self permanent`. It is used for IPv6 `Neighbor Discovery Protocol (NDP)`.


**Analyze `br0`**

- **33:33:00:00:00:01**, **01:00:5e:00:00:01**：The bridge device’s own `IPv6` and `IPv4` multicast addresses.
- **01:00:5e:00:00:6a**, **33:33:00:00:00:6a**：Additional multicast addresses that may be associated with specific multicast groups (e.g., for certain protocols or services).
- **33:33:ff\:dc\:15:1c**：The bridge device’s `IPv6` solicited-node multicast address, generated based on `16:f0:f3:dc:15:1c`.
- **16\:f0\:f3\:dc\:15:1c**：The MAC address of the bridge device `br0` itself, statically configured, appearing both with and without VLAN 1 association.


### Let’s ping ns4 from ns1

As shown in the right diagram, in `ns2`, `ns3`, and `ns4`, we use `tcpdump -vvvvln -i <interface>` to monitor packets on each network namespace interface.


![Let’s ping ns4 from ns1 — screenshot](/images/linux-bridge-explained/13-screenshot-2025-07-22-9-54-15.png)

![Let’s ping ns4 from ns1 — screenshot](/images/linux-bridge-explained/14-screenshot-2025-07-22-9-55-33.png)

After successfully executing the `ping` command, we can observe that:

- `ns2` and `ns3` receive the ARP packets, but since the requested IP address (`Request who-has`) is not theirs, they do not respond.
- `ns4`, being the target, replies with an ARP Reply to inform `ns1`, then receives the ICMP packet from `ns1` and finally responds with the ICMP reply.


### Revisit br0’s Forwarding Database (FDB）

```txt
$ bridge fdb show br0
.
.
.
e6:28:92:72:f6:01 dev veth0 master br0
42:a3:b1:71:35:5c dev veth0 vlan 1 master br0 permanent
42:a3:b1:71:35:5c dev veth0 master br0 permanent
33:33:00:00:00:01 dev veth0 self permanent
01:00:5e:00:00:01 dev veth0 self permanent
33:33:ff:71:35:5c dev veth0 self permanent
8a:0d:df:ba:d4:1f dev veth2 vlan 1 master br0 permanent
8a:0d:df:ba:d4:1f dev veth2 master br0 permanent
33:33:00:00:00:01 dev veth2 self permanent
01:00:5e:00:00:01 dev veth2 self permanent
33:33:ff:ba:d4:1f dev veth2 self permanent
a6:21:69:7e:aa:bd dev veth4 vlan 1 master br0 permanent
a6:21:69:7e:aa:bd dev veth4 master br0 permanent
33:33:00:00:00:01 dev veth4 self permanent
01:00:5e:00:00:01 dev veth4 self permanent
33:33:ff:7e:aa:bd dev veth4 self permanent
c6:e9:9b:3e:43:4a dev veth6 master br0
e6:42:3e:0e:65:6b dev veth6 vlan 1 master br0 permanent
e6:42:3e:0e:65:6b dev veth6 master br0 permanent
33:33:00:00:00:01 dev veth6 self permanent
01:00:5e:00:00:01 dev veth6 self permanent
33:33:ff:0e:65:6b dev veth6 self permanent
33:33:00:00:00:01 dev br0 self permanent
01:00:5e:00:00:6a dev br0 self permanent
33:33:00:00:00:6a dev br0 self permanent
01:00:5e:00:00:01 dev br0 self permanent
33:33:ff:dc:15:1c dev br0 self permanent
16:f0:f3:dc:15:1c dev br0 vlan 1 master br0 permanent
16:f0:f3:dc:15:1c dev br0 master br0 permanent
```
After running the ping command, let's check if there are any changes in the `FDB`.

Since we focused on communication between `ns1` and `ns4`, we observe changes related to `veth0`, `veth6`, and `br0`:

- New entries with `master br0` appear for `veth0` and `veth6`:
  - When `veth0` sends ICMP packets to `veth6`, the Linux Bridge `br0` dynamically learns and records their MAC addresses in the FDB.
  - This way, the FDB contains MAC addresses for both `veth0` and `veth6`, enabling efficient forwarding of subsequent packets.


## Conclusion

In the previous article, we demonstrated communication using direct end-to-end VETH pairs. In this chapter, by leveraging the Linux Bridge, communication among multiple isolated environments becomes easier and more manageable.
