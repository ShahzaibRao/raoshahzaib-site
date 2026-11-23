---
title: "A Complete Journey Through Ansible Core Concepts Part 2: Playbooks, Variables, Vault and Conditionals"
description: "Ansible part 2: write playbooks, work with variables and facts, encrypt secrets with Ansible Vault, and control execution with conditionals, loops and handlers."
slug: "ansible-core-concepts-part-2"
---

By Rao Shahzaib · DevOps

A Complete Journey through Ansible Core Concepts | 2/2

![Ansible Core Concepts Part 2](/images/ansible-core-concepts-part-2/01-installation-1-.png)

**## Ansible Core Concepts **

Ansible is an open-source automation tool that is used for configuration management, application deployment, task automation, and IT orchestration. It is designed to simplify and streamline various IT tasks by automating them, which can help save time, reduce errors, and improve efficiency in managing and maintaining IT infrastructure.

#### Ansible Playbook

"Writing Ansible Playbooks" refers to the process of creating automation scripts using Ansible's Playbook format. Playbooks are written in YAML and contain a series of tasks, modules, and other automation directives. These Playbooks define the desired state of the system and can automate various tasks, configurations, and deployments on managed nodes. Playbook writing involves specifying hosts, tasks, and the desired outcome, allowing for efficient and repeatable automation workflows.

we can perform any automation job by pushing the task in ansible by two methods:

1. Ad-Hoc Commands (command method)

2. Ansible Playbook (File method)

If there is a repetitive or complex task, Ad-Hoc commands are not suitable; Playbooks are used in such cases.

Limitations of Ad-Hoc Commands:

- Manual typing of commands is required for each job.

- Not suitable for conditional statements.

- Cannot handle multi-tasking.

- Variables cannot be used.

Ansible Playbooks:

- No manual typing required.

- Multiple tasks can be automated with a single playbook.

- Conditional statements can be easily implemented.

- Allows performing multiple tasks using a single playbook.

- Variables can be utilized.

A playbook is a file where Ansible tasks are defined. It can be created anywhere in your system; just ensure the file extension is .**yml** or .**yaml **. Playbooks are human-readable files and follow data rules such as string format, array format, and mapping.

##### Lest supposed we have few repetative task which we need to perform on the managed nodes in the RHEL group on daily basis

1. Create a directoy on all machine in /tmp/ directory with trhe name as testdir

2. Copy the /etc/fstab file from the central server to the /tmp/testdir/ directory on the managed nodes

3. Insatall the httpd package

4. Start & Enable the httpd service
##### vi firstplaybook.yaml

--- name: Perform Repetitive Tasks on RHEL Nodes hosts: redhat # Assuming 'rhel' is your host group in the inventory become: true # Run tasks as sudo tasks: - name: Create a directory in /tmp file: path: /tmp/testdir state: directory - name: Copy /etc/fstab to /tmp/testdir/ copy: src: /etc/fstab dest: /tmp/testdir/fstab - name: Install httpd package package: name: httpd state: present - name: Start httpd service service: name: httpd state: started enabled: yes

```
[ansible@Ansible-Server ~]$ ansible-playbook firstplaybook.yaml --syntax-checkplaybook: firstplaybook.yaml[ansible@Ansible-Server ~]$ ansible-playbook firstplaybook.yaml -bPLAY [Perform Repetitive Tasks on RHEL Nodes] **************************************************************************************TASK [Gathering Facts] *************************************************************************************************************ok: [node-1]ok: [node-2]TASK [Create a directory in /tmp] ***************************************************************************changed: [node-2]changed: [node-1]TASK [Copy /etc/fstab to /tmp/testdir/] ***************************************************************************changed: [node-2]changed: [node-1]TASK [Install httpd package] ***************************************************************************changed: [node-1]changed: [node-2]TASK [Start httpd service] ***************************************************************************changed: [node-2]changed: [node-1]PLAY RECAP ***************************************************************************node-1                     : ok=5    changed=4    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0node-2                     : ok=5    changed=4    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0[ansible@Ansible-Server ~]$
```

##### Using Variables in Ansible Playbooks

Variables in Ansible are values that can change based on conditions or information. They are used to store information.

Types of Variables in Ansible:

1. User-Defined Variables: Defined by the user to store custom information.

2. System-Defined Variables: Predefined by Ansible to store system-related information.

Places in Ansible Where Variables Can Be Defined:

1. Playbooks: Variables can be defined within playbooks to store specific information for tasks.

2. Command Line: Variables can be defined via the command line using `-e` or `--extra-vars`.

3. Inventory File: Variables can be defined in the inventory file associated with hosts or groups."

##### vi varibaleplaybook.yml

--- - hosts: redhat tasks: - name: ansible built in varibale debug: msg: "{{ inventory_hostname }}" ... 

```
[ansible@Ansible-Server ~]$ ansible-playbook  varibaleplaybook.yml  --syntax-checkplaybook: varibaleplaybook.yml[ansible@Ansible-Server ~]$ ansible-playbook varibaleplaybook.ymlPLAY [redhat] **********************************************************************************************************************TASK [Gathering Facts] *************************************************************************************************************ok: [node-2]ok: [node-1]TASK [ansible built in varibale] ***************************************************************************************************ok: [node-1] => {    "msg": "node-1"}ok: [node-2] => {    "msg": "node-2"}PLAY RECAP *************************************************************************************************************************node-1                     : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0node-2                     : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0[ansible@Ansible-Server ~]$
```

##### User define variable

--- - name: User-Define Variable hosts: all vars: name: "Rao Shahzaib" tasks: - name: Display the Userdefine Varibale debug: msg: "{{ name }}" ... 

```
[ansible@Ansible-Server ~]$ vi userdefineplaybook.yml[ansible@Ansible-Server ~]$ ansible-playbook  userdefineplaybook.yml  --syntax-checkplaybook: userdefineplaybook.yml[ansible@Ansible-Server ~]$ ansible-playbook userdefineplaybook.yml[WARNING]: Found variable using reserved name: namePLAY [User-Define Variable] ***************************************************************************TASK [Gathering Facts] ***************************************************************************ok: [node-2]ok: [node-1]ok: [node-3]TASK [Display the Userdefine Varibale] ***************************************************************************ok: [node-1] => {    "msg": "Rao Shahzaib"}ok: [node-2] => {    "msg": "Rao Shahzaib"}ok: [node-3] => {    "msg": "Rao Shahzaib"}PLAY RECAP ***************************************************************************node-1                     : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0node-2                     : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0node-3                     : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0[ansible@Ansible-Server ~]$
```

##### Types of Ansible Playbook Variables:
**String Type Variables:**
package: vsftpd

**Array Type Variables:**
var:
 - httpd
 - vsftpd
 - nfs

**Mapping Type Variables:**
users:
 - name: zybi
 pw: <redacted>
 uid: 1058
 - name: ali
 pw: <redacted>
 uid: 1059

