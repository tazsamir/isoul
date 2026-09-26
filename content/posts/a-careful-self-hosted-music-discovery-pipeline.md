---
title: "A Careful Self-Hosted Music Discovery Pipeline"
date: 2026-09-25
description: "Replacing Spotify-style recommendations with a self-hosted loop built around listening, human choice and an intentional local library."
---

A self-hosted music library is good at playing music I already know. Spotify and Apple Music are good at answering a different question: **what should I listen to next?** The usual bargain is that they learn my habits, keep the recommendation system on their servers, and make discovery part of a subscription catalogue I do not control.

I wanted to separate those things. Navidrome could remain the player for music I keep locally, while an open recommendation service could learn from my listening and suggest unfamiliar artists. Most importantly, a recommendation would still be a suggestion rather than an instruction to collect another album.

The result is a personal music-discovery loop built from several small tools:

```text
Navidrome → ListenBrainz → Explo → Lidarr → acquisition → Navidrome
```

The useful part is not automation for its own sake. It is the order of the loop:

> **recommendation → human choice → lawful acquisition → local library**

A track can appear in a discovery playlist without automatically becoming a permanent album on disk. I can listen, ignore it, investigate the artist, or deliberately choose to keep it. The system restores the pause that an endless recommendation feed tends to remove.

## What I am replacing — and what I am not

This is my alternative to the *discovery function* of a commercial streaming service, not an attempt to reproduce its complete catalogue at home. That distinction keeps the project realistic.

Spotify can combine recommendations and instant playback because it has licensing agreements for a huge catalogue. A self-hosted server does not inherit those rights. My version therefore has a deliberate break in the middle: software may recommend music, but I decide whether I want it and obtain it from a legitimate source.

That break is a feature. It gives me a recommendation history that is not tied to one playback company, a local library that still works if a service changes direction, and a collection shaped by actual choices instead of an algorithm quietly filling storage.

## What each part does

