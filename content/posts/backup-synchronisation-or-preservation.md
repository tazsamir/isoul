---
title: "Backup, synchronisation or preservation?"
date: 2026-09-14T10:05:00+01:00
draft: false
description: "Three different jobs that are often confused in self-hosted setups."
tags: [backups, digital-preservation, self-hosting, homelab]
---

A copy of a file is not automatically a backup, and a backup is not automatically a preservation system. Self-hosting becomes much easier to reason about when these three jobs are kept separate.

## Synchronisation keeps copies convenient

Synchronisation keeps data available on more than one device. Syncthing is useful for this kind of direct device synchronisation, and it makes working files available where I need them.

But synchronisation also copies mistakes. If a file is deleted, corrupted or encrypted, that change may travel to the other copy. Synchronisation improves availability; it does not replace a backup.

## A backup gives you a recovery point

A backup is a separate copy that can take you back to an earlier state. It should be protected from the normal failure of the source and should be possible to restore without relying on memory.

For my homelab, that means thinking about:

- what data is included;
- how often it is copied;
- how long old versions are retained;
- whether credentials are protected;
- whether the backup is encrypted;
- whether the restore procedure has been tested.

Restic is useful for encrypted, verifiable backup jobs, but the tool alone does not create a complete backup strategy. The source paths, schedule, retention and restore test matter just as much.

## Preservation keeps meaning and access

Preservation is a longer-term job. It is not only about keeping bytes. It also means retaining enough context to understand what the files are, checking that they have not silently changed, using formats that remain practical to read, and keeping more than one recovery path.

For web material, a saved URL is not preservation. The page may change or disappear. Tools such as [ArchiveBox](https://github.com/ArchiveBox/ArchiveBox) can create local captures, while larger institutional workflows such as [Archivematica](https://www.archivematica.org/en/) show how preservation involves ingest, processing, metadata and access.

## A simple test

For each important item, ask three questions:

1. **Do I need it available on another device?** That is synchronisation.
2. **Do I need to recover an older version after loss or damage?** That is backup.
3. **Do I need to understand and access it years from now?** That is preservation.

The same file may need all three, but the design is different for each job.

## How this applies to my lab

The live data on TrueNAS-Normandy is the working copy. Replication to another system can provide another local recovery path, but it should not be treated as the only backup. Restic configuration backups protect the information needed to rebuild services, while service data and databases need their own explicit inclusion and restore plans.

The most important question is not “Where is the copy?” It is:

> Can I prove that I can find, understand and restore the thing I care about?

That is the difference between having copies and having a recovery system.
