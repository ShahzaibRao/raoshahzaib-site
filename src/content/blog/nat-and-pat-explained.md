---
title: "NAT and PAT Explained: A Brief Discussion of Network Address Translation"
description: "What NAT and PAT are, how static NAT, dynamic NAT, and port address translation differ, and why address translation exists, with diagrams and real examples."
slug: "nat-and-pat-explained"
---

By Rao Shahzaib · DevOps

## Key Takeaway

> In this chapter, we begin by discussing and exploring why, in the experiments from previous chapters, we were unable to successfully ping Google DNS from a self-created network namespace. This issue leads us to the main topic of this chapter: **`Network Address Translation (NAT)`**, along with an explanation of its various types and **`Port Address Translation (PAT)`**.

> In the next chapter, we will conduct hands-on experiments using `iptables` to learn about **`SNAT`**, **`DNAT`**, and **`Conntrack`**, among other key concepts. Therefore, understanding NAT and PAT will serve as essential prerequisite knowledge for the upcoming chapter.

## The Previous Issue – Why couldn’t we successfully ping Google DNS from a self-created network namespace?

In a previous article ([5. Understand Linux Routing System - Part 2](/blog/linux-routing-system-part-2)  ), we left an open question. We attempted to send a ping from our self-created network namespace `ns1` to an external network service, Google DNS. However, we observed that while the ICMP Echo Request packets were successfully sent, the ICMP Echo Reply packets never arrived.

![Diagram: The Previous Issue – Why couldn’t we successfully ping Google DNS from a self-created network namesp](/images/nat-and-pat-explained/01-nat-and-pat-explained.svg)

To better understand this issue, let’s break down the **ping flow** step by step.

### Ping Flow

![Diagram: Ping Flow](/images/nat-and-pat-explained/02-nat-and-pat-explained.svg)
We will use the diagram below to illustrate the packet flow of a ping command:

- The **`WAN (Wide Area Network)`** in the diagram represents the external public network.
- `203.0.113.9` represents a machine in the WAN that is on the same subnet as our Linux host.
- `203.0.113.123` represents a machine in the WAN that is on the same subnet as Google DNS.
- In addition to our architecture diagram, there is an **`ICMP Packet`** section below that shows the contents of the ICMP packet at each step along the arrows.


#### ICMP Echo Request 1 - `ns1` to `br0`

![Diagram: ICMP Echo Request 1 - ns1 to br0](/images/nat-and-pat-explained/03-nat-and-pat-explained.svg)
When we initiate a ping from `ns1` to Google DNS, the ICMP Request packet travels through the virtual `eth0` interface and enters the `br0` bridge. At this point, the contents of the ICMP packet are as shown in the diagram.

#### ICMP Echo Request 2 - `br0` to `wan (203.0.113.12)`

![Diagram: ICMP Echo Request 2 - br0 to wan (203.0.113.12)](/images/nat-and-pat-explained/04-nat-and-pat-explained.svg)
Next, as the packet travels from `br0` to the host’s `eth0`, this segment is handled within the same kernel network namespace, so it can be considered internal kernel processing.

For the segment from the host’s `eth0` to a machine in the WAN, **assuming no additional mechanisms or external assistance**, the ICMP packet’s **`Source`** and **`Destination IP addresses`** **remain unchanged**. This ensures that the packet knows where to send the reply. What does change, however, is the **MAC address**.


#### ICMP Echo Request 3 - `wan (203.0.113.123)`  to Google DNS

![Diagram: ICMP Echo Request 3 - wan (203.0.113.123)  to Google DNS](/images/nat-and-pat-explained/05-nat-and-pat-explained.svg)
Next, the ICMP Request packet may traverse multiple routers within the WAN and eventually reach Google DNS, hypothetically arriving from the machine with IP address `203.0.113.123`. At this point, the contents of the ICMP packet are as shown in the diagram.

#### ICMP Echo Reply

