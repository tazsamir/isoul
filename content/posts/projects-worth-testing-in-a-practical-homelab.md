---
title: "Projects worth testing in a practical homelab"
date: 2026-09-14
description: "A short list of self-hosted projects that fit a practical homelab, beyond the tools already in use."
tags: [self-hosting, homelab, privacy, networking, media]
---

A useful project is not automatically worth adding just because it is new, popular or active on GitHub. I look for a clear problem, sensible deployment, useful documentation, a workable backup path and enough maintenance history to justify the time spent learning it.

This list deliberately excludes tools already used here, including Beszel, Dockhand and `youtube-dl` workflows. Karakeep is also excluded as a recommendation because it is already in use and has proved to be good in practice.

## Homelable — worth testing

[Homelable](https://github.com/Pouzor/homelable) is a self-hosted homelab infrastructure visualiser with an interactive network diagram and live status monitoring.[^1]

This is interesting because a homelab eventually becomes difficult to explain. A diagram that reflects service status could be useful for documenting hosts, networks and dependencies without maintaining a completely separate diagram by hand.

The project is still a watch-and-test item rather than a recommendation. Check authentication, how stale or missing services are represented, whether the diagram can be backed up or exported, and whether the licence is clear before relying on it as the authoritative record of a network.

**Status:** Worth testing.

**Open questions:** maturity, licence, authentication and accuracy of live discovery.

## Pangolin — worth testing cautiously

[Pangolin](https://github.com/fosrl/pangolin) is a self-hosted networking and security platform built around WireGuard, with zero-trust VPN access, reverse proxying, identity-aware access and a dashboard.[^2]

It is not an obvious replacement for Tailscale when Tailscale is already working well. Its interest is different: it may give a self-hoster more control over the access and publishing layer, particularly when private services need to be reached through a central gateway.

Pangolin is security-sensitive and appears to be moving quickly. The Community Edition is reported as AGPL-3.0, while additional enterprise functionality uses a commercial licence, so the current boundaries need to be checked carefully.[^3] Client compatibility, identity-provider integration, failure recovery and upgrade procedures should all be tested before putting it in front of important services.

**Status:** Watching, with a possible controlled test.

**Flags:** security-sensitive; licence boundaries need checking; not a casual Tailscale replacement.

## youtube-dl-nas — useful idea, but already tested here

[youtube-dl-nas](https://github.com/hyeonsangjeon/youtube-dl-nas) provides an authenticated `yt-dlp` queue for NAS use, including video, audio, subtitles, mobile sharing, restart-safe downloads and Docker.[^4]

The project matches a real self-hosting need: turning downloads into a controlled queue rather than relying on a desktop session. It is also a good example of a narrowly focused tool solving one practical problem.

It is not a new recommendation here because it has already been used. Anyone evaluating it should still check authentication storage, cookie handling, download legality, update behaviour when `yt-dlp` changes and whether the project has enough maintenance depth for their collection.

**Status:** Previously tested; not a new candidate.

## Dockhand — already useful here

[Dockhand](https://github.com/Finsys/dockhand) is a Docker management application with container management, Compose stack support, remote-host features, logs and an in-browser shell.[^5]

Its practical value here is not replacing manually written Docker Compose files. It is useful for checking containers and managing updates while keeping the Compose definition as the source of truth. That separation matters: a UI should make routine operations easier without hiding how the service is actually deployed.

Docker management interfaces deserve careful treatment because they can have host-level privileges. Authentication, remote-agent security, secret handling and audit behaviour should be checked before exposing one outside the local network.

**Status:** Used here; positive practical experience.

## Beszel — already used here

[Beszel](https://github.com/henrygd/beszel) is a lightweight monitoring system with historical data, Docker statistics and alerts.[^6] A `0.19.0` release was published on 3 September 2026.[^7]

It is already used here, so it belongs on the app shelf rather than this list of new things to try. Its continued release activity is worth tracking, but repeating the recommendation would add little value.

**Status:** Used here; report updates rather than recommend again.

## What I would test first

If I were starting a small evaluation, I would begin with Homelable because it fills a documentation and visibility gap rather than duplicating an existing service. Pangolin would come next, but only in an isolated test path with a rollback plan. The other projects are either already used or already tested here.

That is the useful distinction: a project can be interesting without being a new recommendation for a particular homelab.

## Sources

[^1]: [Homelable on GitHub](https://github.com/Pouzor/homelable)
[^2]: [Pangolin on GitHub](https://github.com/fosrl/pangolin)
[^3]: [Pangolin licensing discussion](https://linuxdork.com/self-hosted-apps/pangolin/)
[^4]: [youtube-dl-nas on GitHub](https://github.com/hyeonsangjeon/youtube-dl-nas)
[^5]: [Dockhand on GitHub](https://github.com/Finsys/dockhand)
[^6]: [Beszel on GitHub](https://github.com/henrygd/beszel)
[^7]: [Beszel releases](https://github.com/henrygd/beszel/releases)
