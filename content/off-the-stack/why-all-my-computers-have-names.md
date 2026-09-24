---
title: "Why All My Computers Have Names"
date: 2026-09-22
description: "Borgcube, Deltaflyer, Normandy and Bebop: why naming homelab machines makes the infrastructure feel a little more personal."
tags:
  - homelab
  - self-hosting
  - science-fiction
  - personal
draft: true
---

> **Previously on isoul.uk:** Two decades of online accounts accumulate quietly until an account stops feeling like an account and starts feeling like infrastructure. Photos, files, contacts, calendars — once I started asking where all of it actually lived, moving some of it home started feeling less like a technical exercise and more like a deliberate choice.


Some people name servers after their function.

`docker01`.

`nas01`.

`backup02`.

That is sensible.

I have machines called **Borgcube**, **Deltaflyer**, **Normandy** and **Bebop**.

This is less sensible.

I recommend it.

## A homelab is already unnecessary enough

Most of what I run at home could be replaced with hosted services.

That means the homelab isn't only infrastructure. It is also a hobby.

Once I accepted that, there wasn't much reason to pretend the machines needed enterprise naming conventions.

I wanted names I would actually enjoy seeing.

Science fiction supplied plenty.

## Borgcube

**Borgcube** is one of my NAS names.

The name comes from the Borg cubes in *Star Trek*: huge, functional ships built around storage, resilience and redundancy rather than elegance.

That makes it a good fit for the square Node 804 case and for a machine whose job is to hold a separate recovery copy.

## Deltaflyer

My Proxmox host is **Deltaflyer**.

The Delta Flyer was the custom shuttle from *Star Trek: Voyager*, so the name still keeps part of the original *Star Trek* thread while belonging to a separate machine.

It also sounds much better than `pve01`.

The server doesn't care.

I do.

## Normandy

My main NAS is **Normandy**.

That one comes from *Mass Effect* rather than *Star Trek*.

Again, the theme isn't perfectly consistent.

I am not running a real datacentre, so this has never concerned me.

Normandy has become one of the important machines in the house because it holds files and photos and acts as a central point for a lot of the things I run.

The name gives it an identity that "main NAS" never would.

## Bebop

My little Intel N100 Docker host is **Bebop**.

That came later.

Bebop is the always-on machine doing a surprising amount of work for something so small: containers, hosted services, DNS-related jobs and monitoring all live around it.

The name comes from another bit of science-fiction/anime history rather than following the *Star Trek* pattern.

That is fine.

A good naming scheme should survive contact with things you like.

## Names help more than I expected

There is actually one practical benefit.

I remember names more easily than numbered hosts.

"SSH to Bebop" is instantly clear in my head.

"Check Deltaflyer" tells me exactly which physical machine I mean.

"Normandy backup" means something.

That matters once a homelab grows beyond a single PC under a desk.

## The names connect the hobby to everything before it

The part I like most is that the naming scheme accidentally connects different periods of my life.

I grew up watching science fiction because my older siblings watched it.

Later I got deeply into anime.

Then I became the sort of adult who runs Linux servers at home for fun.

Now those servers are named after things I watched decades earlier.

None of that was planned.

But it makes the whole setup feel more personal.

And if I am going to spend an evening troubleshooting why a Linux bridge refuses to behave, I would much rather be angry at **Deltaflyer** than `pve01`.