##### String Type Variables
"Let's assume we want to configure an Apache server."
--- - name: Configure Apache server using variables hosts: redhat vars: server_name: httpd location: /var/www/html/ tasks: - name: Installing Apache HTTPD Server on Redhat Machines yum: name: "{{ server_name }}" state: installed - name: Starting & Enabling the HTTPD service service: name: "{{ server_name }}" state: started enabled: yes - name: Creating "{{ server_name }}" directory file: path: "{{ location }}" state: directory - name: Creating index.html copy: content: "This is Ansible Lab" dest: "{{ location }}/index.html" ...

```
[ansible@Ansible-Server ~]$ vi stringplaybook.yml[ansible@Ansible-Server ~]$ ansible-playbook stringplaybook.ymlPLAY [Configure Apache server using variables] ***************************************************************************TASK [Gathering Facts] ***************************************************************************ok: [node-2]ok: [node-1]TASK [Installing Apache HTTPD Server on Redhat Machines] ***************************************************************************ok: [node-1]ok: [node-2]TASK [Starting & Enabling the HTTPD service] ***************************************************************************ok: [node-2]ok: [node-1]TASK [Creating "httpd" directory] ***************************************************************************ok: [node-1]ok: [node-2]TASK [Creating index.html] ***************************************************************************changed: [node-1]changed: [node-2]PLAY RECAP ***************************************************************************node-1                     : ok=5    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0node-2                     : ok=5    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0[ansible@Ansible-Server ~]$
```

You can import these variables into another playbook using the vars_files directive:
##### vi vars.yml

apache_server_name: httpd apache_location: /var/www/html/ 

**vi stringplaybook.yml**
--- - name: Configure Apache server using imported variables hosts: redhat vars_files: - vars.yml tasks: - name: Installing Apache HTTPD Server on Redhat Machines yum: name: "{{ apache_server_name }}" state: installed - name: Starting & Enabling the HTTPD service service: name: "{{ apache_server_name }}" state: started enabled: yes - name: Creating "{{ apache_server_name }}" directory file: path: "{{ apache_location }}" state: directory - name: Creating index.html copy: content: "This is Ansible Lab" dest: "{{ apache_location }}/index.html" ...

```
[ansible@Ansible-Server ~]$ vi stringplaybook.yml[ansible@Ansible-Server ~]$ ansible-playbook stringplaybook.yml --syntax-checkplaybook: stringplaybook.yml[ansible@Ansible-Server ~]$ ansible-playbook stringplaybook.ymlPLAY [Configure Apache server using imported variables] ****************************************************************************TASK [Gathering Facts] ***************************************************************************ok: [node-2]ok: [node-1]TASK [Installing Apache HTTPD Server on Redhat Machines] ***************************************************************************ok: [node-1]ok: [node-2]TASK [Starting & Enabling the HTTPD service] ***************************************************************************ok: [node-2]ok: [node-1]TASK [Creating "httpd" directory] ***************************************************************************ok: [node-1]ok: [node-2]TASK [Creating index.html] ***************************************************************************ok: [node-1]ok: [node-2]PLAY RECAP ***************************************************************************node-1                     : ok=5    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0node-2                     : ok=5    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0[ansible@Ansible-Server ~]$
```

##### List / Array type varibales 

--- - name: listing type playbook hosts: redhat become: true vars: required_packages: - ftp - vsftpd - zsh tasks: - name: Installing the Packages yum: name: "{{ required_packages }}" state: installed ...

```
[ansible@Ansible-Server ~]$ vi listarry.yml[ansible@Ansible-Server ~]$ ansible-playbook listarry.yml --syntax-checkplaybook: listarry.yml[ansible@Ansible-Server ~]$ ansible-playbook listarry.ymlPLAY [listing type playbook] ***************************************************************************TASK [Gathering Facts] ***************************************************************************ok: [node-2]ok: [node-1]TASK [Installing the Packages] ***************************************************************************changed: [node-2]changed: [node-1]PLAY RECAP ***************************************************************************node-1                     : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0node-2                     : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0[ansible@Ansible-Server ~]$
```

##### Mapping and directory

--- - name: Mapping hosts: redhat tasks: - name: create new user user: name: '{{ item.name }}' uid: '{{ item.uid }}' state: present loop: - name: hamze uid: 1020 - name: mazz uid: 1030 - name: rabil uid: 1040 ...

```
[ansible@Ansible-Server ~]$ vi mappingdirctory.yml[ansible@Ansible-Server ~]$ ansible-playbook  mappingdirctory.yml --syntax-checkplaybook: mappingdirctory.yml[ansible@Ansible-Server ~]$ ansible-playbook mappingdirctory.ymlPLAY [Mapping] ***************************************************************************TASK [Gathering Facts] ***************************************************************************ok: [node-2]ok: [node-1]TASK [create new user] ***************************************************************************changed: [node-1] => (item={'name': 'hamze', 'uid': 1020})changed: [node-2] => (item={'name': 'hamze', 'uid': 1020})changed: [node-1] => (item={'name': 'mazz', 'uid': 1030})changed: [node-2] => (item={'name': 'mazz', 'uid': 1030})changed: [node-1] => (item={'name': 'rabil', 'uid': 1040})changed: [node-2] => (item={'name': 'rabil', 'uid': 1040})PLAY RECAP ***************************************************************************node-1                     : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0node-2                     : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0[ansible@Ansible-Server ~]$
```

##### Get input from user

In Ansible, you can get input from the user during playbook execution using the `vars_prompt` feature. Here's an example of how you can prompt the user for input
##### vi getinput.yml

--- - name: Get Input From User hosts: all vars_prompt: - name: user_name prompt: "Please enter your name" private: no - name: password prompt: "Enter your password" private: yes tasks: - debug: msg: "The username is {{ user_name }} and password {{ password }}" ...

```
[ansible@Ansible-Server ~]$ vi getinput.yml[ansible@Ansible-Server ~]$ ansible-playbook getinput.yml --syntax-checkplaybook: getinput.yml[ansible@Ansible-Server ~]$ ansible-playbook getinput.ymlPlease enter your name: Rao ShahzaibEnter your password:PLAY [Get Input From User] ***************************************************************************TASK [Gathering Facts] ***************************************************************************ok: [node-2]ok: [node-1]ok: [node-3]TASK [debug] ***************************************************************************ok: [node-1] => {    "msg": "The username is Rao Shahzaib and password [redacted]"}ok: [node-2] => {    "msg": "The username is Rao Shahzaib and password [redacted]"}ok: [node-3] => {    "msg": "The username is Rao Shahzaib and password [redacted]"}PLAY RECAP ***************************************************************************node-1                     : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0node-2                     : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0node-3                     : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0[ansible@Ansible-Server ~]$
```

##### 1. Command Line Variables:

When running a playbook, you can pass variables through the command line. For example:

bash

ansible-playbook your_playbook.yml -e "variable_name=variable_value"

2. **Inventory Variable**s:

Variables can be defined in the inventory file associated with hosts or groups. For example, in your inventory file (`inventory.ini`):

ini

[web_servers]

server1 ansible_host=192.168.1.1 ansible_user=admin

[database_servers]

