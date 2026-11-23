---
title: "A Complete Journey Through Ansible Core Concepts Part 1: Inventory, Ad-Hoc Commands and Modules"
description: "Ansible part 1: install Ansible, build your inventory, connect EC2 nodes, run ad-hoc commands and master the core modules: copy, file, user, yum and service."
slug: "ansible-core-concepts-part-1"
---

By Rao Shahzaib · DevOps

A Complete Journey through Ansible Core Concepts | 1/2

![Ansible Core Concepts](/images/ansible-core-concepts-part-1/01-installation-1-.png)

**## **
**## Ansible Core Concepts **

Ansible is an open-source automation tool that is used for configuration management, application deployment, task automation, and IT orchestration. It is designed to simplify and streamline various IT tasks by automating them, which can help save time, reduce errors, and improve efficiency in managing and maintaining IT infrastructure.
##### Key features and concepts associated with Ansible include:

1. **Agentless**: Ansible is agentless, meaning it doesn't require software agents to be installed on the target machines. Instead, it uses SSH (for Unix-like systems) and WinRM (for Windows) to connect to and manage remote hosts. This makes Ansible easy to set up and use.
2. **Infrastructure **as Code: Ansible uses a declarative language to define the desired state of systems and infrastructure. Users specify the configuration in Ansible playbooks, which are written in YAML (Yet Another Markup Language). This makes it easy to understand and version control your infrastructure.

3. **Playbooks**: Playbooks are Ansible's configuration files that describe the tasks and configurations that need to be applied to target hosts. Playbooks are written in YAML and can include roles, variables, and other configuration details.

4. **Modules**: Ansible comes with a large library of modules that provide abstractions for different system tasks. These modules can be used in playbooks to manage various aspects of systems, such as package management, file operations, user management, and more.

5. **Roles**: Roles are a way to organize and package related tasks and configurations in Ansible. They allow you to reuse and share common sets of configurations and tasks across different playbooks.

6. **Inventory**: Ansible uses an inventory file to define the hosts and groups of hosts that it will manage. The inventory can be static or dynamic and can include details about the hosts, such as their IP addresses and SSH credentials.

7. **Idempotence**: Ansible is idempotent, meaning you can run the same playbook multiple times without causing unintended changes. If a task has already achieved the desired state, Ansible will not make any further changes.

8. **Ad-Hoc Commands**: In addition to playbooks, Ansible allows you to run ad-hoc commands to perform quick tasks on remote hosts without the need for a playbook.

Ansible is widely used in DevOps and system administration for tasks like server provisioning, application deployment, configuration management, and continuous delivery. It has a strong and active community, and many organizations use Ansible to manage and automate their IT infrastructure.

### Let's get started with a simple lab setup

![Ansible lab setup](/images/ansible-core-concepts-part-1/02-installation.gif)

For the This im using AWS cloud.

![AWS console showing the Ansible lab EC2 instances](/images/ansible-core-concepts-part-1/03-opera-snapshot_2023-10-25_155132_ap-south-1.consol.png)

#### Install of Ansible control nodes

First, we need to set our machine's static hostname in our machine.

SSH Ansible instance 

sudo hostnamectl set-hostname

```
[ec2-user@ip-172-31-43-32 ~]$ sudo hostnamectl set-hostname Ansible-Server
```

SSH node-1 instance 

sudo hostnamectl set-hostname

```
[ec2-user@ip-172-31-44-32 ~]$ sudo hostnamectl set-hostname node-1
```

SSH node-2 instance 

sudo hostnamectl set-hostname

```
[ec2-user@ip-172-31-43-32 ~]$ sudo hostnamectl set-hostname node-2
```

SSH node-3 instance 

sudo hostnamectl set-hostname

```
[ec2-user@ip-172-31-43-32 ~]$ sudo hostnamectl set-hostname node-3
```

sudo vi /etc/hosts/

```
[ec2-user@Ansible-Server ~]$ sudo vi /etc/hosts
172.31.0.10 Ansible-Server
172.31.0.11 node-1
172.31.0.12 node-2
172.31.0.13 node-3
```

"Now let's check the connectivity."

```
[ec2-user@Ansible-Server ~]$ ping node-1PING node-1 (172.31.0.11) 56(84) bytes of data.--- node-1 ping statistics ---4 packets transmitted, 0 received, 100% packet loss, time 3091ms[ec2-user@Ansible-Server ~]$
```

Go to your Aws account and add allow icmp - IPv4 in security group

```
[ec2-user@Ansible-Server ~]$ ping node-1PING node-1 (172.31.0.11) 56(84) bytes of data.64 bytes from node-1 (172.31.0.11): icmp_seq=1 ttl=63 time=0.515 ms64 bytes from node-1 (172.31.0.11): icmp_seq=2 ttl=63 time=0.578 ms64 bytes from node-1 (172.31.0.11): icmp_seq=3 ttl=63 time=0.547 ms64 bytes from node-1 (172.31.0.11): icmp_seq=4 ttl=63 time=0.426 ms^C--- node-1 ping statistics ---4 packets transmitted, 4 received, 0% packet loss, time 3089msrtt min/avg/max/mdev = 0.426/0.516/0.578/0.056 ms[ec2-user@Ansible-Server ~]$[ec2-user@Ansible-Server ~]$ ping node-2
PING node-2 (172.31.0.12) 56(84) bytes of data.
64 bytes from node-2 (172.31.0.12): icmp_seq=1 ttl=63 time=0.465 ms
64 bytes from node-2 (172.31.0.12): icmp_seq=2 ttl=63 time=0.551 ms
64 bytes from node-2 (172.31.0.12): icmp_seq=3 ttl=63 time=0.527 ms
64 bytes from node-2 (172.31.0.12): icmp_seq=4 ttl=63 time=0.477 ms
--- node-2 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3094ms
rtt min/avg/max/mdev = 0.465/0.505/0.551/0.035 ms
[ec2-user@Ansible-Server ~]$[ec2-user@Ansible-Server ~]$ ping node-3
PING node-3 (172.31.0.13) 56(84) bytes of data.
64 bytes from node-3 (172.31.0.13): icmp_seq=1 ttl=63 time=0.435 ms
64 bytes from node-3 (172.31.0.13): icmp_seq=2 ttl=63 time=0.520 ms
64 bytes from node-3 (172.31.0.13): icmp_seq=3 ttl=63 time=0.519 ms
--- node-3 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2044ms
rtt min/avg/max/mdev = 0.435/0.491/0.520/0.039 ms
[ec2-user@Ansible-Server ~]$
```

"Now, let's install the Ansible package on our machine."

```
[ec2-user@Ansible-Server ~]$ sudo dnf install ansible-core -yUpdating Subscription Management repositories.Unable to read consumer identityInstalled: ansible-core-2.14.2-5.el9_2.x86_64 git-core-2.39.3-1.el9_2.x86_64             libnsl2-2.0.0-1.el9.x86_64 libtirpc-1.3.3-1.el9.x86_64          mpdecimal-2.5.1-3.el9.x86_64          python3.11-3.11.2-2.el9_2.2.x86_64 python3.11-cffi-1.15.1-1.el9.x86_64 python3.11-cryptography-37.0.2-5.el9.x86_64 python3.11-libs-3.11.2-2.el9_2.2.x86_64 python3.11-pyyaml-6.0-1.el9.x86_64 python3.11-setuptools-wheel-65.5.1-2.el9.noarch python3.11-six-1.16.0-1.el9.noarch sshpass-1.09-4.el9.x86_64
Complete![ec2-user@Ansible-Server ~]$
```

lets verify ansible instalation

ansible --version

```
[ec2-user@Ansible-Server ~]$ ansible --versionansible [core 2.14.2]  config file = /etc/ansible/ansible.cfg  configured module search path = ['/home/ec2-user/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']  ansible python module location = /usr/lib/python3.11/site-packages/ansible  ansible collection location = /home/ec2-user/.ansible/collections:/usr/share/ansible/collections  executable location = /bin/ansible  python version = 3.11.2 (main, Sep 12 2023, 00:00:00) [GCC 11.3.1 20221121 (Red Hat 11.3.1-4)] (/usr/bin/python3.11)  jinja version = 3.1.2  libyaml = True[ec2-user@Ansible-Server ~]$
```

"Here, it's showing the location of our configuration file. If you want, you can create your own configuration file."
#### Inventory File (Static inventory)

"First, we need to understand the inventory file so that we can connect our nodes with the server."

"Inventory files come in two types: Static and Dynamic.

An inventory file is a file that contains a collection of your managed nodes, the machines you want to manage. In this file, groups of these machines are defined, allowing us to run tasks, commands, modules, or playbooks on them. The common formats for this file are INI or YAML.

**1. Static Inventory:**

 This type of file does not change frequently. Whatever is defined in this file remains fixed until you manually make changes. It serves as a blueprint or a test plan where entries for your hosts and their groups are specified.

 The default static inventory file is often found at /etc/ansible/hosts. You can also create your own inventory file if you prefer.

 Features of an inventory file include:

 1. Name: You can use any name you prefer.

 2. Path: There is no fixed path; you can create the file anywhere you want.

 3. Root Access: Not required.

 4. Language: Can be written in INI or YAML."

**now lets create our custom inventory file**

```
[ec2-user@Ansible-Server ~]$ mkdir inventory[ec2-user@Ansible-Server ~]$ cd inventory/[ec2-user@Ansible-Server inventory]$ vi nodes_details[olx]
node-1
node-2
[daraz]
node-3
[app]app1.shahzaib.cloudapp2.shahzaib.cloudapp3.shahzaib.cloud
[all]
node-1
node-2node-3
[test:children]olxdaraz
```

ansible olx --list-hosts -i ~/inventory/nodes_details

```
[ec2-user@Ansible-Server inventory]$ ansible olx --list-hosts -i ~/inventory/nodes_details  hosts (2):    node-1    node-2[ec2-user@Ansible-Server inventory]$ [ec2-user@Ansible-Server inventory]$ ansible all --list-hosts -i ~/inventory/nodes_details
 hosts (6):
 node-1
 node-2
 node-3
 app1.shahzaib.cloud
 app2.shahzaib.cloud
 app3.shahzaib.cloud
[ec2-user@Ansible-Server inventory]$
```

There are different ways to add nodes in inventory files

vi nodes

```
[ec2-user@Ansible-Server inventory]$ vi node-machines[redhat]
172.31.0.11
172.31.0.12

[ubuntu]
172.31.0.13
```

ansible ubuntu --list-hosts -i ~/inventory/

```
[ec2-user@Ansible-Server inventory]$ ansible ubuntu --list-hosts -i ~/inventory/  hosts (1):    172.31.0.13[ec2-user@Ansible-Server inventory]$ ansible redhat --list-hosts -i ~/inventory/ hosts (2): 172.31.0.11 172.31.0.12[ec2-user@Ansible-Server inventory]$ ansible all --list-hosts -i ~/inventory/ hosts (3): 172.31.0.11 172.31.0.12 172.31.0.13[ec2-user@Ansible-Server inventory]$
```

"If you want to use the default inventory file, you need to have root access."

sudo vi /etc/ansible/hosts/

```
[ec2-user@Ansible-Server inventory]$ sudo vi /etc/ansible/hosts[shahzaib]
172.31.0.11
172.31.0.12
172.31.0.13
```

ansible all --list-hosts

```
[ec2-user@Ansible-Server inventory]$ ansible all --list-hosts  hosts (3):    172.31.0.11    172.31.0.12    172.31.0.13[ec2-user@Ansible-Server inventory]$ ansible shahzaib --list-hosts  hosts (3):    172.31.0.11    172.31.0.12    172.31.0.13[ec2-user@Ansible-Server inventory]$
```

"If you want to make your custom inventory file the default inventory file the fellow these steps"

ansible --version

```
[ec2-user@Ansible-Server inventory]$ ansible --versionansible [core 2.14.2]  config file = /etc/ansible/ansible.cfg  configured module search path = ['/home/ec2-user/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']  ansible python module location = /usr/lib/python3.11/site-packages/ansible  ansible collection location = /home/ec2-user/.ansible/collections:/usr/share/ansible/collections  executable location = /bin/ansible  python version = 3.11.2 (main, Sep 12 2023, 00:00:00) [GCC 11.3.1 20221121 (Red Hat 11.3.1-4)] (/usr/bin/python3.11)  jinja version = 3.1.2  libyaml = True[ec2-user@Ansible-Server inventory]$
```

we need to edit ansible.cfg file

vi /etc/ansible/ansible.cfg

```
[ec2-user@Ansible-Server inventory]$ sudo vi  /etc/ansible/ansible.cfg[defaults]
inventory = /home/ec2-user/inventory/
```

ansible all --list-hosts

```
[ec2-user@Ansible-Server inventory]$ ansible redhat --list-hosts  hosts (2):    172.31.0.11    172.31.0.12[ec2-user@Ansible-Server inventory]$ ansible ubuntu --list-hosts  hosts (1):    172.31.0.13[ec2-user@Ansible-Server inventory]$ ansible all --list-hosts  hosts (3):    172.31.0.11    172.31.0.12    172.31.0.13[ec2-user@Ansible-Server inventory]$
```

