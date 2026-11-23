---
title: "How IP and ARP Work in Linux: Addresses, Resolution and Packets"
description: "See how IP addressing and ARP really work in Linux: assign addresses to veth interfaces, inspect the ARP table, and capture ICMP and ARP packets with tcpdump."
slug: "how-ip-and-arp-work"
---

By Rao Shahzaib · DevOps

## Key TakeAway

On a Linux host, use the `Ping` command within different `Network Namespaces` to observe the complete transmission and reception process of `ICMP` packets, and gain a deeper understanding of how the Linux Kernel resolves the target MAC address through `ARP` packets.

By utilizing Namespace, VETH, and IP commands, implement and explore the operational mechanism of ARP in the Linux Kernel, mastering the core principles of Linux networking.


*P.S.* Before staring this journey, I recommend you to know the Network Namespace and VETH concepts, feel free to check out my earlier article: [Network Namespace and Virtual Ethernet (VETH)](/blog/linux-network-namespace-veth)


## Address Resolution Protocol (ARP)

### The Concept of ARP

ARP (Address Resolution Protocol) is a protocol used in IPv4 networks to map IP addresses to MAC addresses. It serves as an essential component in the interaction between the Network Layer (Layer 3) and the Data Link Layer (Layer 2) within the TCP/IP protocol stack. ARP is primarily used for communication between devices within a local area network (LAN).

#### Core Function

The main function of ARP is to solve the following problem:

Within the same local area network (LAN), when a device knows the destination's **`IP address`**, how can it obtain the corresponding **`MAC address`** in order to transmit packets at the Data Link Layer (Layer 2).

#### Key Characteristics

- **`Broadcast` and `Unicast`**: ARP requests are broadcast (sent to all devices on the network), while ARP replies are unicast (sent only to the requester).
- **Scope of Application**: ARP only works within the same subnet (Layer 2 network). Communication across different subnets relies on routers and Proxy ARP.
- **Protocol Layering**: ARP operates at the Data Link Layer (Layer 2) but serves the IP protocol at the Network Layer (Layer 3).
- **Security Issues**: ARP lacks authentication mechanisms, making it vulnerable to **ARP spoofing** attacks, where an attacker can forge MAC addresses to intercept or redirect network traffic.

#### How It Works

1. **ARP Request**
   - When Device A wants to communicate with Device B but only knows B’s IP address (e.g., 192.168.1.2), it `broadcasts` an **`ARP request`** packet to the local network.
   - The request packet includes:
   - The sender’s IP and MAC addresses.
   - The target IP address (e.g., 192.168.1.2).
   - The target MAC address field is left blank (usually filled with all `zeros`).
   - This broadcast packet is received by all devices on the same subnet.
2. **ARP Reply**
   - When Device B receives the ARP request and sees that the target IP matches its own, it sends back an **`ARP reply`** packet.
   - The reply contains B’s MAC address and is sent directly to Device A (`unicast`).
   - Upon receiving the reply, Device A stores the IP-MAC mapping in its **`ARP table`** (ARP cache) for future use.

### ARP Table

In Linux `network namespaces`, each namespace maintains its own separate ARP table. Therefore, ARP requests and replies are limited to the network interfaces within that specific namespace.

- Every device maintains an ARP table that stores the mappings between resolved IP addresses and their corresponding MAC addresses.
- ARP table entries have a limited lifetime; expired entries are removed and require a new ARP request to be sent.

## Experiment

### Setting Up the Experiment Environment – Network Namespace


If you'd like to try it out yourself, you can refer to the experimental environment I built using **Vagrant + VirtualBox + Ubuntu 24.04**.: [Notion page](https://app.notion.com/p/2348a3a7d9d480b7adbec6d6b613f703)


#### Creating Namespaces and VETH

In our host system, we will create two isolated network namespaces and connect them using a pair of virtual Ethernet (veth) interfaces. This setup simulates two virtual hosts on the same local network.

```bash
$ sudo ip netns add ns1
$ sudo ip netns add ns2
$ sudo ip link add veth1 type veth peer veth2
$ sudo ip link set netns ns1 dev veth1 name eth0
$ sudo ip link set netns ns2 dev veth2 name eth0
```

#### Assigning IP Addresses to VETH Interfaces

![Assigning IP Addresses to VETH Interfaces — screenshot](/images/how-ip-and-arp-work/01-screenshot-2025-07-18-2-02-57.png)

Using the following commands, we assign an IP address to the `eth0` interface in each network namespace, as shown in the figure on the left.

**Commands**

```bash
# Take ns2 for example

$ sudo ip netns exec ns2 bash

root@network-lab:/home/vagrant# ip link set dev eth0 up
root@network-lab:/home/vagrant# ip addr add 10.22.33.55/24 dev eth0
```


### 實驗 一: 查看 ARP Table

![實驗 一: 查看 ARP Table — screenshot](/images/how-ip-and-arp-work/02-screenshot-2025-07-18-2-11-49.png)


Here’s a breakdown of the steps shown in the left diagram:

1. **Check the ARP table in `ns1`:**
   - Initially, you’ll observe that there are no entries in the ARP table.
2. **Ping `ns2` from `ns1`:**
   - This tests whether `ns1` can communicate with `ns2`.