server2 ansible_host=192.168.1.2 ansible_user=admin

Here, `ansible_host` and `ansible_user` are inventory variables associated with specific hosts.
##### vi commandline.yml

--- - name: Commadn Line Varibales hosts: all become: true tasks: - name: Adding user and password user: name: "{{ user_name }}" state: present password: "{{ password }}" ...

```
[ansible@Ansible-Server ~]$ vi commandline.yml[ansible@Ansible-Server ~]$ ansible-playbook commandline.yml --syntax-checkplaybook: commandline.yml[ansible@Ansible-Server ~]$ ansible-playbook commandline.yml  -e user_name=asad -e password=[redacted]PLAY [Commadn Line Varibales] ***************************************************************************TASK [Gathering Facts] ***************************************************************************ok: [node-1]ok: [node-2]ok: [node-3]TASK [Adding user and password] ***************************************************************************[WARNING]: The input password appears not to have been hashed. The 'password' argument must be encrypted for this module to workproperly.changed: [node-3]changed: [node-1]changed: [node-2]PLAY RECAP ***************************************************************************node-1                     : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0node-2                     : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0node-3                     : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0[ansible@Ansible-Server ~]$ ansible redhat -m command -a 'tail /etc/passwd'node-2 | CHANGED | rc=0 >>mazz:x:1030:1030::/home/mazz:/bin/bashrabil:x:1040:1040::/home/rabil:/bin/bashasad:x:1041:1041::/home/asad:/bin/bash[ansible@Ansible-Server ~]$ ansible redhat -m command -a 'tail -3 /etc/shadow'node-1 | CHANGED | rc=0 >>mazz:!!:19658:0:99999:7:::rabil:!!:19658:0:99999:7:::asad:!:19658:0:99999:7:::node-2 | CHANGED | rc=0 >>mazz:!!:19658:0:99999:7:::rabil:!!:19658:0:99999:7:::asad:!:19658:0:99999:7:::[ansible@Ansible-Server ~]$
```

##### Inventory file varibales
**##### 1. Host Scope Variables:
Variables defined for specific hosts in the inventory file. For example:

**2. Group Scope Variables**
Variables defined for groups of hosts in the inventory file. For example:

```
[ansible@Ansible-Server ~]$ vi /etc/ansible/hosts[redhat]
node-1 dir=/tmp/testdir
node-2 dir=/tmp/testdir[ubuntu]
node-2 dir=/tmp/newdir
```

--- - name: Inventory Variables hosts: all become: true tasks: - name: Creating Directory ansible.builtin.file: path: "{{ dir }}" state: directory - name: Debug Directory Path debug: msg: "{{ dir }}" ...

```
[ansible@Ansible-Server ~]$ vi inventory_variable.yml[ansible@Ansible-Server ~]$ ansible-playbook inventory_variable.yml --syntax-checkplaybook: inventory_variable.yml[ansible@Ansible-Server ~]$ ansible-playbook inventory_variable.ymlPLAY [Inventory Variables] ***************************************************************************TASK [Gathering Facts] ***************************************************************************ok: [node-2]ok: [node-1]ok: [node-3]TASK [Creating Directory] ***************************************************************************changed: [node-3]ok: [node-2]ok: [node-1]TASK [Debug Directory Path] ***************************************************************************ok: [node-1] => {    "msg": "/tmp/testdir"}ok: [node-2] => {    "msg": "/tmp/testdir"}ok: [node-3] => {    "msg": "/tmp/testdir"}PLAY RECAP ***************************************************************************node-1                     : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0node-2                     : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0node-3                     : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0[ansible@Ansible-Server ~]$ ansible all -m command -a 'ls -ld /tmp/testdir'[ansible@Ansible-Server ~]$
```

Let's now use Group Scope variables

```
[ansible@Ansible-Server ~]$ vi /etc/ansible/hosts[redhat]
node-1 node-2[ubuntu]
node-2 [redhat:vars]
dir=/tmp/testdir
```

```
[ansible@Ansible-Server ~]$ sudo vi /etc/ansible/hosts[ansible@Ansible-Server ~]$ ansible-playbook inventory_variable.ymlPLAY [Inventory Variables] ***************************************************************************TASK [Gathering Facts] ***************************************************************************ok: [node-2]ok: [node-1]ok: [node-3]TASK [Creating Directory] ***************************************************************************ok: [node-3]ok: [node-2]ok: [node-1]TASK [Debug Directory Path] ***************************************************************************ok: [node-1] => {    "msg": "/tmp/testdir"}ok: [node-2] => {    "msg": "/tmp/testdir"}ok: [node-3] => {    "msg": "/tmp/testdir"}PLAY RECAP ***************************************************************************node-1                     : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0node-2                     : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0node-3                     : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0[ansible@Ansible-Server ~]$
```

If your inventory file contains multiple groups and you want to set variables for these groups to enhance readability and simplify troubleshooting, you can utilize the /etc/ansible/group_vars/ directory
##### 1. Host-specific Variables:

 To set host-specific variables, you can create a file in the /etc/ansible/host_vars/ directory with the host's name as the file name. For instance, if you want to set variables for the server1 host, you can create a file named server1:

 /etc/ansible/host_vars/server1
##### 2. Group-specific Variables:

 For setting variables specific to groups, you can create a file in the /etc/ansible/group_vars/ directory with the group's name as the file name. For example, if you want to set variables for the web_servers group, you can create a file named web_servers:

 /etc/ansible/group_vars/web_servers

This approach allows you to define variables for each group in separate files, improving readability and making troubleshooting more straightforward.

```
[ansible@Ansible-Server ~]$ sudo mkdir /etc/ansible/host_vars[ansible@Ansible-Server ~]$ sudo mkdir /etc/ansible/group_vars[ansible@Ansible-Server ~]$ sudo vi  /etc/ansible/host_vars[ansible@Ansible-Server ~]$ sudo vi  /etc/ansible/host_vars/node-3[ansible@Ansible-Server ~]$ sudo cat /etc/ansible/host_vars/node-3dir:/tmp/testdir[ansible@Ansible-Server ~]$ sudo vi  /etc/ansible/group_vars/redhat[ansible@Ansible-Server ~]$ sudo cat  /etc/ansible/group_vars/redhatdir:/tmp/newdir[ansible@Ansible-Server ~]$
```

```
[ansible@Ansible-Server ~]$ ansible-playbook inventory_variable.ymlPLAY [Inventory Variables] ***************************************************************************TASK [Gathering Facts] ***************************************************************************ok: [node-2]ok: [node-1]ok: [node-3]TASK [Creating Directory] ***************************************************************************ok: [node-3]ok: [node-2]ok: [node-1]TASK [Debug Directory Path] ***************************************************************************ok: [node-1] => {    "msg": "/tmp/testdir"}ok: [node-2] => {    "msg": "/tmp/testdir"}ok: [node-3] => {    "msg": "/tmp/testdir"}PLAY RECAP ***************************************************************************node-1                     : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0node-2                     : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0node-3                     : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0[ansible@Ansible-Server ~]$[ansible@Ansible-Server ~]$ ansible redhat -m command -a 'ls -ld /tmp/testdir' node-2 | CHANGED | rc=0 >>
drwxr-xr-x. 2 root root 19 Oct 28 05:29 /tmp/testdir node-1 | CHANGED | rc=0 >>
drwxr-xr-x. 2 root root 19 Oct 28 05:29 /tmp/testdir[ansible@Ansible-Server ~]$
```