![Diagram: ICMP Echo Reply](/images/nat-and-pat-explained/06-nat-and-pat-explained.svg)
When the Google DNS host receives the ICMP Request packet, it sends back an ICMP Reply packet. However, we notice that the **Destination IP** of the reply is `10.22.33.4`—a private IP within our internal network.

Since no one on the public network knows where this IP resides, the packet cannot be delivered to the correct destination and is ultimately **dropped during routing**.

### Restating Our Issue

Based on the ping flow above, we can now describe our issue more precisely.

> Can’t route back to my host since nobody knows how to route according to the Destination IP (10.22.33.4)

### An Idea to solve the problem…

![Diagram: An Idea to solve the problem…](/images/nat-and-pat-explained/07-nat-and-pat-explained.svg)
> So, can we modify the **Destination IP** of the ICMP Reply packet—originally `ns1`’s IP (`10.22.33.4`)—to the host’s `eth0` IP (`203.0.113.2`), so that the ICMP Reply can be routed from the external network to our Linux host, and then forwarded internally back to `ns1`?

This is a good idea, but…

- **How can we modify the Source IP address of the ICMP Request packet?**
- **Who has the ability to perform this modification?**
- **How can we keep track of these changes so that the ICMP Reply packet arriving at the host can be correctly updated back to the original** **`ns1`** **IP?**

## **Network Address Translation (NAT)**

### What is NAT?

NAT (Network Address Translation) is a networking technology used to translate IP addresses from one network to another. It is commonly implemented on routers or gateways to help private networks—such as home or corporate networks—connect to public networks like the Internet.

Simply put, NAT acts as a **`middleman`**, translating your private IP address into a public IP address so that your devices can communicate with external networks.

As illustrated in the diagram below, when an ICMP Request packet is sent from a host inside a LAN, it may pass through numerous routers before reaching the public WAN. To ensure that the packet can successfully return to its original sender (`172.16.0.7` in this example), each router along the path performs **Source IP Address translation (SNAT)**. This allows the packet to be correctly routed through a different network while keeping track of its origin.

Thanks to NAT, when the ICMP Reply packet is sent back, each router applies the corresponding NAT translation, allowing the reply to ultimately reach the correct original sender (the host).

![Diagram: What is NAT?](/images/nat-and-pat-explained/08-nat-and-pat-explained.svg)

It is recommended to watch the following YouTube videos to gain a better understanding of NAT

