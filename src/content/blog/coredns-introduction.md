---
title: "Introduction to CoreDNS: The Cloud-Native DNS Server"
description: "An introduction to CoreDNS: its plugin chain, how a query flows through it, how it compares with BIND, and how to install, configure, and run it yourself."
slug: "coredns-introduction"
---

By Rao Shahzaib · DevOps

## **Introduction to CoreDNS**

### **A Brief History**

CoreDNS was started by **Miek Gieben** as a fork of the Caddy web server's DNS features. The goal was to create a modern, extensible DNS server written in the Go programming language.

> **Timeline**

> **2016:** CoreDNS project started

> **2017:** Accepted into Cloud Native Computing Foundation (CNCF)

> **2019:** Graduated from CNCF

> **Present:** Default DNS server for Kubernetes

### **The Plugin-Based Design Philosophy**

CoreDNS is built on a simple yet powerful idea borrowed from the Unix philosophy: ***everything is a plugin.***

Unlike traditional, monolithic DNS servers where all features are baked into one large application, CoreDNS provides a simple core server whose only job is to route DNS queries through a series of plugins. ***Each plugin is designed to do one specific thing and do it well.***

**Key Benefits**

- **Flexible:** You only use and enable the features you need.
- **Secure:** A smaller codebase with fewer running features reduces the potential attack surface.
- **Extensible:** Adding new functionality is as simple as writing a new plugin.

### **Why CoreDNS? The Cloud-Native Advantage**

CoreDNS excels in modern, dynamic cloud-native environments due to three key advantages:

- **Extensibility for Service Discovery:** Unlike traditional DNS servers built for static IPs, CoreDNS uses plugins to integrate directly with APIs. The kubernetes plugin automatically updates DNS records as services are created, scaled, or moved.
- **Simplicity and Performance:** It features a single, readable Corefile configuration and a lightweight binary with a low memory footprint and high performance capabilities.
- **Kubernetes Standard:** As the default DNS provider for Kubernetes, CoreDNS knowledge is essential for cloud-native work.

### **The Core Architecture: A Chain of Plugins**

The CoreDNS server itself does very little. Its main job is to **receive a DNS query and pass it down a ****`"plugin chain"`**. **Each plugin in the chain is a self-contained piece of code that performs one specific task.**

### **How a Query Flows Through CoreDNS**

Imagine an assembly line for building a car. Each station does one specific job.

1. A DNS query arrives at the CoreDNS server.
2. CoreDNS hands the query to the first plugin in the chain defined in the Corefile.
3. That plugin inspects the query and decides what to do:
- **Handle it:** If the plugin can answer the query (e.g., the cache plugin finds the answer in its cache), it does so and the process stops.
- **Modify it:** The plugin might change the query (e.g., the rewrite plugin) and then pass it to the next plugin in the chain.
- **Ignore it:** If the plugin can't handle the query, it simply passes it to the next plugin.
4. This continues down the chain until a plugin handles the query or the chain ends.

> **NOTE:** `The order of plugins in your Corefile matters immensely! If a plugin handles a query early in the chain, subsequent plugins will never see it.`

![Diagram: How a Query Flows Through CoreDNS](/images/coredns-introduction/01-coredns-introduction.png)

#### **Example Corefile**

```txt
my-app.local {
    log
    cache
    rewrite name my-app.local my-app.prod.backend
    forward . 8.8.8.8
}
```

#### **Flowchart Explanation**

> **The Flowchart above shows a typical flow. A query first goes to the *****log***** plugin (which logs every query), then to the *****cache***** (to check for a cached answer), then to *****rewrite***** (to potentially block a domain), and finally to *****forward***** to ask an upstream resolver like Google's 8.8.8.8. The first plugin to provide a definitive answer stops the chain.**

### **CoreDNS vs. BIND: The Need for a New Approach**

| **Feature** | **CoreDNS** | **BIND** |
| --- | --- | --- |
| **Configuration** | *Corefile: Simple, human-readable* | named.conf & Zone Files: Complex syntax |
| **Architecture** | *Plugin-Based: Highly modular* | Monolithic: Single large application |
| **Extensibility** | *Easy: Write plugins in Go* | Difficult: Complex C codebase |
| **Primary Use Case** | *Cloud-Native & Service Discovery* | Traditional Authoritative DNS |
| **Resource Usage** | *Lightweight: Smaller footprint* | Heavier: More resource-intensive |