##### Ansible Facts

 Ansible Facts are system properties collected by Ansible when it interacts with remote systems. When Ansible runs a playbook or performs tasks on a remote system, it collects system information such as IP addresses, MAC addresses, hostname, storage details, and more. These properties are stored as variables and are referred to as Ansible Facts.
**1. Custom Facts in Ansible:**
 Ansible allows you to gather custom facts beyond the default system properties. Custom Facts are user-defined variables that can be collected from managed nodes. These facts can be specific to your organization's needs and can provide additional context for your playbooks.

**##### 3. Magic Variables:**
 In Ansible, there are special variables called "magic variables" that provide information about the system or the current playbook execution. For example, `{{ inventory_hostname }}` represents the hostname of the current managed node, and `{{ ansible_distribution }}` represents the Linux distribution running on the managed node. These magic variables are essential for dynamic playbook execution and conditional task execution based on system properties.
When you work with remote systems using Ansible, the collection and utilization of Ansible Facts enable you to automate tasks based on the specific properties of each managed node.

When you perform any task on a remote system using Ansible, such as running a playbook, Ansible collects system properties during the process. These properties, like IP addresses, MAC addresses, hostname, storage details, and more, are gathered and stored as variables. This collection process is known as Ansible Facts. In essence, Ansible Facts refer to the system properties of managed nodes that are collected, stored, and utilized for automation tasks.

```
[ansible@Ansible-Server ~]$ ansible all -m setup[ansible@Ansible-Server ~]$ ansible all -m setup -a 'filter=ansible_hostname'node-2 | SUCCESS => {    "ansible_facts": {        "ansible_hostname": "node-2",        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": false}node-1 | SUCCESS => {    "ansible_facts": {        "ansible_hostname": "node-1",        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": false}node-3 | SUCCESS => {    "ansible_facts": {        "ansible_hostname": "node-3",        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": false}[ansible@Ansible-Server ~]$
```

**lets create a playbook for checking the kernel version**

--- - name: Ansible Facts hosts: all become: true tasks: - name: Capture the kernel version ansible.builtin.copy: content: "The available kernel is {{ ansible_kernel }}" dest: /tmp/kernel_version.txt ...

```
[ansible@Ansible-Server ~]$ ansible-playbook kernernelversion.yaml --syntax-checkplaybook: kernernelversion.yaml[ansible@Ansible-Server ~]$ ansible-playbook kernernelversion.yamlPLAY [Ansible Facts] ***************************************************************************************************************TASK [Gathering Facts] *************************************************************************************************************ok: [node-2]ok: [node-1]ok: [node-3]TASK [Capture the kernel version] **************************************************************************************************changed: [node-3]changed: [node-2]changed: [node-1]PLAY RECAP *************************************************************************************************************************node-1                     : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0node-2                     : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0node-3                     : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0[ansible@Ansible-Server ~]$ ansible all -m command -a 'cat /tmp/kernel_version.txt'node-3 | CHANGED | rc=0 >>The available kernel is 6.2.0-1014-awsnode-2 | CHANGED | rc=0 >>The available kernel is 5.14.0-284.30.1.el9_2.x86_64node-1 | CHANGED | rc=0 >>The available kernel is 5.14.0-284.30.1.el9_2.x86_64[ansible@Ansible-Server ~]$
```

Let's assume you want to add an entry for a host named webserver with the IP address 192.168.1.10 to the /etc/hosts file on multiple remote servers.

--- - name: IP and HOSTNAME entry in host file of remote system hosts: all become: true tasks: - name: Append the IP address and hostname information lineinfile: line: "{{ ansible_default_ipv4.address }} {{ ansible_fqdn }}" dest: /etc/hosts ...

```
[ansible@Ansible-Server ~]$ vi ipaddresshots.yml[ansible@Ansible-Server ~]$ ansible-playbook ipaddresshots.yml --syntax-checkplaybook: ipaddresshots.yml[ansible@Ansible-Server ~]$ ansible-playbook ipaddresshots.ymlPLAY [IP and HOSTNAME entry in host file of remote system] *************************************************************************TASK [Gathering Facts] *************************************************************************************************************ok: [node-1]ok: [node-2]ok: [node-3]TASK [Append the IP address and hostname information] ******************************************************************************changed: [node-3]changed: [node-2]changed: [node-1]PLAY RECAP *************************************************************************************************************************node-1                     : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0node-2                     : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0node-3                     : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0[ansible@Ansible-Server ~]$[ansible@Ansible-Server ~]$ ansible all -m command -a 'cat /etc/hosts'node-3 | CHANGED | rc=0 >>127.0.0.1 localhost
172.31.0.10 Ansible-Server
172.31.0.11 node-1
172.31.0.12 node-2
172.31.0.13 node-3

# The following lines are desirable for IPv6 capable hosts::1 ip6-localhost ip6-loopbackfe00::0 ip6-localnetff00::0 ip6-mcastprefixff02::1 ip6-allnodesff02::2 ip6-allroutersff02::3 ip6-allhosts192.168.1.10 webserver172.31.32.20 node-3node-2 | CHANGED | rc=0 >>172.31.0.10 Ansible-Server
172.31.0.11 node-1
172.31.0.12 node-2
172.31.0.13 node-3
127.0.0.1 localhost localhost.localdomain localhost4 localhost4.localdomain4::1 localhost localhost.localdomain localhost6 localhost6.localdomain6192.168.1.10 webserver172.31.37.148 node-2node-1 | CHANGED | rc=0 >>127.0.0.1 localhost localhost.localdomain localhost4 localhost4.localdomain4::1 localhost localhost.localdomain localhost6 localhost6.localdomain6192.168.1.10 webserver172.31.2.162 node-1[ansible@Ansible-Server ~]$
```

If our environment is very large, gathering facts can take a lot of time. If we don't use facts in our tasks, in that case, we set facts gathering to false. Doing this significantly speeds up our playbook execution.

--- - name: IP or Hostname Entry in Hosts File hosts: all become: true gather_facts: false tasks: - name: Append the IP address and hostname information lineinfile: line: "{{ ansible_default_ipv4.address }} {{ ansible_fqdn }}" dest: /etc/hosts ...

##### Custom Facts

"If the information you need is not available on the managed nodes, you may want to create it manually there.
Let's say we need to fetch additional information from node-1."

Go to node-1 sudo mkdir -p /etc/ansible/facts.d/ vi /etc/ansible/facts.d/httpd.fact [basic] package=httpd service=httpd state=started enabled=true