now we our custom define inventory file is set as default inventory for ansible 

"Now, let's remove the changes we made."

```
[ec2-user@Ansible-Server inventory]$ sudo vi  /etc/ansible/ansible.cfg[defaults]
inventory = /home/ec2-user/inventory/
```

ansible --version

```
[ec2-user@Ansible-Server inventory]$ ansible --versionansible [core 2.14.2]  config file = /etc/ansible/ansible.cfg  configured module search path = ['/home/ec2-user/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']  ansible python module location = /usr/lib/python3.11/site-packages/ansible  ansible collection location = /home/ec2-user/.ansible/collections:/usr/share/ansible/collections  executable location = /bin/ansible  python version = 3.11.2 (main, Sep 12 2023, 00:00:00) [GCC 11.3.1 20221121 (Red Hat 11.3.1-4)] (/usr/bin/python3.11)  jinja version = 3.1.2  libyaml = True[ec2-user@Ansible-Server inventory]$
```

"Now, let's see how we can create our own configuration file."

vi ansible.cfg

```
[ec2-user@Ansible-Server ~]$ vi ansible.cfg[defaults]
inventory = /home/ec2-user/inventory/
```

lest verify out ansible config file address

ansible --version

```
[ec2-user@Ansible-Server ~]$ ansible --versionansible [core 2.14.2]  config file = /home/ec2-user/ansible.cfg  configured module search path = ['/home/ec2-user/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']  ansible python module location = /usr/lib/python3.11/site-packages/ansible  ansible collection location = /home/ec2-user/.ansible/collections:/usr/share/ansible/collections  executable location = /usr/bin/ansible  python version = 3.11.2 (main, Sep 12 2023, 00:00:00) [GCC 11.3.1 20221121 (Red Hat 11.3.1-4)] (/usr/bin/python3.11)  jinja version = 3.1.2  libyaml = True[ec2-user@Ansible-Server ~]$[ec2-user@Ansible-Server ~]$ ansible all --list-host
 hosts (3):
 172.31.0.11
 172.31.0.12
 172.31.0.13
[ec2-user@Ansible-Server ~]$
```

"If the inventory file is in your home directory, it will be automatically fetched. However, if you create it in a different location, you will need to export its path."

```
[ec2-user@Ansible-Server ~]$ cp ansible.cfg /home/ec2-user/olx/ansible.cfg[ec2-user@Ansible-Server ~]$ echo $ANSIBLE_CONFIG[ec2-user@Ansible-Server ~]$ export ANSIBLE_CONFIG=/home/ec2-user/olx/ansible.cfg[ec2-user@Ansible-Server ~]$ echo $ANSIBLE_CONFIG/home/ec2-user/olx/ansible.cfg[ec2-user@Ansible-Server ~]$ ansible --versionansible [core 2.14.2]  config file = /home/ec2-user/olx/ansible.cfg  configured module search path = ['/home/ec2-user/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']  ansible python module location = /usr/lib/python3.11/site-packages/ansible  ansible collection location = /home/ec2-user/.ansible/collections:/usr/share/ansible/collections  executable location = /usr/bin/ansible  python version = 3.11.2 (main, Sep 12 2023, 00:00:00) [GCC 11.3.1 20221121 (Red Hat 11.3.1-4)] (/usr/bin/python3.11)  jinja version = 3.1.2  libyaml = True[ec2-user@Ansible-Server ~]$
```

"If you want to make this entry permanent, you need to add it to your `bashrc` file."
##### Let's understand the order in which Ansible reads the configuration file:

1. Ansible first checks the value of the exported variable (if set).

2. Next, it looks in the present working directory.

3. After that, it checks the user's HOME directory.

4. If Ansible doesn't find the configuration file in any of these locations, it loads the configuration from the default location: `/etc/ansible/hosts`."
Lest Remove createed changes

```
[ec2-user@Ansible-Server ~]$ unset ANSIBLE_CONFIG[ec2-user@Ansible-Server ~]$ echo $ANSIBLE_CONFIG[ec2-user@Ansible-Server ~]$ lsansible.cfg  inventory  olx[ec2-user@Ansible-Server ~]$ rm -rvf *removed 'ansible.cfg'removed 'inventory/node-machines'removed directory 'inventory'removed 'olx/ansible.cfg'removed directory 'olx'[ec2-user@Ansible-Server ~]$ ansible --versionansible [core 2.14.2]  config file = /etc/ansible/ansible.cfg  configured module search path = ['/home/ec2-user/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']  ansible python module location = /usr/lib/python3.11/site-packages/ansible  ansible collection location = /home/ec2-user/.ansible/collections:/usr/share/ansible/collections  executable location = /usr/bin/ansible  python version = 3.11.2 (main, Sep 12 2023, 00:00:00) [GCC 11.3.1 20221121 (Red Hat 11.3.1-4)] (/usr/bin/python3.11)  jinja version = 3.1.2  libyaml = True[ec2-user@Ansible-Server ~]$
```

#### Connection with Manage Nodes

"Now, let's see how we can establish a connection to our Ansible server with our managed nodes. There are three ways to do this:

**1. Password-Based:**

 This method involves connecting using passwords for authentication.

**2. Password-less or Key-Based:**

 In this approach, connections are established using SSH keys, allowing password-less logins.

**3. Inventory-Based:**

 Connections are established based on the inventory file, which contains information about hosts and their connection details."
sudo vi /etc/ansible/hosts

```
[ec2-user@Ansible-Server ~]$ sudo vi /etc/ansible/hosts[redhat]
172.31.0.11
172.31.0.12 
[ubuntu]
172.31.0.13 
```

Password base

ansible all -m ping

```
[ec2-user@Ansible-Server ~]$ ansible all -m pingThe authenticity of host '172.31.0.11 (172.31.0.11)' can't be established.ED25519 key fingerprint is SHA256:Ybu4SIjsogi47q7FLJhx4Z+dJonvOf3FiH/6zp2Reok.This key is not known by any other namesThe authenticity of host '172.31.0.13 (172.31.0.13)' can't be established.ED25519 key fingerprint is SHA256:9No4P95JZXL664azox4IvvnbSUPQCWVjRBcWlRya2jw.This key is not known by any other namesThe authenticity of host '172.31.0.12 (172.31.0.12)' can't be established.ED25519 key fingerprint is SHA256:MpVobyfN/xW9RlWuOmjTlOLzwsVn4h3pU8ID72/kNZ8.This key is not known by any other namesAre you sure you want to continue connecting (yes/no/[fingerprint])? yes3.110.182.172 | UNREACHABLE! => {    "changed": false,    "msg": "Failed to connect to the host via ssh: Warning: Permanently added '172.31.0.11' (ED25519) to the list of known hosts.\r\nec2-user@172.31.0.11: Permission denied (publickey,gssapi-keyex,gssapi-with-mic).",    "unreachable": true}adminPlease type 'yes', 'no' or the fingerprint: yes65.0.17.220 | UNREACHABLE! => {    "changed": false,    "msg": "Failed to connect to the host via ssh: Warning: Permanently added '172.31.0.12' (ED25519) to the list of known hosts.\r\nec2-user@172.31.0.12: Permission denied (publickey,gssapi-keyex,gssapi-with-mic).",    "unreachable": true}adminPlease type 'yes', 'no' or the fingerprint: yes65.2.152.159 | UNREACHABLE! => {    "changed": false,    "msg": "Failed to connect to the host via ssh: Warning: Permanently added '172.31.0.13' (ED25519) to the list of known hosts.\r\nec2-user@172.31.0.13: Permission denied (publickey).",    "unreachable": true}[ec2-user@Ansible-Server ~]$
```

first we need edite our nodes ssh_confg file or allow passwordbase authentication yes

sudo vi /etc/ssh/sshd_config

```
[ec2-user@node-1 ~]$ sudo vi /etc/ssh/sshd_configPasswordAuthentication yes # Disable password authenticationPubkeyAuthentication yes # Enable public key authenticationPermitRootLogin yes[ec2-user@node-1 ~]$ sudo systemctl restart sshd
```

add ansible user to all node-s and add this user entry in sudoers file so we can easy fire our superuser commands.

useradd ansible

```
[ec2-user@node-1 ~]$ sudo -i[root@node-1 ~]# useradd ansible[root@node-1 ~]# echo "<redacted>" | passwd --stdin ansible
Changing password for user ansible.passwd: all authentication tokens updated successfully.[root@node-1 ~]# echo "ansible ALL=(ALL) NOPASSWD:ALL" | sudo tee /etc/sudoers.d/ansibleansible ALL=(ALL) NOPASSWD:ALL[root@node-1 ~]#
```

node-2

useradd ansible

```
[root@node-2 ~]# useradd ansible[root@node-2 ~]# echo "<redacted>" | passwd --stdin ansible
Changing password for user ansible.passwd: all authentication tokens updated successfully.[root@node-2 ~]# echo "ansible ALL=(ALL) NOPASSWD:ALL" | sudo tee /etc/sudoers.d/ansibleansible ALL=(ALL) NOPASSWD:ALL[root@node-2 ~]#
```

node-3

adduser ansible

```
ubuntu@node-3:~$ sudo -iroot@node-3:~# adduser ansibleAdding user `ansible' ...Adding new group `ansible' (1001) ...Adding new user `ansible' (1001) with group `ansible' ...Creating home directory `/home/ansible' ...Copying files from `/etc/skel' ...New password:Retype new password:passwd: password updated successfullyChanging the user information for ansibleEnter the new value, or press ENTER for the default        Full Name []:        Room Number []:        Work Phone []:        Home Phone []:        Other []:Is the information correct? [Y/n] yroot@node-3:~# echo "ansible ALL=(ALL) NOPASSWD:ALL" | sudo tee /etc/sudoers.d/ansibleansible ALL=(ALL) NOPASSWD:ALLroot@node-3:~#
```

also set password for you instances defaults accounts 

```
[root@Ansible-Server ~]# passwd ec2-userChanging password for user ec2-user.New password:BAD PASSWORD: The password is shorter than 8 charactersRetype new password:passwd: all authentication tokens updated successfully.[root@Ansible-Server ~]#[root@node-1 ~]# passwd ec2-userChanging password for user ec2-user.New password:BAD PASSWORD: The password is shorter than 8 charactersRetype new password:passwd: all authentication tokens updated successfully.[root@node-1 ~]# passwd rootChanging password for user root.New password:BAD PASSWORD: The password is shorter than 8 charactersRetype new password:passwd: all authentication tokens updated successfully.[root@node-1 ~]#[root@node-2 ~]# passwd ec2-userChanging password for user ec2-user.New password:BAD PASSWORD: The password is shorter than 8 charactersRetype new password:passwd: all authentication tokens updated successfully.[root@node-2 ~]# passwd rootChanging password for user root.New password:BAD PASSWORD: The password is shorter than 8 charactersRetype new password:passwd: all authentication tokens updated successfully.[root@node-2 ~]#root@node-3:~# passwd ubuntuNew password:Retype new password:passwd: password updated successfullyroot@node-3:~# passwd rootNew password:Retype new password:passwd: password updated successfullyroot@node-3:~#
```

lets ping our nodes

ansible all -m ping -k

```
[ansible@Ansible-Server ~]$ ansible all -m ping65.2.152.159 | SUCCESS => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": false,    "ping": "pong"}172.31.0.11 | SUCCESS => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": false,    "ping": "pong"}172.31.0.12 | SUCCESS => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": false,    "ping": "pong"}[ansible@Ansible-Server ~]$
```

#### Password-less Connection

"To establish a password-less connection, you need to copy your SSH key to both nodes."

ssh-keygen

```
[ansible@Ansible-Server ~]$ ssh-keygenGenerating public/private rsa key pair.Enter file in which to save the key (/home/ansible/.ssh/id_rsa):Enter passphrase (empty for no passphrase):Enter same passphrase again:Your identification has been saved in /home/ansible/.ssh/id_rsaYour public key has been saved in /home/ansible/.ssh/id_rsa.pubThe key fingerprint is:SHA256:JFqzZ5vH5S9dXAJMkM5ywcskG06kHRaXP6rKNnHNCug ansible@Ansible-ServerThe key's randomart image is:+---[RSA 3072]----+|       .=oo*.    ||       ++o* o    ||      =ooO + .   ||     o =+ * o . .||    ... S= ... o.||    . oo.++o    o||   .   +ooo .. . ||    E.o o.  ...  ||     .oo     ..  |+----[SHA256]-----+[ansible@Ansible-Server ~]$
```

copy ssh key on all nodes 

ssh-copy-id ansible@node[1-3]

