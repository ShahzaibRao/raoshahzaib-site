---
title: "Linux Network Namespaces and VETH Pairs Explained"
description: "Learn Linux network namespaces and virtual Ethernet pairs hands-on: create namespaces, link them with veth, and ping safely between isolated network stacks."
slug: "linux-network-namespace-veth"
---

By Rao Shahzaib · DevOps

## Key Takeaway

In this article, we will learn about the purpose of Linux Network Namespaces and how to enable communication between isolated Network Namespaces using Virtual Ethernet (VETH) pairs.

Finally, a simple hands-on experiment will guide you step by step to achieve the results described above.

![Key Takeaway — diagram](/images/linux-network-namespace-veth/01-veth-drawio.svg)

## Introduction of Linux Namespace

Linux namespaces are a core component of containerization technology. They provide resource isolation between processes and are widely used in containerization, virtualization, and security scenarios. By dividing system resources into separate namespaces, processes are restricted to accessing only the resources within their own namespace, preventing direct interference with resources in other namespaces. The following are the current types of namespaces:

- **Network Namespace**
  - Isolates network resources, including network interfaces, routing tables, firewall rules, etc.
  - **Use case:** Each container can have its own networking environment, such as a unique IP address and ports.
  - **Example:** Containers can run independent web servers bound to the same port (e.g., 80) without conflict.
- **UTS Namespace (UNIX Timesharing System)**
  - Isolates hostname and NIS domain name.
  - **Use case:** Containers can have their own hostnames, separate from the host or other containers.
  - **Example:** The `hostname` command inside a container returns a unique hostname.
- **User Namespace**
  - Isolates user and group ID mappings. It allows processes to run as root within a namespace while being mapped to an unprivileged user on the host.
  - **Use case:** Enhances container security by preventing root privileges inside the container from affecting the host.
  - **Example:** UID 0 (root) inside the container may be mapped to a non-root UID on the host.
- **IPC Namespace (Inter-Process Communication)**
  - Isolates IPC resources such as message queues, shared memory, and semaphores.
  - **Use case:** Ensures that IPC resources used within a container do not interfere with the host or other containers.
- **Cgroup Namespace**
  - Isolates the view of control groups (cgroups), so that processes only see the cgroups within their namespace.
  - **Use case:** Restricts access to cgroup structures inside containers, improving resource management and isolation.
- **Time Namespace**
  - Isolates system time and monotonic time.
  - **Use case:** Allows processes in containers to perceive different time settings (a newer feature introduced in Linux 5.6).

### **Network Namespace**

A Network Namespace isolates the following network-related resources:

- **Network Interfaces**: Such as `eth0`, `lo` (loopback interface). Each namespace can have its own set of network interfaces.
- **IP Address**: Each namespace can be assigned a unique IP address, supporting both IPv4 and IPv6.
- **Routing Table**: Each namespace has its own routing rules that determine how packets are forwarded.
- **Firewall Rules** (iptables/netfilter): Each namespace can define its own firewall policies independently.
- **Protocol Stack**: Separate instances of network protocols like TCP, UDP, etc.
- **Port Space**: Each namespace has an independent port range, allowing the reuse of the same port numbers (e.g., multiple containers binding to port 80 without conflict).

**`Note`:** Physical network hardware (such as network interface cards) is still shared by the host system. Network namespaces only isolate network configurations at the logical level.

## Prepare the Experiment Environment

This experiment was conducted using the Ubuntu 24.04 Server image with Vagrant and VirtualBox

Here’s the vagrant file, you can simply spin up the virtual machine via `$ vagrant up` and ssh into it via `$ vagrant ssh`

**Vagrantfile**

```bash
# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  # https://portal.cloud.hashicorp.com/vagrant/discover/bento/ubuntu-24.04
  config.vm.box = "bento/ubuntu-24.04"
  config.vm.box_version = "202502.21.0"
  config.vm.hostname = 'network-lab'
  config.vm.define vm_name = 'net'

  config.vm.provision "shell", privileged: false, inline: <<-SHELL
    set -e -x -u
    export DEBIAN_FRONTEND=noninteractive

    # Update packages and install required tools
    sudo apt-get update
    sudo apt-get install -y vim git cmake build-essential tcpdump tig socat bash-completion libpcap-dev bridge-utils ipcalc conntrack curl ca-certificates lsb-release gnupg

    # Install latest Docker (official recommended way)
    sudo install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) stable" | \
      sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt-get update
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    sudo usermod -aG docker $USER
    sudo modprobe br_netfilter



    git clone --depth=1 https://github.com/Bash-it/bash-it.git ~/.bash_it
    bash ~/.bash_it/install.sh -s
  SHELL

  config.vm.network :private_network, ip: "172.17.8.222"
  config.vm.provider :virtualbox do |v|
      v.customize ["modifyvm", :id, "--cpus", 2]
      v.customize ["modifyvm", :id, "--memory", 2048]
      v.customize ['modifyvm', :id, '--nicpromisc1', 'allow-all']
  end
end
```