```
[ansible@Ansible-Server ~]$ ansible all  -m setup -a 'filter=ansible_local'node-2 | SUCCESS => {    "ansible_facts": {        "ansible_local": {},        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": false}node-1 | SUCCESS => {    "ansible_facts": {        "ansible_local": {            "httpd": {                "basic": {                    "enabled": "true",                    "package": "httpd",                    "service": "httpd",                    "state": "started"                }            }        },        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": false}node-3 | SUCCESS => {    "ansible_facts": {        "ansible_local": {},        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": false}[ansible@Ansible-Server ~]$ ansible node-3 -m setup -a 'filter=ansible_local'node-3 | SUCCESS => {    "ansible_facts": {        "ansible_local": {},        "discovered_interpreter_python": "/usr/bin/python3"    },    "changed": false}[ansible@Ansible-Server ~]$
```

SSH node-3 instance 

--- - name: Install httpd hosts: node-1 become: true tasks: - name: Install HTTPD yum: name: "{{ ansible_facts.ansible_local.httpd.basic.package }}" state: latest - name: Start and enable httpd service: name: "{{ ansible_facts.ansible_local.httpd.basic.service }}" state: "{{ ansible_facts.ansible_local.httpd.basic.state }}" enabled: "{{ ansible_facts.ansible_local.httpd.basic.enabled }}" ...

```
[ansible@Ansible-Server ~]$ ansible-playbook installapachewithlocalfacts.ymlPLAY [Install httpd] ***************************************************************************************************************TASK [Gathering Facts] *************************************************************************************************************ok: [node-1]TASK [Install HTTPD] ***************************************************************************************************************ok: [node-1]TASK [Start and enable httpd] ******************************************************************************************************ok: [node-1]PLAY RECAP *************************************************************************************************************************node-1                     : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0[ansible@Ansible-Server ~]$
```

**ansible node-1 -m command -a 'systemctl status httpd'**

```
[ansible@Ansible-Server ~]$ ansible node-1 -m command -a 'systemctl status httpd'node-1 | CHANGED | rc=0 >>● httpd.service - The Apache HTTP Server     Loaded: loaded (/usr/lib/systemd/system/httpd.service; enabled; preset: disabled)     Active: active (running) since Sat 2023-10-28 11:58:41 UTC; 1h 9min ago       Docs: man:httpd.service(8)   Main PID: 628 (httpd)     Status: "Total requests: 4; Idle/Busy workers 100/0;Requests/sec: 0.000959; Bytes served/sec:   0 B/sec"      Tasks: 213 (limit: 4269)     Memory: 40.6M        CPU: 1.971s     CGroup: /system.slice/httpd.service             ├─628 /usr/sbin/httpd -DFOREGROUND             ├─650 /usr/sbin/httpd -DFOREGROUND             ├─652 /usr/sbin/httpd -DFOREGROUND             ├─654 /usr/sbin/httpd -DFOREGROUND             └─655 /usr/sbin/httpd -DFOREGROUNDOct 28 11:58:41 node-1 systemd[1]: Starting The Apache HTTP Server...Oct 28 11:58:41 node-1 httpd[628]: AH00558: httpd: Could not reliably determine the server's fully qualified domain name, using ::1. Set the 'ServerName' directive globally to suppress this messageOct 28 11:58:41 node-1 systemd[1]: Started The Apache HTTP Server.Oct 28 11:58:41 node-1 httpd[628]: Server configured, listening on: port 80[ansible@Ansible-Server ~]$
```

##### Magic Variables

Magic variables are built-in variables in Ansible that provide dynamic information during playbook execution. Some commonly used magic variables include:
- **hostvars**: Provides variables for a specific host, including facts and user-defined variables.

- **groups**: Contains information about all defined groups in the inventory file.
- **group_names**: Lists the names of all groups the current host is a member of.
- **inventory_hostname**: Represents the name of the current host as known by Ansible.
These magic variables are essential for dynamic playbook execution and conditional task execution based on the system's properties and group memberships.

vi magicfacts.yml

--- - name: Gather Facts hosts: node-1 tasks: - name: Gather all facts for {{ inventory_hostname }} debug: var: ansible_facts ... 

```
[ansible@Ansible-Server ~]$ vi magicfacts.yml[ansible@Ansible-Server ~]$ ansible-playbook magicfacts.yml --syntax-checkplaybook: magicfacts.yml[ansible@Ansible-Server ~]$ ansible-playbook magicfacts.ymlPLAY [Gather Facts] ****************************************************************************************************************TASK [Gathering Facts] *************************************************************************************************************ok: [node-1]TASK [Gather all facts for node-1] *************************************************************************************************ok: [node-1] => {    "ansible_facts": {        "all_ipv4_addresses": [            "172.31.2.162"        ],        "all_ipv6_addresses": [            "fe80::818:88ff:fe82:733c"        ],        "ansible_local": {            "httpd": {                "basic": {                    "enabled": "true",                    "package": "httpd",                    "service": "httpd",                    "state": "started"                }            }        },            "xen"        ],        "virtualization_tech_host": [],        "virtualization_type": "xen"    }}PLAY RECAP *************************************************************************************************************************node-1                     : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0[ansible@Ansible-Server ~]$
```

##### Registering Ansible Variables

How you can register variables, up until now, the variables we were using were predefined. Many times, we may need to register variables, and in today's session, we will see how to do that.
Imagine you have run a playbook or a task on a remote machine, and the output you received contains certain values that you want to use in further tasks. To accomplish this, we use registered variables.

vi registervaribale.yml

--- - name: Register the Variable in ansible hosts: all tasks: - name: Check the machine hostname command: hostname register: output - debug: var: output.stdout ...

```
[ansible@Ansible-Server ~]$ vi registervaribale.yml[ansible@Ansible-Server ~]$ ansible-playbook registervaribale.yml --syntax-checkplaybook: registervaribale.yml[ansible@Ansible-Server ~]$ ansible-playbook registervaribale.ymlPLAY [Register the Variable in  ansible] *******************************************************************************************TASK [Gathering Facts] *************************************************************************************************************ok: [node-2]ok: [node-1]ok: [node-3]TASK [Check the machine hostname] **************************************************************************************************changed: [node-3]changed: [node-1]changed: [node-2]TASK [debug] ***********************************************************************************************************************ok: [node-1] => {    "output.stdout": "node-1"}ok: [node-2] => {    "output.stdout": "node-2"}ok: [node-3] => {    "output.stdout": "node-3"}PLAY RECAP *************************************************************************************************************************node-1                     : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0node-2                     : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0node-3                     : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0[ansible@Ansible-Server ~]$
```

##### Secure Playbooks Using Ansible Vault

now, we will explore how to protect sensitive information using Ansible Vault. Ansible Vault is a feature that allows you to safely encrypt sensitive data, such as keys or passwords.
With Ansible Vault, you can perform tasks like adding users and setting passwords securely. Let's write a playbook to add a user and set a password using Ansible Vault.

vi adduservault.yml

--- - name: ansible vault playbook hosts: all become: true vars: pw: "<redacted>" tasks: - name: creat user account and setting the password user: name: haris password: "{{ pw }}" ...

