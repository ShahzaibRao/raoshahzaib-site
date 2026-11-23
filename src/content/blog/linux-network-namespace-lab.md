---
title: "Linux Network Namespace Lab: A Complete Hands-On Guide"
description: "A full hands-on Linux network namespace lab: veth pairs, bridges, routing, and ARP experiments that connect a namespace to the host, the bridge, and beyond."
slug: "linux-network-namespace-lab"
---

By Rao Shahzaib · DevOps

---

## **Linux Network Namespace Lab – Full Guide (Routing & ARP Experiments)**

**Lab Goals:**

1. Understand routing inside a network namespace (`ns1`).
2. Learn ARP behavior when using a Linux bridge.
3. Explore communication to the host (`eth0`) and external networks (Google DNS).
4. Learn how to use a bridge (`br0`) as a gateway.

**Requirements:**

- Ubuntu 24.04 or later
- Root privileges
- `iproute2` tools (`ip`, `arp`)

---

### **Step 0: Verify your environment**

Check existing network namespaces and interfaces:

```bash
ip netns list
ip link show

```

Expected: Usually no extra namespaces exist yet.

---

### **Step 1: Create a Network Namespace**

```bash
sudo ip netns add ns1

```

**Explanation:**

- `ns1` is a separate L3 (IP) environment.
- Interfaces inside ns1 are isolated from the host.

Check:

```bash
sudo ip netns list

```

Expected output:

```txt
ns1

```

---

### **Step 2: Create a Virtual Ethernet Pair**

```bash
sudo ip link add veth1 type veth peer name veth2

```

**Explanation:**

- `veth1` → stays on the host.
- `veth2` → will be moved into `ns1`.
- These act like two ends of a pipe.

Check interfaces:

```bash
ip link show

```

Expected: `veth1` and `veth2` appear.

---

### **Step 3: Move one end into ns1**

```bash
sudo ip link set veth2 netns ns1

```

- `veth2` is now inside `ns1`.
- Check inside ns1:

```bash
sudo ip netns exec ns1 ip link show

```

Expected: Only `lo` and `veth2` are present.

---

### **Step 4: Create a Linux Bridge on Host**

```bash
sudo ip link add br0 type bridge
sudo ip link set veth1 master br0
sudo ip link set veth1 up
sudo ip link set br0 up

```

**Explanation:**

- `br0` connects host and namespace at Layer 2 (Ethernet).
- `veth1` is attached to bridge.

Check:

```bash
brctl show   # If brctl installed
ip link show

```

Expected: `veth1` is enslaved to `br0`.

---

### **Step 5: Configure ns1 interface**

Rename `veth2` to `eth0` inside ns1 and assign IP:

```bash
sudo ip netns exec ns1 ip link set veth2 name eth0
sudo ip netns exec ns1 ip link set eth0 up
sudo ip netns exec ns1 ip addr add 10.22.33.4/24 dev eth0

```

Assign IP to bridge:

```bash
sudo ip addr add 10.22.33.1/24 dev br0

```

Check connectivity:

```bash
sudo ip netns exec ns1 ping 10.22.33.1

```

✅ Ping should succeed → ns1 ↔ br0 connected.

---

### **Step 6: Try to ping host eth0 (different subnet)**

```bash
sudo ip netns exec ns1 ping 172.16.0.2

```

Expected:

```txt
Network is unreachable

```

**Reason:** ns1 does not know how to reach 172.16.0.2.

---

### **Step 7: Add direct route inside ns1**

```bash
sudo ip netns exec ns1 ip route add 172.16.0.2/32 dev eth0
sudo ip netns exec ns1 ping 172.16.0.2

```

Observation: Ping **hangs**.

Check ARP table inside ns1:

```bash
sudo ip netns exec ns1 arp -n

```

- IP maps to MAC of **br0**, not Host eth0.

**Explanation:** Linux kernel treats 172.16.0.2 as local, sends ARP → br0 responds because it’s in same kernel namespace.

---

### **Step 8: Add return route on host**

```bash
sudo ip route add 10.22.33.0/24 dev br0

```

- This allows host to route packets back to ns1.

Test ping again:

```bash
sudo ip netns exec ns1 ping 172.16.0.2

```

✅ Ping now succeeds.

**Concept Learned:** Both sides must have routes configured.

---

### **Step 9: Test access to external network (Google DNS)**

1. Test ping from host:

```bash
ping 8.8.8.8

```

✅ Should succeed.

1. Test ping from ns1:

```bash
sudo ip netns exec ns1 ping 8.8.8.8

```

❌ Will fail: `Network is unreachable`

Reason: ns1 does not know how to reach external network.

---

### **Step 10: Set bridge as gateway inside ns1**

```bash
sudo ip netns exec ns1 ip route add default via 10.22.33.1 dev eth0

```

- 10.22.33.1 → IP of br0 (gateway for ns1).

Test ping:

```bash
sudo ip netns exec ns1 ping 8.8.8.8

```

- ICMP requests reach host, but ICMP replies may not come back yet.

---

### **Step 11: Enable IP forwarding on host**

```bash
sudo sysctl -w net.ipv4.ip_forward=1

```

- This allows host to forward packets between ns1 and external network.

Optional: Set up NAT so ns1 can access internet:

```bash
sudo iptables -t nat -A POSTROUTING -s 10.22.33.0/24 -o eth0 -j MASQUERADE

```

Test ping again:

```bash
sudo ip netns exec ns1 ping 8.8.8.8

```

✅ Ping should now succeed.

---

### **Step 12: Check ARP table in ns1**

```bash
sudo ip netns exec ns1 arp -n

```

- Entry for `10.22.33.1` shows MAC of br0.
- Entry for external IP (8.8.8.8) cannot be resolved → requires gateway.

---

### **Step 13: Monitor traffic**

Use tcpdump to see packets:

```bash
sudo tcpdump -i br0 icmp
sudo ip netns exec ns1 ping 172.16.0.2

```

- Observe ICMP request/reply.
- ARP requests and responses visible on br0.

---

### **Step 14: Cleanup lab**

```bash
# Delete namespace
sudo ip netns delete ns1

# Delete bridge
sudo ip link set br0 down
sudo ip link delete br0 type bridge

# Delete veth interfaces
sudo ip link delete veth1 type veth

```

✅ Lab environment is clean.

---

### **Key Concepts Learned**

1. **Network namespaces** isolate L3 environments.
2. **Veth pairs** connect namespaces to host.
3. **Bridges** forward Ethernet frames.
4. **Routing tables** must exist at all nodes for successful communication.
5. **ARP behavior**: bridge responds on behalf of local IPs in the kernel.
6. **Gateways** required for inter-subnet or external network traffic.
7. **IP forwarding + NAT** allows namespace to access the internet.

---

I can also **make a full diagram showing ns1, veth pair, br0, host eth0, routes, and gateways** — this will visually explain everything in one view like the original article.

Do you want me to make that diagram too?

---