## Basic Commands and Demonstration

### `ip netns` command

[ip-netns(8) - Linux manual page](https://man7.org/linux/man-pages/man8/ip-netns.8.html)

- `ip netns ls`: list all namespaces
- `ip netns add <name>`: Add a namespace
- `ip netns delete <name>`: Delete a namespace
- `ip netns exec <name>`:  Run arbitrary commands inside a given network namespace

### Create namespace

![Create namespace — screenshot](/images/linux-network-namespace-veth/02-screenshot-2025-07-11-2-16-48.png)

#### The `/var/run/netns` directory
We can create a network namespace named `ns1` like left hand side.

However, we may encounter a `mkdir … `error like the one shown on the left.

***Why does this happen?***


This happens because, in Linux, all network namespaces are stored under the `/var/run/netns` directory. If this directory does not exist, the `ip netns add` command will try to create the `/run/netns` directory when you attempt to create a namespace. However, due to insufficient permissions, it fails to create this directory.

- [iproute2/iproute2 — ip/ipnetns.c](https://github.com/iproute2/iproute2/blob/v6.15.0/ip/ipnetns.c#L757-L798)


Below is the result of creating two namespaces, `ns1` and `ns2`, after elevating privileges with `sudo`.

![The /var/run/netns directory — screenshot](/images/linux-network-namespace-veth/03-screenshot-2025-07-11-2-26-49.png)

### Operate and Inspect the Namespace

The left side of the image below shows the network configuration as seen on my virtual machine, while the right side shows the network configuration inside the `ns1` namespace accessed via `ip netns exec ns1`.

We can observe that in the `ns1` namespace, there is only one interface — the `lo` (loopback) interface — and it is in the `DOWN` state.

![Operate and Inspect the Namespace — screenshot](/images/linux-network-namespace-veth/04-screenshot-2025-07-11-2-30-44.png)

#### Ping External Networks

We did `ping 8.8.8.8` both from the host and from within the `ns1` network namespace. You can observe that since the `ns1` namespace has no active network interfaces enabled, it cannot communicate with external networks.

![Ping External Networks — screenshot](/images/linux-network-namespace-veth/05-screenshot-2025-07-11-2-34-57.png)

## Docker and Network Namespace

Docker uses Linux network namespaces to provide network isolation for containers. Each Docker container runs inside its own network namespace, which means it has its own independent network stack including interfaces, IP addresses, routing tables, and firewall rules.<br /><br />For example, two containers can both listen on port 80 without interfering with each other because they exist in different network namespaces.

***However, do you know why can’t we see the container’s network namespace from the host using the `ip netns` command?***

This is because the network namespaces created by Docker containers are not stored under `/var/run/netns` or `/run/netns`. Instead, they are located in the `/var/run/docker/netns` directory.

The image below shows two containers, each with its own network namespace present in the `/var/run/docker/netns` directory.

![Docker and Network Namespace — screenshot](/images/linux-network-namespace-veth/06-screenshot-2025-07-15-10-12-37.png)

We can create symbolic links for the containers' network namespaces in `/var/run/netns`. By doing so, we can also ***`view`*** and ***`exec`*** the Docker containers’ namespaces using the `ip netns ...` commands

![Docker and Network Namespace — screenshot](/images/linux-network-namespace-veth/07-screenshot-2025-07-15-10-14-17.png)


## Introduction to Virtual Ethernet (veth)

In Linux systems, Virtual Ethernet (VETH) is a technology used to create **`virtual`** network interfaces that simulate a `pair` of directly connected Ethernet interfaces.

VETH is part of the ***Linux kernel’s network device drivers*** and is managed by the kernel’s network stack. Its creation, management, and data transmission all happen at the kernel level.

### Core Concepts of VETH

- **Always Created in Pairs**: VETH interfaces always come in pairs (e.g., `veth0` and `veth1`), like a virtual network cable connecting two endpoints that can reside in different network namespaces or devices.
- **Data Transmission**: When data is sent from one end (e.g., `veth0`), it is immediately received at the other end (`veth1`), simulating a real network connection.
- **Use Cases**:
  - **Container Networking**: In container technologies, VETH pairs connect a container’s network namespace to the host’s namespace or a bridge (like Docker’s `docker0` bridge), enabling communication between containers and external networks.
  - **Network Isolation**: By placing one end of the VETH pair in a separate network namespace, network isolation is achieved while allowing controlled data flow between namespaces.
  - **Virtual Machines or Network Simulation**: Used to simulate complex network topologies.

### How It Works

1. **Create a VETH Pair**: Use a command like `$ ip link add veth0 type veth peer name veth1`to create a pair of linked VETH interfaces.
2. **Assign to Network Namespaces**: Move one end (e.g., `veth1`) into a network namespace (such as a container), while keeping the other end (`veth0`) in the host namespace or connecting it to a bridge.
3. **Configure IP and Routing**: Assign IP addresses and routing rules to ensure proper data flow.
4. **Data Forwarding**: Packets sent to one VETH interface appear directly on the peer interface, enabling efficient virtual network communication.

## Experiment

The following three labs are connected in sequence. Ultimately, they will build the setup shown below.

![Experiment — diagram](/images/linux-network-namespace-veth/08-veth-drawio.svg)

### Experiment 1 – Creating a veth Pair Using the `ip` Command

![Experiment 1 – Creating a veth Pair Using the ip Command — screenshot](/images/linux-network-namespace-veth/09-screenshot-2025-07-16-8-23-19.png)

Using the `ip link` command, we let the Linux kernel create a pair of virtual Ethernet interfaces, named `veth1` and `veth2`.

You can observe that two interfaces are created: `veth1@veth2` and `veth2@veth1`. The name after the `@` symbol indicates their peer interface, showing that they form a connected veth pair, simulating a virtual network cable.


![Experiment 1 – Creating a veth Pair Using the ip Command — screenshot](/images/linux-network-namespace-veth/10-screenshot-2025-07-16-8-23-31.png)

Try to bring up the `veth1` interface. You will observe that the `veth1@veth2` interface changes from DOWN to UP.

### Experiment 2 – Communication Between Host and a Single Network Namespace

![Experiment 2 – Communication Between Host and a Single Network Namespace — screenshot](/images/linux-network-namespace-veth/11-screenshot-2025-07-16-8-36-29.png)

- **Step 1:** Create a network namespace named `ns1`.
- **Step 2:** Attach one of the virtual interfaces, `veth2`, to the `ns1` network namespace and rename it to `eth1000`.
- **Step 3:** Enter the `ns1` namespace and check if the interface has been successfully attached.


![Experiment 2 – Communication Between Host and a Single Network Namespace — screenshot](/images/linux-network-namespace-veth/12-screenshot-2025-07-16-8-39-17.png)

After successfully attaching the virtual interface `veth2` to `ns1`, we perform the following steps:

- **Step 1:** Bring up the `eth1000` interface.
- **Step 2:** Assign an IP address. Here, we assign the IP address `10.66.77.24/24` to the interface.


![Experiment 2 – Communication Between Host and a Single Network Namespace — screenshot](/images/linux-network-namespace-veth/13-screenshot-2025-07-16-8-47-21.png)


After attaching `veth2` to the `ns1` network namespace (shown on the left side of the left image), if we check the network interfaces on the host again, we find that `veth2` is no longer present—only `veth1` remains (shown on the right side of the left image).

This is because the `ip` command only displays interfaces within the current network namespace. Since `veth2` has been moved out of the host’s default namespace and into the `ns1` network namespace, it is expected that it won’t be visible from the host.

What is ifindex?

**Click me to see explanation**

- Each network interface in the Linux kernel has a unique interface index (ifindex), which is an integer used internally to identify the network interface.
- When a VETH pair is created, each end is assigned a pair of consecutive or nearby ifindex values. For example, `veth1` might be assigned ifindex 11, and `veth2` assigned ifindex 12.
- **Rules for VETH naming display:**
  - When both ends of the VETH pair reside in the same network namespace, the `ip link` command shows them as `veth1@veth2` and `veth2@veth1`, indicating their pairing relationship.
  - When one end of the VETH pair is moved to a different network namespace, the kernel cannot directly display the paired interface’s name (because the other end may have been renamed or exists in another namespace). In this case, `ip link` shows the peer’s interface index (ifindex) to indicate the connection.

![Experiment 2 – Communication Between Host and a Single Network Namespace — screenshot](/images/linux-network-namespace-veth/14-screenshot-2025-07-16-8-56-58.png)

Next, we assign the IP address `10.66.77.25/24` to the host’s `veth1` interface (shown on the right side of the left image).

On the host side, we use the `tcpdump` command to monitor ICMP packets on this interface. Meanwhile, inside the `ns1` network namespace (left side of the left image), we send packets to the `veth1` interface by using the `ping` command.

The result shows that the host and `ns1` can communicate with each other through the VETH pair: `veth1` on the host and `veth2` (renamed to `eth1000`) in `ns1`.


### Experiment 3 – Point-to-Point Communication Between Network Namespaces

![Experiment 3 – Point-to-Point Communication Between Network Namespaces — screenshot](/images/linux-network-namespace-veth/15-screenshot-2025-07-16-9-40-01.png)

Previously, we established communication between `ns1` and the host.

Next, we create another network namespace called `ns2` and attach `veth1` to `ns2`, renaming it to `eth99`. This setup enables successful communication between `ns1` and `ns2` via the virtual Ethernet pair.


## Conclusion

`Network namespaces` provide isolated network environments within a single Linux host, allowing processes to have separate network stacks including interfaces, IP addresses, and routing tables. This isolation is fundamental for containerization and advanced network segmentation.

`Virtual Ethernet (veth)` pairs act as virtual cables connecting two network namespaces. By linking namespaces through veth pairs, isolated network environments can communicate securely and efficiently. Veth pairs are essential for enabling container-to-container or container-to-host networking, making them a key building block in modern Linux networking and container technologies.