"If this file is placed in a location where the user has read access, they can read the file's content by using the `cat` command:

"We want to prevent anyone from reading this playbook; we aim to enhance its security."

```
[ansible@Ansible-Server ~]$ ansible-vault encrypt adduservault.ymlNew Vault password:Confirm New Vault password:Encryption successful[ansible@Ansible-Server ~]$ cat adduservault.yml$ANSIBLE_VAULT;1.1;AES256393232353762616434623931663665643536313161353561353831383339636535626132656335636637306437646438313432333831623337633364353238320a376333633334343132333231303839626134323635376136626438353362633933383136313162303730646166663566333361356431373234383463316438340a37666562613130656131393936646534396138303137356638613763303535643863366663343436373332643335663738626134653863396336616230633939383065373561386163616330393433616131366462613566303735376237353230353563306362353762393833643361326234643963366335383836343664623262626634333638663530326439643638306365313037366161613134663334303334666536643931303237363963323034653362386139383963396330323532316534313335626364643061363762623230303863623462653238373165616631336338653431643439623732336561343965616632666534396339363566323162323963656635373334616166346333313766343135656364653731323061616532623133363366613235383166313233396365333331633936643136346436643461393633306136666133346363626166393865626631316234336132313961343561356332373165303034376338336635366434356662656461303766623831633832303266393338616239383930383338333436656130393330656433366531663964383065393239306237333766353666316634333731326364[ansible@Ansible-Server ~]$
```

"AES 256 encryption method is utilized for encryption. This is a highly significant encryption technique."

if we want to see file content.

```
[ansible@Ansible-Server ~]$ ansible-vault view adduservault.ymlVault password:---- name: ansible vault playbook  hosts: all  become: true  vars:    pw: "<redacted>"  tasks:   - name: creat user account and setting the password     user:       name: haris       password: "{{ pw }}"...[ansible@Ansible-Server ~]$
```

```
[ansible@Ansible-Server ~]$ ansible-vault edit adduservault.ymlVault password:[ansible@Ansible-Server ~]$ ansible-playbook adduservault.yml  --ask-vault-passVault password:PLAY [ansible vault playbook] ******************************************************************************************************TASK [Gathering Facts] *************************************************************************************************************ok: [node-1]ok: [node-3]ok: [node-2]TASK [creat user account and setting the password] *********************************************************************************[WARNING]: The input password appears not to have been hashed. The 'password' argument must be encrypted for this module to workproperly.changed: [node-3]changed: [node-1]changed: [node-2]PLAY RECAP *************************************************************************************************************************node-1                     : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0node-2                     : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0node-3                     : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0[ansible@Ansible-Server ~]$
```

##### "If you want to decrypt this file,..."

```
[ansible@Ansible-Server ~]$ ansible-vault decrypt adduservault.ymlVault password:Decryption successful[ansible@Ansible-Server ~]$
```

"If we only want to encrypt specific sensitive data within a file rather than the entire file, we need to grant read access to the user for the file. The sensitive information inside the file needs to be encrypted. In this case, we can import that data from another file into our desired file."
##### vi vaultefile.yml

--- - name: Ansible Vault Playbook hosts: all become: true vars_files: - /home/ansible/crypt.yml tasks: - name: create user account and setting the password user: name: saud password: "{{ pass }}" ... 

"Now, let's create it and apply encryption simultaneously."

```
[ansible@Ansible-Server ~]$ ansible-vault create /home/ansible/crypt.ymlNew Vault password:Confirm New Vault password:[ansible@Ansible-Server ~]$ ansible-playbook vaultefile.yml --syntax-checkERROR! Attempting to decrypt but no vault secrets found[ansible@Ansible-Server ~]$ ansible-playbook vaultefile.yml  --ask-vault-passVault password:PLAY [Ansible Vault Playbook] ******************************************************************************************************TASK [Gathering Facts] *************************************************************************************************************ok: [node-2]ok: [node-1]ok: [node-3]TASK [create user account and setting the password] ********************************************************************************[WARNING]: The input password appears not to have been hashed. The 'password' argument must be encrypted for this module to workproperly.changed: [node-3]changed: [node-1]changed: [node-2]PLAY RECAP *************************************************************************************************************************node-1                     : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0node-2                     : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0node-3                     : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0[ansible@Ansible-Server ~]$
```

##### Using Loops in Ansible

"Ansible loops are essential for repetitive tasks, allowing us to perform repeated actions efficiently. Similar to other programming languages, loops in Ansible enable us to iterate over a set of items. 
Loops help us reduce the size of our playbooks, making the code clean and easy to understand. Additionally, smaller code execution tends to be faster."

Types of Loops:
**##### 1. Simple/Standard Loop**
##### 2. Hash/Mapping Loops
##### 3. Nested Loops
##### vi useraddloop.yml

--- - name: User Account Creation Playbook hosts: all become: true tasks: - name: Adding user accounts user: name: "{{ item }}" state: present with_items: - sarmad - waleed - qanzal - sameer ...

```
[ansible@Ansible-Server ~]$ vi useraddloop.yml[ansible@Ansible-Server ~]$ ansible-playbook useraddloop.yml --syntax-checkplaybook: useraddloop.yml[ansible@Ansible-Server ~]$ ansible-playbook useraddloop.ymlPLAY [User Account Creation Playbook] **********************************************************************************************TASK [Gathering Facts] *************************************************************************************************************ok: [node-2]ok: [node-1]ok: [node-3]TASK [Adding user accounts] ********************************************************************************************************changed: [node-3] => (item=sarmad)changed: [node-1] => (item=sarmad)changed: [node-2] => (item=sarmad)changed: [node-3] => (item=waleed)changed: [node-1] => (item=waleed)changed: [node-2] => (item=waleed)changed: [node-3] => (item=qanzal)changed: [node-3] => (item=sameer)changed: [node-2] => (item=qanzal)changed: [node-1] => (item=qanzal)changed: [node-2] => (item=sameer)changed: [node-1] => (item=sameer)PLAY RECAP *************************************************************************************************************************node-1                     : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0node-2                     : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0node-3                     : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0[ansible@Ansible-Server ~]$ ansible all -m command -a 'tail -5 /etc/passwd'node-3 | CHANGED | rc=0 >>saud:x:1004:1004::/home/saud:/bin/shsarmad:x:1005:1005::/home/sarmad:/bin/shwaleed:x:1006:1006::/home/waleed:/bin/shqanzal:x:1007:1007::/home/qanzal:/bin/shsameer:x:1008:1008::/home/sameer:/bin/shnode-2 | CHANGED | rc=0 >>saud:x:1043:1043::/home/saud:/bin/bashsarmad:x:1044:1044::/home/sarmad:/bin/bashwaleed:x:1045:1045::/home/waleed:/bin/bashqanzal:x:1046:1046::/home/qanzal:/bin/bashsameer:x:1047:1047::/home/sameer:/bin/bashnode-1 | CHANGED | rc=0 >>saud:x:1043:1043::/home/saud:/bin/bashsarmad:x:1044:1044::/home/sarmad:/bin/bashwaleed:x:1045:1045::/home/waleed:/bin/bashqanzal:x:1046:1046::/home/qanzal:/bin/bashsameer:x:1047:1047::/home/sameer:/bin/bash[ansible@Ansible-Server ~]$
```

