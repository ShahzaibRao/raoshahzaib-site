---
title: "Configuring Jenkins Master-Slave Architecture for Scalable CI/CD Pipelines"
description: "Set up Jenkins master-slave architecture for scalable CI/CD: add a permanent agent over SSH, configure labels and launch method, and scale builds across nodes."
slug: "jenkins-master-slave-architecture"
---

By Rao Shahzaib · DevOps

Configuring Jenkins Master-Slave Architecture for Scalable CI/CD Pipelines

![Jenkins master-slave architecture installation overview](/images/jenkins-master-slave-architecture/01-installation.png)

**### Enhancing Scalability and Efficiency**

**Jenkins Master-Slave Configuration** enables efficient workload distribution in Continuous Integration and Continuous Deployment (CI/CD) pipelines. In this setup, the **Master **server orchestrates tasks, while **Slave **nodes execute jobs. Scalable and flexible, it optimizes resource usage, enhances build isolation, and ensures high availability, streamlining the software development process
#### Prerequisites

**1. Jenkins Installed:** Ensure that Jenkins is installed and running on your Master server, to installing Jenkins , you can fellow our this [blog post](https://www.raoshahzaib.cloud/2023/10/httpswww.raoshahzaib.cloudinstall-jenkins-on-ubuntu.html).

**2. Slave Machine: **Ready your Other Machine which ones you want to add as slave node with Jenkins, also install Jenkins on that machine.
For this LAB I'm using my VirtualBox , you can use your own machine or any Cloud like AWS, GCP, Azure.

![Jenkins master slave](/images/jenkins-master-slave-architecture/02-screenshot_7.png)

**##### Start your Machines :**

![Configure Jenkins master and slave](/images/jenkins-master-slave-architecture/03-screenshot_8.png)

**Verify Jenkins is Running on your Both Machines:**

sudo systemctl status jenkins.service**

![Jenkins service running](/images/jenkins-master-slave-architecture/04-screenshot_9.png)

**Go to Browser and Access you Jenkins Master Server(192.168.100.9:8080)**

![Jenkins Dashboard](/images/jenkins-master-slave-architecture/05-screenshot_10.png)

##### Step 1: click on Manage Jenkins

![Manage Jenkins nodes](/images/jenkins-master-slave-architecture/06-screenshot_11.png)

Step 2: Click on Nodes 

![Adding a node in Jenkins master](/images/jenkins-master-slave-architecture/07-screenshot_12.png)

##### Step 3: Click on New Node

![New Node creation form in Jenkins](/images/jenkins-master-slave-architecture/08-screenshot_13.png)

**##### Step 4: Put Your Slave Machine name and click on Permanent Agent and create**
![Node in Jenkins](/images/jenkins-master-slave-architecture/09-screenshot_14.png)

**##### step 5: Here you need to set some configurations, **
go to Remote root directory and set any directory where you want your slave machine store pipeline data, or set labels, to remember where you want to run your Jenkins jobs, in our case we have are deploying only one slave , but in industry you have multiple slave machines, in different zone and regions, so labels are most important, you can also set usage of nodes machine when your node machine running jobs, or net not , im my case i have only machine so i set usage to default, Use this as much as possible.

![Jenkins node setup](/images/jenkins-master-slave-architecture/10-screenshot_15.png)

click on Launch method and select **Launch Agent via SSH** .Add you slave machine IP in Host filed , then click on **add **Button and click on **Jenkins**, for adding credentials.

![SSH launch method and host settings for the Jenkins agent](/images/jenkins-master-slave-architecture/11-screenshot_16.png)

Now select Kind **username **with **password**
and give you username on slave machine , password ,give any id you rembering the Credentials.

![Username and password credentials for the Jenkins agent node](/images/jenkins-master-slave-architecture/12-screenshot_17.png)

in **host key verification Strategy** we are going with Non verifying Verification Strategy

![Host key verification strategy settings](/images/jenkins-master-slave-architecture/13-screenshot_18.png)

**No click on Save**
****Here is Jenkins-slave click on it.

![Jenkins nodes](/images/jenkins-master-slave-architecture/14-screenshot_20.png)

it will take sometime don't be panic give it some time i will be available for your Jenkins masters as a slave.

#### Benefits of Jenkins Master-Slave Architecture:

**Scalability: **Easily scale your CI/CD infrastructure by adding more Slave nodes to distribute the load.**Resource Utilization:** Optimize resource utilization by running builds on different platforms and configurations.**Isolation:** Achieve build isolation by running jobs in isolated environments, preventing one job from affecting others.**High Availability:** Ensure high availability by configuring multiple Slave nodes, reducing downtime in case of hardware failures or maintenance.