- **[Navidrome](https://github.com/navidrome/navidrome)** serves the local music collection and records what is played.
- **[ListenBrainz](https://github.com/metabrainz/listenbrainz-server)** receives listening history and produces recommendations such as Weekly Exploration.
- **[Explo](https://github.com/LumePart/Explo)** turns those recommendations into playlists and can pass selected music to Lidarr.
- **[Lidarr](https://github.com/Lidarr/Lidarr)** keeps track of artists, albums and missing files.
- **[slskd](https://github.com/slskd/slskd)** is a self-hosted client for the Soulseek network.
- **[Soularr](https://github.com/mrusse/soularr)** connects Lidarr to slskd.
- **[Gluetun](https://github.com/passteque/gluetun)** provides a controlled VPN network namespace for the acquisition client.

The last three components are optional. Navidrome, ListenBrainz and Explo already make a useful discovery system. I can listen to a recommendation elsewhere, buy it from the artist or a shop, and import the files normally.

## The legal boundary

None of these tools grants a right to copy music. Soulseek is a protocol, not a licence, and owning a CD or streaming subscription does not automatically make somebody else's upload lawful to download.

A cautious workflow limits acquisition to music that is:

- released under a licence that permits downloading;
- in the public domain;
- offered freely by the artist or rights holder;
- purchased as downloadable files; or
- otherwise supplied with explicit permission.

The law also depends on jurisdiction. In the UK, the private-copying exception introduced in 2014 was [quashed in 2015](https://www.gov.uk/government/news/quashing-of-private-copying-exception). That makes casual claims such as “ripping a CD you own is always legal” unreliable. The UK Intellectual Property Office maintains [current guidance on copyright exceptions](https://www.gov.uk/guidance/exceptions-to-copyright), but it is not a substitute for legal advice.

There is a second practical issue: peer-to-peer clients may share files as well as download them. Do not expose or share a music directory unless every file in it can lawfully be distributed. An empty dedicated share is safer than pointing the client at a personal library.

## Get the starter files

The sanitized Compose file, environment templates and Soularr configuration are available in the public [`isoul-article-resources` repository](https://github.com/tazsamir/isoul-article-resources/tree/main/music/self-hosted-music-discovery).

Download the repository with Git:

```bash
git clone https://github.com/tazsamir/isoul-article-resources.git
cd isoul-article-resources/music/self-hosted-music-discovery
```

GitHub also provides **Code → Download ZIP** for readers who do not use Git. The examples contain placeholders only; they still need local paths, credentials and provider settings before use.

## Before writing Compose

The stack needs a few decisions first:

1. Choose one host directory for the music library.
2. Give Navidrome and Lidarr the **same container path** for that directory, such as `/music`.
3. Keep incomplete downloads separate from the library.
4. Put passwords and API tokens in environment files, not in Compose.
5. Bind web interfaces to the LAN address or a private overlay network, not every interface.
6. Back up the current Compose files and application databases.

Consistent paths matter. If one container calls a directory `/downloads` and another sees the same files as `/data/incomplete`, imports become needlessly fragile.

## A Compose blueprint

This is a blueprint rather than a drop-in promise. Images change, VPN providers require different settings, and existing installations should be extended rather than replaced. Pin tested image versions or digests before using this in production.

```yaml
name: music-discovery

services:
  navidrome:
    image: deluan/navidrome:latest
    restart: unless-stopped
    user: "${PUID}:${PGID}"
    environment:
      ND_MUSICFOLDER: /music
      ND_DATAFOLDER: /data
      ND_SCANSCHEDULE: 1h
    volumes:
      - ./navidrome:/data
      - ${MUSIC_DIR}:/music:ro
    ports:
      - "${LAN_IP}:4533:4533"

  lidarr:
    image: lscr.io/linuxserver/lidarr:latest
    restart: unless-stopped
    environment:
      PUID: ${PUID}
      PGID: ${PGID}
      TZ: ${TZ}
    volumes:
      - ./lidarr:/config
      - ${MUSIC_DIR}:/music
      - ./downloads:/downloads
    ports:
      - "${LAN_IP}:8686:8686"

  explo:
    image: ghcr.io/lumepart/explo:latest
    restart: unless-stopped
    env_file:
      - ./explo.env
    volumes:
      - ./explo:/opt/explo
    depends_on:
      - navidrome
      - lidarr

  gluetun:
    image: qmcgaw/gluetun:latest
    restart: unless-stopped
    cap_add:
      - NET_ADMIN
    devices:
      - /dev/net/tun:/dev/net/tun
    env_file:
      - ./vpn.env
    ports:
      - "${LAN_IP}:5030:5030" # slskd UI through Gluetun

  slskd:
    image: slskd/slskd:latest
    restart: unless-stopped
    network_mode: "service:gluetun"
    env_file:
      - ./slskd.env
    volumes:
      - ./slskd:/app
      - ./downloads:/downloads
      - ./empty-share:/shared:ro
    depends_on:
      - gluetun

  soularr:
    image: mrusse08/soularr:latest
    restart: unless-stopped
    volumes:
      - ./soularr/config.ini:/data/config.ini:ro
      - ./downloads:/downloads
    depends_on:
      - lidarr
      - slskd
```

The important networking detail is `network_mode: "service:gluetun"`. slskd shares Gluetun's network namespace, so its web port must be published by **Gluetun**, not by slskd. This reduces the chance of accidentally giving the client a second route that bypasses the VPN.

Do not copy VPN settings from an article. Use the [Gluetun provider documentation](https://github.com/qdm12/gluetun-wiki/tree/main/setup/providers) for the provider actually in use.

## Environment files

A non-secret `.env` can hold paths and numeric IDs:

```dotenv
PUID=1000
PGID=1000
TZ=Europe/London
LAN_IP=192.0.2.10
MUSIC_DIR=/srv/music
```

`192.0.2.10` is a documentation address; replace it with the host's private address.

Keep credentials in separate files with restrictive permissions:

```bash
chmod 600 explo.env vpn.env slskd.env soularr/config.ini
```

Typical Explo settings include the Navidrome URL, Lidarr URL, ListenBrainz username and ListenBrainz token. slskd needs separate local web credentials and Soulseek credentials. Soularr needs the Lidarr and slskd URLs and API keys. Consult each project's current documentation for exact variable names because they can change between releases.

Never commit these files. A small `.gitignore` is enough:

```gitignore
.env
*.env
soularr/config.ini
navidrome/
lidarr/
slskd/
downloads/
```

## Configure the loop

### 1. Navidrome to ListenBrainz

Create a ListenBrainz account and token, then enable ListenBrainz scrobbling in the Navidrome user's personal settings. Scrobbling is per user, which is useful in a household: one person's listening does not have to distort another person's recommendations.

Play a track and check that a new listen appears in ListenBrainz before adding another layer.

### 2. ListenBrainz to Explo

Give Explo the ListenBrainz identity and token, plus the internal Navidrome URL. Start with playlist generation only. A Weekly Exploration playlist appearing in Navidrome proves discovery works without acquiring a single file.

### 3. Explo to Lidarr

Add Lidarr's URL and API key to Explo. Use conservative monitoring:

- monitor selected albums rather than an artist's entire catalogue;
- do not enable upgrades merely because a larger file exists;
- apply a quality profile with sensible size limits;
- inspect recommendations before starting a search.

### 4. Lidarr to slskd

Soularr reads wanted albums from Lidarr, searches through slskd, and leaves completed files where Lidarr can import them. The download path must mean the same thing inside all three containers.

Treat this as an optional transport, not as the source of permission. Search results still need a lawful basis.

## The manual discovery method

Automation does not need to make the final decision. My preferred manual loop is:

1. Open Weekly Exploration on ListenBrainz.
2. Play unfamiliar artists without adding them permanently.
3. Look up an artist's official site, Bandcamp page or label.
4. Buy or download an authorised release.
5. Add only the chosen artist or album to Lidarr.
6. Import the files and let Navidrome scan the library.

If using Lidarr to initiate a search, monitor only the specific album and use the album-level search button. “Monitor everything” is convenient, but it turns discovery into collection growth before I have decided whether I like the music.

## Verification that matters

A running container is not an end-to-end test. Check each boundary:

- a Navidrome play reaches ListenBrainz;
- Explo creates or updates the expected Navidrome playlist;
- a selected album appears in Lidarr;
- slskd and Gluetun report the same public address;
- the download path is writable by Soularr and readable by Lidarr;
- Lidarr imports a permitted test release;
- Navidrome finds it on the next scan;
- restarting the stack preserves configuration and history.

Also check that slskd is not listening directly on a public host interface. A VPN protects outbound routing; it does not excuse an exposed administration page.

## Restraint is part of the design

The best feature in this stack is the pause between recommendation and acquisition. ListenBrainz can suggest widely, Explo can organise the suggestions, and I can decide narrowly.

That keeps the library intentional. Discovery should create more listening, not merely more files.

## Project documentation

- [Navidrome documentation](https://www.navidrome.org/docs/)
- [ListenBrainz](https://listenbrainz.org/)
- [Explo source and documentation](https://github.com/LumePart/Explo)
- [LinuxServer.io Lidarr image](https://docs.linuxserver.io/images/docker-lidarr/)
- [slskd Docker documentation](https://github.com/slskd/slskd/blob/master/docs/docker.md)
- [Soularr documentation](https://soularr.net/)
- [Gluetun documentation](https://github.com/qdm12/gluetun-wiki)
