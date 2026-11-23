---
title: "Docker Networking Revisited: A Review of What We Learned"
description: "A hands-on review of Docker networking: namespaces, bridges, and iptables rules, revisiting each concept with experiments that show how packets really flow."
slug: "docker-networking-revisited"
---

By Rao Shahzaib · DevOps

## Key Takeaway

> In this chapter, we will use Docker to review the techniques we previously learned, including Network Namespace, Virtual Ethernet, Linux Bridge, and more.

![Diagram: Key Takeaway](/images/docker-networking-revisited/01-docker-networking-revisited.svg)

## Quick Review

If you want to understand the changes in **iptables** after installing Docker, please refer to this article: [6. Understanding the Relationship Between iptables, Docker, and Linux Bridge](/blog/iptables-docker-linux-bridge/)
If you want to understand the relationship between **Docker** and **Network Namespace**, please refer to this article: [1. Network Namespace and Virtual Ethernet (VETH)](/blog/linux-network-namespace-veth)

## Experiment

### **Set Up the Experiment Environment**

> This environment uses the **Ubuntu 24.04 server** provided by **iximiuz Labs**, which offers a fast and convenient online practice environment.

> Reference: [https://labs.iximiuz.com/](https://labs.iximiuz.com/)

#### **Install Docker**

Install following the official guide: [Docker Documentation](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository)[**Ubuntu**](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository)

After installation, the Docker service is not enabled by default, so we need to enable it using the following command:

```bash
$ sudo systemctl status docker.service
$ sudo systemctl start docker.service
$ sudo systemctl enable docker.service
```

### Let’s begin the experiment!

![Diagram: Let’s begin the experiment!](/images/docker-networking-revisited/02-docker-networking-revisited.png)
- **Step 1:** Use the command `sudo docker run -d --name <ng1/ng2> nginx` to create two nginx Docker containers.
- **Step 2:** After creating the two nginx containers, you will notice that two additional virtual ethernet interfaces have been added, both connected to the `docker0` bridge.
- **Step 3:** Use the `$ ip route` command to check the host’s routing table. You can observe that the `docker0` rule, like `eth0`, is created automatically by the kernel.

![Diagram: Let’s begin the experiment!](/images/docker-networking-revisited/03-docker-networking-revisited.png)
Next, let’s enter the network namespaces of the two containers to check the IP addresses assigned to them.

Here, we use the `nsenter` command to enter the network namespace. If you prefer to use the `ip netns` approach, you can refer to this article: <https://app.notion.com/p/2348a3a7d9d48076bb40e0306edc876b>

- **Step 1:** Retrieve the process IDs of the two containers, which are `3152` and `3281`.
- **Step 2:** Use the command `sudo nsenter -n -t 3152` to enter the network namespace of the `ng1` container. The method for entering `ng2` is similar.

![Diagram: Let’s begin the experiment!](/images/docker-networking-revisited/04-docker-networking-revisited.png)
- **Step 1:** After entering the network namespaces of the two containers, we ping the `ng2` container directly from the `ng1` container. The experiment shows that the two containers can communicate with each other.


![Diagram: Let’s begin the experiment!](/images/docker-networking-revisited/05-docker-networking-revisited.png)
- **Step 1:** This time, we observe the packets passing through the `docker0` bridge from the **Host**.
- **Step 2:** Once again, we ping the `ng2` container directly from the `ng1` container.

We can observe that both ARP and ICMP packets are being transmitted and received normally.


![Diagram: Let’s begin the experiment!](/images/docker-networking-revisited/06-docker-networking-revisited.png)
As a side note, how can we tell which virtual ethernet interface on the Host corresponds to the container’s network namespace?

From the diagram on the left, we can see that the interface number `12` on the `Host` (Bottom) corresponds to the `eth0` interface inside the container (Up), which also ends with `12`.


![Diagram: Let’s begin the experiment!](/images/docker-networking-revisited/07-docker-networking-revisited.png)
Now, let’s take a look at the **iptables filter table**.

- **Step 1:** From the `ng1` container’s network namespace, ping `8.8.8.8`.
- **Step 2:** Use the command `sudo iptables-save -t filter -c` to observe the packet and byte counters for Docker’s custom chains.

You can see that the packet and byte counts for the Docker channels increase with each ping.

![Diagram: Let’s begin the experiment!](/images/docker-networking-revisited/08-docker-networking-revisited.png)
In this experiment, we attempt to delete one of Docker’s iptables rules.

- **Step 1:** Delete the Docker iptables rule.

You will notice that the previously working `ping 8.8.8.8` command stops. This indicates that packets can no longer be forwarded through the `docker0` bridge, and therefore cannot reach `eth0` or communicate with the outside network.

![Diagram: Let’s begin the experiment!](/images/docker-networking-revisited/09-docker-networking-revisited.png)
- **Step 1:** After adding the rule back, packets can be sent again, and the `ng1` container can successfully communicate with `8.8.8.8`.

## Conclusion

In this chapter, we conducted simple experiments using Docker to verify and review the concepts we previously learned. This also lays a solid foundation for learning Docker and related networking technologies in the future.


---
