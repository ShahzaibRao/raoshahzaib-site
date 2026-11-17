---
title: "GitOps with ArgoCD: why Git is the source of truth"
description: "GitOps means the cluster follows Git, not the other way round. How ArgoCD, drift detection, and pull-request reviews keep a real Kubernetes platform honest."
slug: "gitops-with-argocd"
---

By Rao Shahzaib · DevOps

I run a two-node Kubernetes cluster on Oracle Cloud, and I am the only person who touches it. That is exactly why Git is the source of truth for it. When a team of one changes something by hand at 2 a.m., nobody remembers it the next morning — not even me. So nothing is allowed to change the cluster except a commit.

ArgoCD is the thing that enforces that. It watches my Git repository and compares it with the live cluster, all the time. If the two disagree, ArgoCD shows me the drift and brings the cluster back to what Git says. The repository is the one place I can read to know what should be running, and if the answer is not in Git, it is not running — or it should not be.

A change is a pull request. I write it, I review it, it merges, ArgoCD notices, and the cluster moves. A bad change is a revert, and the revert is a reviewed change too. There is no separate deploy step to forget, and nothing needs cluster credentials to ship — repository access and a review are enough. That separation is the security point as well: the cluster only ever pulls from Git. A compromised laptop cannot push straight into production, because the laptop cannot push to the cluster at all.

I organise the whole thing with the app-of-apps pattern. One root ArgoCD application points at a folder in the repository, and it creates the rest: cert-manager for TLS, External Secrets for secrets, the monitoring stack, Velero for backups, and the application workloads. Adding a component means adding a file to Git. I never run a command to install something on the cluster.

Secrets are the one thing that never goes into Git, and I am strict about it. They live in OCI Vault, and the External Secrets Operator delivers them into the cluster. Git only holds the reference — which secret, from where. The value never appears in a repository. I treat any password that lands in Git as public forever, because sooner or later it is.

I also run a daily GitHub Actions job that plans the Terraform and checks for drift, and it opens an issue if something moved. It only alerts. It never recreates anything on its own, because I want to read the drift before anything touches the cluster.

ArgoCD syncs the cluster back to Git on its own. I press nothing manually — the merge is the deployment.

GitOps will not fix a bad application, and it will not stop me from merging a bad manifest. What it gives me is a record. Every change has an author, a review, and a time. When something breaks at 2 a.m., I do not guess what changed. I read the log, find the commit, and revert it. The cluster is a machine. Git is its memory.
