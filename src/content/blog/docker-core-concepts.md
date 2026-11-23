---
title: "A Complete Journey Through Docker's Core Concepts | Docker 360"
description: "Docker from the ground up: containers vs VMs, architecture, images, networks, volumes, Dockerfile builds, registries and every core command with real output."
slug: "docker-core-concepts"
---

By Rao Shahzaib · DevOps

A Complete Journey through Docker's Core Concepts | Docker 360

![A Complete Journey through Docker's Core Concepts | Docker 360](/images/docker-core-concepts/01-installation.png)

## Introduction And Architecture

Docker is an open container management platform. It is a software platform used to run applications contained within containers. Docker helps you separate your applications from your infrastructure, allowing you to deliver software quickly.

With Docker, you can manage your infrastructure in the same way you manage your applications. By leveraging Docker's technology, we can build, test, and deploy code quickly, significantly reducing the waiting time between writing code and running it in production.

### VMs vs Containers

![VMs vs Containers](/images/docker-core-concepts/02-download.png)

##### Virtual Machine:

A Virtual Machine (VM) is a system that operates just like a real computer. VMs mimic physical hardware and allow a single server to transform into multiple servers. This is made possible through a technology called a hypervisor, which permits multiple VMs to run on the same machine. Each VM includes a complete operating system.
##### Containers:

In contrast, containers isolate different application environments from each other and share only the underlying operating system (OS) kernel. They provide an abstraction layer that packages code and its dependencies together. By default, a container is effectively isolated from other containers and its host machine. You can control how much a container's network, storage, or other underlying subsystems are isolated from other containers or the host machine.
Multiple containers can run on a single machine, sharing the same OS kernel with other containers. Each container operates as an isolated process within the user space. Containers require less space compared to virtual machines (container images are usually just a few MBs in size), can handle more applications, and reduce the need for multiple VMs and operating systems.
##### Docker architecture:

Docker uses a client-server architecture. The Docker client interacts with the Docker daemon, which is responsible for creating, running, and managing your Docker containers. The Docker client and daemon communicate using the REST API, either through UNIX sockets or network interfaces.

![Docker architecture](/images/docker-core-concepts/03-download-1-.png)

##### Install Docker
##### 1. Update Package Database:

sudo apt-get update
##### 2. Install Prerequisites:

sudo apt-get install apt-transport-https ca-certificates curl software-properties-common

**3. Add Docker GPG Key:**

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

**4. Set Up Docker Repository:**

sudo add-apt-repository "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
##### 5. Update Package Database Again:

sudo apt-get update
##### 6. Install Docker:

sudo apt-get install docker-ce
##### 6. Verify Docker Installation:

sudo docker --version

#### Docker Command Overview

```
docker help
```
Let's run some basic Docker commands and see:

```
ubuntu@Docker-Lab:~$ docker help

Usage: docker [OPTIONS] COMMAND

A self-sufficient runtime for containers

Common Commands:
 run Create and run a new container from an image
 exec Execute a command in a running container
 ps List containers
 build Build an image from a Dockerfile
 pull Download an image from a registry
 push Upload an image to a registry
 images List images
 login Log in to a registry
 logout Log out from a registry
 search Search Docker Hub for images
 version Show the Docker version information
 info Display system-wide information
```

```
docker ps
```

```
ubuntu@Docker-Lab:~$ docker ps
CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES
```

```
docker image ls
```

```
ubuntu@Docker-Lab:~$ docker image ls
REPOSITORY TAG IMAGE ID CREATED SIZE
```

```
docker network ls
```

```
ubuntu@Docker-Lab:~$ docker network ls
NETWORK ID     NAME DRIVER     SCOPE
e10e6b7a8a46 bridge bridge local
6936a8aafc90 host host local
d76ccf9fa189 none null local
```

```
docker volume ls
```

```
ubuntu@Docker-Lab:~$ docker volume ls
DRIVER VOLUME NAME
```

##### Create Your First Container in Docker

"There are several commands to manage Docker containers and images. Let's see if there are any images available in our local Docker library or not."

```
docker image ls
```

"The 'Docker images' command provides us with a list of local images that can be used to create Docker containers. In the given output above, no local images are being displayed."

"Let's use the `docker search ubuntu` command to search for an image to download."

```
docker image pull ubuntu:18.04
```

```
ubuntu@Docker-Lab:~$ docker image pull ubuntu:18.04
18.04: Pulling from library/ubuntu
Digest: sha256:152dc042452c496007f07ca9127571cb9c29697f4
Status: Image is up to date for ubuntu:18.04
docker.io/library/ubuntu:18.04
```

"You can check if the image has been downloaded by using the following command:"

```
docker image ls
```

```
ubuntu@Docker-Lab:~$ docker image ls
REPOSITORY TAG IMAGE ID CREATED SIZE
ubuntu 18.04 f9a80a55f492 4 months ago 63.2MB
ubuntu@Docker-Lab:~$
```

"Create a Docker container using the run command and specify that the container should run the Bash shell."

```
docker run -it ubuntu /bin/bash
```

```
ubuntu@Docker-Lab:~$ docker run -it ubuntu:18.04 /bin/bash
root@47613a6e0f09:/#
```

In this command:

docker run is used to create and run a new container.

-it flag enables interactive mode with a terminal.

ubuntu is the name of the Docker image.

/bin/bash specifies the Bash shell to be run inside the container.
Press **[ctrl+pq]** to exit
```
docker container ls
```

```
ubuntu@Docker-Lab:~$ docker container ls
CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES
47613a6e0f09 ubuntu:18.04 "/bin/bash" 2 minutes ago Up 2 minutes gallant_swanson
ubuntu@Docker-Lab:~$
```

"To remove a container, simply use the `rm` command provided by Docker, like this:"

```
docker container rm 0efe11b043cc
```

```
ubuntu@Docker-Lab:~$ docker container rm 0efe11b043cc
0efe11b043cc
ubuntu@Docker-Lab:~$
```

Replace `[container_name_or_id]` with the actual name or ID of the container you want to remove. This command will remove the specified Docker container from your system.

#### Docker Container run
"The 'Docker run' command is a combination of creating and starting a container. First, it creates a container and then starts it. The 'Docker run' command creates a writable container layer over the specified image and then starts it using the specified command."
```
docker container run -d ubuntu:18.04 sleep 30
```

Docker allows you to run a container in interactive mode as well

```
docker container run -it ubuntu:14.04 /bin/bash
```

```
ubuntu@Docker-Lab:~$ docker container run -d ubuntu:18.04 sleep 30
8668c2250985bc28066e1b5a9965817ef6222ecc680b72804dcff5e53d4b550d
ubuntu@Docker-Lab:~$ docker container run -it ubuntu:18.04 /bin/bash
root@779c3d782a4e:/#
```

#### Docker Container - Start and Stop

```
docker container ls
```

```
ubuntu@Docker-Lab:~$ docker container ls
CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES
779c3d782a4e ubuntu:18.04 "/bin/bash" 2 minutes ago Up 2 minutes interesting_margulis
ubuntu@Docker-Lab:~$
```

```
docker container stop [container_name_or_id]
```

```
ubuntu@Docker-Lab:~$ docker container stop 779c3d782a4e
779c3d782a4e
ubuntu@Docker-Lab:~$
ubuntu@Docker-Lab:~$ docker container ls -a
CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES
779c3d782a4e ubuntu:18.04 "/bin/bash" 6 minutes ago Exited (0) 50 seconds ago interesting_margulis
ubuntu@Docker-Lab:~$
```

```
docker container start [container_name_or_id]
```

```
ubuntu@Docker-Lab:~$ docker container start 779c3d782a4e
779c3d782a4e
ubuntu@Docker-Lab:~$ docker container ls
CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES
779c3d782a4e ubuntu:18.04 "/bin/bash" 7 minutes ago Up 4 seconds interesting_margulis
ubuntu@Docker-Lab:~$
```

```
docker container pause [container_name_or_id]
```

```
ubuntu@Docker-Lab:~$ docker container pause 779c3d782a4e
779c3d782a4e
ubuntu@Docker-Lab:~$ docker container ls -a
CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES
779c3d782a4e ubuntu:18.04 "/bin/bash" 9 minutes ago Up About a minute (Paused) interesting_margulis
ubuntu@Docker-Lab:~$
```

```
docker container unpause [container_name_or_id]
```

```
ubuntu@Docker-Lab:~$ docker container unpause 779c3d782a4e
779c3d782a4e
ubuntu@Docker-Lab:~$ docker container ls
CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES
779c3d782a4e ubuntu:18.04 "/bin/bash" 10 minutes ago Up 3 minutes interesting_margulis
ubuntu@Docker-Lab:~$
```

#### Inspecting Docker Objects
"`docker inspect` ek command hai jo Docker objects jaise ki docker images, containers, networks, volumes, wagaira ke baare mein low-level information provide karta hai. Aam taur par, `docker inspect` JSON format mein results return karta hai."
```
docker container inspect [container_name_or_id]
```

```
ubuntu@Docker-Lab:~$ docker container ls
CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES
779c3d782a4e ubuntu:18.04 "/bin/bash" 12 minutes ago Up 5 minutes interesting_margulis
ubuntu@Docker-Lab:~$ docker container inspect 779c3d782a4e
[
 {
 "Id": "779c3d782a4e96f49cecb22046e288aa346387d690227db19a9c7c0d07f920b2",
 "Created": "2023-10-24T17:25:07.69390592Z",
 "Path": "/bin/bash",
 "Args": [],
 "State": {
...
ubuntu@Docker-Lab:~$
```

#### Docker Container logs

"If you are running your container in detached mode (-d) or through the Docker remote API, you won't see any logs in the console. To access the logs of a running container, you need to use the `docker logs` command."

-f --follow Follow log output ( if you want to see logs continuously)

```
docker container logs [container_name_or_id]
```

```
ubuntu@Docker-Lab:~$ docker container logs 779c3d782a4e
root@779c3d782a4e:/#
ubuntu@Docker-Lab:~$ docker container run -d ubuntu:18.04 sleep 30
bash: ubuntu@Docker-Lab:~$: command not found
root@779c3d782a4e:/# 8668c2250985bc28066e1b5a9965817ef6222ecc680b72804dcff5e53d4b550d
bash: 8668c2250985bc28066e1b5a9965817ef6222ecc680b72804dcff5e53d4b550d: command not found
root@779c3d782a4e:/#
ubuntu@Docker-Lab:~$ docker container run -it ubuntu:18.04 /bin/bash
bash: ubuntu@Docker-Lab:~$: command not found
root@779c3d782a4e:/#
root@779c3d782a4e:/#
bash: root@779c3d782a4e:/#: No such file or directory
root@779c3d782a4e:/# exit
root@779c3d782a4e:/# exit
ubuntu@Docker-Lab:~$
```

##### Docker Restart and Rename

```
docker rename old_container new_container
```

```
ubuntu@Docker-Lab:~$ docker container ls
CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES
779c3d782a4e ubuntu:18.04 "/bin/bash" 21 minutes ago Up 14 minutes interesting_margulis
ubuntu@Docker-Lab:~$ docker container rename interesting_margulis my_os
ubuntu@Docker-Lab:~$ docker container ls
CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES
779c3d782a4e ubuntu:18.04 "/bin/bash" 21 minutes ago Up 14 minutes my_os
ubuntu@Docker-Lab:~$
```

##### Docker Port Mapping
"When you create a container using `docker create` or `docker run`, it doesn't automatically expose its ports to the outside world. To make ports accessible for external services, we use the `--publish` or `-p` flag. This creates a firewall rule that maps a container port to a port on the Docker host, which is accessible externally to the outside world."
```
docker container run -itd -p 3600:80 nginx
```

```
ubuntu@Docker-Lab:~$ docker container run -itd -p 8080:80 nginx
b3d7fa3664af23b37d71a94a990ee9023f6eb055f9b3f938c9164172a3a52d1e
ubuntu@Docker-Lab:~$ docker container ls
CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES
b3d7fa3664af nginx "/docker-entrypoint.…" 18 seconds ago Up 16 seconds 0.0.0.0:8080->80/tcp, :::8080->80/tcp trusting_wilson
779c3d782a4e ubuntu:18.04 "/bin/bash" 26 minutes ago Up 18 minutes my_os
ubuntu@Docker-Lab:~$
```

Go to Browser Enter your IP with port 8080 you get index page for Nginx

**172.31.11.221:8080**

#### Docker Attach

"The `docker attach` command is used to connect your terminal's standard input, output, and error streams to a running container, typically identified by its ID or name. This allows you to view the live output of the container or interactively control it, as if you were directly running commands in your terminal."

```
docker container attach [container_name_or_id]
```

```
ubuntu@Docker-Lab:~$ docker container ls
CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES
b3d7fa3664af nginx "/docker-entrypoint.…" 3 minutes ago Up 3 minutes 0.0.0.0:8080->80/tcp, :::8080->80/tcp trusting_wilson
779c3d782a4e ubuntu:18.04 "/bin/bash" 29 minutes ago Up 22 minutes my_os
ubuntu@Docker-Lab:~$ docker container attach b3d7fa3664af
2023/10/24 17:55:00 [notice] 1#1: signal 28 (SIGWINCH) received
2023/10/24 17:55:00 [notice] 29#29: signal 28 (SIGWINCH) received
2023/10/24 17:55:00 [notice] 1#1: signal 28 (SIGWINCH) received
2023/10/24 17:55:00 [notice] 29#29: signal 28 (SIGWINCH) received
```

#### Docker Container Kill

"This command will stop one or more running containers. It will forcibly stop the processes inside the container. However, 'docker stop' will only stop the processes inside the container, whereas 'docker kill' will immediately terminate the process itself."

```
docker container kill [container_name_or_id]
```

```
ubuntu@Docker-Lab:~$ docker container ls
CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES
779c3d782a4e ubuntu:18.04 "/bin/bash" 32 minutes ago Up 25 minutes my_os
ubuntu@Docker-Lab:~$ docker container kill my_os
my_os
ubuntu@Docker-Lab:~$ docker container ls -a
CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES
b3d7fa3664af nginx "/docker-entrypoint.…" 7 minutes ago Exited (0) 35 seconds ago trusting_wilson
779c3d782a4e ubuntu:18.04 "/bin/bash" 33 minutes ago Exited (137) 12 seconds ago my_os
ubuntu@Docker-Lab:~$
```

#### Docker Container Prune
"This command removes all stopped containers."
```
docker container prune
```

```
ubuntu@Docker-Lab:~$ docker container ls -a
CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES
b3d7fa3664af nginx "/docker-entrypoint.…" 10 minutes ago Exited (0) 3 minutes ago trusting_wilson
779c3d782a4e ubuntu:18.04 "/bin/bash" 36 minutes ago Exited (137) 3 minutes ago my_os
ubuntu@Docker-Lab:~$ docker container prune
WARNING! This will remove all stopped containers.
Are you sure you want to continue? [y/N] y
Deleted Containers:
b3d7fa3664af23b37d71a94a990ee9023f6eb055f9b3f938c9164172a3a52d1e
779c3d782a4e96f49cecb22046e288aa346387d690227db19a9c7c0d07f920b2

Total reclaimed space: 1.315kB
ubuntu@Docker-Lab:~$ docker container ls -a
CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES
ubuntu@Docker-Lab:~$
```

#### Docker Container Create

"Docker run = Docker create + Docker start. The Docker create command creates a writable container from an image and prepares it for running, whereas the Docker run command creates a container (similar to Docker create) and starts it."

```
docker container create
```

```
ubuntu@Docker-Lab:~$ docker container create nginx sleep 60
682c9ddcffd8f8736edb9a882a046e4aa56bfe3b1d9439d88f5456403b056a70
ubuntu@Docker-Lab:~$ docker container ls -a
CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES
682c9ddcffd8 nginx "/docker-entrypoint.…" 10 seconds ago Created elegant_wright
ubuntu@Docker-Lab:~$ docker container start 682c9ddcffd8
682c9ddcffd8
ubuntu@Docker-Lab:~$
```

#### Docker Container Diff

"This command inspects changes made to files or directories in the container's filesystem. It helps us track which files or directories have been added or removed from the container layer."

```
docker container diff
```

```
ubuntu@Docker-Lab:~$ docker container ls
CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES
7aa2cdc7cdca nginx "/docker-entrypoint.…" 31 seconds ago Up 29 seconds 80/tcp dazzling_solomon
ubuntu@Docker-Lab:~$ docker container diff 7aa2cdc7cdca
C /run
A /run/nginx.pid
C /var
C /var/cache
C /var/cache/nginx
A /var/cache/nginx/client_temp
A /var/cache/nginx/fastcgi_temp
A /var/cache/nginx/proxy_temp
A /var/cache/nginx/scgi_temp
A /var/cache/nginx/uwsgi_temp
C /etc
C /etc/nginx
C /etc/nginx/conf.d
C /etc/nginx/conf.d/default.conf
ubuntu@Docker-Lab:~$
```

Docker has 3 symbols for identifying changes in its diff output

A: A file or directory was created

C: A file or directory was changed

D: A file or directory was deleted

#### Docker Container Copy

"Sometimes we need to copy files from our local machine to a container or from a container to our local machine. Therefore, the 'container cp' command is used to copy files/folders between a container and the local filesystem, and vice versa."

```
docker container cp file/path/ [con_id]:/path/
```

```
ubuntu@Docker-Lab:~$ echo "Hello this is Docker LAB"> index.html
ubuntu@Docker-Lab:~$ ls
index.html
ubuntu@Docker-Lab:~$ docker container run -itd -p 8080:80 nginx
53c2c1524d2788032a8d4f1a3a08c935c06eae33ac216d9f8dc5e9e90aeca485
ubuntu@Docker-Lab:~$ docker container cp index.html 53c:/usr/share/nginx/html
Successfully copied 2.05kB to 53c:/usr/share/nginx/html
ubuntu@Docker-Lab:~$ #lest verify
ubuntu@Docker-Lab:~$ docker container exec -it 53c ls /usr/share/nginx/html/
50x.html index.html
ubuntu@Docker-Lab:~$ docker container exec -it 53c cat /usr/share/nginx/html/index.html
Hello this is Docker LAB
ubuntu@Docker-Lab:~$
```

You can Copy a from container to host machine using below command

docker container cp containerId:/path/in/container /path/in/hostmachine
#### Docker Import and Export

"This command exports a container's filesystem as a tar archive that can be shared. To export a container, move the exported file to the target machine and then import the container there."

```
docker container export
```

```
ubuntu@Docker-Lab:~$ docker image ls
REPOSITORY TAG IMAGE ID CREATED SIZE
nginx latest bc649bab30d1 12 days ago 187MB
ubuntu 18.04 f9a80a55f492 4 months ago 63.2MB
ubuntu@Docker-Lab:~$ docker container run -it ubuntu:18.04 bash
root@a0c37ec880e8:/# apt-get update && apt-get install git -y
root@a0c37ec880e8:/# git --version
git version 2.17.1
root@a0c37ec880e8:/#
Press [ctrl+pq]
ubuntu@Docker-Lab:~$ docker container ls
CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES
a0c37ec880e8 ubuntu:18.04 "bash" 2 minutes ago Up 2 minutes nice_chatterjee
ubuntu@Docker-Lab:~$ docker container export a0c37ec880e8 -o my-git.tar
ubuntu@Docker-Lab:~$ ls
index.html my-git.tar
ubuntu@Docker-Lab:~$
```

Importing a container

```
docker image import
```

```
ubuntu@Docker-Lab:~$ ls
index.html my-git.tar
ubuntu@Docker-Lab:~$ docker images
REPOSITORY TAG IMAGE ID CREATED SIZE
nginx latest bc649bab30d1 12 days ago 187MB
ubuntu 18.04 f9a80a55f492 4 months ago 63.2MB
ubuntu@Docker-Lab:~$ docker image import my-git.tar my-git
sha256:c13b281cd001045d396ad46ad3f6cb5c73fe77edf277b0c578be9b919e3e8b69
ubuntu@Docker-Lab:~$ docker image ls
REPOSITORY TAG IMAGE ID CREATED SIZE
my-git latest c13b281cd001 5 seconds ago 203MB
nginx latest bc649bab30d1 12 days ago 187MB
ubuntu 18.04 f9a80a55f492 4 months ago 63.2MB
ubuntu@Docker-Lab:~$ docker container run -it my-git bash
root@4c82ad817bb3:/# git --version
git version 2.17.1
root@4c82ad817bb3:/#
```

#### Create Docker Image From Running Container

"When working with containers, we often make installations and other changes to run our applications. And when we feel everything is set up the way we want, we might want to capture that setup into an image. In this guide, we will see how to create an image from a running container."

```
docker container commit
```
"This command is used to create an image of a running container. When an image is taken, all processes are paused, ensuring that when this image is used to create another container, no issues arise."

```
ubuntu@Docker-Lab:~$ docker container run -it nginx /bin/bash
root@7fa295f53021:/# cd /usr/share/nginx/html/
root@7fa295f53021:/usr/share/nginx/html# ls
50x.html index.html
root@7fa295f53021:/usr/share/nginx/html# rm -rvf *
removed '50x.html'
removed 'index.html'
root@7fa295f53021:/usr/share/nginx/html# echo "hello user this is devopsLab" > index.html
root@7fa295f53021:/usr/share/nginx/html# ls
index.html
root@7fa295f53021:/usr/share/nginx/html# #press ctrl+pq
root@7fa295f53021:/usr/share/nginx/html#
root@7fa295f53021:/usr/share/nginx/html#
ubuntu@Docker-Lab:~$ docker container ls
CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES
7fa295f53021 nginx "/docker-entrypoint.…" About a minute ago Up About a minute 80/tcp priceless_antonelli
ubuntu@Docker-Lab:~$ docker container commit 7fa295f53021 new_nginx
sha256:7e06edcf98a09aca359d5ba7eaa3092edc78c213d38b8192b0272e837c57d025
ubuntu@Docker-Lab:~$ docker image ls
REPOSITORY TAG IMAGE ID CREATED SIZE
new_nginx latest 7e06edcf98a0 5 seconds ago 187MB
my-git latest c13b281cd001 7 minutes ago 203MB
nginx latest bc649bab30d1 12 days ago 187MB
ubuntu 18.04 f9a80a55f492 4 months ago 63.2MB
ubuntu@Docker-Lab:~$ docker container run -it new_nginx bash
root@382bf4317420:/# cat /usr/share/nginx/html/index.html
hello user this is devopsLab
root@382bf4317420:/#
```

#### Image Operations (Pull, Push, Tag)

"Every time we run a container using an image, it first checks for that image in local storage. If the image is not found locally, Docker then searches for the image on Docker Hub."

**Go to docker hub and create account**

```
docker image pull
```

```
docker image push
```

```
docker image tag
```

```
ubuntu@Docker-Lab:~$ docker image pull ubuntu:18.04
18.04: Pulling from library/ubuntu
7c457f213c76: Already exists
Digest: sha256:152dc042452c496007f07ca9127571cb9c29697f42acbfad72324b2bb2e43c98
Status: Downloaded newer image for ubuntu:18.04
docker.io/library/ubuntu:18.04
ubuntu@Docker-Lab:~$ docker login
Username: raoshahzaib
Password:
WARNING! Your password will be stored unencrypted in /home/ubuntu/.docker/config.json.
Configure a credential helper to remove this warning. See
https://docs.docker.com/engine/reference/commandline/login/#credentials-store

Login Succeeded
ubuntu@Docker-Lab:~$
ubuntu@Docker-Lab:~$ docker image ls
REPOSITORY TAG IMAGE ID CREATED SIZE
ubuntu 18.04 f9a80a55f492 4 months ago 63.2MB
ubuntu@Docker-Lab:~$ #lets tag our image for pusing on docker hub
ubuntu@Docker-Lab:~$ docker image tag ubuntu:18.04 raoshahzaib/myubuntu
ubuntu@Docker-Lab:~$ docker image ls
REPOSITORY TAG IMAGE ID CREATED SIZE
ubuntu 18.04 f9a80a55f492 4 months ago 63.2MB
raoshahzaib/myubuntu latest f9a80a55f492 4 months ago 63.2MB
ubuntu@Docker-Lab:~$ docker image push raoshahzaib/myubuntu:latest
The push refers to repository [docker.io/raoshahzaib/myubuntu]
548a79621a42: Mounted from library/ubuntu
latest: digest: sha256:bd76fb63227e275111397c2b8d7eccd0134ad0efe634fdfd39fe5b3df07bf0b8 size: 529
ubuntu@Docker-Lab:~$
```

go to Docker hub account and verify 

```
docker image pull
```

```
ubuntu@Docker-Lab:~$ docker image ls
REPOSITORY TAG IMAGE ID CREATED SIZE
ubuntu 18.04 f9a80a55f492 4 months ago 63.2MB
raoshahzaib/myubuntu latest f9a80a55f492 4 months ago 63.2MB
ubuntu@Docker-Lab:~$ docker image rm raoshahzaib/myubuntu:latest
Untagged: raoshahzaib/myubuntu:latest
Untagged: raoshahzaib/myubuntu@sha256:bd76fb63227e275111397c2b8d7eccd0134ad0efe634fdfd39fe5b3df07bf0b8
ubuntu@Docker-Lab:~$ docker image rm ubuntu:18.04
Untagged: ubuntu:18.04
Untagged: ubuntu@sha256:152dc042452c496007f07ca9127571cb9c29697f42acbfad72324b2bb2e43c98
Deleted: sha256:f9a80a55f492e823bf5d51f1bd5f87ea3eed1cb31788686aa99a2fb61a27af6a
ubuntu@Docker-Lab:~$ docker image ls
REPOSITORY TAG IMAGE ID CREATED SIZE
ubuntu@Docker-Lab:~$ #lets pull our uploaded image form docker hub
ubuntu@Docker-Lab:~$ docker image pull raoshahzaib/myubuntu:latest
latest: Pulling from raoshahzaib/myubuntu
7c457f213c76: Already exists
Digest: sha256:bd76fb63227e275111397c2b8d7eccd0134ad0efe634fdfd39fe5b3df07bf0b8
Status: Downloaded newer image for raoshahzaib/myubuntu:latest
docker.io/raoshahzaib/myubuntu:latest
ubuntu@Docker-Lab:~$ docker image ls
REPOSITORY TAG IMAGE ID CREATED SIZE
raoshahzaib/myubuntu latest f9a80a55f492 4 months ago 63.2MB
ubuntu@Docker-Lab:~$
```

#### Docker Image List And History

```
docker image history
```

```
ubuntu@Docker-Lab:~$ docker image ls
REPOSITORY TAG IMAGE ID CREATED SIZE
nginx latest bc649bab30d1 12 days ago 187MB
ubuntu latest e4c58958181a 2 weeks ago 77.8MB
raoshahzaib/myubuntu latest f9a80a55f492 4 months ago 63.2MB
ubuntu@Docker-Lab:~$ docker image history ubuntu:latest
IMAGE CREATED CREATED BY SIZE COMMENT
e4c58958181a 2 weeks ago /bin/sh -c #(nop) CMD ["/bin/bash"] 0B
<missing> 2 weeks ago /bin/sh -c #(nop) ADD file:63d5ab3ef0aab308c… 77.8MB
<missing> 2 weeks ago /bin/sh -c #(nop) LABEL org.opencontainers.… 0B
<missing> 2 weeks ago /bin/sh -c #(nop) LABEL org.opencontainers.… 0B
<missing> 2 weeks ago /bin/sh -c #(nop) ARG LAUNCHPAD_BUILD_ARCH 0B
<missing> 2 weeks ago /bin/sh -c #(nop) ARG RELEASE 0B
ubuntu@Docker-Lab:~$
```

#### Docker Image Remove

```
docker image rm
```

```
ubuntu@Docker-Lab:~$ docker images
REPOSITORY TAG IMAGE ID CREATED SIZE
nginx latest bc649bab30d1 12 days ago 187MB
ubuntu latest e4c58958181a 2 weeks ago 77.8MB
raoshahzaib/myubuntu latest f9a80a55f492 4 months ago 63.2MB
ubuntu@Docker-Lab:~$ docker image rm bc649bab30d1
Untagged: nginx:latest
Untagged: nginx@sha256:b4af4f8b6470febf45dc10f564551af682a802eda1743055a7dfc8332dffa595
Deleted: sha256:bc649bab30d150c10a84031a7f54c99a8c31069c7bc324a7899d7125d59cc973
Deleted: sha256:c6f480996a203ed077606cce624f944b041449833e2db3f7d19fe22974fb965b
Deleted: sha256:e4347a01432c5f4350b041632f5703c3dd47de2ec68547b9339d11ea44708389
Deleted: sha256:9d40098fc19fdfff9c74fd3c2c0ff49bfda7d9d04b5d7806d0843d32055d769a
Deleted: sha256:165ae0ef2ddd33b6d5a7f206633b9b0c30cd94ff18a4ed5c3aeb59bf28388526
Deleted: sha256:06dabb44ac4d1f0b5544255e944f15a939178d77aff60a5b296e38bd8743efeb
Deleted: sha256:ee220599571f649e0fb74b40db1615a4c9c1355ac912f9e70087b695617af352
Deleted: sha256:cb4596cc145400fb1f2aa56d41516b39a366ecdee7bf3f9191116444aacd8c90
ubuntu@Docker-Lab:~$ docker rmi e4c58958181a
Untagged: ubuntu:latest
Untagged: ubuntu@sha256:2b7412e6465c3c7fc5bb21d3e6f1917c167358449fecac8176c6e496e5c1f05f
Deleted: sha256:e4c58958181a5925816faa528ce959e487632f4cfd192f8132f71b32df2744b4
Deleted: sha256:256d88da41857db513b95b50ba9a9b28491b58c954e25477d5dad8abb465430b
ubuntu@Docker-Lab:~$ docker image prune
WARNING! This will remove all dangling images.
Are you sure you want to continue? [y/N] y
Total reclaimed space: 0B
ubuntu@Docker-Lab:~$
```

Options:

--all, -a Remove all unused images, not just dangling ones

--filter Provide filter values (e.g. 'until=<timestamp>')

--force, -f Do not prompt for confirmation
#### What is a docker file?
"A Dockerfile is a document containing scripts or instructions that can be used to create an image."

```
vi Dockerfile
```

"The Docker build command by default creates an image based on the instructions provided in a file named 'Dockerfile' located in the current working directory. It is always recommended to name your Dockerfile as 'Dockerfile'. If you name it differently, you would need to explicitly specify the name of the Dockerfile using the '-f' option with the docker build command.

```dockerfile
FROM ubuntu:18.04
```
In the Dockerfile content above, an image will be created based on the ubuntu:18.04 **base**Docker image.
The '**FROM**' keyword is used to specify the base image, and it will create a layer with the docker image '**ubuntu:18.04**' as the base layer.
Note: Best practices related to **Dockerfiles** are available in the Docker documentation.
When you execute the build command, an image named '**myubuntu**' with tag '1' will be created, as shown in the example above. You will notice that the **IMAGE_ID**for '**myubuntu:1**' and '**ubuntu:18.04**' is the same. This is because there were no file structure changes in the base image, so the new image is tagged with the same ID as the existing image."

```
vi Dockerfile
```

```
FROM ubuntu:16.04
RUN apt-get update && apt-get install -y tree
RUN touch /tmp/myfile.txt
```

"In the above image, the `RUN` instruction will install the tree command in our container image and create some text files in the tmp folder.

The `RUN` instruction is used to execute any command on the image, adding a new layer on top of existing layers.

The Docker daemon executes each instruction provided in the Dockerfile one by one, and each instruction is executed independently. Therefore, the impact of one instruction doesn't affect the next one. Each instruction in the Dockerfile creates a new layer on top of existing layers.

Before creating a new image, let's check which images are currently present in our file system."

```
docker image build -t
```

```
ubuntu@Docker-Lab:~$ docker image build -t myubuntu:1 .
DEPRECATED: The legacy builder is deprecated and will be removed in a future release.
 Install the buildx component to build images with BuildKit:
 https://docs.docker.com/go/buildx/

Sending build context to Docker daemon 207.4MB
Step 1/3 : FROM ubuntu:18.04
18.04: Pulling from library/ubuntu
Digest: sha256:152dc042452c496007f07ca9127571cb9c29697f42acbfad72324b2bb2e43c98
Status: Downloaded newer image for ubuntu:18.04
 ---> f9a80a55f492
Step 2/3 : RUN apt-get update && apt-get install -y tree
 ---> Running in bcafefc54583
Get:1 http://security.ubuntu.com/ubuntu bionic-security InRelease [88.7 kB]
Get:2 http://archive.ubuntu.com/ubuntu bionic InRelease [242 kB]
...
Preparing to unpack .../tree_1.7.0-5_amd64.deb ...
Unpacking tree (1.7.0-5) ...
Setting up tree (1.7.0-5) ...
Removing intermediate container bcafefc54583
 ---> 8749a0c165c1
Step 3/3 : RUN touch /tmp/myfile.txt
 ---> Running in 31891c3a87af
Removing intermediate container 31891c3a87af
 ---> fcf10bb1e6e2
Successfully built fcf10bb1e6e2
Successfully tagged myubuntu:1
ubuntu@Docker-Lab:~$
ubuntu@Docker-Lab:~$ docker image ls
REPOSITORY TAG IMAGE ID CREATED SIZE
myubuntu 1 fcf10bb1e6e2 About a minute ago 110MB
ubuntu 18.04 f9a80a55f492 4 months ago 63.2MB
raoshahzaib/myubuntu latest f9a80a55f492 4 months ago 63.2MB
ubuntu@Docker-Lab:~$ docker container run -it myubuntu:1
root@885acebee006:/# cd /tmp/
root@885acebee006:/tmp# ls
myfile.txt
root@885acebee006:/tmp#
```

"Note: Using multiple `RUN` instructions in a Dockerfile is not recommended as it creates a large number of layers.

Another important consideration is that Docker caches commands for better performance that have been executed previously.

So, if we make a modification to an existing Dockerfile and add a `RUN` instruction in the middle of the Dockerfile instead of adding it at the end, Docker will be forced to execute each command as a fresh command, impacting performance."
#### Dockerfile - Label, Env, Run and Workdir

"The 'LABEL' command in Docker is used to add metadata to Docker objects such as images, containers, local daemons, volumes, networks, swarm nodes, and swarm services.

Labels are stored as key-value pairs, represented as strings, and can be used to organize your images, add licensing information, and more. Multiple labels can be added to a Docker object."

"The 'ENV' instruction is used to provide environment variables in an image, which persist when a container is run."

"The 'RUN' instruction is used to execute any command in a new layer on top of the current image, and the resulting image is used for the next step in the Dockerfile."

"The 'WORKDIR' instruction is used to set or change the working directory for any instructions that follow in the Dockerfile."

```
vi Dockerfile
```

```
FROM ubuntu:18.04
RUN apt-get update && apt-get install -y tree
RUN touch /tmp/myfile.txt
LABEL name="Rao Shahziab"
ENV name shahzaib
ENV pass devopsi
WORKDIR /tmp
```

docker image build -t myubuntu:2 .

```
ubuntu@Docker-Lab:~$ docker image build -t myubuntu:2 .
DEPRECATED: The legacy builder is deprecated and will be removed in a future release.
 Install the buildx component to build images with BuildKit:
 https://docs.docker.com/go/buildx/

Sending build context to Docker daemon 207.4MB
Step 1/7 : FROM ubuntu:18.04
 ---> f9a80a55f492
Step 2/7 : RUN apt-get update && apt-get install -y tree
 ---> Using cache
 ---> 8749a0c165c1
Step 3/7 : RUN touch /tmp/myfile.txt
 ---> Using cache
 ---> fcf10bb1e6e2
Step 4/7 : LABEL name="Rao Shahziab"
 ---> Running in 2ead4744981c
Removing intermediate container 2ead4744981c
 ---> b815571e270c
Step 5/7 : ENV name shahzaib
 ---> Running in eb8fe446b8f8
Removing intermediate container eb8fe446b8f8
 ---> c803b760c143
Step 6/7 : ENV pass devopsi
 ---> Running in 98715a380945
Removing intermediate container 98715a380945
 ---> d3596130c34d
Step 7/7 : WORKDIR /tmp
 ---> Running in 6e0fb122506e
Removing intermediate container 6e0fb122506e
 ---> 0999155abf53
Successfully built 0999155abf53
Successfully tagged myubuntu:2
ubuntu@Docker-Lab:~$ #lest run container with our image
ubuntu@Docker-Lab:~$ docker container run -it myubuntu:2
root@8302f0e98e66:/tmp#
```

#### Dockerfile - Add, Copy

"The 'COPY' instruction is used to copy files or directories from a specified source on the host machine into a specified destination within the container's filesystem."

"The 'ADD' instruction is also used to copy files or directories from a specified source on the host machine into a specified destination within the container's filesystem. However, in addition to the 'COPY' instruction, 'ADD' can also download files from URLs, extract local tar files, and copy files from remote URLs."

```
ubuntu@Docker-Lab:~$ mkdir devopslab
ubuntu@Docker-Lab:~$ cd devopslab/
ubuntu@Docker-Lab:~/devopslab$ echo "This is devops lab by Rao Shahzaib" > read.me
ubuntu@Docker-Lab:~/devopslab$ ls
read.me
ubuntu@Docker-Lab:~/devopslab$ cd ..
ubuntu@Docker-Lab:~$ ls
Dockerfile devopslab index.html
ubuntu@Docker-Lab:~$ tar cfv archive.tar index.html
index.html
ubuntu@Docker-Lab:~$ ls
Dockerfile archive.tar devopslab index.html
ubuntu@Docker-Lab:~$
ubuntu@Docker-Lab:~$ vi Dockerfile
```

```
vi Dockerfile
```

```
FROM ubuntu:14.04
RUN mkdir -p /tmp/mydata
COPY devopslab /tmp/mydata/
ADD archive.tar /tmp/mydata/
ADD https://www.free-css.com/free-css-templates/page296/oxer /tmp/mydata/
```

```
docker image build -t myubuntu:3 .
```

```
ubuntu@Docker-Lab:~$ docker image ls
REPOSITORY TAG IMAGE ID CREATED SIZE
myubuntu 2 0999155abf53 26 minutes ago 110MB
myubuntu 1 fcf10bb1e6e2 37 minutes ago 110MB
ubuntu 18.04 f9a80a55f492 4 months ago 63.2MB
raoshahzaib/myubuntu latest f9a80a55f492 4 months ago 63.2MB
ubuntu@Docker-Lab:~$ docker image build -t myubuntu:3 .
DEPRECATED: The legacy builder is deprecated and will be removed in a future release.
 Install the buildx component to build images with BuildKit:
 https://docs.docker.com/go/buildx/

Sending build context to Docker daemon 35.84kB
Step 1/5 : FROM ubuntu:14.04
14.04: Pulling from library/ubuntu
2e6e20c8e2e6: Pull complete
0551a797c01d: Pull complete
512123a864da: Pull complete
Digest: sha256:64483f3496c1373bfd55348e88694d1c4d0c9b660dee6bfef5e12f43b9933b30
Status: Downloaded newer image for ubuntu:14.04
 ---> 13b66b487594
Step 2/5 : RUN mkdir -p /tmp/mydata
 ---> Running in d8985e3367e2
Removing intermediate container d8985e3367e2
 ---> 3402dff5c3e5
Step 3/5 : COPY devopslab /tmp/mydata/
 ---> 76b3184e3b39
Step 4/5 : ADD archive.tar /tmp/mydata/
 ---> 1daf1686e7c5
Step 5/5 : ADD https://www.free-css.com/free-css-templates/page296/oxer /tmp/mydata/
Downloading 9.062kB
 ---> c8a83305975e
Successfully built c8a83305975e
Successfully tagged myubuntu:3
```

```
ubuntu@Docker-Lab:~$ docker image ls
REPOSITORY TAG IMAGE ID CREATED SIZE
myubuntu 3 c8a83305975e 4 minutes ago 197MB
myubuntu 2 0999155abf53 32 minutes ago 110MB
myubuntu 1 fcf10bb1e6e2 42 minutes ago 110MB
raoshahzaib/myubuntu latest f9a80a55f492 4 months ago 63.2MB
ubuntu 18.04 f9a80a55f492 4 months ago 63.2MB
ubuntu 14.04 13b66b487594 2 years ago 197MB
ubuntu@Docker-Lab:~$
ubuntu@Docker-Lab:~$ docker container run -it myubuntu:3
root@0f1c1fdaa5d3:/# cd /tmp/
root@0f1c1fdaa5d3:/tmp# ls
mydata
root@0f1c1fdaa5d3:/tmp# cd mydata/
root@0f1c1fdaa5d3:/tmp/mydata# ls
index.html oxer read.me
root@0f1c1fdaa5d3:/tmp/mydata# cat index.html
Hello this is Docker LAB
root@0f1c1fdaa5d3:/tmp/mydata# cat read.me
This is devops lab by Rao Shahzaib
root@0f1c1fdaa5d3:/tmp/mydata# cd oxer
bash: cd: oxer: Not a directory
root@0f1c1fdaa5d3:/tmp/mydata# ll
total 28
drwxr-xr-x 1 root root 4096 Oct 24 19:44 ./
drwxrwxrwt 1 root root 4096 Oct 24 19:44 ../
-rw-rw-r-- 1 1000 1000 25 Oct 24 18:12 index.html
-rw------- 1 root root 9062 Jan 1 1970 oxer
-rw-rw-r-- 1 root root 35 Oct 24 19:24 read.me
root@0f1c1fdaa5d3:/tmp/mydata#
```

#### Dockerfile - CMD and Entrypoint

"The 'CMD' instruction is used to provide a default executable or entry point for an executing container. When an executable is provided in the 'CMD' instruction, it will be automatically executed when the container is run."

"The 'ENTRYPOINT' instruction allows us to configure a container as an executable."

```
vi Dockerfile
```

```
FROM ubuntu:18.04
RUN apt-get update && apt-get install -y openssh-server && apt-get install -y python
CMD ["python"]
```

```
docker image build -t myubuntu:4 .
```

```
ubuntu@Docker-Lab:~$ docker image build -t myubuntu:4 .
DEPRECATED: The legacy builder is deprecated and will be removed in a future release.
 Install the buildx component to build images with BuildKit:
 https://docs.docker.com/go/buildx/
Sending build context to Docker daemon 37.38kB
Step 1/3 : FROM ubuntu:18.04
 ---> f9a80a55f492
Step 2/3 : RUN apt-get update && apt-get install -y openssh-server && apt-get install -y python
 ---> Running in 40cc119e493a
Removing intermediate container 40cc119e493a
 ---> 7a79a373390b
Step 3/3 : CMD ["python"]
 ---> Running in 0403fe906147
Removing intermediate container 0403fe906147
 ---> d9399411d0de
Successfully built d9399411d0de
Successfully tagged myubuntu:4
ubuntu@Docker-Lab:~$
```

Lets run our image

```
ubuntu@Docker-Lab:~$ docker image ls
REPOSITORY TAG IMAGE ID CREATED SIZE
myubuntu 4 d9399411d0de About a minute ago 247MB
myubuntu 3 c8a83305975e 16 minutes ago 197MB
myubuntu 2 0999155abf53 44 minutes ago 110MB
myubuntu 1 fcf10bb1e6e2 54 minutes ago 110MB
ubuntu 18.04 f9a80a55f492 4 months ago 63.2MB
raoshahzaib/myubuntu latest f9a80a55f492 4 months ago 63.2MB
ubuntu 14.04 13b66b487594 2 years ago 197MB
ubuntu@Docker-Lab:~$ docker container run -it myubuntu:4
Python 2.7.17 (default, Mar 8 2023, 18:40:28)
[GCC 7.5.0] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> 2+5
7
>>> exit()
ubuntu@Docker-Lab:~$
```

```
vi Dockerfile
```

```
FROM ubuntu:18.14
RUN apt-get update && apt-get install -y python tree
ENTRYPOINT ["tree"]
```

```
docker image build -t myubuntu:5 .
```

```
ubuntu@Docker-Lab:~$ docker image build -t myubuntu:5 .
DEPRECATED: The legacy builder is deprecated and will be removed in a future release.
 Install the buildx component to build images with BuildKit:
 https://docs.docker.com/go/buildx/

Sending build context to Docker daemon 38.4kB
Step 1/3 : FROM ubuntu:18.04
 ---> f9a80a55f492
Step 2/3 : RUN apt-get update && apt-get install -y tree
 ---> Running in 3bcafe7f08b1
Reading package lists...
Reading package lists...
Building dependency tree...
Reading state information...
The following NEW packages will be installed:
 tree
0 upgraded, 1 newly installed, 0 to remove and 0 not upgraded.
Need to get 40.7 kB of archives.
After this operation, 105 kB of additional disk space will be used.
Get:1 http://archive.ubuntu.com/ubuntu bionic/universe amd64 tree amd64 1.7.0-5 [40.7 kB]
debconf: delaying package configuration, since apt-utils is not installed
Fetched 40.7 kB in 0s (86.2 kB/s)
Selecting previously unselected package tree.
(Reading database ... 4050 files and directories currently installed.)
Preparing to unpack .../tree_1.7.0-5_amd64.deb ...
Unpacking tree (1.7.0-5) ...
Setting up tree (1.7.0-5) ...
Removing intermediate container 3bcafe7f08b1
 ---> 3ace613e1aa3
Step 3/3 : ENTRYPOINT ["tree"]
 ---> Running in 9a177fc8a704
Removing intermediate container 9a177fc8a704
 ---> ef2389a048ee
Successfully built ef2389a048ee
Successfully tagged myubuntu:5
ubuntu@Docker-Lab:~$
ubuntu@Docker-Lab:~$ docker image ls
REPOSITORY TAG IMAGE ID CREATED SIZE
myubuntu 5 ef2389a048ee About a minute ago 110MB
myubuntu 4 d9399411d0de 7 minutes ago 247MB
myubuntu 3 c8a83305975e 22 minutes ago 197MB
myubuntu 2 0999155abf53 49 minutes ago 110MB
myubuntu 1 fcf10bb1e6e2 About an hour ago 110MB
raoshahzaib/myubuntu latest f9a80a55f492 4 months ago 63.2MB
ubuntu 18.04 f9a80a55f492 4 months ago 63.2MB
ubuntu 14.04 13b66b487594 2 years ago 197MB
ubuntu@Docker-Lab:~$
```

lets run our container with our image

```
docker container run -it myubuntu:5
```

```
ubuntu@Docker-Lab:~$ docker container run -it myubuntu:5
.
|-- bin
| |-- bash
| |-- bunzip2
| |-- bzcat
| |-- bzcmp -> bzdiff
| |-- bzdiff
| |-- bzegrep -> bzgrep
| |-- bzexe
| |-- bzfgrep -> bzgrep
| |-- bzgrep
| |-- bzip2
| |-- bzip2recover
| |-- bzless -> bzmore
...
 |-- local
 |-- lock -> /run/lock
 |-- log
 | |-- alternatives.log
 | |-- apt
 | | |-- eipp.log.xz
 | | |-- history.log
 | | `-- term.log
 | |-- bootstrap.log
 | |-- btmp
 | |-- dpkg.log
 | |-- faillog
 | |-- lastlog
 | |-- tallylog
 | `-- wtmp
 |-- mail
 |-- opt
 |-- run -> /run
 |-- spool
 | `-- mail -> ../mail
 `-- tmp

4891 directories, 21078 files
ubuntu@Docker-Lab:~$
```

#### Docker Volume

"Docker storage is a crucial component of Docker containerization. Let's talk about what Docker Storage is, how we can use it, and how it can assist us.

Firstly, let's understand how storage works in Docker. If we talk about default storage, it resides inside our Docker container. However, this storage method is not very efficient. We need to grasp that a Docker container is constructed from multiple layers. When we run an application, the data it produces is stored within these layers of the Docker container. This can slow down the performance of the container.

Therefore, we never store data directly inside a Docker container. Instead, we store our data in different storage types provided by Docker. These storage options offer better performance and scalability."
##### Docker Storage types

1. **Volumes**
1. **Bind mount**
1. **Tmpfs mount**

```
docker volume ls
```

```
ubuntu@Docker-Lab:~$ docker volume ls
DRIVER VOLUME NAME
ubuntu@Docker-Lab:~$
```

```
docker volume create
```

```
ubuntu@Docker-Lab:~$ docker volume create olxdata
olxdata
ubuntu@Docker-Lab:~$ docker volume ls
DRIVER VOLUME NAME
local olxdata
ubuntu@Docker-Lab:~$
```

now we create a MySQL container and attach olxdata volume with it

```
docker container run -d --name container_name -v volume_name:/var/lib/mysql -e MYSQL_ALLOW_EMPTY_PASSWORD=true mysql
```

```
ubuntu@Docker-Lab:~$ docker container run -d --name olx_database -v olxdata:/var/lib/mysql -e MYSQL_ALLOW_EMPTY_PASSWORD=true mysql Unable to find image 'mysql:latest' locally
latest: Pulling from library/mysql
8e0176adc18c: Pull complete
14e977b0f4b2: Pull complete
a7b58dd6f78b: Pull complete
fba70cc872a5: Pull complete
5db2cc6eab8f: Pull complete
081f41f573ba: Pull complete
86bf2dc4ded9: Pull complete
47f08b0e916e: Pull complete
850e29ae8eeb: Pull complete
13517fe0d921: Pull complete
Digest: sha256:f61944ff3f2961363a4d22913b2ac581523273679d7e14dd26e8db8c9f571a7e
Status: Downloaded newer image for mysql:latest
41857ac6db556ce54d1a5872d59f5d9597d73a257f379ece34831dff2fcb3753
ubuntu@Docker-Lab:~$
```

**Create some data in mysql container for testing**

```
ubuntu@Docker-Lab:~$ docker container ls
CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES
f9e8c01a27ad mysql "docker-entrypoint.s…" 47 seconds ago Up 46 seconds 3306/tcp, 33060/tcp olx_database
ubuntu@Docker-Lab:~$ docker exec -it f9e8c01a27ad bash
bash-4.4# mysql
Welcome to the MySQL monitor. Commands end with ; or \g.
Your MySQL connection id is 8
Server version: 8.1.0 MySQL Community Server - GPL

Copyright (c) 2000, 2023, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> show databases;
+--------------------+
| Database |
+--------------------+
| information_schema |
| mysql |
| performance_schema |
| sys |
+--------------------+
4 rows in set (0.12 sec)
mysql> create database id;
Query OK, 1 row affected (0.03 sec)

mysql> create database pass;
Query OK, 1 row affected (0.01 sec)

mysql> show databases;
+--------------------+
| Database |
+--------------------+
| id |
| information_schema |
| mysql |
| pass |
| performance_schema |
| sys |
+--------------------+
6 rows in set (0.00 sec)

mysql> exit
bash-4.4#
ubuntu@Docker-Lab:~$ docker volume ls
DRIVER VOLUME NAME
local olxdata
ubuntu@Docker-Lab:~$ docker container ls
CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES
f9e8c01a27ad mysql "docker-entrypoint.s…" 3 minutes ago Up 3 minutes 3306/tcp, 33060/tcp olx_database
ubuntu@Docker-Lab:~$ docker container stop f9
f9
ubuntu@Docker-Lab:~$ docker container rm f9
f9
ubuntu@Docker-Lab:~$
```

now im going to create a another MySQL container and attach olxdata volume with it, so we can check data is persistent or not 

```
docker container run -d --name new_olx_container -v olxdata:/var/lib/mysql -e MYSQL_ALLOW_EMPTY_PASSWORD=true mysql
```

```
ubuntu@Docker-Lab:~$ docker container run -d --name new_olx_container -v olxdata:/var/lib/mysql -e MYSQL_ALLOW_EMPTY_PASSWORD=true mysql
2289412c6811bf514b1f7bfa581c08f7bfd8226dd8feac5a49dacef722545391
ubuntu@Docker-Lab:~$ docker exec -it 22 bash
bash-4.4# mysql
Welcome to the MySQL monitor. Commands end with ; or \g.
Your MySQL connection id is 8
Server version: 8.1.0 MySQL Community Server - GPL

Copyright (c) 2000, 2023, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> show databases;
+--------------------+
| Database |
+--------------------+
| id |
| information_schema |
| mysql |
| pass |
| performance_schema |
| sys |
+--------------------+
6 rows in set (0.09 sec)

mysql> exit
Bye
bash-4.4#
```

#### Docker Bind mount
"By using Docker bind mounts, you can mount a file or folder from the host machine into the container. The file or directory is referenced on the host machine through its absolute path."

```
ubuntu@Docker-Lab:~$ mkdir bind
ubuntu@Docker-Lab:~$ cd bind/
ubuntu@Docker-Lab:~/bind$ echo "hello user this devops lab" > read.me
ubuntu@Docker-Lab:~/bind$ cat read.me
hello user this devops lab
ubuntu@Docker-Lab:~/bind$
```

```
docker container run -it -v /host/path:/container/path ubuntu:18.04
```

```
ubuntu@Docker-Lab:~$ docker container run -it -v /home/ubuntu/bind/:/tmp/ ubuntu:18.04
root@b6950797e9bc:/# cd tmp/
root@b6950797e9bc:/tmp# ls
read.me
root@b6950797e9bc:/tmp# cat read.me
root@b6950797e9bc:/tmp# echo "This file container file" > container.txt
root@b6950797e9bc:/tmp# ls
container.txt read.me
root@b6950797e9bc:/tmp# exit
exit
ubuntu@Docker-Lab:~$ ls
bind
ubuntu@Docker-Lab:~$ cd bind/
ubuntu@Docker-Lab:~/bind$ ls
container.txt read.me
ubuntu@Docker-Lab:~/bind$ cat container.txt
This file container file
ubuntu@Docker-Lab:~/bind$
```

#### Docker Networking

"Docker containers require a networking layer so that they can communicate with each other, the host machine, or the external world."

"Now let's talk about Docker networks. We'll explore how our created containers communicate with each other and how we can create networks according to our requirements. When we run a service, it might be dependent on different containers. Hence, communication between containers is essential. For applications to communicate effectively, there needs to be virtualized networking, enabling them to communicate seamlessly without any additional effort. Docker networks make this possible."

"Docker networks are essentially connections between one container and another. It's also possible for a network to connect different sets of containers. Managing and isolating them becomes very easy with Docker networks. Isolation is a crucial aspect; if you want to prevent a container from communicating with another, you can place it in isolation."
### Types of networks

1. **Bridge network**

1. **Host network**

1. **Overlay network**

1. **Macvlan network**

1. **None network**

##### Bridge Network:

This is a simple network and is, in fact, the default network that many containers are already connected to. It's the most basic network setup that we can use.

##### Host Network:

Host network essentially eliminates the isolation layer between your host system and the container. With this setup, your containers can directly access resources on your host system.

##### Overlay Network:

Overlay network is a vital network type, especially when we talk about connecting different nodes. For instance, if you have 5 or 8 servers with Docker engines running on them and containers on these servers need to communicate with each other, they can use the Overlay network. Unlike Bridge network, when containers need to communicate across servers, Overlay network comes into play.

##### Macvlan Network:
Macvlan network helps us in fooling software. By 'fooling', we mean that when you have legacy software that always needs physical access for communication over a specific network, this type of network comes in handy. These are old applications that require a real physical network connection. However, nowadays, we can create virtual networks. Using Macvlan, we can make these applications believe they are connected to an actual physical network, even though it's a virtual network, by generating Mac addresses.

##### None Network 

The 'None' network essentially means no networking. Containers in this mode don't have external network access. It's useful in situations where you want complete network isolation for your containers."

```
docker network ls
```

```
ubuntu@Docker-Lab:~$ docker network ls
NETWORK ID NAME DRIVER SCOPE
a8988423d384 bridge bridge local
6936a8aafc90 host host local
d76ccf9fa189 none null local
ubuntu@Docker-Lab:~$
```

**Let's inspect this network-**

```
docker network inspect
```

```
ubuntu@Docker-Lab:~$ docker network inspect bridge
[
 {
 "Name": "bridge",
 "Id": "a8988423d384a426a9c82146640a65df6653161255e3c8d2c6f71e20a4d76185",
 "Created": "2023-10-25T04:13:35.852390506Z",
 "Scope": "local",
 "Driver": "bridge",
 "EnableIPv6": false,
 "IPAM": {
 "Driver": "default",
 "Options": null,
 "Config": [
 {
 "Subnet": "172.17.0.0/16",
 "Gateway": "172.17.0.1"
 }
 ]
 },
 "Internal": false,
 "Attachable": false,
 "Ingress": false,
 "ConfigFrom": {
 "Network": ""
 },
 "ConfigOnly": false,
 "Containers": {},
 "Options": {
 "com.docker.network.bridge.default_bridge": "true",
 "com.docker.network.bridge.enable_icc": "true",
 "com.docker.network.bridge.enable_ip_masquerade": "true",
 "com.docker.network.bridge.host_binding_ipv4": "0.0.0.0",
 "com.docker.network.bridge.name": "docker0",
 "com.docker.network.driver.mtu": "1500"
 },
 "Labels": {}
 }
]
ubuntu@Docker-Lab:~$
```

**Lets create docker network**

```
ubuntu@Docker-Lab:~$ docker network create --driver bridge olxnet
fe31926f67087f0c70387228b2fe507c132e021d9520ad7bc95ea24d3d90be67
ubuntu@Docker-Lab:~$ docker network ls
NETWORK ID NAME DRIVER SCOPE
a8988423d384 bridge bridge local
6936a8aafc90 host host local
d76ccf9fa189 none null local
fe31926f6708 olxnet bridge local
ubuntu@Docker-Lab:~$
```

**Let's run two container 1 with default bridge network or 1 with out olxnet , and can the communicate.**

```
ubuntu@Docker-Lab:~$ docker run -itd --name defaultCon ubuntu:18.04
1a50cffd11dc80e972642dfa79f816e6318d23fb847a58b19d2f6380c9579c49
ubuntu@Docker-Lab:~$ docker container inspect defaultCon
[
 {
 "Id": "1a50cffd11dc80e972642dfa79f816e6318d23fb847a58b19d2f6380c9579c49",
 "Created": "2023-10-25T04:29:49.423574405Z",
 "Path": "/bin/bash",
 "Args": [],
 "State": {
 "Status": "running",
 "Running": true,
 "Paused": false,
 "Restarting": false,
 "OOMKilled": false,
 "Dead": false,
 "Pid": 1511,
 "ExitCode": 0,
 "Error": "",
 "StartedAt": "2023-10-25T04:29:50.615065162Z",
 "FinishedAt": "0001-01-01T00:00:00Z"
 },

 "Networks": {
 "bridge": {
 "IPAMConfig": null,
 "Links": null,
 "Aliases": null,
 "NetworkID": "a8988423d384a426a9c82146640a65df6653161255e3c8d2c6f71e20a4d76185",
 "EndpointID": "a620d644e6a25b55a6ea44e2d711c478c0822715893a48d6e40c52a62863c83a",
 "Gateway": "172.17.0.1",
 "IPAddress": "172.17.0.2",
 "IPPrefixLen": 16,
 "IPv6Gateway": "",
 "GlobalIPv6Address": "",
 "GlobalIPv6PrefixLen": 0,
 "MacAddress": "02:42:ac:11:00:02",
 "DriverOpts": null
 }
 }
 }
 }
]
ubuntu@Docker-Lab:~$ copy the IPAddress
```

**lets see.**

```
ubuntu@Docker-Lab:~$ docker run -itd --name olxCon --network olxnet ubuntu:18.04
0e0f7d975759d3b62bfbfe82b8a31cdf134edd95aabb6c42f5a39b56a5b62e01
ubuntu@Docker-Lab:~$
ubuntu@Docker-Lab:~$ docker container exec -it 0e bash
root@0e0f7d975759:/# apt-get update && apt-get install iputils-ping -y
Setting up libcap2-bin (1:2.25-1.2) ...
Processing triggers for libc-bin (2.27-3ubuntu1.6) ...
root@0e0f7d975759:/# ping 8.8.8.8
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=50 time=2.23 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=50 time=5.99 ms
64 bytes from 8.8.8.8: icmp_seq=3 ttl=50 time=2.37 ms
64 bytes from 8.8.8.8: icmp_seq=4 ttl=50 time=2.20 ms
^C
--- 8.8.8.8 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3003ms
rtt min/avg/max/mdev = 2.205/3.203/5.995/1.613 ms
root@0e0f7d975759:/# ping 172.17.0.2
PING 172.17.0.2 (172.17.0.2) 56(84) bytes of data.
^C
--- 172.17.0.2 ping statistics ---
3 packets transmitted, 0 received, 100% packet loss, time 2026ms

root@0e0f7d975759:/# not able to ping defult network container
bash: not: command not found
root@0e0f7d975759:/#
```

**if we run both both container in same network then the will able to communicate each other.**

```
ping 172.18.0.3
```

```
ubuntu@Docker-Lab:~$ docker run -itd --name olxnewCon --network olxnet ubuntu:18.04
0c047ca83edb8afd91e4fb4dc1c8d125095126a120d209e1b4e3c9877962947a
ubuntu@Docker-Lab:~$ docker container inspect olxnewCon
[
 {
 "Id": "0c047ca83edb8afd91e4fb4dc1c8d125095126a120d209e1b4e3c9877962947a",
 "Created": "2023-10-25T04:37:22.520944007Z",
 "Path": "/bin/bash",
 "Args": [],
 "State": {
 "Status": "running",
 "Running": true,
 "Paused": false,
 "Restarting": false,
 "OOMKilled": false,
 "Dead": false,
 "Pid": 2219,
 "ExitCode": 0,
 "Error": "",
 "StartedAt": "2023-10-25T04:37:23.345243369Z",
 "FinishedAt": "0001-01-01T00:00:00Z"
 },

 "Networks": {
 "olxnet": {
 "IPAMConfig": null,
 "Links": null,
 "Aliases": [
 "0c047ca83edb"
 ],
 "NetworkID": "fe31926f67087f0c70387228b2fe507c132e021d9520ad7bc95ea24d3d90be67",
 "EndpointID": "9e86e64f36685023731a73d2a01f1a848601879eeda60827f4eb9fb07a90b2d0",
 "Gateway": "172.18.0.1",
 "IPAddress": "172.18.0.3",
 "IPPrefixLen": 16,
 "IPv6Gateway": "",
 "GlobalIPv6Address": "",
 "GlobalIPv6PrefixLen": 0,
 "MacAddress": "02:42:ac:12:00:03",
 "DriverOpts": null
 }
 }
 }
 }
]
ubuntu@Docker-Lab:~$ copy IPAdress
ubuntu@Docker-Lab:~$ docker container ls
CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES
0c047ca83edb ubuntu:18.04 "/bin/bash" About a minute ago Up About a minute olxnewCon
0e0f7d975759 ubuntu:18.04 "/bin/bash" 6 minutes ago Up 6 minutes olxCon
1a50cffd11dc ubuntu:18.04 "/bin/bash" 8 minutes ago Up 8 minutes defaultCon
ubuntu@Docker-Lab:~$
ubuntu@Docker-Lab:~$ docker container ls
CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES
0c047ca83edb ubuntu:18.04 "/bin/bash" About a minute ago Up About a minute olxnewCon
0e0f7d975759 ubuntu:18.04 "/bin/bash" 6 minutes ago Up 6 minutes olxCon
1a50cffd11dc ubuntu:18.04 "/bin/bash" 8 minutes ago Up 8 minutes defaultCon
ubuntu@Docker-Lab:~$ docker container exec -it olxCon bash
root@0e0f7d975759:/# ping 172.18.0.3
PING 172.18.0.3 (172.18.0.3) 56(84) bytes of data.
64 bytes from 172.18.0.3: icmp_seq=1 ttl=64 time=0.124 ms
64 bytes from 172.18.0.3: icmp_seq=2 ttl=64 time=0.077 ms
64 bytes from 172.18.0.3: icmp_seq=3 ttl=64 time=0.063 ms
^C
--- 172.18.0.3 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2026ms
rtt min/avg/max/mdev = 0.063/0.088/0.124/0.026 ms
root@0e0f7d975759:/# boom the ping each other
```

#### Host Network

Docker container that are connected to host network basically shared the namespace with their hosts. i.e the containers share the IP address of the host and don't have one of their own.

```
docker container run -itd --name MyCon --network host nginx
```

```
ubuntu@Docker-Lab:~$ docker network ls
NETWORK ID NAME DRIVER SCOPE
a8988423d384 bridge bridge local
6936a8aafc90 host host local
d76ccf9fa189 none null local
fe31926f6708 olxnet bridge local
ubuntu@Docker-Lab:~$ docker container run -itd --name MyCon --network host nginx
eefa1058d7898ee0e90ac9f954d413395105614c3595011e805e559dc5d822d3
ubuntu@Docker-Lab:~$ docker container ls
CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES
eefa1058d789 nginx "/docker-entrypoint.…" 4 seconds ago Up 4 seconds MyCon
ubuntu@Docker-Lab:~$ Go to your and enter your IP
```

**lets verify**

```
curl localhost
```

```
ubuntu@Docker-Lab:~$ curl localhost
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
html { color-scheme: light dark; }
body { width: 35em; margin: 0 auto;
font-family: Tahoma, Verdana, Arial, sans-serif; }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
ubuntu@Docker-Lab:~$
```

##### Remove Network's

```
docker network rm
```

```
ubuntu@Docker-Lab:~$ docker network ls
NETWORK ID NAME DRIVER SCOPE
a8988423d384 bridge bridge local
6936a8aafc90 host host local
d76ccf9fa189 none null local
fe31926f6708 olxnet bridge local
ubuntu@Docker-Lab:~$ docker network rm olxnet
olxnet
ubuntu@Docker-Lab:~$ docker network ls
NETWORK ID NAME DRIVER SCOPE
a8988423d384 bridge bridge local
6936a8aafc90 host host local
d76ccf9fa189 none null local
ubuntu@Docker-Lab:~$
```

#### Docker Registry/Repository (Insecure)

"When we use the 'docker image pull' command to download an official Docker image, it is fetched from a remote server's hosted Docker registry.
However, if we want to download or push these images from/to our private registry instead of Docker Hub, we can achieve this using Docker Registry.
A Registry is a stateless, highly scalable server-side application that stores Docker images and allows distribution. It is open-source and operates under the Apache license.
Docker provides its own image for this purpose named 'registry.' To use it, we need to pull this image and run a container based on it."

```
docker container run -d -p 5000:5000 --name my_registry registry
```

```
ubuntu@Docker-Lab:~$ docker container run -d -p 5000:5000 --name my_registry registry
Unable to find image 'registry:latest' locally
latest: Pulling from library/registry
96526aa774ef: Pull complete
834bccaa730c: Pull complete
87a69098c0a9: Pull complete
afc17120a9f7: Pull complete
e5ac04f3acf5: Pull complete
Digest: sha256:8a60daaa55ab0df4607c4d8625b96b97b06fd2e6ca8528275472963c4ae8afa0
Status: Downloaded newer image for registry:latest
3dd2cad66b41d5562425507a785f7812588f8b5610beda8076ac90457a047cde
ubuntu@Docker-Lab:~$ docker container ls
CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES
3dd2cad66b41 registry "/entrypoint.sh /etc…" 11 seconds ago Up 9 seconds 0.0.0.0:5000->5000/tcp, :::5000->5000/tcp my_registry
ubuntu@Docker-Lab:~$ curl http://127.0.0.1:5000/v2/_catalog
{"repositories":[]}
ubuntu@Docker-Lab:~$
ubuntu@Docker-Lab:~$ docker container inspect my_registry
[
 {
 "Id": "3dd2cad66b41d5562425507a785f7812588f8b5610beda8076ac90457a047cde",
 "Created": "2023-10-25T04:54:52.884990488Z",
 "Path": "/entrypoint.sh",
 "Args": [
 "/etc/docker/registry/config.yml"

 "Mounts": [
 {
 "Type": "volume",
 "Name": "c7e93e205f4409cf29e020f46400a9affe7f3b7436e9f74a5021344d1fc51784",
 "Source": "/var/lib/docker/volumes/c7e93e205f4409cf29e020f46400a9affe7f3b7436e9f74a5021344d1fc51784/_data",
 "Destination": "/var/lib/registry",
 "Driver": "local",
 "Mode": "",
 "RW": true,
 "Propagation": ""
 }
 ],

ubuntu@Docker-Lab:~$
```

"We can view volume information in the format provided above by using the 'inspect' command output. If, for any reason, our container stops and we want to restart it, we can reconnect the same volume to the container using the volume information given above.

Notice in the volume information provided above, the 'driver' is 'local' because our data will be stored in the local file system. There are also drivers available for remote cloud storage, allowing us to store our data remotely, such as AWS S3, Google Cloud, Azure, and others."

```
docker image push local_registry
```

```
ubuntu@Docker-Lab:~$ docker image ls
REPOSITORY TAG IMAGE ID CREATED SIZE
nginx latest 593aee2afb64 4 hours ago 187MB
registry latest ff1857193a0b 4 days ago 25.4MB
ubuntu 18.04 f9a80a55f492 4 months ago 63.2MB
raoshahzaib/myubuntu latest f9a80a55f492 4 months ago 63.2MB
ubuntu@Docker-Lab:~$ docker image tag nginx:latest 127.0.0.1:5000/newubuntu:latest
ubuntu@Docker-Lab:~$ docker image ls
REPOSITORY TAG IMAGE ID CREATED SIZE
127.0.0.1:5000/newubuntu latest 593aee2afb64 4 hours ago 187MB
nginx latest 593aee2afb64 4 hours ago 187MB
registry latest ff1857193a0b 4 days ago 25.4MB
ubuntu 18.04 f9a80a55f492 4 months ago 63.2MB
raoshahzaib/myubuntu latest f9a80a55f492 4 months ago 63.2MB
ubuntu@Docker-Lab:~$ docker image push 127.0.0.1:5000/newubuntu:latest
The push refers to repository [127.0.0.1:5000/newubuntu]
97c766ccce63: Pushed
a7d081791a97: Pushed
9c7a17c7c18b: Pushed
572e6b1b9ddf: Pushed
f4e84f2b0154: Pushed
4ccbaf6751da: Pushed
cb4596cc1454: Pushed
latest: digest: sha256:0d60ba9498d4491525334696a736b4c19b56231b972061fab2f536d48ebfd7ce size: 1778
ubuntu@Docker-Lab:~$
```

The image is pushed. Now let’s verify if the image is pushed successfully or not. For verifying, curl to http://127.0.0.1:5000/v2/_catalog, we see that our image has been pushed successfully.

```
docker network ls
```

```
ubuntu@Docker-Lab:~$ curl http://127.0.0.1:5000/v2/_catalog
{"repositories":["newubuntu"]}
ubuntu@Docker-Lab:~$
```

**Now let us delete the Redis image present on our local file system.**

```
docker rmi
```

```
ubuntu@Docker-Lab:~$ docker image ls
REPOSITORY TAG IMAGE ID CREATED SIZE
127.0.0.1:5000/newubuntu latest 593aee2afb64 4 hours ago 187MB
nginx latest 593aee2afb64 4 hours ago 187MB
registry latest ff1857193a0b 4 days ago 25.4MB
ubuntu 18.04 f9a80a55f492 4 months ago 63.2MB
raoshahzaib/myubuntu latest f9a80a55f492 4 months ago 63.2MB
ubuntu@Docker-Lab:~$ docker rmi 127.0.0.1:5000/newubuntu:latest
Untagged: 127.0.0.1:5000/newubuntu:latest
Untagged: 127.0.0.1:5000/newubuntu@sha256:0d60ba9498d4491525334696a736b4c19b56231b972061fab2f536d48ebfd7ce
ubuntu@Docker-Lab:~$
```

If we disconnect our internet and try to pull the same image again, we get the below error as the default registry is unreachable.

But we are able to download the image from the local registry.

```
docker image pull 127.0.0.1:5000/newubuntu:latest
```

```
ubuntu@Docker-Lab:~$ docker image pull 127.0.0.1:5000/newubuntu:latest
latest: Pulling from newubuntu
Digest: sha256:0d60ba9498d4491525334696a736b4c19b56231b972061fab2f536d48ebfd7ce
Status: Downloaded newer image for 127.0.0.1:5000/newubuntu:latest
127.0.0.1:5000/newubuntu:latest
ubuntu@Docker-Lab:~$ docker images
REPOSITORY TAG IMAGE ID CREATED SIZE
nginx latest 593aee2afb64 4 hours ago 187MB
127.0.0.1:5000/newubuntu latest 593aee2afb64 4 hours ago 187MB
registry latest ff1857193a0b 4 days ago 25.4MB
raoshahzaib/myubuntu latest f9a80a55f492 4 months ago 63.2MB
ubuntu 18.04 f9a80a55f492 4 months ago 63.2MB
ubuntu@Docker-Lab:~$
```

When we try to push this image,we get the error message shown in the below image which tells us to use https instead of http.

```
docker image push 172.31.11.221:5000/mynginx
```

```
ubuntu@Docker-Lab:~$ docker image tag nginx:latest 172.31.11.221:5000/mynginx:latest
ubuntu@Docker-Lab:~$ docker images
REPOSITORY TAG IMAGE ID CREATED SIZE
127.0.0.1:5000/newubuntu latest 593aee2afb64 4 hours ago 187MB
172.31.11.221:5000/mynginx latest 593aee2afb64 4 hours ago 187MB
nginx latest 593aee2afb64 4 hours ago 187MB
registry latest ff1857193a0b 4 days ago 25.4MB
ubuntu 18.04 f9a80a55f492 4 months ago 63.2MB
raoshahzaib/myubuntu latest f9a80a55f492 4 months ago 63.2MB
ubuntu@Docker-Lab:~$ docker image push 172.31.11.221:5000/mynginx
Using default tag: latest
The push refers to repository [172.31.11.221:5000/mynginx]
Get "https://172.31.11.221:5000/v2/": http: server gave HTTP response to HTTPS client
ubuntu@Docker-Lab:~$
```

"To allow Docker to access insecure locations, we need to modify the Docker configuration in the following way:

First, we need to locally create the 'daemon.json' file and add the IP address we want to allow in the IP list.

Here is an example of how we can create the 'daemon.json' file in the '/etc/docker' directory:"

```
vi daemon.json
```

```
ubuntu@Docker-Lab:~$ cd /etc/docker/
ubuntu@Docker-Lab:/etc/docker$ ls
ubuntu@Docker-Lab:/etc/docker$ vi daemon.json
{
 "insecure-registries": ["172.31.11.221:5000"]
}
```

**Now we need to restart the docker service and our container which has stopped.**

```
sudo systemctl restart docker
```

```
ubuntu@Docker-Lab:/etc/docker$ sudo systemctl restart docker
ubuntu@Docker-Lab:/etc/docker$ docker container ls -a
CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES
3dd2cad66b41 registry "/entrypoint.sh /etc…" 23 minutes ago Exited (2) 22 seconds ago my_registry
ubuntu@Docker-Lab:/etc/docker$ docker container start my_registry
my_registry
ubuntu@Docker-Lab:/etc/docker$
```

**Now if we push our image again -**

```
docker image push 172.31.11.221:5000/mynginx
```

```
ubuntu@Docker-Lab:/etc/docker$ docker image push 172.31.11.221:5000/mynginx
Using default tag: latest
The push refers to repository [172.31.11.221:5000/mynginx]
97c766ccce63: Pushed
a7d081791a97: Pushed
9c7a17c7c18b: Pushed
572e6b1b9ddf: Pushed
f4e84f2b0154: Pushed
4ccbaf6751da: Pushed
cb4596cc1454: Pushed
latest: digest: sha256:0d60ba9498d4491525334696a736b4c19b56231b972061fab2f536d48ebfd7ce size: 1778
ubuntu@Docker-Lab:/etc/docker$
```

**The image is pushed successfully!**
