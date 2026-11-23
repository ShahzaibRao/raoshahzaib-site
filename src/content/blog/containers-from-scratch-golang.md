---
title: "Containers From Scratch with Go: Build Your Own Docker-Like Runtime"
description: "Build a Docker-like container runtime from scratch in Go: namespaces, cgroups, chroot and networking, following Liz Rice's hands-on course step by step."
slug: "containers-from-scratch-golang"
---

By Rao Shahzaib · DevOps

If you like my article, feel free to give me a like and share my post on Linkedin → [Containers From Scratch by Golang (feat. Liz Rice) \| Notion \| Pei Yao Chang \| 12 comments](https://www.linkedin.com/feed/update/urn:li:activity:7370063234709581825/)

## Learning Materials

This note is my study summary from Liz Rice’s online course. I highly recommend going through the following content first, and then using this note to reinforce and deepen your understanding of the related topics.

- [Building Containers from Scratch with Go](https://learning.oreilly.com/videos/building-containers-from/9781491988404/9781491988404-video312009/)
- [Containers from scratch: The sequel - Liz Rice (Aqua Security)](https://youtu.be/_TsSmSu57Zo?si=I_i0ZKqJ0f7BvM8d)
- [Containers From Scratch • Liz Rice • GOTO 2018](https://youtu.be/8fi7uSYlOdc?si=ibYFnHb_rachCnPK)
- [Rootless Containers from Scratch - Liz Rice, Aqua Security](https://youtu.be/jeTKgAEyhsA?si=LlzWb-MSNjHdUCGd)

## My Source Code

You can get the complete sample code from my repo below

[baconYao/container-from-scratch-golang](https://github.com/baconYao/container-from-scratch-golang)

## Online Practice Machine

![Online Practice Machine — screenshot](/images/containers-from-scratch-golang/01-screenshot-2026-01-01-8-06-53.png)

I’ll be using the **`iximiuz`** Golang environment in this post, making it easier for readers to follow the exercises.

Give it a shot: [Go(lang) Playground \| iximiuz Labs](https://labs.iximiuz.com/playgrounds/golang)


## Our Targets

As Liz Rice mentions in each lesson, our goal is to mimic Docker’s **`run`** command so that an application can run in an environment isolated from the host (aka a container). However, note that we won’t be pulling a public image—instead, we’ll use the Ubuntu 24.04 rootfs as the container’s file system.

Therefore, we’ll use Golang to build a small program that provides a capability similar to **`docker run`**.

![Capture from Liz Rice’s materials](/images/containers-from-scratch-golang/02-capture-from-liz-rice-s-materials.png)

As we enhance the functionality of our small program, we will explore the following topics, allowing us to create a basic simulation of a non-production container environment.

1. UTS Namespace
2. Chroot
3. PID Namespace
4. Mount Namespace
5. Control Group
6. Rootless Container

### Initial Code

At this stage, there is no containerization-related code. It is simply a command-line tool used to execute a specified external command and pass arguments to it.

**main.go**

```go
package main

import (
	"fmt"
	"os"
	"os/exec"
)

// go run main.go run <cmd> <args>
func main() {
	switch os.Args[1] {
	case "run":
		run()
	default:
		panic("help")
	}
}

func run() {
	fmt.Printf("Running %v\n", os.Args[2:])

	cmd := exec.Command(os.Args[2], os.Args[3:]...)
	cmd.Stdin = os.Stdin
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr

	must(cmd.Run())
}

func must(err error) {
	if err != nil {
		panic(err)
	}
}

```
![Initial Code — screenshot](/images/containers-from-scratch-golang/03-screenshot-2025-08-23-8-40-49.png)

- **`run` function**
  - The `run` function is responsible for executing external commands. The command name is obtained from `os.Args[2]`, and subsequent arguments are passed from `os.Args[3:]`.
  - It uses `exec.Command` to create a command object, with `os.Args[2]` as the command name and `os.Args[3:]` as the arguments.
  - Standard input (`Stdin`), standard output (`Stdout`), and standard error (`Stderr`) are bound to the corresponding streams of the current process, ensuring the external command’s I/O is consistent with the terminal.
  - The command is executed with `cmd.Run()`, and the `must` function is used to check for any errors.
- **`must` function**
  - This is a simple error-handling function that takes an error object `err`.
  - If `err` is not nil, the program will panic, terminate execution, and print the error message.


## Step 1 - Modifying the Container’s Hostname via the UTS Namespace

The UTS namespace (Unix Time-sharing System namespace) is a type of namespace used to isolate a process’s hostname and NIS domain name.

**`Goal`:** Learn the concept of the UTS namespace and use `CLONE_NEWUTS` to change the container’s hostname.

<br />Ref:

- [namespaces(7) - Linux manual page](https://man7.org/linux/man-pages/man7/namespaces.7.html)
- [uts\_namespaces(7) - Linux manual page](https://man7.org/linux/man-pages/man7/uts_namespaces.7.html)<br />

#### Why Do We Need to Modify the Container’s Hostname?

In Linux, the hostname actually belongs to the **UTS namespace** (UNIX Time-sharing System namespace), which allows each container to have its ***own hostname and domain name.*

- On the host machine, the `hostname` might be `prod-node-01`.
- Inside a container, it can be set to `web-1`, `db-1`, or even a random UUID.
- This way, **hundreds of containers running on the same host won’t share the same hostname**.

In other words, the **UTS namespace provides the ability to identify containers**.

#### Advantage

- **Readability and Isolation**
  - When developers or operators `exec` into a container, the prompt:
    ```bash
    root@web-1:/#
    ```


    immediately indicates which service they are in, avoiding confusion with the host.

  - Without hostname isolation, all containers would show the host’s name, making accidental operations much more likely.
- **Kubernetes / Docker Metadata Integration**
  - Docker sets the container hostname to the container ID (or name).
  - In a Kubernetes Pod, a container’s hostname equals the Pod name, which allows direct resolution via cluster DNS:
    ```bash
    curl http://my-service.my-namespace.svc.cluster.local
    ```
  - This entire design relies on **UTS namespace isolation**.
- **Application Behavior**
  - Many applications use `gethostname()` as an identifier, for example:
    - Web server logs (to record which instance handled a request)
    - Distributed systems (Redis cluster, Cassandra, Elasticsearch) often use the hostname as a node ID
  - Without isolation, all containers would report the same hostname → leading to confusion.
- **Security and Multi-Tenant Isolation**
  - Without a hostname namespace, a container from tenant A could read the host’s real hostname (e.g., `prod-db01`) → an information leak.
  - In SaaS or public cloud environments, this poses a **security risk**.

#### Conclusion

- **Technical perspective**
  - The hostname belongs to the **UTS namespace**, allowing the container to decide for itself “*who I am*.”
- **Practical perspective**
  - Makes debugging easier, avoiding confusion between the host and containers.
  - Kubernetes/Docker rely on it for DNS and cluster identity.
  - Prevents information leaks and security risks.
  - Distributed systems require independent hostnames as IDs.

### Hands-on Experiment

Before applying the UTS namespace concept, let’s first run the original version of the program

![Hands-on Experiment — screenshot](/images/containers-from-scratch-golang/04-screenshot-2025-09-01-7-40-50.png)

- **Step 1:** Switch to the root user and run the program. Once inside the newly forked Bash environment, use the `hostname` command tocheck the current hostname.
  - The current hostname is `golang-01`.
- **Step 2:** Use the command `hostname baconyao-container` to set the hostname to `baconyao-container`.
- **Step 3:** Exit the forked Bash environment and check the hostname.

At this point, you’ll notice that the hostname has been **permanently** changed to `baconyao-container`. How can we avoid this? The answer is to use the **UTS namespace** to isolate the forked process.

#### Manually Changing the Hostname

```go
func run() {
	fmt.Printf("Running %v\n", os.Args[2:])

	cmd := exec.Command(os.Args[2], os.Args[3:]...)
	cmd.Stdin = os.Stdin
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	cmd.SysProcAttr = &syscall.SysProcAttr{
		Cloneflags: syscall.CLONE_NEWUTS,
	}

	must(cmd.Run())
}
```


First, in the `run` function inside `main.go`, we set the `CLONE_NEWUTS` flag using `cmd.SysProcAttr`. Its specific behavior is as follows:

- `SysProcAttr` is an instance of the `syscall.SysProcAttr` struct, used to control the behavior of a new process.
- `Cloneflags: syscall.CLONE_NEWUTS` sets the `CLONE_NEWUTS` flag, a Linux-specific system call flag that creates a separate **UTS namespace** (UTS = Unix Time-sharing System) for the new process when executing the command.
- The **UTS namespace** controls a process’s hostname and domain name. Enabling `CLONE_NEWUTS` means the new process will have its own UTS namespace, isolated from the parent process, allowing the hostname or domain name to be changed without affecting the global system.

**Notes:**

- **Platform limitation:** `syscall.CLONE_NEWUTS` only works on Linux and requires sufficient permissions (e.g., root). Without proper privileges, it may fail.
- **Dependency:** This code relies on the `syscall` package, and `CLONE_NEWUTS` is Linux-specific. It does not work on non-Linux platforms (e.g., Windows or macOS).

![Manually Changing the Hostname — screenshot](/images/containers-from-scratch-golang/05-manually-changing-the-hostname-12.png)

After adding the `CLONE_NEWUTS` flag, let’s give it a try.

- **Step 1:** Inside the container environment above, use the `hostname` command to change the container’s hostname to `baconyao-container`.
- **Step 2:** In the host environment below, check the current hostname with `hostname`. You’ll see that the host’s name is still `golang-01`.

So far, we have successfully changed the hostname inside the container.

However, this approach has two drawbacks:

1. It requires manual intervention to change the hostname.
2. As shown in the diagram (blue line), the user’s prompt still displays the original host name (`golang-01`).

To address these issues, we will now handle it programmatically.


#### Code Implementation

```go
func run() {
	fmt.Printf("Running %v\n", os.Args[2:])

	cmd := exec.Command(os.Args[2], os.Args[3:]...)
	cmd.Stdin = os.Stdin
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	cmd.SysProcAttr = &syscall.SysProcAttr{
		Cloneflags: syscall.CLONE_NEWUTS,
	}

	must(syscall.Sethostname([]byte("baconayo-container")))

	must(cmd.Run())
}
```
To ensure that users see the modified hostname immediately upon entering the container, we need to set the new hostname ***before*** entering the Bash environment.

In practice, this is done using the `syscall.Sethostname` command to set the hostname to `baconyao-container`.

Although the `run` function on the left allows us to set the hostname, this approach actually **violates the design principle of namespaces**. Linux’s UTS namespace requires that child processes be isolated from the parent process. If we set the hostname directly in the `run` function before executing the command, it will affect the parent process’s hostname, ***breaking the isolation principle.*

Reference

- [https://man7.org/linux/man-pages/man7/namespaces.7.html](https://man7.org/linux/man-pages/man7/namespaces.7.html)
- [https://man7.org/linux/man-pages/man2/clone.2.html](https://man7.org/linux/man-pages/man2/clone.2.html)


```go
// go run main.go run <cmd> <args>
func main() {
	switch os.Args[1] {
	case "run":
		run()
	case "child":
		child()
	default:
		panic("help")
	}
}

func run() {
	fmt.Printf("Running %v\n", os.Args[2:])

	cmd := exec.Command("/proc/self/exe", append([]string{"child"}, os.Args[2:]...)...)
	cmd.Stdin = os.Stdin
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	cmd.SysProcAttr = &syscall.SysProcAttr{
		Cloneflags: syscall.CLONE_NEWUTS,
	}

	must(cmd.Run())
}

func child() {
	fmt.Printf("Running %v\n", os.Args[2:])

	cmd := exec.Command(os.Args[2], os.Args[3:]...)
	cmd.Stdin = os.Stdin
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr

	must(syscall.Sethostname([]byte("baconayo-container")))

	must(cmd.Run())
}


```
To preserve the principle of isolation, we need a separate `child` function to handle these operations in the child process.

Therefore, we refactor the current code to separate the responsibilities of the `run` and `child` functions.

- **`run` function**
  - To let the parent process (`run`) start a child process, we use `/proc/self/exe child ...`. This forks a new process that executes **the same binary**, but the first argument is now `"child"`.
  - We set a new UTS namespace for the child process with `cmd.SysProcAttr = &syscall.SysProcAttr{Cloneflags: syscall.CLONE_NEWUTS}`.
- **`child` function**
  - `syscall.Sethostname([]byte("baconyao-container"))` sets the hostname for the child process. This only affects the child’s UTS namespace and does not impact the parent process.

This design leverages the isolation feature of the UTS namespace: the child process is separated from the parent (via a new UTS namespace) to allow an independent hostname.

This approach is similar to how container technologies (like Docker) work. The `run` function acts like a container launcher, creating an isolated environment, while the `child` function represents the process inside the container, executing tasks within that isolated environment.

**A Detailed Exploration of `/proc/self/exe`**

- 在 Linux 系統裡，`/proc/self/exe` 是一個 **`symlink`**，指向「目前這個 process 執行的 binary」。意思是：這行會再呼叫**自己這個 Go 程式**（同一個編譯出來的 binary）。
- **Parsing `append([]string{"child"}, os.Args[2:]...)`**
  - Suppose we run the program as `$ go run main.go run /bin/bash`
    - This produces `os.Args = [".../tmp/go-buildxxxx/b001/exe/main", "run", "/bin/bash"]`
      - `go run` first compiles a temporary binary and then executes it, so `os.Args[0]` is not `main.go` but the path to the temporary executable.
    - Next, look at `os.Args[2:]`
      ```go
      os.Args[2:] = ["/bin/bash"]
      ```
    - Then we look at `append([]string{"child"}, os.Args[2:]...)`
      ```go
      ["child", "/bin/bash"]
      ```
    - So the final effect of `exec.Command` is:
      ```bash
      /proc/self/exe child /bin/bash
      ```


![Code Implementation — screenshot](/images/containers-from-scratch-golang/06-code-implementation-13.png)

After running our program, we will get the outcome like the left diagram.


## Step 2 - chroot – A Filesystem Isolation Mechanism

**`Goal`:** Simulate an independent filesystem environment that provides filesystem isolation, allowing a process to access only a specified portion of the filesystem, thereby enhancing security and isolation.

![Capture from Liz Rice’s materia](/images/containers-from-scratch-golang/07-capture-from-liz-rice-s-materia.png)

The image on the left is taken from Liz Rice’s slides. In her demo, the `chroot` system call is used to set the process’s root directory to a specified path, without changing the filesystem’s mount structure.

**What is the filesystem mount structure?**

It refers to the way an operating system organizes how filesystems (such as disk partitions, virtual filesystems, or remote filesystems) are attached to the filesystem tree. Specifically, it describes how a filesystem is **`mounted`** at a particular directory (called a mount point), allowing the contents of that filesystem to be accessed under that directory.

Linux uses a global mount structure (maintained by the kernel), which can be viewed using:

- **Command:** `mount` or `cat /proc/mounts`
- **Example output:**
  ```bash
  /dev/sda1 / ext4 rw,relatime 0 0
  /dev/sdb1 /mnt ext4 rw,relatime 0 0
  tmpfs /tmp tmpfs rw,nosuid,nodev 0 0
  ```
- `/dev/sda1` is mounted to `/` (root directory, using the ext4 filesystem).
- `/dev/sdb1` is mounted to `/mnt`.
- `tmpfs` (a memory-based filesystem) is mounted to `/tmp`.

The mount structure determines the ***filesystem view*** that a process sees when accessing files. For example, when a process accesses `/mnt/file.txt`, it is actually accessing `file.txt` on `/dev/sdb1`.

`chroot` only changes the root directory for a specific process; the rest of the system continues to operate under the original root directory. Because of this, `chroot` does **not** modify the global namespace’s mount table, making it relatively easy to ***escape (chroot breakout)*** from the chrooted sandbox and access the host’s full filesystem.

In well-known container technologies like Docker, the `pivot_root` system call is used together with the **mount namespace**. This not only changes the root directory but also moves the old root filesystem to another location and optionally unmounts it, providing much stronger isolation.

### Obtaining the Root Filesystem (rootfs)

##### What is rootfs?

**rootfs** (root filesystem) is a directory structure of a filesystem that ***typically contains the minimal set of files and directories needed for an independent operating system environment***. It is a core component of containers or similar isolated environments, providing the filesystem view required for process execution. Rootfs usually simulates a complete OS filesystem but on a smaller scale, including essential libraries, executables, configuration files, and more.

- Rootfs forms the foundation of container images; for example, the base of a Docker image is a rootfs.
- It can come from a minimal version of a Linux distribution (such as Ubuntu or Alpine) or be customized for a specific application.

#### Uses of rootfs

- **Containerization:** Rootfs provides a container with an independent filesystem environment, ensuring that processes inside the container can only access this restricted filesystem.
- **System booting:** During Linux system startup, `initramfs` (initial RAM filesystem) acts as a temporary rootfs to load kernel modules and eventually mount the real root filesystem.
- **Embedded systems:** Embedded devices often use a minimal rootfs to provide a lightweight runtime environment.

We use the Ubuntu 24.04 rootfs as the container’s root filesystem.

You can obtain and extract it using the following commands

```go
$ wget https://cloud-images.ubuntu.com/wsl/releases/24.04/current/ubuntu-noble-wsl-amd64-24.04lts.rootfs.tar.gz
$ mkdir ubuntu-2404-rootfs
$ sudo tar -xzf ubuntu-noble-wsl-amd64-24.04lts.rootfs.tar.gz -C ubuntu-2404-rootfs
```

The image below shows the contents of my current directory.

![Uses of rootfs — screenshot](/images/containers-from-scratch-golang/08-screenshot-2025-08-23-10-38-28.png)

### Modifying the `child` Function

```go
func child() {
	fmt.Printf("Running %v\n", os.Args[2:])

	cmd := exec.Command(os.Args[2], os.Args[3:]...)
	cmd.Stdin = os.Stdin
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr

	must(syscall.Sethostname([]byte("baconayo-container")))
	must(syscall.Chroot("/home/laborant/container/ubuntu-2404-rootfs"))
	must(os.Chdir("/"))

	must(cmd.Run())
}
```


After obtaining the rootfs, in the `child` function we use the `syscall.Chroot` system call to rstrict the process’s filesystem view to the specified rootfs (here, `/home/laborant/container/ubuntu-2404-rootfs`). This means the process can only see and access files within the rootfs and cannot access the host’s filesystem (e.g., `/etc` or `/home` on the host).

- For example, when the process executes `ls /`, it only sees the contents of `ubuntu-2404-rootfs`, not the host’s root directory. This is a core mechanism of containerization, ensuring that processes run in an isolated environment.

After executing `syscall.Chroot`, the process’s root directory becomes `/home/laborant/container/ubuntu-2404-rootfs`, but the current working directory may still point to the old path (e.g., a directory on the host). Therefore, we also need to use `os.Chdir("/")` to switch the working directory to the new root (i.e., `/` inside the rootfs), ensuring that subsequent operations (like `cmd.Run()`) execute in the context of the rootfs. Otherwise, path errors may occur.

### Running the Container Again

![Running the Container Again — screenshot](/images/containers-from-scratch-golang/09-running-the-container-again-11.png)

- **Step 1:** Before running our program, first check the host’s root directory on the host side.
- **Step 2:** Next, switch to the `ubuntu-2404-rootfs` directory. To verify later whether the process’s root directory has been successfully changed to `ubuntu-2404-rootfs`, create a file named `BACONYAO_CONTAINER_ROOT` in this directory.
- **Step 3:** Finally, run the program. Once inside the container, check the process’s root directory. You should see the `BACONYAO_CONTAINER_ROOT` file, indicating that `ubuntu-2404-rootfs` has been successfully set as the filesystem visible to the process. This ensures that the process and its child processes can only access this portion of the filesystem and cannot access the host’s root directory.


![Running the Container Again — screenshot](/images/containers-from-scratch-golang/10-running-the-container-again-12.png)

- **Step 1:** Create a file named `abc` in the container’s root directory.
- **After Step 1:** On the host side, in the `ubuntu-2404-rootfs` directory, you will notice that the file `abc` is also visible from the host.


***Why can the host see the **`abc`** file created inside the container?***

- **chroot does not create an independent filesystem; the filesystem is shared with the host**
  - Because `chroot` only changes the process’s root directory view and does not copy or isolate the underlying filesystem, file operations inside the container (e.g., `touch /abc`) are actually written directly to the host at `/home/laborant/container/ubuntu-2404-rootfs/abc`.
- **No independent mount namespace**
  - `chroot` does not create a separate mount namespace. This means that processes inside the container share the same filesystem mount structure (mount table) as the host. As a result, file operations inside the container directly affect the host’s filesystem.
- **No union filesystem**
  - Our code uses a simple `chroot` and does not employ a union filesystem like modern containers (e.g., Docker). A union filesystem (such as `OverlayFS`) separates container writes from the underlying rootfs, storing changes in a writable layer without affecting the base rootfs.


## Step 3 - Process Tree Isolation Using PID Namespace

**`Goal`:** Learn the concept of the PID namespace and use `CLONE_NEWPID` to provide a process with an independent process ID space, so that processes in different namespaces have isolated PIDs.


Ref: [pid\_namespaces(7) - Linux manual page](https://man7.org/linux/man-pages/man7/pid_namespaces.7.html)

#### What is PID Namespace?

![Step 3 - Process Tree Isolation Using PID Namespace — diagram](/images/containers-from-scratch-golang/11-pid-namespace-drawio.svg)

- **Core Concepts**
  - In each PID namespace, process IDs start from 1 and are independent of the host or other namespaces.
  - Processes inside the container can only see other processes within the same namespace and cannot see host or other container processes.
  - The first process entering a new PID namespace receives `PID 1`, acting like an independent system’s `init` process, responsible for managing child processes (e.g., reaping zombie processes).
- **Example**
  - On the host, suppose there is a process with PID 1000 (e.g., bash).
  - Inside a container with `CLONE_NEWPID` enabled, running a new process (e.g., bash) will be assigned PID 1.
  - Inside the container, `/proc/1` points to the container’s bash, while the host’s PID 1000 is invisible to the container.

#### Benefits

- **Process Isolation**
  - Processes inside a container cannot perceive or interfere with host or other container processes. For example, a container process cannot terminate host processes using the `kill` command, preventing malicious code inside the container from affecting the host.
- **Simulating an Independent System**
  - The first process inside the container (PID 1) can act like a traditional OS `init` process, managing child processes or handling signals (e.g., SIGTERM).
- **Preventing PID Conflicts**
  - Without PID namespaces, container processes share the same PID space as the host, which can lead to PID conflicts or accidental interference.
  - With PID namespaces, container PIDs are independent, simplifying process management and debugging.
- **Integration with `/proc` Filesystem**
  - The `/proc` filesystem dynamically reflects the current PID namespace. With `CLONE_NEWPID` and an isolated `/proc` mount, `/proc` inside the container only shows container processes, enhancing isolation.

#### Limitations and Characteristics

- **Hierarchy**
  - PID namespaces are hierarchical. Processes in a child namespace are invisible to the parent namespace, but the parent can see child namespace processes via `/proc` (with different PIDs).
  - For example, PID 1 inside the container may correspond to a different PID (e.g., 1234) on the host.
- **Special Role of PID 1**
  - In a PID namespace, PID 1 is responsible for reaping child processes (e.g., cleaning up zombie processes). If PID 1 exits, other processes in the namespace are typically terminated as well.
- **Usually Combined with Other Namespaces**
  - PID namespaces are often used together with other namespaces (e.g., UTS, Mount) to achieve complete container isolation.

### **Starting the Experiment**

#### Running the `ps` Command for the First Time

![Running the ps Command for the First Time — screenshot](/images/containers-from-scratch-golang/12-running-the-ps-command-for-the-first-time-12.png)

When running the `ps` command on the **`host`**, you can retrieve the running processes.

However, inside the **container**, running `ps` returns an error:

```txt
Error, do this: mount -t proc proc /proc
```

`ps` is a tool used to display process information, and it relies on Linux’s **`procfs`** (`/proc` filesystem) to obtain process-related data. `/proc` is a virtual filesystem that dynamically reflects the system’s processes, kernel state, and other information, for example:

- `/proc/[pid]`: Directory for each process, containing its status, memory usage, etc. (e.g., `/proc/1/status`).
- `/proc/self`: Points to information about the current process.
- `/proc/cpuinfo`: CPU information.
- `/proc/meminfo`: Memory information.

In our `rootfs` (`/home/laborant/container/ubuntu-2404-rootfs`), the `/proc` directory might just be an empty regular directory (procfs is not mounted), because `chroot` does **not automatically mount procfs**.

Therefore, when we run `ps` inside the container, it tries to read process information from `/proc`. If `/proc` is not correctly mounted, `ps` cannot access valid procfs data (it might be empty or still pointing to the host’s `/proc`) and fails, resulting in the error.

#### Mounting the `/proc` Directory

```go
func child() {
	fmt.Printf("Running %v\n", os.Args[2:])

	cmd := exec.Command(os.Args[2], os.Args[3:]...)
	cmd.Stdin = os.Stdin
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr

	must(syscall.Sethostname([]byte("baconayo-container")))
	must(syscall.Chroot("/home/laborant/container/ubuntu-2404-rootfs"))
	must(os.Chdir("/"))
	must(syscall.Mount("proc", "proc", "proc", 0, ""))

	must(cmd.Run())

	must(syscall.Unmount("proc", 0))
}
```
After understanding the issue, we try to mount the `/proc` directory inside our child process.

In the `child` function, we use `syscall.Mount` to mount `/proc`:

- This line of code mounts a new `procfs` at the container’s `/proc` directory (i.e., `/home/laborant/container/ubuntu-2404-rootfs/proc`) and binds it to the container’s PID namespace.

Additionally, don’t forget that when exiting or terminating the process (container), you should use `syscall.Unmount` to release the `proc` mount.

![Mounting the /proc Directory — screenshot](/images/containers-from-scratch-golang/13-mounting-the-proc-directory-12.png)

After running the modified program again, we observe the situation shown in the image on the left using the `mount` command:

- On the **`host`**, we can see a mount point named `proc` mounted on the `proc` directory inside our `ubuntu-2404-rootfs` directory.
- Inside the **`container`**, we can see that the `proc` mount point has been successfully mounted.

![Mounting the /proc Directory — screenshot](/images/containers-from-scratch-golang/14-mounting-the-proc-directory-13.png)

Next, we check the output of the `ps` command again.

This time, inside the container, we can successfully retrieve process information. However, if we look closely, we may notice that the process information appears somewhat unusual.


![Mounting the /proc Directory — screenshot](/images/containers-from-scratch-golang/15-mounting-the-proc-directory-14.png)

Let’s compare the processes seen inside the **`container`** and on the **`host`**, and we’ll be surprised to find that our container can still see host processes—for example, PIDs 2184, 2185, 2186, 7633, 7667, 7673, 7679.

For a container environment, this is clearly ***unsafe and unacceptable***. So, what are we still missing to achieve proper PID isolation?


#### Adding the `CLONE_NEWPID` Flag

```go
func run() {
	fmt.Printf("Running %v\n", os.Args[2:])

	cmd := exec.Command("/proc/self/exe", append([]string{"child"}, os.Args[2:]...)...)
	cmd.Stdin = os.Stdin
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	cmd.SysProcAttr = &syscall.SysProcAttr{
		Cloneflags: syscall.CLONE_NEWUTS | syscall.CLONE_NEWPID,
	}

	must(cmd.Run())
}為了能達到 Process isolation，我們需透過 PID Namespace 達成目標。方法也非常的簡單，只需要在 run function 內加上 syscall.CLONE_NEWPID flag 就可以了。
```
To achieve process isolation, we need to use a **PID namespace**. The method is quite simple: just add the `syscall.CLONE_NEWPID` flag in the `run` function.


![Adding the CLONE_NEWPID Flag — screenshot](/images/containers-from-scratch-golang/16-adding-the-clone-newpid-flag-15.png)

Let’s try running the container with the `syscall.CLONE_NEWPID` flag enabled.

Now, inside the container environment, we can no longer see the host’s processes, and the initial process has `PID 1`.

So far, we have successfully achieved ***process tree isolation.*


## Step 4 - Dive Deep into Mount Namespace

**`Goal`:** Learn the concept of the **Mount namespace** and use `CLONE_NEWNS` to provide a process with an independent filesystem mount structure (mount table), so that processes in each namespace see mount points isolated from other namespaces.<br /><br />Ref: [mount(2) - Linux manual page](https://man7.org/linux/man-pages/man2/mount.2.html)

#### Why we need Mount Namespace?

In **Step 3**, we already used `syscall.Mount` to mount the `/proc` directory inside the container, and it worked correctly. So why do we still need to specifically discuss **mount namespaces**?

The reason is that the primary purpose of a **Mount Namespace** is to provide processes with an independent filesystem mount view, which is especially important for containerization. Its specific roles include:

1. **Filesystem Isolation**
   - Each container can have its own mount structure, isolated from the host and other containers.
   - For example, `/proc` inside a container can be mounted with a dedicated `procfs` that only shows container processes, preventing leakage of host information (as we did in Step 3).
2. **Simulating an Independent System Environment**
   - Mount namespaces allow containers to mount their own filesystems (e.g., `/proc`, `/dev`, `/sys`), simulating a complete operating system environment.
   - For instance, in our code, we manually mounted `procfs` (`syscall.Mount("proc", "proc", "proc", 0, "")`) to provide an independent `/proc` for the container’s PID namespace. Mount namespaces ensure these mounts do not affect the host.
3. **Flexible Filesystem Configuration**
   - Containers can mount different filesystems as needed (e.g., `tmpfs`, `OverlayFS`), and these operations only affect the current mount namespace.
   - For example, Docker uses `OverlayFS` to provide layered filesystems for containers, ensuring modifications inside the container do not affect the base image.
4. **Preventing Mount Point Leakage**
   - Without a mount namespace, host mount points (e.g., `/mnt/data`) could be visible inside the container, posing a security risk. Mount namespaces ensure that the container only sees the necessary mount points.

### Starting the Experiment

#### Mounting a tmpfs

In the previous steps, we already mounted `/proc` inside the container. This time, we will try mounting a **temporary filesystem** into the container.

First, on the **host**, create a directory named `baconyao_temp` inside `ubuntu-2404-rootfs`.

```go
func child() {
	fmt.Printf("Running %v\n", os.Args[2:])

	cmd := exec.Command(os.Args[2], os.Args[3:]...)
	cmd.Stdin = os.Stdin
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr

	must(syscall.Sethostname([]byte("baconayo-container")))
	must(syscall.Chroot("/home/laborant/container/ubuntu-2404-rootfs"))
	must(os.Chdir("/"))
	must(syscall.Mount("proc", "proc", "proc", 0, ""))
	must(syscall.Mount("bacon", "baconyao_temp", "tmpfs", 0, "")) // mount

	must(cmd.Run())

	must(syscall.Unmount("proc", 0))
	must(syscall.Unmount("baconyao_temp", 0)) // unmount
}
```
Next, following the same approach we used to mount `/proc`, we mount a directory named `baconyao_temp` inside the container.

- **`source: "bacon"`**: This specifies the source of the filesystem to mount. The value "bacon" is unusual and likely a placeholder or a specific device name. In practice, this could refer to a device (e.g., /dev/sda1) or a pseudo-filesystem source like tmpfs. For tmpfs, the source is often arbitrary or ignored, so "bacon" is just a dummy value.
- **`target: "baconyao_temp"`**: This is the `mount point`, the directory where the filesystem will be mounted. In this case, it’s likely a directory named baconyao\_temp. The directory must exist before mounting.
- **`fstype: "tmpfs"`**: The filesystem type is tmpfs, which is an in-memory filesystem. tmpfs stores files in RAM, making it fast but volatile (data is lost on reboot).
- **`flags: 0`**: No specific mount flags are provided (e.g., no `MS_RDONLY` for read-only or `MS_NOEXEC` to prevent execution). This means the mount uses default behavior.
- **`data: ""`**: No additional filesystem-specific options are provided.

![Mounting a tmpfs — screenshot](/images/containers-from-scratch-golang/17-mounting-a-tmpfs-12.png)

Next, after running the program, we will see the new `baconyao_temp` mount both on the host and inside the container.

![Mounting a tmpfs — screenshot](/images/containers-from-scratch-golang/18-mounting-a-tmpfs-13.png)

Similarly, if we create a file named `ABC` inside the `baconyao_temp` mount point within the container, it will also be visible and accessible on the host.

So far, we have ***not yet achieved mount point isolation***. The question is: how can we fix this?

#### Adding the `CLONE_NEWNS` Flag

```go
func run() {
    fmt.Printf("Running %v\n", os.Args[2:])

    cmd := exec.Command("/proc/self/exe", append([]string{"child"}, os.Args[2:]...)...)
    cmd.Stdin = os.Stdin
    cmd.Stdout = os.Stdout
    cmd.Stderr = os.Stderr
    cmd.SysProcAttr = &syscall.SysProcAttr{
        Cloneflags: syscall.CLONE_NEWUTS |
                    syscall.CLONE_NEWPID |
                    syscall.CLONE_NEWNS,
    }

    must(cmd.Run())
}
```
We just need to add the `CLONE_NEWNS` flag in the `run` function, which creates an independent **mount namespace** for the container. This ensures that mount operations inside the container (such as mounting `/proc` or `/baconyao_temp`) do not affect the host’s mount table.


#### Mount Propagation

Since I initially followed [Building Containers from Scratch with Go](https://learning.oreilly.com/videos/building-containers-from/9781491988404/9781491988404-video312009/) for implementation, after adding the `CLONE_NEWNS` flag, I noticed that it did **not behave as expected**. The container’s `/proc` and `/baconyao_temp` mount points were still visible and accessible from the host.

After researching for a while, I realized that the issue was caused by ***mount propagation***.

So, what is **`Mount Propagation`**?

> The **mount namespace** was the first namespace supported in Linux, introduced in Linux 2.4.19 in 2002.

> Initially, user-space mounts were completely isolated. For example, if a device (like a CD or DVD) was inserted on the host, the only way to make it visible in all mount namespaces was to mount it separately in each namespace, which was cumbersome.

> To address this issue, **shared subtrees** were introduced in Linux 2.6.15. The core feature of shared subtrees is that they allow mount and unmount events to **propagate automatically and controllably** between different namespaces. This mechanism is known as **mount propagation**.

正是由於 `mount propagation` 這個機制，儘管有使用 `CLONE_NEWNS` flag，在新的 mount point 建立時，它依然會繼承父 namespace 的掛載點樹狀結構，而且預設 propagation mode 是 **`shared`**。意味著 `child` namespace 裡的 `mount`/`unmount` 會**同步到 `parent` namespace**。所以在 `child` process 裡做的 `syscall.Mount("bacon", "baconyao_temp", "tmpfs", ...)`，也會出現在 `host` 的 mount list (`/proc/self/mounts` / `mount`)。

Because of the **mount propagation** mechanism, even when using the `CLONE_NEWNS` flag, newly created mount points still inherit the parent namespace’s mount tree, and the default propagation mode is **`shared`**. This means that mount/unmount operations in the child namespace can ***propagate to the parent namespace.*

Mount propagation defines the relationships between mount objects. The system uses these relationships to determine how mount or unmount events in one mount object affect other mount objects. There are several types of propagation relationships:

<table header-row="true">
<tr>
<td>
Flag
</td>
<td>
Propagation Behavior
</td>
<td>
Can Be Bound?
</td>
<td>
Use Case Example
</td>
</tr>
<tr>
<td>
`MS_SHARED`
</td>
<td>
Sends/receives mount events to/from peers
</td>
<td>
Yes
</td>
<td>
Shared filesystems in containers
</td>
</tr>
<tr>
<td>
`MS_SLAVE`
</td>
<td>
Receives events from master, no sending
</td>
<td>
Yes
</td>
<td>
Controlled visibility in namespaces
</td>
</tr>
<tr>
<td>
`MS_PRIVATE`
</td>
<td>
No propagation in or out
</td>
<td>
Yes
</td>
<td>
Isolated mounts in containers
</td>
</tr>
<tr>
<td>
`MS_UNBINDABLE`
</td>
<td>
No propagation, cannot be bound
</td>
<td>
No
</td>
<td>
Secure, isolated mounts
</td>
</tr>
</table>

- **Shared (MS\_SHARED)**
  - This mount point shares mount and unmount events with other mount points in the same **peer group**. Propagation is **`bidirectional`**: mount events from one mount object propagate to other mount objects across mount namespaces, and vice versa.
- **Slave (MS\_SLAVE)**
  - Propagation is **`unidirectional`**, meaning events only propagate from the master to the slave.
- **Private (MS\_PRIVATE)**
  - Mount and unmount events in different mount namespaces do ***not affect each other.*
- **Unbindable (MS\_UNBINDABLE)**
  - Similar to private mounts, an unbindable mount ***cannot propagate events*** and also ***cannot be bound*** to other mount points.

#### Checking the Host Environment

How can we check the current system’s **mount propagation** settings? There are two ways:

**Method 1 – Using the following command**

```bash
cat /proc/self/mountinfo | grep shared:
```

You might see entries like `shared:1` or `shared:2`, which indicate that this mount belongs to **shared group 1**.

- `shared:N` → This mount is shared and propagates events with other members of group N.
- `master:N` → This mount is a slave; it follows the master N mount but does not propagate back.
- `unbindable` → Cannot be used in bind mounts.
- `private` → Completely independent; does not propagate events.

![Checking the Host Environment — screenshot](/images/containers-from-scratch-golang/19-screenshot-2025-08-26-1-44-34.png)

**Method 2 – Using the `findmnt` command**

From this, we can see that the root directory `/` is **shared**. Therefore, if no special configuration is applied, creating new mount points inside the container using a mount namespace will still ***propagate back to the host.*

![Checking the Host Environment — screenshot](/images/containers-from-scratch-golang/20-screenshot-2025-08-26-1-44-44.png)

#### **Solution for Mount Propagation**

Because the host’s default propagation mode is **shared**, all directories under the root (`/`) inherit this state. This means that the `chroot(.../ubuntu-2404-rootfs)` we performed earlier also has a **shared** propagation mode. As a result, even with a Mount Namespace, proper isolation cannot be achieved.

Therefore, in the `child()` function, we first need to set the **root mount** to **private**, so that new mounts inside the container will **not propagate back to the host**.

This is exactly the first step performed by container runtimes such as **`Docker`** or **`runc`**.

```go
func child() {
	fmt.Printf("Running %v\n", os.Args[2:])

	cmd := exec.Command(os.Args[2], os.Args[3:]...)
	cmd.Stdin = os.Stdin
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr

	must(syscall.Sethostname([]byte("baconayo-container")))
	must(syscall.Mount("", "/", "", syscall.MS_REC|syscall.MS_PRIVATE, ""))
	must(syscall.Chroot("/home/laborant/container/ubuntu-2404-rootfs"))
	must(os.Chdir("/"))

	must(syscall.Mount("proc", "proc", "proc", 0, ""))
	must(syscall.Mount("bacon", "baconyao_temp", "tmpfs", 0, ""))

	must(cmd.Run())

	must(syscall.Unmount("proc", 0))
	must(syscall.Unmount("baconyao_temp", 0))
}
```
In the `child()` function, **before the child process performs `chroot`**, add the following code to set the host’s root directory `/` to **`MS_PRIVATE`**. Also, use `MS_REC` to apply this setting ***recursively to all submounts.*

```go
	must(syscall.Mount("", "/", "", syscall.MS_REC|syscall.MS_PRIVATE, ""))
```

**MS\_REC**

```txt
Used in conjunction with MS_BINDto create a recursive bind mount, and in conjunction with the propagation type flags to recursively change the propagation type of all of the mounts in a subtree.
```


![Solution for Mount Propagation — screenshot](/images/containers-from-scratch-golang/21-solution-for-mount-propagation-14.png)

From the figure on the left, we can observe that the `proc` and `bacon` mount points inside the container appear **only within the container** and do **not** show up on the host.

In this way, we have successfully achieved **mount isolation**.

#### Elegant Solution for Mount Propagation

When I revisited Liz Rice’s demo video ([Containers From Scratch • Liz Rice • GOTO 2018](https://youtu.be/8fi7uSYlOdc?si=PSqERqzmm4wMqsr0&t=1364)), I discovered a **cleaner and more canonical solution**.

1. We no longer need to manually remount the host’s root filesystem in the `child` function:
   1. Remove `must(syscall.Mount("", "/", "", syscall.MS_REC|syscall.MS_PRIVATE, ""))` from the `child` function.
2. Instead, set it up in the `run` function using `Unshareflags`. An example is as follows:

```go
func run() {
    fmt.Printf("Running %v\n", os.Args[2:])

    cmd := exec.Command("/proc/self/exe", append([]string{"child"}, os.Args[2:]...)...)
    cmd.Stdin = os.Stdin
    cmd.Stdout = os.Stdout
    cmd.Stderr = os.Stderr
    cmd.SysProcAttr = &syscall.SysProcAttr{
        Cloneflags: syscall.CLONE_NEWUTS |
                    syscall.CLONE_NEWPID |
                    syscall.CLONE_NEWNS,
        Unshareflags: syscall.CLONE_NEWNS,
    }

    must(cmd.Run())
}
```

***So, what is `unshare`?***

> Linux provides several system call APIs for managing namespaces, including `clone()`, `unshare()`, and `setns()`.

- **clone()**
  - Implements a system call for creating a new process, allowing the specification of `CLONE_NEW*` flags to create new namespaces.
  - The newly created process belongs to the specified namespace, and any subsequent processes it spawns will, by default, be part of the same namespace.
- **unshare()**
  - Used to detach the current process from its existing namespace and join a new namespace.
  - The unshare system call allows a process to create new namespaces or disassociate from existing ones, effectively isolating certain resources (e.g., mount points, process IDs, network stack) from the parent process or other processes. The Unshareflags field specifies which namespaces to unshare.
  - In Golang, this field is used when starting a new process (e.g., via `exec.Command`) to control the namespace isolation behavior. It’s distinct from Cloneflags, which is used when creating a new process or thread with `clone(2)`, but the flags often overlap because both system calls deal with namespaces.
- **setns()**
  - Moves a process into an existing namespace. This operation updates the process’s corresponding entries in `/proc/[pid]/ns`.

## Step 5 - Resource Control through Control Group

`Goal`: Gain a preliminary understanding of **Cgroup** functionality by creating a cgroup with a **memory limit** and adding the current program’s PID to it.

This section is inspired by Liz Rice’s [Containers From Scratch • Liz Rice • GOTO 2018](https://youtu.be/8fi7uSYlOdc?si=RV7HuFiskev4VS05&t=1597). Her implementation was based on **Cgroup v1**, but since our host is **Ubuntu 24.04**, we will implement it using **Cgroup v2**.

### What is a Control Group?

A **Control Group (cgroup)** is a Linux kernel feature that allows you to **limit and manage system resources** for a group of processes, such as CPU, memory, I/O, and network bandwidth.

In the context of **containers**, cgroups form the **foundation for resource isolation**.

#### Features of Cgroup v2

1. **Unified Hierarchy**
   - All resource controllers are attached to a single tree, making it much cleaner than v1’s multiple trees.
2. **More Consistent Behavior**
   - APIs for all controllers are uniform, making behavior more predictable.
3. **Finer Resource Control**
   - `memory`: Limit memory peak, swap usage, and control OOM behavior.
   - `CPU`: Use `cpu.weight` to control allocation proportion, which is more intuitive than v1’s CPU shares.
   - `I/O`: Supports fine-grained I/O bandwidth control.
4. **Delegation Support**
   - Allows handing over management of a subtree to unprivileged users, which is crucial for **`rootless containers`**.

#### Simple Example

If you want to limit a process to **200MB of memory**, you can do the following (assuming **cgroup v2** is enabled and mounted at `/sys/fs/cgroup`):

```bash
#  Create a new cgroup named test
mkdir /sys/fs/cgroup/test

# Set memory limit
echo 200M > /sys/fs/cgroup/test/memory.max

# Add the current process (or any PID) to the cgroup
echo 12345 > /sys/fs/cgroup/test/cgroup.procs

```

### **Starting the Experiment**

#### Code Implementation - Cgroup v1

```go
// cg is the cgroup v1
func cg() {
	cgroups := "/sys/fs/cgroup/"

	mem := filepath.Join(cgroups, "memory")
	os.Mkdir(filepath.Join(mem, "baconyao"), 0755)
	must(ioutil.WriteFile(filepath.Join(mem, "baconyao/memory.limit_in_bytes"), []byte("999424"), 0700))
	must(ioutil.WriteFile(filepath.Join(mem, "baconyao/memory.memsw.limit_in_bytes"), []byte("999424"), 0700))
	must(ioutil.WriteFile(filepath.Join(mem, "baconyao/notify_on_release"), []byte("1"), 0700))

	pid := strconv.Itoa(os.Getpid())
	must(ioutil.WriteFile(filepath.Join(mem, "baconyao/cgroup.procs"), []byte(pid), 0700))
}
```


First, let's take a look at Liz Rice's **CGroup v1** version.

- `mem := filepath.Join(cgroups, "memory")` means specifying the controller (subsystem) to operate on.
- Under the memory cgroup, a subdirectory `baconyao` is created, representing a new **cgroup group**.
  - Actual path: `/sys/fs/cgroup/memory/baconyao`.
- Set the memory limit `memory.limit_in_bytes` to `999424` bytes (\~976 KB).
- Set the total **memory + swap limit**; here it is also `999424` bytes, meaning swap is not enabled.
- Enable **`notify_on_release`**, so that when the last process in this cgroup exits, the kernel can trigger release actions.
- Finally, get the current process's **`PID`** and write it into `cgroup.procs`, which moves the current process into the specified cgroup.

#### Code Implementation - Cgroup v2

```go
// CGroup v2
func cgv2() {
	cgroups := "/sys/fs/cgroup/"
	path := filepath.Join(cgroups, "baconyao")
	os.Mkdir(path, 0755)

	// Set memory limitation
	must(ioutil.WriteFile(filepath.Join(path, "memory.max"), []byte("999424"), 0700))
	// Disable swap
	must(ioutil.WriteFile(filepath.Join(path, "memory.swap.max"), []byte("0"), 0700))

	// Add the current process (or any PID) to the cgroup
	pid := strconv.Itoa(os.Getpid())
	must(ioutil.WriteFile(filepath.Join(path, "cgroup.procs"), []byte(pid), 0700))
}
```


On the left is my modified **CGroup v2** version, which I used for testing and experimentation on my Ubuntu 24.04 machine.

Finally, we just need to call this function inside the `child` function **before executing `exec.Command`** (i.e., before forking a new process). This ensures that any subsequently forked process (e.g., `/bin/bash`) will be governed by the `baconyao` cgroup.

```go
func child() {
	fmt.Printf("Running %v\n", os.Args[2:])

	cgv2()

	cmd := exec.Command(os.Args[2], os.Args[3:]...)
	...
}
```

#### Why we got `panic: signal :killed` ?

Checking the cgroup’s `memory.events`, I found that the termination was caused by **`oom_kill`**— meaning the process was killed because it exceeded the memory limit set by the cgroup.

![Why we got panic: signal :killed ? — screenshot](/images/containers-from-scratch-golang/22-screenshot-2025-08-26-3-13-24.png)

But why was `oom_kill` triggered?

In my `cgv2()` function, the memory limit was set to **999,424 bytes ≈ 975 KB**.

```go
must(ioutil.WriteFile(filepath.Join(path, "memory.max"), []byte("999424"), 0700))
```

However, even a minimal `/bin/bash` process on Ubuntu consumes several MB of RSS/heap just to start, so it simply cannot run within 1 MB.

As a result:

- The kernel immediately detects that the process exceeded the `memory.max` limit.
- The OOM killer terminates the process.
- The Go parent process receives `signal: killed` and panics.

![Why we got panic: signal :killed ? — screenshot](/images/containers-from-scratch-golang/23-why-we-got-panic-signal-killed-15.png)

Finally, I increased the memory limit to **2,097,152 bytes (≈2 MB)**, which allowed the container to start and run properly.

On the **Host**, you can check the `baconyao` cgroup settings under `/sys/fs/cgroup/baconyao`:

- Use `cat memory.max` to see the memory limit set for the `baconyao` cgroup.
- Use `cat memory.current` to check the current memory usage.

![Why we got panic: signal :killed ? — screenshot](/images/containers-from-scratch-golang/24-why-we-got-panic-signal-killed-16.png)

Next, in Liz Rice’s demo, she uses the `sleep` command to verify that the process is controlled by the specified cgroup. Let’s go through it step by step:

- **Step 1:** Inside the container, run `sleep 1000`.
- **Step 2:** On the **Host**, use `pidof sleep` to check all running `sleep` processes. You’ll see only one, with PID **3554**, which corresponds to the process started inside the container.
- **Step 3:** Check `/sys/fs/cgroup/baconyao/cgroup.procs` on the Host to see if PID 3554 is listed.

This confirms that the `baconyao` cgroup is successfully created and all processes inside the container are managed under it.


## Step 6 - Rootless Container

`Goal`: Previously, we needed root privileges to run our program. In this section, we will explore how to use **`CLONE_NEWUSER`** to allow a regular, unprivileged user to execute the program and enter the container environment.

### What is User namespace？

The purpose of a **User Namespace** is to isolate and separate permission management, mainly in two aspects:

- **UID/GID mapping**
- **Capabilities**

A user’s UID and GID can differ across different user namespaces (similar to how PID namespaces work). That is, a user can be a regular user in one user namespace but have root privileges in another.

Even if the same user is `root`, their permissions inside a container are different from those on the host. This is because Linux introduces the **capabilities** mechanism, which provides fine-grained control over root privileges, reducing the potential attack surface of the system.

### **Starting the Experiment**

#### Operation not permitted

![Operation not permitted — screenshot](/images/containers-from-scratch-golang/25-operation-not-permitted-17.png)

In the Container environment shown on the left, if the program is not executed as `root`, we immediately encounter an **“operation not permitted”** error.

This happens because in **rootless environments** (or in kernels/container runtimes with enhanced security, such as Docker’s rootless mode or systemd’s user namespace), **non-root processes are not allowed to re-execute `/proc/self/exe`**. Attempting to do so directly results in an “operation not permitted” error.


```go
func run() {
	fmt.Printf("Running %v\n", os.Args[2:])

	cmd := exec.Command("/proc/self/exe", append([]string{"child"}, os.Args[2:]...)...)
	cmd.Stdin = os.Stdin
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	cmd.SysProcAttr = &syscall.SysProcAttr{
		Cloneflags: syscall.CLONE_NEWUTS | syscall.CLONE_NEWPID | syscall.CLONE_NEWNS | syscall.CLONE_NEWUSER,
		Unshareflags: syscall.CLONE_NEWNS,
		Credential: &syscall.Credential{Uid: 0, Gid: 0},
		UidMappings: []syscall.SysProcIDMap{
			{ContainerID: 0, HostID: os.Getuid(), Size: 1},
		},
		GidMappings: []syscall.SysProcIDMap{
			{ContainerID: 0, HostID: os.Getgid(), Size: 1},
		},
	}

	must(cmd.Run())
}
```
By simply adding `CLONE_NEWUSER` to the `Cloneflags` in the `run` function and configuring the following settings:

- **`Credential…`**
  - Map yourself as root (UID=0, GID=0) inside the new user namespace.
- **`UidMappings…`**
  - Set UID mapping: container’s UID 0 → your host UID.
- **`GidMappings…`**
  - Set GID mapping: container’s GID 0 → your host GID.

After this setup, a ***non-root program can have “fake root privileges”** inside the new user namespace:

- Inside the namespace, it appears as UID 0 (root), but this root actually maps to your unprivileged host UID.
- Therefore, it has full privileges within the container but **cannot affect the host system**, preserving security.

#### Permission denied

![Permission denied — screenshot](/images/containers-from-scratch-golang/26-permission-denied-18.png)

**Step 1**

After modifying the `run` function, when we run our example program again as a non-root user, we encounter a new issue:

`panic: open /sys/fs/cgroup/baconyao/memory.max: permission denied`

This problem is clearly related to cgroups. The reason is that many operations in **cgroup** (especially **cgroup v2**) require **root privileges**.

***Further Exploration of Cgroup Permissions***

- **Cgroup Filesystem Operations**
  - Cgroup configurations (e.g., `memory.max`, `cpu.max`) are managed via the filesystem interface under `/sys/fs/cgroup`. These files are typically owned by `root`, and write permissions are restricted to root or specific privileged users.
  - For example, in my code, writing to `/sys/fs/cgroup/baconyao/memory.max` and `cgroup.procs` requires write access to `/sys/fs/cgroup`, which usually demands root privileges.
- **Creating and Assigning Cgroups**
  - Creating new cgroup directories (e.g., `/sys/fs/cgroup/baconyao`) and assigning processes to a specific cgroup (writing to `cgroup.procs`) generally requires root privileges because it involves system-level resource management.
- **Exception: Delegated Cgroups**
  - In cgroup v2, an administrator can delegate control of certain cgroup subtrees to non-root users. For example, `/sys/fs/cgroup/user.slice` can be configured so that specific users have permission to manage their child cgroups.
  - This delegation must be pre-configured by the system administrator and still requires initial root privileges to set up the delegation.

**Permission Issues with `/sys/fs/cgroup`**

- In cgroup v2, control files like `memory.max` are **by default writable only by the host’s root**.
- When we try to `open /sys/fs/cgroup/.../memory.max` from within a child namespace:
  - Inside the user namespace, we appear as root (UID 0).
  - However, the VFS (Virtual Filesystem) checks the **real UID/GID on the host**, which is still a non-root user.
  - As a result, the operation fails with `permission denied`.

**Step 2**

Since we haven’t configured **`Delegated cgroups`**, the only practical workaround to successfully run our example program is to **comment out the `cgv2` call inside the `child` function** and execute the container.

After running, you’ll see the prompt as `root@baconyao-container:/#`. Although it shows **root**, this is a “fake root”—from the host’s perspective, it’s just a normal user.

Inside the container, you can verify this by running `id` command, this will show the current UID and GID as 0 (root) **inside the user namespace**, while on the host they map to your actual non-root UID/GID.

## Conclusion

In this set of notes, we followed Liz Rice’s demo to learn some fundamental concepts of containers, and through additional extensions, we gained a deeper understanding of the importance of these basic namespaces for container isolation.

However, there are still many areas to explore and enhance, such as:

- **`Control Group v2`** for resource management
- **`Network Namespace`** for container networking
- **`IPC Namespace`** for inter-process communication isolation
- **`Time Namespace`** for controlling time-related aspects

Each namespace is a topic worthy of deeper study.

Additionally, `chroot` is considered an older approach; I plan to write a dedicated article exploring `pivot_root`.

Finally, **`rootless containers`** are undeniably important for container security, and this will be a focus of my future explorations in system security.