```
[ansible@Ansible-Server ~]$ ssh-copy-id ansible@node-1/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "/home/ansible/.ssh/id_rsa.pub"The authenticity of host 'node-1 (172.31.0.11)' can't be established.ED25519 key fingerprint is SHA256:Ybu4SIjsogi47q7FLJhx4Z+dJonvOf3FiH/6zp2Reok.This host key is known by the following other names/addresses:    ~/.ssh/known_hosts:1: 3.110.182.172Are you sure you want to continue connecting (yes/no/[fingerprint])? yes/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keysansible@node-1's password:Number of key(s) added: 1Now try logging into the machine, with:   "ssh 'ansible@node-1'"and check to make sure that only the key(s) you wanted were added.[ansible@Ansible-Server ~]$ ssh-copy-id ansible@node-2/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "/home/ansible/.ssh/id_rsa.pub"The authenticity of host 'node-2 (172.31.0.12)' can't be established.ED25519 key fingerprint is SHA256:MpVobyfN/xW9RlWuOmjTlOLzwsVn4h3pU8ID72/kNZ8.This host key is known by the following other names/addresses:    ~/.ssh/known_hosts:3: 65.0.17.220Are you sure you want to continue connecting (yes/no/[fingerprint])? yes/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keysansible@node-2's password:Number of key(s) added: 1Now try logging into the machine, with:   "ssh 'ansible@node-2'"and check to make sure that only the key(s) you wanted were added.[ansible@Ansible-Server ~]$ ssh-copy-id ansible@node-3/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "/home/ansible/.ssh/id_rsa.pub"The authenticity of host 'node-3 (172.31.0.13)' can't be established.ED25519 key fingerprint is SHA256:9No4P95JZXL664azox4IvvnbSUPQCWVjRBcWlRya2jw.This host key is known by the following other names/addresses:    ~/.ssh/known_hosts:2: 65.2.152.159Are you sure you want to continue connecting (yes/no/[fingerprint])? yes/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keysansible@node-3's password:Number of key(s) added: 1Now try logging into the machine, with:   "ssh 'ansible@node-3'"and check to make sure that only the key(s) you wanted were added.[ansible@Ansible-Server ~]$
```

try to ssh 

ssh node[1-3]

```
[ansible@Ansible-Server ~]$ ssh node-1Register this system with Red Hat Insights: insights-client --registerCreate an account or view all your systems at https://red.ht/insights-dashboardLast login: Thu Oct 26 04:59:47 2023 from 172.31.0.10[ansible@node-1 ~]$ exitlogoutConnection to node-1 closed.[ansible@Ansible-Server ~]$ ssh node-2Register this system with Red Hat Insights: insights-client --registerCreate an account or view all your systems at https://red.ht/insights-dashboardLast login: Thu Oct 26 04:59:47 2023 from 172.31.0.10[ansible@node-2 ~]$ exitlogoutConnection to node-2 closed.[ansible@Ansible-Server ~]$ ssh node-3Welcome to Ubuntu 22.04.3 LTS (GNU/Linux 6.2.0-1012-aws x86_64) * Documentation:  https://help.ubuntu.com * Management:     https://landscape.canonical.com * Support:        https://ubuntu.com/advantage  System information as of Thu Oct 26 05:07:06 UTC 2023  System load:  0.0               Processes:             108  Usage of /:   24.1% of 7.57GB   Users logged in:       1  Memory usage: 23%               IPv4 address for eth0: 172.31.32.20  Swap usage:   0%Expanded Security Maintenance for Applications is not enabled.38 updates can be applied immediately.27 of these updates are standard security updates.To see these additional updates run: apt list --upgradableEnable ESM Apps to receive additional future security updates.See https://ubuntu.com/esm or run: sudo pro statusLast login: Thu Oct 26 04:59:47 2023 from 43.205.117.145ansible@node-3:~$ exitlogoutConnection to node-3 closed.[ansible@Ansible-Server ~]$
```

decscription

Commad

```
[ansible@Ansible-Server ~]$ mkdir automation[ansible@Ansible-Server ~]$ cd automation/[ansible@Ansible-Server automation]$ vi ansible.cfg[defaults]inventory = ./inventoryhost_key_checking = falseremote_user = zybiask_pass = False
[privilege_escalation]become = truebecome_method = sudobecome_user = rootbecome_ask_pass= False[ansible@Ansible-Server automation]$ vi inventory[redhat]
172.31.0.11
172.31.0.12 
[ubuntu]
172.31.0.13 [ansible@Ansible-Server automation]$
```

lest try to ping our nodes

ansible all -m ping 

```
[ansible@Ansible-Server automation]$ ansible all -m ping65.2.152.159 | SUCCESS => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": false,    "ping": "pong"}172.31.0.11 | SUCCESS => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": false,    "ping": "pong"}172.31.0.12 | SUCCESS => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": false,    "ping": "pong"}[ansible@Ansible-Server automation]$
```

"Now, let's remove what we have created here."

rm -rvf *

#### Inventory Based

```
useradd hamza
echo "<redacted>" | passwd --stdin hamza
echo "hamza ALL=(ALL) NOPASSWD:ALL" | sudo tee /etc/sudoers.d/hamzasu hamzamkdir automationcd automationvi ansible.cfg[defaults]inventory = ./inventoryhost_key_checking = falsevi inventory[web]
172.31.0.11 ansible_ssh_user=zybi ansible_ssh_pass=<redacted>
172.31.0.12 ansible_ssh_user=zybi ansible_ssh_pass=<redacted>
172.31.0.13 ansible_ssh_user=zybi ansible_ssh_pass=<redacted>saveansible all -m ping 
```

#### Ansible Ad-Hoc Commands & Modules

Ad-Hoc Commands are used for one-time automation tasks. They are written and executed directly on the command line, allowing you to perform quick tasks without writing a playbook. These commands use Ansible modules to perform specific actions on managed nodes.

Modules are Ansible's way of abstracting certain system tasks, such as managing packages, files, services, etc. Modules are used by Ad-Hoc Commands and Playbooks to perform specific automation tasks on the managed nodes.

Understanding Ad-Hoc Commands and modules is essential before learning to write Ansible Playbooks. While Ad-Hoc Commands are suitable for quick tasks, Playbooks are used for more complex and repetitive tasks, providing a more organized and maintainable way to manage your infrastructure."

"1. Ansible Ad-Hoc Commands:

 Ansible Ad-Hoc Commands are commands that reside within /usr/bin/ansible. They are used to automate single tasks and are fast, easy to use, but not reusable. Ad-Hoc Commands are not suitable for tasks that need to be performed repeatedly.

2. Ansible Modules:

 Modules are units of code that allow us to control and manage system resources easily. They enable the execution of system commands. For example:

 ansible webserver -m yum -a "name=httpd state=latest"

 In this command, the 'yum' module is used to manage packages. It ensures that the 'httpd' package is installed and is in the latest state on the 'webserver' host."

"Now, if you want, you can use the default inventory file, or you can create your own inventory file. Here, we will use Ansible's default inventory file."
##### rm -rvf *

```
[ansible@Ansible-Server automation]$ cd[ansible@Ansible-Server ~]$ rm -rvf *removed directory 'automation'[ansible@Ansible-Server ~]$ ansible --versionansible [core 2.14.2]  config file = /etc/ansible/ansible.cfg  configured module search path = ['/home/ansible/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']  ansible python module location = /usr/lib/python3.11/site-packages/ansible  ansible collection location = /home/ansible/.ansible/collections:/usr/share/ansible/collections  executable location = /bin/ansible  python version = 3.11.2 (main, Sep 12 2023, 00:00:00) [GCC 11.3.1 20221121 (Red Hat 11.3.1-4)] (/usr/bin/python3.11)  jinja version = 3.1.2  libyaml = True[ansible@Ansible-Server ~]$ sudo vi /etc/ansible/hosts[ansible@Ansible-Server ~]$[redhat]
node-1
node-2
[ubuntu]
node-3[ansible@Ansible-Server ~]$ ansible all --list-hosts hosts (3): node-1 node-2 node-3[ansible@Ansible-Server ~]$
```

"If you want to see the available modules on your machine, you can use the following command:
##### ansible-doc -l

```
[ansible@Ansible-Server ~]$ ansible-doc -lansible.builtin.apt                    Manages apt-packagesansible.builtin.apt_key                Add or remove an apt keyansible.builtin.apt_repository         Add and remove APT repositoriesansible.builtin.assert                 Asserts given expressions are trueansible.builtin.async_status           Obtain status of asynchronous taskansible.builtin.command                Execute commands on targetsansible.builtin.copy                   Copy files to remote locationsansible.builtin.cron                   Manage cron.d and crontab entries
```

**##### important Modules**
- Copy
- Command
- Raw
- Shell
- File
- Fetch
- Get_url
- Lineinfile
- Replace
- User
- Group
- Yum
- Package
- Stat
- Mount
- Setup
- Systemd
- Debug
- Uri
- Parted
- Cron
- Script
- Service

##### Copy Module
"Using the `copy` module, we can copy files from the Ansible server to managed nodes."

```
[ansible@Ansible-Server ~]$ echo "This is ansible lab" > read.me[ansible@Ansible-Server ~]$ ansible all -m copy -a 'src=read.me dest=/tmp'node-3 | CHANGED => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": true,    "checksum": "47b70d64a526bf8ed03762d5d5ab68247c38d916",    "dest": "/tmp/read.me",    "gid": 1001,    "group": "ansible",    "md5sum": "55126c6131cb873b227cde9f6dccc463",    "mode": "0664",    "owner": "ansible",    "size": 20,    "src": "/home/ansible/.ansible/tmp/ansible-tmp-1698299220.5933018-2356-249856831982890/source",    "state": "file",    "uid": 1001}node-1 | CHANGED => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": true,    "checksum": "47b70d64a526bf8ed03762d5d5ab68247c38d916",    "dest": "/tmp/read.me",    "gid": 1001,    "group": "ansible",    "md5sum": "55126c6131cb873b227cde9f6dccc463",    "mode": "0644",    "owner": "ansible",    "secontext": "unconfined_u:object_r:user_home_t:s0",    "size": 20,    "src": "/home/ansible/.ansible/tmp/ansible-tmp-1698299220.462766-2354-93913610666888/source",    "state": "file",    "uid": 1001}node-2 | CHANGED => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": true,    "checksum": "47b70d64a526bf8ed03762d5d5ab68247c38d916",    "dest": "/tmp/read.me",    "gid": 1001,    "group": "ansible",    "md5sum": "55126c6131cb873b227cde9f6dccc463",    "mode": "0644",    "owner": "ansible",    "secontext": "unconfined_u:object_r:user_home_t:s0",    "size": 20,    "src": "/home/ansible/.ansible/tmp/ansible-tmp-1698299220.3630748-2355-30214545301825/source",    "state": "file",    "uid": 1001}[ansible@Ansible-Server ~]$
```

go to nodes machines and very file is copied or not
##### Go to node[1-3]

```
[ansible@node-1 ~]$ ll /tmp/read.me-rw-r--r--. 1 ansible ansible 20 Oct 26 05:47 /tmp/read.me[ansible@node-1 ~]$[ansible@node-2 ~]$ ll /tmp/read.me-rw-r--r--. 1 ansible ansible 20 Oct 26 05:47 /tmp/read.me[ansible@node-2 ~]$ansible@node-3:~$ ll /tmp/read.me-rw-rw-r-- 1 ansible ansible 20 Oct 26 05:47 /tmp/read.meansible@node-3:~$
```

we can also very file by using command module
##### ansible all -m command -a 'ls -lh /tmp/read.me'

```
[ansible@Ansible-Server ~]$ ansible all -m command -a 'ls -lh /tmp/read.me'node-3 | CHANGED | rc=0 >>-rw-rw-r-- 1 ansible ansible 20 Oct 26 05:47 /tmp/read.menode-1 | CHANGED | rc=0 >>-rw-r--r--. 1 ansible ansible 20 Oct 26 05:47 /tmp/read.menode-2 | CHANGED | rc=0 >>-rw-r--r--. 1 ansible ansible 20 Oct 26 05:47 /tmp/read.me[ansible@Ansible-Server ~]$
```

if you want to know more about copy module.
##### ansible-doc copy

