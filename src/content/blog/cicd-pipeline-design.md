---
title: "Designing a CI/CD pipeline that fails safe"
description: "A good pipeline is not the fastest one. It is the one that refuses to ship a broken build, keeps its secrets out of reach, and can always roll back."
slug: "cicd-pipeline-design"
---

By Rao Shahzaib · DevOps

My rule for a pipeline is simple: a broken build must never reach the cluster. Speed comes second. Caching, parallel jobs, a nice dashboard — all of that is secondary. If a pipeline can deploy a failing build, it will, at the worst possible moment. So I design around that one rule, and every other choice follows from it.

I keep building and deploying apart. The CI job builds the code, runs the tests, scans the image, and pushes it to the registry with a digest pin — a hash, not a moving tag like `latest`. Nothing in that job touches the cluster. Deployment is a separate act: a change to a Git repository that says "run this digest." The cluster picks it up from there, through ArgoCD. If the build fails, there is no new digest and nothing to deploy. If the deploy fails, the build is untouched and the previous digest is still right there in Git.

Then the gates. Every gate in my pipeline is a real gate. Tests run on every pull request, and a red build blocks the merge. No overrides, no "merge it and fix it later." A static analysis scan runs on the code — I use SonarCloud — and an image scan runs on the built image, and both have to pass before the image is pushed. The gates feel slow for the first week, then they disappear into the background. What they replace is the 2 a.m. page that says a bad image is in production.

Secrets get the same treatment. A pipeline needs credentials — registry logins, cloud keys, deployment tokens. Mine live in the CI system's secret store, injected at run time, and nowhere else. They never appear in a log, never sit in a repository, and never get baked into an image. If a secret leaks into a log, I rotate it and fix the logging. On my own projects the rule is absolute: no hardcoded passwords anywhere, in any file, for any reason. That is a rule I have refused to bend even when it slowed me down.

The rollback plan gets written before the deploy, not after the incident. A deploy that cannot be undone is a gamble. With digest pins and Git as the source of truth, a rollback is a revert: the previous known-good digest goes back into the repository and the cluster returns to it. I also keep deployments small and frequent. A small change that breaks something is easy to find. A week of changes shipped at once is a mystery.

The pipeline also has to tell me when it fails, loudly. A failed job nobody notices is worse than no pipeline at all, because it creates the illusion of safety. When a job fails, the failure has to reach me the same day — and a failed deploy blocks the next one until I look at it. GitHub emails me when a run fails. A pipeline that fails safe is a pipeline I can trust. And trust is the only reason to automate deployments at all.