- [Network Address Translation - CompTIA Network+ N10-009 - 2.1](https://youtu.be/UILwCNOC5EI?si=0JL3rSZsGa9f3Hy0)
- [How does NAT conserve IP Address Space? (and why!) - Network Address Translation](https://youtu.be/BgtORKB0lls?si=aSS6Vlqf6EASCXX6)

### Advantages and Disadvantages

#### Advantages of NAT

1. **IP Address Conservation**: Allows multiple devices to share a single public IP.
2. **Enhanced Security**: External networks cannot directly see the private IPs of internal devices, reducing the risk of attacks.
3. **Flexibility**: Internal networks can freely use private IPs without conflicting with external networks.

#### Disadvantages of NAT

1. **Increased Complexity**: NAT adds complexity to network configuration and may cause connection issues for certain applications (e.g., P2P apps).
2. **Latency**: The translation process can introduce slight delays.
3. **Not Suitable for Some Protocols**: NAT breaks the end-to-end principle, causing challenges for applications like VoIP, online gaming, and P2P. Additional protocols (STUN, TURN, UPnP) are often required to allow external devices to connect directly to internal devices.

### Type of Network Address Translation

Based on the video ([NAT vs PAT, Static vs Dynamic -- demystified! -- Network Address Translation](http://youtube.com/watch?si=vr4uBFd22cuzgz3t&v=KA56kj23RPU&feature=youtu.be)), we can summarize four key concepts:

- **NAT**: Network Address Translation that only modifies the `L3 (IP address)` header.
- **PAT**: Network Address Translation that modifies both the `L3 (IP address)` and `L4 (Port Number)` headers.
- This is the most common type of NAT, also called **many-to-one NAT**.
- Multiple private IPs share a single public IP, distinguished by different port numbers.
- Example: Home routers typically use PAT to allow multiple devices to share one public IP.
- **Static**: The administrator explicitly defines the mapping between pre-translation and post-translation addresses.
- **Dynamic**:
- Pre-translation attributes are defined by the administrator.
- Post-translation attributes are assigned dynamically by the translation device.

These four concepts ultimately form four possible combinations, as shown below.

#### **Static NAT**

> Explicit mapping between IP address and another IP address<br /><br />Ref: [Static NAT - Network Address Translation](https://youtu.be/fm_NLOCi1Ns?si=JShs8kvAyg6J5sHQ)

- It makes internal resources external accessible
- **Bidirectional**
- Packets are translated whether initiated by `Internal` or `External` host
- **What content be translated ?**
- Inbound packet: Destination IP address is translated
- Outbound packet: Source IP address is translated
- **Does not conserve any address**
- Each internal IP requires a corresponding public IP. Even if an internal IP is not actively in use, its public IP is still **reserved** for it. Therefore, IP addresses cannot be **reused**, and there is no conservation benefit.

#### **Static PAT**

> Explicit mapping between IP:Port and another IP:Port<br /><br />Ref: [Static PAT - Network Address Translation](https://youtu.be/Q2XEoBEKrso?si=jFMmXGm7oz9rdSmG)

- It makes internal resource ports externally accessible
- Port Forwarding and Hole Punching
- **Bidirectional**
- Multiple internal servers can use on public IP address

#### **Dynamic PAT**

> Administrator defines set of  PRE-translation and POST-translation attributes

> Devices determines actual POST-translation `IP address` and `Port`<br /><br />Ref: [Dynamic PAT - Network Address Translation](https://youtu.be/2t8-WRZWCq8?si=_BAoUuOxSEh2HIQQ)

- **`Many-to-One`** or **`One-to-Many`** **Translation**
- Multiple internal private IPs can share a single public IP.
- Sometimes referred to as **“Many to One”** or **“One to Many”**:
- **Many to One**: From the internal network’s perspective toward the router, many internal devices map to a single shared public IP on the router.
- **One to Many**: From the router’s perspective outward, one shared public IP maps to many external devices.
- ***This provides the greatest potential for IP address conservation.***
- Different internal connections are distinguished using TCP/UDP **ports**.
- Supports around **65,000 concurrent connections per shared IP**.
- **Source port re-randomized**
- **Avoid Port Collisions**
- Multiple internal hosts may use the same internal source port.
- If PAT directly uses the internal port, two internal hosts could map to the same public port, causing connection conflicts.
- Reassigning (randomizing) ports ensures that each connection has a unique public port.
- **Enhance Security**
- Randomizing ports reduces the likelihood that an attacker can guess active connection ports.
- Using fixed ports for every connection makes them easier to scan or attack.
- **Maintain Connection Consistency**
- Each NAT table entry must be unique:
      ```txt
      (Public IP, Public Port) ↔ (Private IP, Private Port)
      ```
- Re-randomization ensures mappings do not conflict, keeping connections safe even if internal ports are identical.
- **Unidirectional**
- Traffic must be initiated from `internal` hosts
- If traffic be initiated by the Outside host, it will be dropped because no translation entry exists

#### **Dynamic NAT**

> Administrator defines set of  PRE-translation and POST-translation attributes

> Devices determines actual POST-translation `IP address`<br /><br />Ref: [Dynamic NAT - Network Address Translation](https://youtu.be/4DKQ3WnVcS4?si=G7-cEFPQPEqcT7m7)

- **Ports are not translated**
- Multiple devices cannot share IP addresses
- If there are four machines on the internal network but the router only provides three public IP addresses, then **at least one machine will be unable to be assigned a public IP**, no matter what.
- **Use Cases**
- Bidirectional while connection is active
- Lazy Static NAT
- But only if the number of hosts is equal to the number of Public IP addresses in translation
- **Non deterministic IP assignments**
- **Dynamic NAT** is a **many-to-many** or **one-to-one mapping from a** **`limited IP pool`**
- Internal private IPs require a temporary public IP to access the Internet.
- The NAT router assigns an available public IP from the IP pool.
- The mapping is temporary; the public IP may be released once the connection ends.
- The next connection may be assigned a different IP from the pool.
- Dynamic NAT does not provide fixed mappings. Each connection is assigned based on the **available IPs in the pool at that moment**, making it unpredictable which IP will be assigned next.

|  | Dynamic NAT | Static NAT |
| --- | --- | --- |
| IP Assignment | Non-deterministic | Deterministic |
| Mapping Duration | During connection | Permanent |
| IP Conservation | Yes | No |

### Four Types of One to Many NAT (Dynamic PAT)

The following four NAT types typically appear in **PAT (Port Address Translation)** scenarios. Since PAT is inherently a **many-to-one** or **one-to-many** NAT, it allows multiple internal devices to share a single public IP while distinguishing connections via different ports. These NAT types describe how the router handles port mappings and external connection restrictions:

- **`Full-Cone`**, **`Address-Restricted`**, and **`Port-Restricted NAT`** use fixed mappings (a single public IP:port corresponds to an internal IP:port) but differ in the level of access restriction.
- **`Symmetric NAT`** uses dynamic mappings, generating a new public IP:port for each connection, making it more complex.

#### Full-Cone NAT

![Diagram: Full-Cone NAT](/images/nat-and-pat-explained/09-nat-and-pat-explained.svg)

- **Definition**
- Full-Cone NAT is the most open type of NAT. The private IP and port of an internal device (e.g., `192.168.1.2:5000`) are mapped to a fixed public IP and port (e.g., `203.0.113.1:5000`). Once this mapping is established, **any external host** can directly communicate with the internal device through this public IP and port, without additional restrictions.
- **Characteristics**
- External hosts can initiate communication without first receiving packets from the internal device.
- This type of NAT imposes the fewest restrictions on external connections, making it suitable for applications that require high connectivity (e.g., certain P2P applications).
- **Advantages**
- Simple connection setup; external devices can easily connect to internal devices.
- Suitable for services that need to be publicly accessible (e.g., servers).
- **Disadvantages**
- Lower security, since any external host can send data to the mapped port.
- **Use Cases**
- Server hosting (e.g., game servers).

**Additional Material**

- [stunmesh-go](https://github.com/tjjh89017/stunmesh-go/): STUNMESH is a Wireguard helper tool to get through Full-Cone NAT.
- [Presented STUNMESH-go at COSCUP 2025 for P2P Wireguard connections \| Date Huang posted on the topic \| LinkedIn](https://www.linkedin.com/posts/tjjh89017_stunmesh-go-wireguard-nat%E7%A9%BF%E9%9A%A7%E5%B7%A5%E5%85%B7%E7%9A%84%E6%BA%90%E8%B5%B7%E8%88%87%E4%BB%8B%E7%B4%B9-activity-7360651167233662976-45la?utm_source=share&utm_medium=member_desktop&rcm=ACoAACJjqQcBGqAspX509zNBfgsiQrOiWrWGpXE)
- [STUNMESH-go: Wireguard NAT穿隧工具的源起與介紹](https://speakerdeck.com/tjjh89017/stunmesh-go-wireguard-natchuan-sui-gong-ju-de-yuan-qi-yu-jie-shao)

#### Address Restricted Cone NAT

![Diagram: Address Restricted Cone NAT](/images/nat-and-pat-explained/10-nat-and-pat-explained.svg)

- **Definition**
- In this NAT type, an internal device’s private IP and port are mapped to a public IP and port, but only after the internal device **sends data to a specific external host IP** can that external host reply through the same public IP and port.
- Restriction: The external host’s IP must match the destination IP that the internal device previously contacted, but the port number is unrestricted.
- **Characteristics**
- More secure than Full-Cone NAT because only external IPs that the internal device has actively contacted can send data back.
- The external host can use **different ports** to return data.
- **Advantages**
- Safer than Full-Cone NAT by limiting unauthorized external connections.
- Still allows some flexibility (no restriction on external port numbers).
- **Disadvantages**
- Requires the internal device to initiate the connection.
- Not suitable for scenarios where external hosts need to initiate connections.
- **Use Cases**
- Certain P2P applications (e.g., BitTorrent).
- Scenarios requiring moderate security for incoming connections.

#### Port Restricted Cone NAT

![Diagram: Port Restricted Cone NAT](/images/nat-and-pat-explained/11-nat-and-pat-explained.svg)

- **Definition**
- This is a stricter NAT type. An internal device’s private IP and port are mapped to a public IP and port, but only after the internal device **sends data to a specific external host IP and port** can that external host reply to the same public IP and port.
- Restriction: Both the external host’s IP and port must match the destination that the internal device previously contacted.
- **Characteristics**
- Stricter than Address-Restricted Cone NAT because it restricts both IP **and** port.
- Higher security but lower connection flexibility.
- **Advantages**
- Provides stronger security, reducing the risk of unauthorized connections.
- **Disadvantages**
- Strict connection restrictions may require additional configuration for some P2P applications (e.g., UPnP or manual port forwarding).
- **Use Cases**
- Common NAT type in home routers.
- Environments that require high security.

#### Symmetric NAT

![Diagram: Symmetric NAT](/images/nat-and-pat-explained/12-nat-and-pat-explained.svg)

- **Definition**
- Symmetric NAT is the strictest NAT type. Each outbound connection from an internal device (to different external IPs or ports) generates a unique public IP and port mapping. In other words, an internal device’s private IP and port are mapped dynamically and independently for each external target.
- Restriction: Only external IPs and ports actively contacted by the internal device can send data back, and the return must use the **same public IP and port mapping** as the original connection.
- **Characteristics**
- Each external connection has a separate mapping; external hosts cannot predict or reuse previous mappings.
- Provides the highest security but is least friendly for P2P applications.
- **Advantages**
- Extremely high security, as external hosts can hardly connect directly to internal devices.
- **Disadvantages**
- P2P connections are very difficult, often requiring intermediate servers (STUN/TURN) for NAT traversal.
- Configuration is complex and may require additional technologies (e.g., UPnP or manual port forwarding).
- **Use Cases**
- Enterprise networks with high security requirements.
- Environments with strict firewall policies.

#### Impact on P2P Applications

These NAT types significantly affect peer-to-peer (P2P) connectivity:

- **Full-Cone NAT**: Easiest for establishing P2P connections, as external hosts can directly access the mapped ports.
- **Address-Restricted** and **Port-Restricted NAT**: Require the internal device to initiate the connection first. P2P applications may need **`STUN`** (Session Traversal Utilities for NAT) to facilitate NAT traversal.
- **Symmetric NAT**: Most difficult for P2P connections, as each connection has a unique mapping. Typically requires a **`TURN`** (Traversal Using Relays around NAT) server to relay data.

## Conclusion

In this chapter, we revisited the issue left over from the previous Network Namespace experiment and used the **ping flow** to understand the root cause.

We then explored NAT in more depth, examining how it works and why it can resolve our problem.

In the next chapter, we will study concepts such as **`SNAT`**, **`DNAT`**, and **`Conntrack`**, and conduct hands-on experiments using **`iptables`** and **`Docker`** to observe and manipulate them in practice.


---
