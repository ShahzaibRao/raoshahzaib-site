---
title: "Kubernetes backups and disaster recovery: what actually restores"
description: "A backup you have never restored is a hope, not a plan. Velero, a real restore drill, and the gaps most people only find during an incident."
slug: "kubernetes-backup-disaster-recovery"
---

By Rao Shahzaib · DevOps

I deleted namespaces on purpose. That is how I found out whether my backups worked.

Everyone has backups. Far fewer people have restores. A backup job that runs every night and reports success tells you almost nothing, because the only question that matters is whether the backup can bring the system back. On my two-node cluster I run Velero backups every day, and I proved them by deleting a namespace and restoring it. The pods came back Running. Until that drill, the backups were a hope, not a plan.

A Kubernetes backup has to capture more than one thing. A cluster is not a single database. It is etcd state, application manifests, secrets, persistent volume data, and the custom resources that operators create. Backing up etcd alone gives you the state but not the data on disk. Snapshotting volumes alone gives you the data but not the objects that point at it. Velero covers the middle ground: it backs up the Kubernetes objects and, with the right configuration, the persistent volumes behind them. My backups go to Cloudflare R2, off the cluster and off the cloud account that runs it, with a 30-day retention. A backup that lives on the same infrastructure it protects is not a backup. I also take etcd snapshots every six hours and keep 72 of them, so even if Velero and the cluster both go away, I can still rebuild the control plane state.

The drill is what matters, and it has to be a real one. Reading the Velero logs is not a drill. A drill is picking a namespace, deleting it, restoring it from the backup, and checking that the application actually works — not just that the pods exist, but that they serve traffic and read their data. The gaps only show up during a restore. The usual ones are secrets that were never in the backup because someone created them by hand, custom resources the backup skipped, and volume snapshots that were never taken because the storage class was not configured for them. Every one of those is a five-minute fix before an incident and a multi-hour problem during one. My own drill took four to five minutes, and I ran it across every namespace in the cluster.

Retention and schedule get the same honesty. Daily backups with a 30-day window mean I can lose a day of work at most, and I can go back a month. That is a deliberate trade. More frequent backups cost more storage and more time, and the right answer depends on how much data you can afford to lose. Whatever you choose, write it down. A recovery plan that only exists in someone's head is not a plan.

The last piece is the runbook, and I will be honest: mine is still the design doc, not a standalone runbook yet. When the cluster is down, nobody should be improvising, and that includes me. The runbook says where the backups live, which command restores them, in what order the namespaces come back, and how you verify each one. It is short, it is tested, and it is boring. Boring is the goal. Disaster recovery is not a heroic act. It is a checklist you have already run, on a calm afternoon, when nothing was on fire.