For performing any repetitive task, loops are used in Ansible.

Ansible utilizes specific keywords:

**- 'loop'**

**- 'with_<lookup term>'**

**- 'until'**
##### vi useraddwithloop.yml

##### --- - name: User Account Creation Playbook hosts: all become: true tasks: - name: Adding user accounts user: name: "{{ item }}" state: present with_items: - sarmad - waleed - qanzal - sameer ...

##### vi useradduntilloop.yml

--- - name: simple loop host: all become: true tasks: - name: Adding user accounts user: name: "{{ item }}" state: present group: wheel loop: - ali - mazz - hamza - asad - saud ...

"Looping over a list of hashes, this data structure operates as key-value pairs."

NAME GROUP asad raiz wheel saud rao wheel nadeem jutt root muzamil ch root

--- - name: Playbook to add multiple users and groups using hash loop hosts: node-1 become: true tasks: - name: Adding groups group: name: "{{ item }}" state: present loop: - daraz - olx - name: Adding local user account user: name: "{{ item.usr }}" state: present groups: "{{ item.grp }}" loop: - { usr: huzaifa, grp: daraz } - { usr: usama, grp: olx } - { usr: masood, grp: daraz } - { usr: hanzala, grp: olx } ...

```
[ansible@Ansible-Server ~]$ vi  adduserhashloop.yml[ansible@Ansible-Server ~]$ ansible-playbook adduserhashloop.yml --syntax-checkplaybook: adduserhashloop.yml[ansible@Ansible-Server ~]$ ansible-playbook adduserhashloop.ymlPLAY [Playbook to add multiple users and groups using hash loop] *******************************************************************TASK [Gathering Facts] *************************************************************************************************************ok: [node-1]TASK [Adding groups] ***************************************************************************************************************changed: [node-1] => (item=daraz)changed: [node-1] => (item=olx)TASK [Adding local user account] ***************************************************************************************************changed: [node-1] => (item={'usr': 'huzaifa', 'grp': 'daraz'})changed: [node-1] => (item={'usr': 'usama', 'grp': 'olx'})changed: [node-1] => (item={'usr': 'masood', 'grp': 'daraz'})changed: [node-1] => (item={'usr': 'hanzala', 'grp': 'olx'})PLAY RECAP *************************************************************************************************************************node-1                     : ok=3    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0[ansible@Ansible-Server ~]$
```

NAME GROUP
asad daraz,olx,elo
saud daraz,olx,elo
nadeem daraz,olx,elx
muzamil daraz,olx,elo

"We cannot achieve this task using a single loop; for this, we need to use a nested loop."

- name: Adding user to multiple groups hosts: node-1 become: true tasks: - name: Adding groups group: name: "{{ item }}" state: present with_items: - daraz - olx - elo - name: Adding local user accounts user: name: "{{ item.0 }}" groups: "{{ item.1 }}" append: yes with_nested: - [asad, saud, ali, zia] - [daraz, olx, elo] 

```
[ansible@Ansible-Server ~]$ vi useraddnestedloop.yml[ansible@Ansible-Server ~]$ ansible-playbook useraddnestedloop.yml --syntax-checkplaybook: useraddnestedloop.yml[ansible@Ansible-Server ~]$ ansible-playbook useraddnestedloop.ymlPLAY [Adding user to multiple groups] **********************************************************************************************TASK [Gathering Facts] *************************************************************************************************************ok: [node-1]TASK [Adding groups] ***************************************************************************************************************ok: [node-1] => (item=daraz)ok: [node-1] => (item=olx)changed: [node-1] => (item=elo)TASK [Adding local user accounts] **************************************************************************************************changed: [node-1] => (item=['asad', 'daraz'])changed: [node-1] => (item=['asad', 'olx'])changed: [node-1] => (item=['asad', 'elo'])changed: [node-1] => (item=['saud', 'daraz'])changed: [node-1] => (item=['saud', 'olx'])changed: [node-1] => (item=['saud', 'elo'])changed: [node-1] => (item=['ali', 'daraz'])changed: [node-1] => (item=['ali', 'olx'])changed: [node-1] => (item=['ali', 'elo'])changed: [node-1] => (item=['zia', 'daraz'])changed: [node-1] => (item=['zia', 'olx'])changed: [node-1] => (item=['zia', 'elo'])PLAY RECAP *************************************************************************************************************************node-1                     : ok=3    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0[ansible@Ansible-Server ~]$
```

##### Ansible Conditional Tasks

Today, we will discuss conditional tasks in Ansible. Often, we need to match a condition before executing a task. For this, we use the "WHEN" keyword.
Syntax:
**when: statement operator value
Example:
**when: ansible_os_family == 'RedHat'**

The statement's value is retrieved from variables, which can be:
1. Custom variables like command line variables
2. Setup variables
3. Registered variables
Operators:
**- `==` (equals)
- `!=` (not equals)
- `>=` (greater than or equal to)
- `<=` (less than or equal to)
- `>` (greater than)
- `<` (less than)**
Logical Operators:
**- `AND` (both values must be true)
- `OR` (any of them must be true)**

"Now, we will check the operating system flavor and install the Apache web server on the nodes."

--- - name: Check OS and install Apache hosts: all become: true tasks: - name: Install the web server on RedHat based Machine yum: name: httpd state: installed when: ansible_distribution == 'RedHat' - name: Install the web server on Ubuntu based machine apt: name: apache2 state: installed when: ansible_distribution == 'Ubuntu' ... 

```
[ansible@Ansible-Server ~]$ ansible-playbook conditioninstallapache.ymlPLAY [Check OS and install Apache] *************************************************************************************************TASK [Gathering Facts] *************************************************************************************************************ok: [node-2]ok: [node-1]ok: [node-3]TASK [Install the web server on RedHat based Machine] ******************************************************************************skipping: [node-3]ok: [node-1]ok: [node-2]TASK [Install the web server on Ubuntu based machine] ******************************************************************************skipping: [node-1]skipping: [node-2]fatal: [node-3]: FAILED! => {"changed": false, "msg": "value of state must be one of: absent, build-dep, fixed, latest, present, got: installed"}PLAY RECAP *************************************************************************************************************************node-1                     : ok=2    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0node-2                     : ok=2    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0node-3                     : ok=1    changed=0    unreachable=0    failed=1    skipped=1    rescued=0    ignored=0[ansible@Ansible-Server ~]$
```

--- - name: check the OS and install Apache hosts: all become: true tasks: - name: install the web server on Redhat based machine where version is 7 yum: name: httpd state: installed when: - ansible_distribution == 'RedHat' - ansible_distribution_major_version == '7' ... 