```
[ansible@Ansible-Server ~]$ ansible-doc copy> ANSIBLE.BUILTIN.COPY    (/usr/lib/python3.11/site-packages/ansible/modules/copy.py)        The `copy' module copies a file from the local or remote machine to a location on the        remote machine. Use the [ansible.builtin.fetch] module to copy files from remote locations        to the local box. If you need variable interpolation in copied files, use the        [ansible.builtin.template] module. Using a variable in the `content' field will result in        unpredictable output. For Windows targets, use the [ansible.windows.win_copy] module        instead.ADDED IN: historical  * note: This module has a corresponding action plugin.OPTIONS (= is mandatory):- attributes        The attributes the resulting filesystem object should have.        To get supported flags look at the man page for `chattr' on the target system.        This string should contain the attributes in the same order as the one displayed by        `lsattr'.        The `=' operator is assumed as default, otherwise `+' or `-' operators need to be included        in the string.        aliases: [attr]        default: null        type: str        added in: version 2.3 of ansible-core- backup
```

let see if we want to try copy this file at any location where ansible user did not have permission.
##### ansible all -m copy -a 'src=read.me dest=/opt'

```
[ansible@Ansible-Server ~]$ ansible all -m copy -a 'src=read.me dest=/opt'node-3 | FAILED! => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": false,    "checksum": "47b70d64a526bf8ed03762d5d5ab68247c38d916",    "msg": "Destination /opt not writable"}node-1 | FAILED! => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": false,    "checksum": "47b70d64a526bf8ed03762d5d5ab68247c38d916",    "msg": "Destination /opt not writable"}node-2 | FAILED! => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": false,    "checksum": "47b70d64a526bf8ed03762d5d5ab68247c38d916",    "msg": "Destination /opt not writable"}[ansible@Ansible-Server ~]$
```

for executing the ansible module we need to be come sudo
##### ansible all -m copy -a 'src=read.me dest=/opt -u root -k '

```
[ansible@Ansible-Server ~]$ ansible all -m copy -a 'src=read.me dest=/opt' -u root -kSSH password:node-3 | CHANGED => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": true,    "checksum": "47b70d64a526bf8ed03762d5d5ab68247c38d916",    "dest": "/opt/read.me",    "gid": 0,    "group": "root",    "md5sum": "55126c6131cb873b227cde9f6dccc463",    "mode": "0644",    "owner": "root",    "size": 20,    "src": "/root/.ansible/tmp/ansible-tmp-1698300124.6965148-2624-74453159114433/source",    "state": "file",    "uid": 0}node-1 | CHANGED => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": true,    "checksum": "47b70d64a526bf8ed03762d5d5ab68247c38d916",    "dest": "/opt/read.me",    "gid": 0,    "group": "root",    "md5sum": "55126c6131cb873b227cde9f6dccc463",    "mode": "0644",    "owner": "root",    "secontext": "system_u:object_r:usr_t:s0",    "size": 20,    "src": "/root/.ansible/tmp/ansible-tmp-1698300124.3605645-2622-146786021762323/source",    "state": "file",    "uid": 0}node-2 | CHANGED => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": true,    "checksum": "47b70d64a526bf8ed03762d5d5ab68247c38d916",    "dest": "/opt/read.me",    "gid": 0,    "group": "root",    "md5sum": "55126c6131cb873b227cde9f6dccc463",    "mode": "0644",    "owner": "root",    "secontext": "system_u:object_r:usr_t:s0",    "size": 20,    "src": "/root/.ansible/tmp/ansible-tmp-1698300124.3860288-2623-113272638282617/source",    "state": "file",    "uid": 0}[ansible@Ansible-Server ~]$
```

but this is not good practice.

"And we can also perform this task using the `sudo` command. For this, the user should have an entry in the sudoers file."
##### ansible all -m copy -a 'src=read.me dest=/opt/myfile' -b --become-method sudo

```
[ansible@Ansible-Server ~]$ ansible all -m copy -a 'src=read.me dest=/opt/myfile' -b --become-method sudonode-1 | CHANGED => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": true,    "checksum": "47b70d64a526bf8ed03762d5d5ab68247c38d916",    "dest": "/opt/myfile",    "gid": 0,    "group": "root",    "md5sum": "55126c6131cb873b227cde9f6dccc463",    "mode": "0644",    "owner": "root",    "secontext": "system_u:object_r:usr_t:s0",    "size": 20,    "src": "/home/ansible/.ansible/tmp/ansible-tmp-1698300296.2832031-2754-178168841188251/source",    "state": "file",    "uid": 0}node-2 | CHANGED => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": true,    "checksum": "47b70d64a526bf8ed03762d5d5ab68247c38d916",    "dest": "/opt/myfile",    "gid": 0,    "group": "root",    "md5sum": "55126c6131cb873b227cde9f6dccc463",    "mode": "0644",    "owner": "root",    "secontext": "system_u:object_r:usr_t:s0",    "size": 20,    "src": "/home/ansible/.ansible/tmp/ansible-tmp-1698300296.2964385-2755-143952912184831/source",    "state": "file",    "uid": 0}node-3 | CHANGED => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": true,    "checksum": "47b70d64a526bf8ed03762d5d5ab68247c38d916",    "dest": "/opt/myfile",    "gid": 0,    "group": "root",    "md5sum": "55126c6131cb873b227cde9f6dccc463",    "mode": "0644",    "owner": "root",    "size": 20,    "src": "/home/ansible/.ansible/tmp/ansible-tmp-1698300297.1310909-2756-143424586836947/source",    "state": "file",    "uid": 0}[ansible@Ansible-Server ~]$
```

also we can use 
##### ansible all -m copy -a 'src=read.me dest=/opt/myfile2' -b
lest check which user is executing the ansible command#### ansible all -m command -a 'id'

```
[ansible@Ansible-Server ~]$ ansible all -m command -a 'id'node-1 | CHANGED | rc=0 >>uid=1001(ansible) gid=1001(ansible) groups=1001(ansible) context=unconfined_u:unconfined_r:unconfined_t:s0-s0:c0.c1023node-2 | CHANGED | rc=0 >>uid=1001(ansible) gid=1001(ansible) groups=1001(ansible) context=unconfined_u:unconfined_r:unconfined_t:s0-s0:c0.c1023node-3 | CHANGED | rc=0 >>uid=1001(ansible) gid=1001(ansible) groups=1001(ansible)[ansible@Ansible-Server ~]$ ansible all -m command -a 'id' -bnode-3 | CHANGED | rc=0 >>uid=0(root) gid=0(root) groups=0(root)node-1 | CHANGED | rc=0 >>uid=0(root) gid=0(root) groups=0(root) context=unconfined_u:unconfined_r:unconfined_t:s0-s0:c0.c1023node-2 | CHANGED | rc=0 >>uid=0(root) gid=0(root) groups=0(root) context=unconfined_u:unconfined_r:unconfined_t:s0-s0:c0.c1023[ansible@Ansible-Server ~]$
```

"If you don't want to use `-b` or `become_user` repeatedly, you need to change the default configuration in Ansible settings.
##### sudo vi /etc/ansible/ansible.cfg

```
sudo vi /etc/ansible/ansible.cfg[privilege_escalation]become = true
```

##### commanddescription
##### command

```
[ansible@Ansible-Server ~]$ ansible all -m command -a 'id'node-3 | CHANGED | rc=0 >>uid=0(root) gid=0(root) groups=0(root)node-2 | CHANGED | rc=0 >>uid=0(root) gid=0(root) groups=0(root) context=unconfined_u:unconfined_r:unconfined_t:s0-s0:c0.c1023node-1 | CHANGED | rc=0 >>uid=0(root) gid=0(root) groups=0(root) context=unconfined_u:unconfined_r:unconfined_t:s0-s0:c0.c1023[ansible@Ansible-Server ~]$
```

"Let's say you want to copy a file with specified permissions."
##### ansible all -m copy -a 'src=read.me dest=/root mode=0755 owner=ansible group=wheel'

```
[ansible@Ansible-Server ~]$ ansible all -m copy -a 'src=read.me dest=/root mode=0755 owner=ansible group=wheel'node-3 | FAILED! => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": false,    "checksum": "47b70d64a526bf8ed03762d5d5ab68247c38d916",    "gid": 0,    "group": "root",    "mode": "0644",    "msg": "chgrp failed: failed to look up group wheel",    "owner": "ansible",    "path": "/root/read.me",    "size": 20,    "state": "file",    "uid": 1001}node-2 | CHANGED => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": true,    "checksum": "47b70d64a526bf8ed03762d5d5ab68247c38d916",    "dest": "/root/read.me",    "gid": 10,    "group": "wheel",    "mode": "0755",    "owner": "ansible",    "path": "/root/read.me",    "secontext": "system_u:object_r:admin_home_t:s0",    "size": 20,    "state": "file",    "uid": 1001}node-1 | CHANGED => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": true,    "checksum": "47b70d64a526bf8ed03762d5d5ab68247c38d916",    "dest": "/root/read.me",    "gid": 10,    "group": "wheel",    "mode": "0755",    "owner": "ansible",    "path": "/root/read.me",    "secontext": "system_u:object_r:admin_home_t:s0",    "size": 20,    "state": "file",    "uid": 1001}[ansible@Ansible-Server ~]$ #file did not copy on node-3 because in ubuntu their is no wheel group[ansible@Ansible-Server ~]$ ansible redhat -m command -a 'ls -lh /root/read.me'node-2 | CHANGED | rc=0 >>-rwxr-xr-x. 1 ansible wheel 20 Oct 26 06:16 /root/read.menode-1 | CHANGED | rc=0 >>-rwxr-xr-x. 1 ansible wheel 20 Oct 26 06:16 /root/read.me[ansible@Ansible-Server ~]$
```

If you want to copy a file from one location to another on your managed nodes...
##### ansible all -m copy -a 'src=/root/read.me dest=/tmp/newfile remote_src=yes'

```
[ansible@Ansible-Server ~]$ ansible all -m copy -a 'src=/root/read.me dest=/tmp/newfile remote_src=yes'node-3 | CHANGED => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": true,    "checksum": "47b70d64a526bf8ed03762d5d5ab68247c38d916",    "dest": "/tmp/newfile",    "gid": 0,    "group": "root",    "md5sum": "55126c6131cb873b227cde9f6dccc463",    "mode": "0644",    "owner": "root",    "size": 20,    "src": "/root/read.me",    "state": "file",    "uid": 0}node-2 | CHANGED => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": true,    "checksum": "47b70d64a526bf8ed03762d5d5ab68247c38d916",    "dest": "/tmp/newfile",    "gid": 0,    "group": "root",    "md5sum": "55126c6131cb873b227cde9f6dccc463",    "mode": "0644",    "owner": "root",    "secontext": "system_u:object_r:admin_home_t:s0",    "size": 20,    "src": "/root/read.me",    "state": "file",    "uid": 0}node-1 | CHANGED => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": true,    "checksum": "47b70d64a526bf8ed03762d5d5ab68247c38d916",    "dest": "/tmp/newfile",    "gid": 0,    "group": "root",    "md5sum": "55126c6131cb873b227cde9f6dccc463",    "mode": "0644",    "owner": "root",    "secontext": "system_u:object_r:admin_home_t:s0",    "size": 20,    "src": "/root/read.me",    "state": "file",    "uid": 0}[ansible@Ansible-Server ~]$[ansible@Ansible-Server ~]$ ansible all -m command -a 'ls -lh /tmp/newfile'
node-3 | CHANGED | rc=0 >>
-rw-r--r-- 1 root root 20 Oct 26 06:19 /tmp/newfile
node-2 | CHANGED | rc=0 >>
-rw-r--r--. 1 root root 20 Oct 26 06:16 /tmp/newfile
node-1 | CHANGED | rc=0 >>
-rw-r--r--. 1 root root 20 Oct 26 06:16 /tmp/newfile
[ansible@Ansible-Server ~]$
```

"When we copy a file, it overwrites the existing one. If you want to create a backup before copying a file..."
##### ansible all -m copy -a 'src=read.me dest/root/ backup=yes'

```
[ansible@Ansible-Server ~]$ ansible all -m copy -a 'src=read.me dest=root/ backup=yes'
node-3 | CHANGED => {
 "ansible_facts": {
 "discovered_interpreter_python": "/usr/bin/python3"
 },
 "changed": true,
 "checksum": "47b70d64a526bf8ed03762d5d5ab68247c38d916",
 "dest": "root/read.me",
 "gid": 0,
 "group": "root",
 "md5sum": "55126c6131cb873b227cde9f6dccc463",
 "mode": "0644",
 "owner": "root",
 "size": 20,
 "src": "/home/ansible/.ansible/tmp/ansible-tmp-1698301935.3888988-3351-233653186437768/source",
 "state": "file",
 "uid": 0
}
node-2 | CHANGED => {
 "ansible_facts": {
 "discovered_interpreter_python": "/usr/bin/python3"
 },
 "changed": true,
 "checksum": "47b70d64a526bf8ed03762d5d5ab68247c38d916",
 "dest": "root/read.me",
 "gid": 0,
 "group": "root",
 "md5sum": "55126c6131cb873b227cde9f6dccc463",
 "mode": "0644",
 "owner": "root",
 "secontext": "unconfined_u:object_r:user_home_t:s0",
 "size": 20,
 "src": "/home/ansible/.ansible/tmp/ansible-tmp-1698301935.1521108-3350-186134287439889/source",
 "state": "file",
 "uid": 0
}
node-1 | CHANGED => {
 "ansible_facts": {
 "discovered_interpreter_python": "/usr/bin/python3"
 },
 "changed": true,
 "checksum": "47b70d64a526bf8ed03762d5d5ab68247c38d916",
 "dest": "root/read.me",
 "gid": 0,
 "group": "root",
 "md5sum": "55126c6131cb873b227cde9f6dccc463",
 "mode": "0644",
 "owner": "root",
 "secontext": "unconfined_u:object_r:user_home_t:s0",
 "size": 20,
 "src": "/home/ansible/.ansible/tmp/ansible-tmp-1698301935.1909003-3349-216573577302110/source",
 "state": "file",
 "uid": 0
}
[ansible@Ansible-Server ~]$

