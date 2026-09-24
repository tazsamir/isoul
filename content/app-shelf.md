---
title: "My app shelf"
description: "The services I actually use across my PC, N100 and TrueNAS-Normandy."
---

This is a record of practical choices in my own setup, not a catalogue of every available project. I prefer software that is understandable, documented, exportable and possible to restore. The shelf is grouped by where I run it; it deliberately does **not** document or recommend the Arr stack.

## Main PC — Fedora and KDE

| Need | App | Experience and notes |
|---|---|---|
| Desktop operating system | [Fedora Linux](https://fedoraproject.org/) | My main Linux desktop and the base for daily work. |
| Desktop environment | [KDE Plasma](https://kde.org/plasma-desktop/) | The desktop environment I use on the PC. |
| AI-assisted maintenance | [Hermes Agent](https://github.com/NousResearch/hermes-agent) | Used from the terminal to inspect, document and safely maintain the workstation and homelab. |
| Device synchronisation | [Syncthing](https://syncthing.net/) | Direct synchronisation between devices rather than relying on a hosted sync provider. |
| Notes | [Simplenote](https://simplenote.com/) | The notes service I use. |
| Remote desktop and support | [RustDesk](https://rustdesk.com/) | Used for remote access where it is useful; access control and exposure still matter. |

## GEEKOM N100 — always-on Docker host

| Need | App | Experience and notes |
|---|---|---|
| Local HTTPS and reverse proxy | [Caddy](https://caddyserver.com/) | Provides the friendly HTTPS routes used by the local services. |
| Local DNS | [CoreDNS](https://coredns.io/) | Maps the homelab service names to the local services. |
| Photos and phone backups | [Immich](https://immich.app/) | The main photo and video library; the live data is stored on Normandy. |
| Films and television playback | [Jellyfin](https://jellyfin.org/) | Personal media access without depending on one streaming service. |
| Music | [Navidrome](https://www.navidrome.org/) | Streams the music collection I control. |
| Audiobooks and podcasts | [Audiobookshelf](https://www.audiobookshelf.org/) | Provides access to audiobooks and podcasts. |
| Book and document reading | [Kavita](https://www.kavitareader.com/) | Used for reading material and library access. |
| Personal document management | [Papra](https://github.com/baptisteArno/papra) | The document application I currently use. |
| Bookmarks and saved web content | [Karakeep](https://github.com/karakeep-app/karakeep) | A project I actively use and rate positively for keeping bookmarks, notes and saved material. |
| Service monitoring | [Uptime Kuma](https://github.com/louislam/uptime-kuma/) | Used in the lab for service monitoring. |
| RSS reader | [FreshRSS](https://freshrss.org/) | Current RSS reader on my stack. |
| Container and server monitoring | [Beszel](https://github.com/henrygd/beszel) | Used for server and PC information with a useful lightweight interface. |
| Network device monitoring | [NetAlertX](https://github.com/jokobsk/netalertx) | Used to see what is connected and active on the homelab network. |
| Container update visibility | [What's Up Docker](https://github.com/getwud/wud) | Checks container images and sends update notifications without taking over Compose management. |
| Notifications | [Gotify](https://gotify.net/) | Receives local health and update notifications. |
| Container API isolation | [Docker Socket Proxy](https://github.com/Tecnativa/docker-socket-proxy) | Keeps monitoring access to Docker's socket narrower than exposing the raw socket directly. |
| Homelab dashboard | [Glance](https://github.com/glanceapp/glance) | Provides a single local dashboard for the services and useful links. |
| PDF tools | [BentoPDF](https://github.com/alam00000/bentopdf) | A lightweight PDF tool I prefer over heavier platforms. |
| Ebook library | [Calibre-web](https://github.com/jOeA28/calibre-web) | Testing whether a Kindle can download books directly; separate from Lazylibrarian's audiobook focus. |
| Foreign-media downloads | [MeTube](https://github.com/alexta69/metube) | A simple web interface around yt-dlp for controlled downloads. |
| Network access | [Tailscale](https://tailscale.com/) | Used for private access between trusted devices; it is not treated as a replacement for local DNS or backups. |

The N100 also hosts other media-management and download components. They are intentionally not listed here as recommendations; this shelf is about the services I use and the roles they fill, not about promoting an Arr-based workflow.

## TrueNAS-Normandy — live storage

| Need | App or service | Experience and notes |
|---|---|---|
| Storage platform | [TrueNAS](https://www.truenas.com/) | Normandy is the active TrueNAS server and the live storage system. |
| Photo-library storage | [Immich](https://immich.app/) data and PostgreSQL data | The live Immich library is stored under the `Shepard` dataset on Normandy. |
| Network file storage | SMB and NFS | Used to make storage available to the PC and Docker services; permissions and identity mapping are part of the design. |
| Local replication target | TrueNAS replication | Normandy is the live copy; Borgcube is the separate recovery copy. |
| Encrypted backup workflow | [Restic](https://restic.net/) | Used for encrypted, verifiable backups of important configuration and service data. |

## Tested, but not current choices

- **[Forgejo](https://forgejo.org/)** — tested, but not something I personally use; still useful to understand as a self-hosted Git option.
- **[Mealie](https://mealie.io/)** — tested and works well. Adding food and recipes can be tedious, which is an important practical limitation.

This list records experience, not endorsements. Check the [review method](/review-method/) before treating any project as a recommendation.
