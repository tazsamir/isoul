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

## A route based on discs you own

None of this is about encouraging people to download things they have no right to. A disc you own is durable access: it does not disappear when a streaming catalogue changes, a licence lapses, or a service decides it no longer wants to host a film. Turning that disc into a library file can be practical, but the law varies by jurisdiction. In the UK, the private-copying exception introduced in 2014 was quashed in 2015, and circumventing copy protection can raise separate legal issues. Ownership of the disc does not automatically make format shifting lawful everywhere, so check the rules where you live.

I want to be plain about how this sits against the rest of this article. The watching policy above is a set of principles. Where local law and the rights attached to the source permit making a personal copy, the workflow below explains the technical process. It is not legal advice or a claim that owning a disc settles every rights question. The UK government provides a [copyright overview](https://www.gov.uk/copyright) and guidance on [using somebody else's intellectual property](https://www.gov.uk/using-somebody-elses-intellectual-property/copyright).

Where those rights permit it, the two technical steps are:

1. **MakeMKV** reads the disc and copies the film, video, audio and subtitles, into a single MKV file, losslessly. It is a straight copy, not a conversion — this is the step that turns "a disc" into "a file", and it is the step that preserves everything.
2. **HandBrake** compresses that MKV down to a sensible size. This is the step that turns "a remux" into "a watchable film under 20 GB". The disc stays on the shelf as the archive; the compressed file is the one that lives in the library.

MakeMKV offers a time-limited beta and a paid licence. HandBrake is free and open-source software. Both run on Linux, although installation and hardware support vary by distribution.

## Sensible settings

The settings below are common starting points rather than a prescription. The useful thing is to know which control does what:

- **Container:** MKV. It handles multiple audio and subtitle tracks well and is widely supported by media servers.
- **Video codec:** the size-vs-compatibility trade-off. x265 (HEVC) can produce smaller files than x264 (H.264) at similar perceived quality, but results depend on the source and encode settings, it is slower to encode, and not every client decodes it cleanly. **x264 8-bit is a useful compatibility baseline.** The honest rule is not "always encode 8-bit" but "encode to match the client that will actually play it." Some devices cannot direct-play particular HEVC profiles or 10-bit video, so the server has to transcode. When in doubt, test one episode on the actual client before encoding a whole series.
- **Quality, not bitrate:** set a rate factor (RF) rather than a target bitrate. The RF scale runs the other way to normal — lower is better quality and bigger file. For 1080p the sweet spot is roughly **RF 20 to 22**; go to RF 18 if a film is grainy or you want the quality to survive a big screen, and up toward RF 24 if you genuinely cannot tell the difference.
- **Audio:** pass through the original track (DTS or AC3) when the player will handle it, or encode to AAC as a widely-compatible fallback. Passthrough avoids another lossy conversion, although lossless tracks such as DTS-HD and Dolby TrueHD can add substantially to file size. Keep them when their quality matters and the playback chain supports them.
- **Subtitles:** keep the English subtitles and any "forced" track (the bits that translate on-screen text). Drop the subtitles for languages you will not watch. If you watch a lot of anime or foreign films, prefer text subtitles — SRT or the richer ASS format anime fansubbing uses — over bitmap-based Blu-ray (PGS) or DVD (VobSub) ones. Those image-based tracks are the other common thing that forces a server transcode, because many clients will not render them natively.
- **Resolution and filters:** leave the resolution at the source — do not upscale a DVD and do not downscale a 1080p Blu-ray unless a specific player needs it. Skip the filtering unless there is a visible problem to fix; filters almost always cost more quality than they save.

The single most useful change is the RF value: it is the one knob that trades size for quality directly, and it is the reason a twenty-hour series can sit at a few gigabytes an episode instead of forty.

## The player matters more than the encode

All of these settings assume the device playing the file can actually decode it. This is where smart TVs can quietly undercut the whole setup. A television's apps run on the TV's own platform — such as VIDAA, Tizen or webOS — and are often less flexible than dedicated players. When the TV cannot play a codec or subtitle track, the media server has to transcode the film on the fly. CPU use rises, quality can drop, and the careful encode is undone at playback by a client that was not built for every format.

It is a mistake most people make once: optimising the encode while ignoring the player. The player is worth more than any codec choice. A dedicated media player — a small PC, an Android TV box, an Apple TV 4K, or something like an NVIDIA Shield — can support more formats directly, so the server is less likely to transcode. Capabilities still vary by model, app, codec, subtitle format and audio chain, so device names are less useful than testing the files that matter on the intended player.

For me the plan is simple: I own an older model of Shield anyway, and putting it back into service beats both the television's own app and another purchase. A dedicated player is the missing link between "a sensible encode" and "a server that does nothing but serve."

## The boundary I try to hold

The library answers one question — is this watchable at home? — and the disc answers another — is this preserved? I try not to let the library creep into doing the disc's job. A remux in the library is just a disc taking up space on a hard drive, one that is already on the shelf.

Restraint is not deprivation. It is the difference between a collection that serves the watching and a collection the watching serves. I would rather have a hundred films I chose, at a size I can live with, than a thousand I did not choose, at a size I have to keep paying for.