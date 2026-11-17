---
title: "Smaller Docker images with multi-stage builds"
description: "A Dockerfile that ships its compiler, its cache, and its history is slow to pull and easy to attack. Multi-stage builds keep the build tools out of the final image."
slug: "docker-multi-stage-builds"
---

By Rao Shahzaib · DevOps

I ship two images from the same Dockerfile. One is slim, for production. The other has a shell, for staging. That one decision fixed most of the image problems I kept running into: big pulls, slow restarts, and tools sitting in production that had no business being there.

The usual mistake is building everything in one stage. The Dockerfile installs the compiler, the test tools, the package cache, builds the application, and ships all of it. The final image carries the whole workshop that built it. Every pull downloads it, every node stores it, and every container runs with an attack surface it never needed.

A multi-stage build splits the job. The first stage is the workshop. It has the compiler and the dependencies, and it produces the application binary. The second stage is the shipping box. It starts from a small base image and copies only the finished binary, with `COPY --from=build`. Nothing else travels. A Go service that needed the full Go toolchain to build can ship as one binary in a minimal image. A Python app can build its wheels in one stage and install only the wheels in the next, leaving pip and the build headers behind.

For LifeQuest I went further and ship distroless images. The production image has no shell at all. The staging image is the debug variant, with a shell, so I can still get in and look around when something is wrong. Same Dockerfile, two targets. If you need a shell for debugging, use a debug variant of the base image. Do not stuff tools into production to save yourself a rebuild.

Order matters as much as size, because Docker caches each layer and a cache miss rebuilds everything below it. I copy the dependency files first and install dependencies before copying the source code. A one-line code change then reuses the cached dependency layer instead of reinstalling the world. And I keep a `.dockerignore` file that leaves `.git`, test data, and local config out of the build context, so the daemon never sends them in the first place.

I pin my base images. `python:3.13-slim` today is not the same image it was last month, and an unpinned tag can change under you without a word. A digest pin makes the build reproducible: same input, same image, and an upgrade is a deliberate commit, not an accident. The same goes for the packages installed inside the image. Reproducible builds are how I answer "what changed?" with a commit hash instead of a shrug.

Then I measure. I run `docker images` before and after, and I look at the number. A smaller image pulls faster on every node, starts faster on every restart, and presents a smaller target. Small images are not a vanity metric. They are what make the rest of the pipeline — the registry, the pull, the rollout — cheap enough to do often.