[ansible@Ansible-Server ~]$ ansible all -m command -a 'ls -lh /root'
node-3 | CHANGED | rc=0 >>
total 8.0K
-rw-r--r-- 1 ansible root 20 Oct 26 06:19 read.me
drwx------ 4 root root 4.0K Oct 25 10:49 snap
node-1 | CHANGED | rc=0 >>
total 4.0K
-rwxr-xr-x. 1 ansible wheel 20 Oct 26 06:16 read.me
node-2 | CHANGED | rc=0 >>
total 4.0K
-rwxr-xr-x. 1 ansible wheel 20 Oct 26 06:16 read.me
[ansible@Ansible-Server ~]$
```

we need to add ansible module that's are available on ansible galaxy 
##### ansible-galaxy collection install ansible.posix

```
[ansible@Ansible-Server ~]$ ansible-galaxy collection install ansible.posixStarting galaxy collection install processProcess install dependency mapStarting collection install processDownloading https://galaxy.ansible.com/api/v3/plugin/ansible/content/published/collections/artifacts/ansible-posix-1.5.4.tar.gz to /home/ansible/.ansible/tmp/ansible-local-3332inr2fskl/tmpsgu6vbkj/ansible-posix-1.5.4-9frfx29nInstalling 'ansible.posix:1.5.4' to '/home/ansible/.ansible/collections/ansible_collections/ansible/posix'ansible.posix:1.5.4 was installed successfully[ansible@Ansible-Server ~]$
```

##### Command Modules

"We can use it to execute a command on our nodes."
##### ansible all -m command -a 'uptime'

```
[ansible@Ansible-Server ~]$ ansible all -m command -a 'uptime'node-3 | CHANGED | rc=0 >> 06:35:35 up  2:54,  5 users,  load average: 0.06, 0.03, 0.01node-2 | CHANGED | rc=0 >> 06:35:35 up  2:54,  2 users,  load average: 0.01, 0.01, 0.00node-1 | CHANGED | rc=0 >> 06:35:35 up  2:54,  1 user,  load average: 1.00, 0.99, 0.85[ansible@Ansible-Server ~]$[ansible@Ansible-Server ~]$ ansible ubuntu -m command -a 'uptime ; lsblk'
node-3 | FAILED | rc=1 >>

Usage:
 uptime [options]

Options:
 -p, --pretty show uptime in pretty format
 -h, --help display this help and exit
 -s, --since system up since
 -V, --version output version information and exit

For more details see uptime(1).non-zero return code
[ansible@Ansible-Server ~]$
```

"The `command` module will only work if your machine has Python version 2.4 installed. Additionally, the `command` module doesn't allow the execution of multiple commands. For that purpose, you need to use the `raw` module."
##### ansible ubuntu -m raw -a 'uptime ; lsblk'

```
[ansible@Ansible-Server ~]$ ansible ubuntu -m raw -a 'uptime ; lsblk'node-3 | CHANGED | rc=0 >> 06:38:24 up  2:57,  5 users,  load average: 0.04, 0.03, 0.00NAME     MAJ:MIN RM   SIZE RO TYPE MOUNTPOINTSloop0      7:0    0  24.6M  1 loop /snap/amazon-ssm-agent/7528loop1      7:1    0  24.9M  1 loop /snap/amazon-ssm-agent/7628loop2      7:2    0  55.7M  1 loop /snap/core18/2790loop3      7:3    0  63.5M  1 loop /snap/core20/2015loop4      7:4    0 111.9M  1 loop /snap/lxd/24322loop5      7:5    0  40.8M  1 loop /snap/snapd/20092loop6      7:6    0  40.9M  1 loop /snap/snapd/20290xvda     202:0    0     8G  0 disk├─xvda1  202:1    0   7.9G  0 part /├─xvda14 202:14   0     4M  0 part└─xvda15 202:15   0   106M  0 part /boot/efiShared connection to node-3 closed.[ansible@Ansible-Server ~]$
```

#### Shell Module

We use the `shell` module to execute remote commands, run scripts, or start a new shell on the managed nodes.
##### vi myscript.sh

```
[ansible@Ansible-Server ~]$ vi myscript.sh[ansible@Ansible-Server ~]$ cat myscript.sh#!/bin/bashecho "This is Ansible Lab"[ansible@Ansible-Server ~]$ 
```

copy our sheel script to nodes 
##### ansible all -m copy -a 'src=myscript.sh dest=/root/ mode=755'
**##### ansible all -m shell -a '/root/myscript.sh'**

```
[ansible@Ansible-Server ~]$ ansible all -m copy -a 'src=myscript.sh dest=/root/ mode=755'node-3 | CHANGED => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": true,    "checksum": "a06a3d3a6515e1ee6820dbde4b514d95860a5cea",    "dest": "/root/myscript.sh",    "gid": 0,    "group": "root",    "md5sum": "7dfa55b1a5581296bf6085c391fb9ac7",    "mode": "0755",    "owner": "root",    "size": 39,    "src": "/home/ansible/.ansible/tmp/ansible-tmp-1698302671.1968052-3605-45114135745186/source",    "state": "file",    "uid": 0}node-2 | CHANGED => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": true,    "checksum": "a06a3d3a6515e1ee6820dbde4b514d95860a5cea",    "dest": "/root/myscript.sh",    "gid": 0,    "group": "root",    "md5sum": "7dfa55b1a5581296bf6085c391fb9ac7",    "mode": "0755",    "owner": "root",    "secontext": "system_u:object_r:admin_home_t:s0",    "size": 39,    "src": "/home/ansible/.ansible/tmp/ansible-tmp-1698302670.8619237-3604-24637721564188/source",    "state": "file",    "uid": 0}node-1 | CHANGED => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": true,    "checksum": "a06a3d3a6515e1ee6820dbde4b514d95860a5cea",    "dest": "/root/myscript.sh",    "gid": 0,    "group": "root",    "md5sum": "7dfa55b1a5581296bf6085c391fb9ac7",    "mode": "0755",    "owner": "root",    "secontext": "system_u:object_r:admin_home_t:s0",    "size": 39,    "src": "/home/ansible/.ansible/tmp/ansible-tmp-1698302670.9563932-3603-82398881778485/source",    "state": "file",    "uid": 0}[ansible@Ansible-Server ~]$[ansible@Ansible-Server ~]$ ansible all -m shell -a '/root/myscript.sh'
node-3 | CHANGED | rc=0 >>
This is Ansible Lab
node-2 | CHANGED | rc=0 >>
This is Ansible Lab
node-1 | CHANGED | rc=0 >>
This is Ansible Lab
[ansible@Ansible-Server ~]$
```

##### File Module

We use the **file **module to perform actions on files and directories.

"Now, let's create a directory on the nodes using the **file** module."
##### command

```
[ansible@Ansible-Server ~]$ ansible all -m file -a 'path=/tmp/data state=directory'node-3 | CHANGED => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": true,    "gid": 0,    "group": "root",    "mode": "0755",    "owner": "root",    "path": "/tmp/data",    "size": 4096,    "state": "directory",    "uid": 0}node-2 | CHANGED => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": true,    "gid": 0,    "group": "root",    "mode": "0755",    "owner": "root",    "path": "/tmp/data",    "secontext": "unconfined_u:object_r:user_tmp_t:s0",    "size": 6,    "state": "directory",    "uid": 0}node-1 | CHANGED => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": true,    "gid": 0,    "group": "root",    "mode": "0755",    "owner": "root",    "path": "/tmp/data",    "secontext": "unconfined_u:object_r:user_tmp_t:s0",    "size": 6,    "state": "directory",    "uid": 0}[ansible@Ansible-Server ~]$
```

"If you make a mistake, Ansible will suggest corrections for you."

```
[ansible@Ansible-Server ~]$ ansible ubuntu -m file -a 'path=/tmp/data state=directoy'node-3 | FAILED! => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": false,    "msg": "value of state must be one of: absent, directory, file, hard, link, touch, got: directoy"}[ansible@Ansible-Server ~]$
```

"If you want to remove a directory..."
##### ansible all -m file -a 'path=/tmp/data state=absent'

```
[ansible@Ansible-Server ~]$ ansible all -m file -a 'path=/tmp/data state=absent'node-3 | CHANGED => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": true,    "path": "/tmp/data",    "state": "absent"}node-2 | CHANGED => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": true,    "path": "/tmp/data",    "state": "absent"}node-1 | CHANGED => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": true,    "path": "/tmp/data",    "state": "absent"}[ansible@Ansible-Server ~]$[ansible@Ansible-Server ~]$ ansible all -m command -a 'ls -ld /tmp/data'node-2 | FAILED | rc=2 >>ls: cannot access '/tmp/data': No such file or directorynon-zero return codenode-3 | FAILED | rc=2 >>ls: cannot access '/tmp/data': No such file or directorynon-zero return codenode-1 | FAILED | rc=2 >>ls: cannot access '/tmp/data': No such file or directorynon-zero return code[ansible@Ansible-Server ~]$
```

##### Fetch Module

"This is the reverse of the `copy` module. With this, we can copy files from nodes to the Ansible server."
##### ansible all -m fatch -a 'src=/root/read.me dest=backup'

```
[ansible@Ansible-Server ~]$ ansible all -m fetch -a 'src=/root/read.me dest=backup'node-3 | CHANGED => {    "changed": true,    "checksum": "47b70d64a526bf8ed03762d5d5ab68247c38d916",    "dest": "/home/ansible/backup/node-3/root/read.me",    "md5sum": "55126c6131cb873b227cde9f6dccc463",    "remote_checksum": "47b70d64a526bf8ed03762d5d5ab68247c38d916",    "remote_md5sum": null}node-2 | CHANGED => {    "changed": true,    "checksum": "47b70d64a526bf8ed03762d5d5ab68247c38d916",    "dest": "/home/ansible/backup/node-2/root/read.me",    "md5sum": "55126c6131cb873b227cde9f6dccc463",    "remote_checksum": "47b70d64a526bf8ed03762d5d5ab68247c38d916",    "remote_md5sum": null}node-1 | CHANGED => {    "changed": true,    "checksum": "47b70d64a526bf8ed03762d5d5ab68247c38d916",    "dest": "/home/ansible/backup/node-1/root/read.me",    "md5sum": "55126c6131cb873b227cde9f6dccc463",    "remote_checksum": "47b70d64a526bf8ed03762d5d5ab68247c38d916",    "remote_md5sum": null}[ansible@Ansible-Server ~]$[ansible@Ansible-Server ~]$ ls
backup
[ansible@Ansible-Server ~]$ cd backup/
[ansible@Ansible-Server backup]$ ls
node-1 node-2 node-3
[ansible@Ansible-Server backup]$
```

**Get_url Modules**

The **get_url **module in Ansible downloads files from URLs to managed nodes.
##### ansible all -m get_url -a 'url=https://linux-training.be/linuxfun.pdf dest=/tmp/linuxfun.pdf'

```
[ansible@Ansible-Server ~]$ ansible all -m get_url -a 'url=https://linux-training.be/linuxfun.pdf dest=/tmp/linuxfun.pdf'node-3 | CHANGED => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": true,    "checksum_dest": null,    "checksum_src": "5d315220d46f1c607decd6a96118efc4bd56af0f",    "dest": "/tmp/linuxfun.pdf",    "elapsed": 1,    "gid": 0,    "group": "root",    "md5sum": "127a5ac6776c2933c37f7b2f9e005369",    "mode": "0644",    "msg": "OK (7022363 bytes)",    "owner": "root",    "size": 7022363,    "src": "/home/ansible/.ansible/tmp/ansible-tmp-1698316145.7147741-2049-256993882915424/tmp7vgjr7dn",    "state": "file",    "status_code": 200,    "uid": 0,    "url": "https://linux-training.be/linuxfun.pdf"}node-2 | CHANGED => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": true,    "checksum_dest": null,    "checksum_src": "5d315220d46f1c607decd6a96118efc4bd56af0f",    "dest": "/tmp/linuxfun.pdf",    "elapsed": 2,    "gid": 0,    "group": "root",    "md5sum": "127a5ac6776c2933c37f7b2f9e005369",    "mode": "0644",    "msg": "OK (7022363 bytes)",    "owner": "root",    "secontext": "unconfined_u:object_r:user_home_t:s0",    "size": 7022363,    "src": "/home/ansible/.ansible/tmp/ansible-tmp-1698316145.4211748-2048-211843187936243/tmpe9rk4kd9",    "state": "file",    "status_code": 200,    "uid": 0,    "url": "https://linux-training.be/linuxfun.pdf"}node-1 | CHANGED => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": true,    "checksum_dest": null,    "checksum_src": "5d315220d46f1c607decd6a96118efc4bd56af0f",    "dest": "/tmp/linuxfun.pdf",    "elapsed": 8,    "gid": 0,    "group": "root",    "md5sum": "127a5ac6776c2933c37f7b2f9e005369",    "mode": "0644",    "msg": "OK (7022363 bytes)",    "owner": "root",    "secontext": "unconfined_u:object_r:user_home_t:s0",    "size": 7022363,    "src": "/home/ansible/.ansible/tmp/ansible-tmp-1698316150.0181334-2047-175344048415219/tmpzkh__uc5",    "state": "file",    "status_code": 200,    "uid": 0,    "url": "https://linux-training.be/linuxfun.pdf"}[ansible@Ansible-Server ~]$ ansible all -m command -a 'ls -lh /tmp/linuxfun.pdf'node-3 | CHANGED | rc=0 >>-rw-r--r-- 1 root root 6.7M Oct 26 10:29 /tmp/linuxfun.pdfnode-2 | CHANGED | rc=0 >>-rw-r--r--. 1 root root 6.7M Oct 26 10:29 /tmp/linuxfun.pdfnode-1 | CHANGED | rc=0 >>-rw-r--r--. 1 root root 6.7M Oct 26 10:29 /tmp/linuxfun.pdf[ansible@Ansible-Server ~]$
```

##### sudo vi /etc/ansible/ansible.cfg

```
[ansible@Ansible-Server ~]$ sudo vi /etc/ansible/ansible.cfg
[defaults]
host_key_checking = false

