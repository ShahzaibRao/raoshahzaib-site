---
title: "Installing Jenkins on Ubuntu: A Simplified Step-by-Step Guide"
description: "Install Jenkins on Ubuntu step by step: Java 17, the Jenkins repository, service setup, the unlock screen, admin user creation and your first dashboard."
slug: "installing-jenkins-on-ubuntu"
---

By Rao Shahzaib · DevOps

Installing Jenkins on Ubuntu a Simplified Guide

![Jenkins installation](/images/installing-jenkins-on-ubuntu/01-jenkins-installation.jpg)

### Jenkins installation on Ubuntu: A Step-by-Step Guide
Jenkins, an open-source automation server, is a popular choice among developers for continuous integration and continuous deployment (CI/CD) pipelines. If you're looking to streamline your development workflow, you're in the right place. In this guide, we will walk you through the process of installing Jenkins on Ubuntu, making the setup smooth and hassle-free.
#### Prerequisites:
Before we dive in ,Ensure you have the following:#### 1. Ubuntu Server

![Ubuntu Server](/images/installing-jenkins-on-ubuntu/02-ubuntu-server.png)

##### 2. JAVA Development Kid (JDK)
Jenkins requires java to run
**sudo apt update**

![Installing OpenJDK Java for Jenkins](/images/installing-jenkins-on-ubuntu/03-jdk-install.png)

**sudo apt install fontconfig openjdk-17-jre**

##### Step 1: Update System Packages

Before installing nay new package, best practice is that you need to update you system packages 

**sudo apt-get update**
##### Step 2: Download and Install Jenkins

We are going with long term support release

![Adding the Jenkins repository](/images/installing-jenkins-on-ubuntu/04-adding-repo.png)

curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | sudo tee \
  /usr/share/keyrings/jenkins-keyring.asc > /dev/null
echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null
**sudo apt-get update**
![Updating package lists after adding the Jenkins repository](/images/installing-jenkins-on-ubuntu/05-update.png)

##### Step 3: Install Jenkins
**sudo apt-get install jenkins**
![Install Jenkins](/images/installing-jenkins-on-ubuntu/06-install-jenkins.png)

##### Step 4: Start and Enable Jenkins Service

**sudo systemctl enable jenkins.service --now**

![Start and enable the Jenkins service](/images/installing-jenkins-on-ubuntu/07-enbale-service.png)

Verify Jenkins is running 

**sudo systemctl status jenkins.service**

![Checking the Jenkins service status](/images/installing-jenkins-on-ubuntu/08-status.png)

##### Step 5: Access Jenkins Web Interface (192.168.100.8:8080)

![Jenkins unlock screen in the browser](/images/installing-jenkins-on-ubuntu/09-jenkins-login.png)

##### Step 6: Go to that address (/var/lib/jenkins/secrets/initialAdminPassword)

![Initial admin password file contents](/images/installing-jenkins-on-ubuntu/10-password.png)

Copy the password and paste it into the Jenkins setup wizard.

![Jenkins unlock screen with the administrator password](/images/installing-jenkins-on-ubuntu/11-screenshot_1.png)

![Customize Jenkins plugins page](/images/installing-jenkins-on-ubuntu/12-screenshot_2.png)

**##### Customize Jenkins**
**##### Step 7: Create Admin User**
![Create first admin user form in Jenkins](/images/installing-jenkins-on-ubuntu/13-screenshot_3.png)

![Jenkins instance configuration page](/images/installing-jenkins-on-ubuntu/14-screenshot_4.png)

![Jenkins getting started page](/images/installing-jenkins-on-ubuntu/15-screenshot_5.png)

**##### Start Using Jenkins**

![Jenkins Dashboard](/images/installing-jenkins-on-ubuntu/16-screenshot_6.png)

**Congratulations! You have successfully installed Jenkins on your Ubuntu server.**
