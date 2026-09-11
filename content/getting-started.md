---
title: "New to homelabs? Start here"
description: "A practical starting point, based on a long and sometimes unnecessarily complicated homelab journey."
---

A homelab is not a competition. You do not need a rack full of servers, a dozen virtual machines or the latest enterprise hardware. You need a problem worth solving, hardware you already have, and a way back when something goes wrong.

## My starting point

My homelab journey started with FreeNAS decades ago. At the time, the idea was simple: keep files on my own hardware instead of relying entirely on someone else's computer.

In 2018, while transitioning into a new job, I came across **Lawrence Systems** and **Novaspirit** on YouTube. Their videos introduced me to a much wider homelab world: Raspberry Pis, containers, virtualisation, networking and the idea that a home server could be both useful and educational.

I have always been someone who keeps technology. I do not always do much with it immediately, but I keep it because it may become useful later. Over the years that has meant accumulating several switches, SFP connections and a 2.5-gigabit switch. The equipment is there, but the current setup is deliberately modest. A pile of hardware is not the same thing as a useful homelab.

## The things I tried

I have experimented with several approaches, including:

- Xen Orchestra
- Proxmox
- Hyper-V
- Windows Server
- Different Linux distributions
- Containers and Docker-based services
- Network storage and dedicated NAS platforms

Trying different platforms was useful, but it also taught me that complexity is easy to add and hard to maintain. A more capable system is not automatically a better system.

These days I usually return to plain **Debian** or **Fedora**, rather than heavily customised derivatives. There is nothing wrong with derivatives, but a straightforward base makes it easier to understand what is installed, follow official documentation and recover from problems.

## Where a new starter should begin

### 1. Start with one real problem

Choose one thing you genuinely want to improve:

- Back up family photos
- Store and stream media locally
- Share files between devices
- Run a password manager
- Host notes or documents
- Learn Linux and Docker

Do not start by installing every service you find interesting. Install one, use it for a while and learn how it works.

### 2. Use hardware you already own

An old desktop, mini PC or Raspberry Pi is enough to begin. Start without buying a rack, enterprise switch or server-grade hardware. Upgrade only when you can explain the limitation you are solving.

A modest, quiet and reliable machine is often better than powerful hardware that uses too much electricity or becomes difficult to maintain.

### 3. Learn the basics before the advanced tools

The useful foundations are:

- Linux command line basics
- Files, permissions and ownership
- IP addresses and DNS
- SSH
- Storage and filesystems
- Docker Compose
- Backups and restores
- Reading logs

Virtualisation, VLANs, Kubernetes and advanced networking can wait. They are useful tools, but they are not prerequisites for running one good service.

### 4. Keep the network boring

You do not need to use every switch, SFP port or high-speed connection immediately. A simple wired network, a sensible DNS name and no unnecessary public exposure are a strong beginning.

Add faster links when they solve a real bottleneck, not simply because the hardware supports them.

### 5. Plan recovery before adding more services

Before installing the next application, know:

- Where its data lives
- How it is backed up
- How it is updated
- How it is restored
- What happens if the server dies

A homelab is successful when it is recoverable, not when its dashboard has the most icons.

## My KISS rule

**Keep it simple, keep it documented and keep a backup.**

The best homelab is the one you understand well enough to repair on a tired Sunday morning. Start small, learn the boring parts and expand only when your existing setup is reliable.