[privilege_escalation]
become= true
become_method = sudo
```

**##### Lineinfile Module**

"We use the `lineinfile` module when we need to append or erase a specific line in a file."
##### ansible all -m lineinfile -a 'dest=/root/read.me line="by Rao Shahzaib"'

```
[ansible@Ansible-Server ~]$ ansible all -m lineinfile -a 'dest=/root/read.me line="By Rao Shahzaib"'node-3 | CHANGED => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "backup": "",    "changed": true,    "msg": "line added"}node-2 | CHANGED => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "backup": "",    "changed": true,    "msg": "line added"}node-1 | CHANGED => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "backup": "",    "changed": true,    "msg": "line added"}[ansible@Ansible-Server ~]$ ansible all -m command -a 'cat /root/read.me'node-3 | CHANGED | rc=0 >>This is ansible labBy Rao Shahzaibnode-2 | CHANGED | rc=0 >>This is ansible labBy Rao Shahzaibnode-1 | CHANGED | rc=0 >>This is ansible labBy Rao Shahzaib[ansible@Ansible-Server ~]$
```

"If you need to add a line to the beginning of a file..."
##### ansible all -m lineinfile -a 'dest=/root/read.me line="Devops" insertafter=BOF'

```
[ansible@Ansible-Server ~]$ ansible all -m lineinfile -a 'dest=/root/read.me line="Devops" insertafter=BOF'node-3 | CHANGED => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "backup": "",    "changed": true,    "msg": "line added"}node-2 | CHANGED => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "backup": "",    "changed": true,    "msg": "line added"}node-1 | CHANGED => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "backup": "",    "changed": true,    "msg": "line added"}[ansible@Ansible-Server ~]$ ansible all -m command -a 'cat /root/read.me'node-3 | CHANGED | rc=0 >>DevopsThis is ansible labBy Rao Shahzaibnode-2 | CHANGED | rc=0 >>DevopsThis is ansible labBy Rao Shahzaibnode-1 | CHANGED | rc=0 >>DevopsThis is ansible labBy Rao Shahzaib[ansible@Ansible-Server ~]$
```

"If you need to add a line to the end of a file..."
##### ansible all -m lineinfile -a 'dest=/root/read.me line=" best of luck" insertafter=Subhan'

```
[ansible@Ansible-Server ~]$ ansible all -m lineinfile -a 'dest=/root/read.me line="ansile is important tool" insertafter=EOF'node-3 | CHANGED => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "backup": "",    "changed": true,    "msg": "line added"}node-2 | CHANGED => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "backup": "",    "changed": true,    "msg": "line added"}node-1 | CHANGED => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "backup": "",    "changed": true,    "msg": "line added"}[ansible@Ansible-Server ~]$ ansible all -m command -a 'cat /root/read.me'node-3 | CHANGED | rc=0 >>DevopsThis is ansible labBy Rao Shahzaibansile is important toolnode-2 | CHANGED | rc=0 >>DevopsThis is ansible labBy Rao Shahzaibansile is important toolnode-1 | CHANGED | rc=0 >>DevopsThis is ansible labBy Rao Shahzaibansile is important tool[ansible@Ansible-Server ~]$
```

"If you want to add a line after a specific keyword..."
**##### ansible all -m lineinfile -a 'dest=/root/read.me line="by RedHat" insertafter=toll'**

```
[ansible@Ansible-Server ~]$ ansible all -m lineinfile -a 'dest=/root/read.me line="by RedHat" insertafter=toll'node-2 | CHANGED => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "backup": "",    "changed": true,    "msg": "line added"}node-3 | CHANGED => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "backup": "",    "changed": true,    "msg": "line added"}node-1 | CHANGED => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "backup": "",    "changed": true,    "msg": "line added"}[ansible@Ansible-Server ~]$[ansible@Ansible-Server ~]$ ansible all -m command -a 'cat /root/read.me'node-2 | CHANGED | rc=0 >>DevopsThis is ansible labBy Rao Shahzaibansile is important toolby RedHatnode-3 | CHANGED | rc=0 >>DevopsThis is ansible labBy Rao Shahzaibansile is important toolby RedHatnode-1 | CHANGED | rc=0 >>DevopsThis is ansible labBy Rao Shahzaibansile is important toolby RedHat[ansible@Ansible-Server ~]$
```

##### Replace Module

"With this module, you can replace a specific string."
##### command

```
[ansible@Ansible-Server ~]$ ansible all -m command -a 'cat /root/read.me'node-3 | CHANGED | rc=0 >>DevopsThis is ansible labBy Rao Shahzaibansile is important toolby RedHatnode-2 | CHANGED | rc=0 >>DevopsThis is ansible labBy Rao Shahzaibansile is important toolby RedHatnode-1 | CHANGED | rc=0 >>DevopsThis is ansible labBy Rao Shahzaibansile is important toolby RedHat[ansible@Ansible-Server ~]$ ansible all -m replace -a "dest=/root/read.me regexp='^ansible' replace='ANSIBLE'"node-3 | SUCCESS => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": false,    "msg": "",    "rc": 0}node-2 | SUCCESS => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": false,    "msg": "",    "rc": 0}node-1 | SUCCESS => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": false,    "msg": "",    "rc": 0}[ansible@Ansible-Server ~]$ 
```

##### User Module

"We use it to manage user accounts."

"Let's add a user and assign them to a group using this module."
##### ansible redhat -m user -a 'name=shazaib state=present uid=1010 groups=wheel'

```
[ansible@Ansible-Server ~]$ ansible redhat -m user -a 'name=shazaib state=present uid=1010 groups=wheel'node-2 | SUCCESS => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "append": false,    "changed": false,    "comment": "",    "group": 1010,    "groups": "wheel",    "home": "/home/shazaib",    "move_home": false,    "name": "shazaib",    "shell": "/bin/bash",    "state": "present",    "uid": 1010}[ansible@Ansible-Server ~]$"Now, let's delete this user."[ansible@Ansible-Server ~]$ ansible redhat -m user -a 'name=shahzaib state=absent'node-2 | SUCCESS => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": false,    "name": "shahzaib",    "state": "absent"}node-1 | SUCCESS => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": false,    "name": "shahzaib",    "state": "absent"}[ansible@Ansible-Server ~]$
```

##### Group Module

"We use it to manage groups."
##### ansible node-2 -m group -a 'name=staff state=present gid=1015

```
[ansible@Ansible-Server ~]$ ansible all -m group -a 'name=staff state=present gid=1015'node-3 | CHANGED => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": true,    "gid": 1015,    "name": "staff",    "state": "present",    "system": false}node-2 | CHANGED => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": true,    "gid": 1015,    "name": "staff",    "state": "present",    "system": false}node-1 | CHANGED => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": true,    "gid": 1015,    "name": "staff",    "state": "present",    "system": false}[ansible@Ansible-Server ~]$[ansible@Ansible-Server ~]$ ansible all -m command -a 'tail -5 /etc/group'node-3 | CHANGED | rc=0 >>netdev:x:119:ubuntulxd:x:120:ubuntu_chrony:x:121:ubuntu:x:1000:ansible:x:1001:node-2 | CHANGED | rc=0 >>ec2-user:x:1000:ansible:x:1001:shazaib:x:1010:ali:x:1011:staff:x:1015:node-1 | CHANGED | rc=0 >>sgx:x:992:systemd-oom:x:991:ec2-user:x:1000:ansible:x:1001:staff:x:1015:[ansible@Ansible-Server ~]$
```

lets delete this group
##### ansible all -m group -a 'name=staff state=absent'

```
[ansible@Ansible-Server ~]$ ansible all -m group -a 'name=staff state=absent'node-3 | CHANGED => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": true,    "name": "staff",    "state": "absent"}node-2 | CHANGED => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": true,    "name": "staff",    "state": "absent"}node-1 | CHANGED => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": true,    "name": "staff",    "state": "absent"}[ansible@Ansible-Server ~]$ ansible all -m command -a 'tail -5 /etc/group'node-3 | CHANGED | rc=0 >>netdev:x:119:ubuntulxd:x:120:ubuntu_chrony:x:121:ubuntu:x:1000:ansible:x:1001:node-2 | CHANGED | rc=0 >>systemd-oom:x:991:ec2-user:x:1000:ansible:x:1001:shazaib:x:1010:ali:x:1011:node-1 | CHANGED | rc=0 >>chrony:x:993:sgx:x:992:systemd-oom:x:991:ec2-user:x:1000:ansible:x:1001:[ansible@Ansible-Server ~]$
```

##### Yum/Dnf/Apt/Package Modules

"With these modules, we can install, remove, and update packages. Now, let's use a module to install a package."
##### ansible all -m yum -a 'name=zsh state=present'

```
[ansible@Ansible-Server ~]$ ansible all -m yum -a 'name=zsh state=present'node-3 | FAILED! => {    "ansible_facts": {        "pkg_mgr": "apt"    },    "changed": false,    "msg": [        "Could not detect which major revision of yum is in use, which is required to determine module backend.",        "You should manually specify use_backend to tell the module whether to use the yum (yum3) or dnf (yum4) backend})"    ]}node-2 | CHANGED => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": true,    "msg": "",    "rc": 0,    "results": [        "Installed: zsh-5.8-9.el9.x86_64"    ]}node-1 | CHANGED => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": true,    "msg": "",    "rc": 0,    "results": [        "Installed: zsh-5.8-9.el9.x86_64"    ]}[ansible@Ansible-Server ~]$# node-3 is ubuntu base machine so that why zsh is not install on that machine [ansible@Ansible-Server ~]$ ansible redhat -m dnf -a 'name=ksh state=present'node-2 | CHANGED => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": true,    "msg": "",    "rc": 0,    "results": [        "Installed: ksh-3:1.0.0~beta.1-2.el9.x86_64"    ]}node-1 | CHANGED => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": true,    "msg": "",    "rc": 0,    "results": [        "Installed: ksh-3:1.0.0~beta.1-2.el9.x86_64"    ]}[ansible@Ansible-Server ~]$#for Ubuntu Machine we use apt[ansible@Ansible-Server ~]$ ansible ubuntu -m apt -a 'name=zsh state=present'node-3 | CHANGED => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "cache_update_time": 1698300325,    "cache_updated": false,    "changed": true,    "stderr": "",    "stderr_lines": [],    "stdout": "Reading package lists...\nBuilding dependency tree...\nReading state information...\nThe following additional packages will be installed:\n  zsh-common\nSuggested packages:\n  zsh-doc\nThe following NEW packages will be installed:\n  zsh zsh-common\n0 upgraded, 2 newly installed, 0 to remove and 23 not upgraded.\nNeed to get 4794 kB of archives.\nAfter this operation, 18.2 MB of additional disk space will be used.\nGet:1 http://ap-south-1.ec2.archive.ubuntu.com/ubuntu jammy/main amd64 zsh-common all 5.8.1-1 [3985 kB]\nGet:2 http://ap-south-1.ec2.archive.ubuntu.com/ubuntu jammy/main amd64 zsh amd64 5.8.1-1 [809 kB]\nFetched 4794 kB in 0s (46.4 MB/s)\nSelecting previously unselected package zsh-common.\r\n(Reading database ... \r(Reading database ... 5%\r(Reading database ... 10%\r(Reading database ... 15%\r(Reading database ... 20%\r(Reading database ... 25%\r(Reading database ... 30%\r(Reading database ... 35%\r(Reading database ... 40%\r(Reading database ... 45%\r(Reading database ... 50%\r(Reading database ... 55%\r(Reading database ... 60%\r(Reading database ... 65%\r(Reading database ... 70%\r(Reading database ... 75%\r(Reading database ... 80%\r(Reading database ... 85%\r(Reading database ... 90%\r(Reading database ... 95%\r(Reading database ... 100%\r(Reading database ... 94486 files and directories currently installed.)\r\nPreparing to unpack .../zsh-common_5.8.1-1_all.deb ...\r\nUnpacking zsh-common (5.8.1-1) ...\r\nSelecting previously unselected package zsh.\r\nPreparing to unpack .../archives/zsh_5.8.1-1_amd64.deb ...\r\nUnpacking zsh (5.8.1-1) ...\r\nSetting up zsh-common (5.8.1-1) ...\r\nSetting up zsh (5.8.1-1) ...\r\nProcessing triggers for man-db (2.10.2-1) ...\r\nNEEDRESTART-VER: 3.5\nNEEDRESTART-KCUR: 6.2.0-1014-aws\nNEEDRESTART-KEXP: 6.2.0-1014-aws\nNEEDRESTART-KSTA: 1\n",    "stdout_lines": [        "Reading package lists...",        "Building dependency tree...",        "Reading state information...",        "The following additional packages will be installed:",        "  zsh-common",        "Suggested packages:",        "  zsh-doc",        "The following NEW packages will be installed:",        "  zsh zsh-common",        "0 upgraded, 2 newly installed, 0 to remove and 23 not upgraded.",        "Need to get 4794 kB of archives.",        "After this operation, 18.2 MB of additional disk space will be used.",        "Get:1 http://ap-south-1.ec2.archive.ubuntu.com/ubuntu jammy/main amd64 zsh-common all 5.8.1-1 [3985 kB]",        "Get:2 http://ap-south-1.ec2.archive.ubuntu.com/ubuntu jammy/main amd64 zsh amd64 5.8.1-1 [809 kB]",        "Fetched 4794 kB in 0s (46.4 MB/s)",        "Selecting previously unselected package zsh-common.",        "(Reading database ... ",        "(Reading database ... 5%",        "(Reading database ... 10%",        "(Reading database ... 15%",        "(Reading database ... 20%",        "(Reading database ... 25%",        "(Reading database ... 30%",        "(Reading database ... 35%",        "(Reading database ... 40%",        "(Reading database ... 45%",        "(Reading database ... 50%",        "(Reading database ... 55%",        "(Reading database ... 60%",        "(Reading database ... 65%",        "(Reading database ... 70%",        "(Reading database ... 75%",        "(Reading database ... 80%",        "(Reading database ... 85%",        "(Reading database ... 90%",        "(Reading database ... 95%",        "(Reading database ... 100%",        "(Reading database ... 94486 files and directories currently installed.)",        "Preparing to unpack .../zsh-common_5.8.1-1_all.deb ...",        "Unpacking zsh-common (5.8.1-1) ...",        "Selecting previously unselected package zsh.",        "Preparing to unpack .../archives/zsh_5.8.1-1_amd64.deb ...",        "Unpacking zsh (5.8.1-1) ...",        "Setting up zsh-common (5.8.1-1) ...",        "Setting up zsh (5.8.1-1) ...",        "Processing triggers for man-db (2.10.2-1) ...",        "NEEDRESTART-VER: 3.5",        "NEEDRESTART-KCUR: 6.2.0-1014-aws",        "NEEDRESTART-KEXP: 6.2.0-1014-aws",        "NEEDRESTART-KSTA: 1"    ]}[ansible@Ansible-Server ~]$
```

lest verify our pkg is installed
##### ansible rhel -m command -a 'rpm -qi zsh'

```
[ansible@Ansible-Server ~]$ ansible redhat -m command -a 'rpm -qi zsh'node-2 | CHANGED | rc=0 >>Name        : zshVersion     : 5.8Release     : 9.el9Architecture: x86_64Install Date: Thu 26 Oct 2023 11:46:36 AM UTCGroup       : UnspecifiedSize        : 8018363License     : MITSignature   : RSA/SHA256, Thu 24 Feb 2022 03:59:15 PM UTC, Key ID 199e2f91fd431d51Source RPM  : zsh-5.8-9.el9.src.rpmBuild Date  : Wed 23 Feb 2022 02:10:14 PM UTCBuild Host  : x86-vm-56.build.eng.bos.redhat.comPackager    : Red Hat, Inc. <http://bugzilla.redhat.com/bugzilla>Vendor      : Red Hat, Inc.URL         : http://zsh.sourceforge.net/Summary     : Powerful interactive shellDescription :The zsh shell is a command interpreter usable as an interactive loginshell and as a shell script command processor.  Zsh resembles the kshshell (the Korn shell), but includes many enhancements.  Zsh supportscommand line editing, built-in spelling correction, programmablecommand completion, shell functions (with autoloading), a historymechanism, and more.node-1 | CHANGED | rc=0 >>Name        : zshVersion     : 5.8Release     : 9.el9Architecture: x86_64Install Date: Thu 26 Oct 2023 11:47:44 AM UTCGroup       : UnspecifiedSize        : 8018363License     : MITSignature   : RSA/SHA256, Thu 24 Feb 2022 03:59:15 PM UTC, Key ID 199e2f91fd431d51Source RPM  : zsh-5.8-9.el9.src.rpmBuild Date  : Wed 23 Feb 2022 02:10:14 PM UTCBuild Host  : x86-vm-56.build.eng.bos.redhat.comPackager    : Red Hat, Inc. <http://bugzilla.redhat.com/bugzilla>Vendor      : Red Hat, Inc.URL         : http://zsh.sourceforge.net/Summary     : Powerful interactive shellDescription :The zsh shell is a command interpreter usable as an interactive loginshell and as a shell script command processor.  Zsh resembles the kshshell (the Korn shell), but includes many enhancements.  Zsh supportscommand line editing, built-in spelling correction, programmablecommand completion, shell functions (with autoloading), a historymechanism, and more.[ansible@Ansible-Server ~]$ ansible ubuntu -m command -a 'apt list zsh'node-3 | CHANGED | rc=0 >>Listing...zsh/jammy,now 5.8.1-1 amd64 [installed]WARNING: apt does not have a stable CLI interface. Use with caution in scripts.[ansible@Ansible-Server ~]$
```

##### Global module (package module)
##### ansible all -m package -a 'name=htop state=latest'

```
[ansible@Ansible-Server ~]$ ansible all -m package -a 'name=htop state=latest'node-3 | SUCCESS => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "cache_update_time": 1698300325,    "cache_updated": false,    "changed": false}node-2 | FAILED! => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": false,    "failures": [        "No package htop available."    ],    "msg": "Failed to install some of the specified packages",    "rc": 1,    "results": []}node-1 | FAILED! => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": false,    "failures": [        "No package htop available."    ],    "msg": "Failed to install some of the specified packages",    "rc": 1,    "results": []}[ansible@Ansible-Server ~]$
```

node-1 and node-2 are RHEL base machine or we did not any subscription,that why the pkg is not able to install , we need to configure our elrepo for downlaod and install other pkgs.
##### Yum_repository
##### ansible redhat -m yum_repository -a 'name=test description="elrepo" baseurl=https://www.elrepo.org/elrepo-release-7.el7.elrepo.noarch.rpm enabled=1 gpgcheck=0'

```
[ansible@Ansible-Server ~]$ ansible redhat -m yum_repository -a 'name=test description="elrepo" baseurl=https://www.elrepo.org/elrepo-release-7.el7.elrepo.noarch.rpm enabled=1 gpgcheck=0'node-2 | CHANGED => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": true,    "repo": "test",    "state": "present"}node-1 | CHANGED => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": true,    "repo": "test",    "state": "present"}[ansible@Ansible-Server ~]$[ansible@Ansible-Server ~]$ ansible redhat -m command -a 'yum repolist all'node-2 | CHANGED | rc=0 >>Updating Subscription Management repositories.Unable to read consumer identityThis system is not registered with an entitlement server. You can use subscription-manager to register.repo id                                                                   repo name                             statuscodeready-builder-for-rhel-9-rhui-debug-rpms  Red Hat CodeReady Linux B disabledcodeready-builder-for-rhel-9-rhui-rpms             Red Hat CodeReady Linux B disabledcodeready-builder-for-rhel-9-rhui-source-rpms Red Hat CodeReady Linux B disabledrhel-9-appstream-rhui-debug-rpms                     Red Hat Enterprise Linux      disabledrhel-9-appstream-rhui-rpms                                Red Hat Enterprise Linux      enabledrhel-9-appstream-rhui-source-rpms                    Red Hat Enterprise Linux      disabledrhel-9-baseos-rhui-debug-rpms                          Red Hat Enterprise Linux      disabledrhel-9-baseos-rhui-rpms                                     Red Hat Enterprise Linux      enabledrhel-9-baseos-rhui-source-rpms                         Red Hat Enterprise Linux      disabledrhel-9-supplementary-rhui-debug-rpms             Red Hat Enterprise Linux      disabledrhel-9-supplementary-rhui-rpms                        Red Hat Enterprise Linux      disabledrhel-9-supplementary-rhui-source-rpms            Red Hat Enterprise Linux      disabledrhui-client-config-server-9                                 Red Hat Enterprise Linux      enabledtest                                                                      elrepo                                      enablednode-1 | CHANGED | rc=0 >>Updating Subscription Management repositories.Unable to read consumer identityThis system is not registered with an entitlement server. You can use subscription-manager to register.repo id                                                                   repo name                             statuscodeready-builder-for-rhel-9-rhui-debug-rpms  Red Hat CodeReady Linux B disabledcodeready-builder-for-rhel-9-rhui-rpms             Red Hat CodeReady Linux B disabledcodeready-builder-for-rhel-9-rhui-source-rpms Red Hat CodeReady Linux B disabledrhel-9-appstream-rhui-debug-rpms                     Red Hat Enterprise Linux      disabledrhel-9-appstream-rhui-rpms                                Red Hat Enterprise Linux      enabledrhel-9-appstream-rhui-source-rpms                    Red Hat Enterprise Linux      disabledrhel-9-baseos-rhui-debug-rpms                          Red Hat Enterprise Linux      disabledrhel-9-baseos-rhui-rpms                                     Red Hat Enterprise Linux      enabledrhel-9-baseos-rhui-source-rpms                         Red Hat Enterprise Linux      disabledrhel-9-supplementary-rhui-debug-rpms             Red Hat Enterprise Linux      disabledrhel-9-supplementary-rhui-rpms                        Red Hat Enterprise Linux      disabledrhel-9-supplementary-rhui-source-rpms            Red Hat Enterprise Linux      disabledrhui-client-config-server-9                                 Red Hat Enterprise Linux      enabledtest                                                                      elrepo                                      enabled[ansible@Ansible-Server ~]$
```

#### Stat Module

"The `stat` module is used to print information about files and directories."
##### ansible all -m stat -a 'path=/etc/passwd'

```
[ansible@Ansible-Server ~]$ ansible all -m stat -a 'path=/etc/passwd'node-3 | SUCCESS => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": false,    "stat": {        "atime": 1698294527.9051015,        "attr_flags": "e",        "attributes": [            "exten    }}node-2 | SUCCESS => {  "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": false,    "stat": {        "atime": 1698294527.9051015,        "attr_flags": "e",        "attributes": [            "exten    }}node-1 | SUCCESS => {   "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": false,    "stat": {        "atime": 1698294527.9051015,        "attr_flags": "e",        "attributes": [            "exten    }}[ansible@Ansible-Server ~]$ ansible all -m stat -a 'path=/dev/sda1'node-3 | SUCCESS => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": false,    "stat": {        "exists": false    }}node-2 | SUCCESS => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": false,    "stat": {        "exists": false    }}node-1 | SUCCESS => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": false,    "stat": {        "exists": false    }}[ansible@Ansible-Server ~]$
```

##### Mount Module 

"The `mount` module is used to activate, configure, and manage mount points, as well as add their entries to the `/etc/fstab` file."
##### ansible node-1 -m mount -a 'path=/opt/ src=/dev/sda fstype=xfs opts=defaults state=present'

```
attach 1 disk with your nodes or disk ko fxs type m formate kr k rakhn li jiyeansible node-1 -m mount -a 'path=/opt/ src=/dev/sda fstype=xfs opts=defaults state=present'ansible-doc -l | grep mountansible-galaxy collection install ansible.posixansible-doc -l | grep mountansible node-1 -m mount -a 'path=/opt/ src=/dev/sda fstype=xfs opts=defaults state=present'ansible node-1 -m command -a 'cat /etc/fstab'ansible node-1 -m command -a 'df -hT'ansible node-1 -m command -a 'mkfs.xfs /dev/sda'ansible node-1 -m command -a 'path=/opt/ src=/dev/sda fstype=xfs opts=defaults state=mounted'ansible node-1 -m command -a 'cat /etc/fstab'ansible node-1 -m command -a 'df -hT'ansible node-1 -m command -a 'path=/opt src=/dev/sda state=unmounted'ansible node-1 -m mount -a 'path=/opt src=/dev/sda state=absent_from_fstab'
```

##### Setup Module

"The `setup` module is used to gather information from managed nodes."
##### ansible all -m setup

```
ansible@Ansible-Server ~]$ ansible all -m setupnode-2 | SUCCESS => {    "ansible_facts": {        "ansible_all_ipv4_addresses": [            "172.31.37.148"        ],        "ansible_all_ipv6_addresses": [            "fe80::87:abff:fe3f:375e"        ],        "ansible_apparmor": {            "status": "disabled"        }, "ansible_virtualization_tech_host": [], "ansible_virtualization_type": "xen", "discovered_interpreter_python": "/usr/bin/python3", "gather_subset": [ "all" ], "module_setup": true }, "changed": false}[ansible@Ansible-Server ~]$
```

##### ansible all -m setup -a 'filter=*kernel*'

```
[ansible@Ansible-Server ~]$ ansible all -m setup -a 'filter=*kernel*'node-2 | SUCCESS => {    "ansible_facts": {        "ansible_kernel": "5.14.0-284.30.1.el9_2.x86_64",        "ansible_kernel_version": "#1 SMP PREEMPT_DYNAMIC Fri Aug 25 09:13:12 EDT 2023",        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": false}node-3 | SUCCESS => {    "ansible_facts": {        "ansible_kernel": "6.2.0-1014-aws",        "ansible_kernel_version": "#14~22.04.1-Ubuntu SMP Thu Oct  5 22:43:45 UTC 2023",        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": false}node-1 | SUCCESS => {    "ansible_facts": {        "ansible_kernel": "5.14.0-284.30.1.el9_2.x86_64",        "ansible_kernel_version": "#1 SMP PREEMPT_DYNAMIC Fri Aug 25 09:13:12 EDT 2023",        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": false}[ansible@Ansible-Server ~]$
```

##### Service Module

"The **service** module is used to start, stop, and restart services."
##### ansible redhat-m package -a 'name=httpd state=latest'
**ansible all -m service -a 'name=httpd state=started enabled=true'**

```
[ansible@Ansible-Server ~]$ ansible redhat -m package -a 'name=httpd state=latest'node-2 | CHANGED => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": true,    "msg": "",    "rc": 0,    "results": [        "Installed: mailcap-2.1.49-5.el9.noarch",        "Installed: mod_lua-2.4.53-11.el9_2.5.x86_64",        "Installed: httpd-2.4.53-11.el9_2.5.x86_64",        "Installed: httpd-core-2.4.53-11.el9_2.5.x86_64",        "Installed: apr-1.7.0-11.el9.x86_64",        "Installed: httpd-tools-2.4.53-11.el9_2.5.x86_64",        "Installed: apr-util-1.6.1-20.el9_2.1.x86_64",        "Installed: apr-util-bdb-1.6.1-20.el9_2.1.x86_64",        "Installed: mod_http2-1.15.19-4.el9_2.4.x86_64",        "Installed: httpd-filesystem-2.4.53-11.el9_2.5.noarch",        "Installed: apr-util-openssl-1.6.1-20.el9_2.1.x86_64",        "Installed: redhat-logos-httpd-90.4-1.el9.noarch"    ]}node-1 | CHANGED => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": true,    "msg": "",    "rc": 0,    "results": [        "Installed: mailcap-2.1.49-5.el9.noarch",        "Installed: mod_lua-2.4.53-11.el9_2.5.x86_64",        "Installed: httpd-2.4.53-11.el9_2.5.x86_64",        "Installed: httpd-core-2.4.53-11.el9_2.5.x86_64",        "Installed: apr-1.7.0-11.el9.x86_64",        "Installed: httpd-tools-2.4.53-11.el9_2.5.x86_64",        "Installed: apr-util-1.6.1-20.el9_2.1.x86_64",        "Installed: apr-util-bdb-1.6.1-20.el9_2.1.x86_64",        "Installed: mod_http2-1.15.19-4.el9_2.4.x86_64",        "Installed: httpd-filesystem-2.4.53-11.el9_2.5.noarch",        "Installed: apr-util-openssl-1.6.1-20.el9_2.1.x86_64",        "Installed: redhat-logos-httpd-90.4-1.el9.noarch"    ]}[ansible@Ansible-Server ~]$
```

##### ansible all -m service -a 'name=httpd state=started enabled=true'

```
[ansible@Ansible-Server ~]$ ansible redhat -m service -a 'name=httpd state=started enabled=true'node-2 | CHANGED => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": true,    "enabled": true,    "name": "httpd",    "state": "started",         "UMask": "0022",        "UnitFilePreset": "disabled",        "UnitFileState": "disabled",        "UtmpMode": "init",        "Wants": "httpd-init.service",        "WatchdogSignal": "6",        "WatchdogTimestampMonotonic": "0",        "WatchdogUSec": "infinity"    }}node-1 | CHANGED => {       "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": true,    "enabled": true,    "name": "httpd",    "state": "started",         "UMask": "0022",        "UnitFilePreset": "disabled",        "UnitFileState": "disabled",        "UtmpMode": "init",        "Wants": "httpd-init.service",        "WatchdogSignal": "6",        "WatchdogTimestampMonotonic": "0",        "WatchdogUSec": "infinity"    }}[ansible@Ansible-Server ~]$[ansible@Ansible-Server ~]$ ansible redhat -m service -a 'name=httpd state=restarted'
node-1 | CHANGED => {
 "ansible_facts": {
 "discovered_interpreter_python": "/usr/bin/python3"
 },
 "changed": true,
 "name": "httpd",
 "state": "started",
 "status": {
 "AccessSELinuxContext": "system_u:object_r:httpd_unit_file_t:s0",
 "ActiveEnterTimestamp": "Sat 2023-10-28 04:31:50 UTC",
 
 }
}
node-2 | CHANGED => {
 "ansible_facts": {
 "discovered_interpreter_python": "/usr/bin/python3"
 },
 "changed": true,
 "name": "httpd",
 "state": "started",
 "status": {
 "AccessSELinuxContext": "system_u:object_r:httpd_unit_file_t:s0",
 "ActiveEnterTimestamp": "Sat 2023-10-28 04:31:50 UTC",
 
 }
}
[ansible@Ansible-Server ~]$
[ansible@Ansible-Server ~]$ ansible redhat -m service -a 'name=httpd state=stopped enabled=false'
node-1 | CHANGED => {
 "ansible_facts": {
 "discovered_interpreter_python": "/usr/bin/python3"
 },
 "changed": true,
 "enabled": false,
 "name": "httpd",
 "state": "stopped",
 "status": {
}
node-2 | CHANGED => {
 "ansible_facts": {
 "discovered_interpreter_python": "/usr/bin/python3"
 },
 "changed": true,
 "enabled": false,
 "name": "httpd",
 "state": "stopped",
 "status": {
}
[ansible@Ansible-Server ~]$
```

##### Systemd Module

"We use the `systemd` module to control services and timers on the system."

"We want the system to reread its configuration."
##### ansible redhat-m systemd -a 'daemon-reload=true'

```
[ansible@Ansible-Server ~]$ ansible redhat -m systemd -a 'daemon-reload=true'node-2 | SUCCESS => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": false,    "name": null,    "status": {}}node-1 | SUCCESS => {    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": false,    "name": null,    "status": {}}[ansible@Ansible-Server ~]$[ansible@Ansible-Server ~]$ ansible redhat -m systemd -a 'daemon-reexec=yes'node-2 | SUCCESS => { "ansible_facts": { "discovered_interpreter_python": "/usr/bin/python3" }, "changed": false, "name": null, "status": {}}node-1 | SUCCESS => { "ansible_facts": { "discovered_interpreter_python": "/usr/bin/python3" }, "changed": false, "name": null, "status": {}}[ansible@Ansible-Server ~]$
```

"Now, let me demonstrate how to perform an action on a service using systemd."

```
ansible redhat-m package -a 'name=httpd state=latest'ansible redhat-m command -a 'systemctl status httpd'ansible redhat-m systemd -a 'name=httpd state=reloaded'ansible redhat-m systemd -a 'name=httpd state=stoped'ansible redhat-m systemd -a 'name=httpd state=restarted'ansible redhat-m systemd -a 'name=httpd enable=false'ansible redhat-m command -a 'systemctl status httpd'
```

##### Debug Module

"We use the **debug** module to print statements for debugging purposes."
##### ansible all -m debug -a 'msg="This is ansible lab"'
"Yes, we can use Ansible's built-in variables."

```
[ansible@Ansible-Server ~]$ ansible all -m debug -a 'msg="This is Ansible Lab"'node-1 | SUCCESS => {    "msg": "This is Ansible Lab"}node-2 | SUCCESS => {    "msg": "This is Ansible Lab"}node-3 | SUCCESS => {    "msg": "This is Ansible Lab"}[ansible@Ansible-Server ~]$[ansible@Ansible-Server ~]$ ansible all -m debug -a 'msg="{{ inventory_hostname }}"'node-1 | SUCCESS => { "msg": "node-1"}node-2 | SUCCESS => { "msg": "node-2"}node-3 | SUCCESS => { "msg": "node-3"}[ansible@Ansible-Server ~]$
```

##### Uri Module

"The `uri` module allows us to interact with HTTP or HTTPS services."
##### ansible all -m uri -a 'url=https://www.google.com'

```
[ansible@Ansible-Server ~]$ ansible all -m uri -a 'url=https://www.google.com'node-3 | SUCCESS => {    "accept_ranges": "none",    "alt_svc": "h3=\":443\"; ma=2592000,h3-29=\":443\"; ma=2592000",    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "status": 200,    "transfer_encoding": "chunked",    "url": "https://www.google.com",    "vary": "Accept-Encoding",    "x_frame_options": "SAMEORIGIN",    "x_xss_protection": "0"}node-1 | SUCCESS => {    "accept_ranges": "none",    "alt_svc": "h3=\":443\"; ma=2592000,h3-29=\":443\"; ma=2592000",    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "status": 200,    "transfer_encoding": "chunked",    "url": "https://www.google.com",    "vary": "Accept-Encoding",    "x_frame_options": "SAMEORIGIN",    "x_xss_protection": "0"}node-2 | SUCCESS => {    "accept_ranges": "none",    "alt_svc": "h3=\":443\"; ma=2592000,h3-29=\":443\"; ma=2592000",    "ansible_facts": {        "discovered_interpreter_python": "/usr/bin/python3"    },    "status": 200,    "transfer_encoding": "chunked",    "url": "https://www.google.com",    "vary": "Accept-Encoding",    "x_frame_options": "SAMEORIGIN",    "x_xss_protection": "0"}[ansible@Ansible-Server ~]$
```

##### Parted Module

"The `parted` module is used to configure block devices, allowing tasks related to disk partitioning and management on managed nodes."
##### sudo hostnamectl set-hostname

```
ansible-doc partedansible-galaxy collection install ansible.posixansible-galaxy collection listansible-galaxy collection install community.generalatach 50 Gb disk with VMansible node-1 -m command -a 'lsblk'ansible node-1 -m parted -a 'device=/dev/sda number=1 part_end=10GiB state=present'ansible node-1 -m command -a 'lsblk'ansible node-1 -m parted -a 'device=/dev/sda number=2 part_start=10GiB part_end=15GiB state=present'ansible node-1 -m command -a 'lsblk' ansible node-1 -m parted -a 'device=/dev/sda number=1 state=absent'ansible node-1 -m command -a 'lsblk'
```

##### Filesystem Module

"The `filesystem` module is used to create filesystems on block devices, allowing the creation and formatting of file systems on managed nodes."

```
ansible node-1 -m command -a 'lsblk -f'ansible node-1 -m filesystem -a 'device=/dev/sda1 fstype=xfs'ansible node-1 -m command -a 'lsblk -f'
```

LVM Module

The `lvm` module in Ansible is used to manage Logical Volume Management (LVM) volumes and volume groups on Linux systems. It allows tasks such as creating, resizing, or removing logical volumes, as well as creating or deleting volume groups. This module provides automation capabilities for handling storage configurations using LVM.

```
ansible node-1 -m lvg -a 'pvs=/dev/sda1 vg=VolGrp state=present'ansible node-1 -m command -a 'vgs'ansible node-1 -m lvg -a 'pvs=/dev/sda1,dev,sda2 vg=VolGrp state=present'ansible node-1 -m command -a 'vgs'Remve vgansible node-1 -m lvg -a 'vg=VolGrp state=absent'ansible node-1 -m command -a 'vgs'ansible node-1 -m lvg -a 'pvs=/dev/sda1,dev,sda2 vg=VolGrp state=present'ansible node-1 -m command -a 'vgs'#LVOLansible node-1 -m lvol -a 'vg=VolGrp lv=LogVol size=4g state=present'ansible node-1 -m command -a 'lvs'Extent the LVMansible node-1 -m lvol -a 'vg=VolGrp lv=LogVol size=+100%FREE status=present'ansible node-1 -m command -a 'lvs'remove lvmansible node-1 -m lvol -a 'vg=VolGrp lv=LogVol status=absent forece=true'ansible node-1 -m command -a 'lvs'ansible node-1 -m command -a 'vgs'
```
