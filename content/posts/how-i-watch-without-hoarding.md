---
title: "How I Watch Without Hoarding"
date: 2026-09-22
description: "A watching policy built on ownership and restraint: 1080p, sensible file sizes, no remuxes, and missing episodes only."
---

I keep a media library, and I try to be honest with myself about what it is for: making the films and shows I actually want to watch available in my own home, without turning the hard drives into a warehouse of everything I once thought I might watch.

A library without a policy drifts. Every new thing looks like something worth keeping, the disks fill, and I end up curating storage instead of watching films. So the watching policy is small enough to remember:

- **1080p is the default.** It is the sweet spot between looking good on a real television and staying a size that a hard drive can hold hundreds of copies of. If a film truly rewards more resolution, a *compressed* HEVC 4K file — around nine or ten gigabytes, nothing like a remux — earns a place; but the bulk of a well-run library stays 1080p.
- **A film should stay under about 20 GB.** Most do, easily. The frame here is not a hard ceiling but a sanity check: if a single film wants more space than twenty other films each, I am probably hoarding a remux rather than keeping a watchable copy.
- **No remuxes, no raw disc rips.** A remux is the disc poured into a container, sometimes forty or fifty gigabytes. It is a preserving choice, not a watching choice. I keep the disc for preserving; the library is for watching.
- **Missing episodes only, no upgrades.** If I have a watchable copy of a season, I do not replace it with a marginally bigger one. The library grows by filling gaps, not by re-buying what I already hold.

The point of those rules is restraint against a particular kind of drift: the collection that grows without the watching. A smaller library of things I chose is worth more to me than a larger one of things that just accumulated.

## A lawful path: ripping discs you own

None of this is about encouraging people to download things they have no right to. A disc you own is the clearest form of access you are allowed to keep. It does not disappear when a streaming catalogue changes, a licence lapses, or a service decides it no longer wants to host a film. The disc is the preservation copy, and ripping it is the lawful way to turn that owned copy into something your library can serve.

I want to be plain about how this sits against the rest of this article. The watching policy above is a set of principles; the ripping workflow below is the lawful route I value for the things I want to hold onto for the long term. It is one honest way to build a collection of things you are entitled to keep, not a claim about how every file you will ever own came to be. I would rather be straight about the distinction than let the article imply something it does not say.

So for a disc I own and want to keep in the library, the two steps are:

1. **MakeMKV** reads the disc and copies the film, video, audio and subtitles, into a single MKV file, losslessly. It is a straight copy, not a conversion — this is the step that turns "a disc" into "a file", and it is the step that preserves everything.
2. **HandBrake** compresses that MKV down to a sensible size. This is the step that turns "a remux" into "a watchable film under 20 GB". The disc stays on the shelf as the archive; the compressed file is the one that lives in the library.

MakeMKV is free while it remains in perpetual beta: the developers publish a key on their forum (usually valid for a month or two at a time) that unlocks Blu-ray support. You can also buy a permanent licence to stop re-entering the key. HandBrake is genuinely free software at no cost at all. Both run fine on Linux, though MakeMKV's Linux package sometimes needs recompiling after a library update.

## Sensible settings

The numbers below are the ones the HandBrake and MakeMKV communities converge on, and they are the settings I reach for when I do rip something. They are a starting point, not a prescription — the useful thing is to know which knob does what:

- **Container:** MKV. Nothing else carries the subtitles and multiple audio tracks as cleanly.
- **Video codec:** the size-vs-compatibility trade-off. x265 (HEVC) gives roughly the same quality at about half the size of x264 (H.264), but it is slower to encode and not every client decodes it cleanly. **x264 8-bit is the compatibility baseline** — it direct-plays nearly everywhere. The honest rule is not "always encode 8-bit" but "encode to match the client that will actually play it": some libraries lean on x265 HEVC, much of it 10-bit, simply because that is what a lot of content ships in, and whether that is safe depends entirely on whether your player can decode it. **10-bit HEVC is the single most common trigger for a server to transcode instead of direct-play**, and a transcode does not just change the picture — it burns CPU on the media server for an entire film. When in doubt, test one episode on your actual client before encoding a whole series.
- **Quality, not bitrate:** set a rate factor (RF) rather than a target bitrate. The RF scale runs the other way to normal — lower is better quality and bigger file. For 1080p the sweet spot is roughly **RF 20 to 22**; go to RF 18 if a film is grainy or you want the quality to survive a big screen, and up toward RF 24 if you genuinely cannot tell the difference.
- **Audio:** pass through the original track (DTS or AC3) when the player will handle it, or encode to AAC as a widely-compatible fallback. Audio passthrough costs almost nothing in size and keeps the disc's actual soundtrack. Some sources ship lossless tracks — FLAC, or the DTS-HD and Dolby TrueHD found on Blu-rays — which are larger than AAC and unusual in video files, but if the player can handle them there is no reason to re-encode them away.
- **Subtitles:** keep the English subtitles and any "forced" track (the bits that translate on-screen text). Drop the subtitles for languages you will not watch. If you watch a lot of anime or foreign films, prefer text subtitles — SRT or the richer ASS format anime fansubbing uses — over Bit-map-based Blu-ray (PGS) or DVD (VobSub) ones. Those image-based tracks are the other common thing that forces a server transcode, because many clients will not render them natively.
- **Resolution and filters:** leave the resolution at the source — do not upscale a DVD and do not downscale a 1080p Blu-ray unless a specific player needs it. Skip the filtering unless there is a visible problem to fix; filters almost always cost more quality than they save.

The single most useful change is the RF value: it is the one knob that trades size for quality directly, and it is the reason a twenty-hour series can sit at a few gigabytes an episode instead of forty.

## The player matters more than the encode

All of this settings work assumes the thing playing the file can actually decode it. This is where smart TVs quietly undercut the whole setup. A television's apps run on the TV's own platform — Hisense's VIDAA, Samsung's Tizen, LG's webOS — and these are the least capable clients in the chain. They are built to stream a handful of subscription services, not to decode an arbitrary video library. The result is the exact thing a careful encode tries to avoid: the TV reports it cannot play a codec or subtitle track, and the media server steps in to transcode the film on the fly. CPU spins, quality drops, and the whole "small, sensible files" policy gets undone at the moment of playback by a client that was never really built for this.

It is a mistake most people make once: optimising the encode while ignoring the player. The player is worth more than any codec choice. A dedicated media player — a small PC, an Android TV box, an Apple TV 4K, or something like an NVIDIA Shield — decodes almost everything directly, so the server sends the file straight through and stays idle. The trade-offs among them are well documented: the Shield passes through lossless audio (the DTS-HD and Dolby TrueHD tracks on a Blu-ray) but does not support HDR10+; the Apple TV 4K handles HDR10+ but not those lossless passthrough tracks. For a mostly-1080p library with ordinary audio, either is dramatically more capable than a built-in TV app, and the difference shows up first as a server that barely has to work during playback.

For me the plan is simple: I own an older model of Shield anyway, and putting it back into service beats both the television's own app and another purchase. A dedicated player is the missing link between "a sensible encode" and "a server that does nothing but serve."

## The boundary I try to hold

The library answers one question — is this watchable at home? — and the disc answers another — is this preserved? I try not to let the library creep into doing the disc's job. A remux in the library is just a disc taking up space on a hard drive, one that is already on the shelf.

Restraint is not deprivation. It is the difference between a collection that serves the watching and a collection the watching serves. I would rather have a hundred films I chose, at a size I can live with, than a thousand I did not choose, at a size I have to keep paying for.