3. **Check the `ARP tables` in both `ns1` and `ns2` again:**
   - You will notice that `ns1`’s ARP table now contains a new entry with the following details:
   1. **IP Address:** `10.22.33.55`
   - This is the IPv4 address of the neighboring device, indicating your system recognizes that this IP is on the same network.
   2. **Device:** `dev eth0`
   - This means the system uses the `eth0` interface to communicate with `10.22.33.55`.
   3. **Link Layer Address (MAC Address):** `lladdr 8a:0d:df:ba:d4:1f`
   - This is the MAC address associated with the IP `10.22.33.55`, representing the physical address of the neighbor device.


### Experiment 2: Using tcpdump to Capture and Analyze How ICMP and ARP Work

This experiment will guide you through observing how the `ping` command communicates with a specified target (either a machine or a network namespace) and help you understand the underlying process of how the system locates the target.

You will gain insights into the ARP-related knowledge illustrated in the diagram below.

![Experiment 2: Using tcpdump to Capture and Analyze How ICMP and ARP Work — diagram](/images/how-ip-and-arp-work/03-arp-drawio.svg)

#### Flush ARP Table

![Flush ARP Table — screenshot](/images/how-ip-and-arp-work/04-screenshot-2025-07-18-2-27-35.png)

To understand the complete process, we can clear the ARP entries for a specific interface using the command:

```bash
ip neigh flush dev <interface_name>
```

This flushes the ARP cache on that interface, forcing the system to perform ARP resolution again on the next communication attempt.

The left image shows a comparison of the ARP table before and after clearing the entries.


#### Use `tcpdump` to record packets

![Use tcpdump to record packets — screenshot](/images/how-ip-and-arp-work/05-screenshot-2025-07-18-2-44-14.png)


Next, open two terminal windows and enter the `ns1` network namespace in both:

1. In the **`bottom window`** (as shown in the left image), run the command:
   ```bash
   $ tcpdump -vvvvnl -i eth0 -w arp_record
   ```


   This listens on the `eth0` interface, capturing all packets in verbose mode and writing them to the file `arp_record` — a `pcap` file you can analyze later with tools like Wireshark.

2. In the **`top window`**, use the `ping` command to send an ICMP packet from `ns1` to `ns2`. Before pinging, make sure the ARP table is cleared so the ARP process will be triggered fresh.


#### Understand How ARP Works - 1 - ARP Request

Here is the `arp_record` pcap file captured by tcpdump, which can be analyzed using Wireshark for detailed inspection.

![Understand How ARP Works - 1 - ARP Request — screenshot](/images/how-ip-and-arp-work/06-screenshot-2025-07-18-3-20-11.png)

When you ping a specific IP address (for example, `10.22.33.55` of `ns2` in this experiment), but there is no corresponding MAC address entry for that IP in your own namespace (`ns1`) ARP table, the kernel triggers the ARP request process. Here's a brief explanation of that process:

1. **Check the ARP Table**

   When you issue the `ping` command, the kernel first checks the local ARP table to see if there is already a MAC address associated with the target IP. If there is, it directly uses that MAC address to send the data packet.

2. **ARP Request Broadcast**

   If the ARP table has no entry for the target IP, the kernel sends an ARP request.


   - This is a broadcast packet sent to all devices on the same network, asking "Who has this IP address?" (`Who has <target IP>?`).
   - The ARP request contains the sender’s IP and MAC addresses, along with the target IP address.
   - Because it is a broadcast, the destination MAC address is set to `ff:ff:ff:ff:ff:ff`.
3. **ARP Reply**

   The device that owns the target IP responds with an ARP reply, providing its MAC address to the requester. This reply is unicast directly back to the sender.

4. **Update the ARP Table**

   Upon receiving the ARP reply, the kernel updates the local ARP table by adding the target IP and its corresponding MAC address. This entry is then used for subsequent data transmissions (such as sending the ICMP echo request to complete the ping).


#### Understand How ARP Works - 2 - ARP Reply

![Understand How ARP Works - 2 - ARP Reply — screenshot](/images/how-ip-and-arp-work/07-screenshot-2025-07-18-3-20-17.png)

Upon receiving the ARP broadcast, `ns2`—which owns the IP address `10.22.33.55`—will reply with an ARP reply, providing its MAC address to the sender. This reply is a unicast packet, sent directly back to the requester.

#### ICMP Packet

Through the ARP mechanism described earlier, the target’s MAC address is resolved and completed, allowing the formation of a complete ICMP packet that can be transmitted successfully.

![ICMP Sender](/images/how-ip-and-arp-work/08-icmp-sender.png)

![ICMP Replier](/images/how-ip-and-arp-work/09-icmp-replier.png)

## Conclusion


This article demonstrates how to use Network Namespace, VETH virtual devices, and IP commands on a Linux host to observe the transmission and reception of ICMP packets via the Ping command.


It further explores how the Linux Kernel resolves the MAC address corresponding to a target IP address through the ARP (Address Resolution Protocol). ARP's primary function is to map network layer IP addresses to data link layer MAC addresses, achieved through broadcasting ARP requests and receiving unicast ARP responses.