```
[ansible@Ansible-Server ~]$ vi condiandplay.yml[ansible@Ansible-Server ~]$ ansible-playbook condiandplay.yml --syntax-checkplaybook: condiandplay.yml[ansible@Ansible-Server ~]$ ansible-playbook condiandplay.ymlPLAY [check the OS and install Apache] *********************************************************************************************TASK [Gathering Facts] *************************************************************************************************************ok: [node-1]ok: [node-2]ok: [node-3]TASK [install the web server on Redhat based machine where version is 7] ***********************************************************skipping: [node-3]ok: [node-1]ok: [node-2]PLAY RECAP *************************************************************************************************************************node-1                     : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0node-2                     : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0node-3                     : ok=1    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0[ansible@Ansible-Server ~]$
```

 Install zsh package if machine has 2GB RAM or Greater then 

--- - name: Check the OS and install zsh package hosts: all become: true tasks: - name: Install zsh package if available RAM is more than 2GB yum: name: zsh state: installed when: ansible_memtotal_mb > 2048 ...

```
[ansible@Ansible-Server ~]$ vi condigreter.yml[ansible@Ansible-Server ~]$ ansible-playbook condigreter.yml --syntax-checkplaybook: condigreter.yml[ansible@Ansible-Server ~]$ ansible-playbook condigreter.ymlPLAY [Check the OS and install zsh package] ****************************************************************************************TASK [Gathering Facts] *************************************************************************************************************ok: [node-2]ok: [node-1]ok: [node-3]TASK [Install zsh package if available RAM is more than 2GB] ***********************************************************************skipping: [node-1]skipping: [node-2]skipping: [node-3]PLAY RECAP *************************************************************************************************************************node-1                     : ok=1    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0node-2                     : ok=1    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0node-3                     : ok=1    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0[ansible@Ansible-Server ~]$
```

##### Ansible Notify & Handlers

Now, we will explore Ansible Notify and Handlers, understanding what Notify is and how Handlers are utilized.
Imagine we have a playbook where we need to run multiple tasks. Let's say we want to monitor our configuration file, and if there are any changes inside it, we want to restart the httpd service. The service should only restart if there are changes inside the configuration file. Here, our second task depends on the first one.
For such tasks, we can use Notify and Handlers. Handlers are tasks that get triggered only when a Notifier reports a change. Instead of using 'when' statements in our playbook, which could make our code complex, we can use Notify and Handlers for cleaner and more efficient code.
The Notifier keyword is used within a task block, indicating which task will report changes. Handlers, on the other hand, are defined separately and can be called by the Notifier task.
Handlers should have unique names, and they always run in the order they are defined. They run only if the state of the task calling them has changed, ensuring efficiency and preventing unnecessary executions.
##### vi notifyhandler.yml

--- - name: Check the OS and install zsh package hosts: all become: true tasks: - name: Install zsh package if available RAM is more than 2GB yum: name: zsh state: installed when: ansible_memtotal_mb > 2048 ...

```
[ansible@Ansible-Server ~]$ vi notifyhandler.yml[ansible@Ansible-Server ~]$ ansible-playbook notifyhandler.yml --syntax-checkplaybook: notifyhandler.yml[ansible@Ansible-Server ~]$ ansible-playbook notifyhandler.ymlPLAY [Install Apache on RHEL server] ***********************************************************************************************TASK [Gathering Facts] *************************************************************************************************************ok: [node-2]ok: [node-1]TASK [Install the latest Apache] ***************************************************************************************************ok: [node-2]ok: [node-1]PLAY RECAP *************************************************************************************************************************node-1                     : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0node-2                     : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0[ansible@Ansible-Server ~]$
```

multiple task and multiple hadler

**1 . Regural task**

 installing the latest version apache

 configuration apache

**2. Handlers**

 Starting Apache service

 configuring the firewall to allow the incoming http traffic
##### vi multitaskhandler.yml

--- - name: Multitask handler hosts: all tasks: - name: Install httpd dnf: name: httpd state: latest - name: Configure Apache copy: content: "Absible lab" dest: /var/www/html/index.html owner: apache group: apache mode: '0644' notify: - Configure Firewall - Start Apache handlers: - name: Start Apache service: name: httpd state: started - name: Configure Firewall firewalld: service: http state: enabled permanent: yes immediate: yes ...

```
[ansible@Ansible-Server ~]$ vi multitaskhandler.yml[ansible@Ansible-Server ~]$ ansible-playbook multitaskhandler.yml --syntax-checkplaybook: multitaskhandler.yml[ansible@Ansible-Server ~]$ ansible-playbook multitaskhandler.ymlPLAY [Multitask handler] ***********************************************************************************************************TASK [Gathering Facts] *************************************************************************************************************ok: [node-2]ok: [node-1]ok: [node-3]TASK [Install httpd] ***************************************************************************************************************fatal: [node-3]: FAILED! => {"changed": false, "msg": "Could not import the dnf python module using /usr/bin/python3 (3.10.12 (main, Jun 11 2023, 05:26:28) [GCC 11.4.0]). Please install `python3-dnf` or `python2-dnf` package or ensure you have specified the correct ansible_python_interpreter. (attempted ['/usr/libexec/platform-python', '/usr/bin/python3', '/usr/bin/python2', '/usr/bin/python'])", "results": []}ok: [node-1]ok: [node-2]TASK [Configure Apache] ************************************************************************************************************changed: [node-2]changed: [node-1]RUNNING HANDLER [Start Apache] *****************************************************************************************************ok: [node-2]ok: [node-1]RUNNING HANDLER [Configure Firewall] ***********************************************************************************************fatal: [node-2]: FAILED! => {"changed": false, "msg": "Failed to import the required Python library (firewall) on node-2's Python /usr/bin/python3. Please read the module documentation and install it in the appropriate location. If the required library is installed, but Ansible is using the wrong Python interpreter, please consult the documentation on ansible_python_interpreter. Version 0.2.11 or newer required (0.3.9 or newer for offline operations)"}fatal: [node-1]: FAILED! => {"changed": false, "msg": "Failed to import the required Python library (firewall) on node-1's Python /usr/bin/python3. Please read the module documentation and install it in the appropriate location. If the required library is installed, but Ansible is using the wrong Python interpreter, please consult the documentation on ansible_python_interpreter. Version 0.2.11 or newer required (0.3.9 or newer for offline operations)"}PLAY RECAP *************************************************************************************************************************node-1                     : ok=4    changed=1    unreachable=0    failed=1    skipped=0    rescued=0    ignored=0node-2                     : ok=4    changed=1    unreachable=0    failed=1    skipped=0    rescued=0    ignored=0node-3                     : ok=1    changed=0    unreachable=0    failed=1    skipped=0    rescued=0    ignored=0[ansible@Ansible-Server ~]$
```

##### Task Error Handling in Ansible
##### vi multitaskhandler.yml

--- - name: Task Error Handling in Ansible hosts: rhel tasks: - name: Install httpd package yum: name: httpd state: present ignore_errors: yes - name: Start httpd service service: name: httpd state: started rescue: - name: Notify administrators about the failure mail: to: admin@example.com subject: "httpd service failed to start on {{ inventory_hostname }}" body: "Please check and resolve the issue.
