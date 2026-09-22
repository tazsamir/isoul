---
title: "Why I Self-Host"
date: 2026-09-22
description: "Self-hosting started as a technical hobby, but ownership, privacy, learning and keeping my own data are why I keep doing it."
tags:
  - self-hosting
  - homelab
  - privacy
  - linux
  - personal
draft: true
---

> **Previously on isoul.uk:** The internet used to feel like something we moved through rather than something that moved content at us. Forums had addresses. Communities had places. Discovery was active. That feeling — of participating rather than consuming — has been harder to find as feeds took over.


There are much easier ways to use technology than self-hosting.

If I want photo storage, somebody will sell it to me.

If I need file sync, there are dozens of services.

If I want media streaming, I can pay a subscription and install an app.

Instead, I have ended up with NASes, Docker hosts, virtual machines, DNS servers, monitoring, backups and enough cables to make the "easy" option look extremely sensible.

So why do I self-host?

The answer has changed over time.

## At first, because I could

A lot of it began as curiosity.

I work with technology and have always liked computers, but running your own infrastructure teaches you things that are difficult to understand purely from documentation.

Docker makes more sense after you have broken a container.

DNS makes more sense after you have spent far too long wondering why a hostname resolves on one device but not another.

Backups become very real after you actually need to restore one.

A homelab turns abstract concepts into annoying, memorable experiences.

That is excellent training.

## Then I started caring about ownership

At some point, the question changed from "Can I run this myself?" to "Why am I giving this data to somebody else in the first place?"

Photos are the obvious example.

They are not just files.

They are family history.

Once I had a working Immich setup, sending every new photo to another company's cloud by default stopped feeling necessary.

The same thinking gradually spread to files, calendars, contacts and other parts of my digital life.

Self-hosting became less about replacing services for the sake of it and more about deciding which things were important enough that I wanted my own copy and my own control.

## Privacy matters, but it isn't absolute

I don't think self-hosting magically creates privacy.

A badly configured server exposed to the internet can be much worse than using a reputable hosted service.

You still have to think about security, updates, access controls and backups.

And I haven't stopped using outside services entirely.

For me, privacy is more about reducing unnecessary dependence.

If something contains years of personal history, I want to know where it is, how it is backed up and how I would get it back.

## The restore changed my attitude

The biggest lesson came when I accidentally wiped my primary NAS while moving house.

Suddenly all the nice diagrams and backup ideas stopped being theoretical.

I had family photos to recover.

There was a secondary NAS. There was Backblaze. There were encrypted datasets, keys, database backups and plenty of moments when I discovered the difference between believing something was backed up and proving it could be restored.

I eventually got the important data back.

The experience permanently changed how I think about self-hosting.

Running the service is only half the job.

The other half is making sure the service can fail without taking your memories with it.

## I also just enjoy it

There is another answer that doesn't need a philosophy behind it.

I enjoy this.

I like running Linux.

I like getting a service working properly.

I like seeing Grafana dashboards light up with data from machines in my house.

I like giving servers ridiculous names from science fiction.

I even occasionally enjoy troubleshooting DNS.

Occasionally.

## My version of self-hosting

I don't think everybody needs a rack, a cluster or twenty services.

My own setup changes constantly.

Some things are always on. Some machines exist for backups. Some services disappear because I realise I never actually use them.

That is part of the point.

Self-hosting gives me the freedom to build the system around my needs instead of changing my habits around somebody else's product.

It is less convenient.

It creates work.

It can fail spectacularly.

And I still wouldn't give it up.