> **In Summary:**

> BIND is like a battleship—powerful, feature-rich, and the standard for traditional, authoritative DNS for static zones. It has been battle-tested for decades.

> CoreDNS is like a set of high-tech LEGOs—you pick the exact pieces (plugins) you need to build the DNS server you want. This makes it incredibly flexible and ideal for today's dynamic, API-driven infrastructure.

### **Installing CoreDNS**

Getting CoreDNS running is straightforward because it's a single, self-contained binary written in Go.

> **The Easiest Method:**

> Download the pre-compiled binary from GitHub releases. This is the fastest and most reliable way to get started.

### **Step-by-Step Installation:**

1. **Go to Downloads Page**
- Navigate to: [CoreDNS Github Release](https://github.com/coredns/coredns/releases)
2. **Find the Latest Release**
- Look for the newest version.
3. **Download the Correct Binary**
- Under the "**Assets**" section, download the archive that matches your operating system (OS) and architecture (e.g., coredns\_1.9.4\_linux\_amd64.tgz for a 64-bit Linux system).
4. **Extract and Run:**
- **Extract the archive**. You will find a single file named coredns.
- Place this file in your system's **PATH** like `/usr/local/bin` to make it easy to run from any directory.
- Open your terminal and run `coredns -version` to verify it's installed correctly.

```txt
# Download CoreDNS
curl -LO https://github.com/coredns/coredns/releases/download/v1.12.3/coredns_1.12.3_linux_amd64.tgz

# Extract the binary
tar -xvzf coredns_1.12.3_linux_amd64.tgz

# Move to system path
sudo mv coredns /usr/local/bin/

# Make the binary executable
sudo chmod +x /usr/local/bin/coredns

# Verify installation
coredns -version
```


## Lab-CoreFile

This lab is designed to guide you through the process of building a production-ready CoreDNS configuration from the ground up. You will start by creating a foundational DNS resolver that utilizes caching and forwards unresolved queries to an upstream server. Next, you will learn to manage local DNS records for internal services by creating custom zones. Additionally, you will gain experience in advanced configuration by setting up a dedicated port for a specific zone and implementing intelligent query fallback to an alternative server. Finally, you will incorporate essential production plugins, such as logging ✍️ and metrics 📈, to ensure your DNS server is both observable and maintainable. This hands-on experience with the Corefile will equip you with a comprehensive understanding of how to manage a versatile and robust DNS service.


CoreDNS is a flexible and extensible DNS server developed in Go. Unlike traditional monolithic DNS servers, CoreDNS employs a plugin-based architecture. This design enables its functionality to be determined by a series of plugins that are configured in a file known as the Corefile. Each plugin is responsible for a specific task, such as caching, forwarding, or serving zone files.

In this lab, you will utilize the forward plugin to direct requests to Google's DNS server and the file plugin to serve local DNS records. This modular design empowers you to develop highly customized and efficient DNS solutions tailored to your specific requirements.

The Corefile specifies a series of server blocks, each of which can listen on distinct addresses and ports, executing unique sets of plugins. This capability allows you to manage example.local on a different port and implement intelligent fallback using the fallthrough keyword. As you will discover, CoreDNS is a powerful tool for modern, dynamic environments such as Kubernetes, while also being well-suited for standalone DNS server tasks.


<h2>
Task
</h2>

CoreDNS: Building a Production-Ready DNS Server 🌐

This lab guides you through creating a production-ready CoreDNS configuration from scratch. You'll begin by setting up a basic caching and forwarding DNS resolver. Then, you'll learn to manage local DNS records for internal services. Finally, you'll add crucial production plugins like logging and metrics to make your DNS server observable and maintainable. This hands-on experience with the Corefile will give you a comprehensive understanding of how to manage a versatile and robust DNS service.

The Corefile is the central configuration file for CoreDNS. It defines how CoreDNS behaves, specifying which plugins to use and how to handle DNS queries for different zones. Mastering the Corefile is key to building a custom and powerful DNS solution tailored to your specific needs.

1. The Initial Setup: Caching and Forwarding 🚀In this task, you'll build the foundation of your DNS resolver. Your goal is to configure CoreDNS to act as a caching DNS resolver on localhost (port 53). This means it will temporarily store responses to frequently requested queries to speed up future lookups. Additionally, you'll configure it to forward all unresolved queries to Google's public DNS at 8.8.8.8.

Action: You'll be editing the Corefile to set up the basic forward and cache plugins.

1. Adding a Local Zone Block to Corefile 🏘️Now it's time to manage internal services. The marketing team has a new internal server, and you need to add a local DNS zone for example.local to your CoreDNS configuration. This will allow internal services to resolve [www.example.local](http://www.example.local/) without sending the query to the public internet.

Before You Start: A zone file named /etc/coredns/db.example.local has been provided for you. This file contains the DNS records for the example.local zone.

Action: You'll append a new server block to your Corefile to handle example.local queries using the provided zone file.

1. Serving the Local Zone on a Separate Port 🚪For security and organization, the example.local zone needs to be served on a dedicated port, separate from the default DNS service. This task requires you to modify your Corefile to listen for queries on port 5300 for the example.local zone.

Action: You'll modify the Corefile to create a new server block specifically for example.local that binds to port 5300.

1. Implementing Intelligent Fallback 🧠In this step, you'll add a new server block for a work-in-progress zone, internal.network. This zone file is incomplete, so you need to configure CoreDNS to use the fallthrough keyword. This will ensure that if a query isn't found in the db.internal.network file, it will automatically fall back and be forwarded to an alternative internal DNS server at 10.0.0.1.

Before You Start: An incomplete zone file /etc/coredns/db.internal.network has been created for you.

Action: You'll create a new server block in your Corefile for internal.network and configure it to fallthrough to the alternate server.


**Corefile Explanation**

The Corefile serves as the primary configuration file for CoreDNS, structured into server blocks, each defined by its respective zones and ports. In this scenario, the server block is denoted as .:53, signifying its role in listening for DNS queries across all zones (.) on the standard DNS port, 53.

Within this server block, you will find a series of plugins, each specified on a separate line. CoreDNS processes these plugins sequentially to manage incoming queries:

1. **log**: This plugin activates logging for every DNS query received by the server. It is essential for debugging and monitoring, as it captures each request and response.
2. **errors**: The errors plugin ensures that any encountered DNS errors are logged to the standard output, facilitating quick diagnosis of configuration issues or problems with upstream servers.
3. **cache**: The cache plugin stores DNS responses to enhance the speed of subsequent lookups. When a query is issued, CoreDNS first checks its cache. If a stored answer is available, it returns the result immediately, thereby minimizing latency and reducing external network traffic.
4. **forward . 8.8.8.8 8.8.4.4**: The forward plugin directs unresolved queries to designated upstream DNS servers.

The period (.) indicates that this rule pertains to all zones, meaning it applies to any queries not managed by a preceding plugin.

The IP addresses 8.8.8.8 and 8.8.4.4 represent the upstream DNS servers. CoreDNS will forward any queries it cannot resolve locally to these servers to obtain the appropriate response.


In CoreDNS, the Corefile serves as the central configuration file that outlines the handling of DNS queries. Specific plugins that are integrated into this file manage the caching and forwarding functionalities. When a DNS query is received, CoreDNS processes it through a sequence of plugins defined within the Corefile.

**How It Works:**

**Caching 💾:** The cache plugin retains DNS responses for a designated period. Upon receiving a query, the cache plugin is one of the initial components in the processing chain that checks for a previously stored answer. If the record resides in the cache and remains valid, CoreDNS promptly delivers the response, conserving time and resources by eliminating the need for an external server query. This process notably accelerates resolution for frequently requested domains.

**Forwarding ⏩:** The forward plugin is responsible for directing queries to an upstream DNS server when CoreDNS is unable to resolve the query independently. After the cache plugin verifies its entries and finds no corresponding match, the query progresses down the plugin chain. The forward plugin captures the request and forwards it to the designated upstream server, specifically Google's public DNS at 8.8.8.8. The response received from the upstream server is subsequently returned to the client and stored in the cache by the cache plugin for potential future use.

The integration of these two plugins fosters an efficient DNS resolver. It first assesses a local cache for rapid responses and then intelligently routes requests to an external server to resolve queries that it has not encountered previously.


A zone file, such as /etc/coredns/db.example.local, is a plaintext file containing all the DNS records for a specific domain. CoreDNS utilizes a plugin called "file" to read these zone files and serve the associated DNS records.

**How It Works 📖**

The provided db.example.local file includes several key records that define the example.local zone:

1. **\$TTL 3600**: This line sets the Time to Live (TTL) for all records in the file to 3600 seconds (1 hour), unless a specific record specifies its own TTL. The TTL indicates to caching resolvers how long they should retain the record before requesting an updated copy.
2. **SOA Record**: The Start of Authority (SOA) record is mandatory in every zone file. It provides essential administrative information about the zone, including the primary name server (ns1.example.local.), the email address of the administrator (hostmaster@example.local), and a series of timing values. The serial number (2023010101) is a crucial component that informs other DNS servers when the zone file has been updated.
3. **NS Record**: The Name Server (NS) record designates the authoritative name server for the zone. In this example, ns1.example.local. is identified as the server responsible for the example.local zone.
4. **A Records**: The Address (A) records associate a domain name with an IPv4 address.
- **ns1 IN A 127.0.0.1**: This entry maps the name server ns1.example.local. to the localhost IP address 127.0.0.1.
- **www IN A 192.168.1.100**: This record corresponds to the internal web server. When a user queries [www.example.local](http://www.example.local/), the DNS server will respond with the internal IP address 192.168.1.100.


**Adding a Local Zone block to Corefile:**

The marketing team has a new internal web server for a project called "Project Falcon." It's not public-facing, so we need to add a local zone to our DNS server for `db.example.local`. All other requests should still be handled as before.

**Action Plan:**

- Append a new server block to your existing Corefile.
- Restart CoreDNS with the updated configuration.

**Your Task with the Corefile ⚙️**

To configure CoreDNS to utilize this zone file, you will need to add a new server block to your Corefile. This block should specify that for any queries ending in `example.local`, CoreDNS should apply the file plugin to retrieve the answer from `/etc/coredns/db.example.local`. This process establishes a custom, local DNS zone that operates independently of public DNS.


Verify that [www.example.local](http://www.example.local/) is resolving to IP address 192.168.1.100.


By default, DNS servers listen on port 53 for all queries. However, for enhanced security and improved network management, it is often beneficial to separate different DNS zones onto their own ports. 🌐 In this task, you will create a new server block in your Corefile specifically to handle queries for the `example.local` zone on port 5300. 🎯 This ensures that all internal DNS traffic is distinctly separated from public-facing DNS requests.

**What the User is Doing**

The user will modify the Corefile to add a new server block configured to:

- **Specify the zone:** `example.local`
- **Bind to a specific port:** `:5300`
- **Utilize the file plugin:** To serve the `db.example.local` zone file, as previously configured. 📂

This creates a dedicated DNS service for the internal zone. Afterward, you will need to restart CoreDNS to apply the changes. 🔄

**How it Works**

When a DNS query arrives, CoreDNS reads its configuration from the Corefile and determines which server block should handle the request based on the domain and port combination. 📊

- **Main Block (Port 53):** Your existing server block will continue to handle public queries on port 53. It will process all non-`example.local` queries by caching and forwarding them to `8.8.8.8`.
- **New Block (Port 5300):** The newly created server block will specifically cater to `example.local`. Any query for `example.local` that comes in on port 5300 will be directed to this block. It will utilize the file plugin to serve the appropriate record from the `db.example.local` file. 📄

This configuration effectively isolates internal DNS traffic. It enables a client (such as an internal application) to specifically query the `example.local` zone by directing its request to port 5300, while a public query for `cloudflare.com` will still route through the default port 53. 🚀


**Serving the Local Zone on a Separate Port**

The security team now requires that all queries for the `example.local zone` be handled on a dedicated port (5300), separate from the default DNS service on port 53. This ensures that internal services can be clearly separated from external/public queries.

**Action Plan:**

Modify the `Corefile` to add a new server block for `example.local` listening on port **`5300`**.

Restart CoreDNS with the updated configuration.


**Implementing Intelligent Fallback**

A senior engineer just told you that the `db.internal.network` zone file is a work in progress. It only has a few records, but for any queries not found in the file, they should automatically be forwarded to a different internal DNS server at `10.0.0.1` All other traffic should continue to be handled by our main resolver. This requires you to add a new server block and use the fallthrough keyword.

**Action Plan:**

1. Append the new server block to your Corefile, configuring fallthrough.
2. Restart CoreDNS after updating configuration

*Before You Start*: An incomplete zone file `/etc/coredns/db.internal.network` has been created for you.

**Note:** For the purposes of this lab, the IP address 10.0.0.1 is used solely for demonstration. There is no functioning DNS service at this address. This exercise is designed to teach you the appropriate configuration for real-world scenarios where a secondary DNS server would be utilized.

Is the failthrough functioning properly?


## Lab: Plugins

This lab serves as a hands-on guide to constructing a production-ready CoreDNS configuration from the ground up. Participants will learn to establish a robust and versatile DNS service by exploring and implementing key CoreDNS plugins. This experience will provide essential skills for managing a highly functional and observable DNS solution suitable for any environment.

**Understanding CoreDNS Plugins:**

CoreDNS serves as an extensible DNS server, with its functionality structured around plugins—modular components that execute specific tasks. This design allows for the creation of a custom DNS server tailored to unique requirements. The significance of plugins includes:

- **Modularity:** Each plugin is tasked with a distinct function, such as resolving from a hosts file, forwarding queries, or serving metrics, promoting a clean and manageable codebase.
- **Flexibility:** Users can combine various plugins to construct a custom DNS chain. For instance, one may configure a server to first check a local hosts file and then forward to a public DNS server if the record is not found.
- **Extensibility:** The plugin-based architecture facilitates community development and the addition of new features to CoreDNS.

Throughout this lab, participants will engage with several crucial plugins, including hosts, forward, etcd, log, errors, and cache, ultimately gaining a comprehensive understanding of their effective use.

**Task 1: Utilizing the Hosts Plugin**

In this task, participants will configure CoreDNS to resolve a custom hostname to a specific IP address using a local hosts file.

**Steps:**

1. **Configure CoreDNS:** Edit the Corefile to incorporate the hosts plugin, which enables CoreDNS to serve DNS records from a local file, akin to the traditional /etc/hosts file.
2. **Resolve a Hostname:** Verify that the configuration is operational by employing a DNS lookup tool (such as dig) to resolve service-a.lab.local. CoreDNS will retrieve the corresponding entry for this hostname from the provided /etc/lab.hosts file.

*Before you start:* The lab environment is pre-configured, with the file /etc/lab.hosts containing a single entry: "192.168.1.100 service-a.lab.local." This file will be utilized in your configuration.

**Task 2: Implementing the Forward Plugin**

This task focuses on utilizing the forward plugin to route DNS queries for a specific domain to an external DNS server, a fundamental requirement for any DNS server resolving public domain names.

**Steps:**

1. **Integrate the Plugin:** Add the forward plugin to your Corefile.
2. **Define Upstream Servers:** Configure the plugin to forward queries for non-local domains to an upstream server, such as Google's Public DNS server at 8.8.8.8.
3. **Test the Forwarding:** A test will be conducted using dig to query a public domain, such as google.com. This query should be successfully forwarded to 8.8.8.8, returning the correct IP address.

**Task 3: Utilizing the Etcd Plugin for Dynamic Service Discovery**

This task introduces advanced use cases involving dynamic service discovery through the etcd plugin, commonly used in microservices architectures where service endpoints may change frequently.

**Steps:**

1. **Configure Etcd:** Set up the CoreDNS server to utilize the etcd plugin for resolving hostnames based on records stored within an etcd cluster.
2. **Add a Service Record:** Launch a separate etcd container and add a service record to it.
3. **Resolve the Service:** Use dig to query for the service recently added, allowing CoreDNS to dynamically retrieve the record from etcd and provide the corresponding IP address.

**Task 4: Chaining Plugins**

In this final task, participants will consolidate their knowledge by chaining plugins to create a complete and robust DNS resolution chain.

**Steps:**

1. **Arrange the Corefile:** Understand the importance of the plugin order in the Corefile, as the CoreDNS server processes queries sequentially through the plugin chain.
2. **Use Fallthrough:** Implement the fallthrough option with the hosts plugin, instructing CoreDNS to resolutely "fall through" to the next plugin in the chain (here, the forward plugin) should a record not be found in the local hosts file.
3. **Verify the Chain:** Test the configuration by first attempting to resolve a hostname from the local hosts file, followed by querying a public domain requiring forwarding to the upstream server. Both queries should succeed, validating the implementation of a production-ready DNS configuration.

---
