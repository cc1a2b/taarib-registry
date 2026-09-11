# taarib-registry

<div align="center">

[![License](https://img.shields.io/badge/license-CC0--1.0-blue.svg)](LICENSE)
[![Manifest](https://img.shields.io/badge/manifest-sequence%202-B7410E)](bayan.json)
[![Patches](https://img.shields.io/badge/patches-1-lightgrey)](isdar)
[![Index](https://img.shields.io/badge/index-267%20translations-2b6cb0)](fahras/tarjamat.json)
[![Client](https://img.shields.io/badge/client-Taarib-orange?style=flat&logo=rust)](https://github.com/cc1a2b/Taarib)

**The public patch registry the Taarib client reads, and an index of every community Arabic game translation that could be verified at its source.**

*Static JSON, sealed packages, no server.*

[العربية](README.ar.md)

</div>

## About

**taarib-registry** is the data behind the "install an Arabic patch" button in
[Taarib](https://github.com/cc1a2b/Taarib). It is a Git repository of static
files and nothing else: a manifest, 256 index shards, a signed revocation list,
and the sealed `.ruqaa` packages those shards point at. The client resolves the
same layout from GitHub, from a CDN mirror of this repository, or from a
directory on disk, and none of the three is trusted more than the others,
because every byte the client acts on is checked against a hash or a signature
before it is parsed.

The repository also carries something the client does not read yet: `fahras/`,
a machine-readable index of Arabic translations of PC games made by fan teams
and individuals outside Taarib, with a link to where each one lives and the
facts its own page states. The registry hosts none of them. It is a map, not a
mirror.

Written and maintained by [cc1a2b](https://github.com/cc1a2b).

---

## Table of Contents

- [About](#about)
- [What is in the tree](#what-is-in-the-tree)
- [How the client reads it](#how-the-client-reads-it)
- [Sealing and revocation](#sealing-and-revocation)
- [The development key, plainly](#the-development-key-plainly)
- [The packages served](#the-packages-served)
- [The community translation index](#the-community-translation-index)
- [Using the registry](#using-the-registry)
- [Quick start](#quick-start)
- [Usage examples](#usage-examples)
- [Command reference](#command-reference)
- [Advanced usage](#advanced-usage)
- [Contributing](#contributing)
- [License](#license)
- [Support](#support)

---

## What is in the tree

```
bayan.json                       the manifest: schema, sequence, one BLAKE3 per shard
sharaih/00.json … ff.json        256 shards; all of them, always, empty ones included
sahb/qaima.json                  the revocation list, Ed25519-signed by the owner key
isdar/<lineage>/<slug>-r<n>.ruqaa the sealed packages; the same bytes are release assets
fahras/tarjamat.json             the community translation index (hand-verified, not cast)
fahras/mukhattat.json            its JSON Schema (draft 2020-12)
fahras/jadwal.py                 validates the index and renders the tables below
LICENSE                          CC0 1.0 with the publisher notice
```

Two kinds of file live here and they are made differently.

**Cast files** (`bayan.json`, `sharaih/`, `sahb/`, `isdar/`) are written by
`crates/taarib-mustawda/src/bin/sabk.rs` in the client repository. Nothing in
them is typed by hand: every listing field is read out of the package's own
sealed metadata, every shard is hashed as it is written, and the manifest is
nothing but the list of those hashes. Edit one byte of a shard and the client
refuses the whole shard, so the only way to change them is to re-run the
caster with the sequence number incremented. The layout contract is
`docs/mustawda.md` in the client repository.

**Curated files** (`fahras/`, this README, `LICENSE`) are written by a person.
The index is checked by `fahras/jadwal.py` against its schema, but its content
is what someone read on a page and wrote down, and it says so on every entry.

### Numbers, as of the last cast

| what | value |
| --- | --- |
| manifest schema / sequence | 1 / 2, cast 2026-09-04T22:27:58Z |
| shards | 256; 255 are the 23-byte empty shard `{"ruqaa":{},"aswat":{}}`, shard `67` holds one listing |
| manifest size | 20 810 bytes, one 64-hex BLAKE3 per shard |
| revocation list | sequence 2, 323 bytes, 0 entries, valid until 2027-09-04 |
| packages | 1 lineage, revision 2, 44 976 bytes |
| signing key | the committed development key `e4260a5f…4cea` (see below) |
| index | 267 translations, 21 teams, checked 2026-09-11 |

---

## How the client reads it

Everything below is what `crates/taarib-mustawda` does; the sentences are
descriptions of code, not policy.

### Sources, in the order they are tried

The client's settings (`IdadatMasadir`) name three kinds of source, and
`silsilat_masadir` in the studio turns them into one chain:

1. **Local directories first** (`mahalliya`): any directory the user configured
   that holds a copy of this tree, whether a `git clone` on disk or a mounted
   network share. They cost nothing, work offline, and a user who configured one
   did so to be asked before the forge is. None are configured by default.
2. **The forge** (`rasmi`), default `https://github.com/cc1a2b/taarib-registry`.
3. **Mirrors** (`maraya`), default
   `https://cdn.jsdelivr.net/gh/cc1a2b/taarib-registry@main`.

A repository path such as `bayan.json` or `sharaih/67.json` is appended to each
root and fetched over `https` only; an `http` root is refused before a socket
opens, redirects are capped at three and may not downgrade, a body over 8 MiB is
cut off while it arrives, and a source that answers with anything other than
2xx loses its turn to the next one.

One consequence is worth stating because it is not obvious from the settings
screen. The default `rasmi` is the repository's *web page*, and GitHub answers
`https://github.com/cc1a2b/taarib-registry/bayan.json` with 404. The client
therefore moves on, and with default settings **every manifest and shard is
served by the jsDelivr mirror**; the forge entry only serves anything if it is
changed to the raw-content root
`https://raw.githubusercontent.com/cc1a2b/taarib-registry/main`. This was
verified with the client's own reader on 2026-09-11: the default `rasmi` alone
fails with "answered 404", the default pair succeeds from the mirror, and the
raw root succeeds from the forge. The catalogue is identical from all of them
because the manifest hash chain is what is trusted, not the host.

### The manifest and the rollback guard

`bayan.json` is parsed with `deny_unknown_fields`; a field this build does not
know is a corrupt manifest, not a forward-compatible extension. Its `tasalsul`
only ever increases. The client passes the sequence it last accepted into the
parser, and a manifest below it is refused as a rollback (`TasalsulLilkhalf`).
A user whose client has seen sequence 2 will refuse sequence 1 forever, which
is why every publication, including one that only swaps a release asset, must
increment it.

### Which shards, and why all 256 exist

A game's shard is the first byte of the BLAKE3 of its identity, and the identity
is a UUIDv5 over `steam:<appid>` and the normalized title
(`LubaId::min_masdar`). R.E.P.O. (Steam 3241660) hashes to
`9034a136-69b8-5ca2-a603-8b000f600abd`, whose first hash byte is `0x67`, so its
listing sits in `sharaih/67.json` and nowhere else. The client fetches the
manifest plus one shard per distinct bucket its own library touches, at most
six at a time, and never the whole catalogue.

A shard that does not resolve is treated as a failure of the whole index fetch,
not as an empty answer, because an unreachable shard and a missing one look the
same over the wire. That is why all 256 are published even when 255 are empty:
a young catalogue that published only its non-empty shards would show nothing
at all to every user whose games fall in the other buckets.

### Hash-before-parse and the cache

Shard bytes become a `ShareehaMuwaththaqa` only through one constructor, which
hashes them and compares the hash to the manifest's entry before parsing a
single record. There is no other way to obtain one, so unverified index content
cannot be represented in the client, let alone read. Verified shards are cached
under the client's data directory at `makhbaa/mustawda/sharaih/`; on the next
refresh a cached shard whose hash still matches the manifest is read from disk
and never requested, so an unchanged catalogue costs one manifest fetch and
zero shard fetches. The background refresh runs every 180 minutes by default,
and `wadaa_ghayr_muttasil` turns the network off entirely for people who want
that guarantee, leaving local directories as the only sources.

### Release assets

A listing carries two absolute `https` addresses, `rabt` and `rabt_mira`, the
package size, and the BLAKE3 of the package file. The downloader refuses any
address that is not `https`, longer than 2048 bytes, or carrying a control
character before it opens a socket; it resumes a cut transfer with
`Range: bytes=<n>-` and restarts from zero if the server ignores the range; it
fails over to the mirror at the same offset; and it hashes the bytes as they
arrive, so a package that does not match its listing is discarded before it is
ever opened. For the one package here the primary is a GitHub release asset
(`nashr-2`) and the mirror is the same file inside this tree served by jsDelivr
at the `nashr-2` tag.

### Install

A downloaded package goes through the same path an imported file or a LAN copy
does: quarantine, then the pre-install gate in `taarib-aman` (signature under
the build's trust anchor, revocation list, anti-cheat and multiplayer evidence,
integrity), which mints the permit `taarib-tathbeet` requires. Restore is
byte-for-byte; the verification walk in `docs/mustawda.md` restored 208 files
and 1 492 605 039 bytes identical to the pristine copy.

---

## Sealing and revocation

Every `.ruqaa` is signed with Ed25519 over its content hash, and the signer's
public key is written into the package's own signature block. A listing's
`musahim` field is that key, not a name typed by whoever published it, so a
listing cannot claim an identity its seal does not back. Verification uses
`verify_strict`, which refuses the small-order and non-canonical keys a
permissive check would accept.

Two trust anchors exist and they are structurally different builds. A release
build of the client is compiled with `TAARIB_MIFTAH_ISDAR` set to the owner's
release public key; a development build is compiled without it and anchors to
the committed development key. Each build trusts its own anchor and no other,
and a release build refuses the development key **by name**
(`SababTawqee::TawqeeTatwir`) rather than treating it as merely unknown.

`sahb/qaima.json` is the kill switch. It can revoke a signing key, a patch
lineage, or one content hash, each with a reason and a timestamp; it is signed
by the owner key over a canonical byte form (`taarib.qaimat-sahb.v1\0` followed
by length-prefixed fields in `BTreeMap` order), it carries its own sequence with
the same rollback rule as the manifest, and it expires one year after the cast
so that a registry nobody has re-signed in a year reports itself as exactly
that. The client fetches it from the same source chain, verifies it before
returning it, and records every refresh outcome beside the cache, so an empty
list is never mistaken for "nothing is revoked" when it means "nobody asked".
On 2026-09-11 the live list verified under the development key, its sequence
equalled the manifest's, the publishing key was not on it, one flipped byte of
the signature was refused, and the same bytes under a different owner key were
refused.

---

## The development key, plainly

**Everything here is sealed under Taarib's development key.** Its public half
is `e4260a5f02029a64b6a41a31a5db53e0af74d6110122d9a352a721a2438b4cea`, it is
committed in the client repository as `MIFTAH_TATWIR`, and its private half sits
in a developer keychain that protects nothing. The revocation list is signed
with the same key, which is the only sense in which anything here is
"owner-signed" today.

What that means for you:

- **A downloaded release build of Taarib refuses every package in this registry,
  by design.** It names the key and says so; this is the intended behaviour and
  not a bug to work around.
- **A build compiled without `TAARIB_MIFTAH_ISDAR` accepts them.** That is the
  development build, and the library screen draws the band "Development build —
  trusts the published development key, not the release key" the whole time.

The release signing key has not been minted. `docs/mustawda.md` §7.1 in the
client repository describes the tool that mints it, on the owner's machine,
into the platform keychain, writing only the public half to a file. When that
happens, every package and the revocation list here will be re-sealed and
republished under a new sequence, and the old ones will become uninstallable on
release builds, which is the property that makes the anchor worth anything.
Nothing in this repository will ever contain a private key, and no second
signing path exists or may be added.

---

## The packages served

One lineage, `01a06d42-dc5d-74b2-b27d-5c4441a03a3f`, for **R.E.P.O.** (Steam
3241660, build `23363152`, Unity 2022, Mono), listed as "REPO — Arabic".

| revision | bytes | BLAKE3 | declared method | state |
| --- | --- | --- | --- | --- |
| r1 | 45 472 | `fac7dfa2…2f0a` | `bashariya_kamila` — "fully human translation" | **withdrawn** 2026-09-04 (commit `c543ae1`), release deleted |
| r2 | 44 976 | `75ee52cc…4003` | `aaliya_faqat` — "machine only, unreviewed" | served: `nashr-2` asset and `isdar/…/r-e-p-o-r2.ruqaa` |

The honest thing to say about this patch is that it exists to prove the
transport, not to be played. Its 90 strings are machine drafts that no reviewer
has approved (`musawwada: 90, muakkada: 0`), no capture session ever recorded
the game's opening so first-hour coverage was never measured, and its own
coverage gate says `qabila_lil_nashr: false`. r1 nonetheless declared
`tareeqa: bashariya_kamila` under the contributor name "haqiqi walk", a name
that appears in no source, fixture or record. That declaration lives inside the
sealed metadata, so correcting it meant a re-seal, not an edit: r2 declares
`aaliya_faqat`, names the development key as the contributor, and crops the
glyph atlas from 4096×4096 to 4096×128 (the same 315 glyphs, 16 MiB less to
allocate). r1 was removed from the tree and its release withdrawn in the same
publication. Neither sealed file has been altered since; a package is never
edited in place, only superseded.

The listing's `rukhsa` is CC0, `aila: unity`, `khalfiya: mono`, `tabaqa: kamil`
(full static tier), and its binding is the launcher build id
`steam-3241660-build-23363152` plus one content fingerprint, which is what
`mutabaqa` matches an installed copy against.

Files that are **not** here, on purpose: the test fixtures the client's own
walks produce (`khayal-saif`, `mithal`, `mutanakkir`, the `taarib_fath_*`
directories, the 624-byte stubs a restore harness seals under a throwaway
key), and the uncompressed working copy the installer places beside a game.
None of them is a translation of anything.

## Publication overrides

The caster refuses a package whose own coverage verdict is `false` unless the
operator writes a sentence explaining why it is published anyway, and that
sentence is written into `bayan.json` as a `tajawuzat` entry naming the
lineage, the exact revision, and the gate's own blocking causes verbatim. The
manifest currently carries one such entry, for r2, whose cause reads: "No
capture session recorded the opening of the game, so first-hour coverage was
never measured at all." No client surface shows this yet; the field is a
durable public record and nothing more.

---

## The community translation index

`fahras/tarjamat.json` answers a different question from the shards: not "what
can Taarib install" but "what Arabic translations of PC games exist at all, and
where". Taarib's own patches are structurally different (shaped through
HarfRust with no presentation forms, sealed, reviewed before publication,
revocable); most of what the index lists is file-replacement work by fan teams,
some of it excellent, some of it machine output, and the index does not grade
it. It records what each page says.

### What it is not

- It hosts nothing and redistributes nothing. Every entry is a link to the
  translation's own home and the facts stated there.
- It does not vouch for legality, quality, or safety. The `rukhsa` field is the
  licence **as the authors state it**; where a page states none, the entry says
  `ghayr_musarraha` and nothing is inferred. Most pages state none.
- It is not exhaustive, and it is not a leaderboard. Breadth and accuracy were
  the aim, not volume.

### Inclusion rule

An entry was added only if its `rabt` was fetched and read on the date in
`tahaqquq.waqt`, by one of the recorded means:

| `tahaqquq.tareeqa` | what was read |
| --- | --- |
| `safha` | the page itself, over HTTPS |
| `api_nexus` | Nexus Mods answers non-browser requests with 403, so its listings were read through Nexus's own v2 GraphQL API by game domain and mod id (`legacyModsByDomain`); the permissions block is not exposed there, so no Nexus entry claims a licence |
| `api_github` | the GitHub REST API: repository metadata, licence file, releases, README |
| `api_gamebanana` | GameBanana's `apiv11` profile record, which does carry the licence field |
| `api_thunderstore` | the community package list, plus the package page |

Games that only run on PC through emulation were left out (the Nintendo titles
on several teams' lists). Translations of *mods* rather than games, font-only
mods, and Nexus listings whose status is `removed`, `hidden` or `wastebinned`
were left out. Work that is distributed only through Discord, YouTube
descriptions, forum shortlinks or aggregator sites (AR Team's Metro Exodus and
Jedi: Fallen Order, the Civilization VI project, the Skyrim translations traded
over forums, the Hades and Sims 4 patches on host sites) was left out because no
authored page could be fetched to record facts from; the aggregators
muarrab.com, ta3reb.com, mahfda.com and free-wargamer.com were used to find
authors' pages and are not themselves indexed.

`arabiya_rasmiya` was filled from Steam's store API (`appdetails` supported
languages) on the day of the check, for every entry with a Steam app id that a
name-exact store search could confirm. Taarib hides its own arabization surface
for a game that ships official Arabic (`istibdal_lugha_rasmiya`), which is why
the field exists; a `naam` next to a fan patch does not make the patch
worthless, it means the game gained Arabic after or alongside it.

### The index

Generated from `fahras/tarjamat.json` by `python3 fahras/jadwal.py`. Dates are
the latest the page states; counts are downloads or Workshop subscribers as
shown that day.

<!-- fahras:start -->
**267** translations of **231** games from **21** teams plus individuals. 216 are free; 51 are sold or subscription-only. 54 state a human translation or credit named translators, 10 state machine translation in whole or in part, the rest do not say. Only 34 state any licence or terms of use. 7 target a game that Steam now lists with official Arabic.

<details>
<summary><strong>[Eternal Dream Arabization](https://etrdream.com/)</strong> — 81</summary>

| Game | Steam | Official Arabic | Author | Host | Coverage | Method | Technical form | Licence | Distribution | Status | Latest date | Checked |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [Afterimage](https://etrdream.com/game/afterimage/) | 1701520 | no | Eternal Dream Arabization; translation: Allen Wouka • Zojaj  | team site | not stated | human | file replacement, font | not stated | free | released | 2025-04-04 | 2026-09-11 |
| [AI LIMIT](https://etrdream.com/game/ai-limit/) | 2407270 | no | Eternal Dream Arabization; translation: Allen Wouka (كلها) | team site | not stated | human | file replacement, font | not stated | free | released | 2026-01-04 | 2026-09-11 |
| [AM2R (Metroid 2 fan remake)](https://etrdream.com/game/am2r-metroid-2-fan-remake/) | — | ? | Eternal Dream Arabization | team site | not stated | not stated | file replacement, font | not stated | free | released | 2021-07-20 | 2026-09-11 |
| [Amnesia: The Bunker](https://etrdream.com/game/amnesia-the-bunker/) | 1944430 | no | Eternal Dream Arabization; translation: فهد العتيبي | team site | full | human | file replacement, font | not stated | free | released | 2025-10-23 | 2026-09-11 |
| [Armored Core VI: Fires of Rubicon](https://etrdream.com/game/armored-core-vi-fires-of-rubicon/) | 1888160 | no | Eternal Dream Arabization; translation: ‏Allen Wouka • منصور | team site | not stated | human | file replacement, font | not stated | free | released | 2024-08-25 | 2026-09-11 |
| [Bad North](https://etrdream.com/game/bad-north/) | 688420 | no | Eternal Dream Arabization; translation: مسدار | team site | not stated | human | file replacement, font | not stated | free | released | 2026-03-22 | 2026-09-11 |
| [Balatro](https://etrdream.com/game/balatro/) | 2379780 | no | Eternal Dream Arabization | team site | not stated | not stated | file replacement, font | not stated | free | released | 2025-06-03 | 2026-09-11 |
| [Blue Archive: Love is War](https://etrdream.com/game/blue-archive-love-is-war/) | — | ? | Eternal Dream Arabization | team site | not stated | not stated | file replacement, font | not stated | free | released | 2024-07-21 | 2026-09-11 |
| [Bokutachi wa Benkyou ga Dekinai (visual novel)](https://etrdream.com/game/bokutachi-wa-benkyou-ga-dekinai-visual-novel/) | — | ? | Eternal Dream Arabization; translation: Flkrin / فلكرين • SH | team site | not stated | human | file replacement, font | not stated | free | released | 2025-06-12 | 2026-09-11 |
| [Bright Memory](https://etrdream.com/game/bright-memory/) | 955050 | no | Eternal Dream Arabization | team site | not stated | not stated | file replacement, font | not stated | free | released | 2024-04-11 | 2026-09-11 |
| [Bright Memory: Infinite](https://etrdream.com/game/bright-memory-infinite/) | 1178830 | no | Eternal Dream Arabization | team site | not stated | not stated | file replacement, font | not stated | free | released | 2024-04-12 | 2026-09-11 |
| [Buckshot Roulette](https://etrdream.com/game/buckshot-roulette/) | 2835570 | no | Eternal Dream Arabization | team site | not stated | not stated | file replacement, font | not stated | free | released | 2026-03-28 | 2026-09-11 |
| [Call of the Sea](https://etrdream.com/game/call-of-the-sea/) | 1042490 | no | Eternal Dream Arabization | team site | not stated | not stated | file replacement, font | not stated | free | released | 2022-09-26 | 2026-09-11 |
| [Celeste](https://etrdream.com/game/celeste/) | 504230 | no | Eternal Dream Arabization | team site | not stated | not stated | file replacement, font | not stated | free | released | 2020-09-06 | 2026-09-11 |
| [Clair Obscur: Expedition 33](https://etrdream.com/game/clair-obscur-expedition-33/) | 1903340 | yes | Eternal Dream Arabization; translation: Allen Wouka • KevRan | team site | not stated | human | file replacement, font | not stated | free | released | 2026-02-14 | 2026-09-11 |
| [Code Vein](https://etrdream.com/game/code-vein/) | 678960 | no | Eternal Dream Arabization; translation: Allen Wouka • عبد ال | team site | not stated | human | file replacement, font | not stated | free | released | 2024-01-13 | 2026-09-11 |
| [Code Vein II](https://etrdream.com/game/code-vein-ii/) | 2362060 | no | Eternal Dream Arabization; translation: Allen Wouka (كل النص | team site | not stated | human | file replacement, font | not stated | free | released | 2026-03-26 | 2026-09-11 |
| [CRYMACHINA](https://etrdream.com/game/crymachina/) | 2258500 | no | Eternal Dream Arabization; translation: Allen Wouka (كلها، أ | team site | not stated | human | file replacement, font | not stated | free | released | 2026-05-29 | 2026-09-11 |
| [Cuphead](https://etrdream.com/game/cuphead/) | 268910 | no | Eternal Dream Arabization; translation: Allen Wouka | team site | full | human | file replacement, font | not stated | free | released | 2025-06-04 | 2026-09-11 |
| [Dark Souls II](https://etrdream.com/game/dark-souls-ii/) | 335300 | no | Eternal Dream Arabization | team site | not stated | not stated | file replacement, font | not stated | free | released | 2024-08-06 | 2026-09-11 |
| [Dark Souls III](https://etrdream.com/game/dark-souls-iii/) | 374320 | no | Eternal Dream Arabization | team site | full | not stated | file replacement, font | not stated | free | released | 2024-08-07 | 2026-09-11 |
| [Dark Souls: Remastered](https://etrdream.com/game/dark-souls-remastered/) | 570940 | no | Eternal Dream Arabization; translation: منصور • جين • The So | team site | not stated | human | file replacement, font | not stated | free | released | 2022-10-03 | 2026-09-11 |
| [DARQ: Complete Edition](https://etrdream.com/game/darq-complete-edition/) | 433550 | no | Eternal Dream Arabization | team site | not stated | not stated | file replacement, font | not stated | free | released | 2019-09-05 | 2026-09-11 |
| [Death's Door](https://etrdream.com/game/deaths-door/) | 894020 | no | Eternal Dream Arabization | team site | not stated | not stated | file replacement, font | not stated | free | released | 2026-03-22 | 2026-09-11 |
| [Deltarune (Chapter 1)](https://etrdream.com/game/deltarune/) | 1671210 | no | Eternal Dream Arabization; translation: السير مروان (المعرب  | team site | not stated | human | file replacement, font | not stated | free | released | 2024-12-24 | 2026-09-11 |
| [Doki Doki Literature Club](https://etrdream.com/game/doki-doki-litterature-club/) | 698780 | no | Eternal Dream Arabization; translation: Allen Wouka • MAZ •  | team site | not stated | human | file replacement, font | not stated | free | released | 2024-02-03 | 2026-09-11 |
| [Dolls Nest](https://etrdream.com/game/dolls-nest/) | 1839430 | no | Eternal Dream Arabization; translation: Tetetetetoris | team site | full | human | file replacement, font | not stated | free | released | 2025-10-16 | 2026-09-11 |
| [Elden Ring](https://etrdream.com/game/elden-ring/) | 1245620 | yes | Eternal Dream Arabization | team site | not stated | not stated | installer, file replacement | not stated | free | released | 2026-02-06 | 2026-09-11 |
| [Fate/stay night [Réalta Nua]](https://etrdream.com/game/fate-stay-night-realta-nua/) | — | ? | Eternal Dream Arabization | team site | not stated | not stated | file replacement, font | not stated | free | released | 2025-11-23 | 2026-09-11 |
| [FEZ](https://etrdream.com/game/fez/) | 224760 | no | Eternal Dream Arabization; translation: مسدار • Allen Wouka | team site | not stated | human | file replacement, font | not stated | free | released | 2026-01-01 | 2026-09-11 |
| [Getting Over It with Bennett Foddy](https://etrdream.com/game/getting-over-it/) | 240720 | no | Eternal Dream Arabization | team site | not stated | not stated | file replacement, font | not stated | free | released | 2020-08-26 | 2026-09-11 |
| [Guacamelee!](https://etrdream.com/game/guacamelee/) | 275390 | no | Eternal Dream Arabization | team site | not stated | not stated | file replacement, font | not stated | free | released | 2021-12-23 | 2026-09-11 |
| [Half-Life](https://etrdream.com/game/half-life/) | 70 | no | Eternal Dream Arabization; translation: Allen Wouka | team site | not stated | human | file replacement, font | not stated | free | released | 2026-03-23 | 2026-09-11 |
| [Half-Life 2](https://etrdream.com/game/half-life-2/) | 220 | no | Eternal Dream Arabization | team site | full | not stated | file replacement, font | not stated | free | released | 2026-07-15 | 2026-09-11 |
| [Hollow Knight](https://etrdream.com/game/hollow-knight/) | 367520 | no | Eternal Dream Arabization | team site | not stated | not stated | file replacement, font | not stated | free | released | 2026-07-27 | 2026-09-11 |
| [Hue](https://etrdream.com/game/hue/) | 383270 | no | Eternal Dream Arabization | team site | not stated | not stated | file replacement, font | not stated | free | released | 2024-02-07 | 2026-09-11 |
| [Hydra Castle Labyrinth](https://etrdream.com/game/hydra-castle-labyrinth/) | — | ? | Eternal Dream Arabization | team site | not stated | not stated | file replacement, font | not stated | free | released | 2026-03-27 | 2026-09-11 |
| [Junji Ito Maniac: An Infinite Gaol](https://etrdream.com/game/junji-ito-maniac-an-infinite-gaol/) | 3633250 | no | Eternal Dream Arabization; translation: KevRan | team site | not stated | human | file replacement, font | not stated | free | released | 2025-12-08 | 2026-09-11 |
| [Katana ZERO](https://etrdream.com/game/katana-zero/) | 460950 | no | Eternal Dream Arabization; translation: آسغور • الضوء • ‏All | team site | full | human | file replacement, font | not stated | free | released | 2025-04-19 | 2026-09-11 |
| [Kena: Bridge of Spirits](https://etrdream.com/game/kena-bridge-of-spirits/) | 1954200 | no | Eternal Dream Arabization; translation: AdamSaeed، و Striver | team site | not stated | human | file replacement, font | not stated | free | released | 2021-12-23 | 2026-09-11 |
| [Lethal Company](https://etrdream.com/game/lethal-company/) | 1966720 | no | Eternal Dream Arabization; translation: Allen Wouka | team site | not stated | human | BepInEx, font | not stated | free | released | 2025-04-04 | 2026-09-11 |
| [Little Witch Nobeta](https://etrdream.com/game/little-witch-nobeta/) | 1049890 | no | Eternal Dream Arabization; translation: ‏Allen Wouka • ‏Zoja | team site | not stated | human | file replacement, font | not stated | free | released | 2024-07-08 | 2026-09-11 |
| [Mark of the Ninja: Remastered](https://etrdream.com/game/mark-of-the-ninja-remastered/) | 860950 | no | Eternal Dream Arabization | team site | not stated | not stated | file replacement, font | not stated | free | released | 2026-06-17 | 2026-09-11 |
| [MOTORSLICE](https://etrdream.com/game/motorslice/) | 2830030 | no | Eternal Dream Arabization | team site | not stated | not stated | file replacement, font | not stated | free | released | 2026-05-31 | 2026-09-11 |
| [Mouthwashing](https://etrdream.com/game/mouthwashing/) | 2475490 | no | Eternal Dream Arabization; translation: KevRan • Stryker24hz | team site | not stated | human | file replacement, font | not stated | free | released | 2026-03-25 | 2026-09-11 |
| [NieR Replicant ver.1.22474487139...](https://etrdream.com/game/nier-replicant-ver-1-22474487139/) | 1113560 | no | Eternal Dream Arabization; translation: Allen Wouka • منصور | team site | not stated | human | file replacement, font | not stated | free | released | 2025-04-28 | 2026-09-11 |
| [NieR: Automata](https://etrdream.com/game/nier-automata/) | 524220 | no | Eternal Dream Arabization; translation: ‏Allen Wouka (كلها ب | team site | not stated | human | file replacement, font | not stated | free | released | 2024-07-12 | 2026-09-11 |
| [Ori and the Blind Forest](https://etrdream.com/game/ori-and-the-blind-forest/) | 387290 | no | Eternal Dream Arabization | team site | not stated | not stated | file replacement, font | not stated | free | released | 2019-09-09 | 2026-09-11 |
| [Pause Ahead](https://etrdream.com/game/pause-ahead/) | — | ? | Eternal Dream Arabization | team site | not stated | not stated | file replacement, font | not stated | free | released | 2019-01-01 | 2026-09-11 |
| [PEAK](https://etrdream.com/game/peak/) | 3527290 | no | Eternal Dream Arabization; translation: AdamSaeed • GinJehad | team site | not stated | human | BepInEx, font | not stated | free | released | 2026-03-25 | 2026-09-11 |
| [Pizza Tower](https://etrdream.com/game/pizza-tower/) | 2231450 | no | Eternal Dream Arabization | team site | not stated | not stated | file replacement, font | not stated | free | released | 2024-11-23 | 2026-09-11 |
| [R.E.P.O.](https://etrdream.com/game/r-e-p-o/) | 3241660 | no | Eternal Dream Arabization; translation: GINJEHAD • AdamSaeed | team site | full | human | BepInEx, font | not stated | free | released | 2025-06-22 | 2026-09-11 |
| [R.E.P.O.](https://thunderstore.io/c/repo/p/Eternal_Dream_Arabization/REPO_Arabic/) | 3241660 | no | Eternal_Dream_Arabization | Thunderstore | not stated | human | BepInEx, XUnity AutoTranslator | not stated | free | released | 2025-04-06 | 2026-09-11 |
| [Rise & Shine](https://etrdream.com/game/rise-and-shine/) | 347290 | no | Eternal Dream Arabization | team site | not stated | not stated | file replacement, font | not stated | free | released | 2021-08-15 | 2026-09-11 |
| [RoboCop: Rogue City](https://etrdream.com/game/robocop-rogue-city/) | 1681430 | no | Eternal Dream Arabization; translation: منصور، Allen Wouka،  | team site | not stated | human | file replacement, font | not stated | free | released | 2024-05-04 | 2026-09-11 |
| [ROKKO CHAN](https://etrdream.com/game/rokko-chan/) | — | ? | Eternal Dream Arabization | team site | full | not stated | file replacement, font | not stated | free | released | 2019-12-31 | 2026-09-11 |
| [Silent Hill 2 (2001, PC)](https://etrdream.com/game/silent-hill-2/) | 2124490 | no | Eternal Dream Arabization | team site | not stated | not stated | file replacement, font | not stated | free | released | 2024-06-09 | 2026-09-11 |
| [Silent Hill 2 (2024)](https://etrdream.com/game/silent-hill-2-2024/) | 2124490 | no | Eternal Dream Arabization; translation: AdamSaeed | team site | not stated | human | pak, font | not stated | free | released | 2025-02-03 | 2026-09-11 |
| [Silent Hill 3](https://etrdream.com/game/silent-hill-3/) | — | ? | Eternal Dream Arabization; translation: AdamSaeed • منصور •  | team site | not stated | human | file replacement, font | not stated | free | released | 2024-12-28 | 2026-09-11 |
| [Silent Hill 4: The Room](https://etrdream.com/game/silent-hill-4/) | — | ? | Eternal Dream Arabization; translation: AdamSaeed • منصور | team site | not stated | human | file replacement, font | not stated | free | released | 2026-08-16 | 2026-09-11 |
| [Silent Hill f](https://etrdream.com/game/silent-hill-f/) | 2947440 | no | Eternal Dream Arabization; translation: Allen Wouka | team site | not stated | human | file replacement, font | not stated | free | released | 2025-11-23 | 2026-09-11 |
| [SMT: Synchrocity](https://etrdream.com/game/smt-synchrocity/) | — | ? | Eternal Dream Arabization | team site | not stated | not stated | file replacement, font | not stated | free | released | 2020-08-13 | 2026-09-11 |
| [Snake Pass](https://etrdream.com/game/snake-pass/) | 544330 | no | Eternal Dream Arabization | team site | not stated | not stated | file replacement, font | not stated | free | released | 2021-09-17 | 2026-09-11 |
| [Snowbreak: Containment Zone](https://etrdream.com/game/snowbreak-containment-zone/) | 2668080 | no | Eternal Dream Arabization; translation: Allen Wouka • Desert | team site | not stated | human | file replacement, font | not stated | free | released | 2025-02-01 | 2026-09-11 |
| [Sonic Omens](https://etrdream.com/game/sonic-omens/) | — | ? | Eternal Dream Arabization | team site | not stated | not stated | file replacement, font | not stated | free | released | 2025-08-28 | 2026-09-11 |
| [Soulstice](https://etrdream.com/game/soulstice/) | 1602080 | no | Eternal Dream Arabization; translation: Allen Wouka | team site | not stated | human | file replacement, font | not stated | free | released | 2025-12-20 | 2026-09-11 |
| [Stellar Blade](https://etrdream.com/game/stellar-blade/) | 3489700 | yes | Eternal Dream Arabization; translation: Allen Wouka | team site | full | human | file replacement, font | not stated | free | released | 2026-02-28 | 2026-09-11 |
| [Stray](https://etrdream.com/game/stray/) | 1332010 | no | Eternal Dream Arabization | team site | not stated | not stated | file replacement, font | not stated | free | released | 2022-08-03 | 2026-09-11 |
| [The First Berserker: Khazan](https://etrdream.com/game/the-first-berserker-khazan/) | 2680010 | no | Eternal Dream Arabization; translation: KOBY | team site | not stated | human | file replacement, font | not stated | free | released | 2025-10-09 | 2026-09-11 |
| [The Last Faith](https://etrdream.com/game/the-last-faith/) | 1274600 | no | Eternal Dream Arabization; translation: KOBY • منصور • Majd  | team site | not stated | human | file replacement, font | not stated | free | released | 2026-02-25 | 2026-09-11 |
| [The Legend of Zelda: Twilight Princess (PC port)](https://etrdream.com/game/the-legend-of-zelda-twilight-princess/) | — | ? | Eternal Dream Arabization; translation: Allen Wouka (كامل ال | team site | not stated | human | file replacement, font | not stated | free | released | 2026-09-02 | 2026-09-11 |
| [Titan Souls](https://etrdream.com/game/titan-souls/) | 297130 | no | Eternal Dream Arabization | team site | not stated | not stated | file replacement, font | not stated | free | released | 2021-12-23 | 2026-09-11 |
| [Touhou Luna Nights](https://etrdream.com/game/touhou-luna-nights/) | 851100 | no | Eternal Dream Arabization; translation: Mega Hero | team site | full | human | file replacement, font | not stated | free | released | 2024-08-21 | 2026-09-11 |
| [Ultra Age](https://etrdream.com/game/ultra-age/) | 1683100 | no | Eternal Dream Arabization | team site | not stated | not stated | file replacement, font | not stated | free | released | 2026-03-29 | 2026-09-11 |
| [Wing of Darkness](https://etrdream.com/game/wing-of-darkness/) | 1179060 | no | Eternal Dream Arabization | team site | full | not stated | file replacement, font | not stated | free | released | 2024-07-11 | 2026-09-11 |
| [Wuchang: Fallen Feathers](https://etrdream.com/game/wuchang-fallen-feathers/) | 2277560 | no | Eternal Dream Arabization | team site | not stated | not stated | file replacement, font | not stated | free | released | 2025-08-24 | 2026-09-11 |
| [Wuthering Waves](https://etrdream.com/game/wuthering-waves/) | 3513350 | no | Eternal Dream Arabization | team site | full | not stated | file replacement, font | not stated | free | released | 2026-07-02 | 2026-09-11 |
| [Yoku's Island Express](https://etrdream.com/game/yokus-island-express/) | 334940 | no | Eternal Dream Arabization; translation: AdamSaeed، منصور | team site | not stated | human | file replacement, font | not stated | free | released | 2024-04-27 | 2026-09-11 |
| [Yume Nikki](https://etrdream.com/game/yume-nikki/) | 650700 | no | Eternal Dream Arabization; translation: MAZ | team site | not stated | human | file replacement, font | not stated | free | released | 2024-06-11 | 2026-09-11 |
| [YUMENIKKI -DREAM DIARY-](https://etrdream.com/game/yumenikki-dream-diary/) | 774811 | no | Eternal Dream Arabization | team site | not stated | not stated | file replacement, font | not stated | free | released | 2025-10-02 | 2026-09-11 |
| [Zelda: The Seeds of Darkness (fan game)](https://etrdream.com/game/zelda-the-seeds-of-darkness/) | — | ? | Eternal Dream Arabization | team site | not stated | not stated | file replacement, font | not stated | free | released | 2019-12-21 | 2026-09-11 |

</details>

<details>
<summary><strong>[Play in Arabic](https://www.playinarabic.com/fan)</strong> — 36</summary>

| Game | Steam | Official Arabic | Author | Host | Coverage | Method | Technical form | Licence | Distribution | Status | Latest date | Checked |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [007 First Light](https://www.playinarabic.com/translations/007-first-light) | 3768760 | no | Play in Arabic | team site | full | not stated | not stated | not stated | free | released | 2026-05-28 | 2026-09-11 |
| [Astroneer](https://www.playinarabic.com/translations/astroneer) | 361420 | no | Play in Arabic | team site | not stated | not stated | not stated | not stated | free | released | 2021-01-01 | 2026-09-11 |
| [Batman: Arkham Knight](https://www.playinarabic.com/translations/batman-arkham-knight) | 208650 | no | Play in Arabic | team site | not stated | not stated | not stated | not stated | paid | released | 2024-01-01 | 2026-09-11 |
| [Bendy and the Ink Machine](https://www.playinarabic.com/translations/bendy-and-the-ink-machine) | 622650 | no | Play in Arabic | team site | not stated | not stated | not stated | not stated | paid | released | 2025-05-30 | 2026-09-11 |
| [Crimson Desert](https://www.playinarabic.com/translations/crimson-desert) | 3321460 | yes | Play in Arabic | team site | full | not stated | not stated | not stated | paid | released | — | 2026-09-11 |
| [Ender Magnolia](https://www.playinarabic.com/translations/ender-magnolia) | — | ? | Play in Arabic | team site | not stated | not stated | not stated | not stated | paid | released | 2025-03-31 | 2026-09-11 |
| [FAMILY SECRETS 1 EMPTY PLATE](https://www.playinarabic.com/translations/family-secrets-1-empty-plate) | — | ? | Play in Arabic | team site | full | not stated | not stated | not stated | paid | released | 2026-08-06 | 2026-09-11 |
| [Fears To Fathom Carson](https://www.playinarabic.com/translations/fears-to-fathom-carson) | — | ? | Play in Arabic | team site | not stated | not stated | not stated | not stated | paid | released | 2025-05-30 | 2026-09-11 |
| [Fears to Fathom Ironbark](https://www.playinarabic.com/translations/fears-to-fathom-ironbark) | 1965810 | ? | Play in Arabic | team site | not stated | not stated | not stated | not stated | paid | released | 2025-05-30 | 2026-09-11 |
| [Fears To Fathom Norwood](https://www.playinarabic.com/translations/fears-to-fathom-norwood) | 1965810 | ? | Play in Arabic | team site | not stated | not stated | not stated | not stated | paid | released | 2025-04-28 | 2026-09-11 |
| [Fears to Fathom Scratch Creek](https://www.playinarabic.com/translations/fears-to-fathom-scratch-creek) | 4121170 | no | Play in Arabic | team site | full | not stated | not stated | not stated | paid | released | 2026-06-20 | 2026-09-11 |
| [Fears to Fathom Woodbury](https://www.playinarabic.com/translations/fears-to-fathom-woodbury) | 1965810 | ? | Play in Arabic | team site | not stated | not stated | not stated | not stated | paid | released | 2025-05-30 | 2026-09-11 |
| [GYLT](https://www.playinarabic.com/translations/gylt) | 2206210 | no | Play in Arabic | team site | not stated | not stated | not stated | not stated | free | released | 2023-01-01 | 2026-09-11 |
| [Heavy Rain](https://www.playinarabic.com/translations/heavy-rain) | 960910 | no | Play in Arabic | team site | full | not stated | not stated | not stated | paid | released | 2026-05-04 | 2026-09-11 |
| [Hollow knight silksong](https://www.playinarabic.com/translations/hollow-knight-silksong) | 1030300 | no | Play in Arabic | team site | not stated | not stated | not stated | not stated | paid | initial | 2025-09-20 | 2026-09-11 |
| [Hollow knight silksong (GAME PASS)](https://www.playinarabic.com/translations/hollow-knight-silksong-game-pass) | 1030300 | no | Play in Arabic | team site | not stated | not stated | not stated | not stated | paid | initial | 2025-09-20 | 2026-09-11 |
| [Karma The Dark World](https://www.playinarabic.com/translations/karma-the-dark-world) | 1376200 | no | Play in Arabic | team site | full | not stated | not stated | not stated | paid | released | 2025-08-18 | 2026-09-11 |
| [Life Is Strange Double Exposure](https://www.playinarabic.com/translations/life-is-strange-double-exposure) | 3122800 | ? | Play in Arabic | team site | not stated | not stated | not stated | not stated | paid | released | 2025-10-21 | 2026-09-11 |
| [Mafia The Old Country](https://www.playinarabic.com/translations/mafia-the-old-country) | 1941540 | no | Play in Arabic | team site | full | not stated | not stated | not stated | paid | released | 2025-08-15 | 2026-09-11 |
| [Mafia: The Old Country DLC](https://www.playinarabic.com/translations/mafia-the-old-country-dlc) | 4492700 | no | Play in Arabic | team site | full | not stated | not stated | not stated | paid | released | — | 2026-09-11 |
| [Red Dead Redemption](https://www.playinarabic.com/translations/red-dead-redemption) | 1174180 | no | Play in Arabic | team site | not stated | not stated | not stated | not stated | paid | released | 2024-01-01 | 2026-09-11 |
| [Remember Me](https://www.playinarabic.com/translations/remember-me) | 228300 | no | Play in Arabic | team site | not stated | not stated | not stated | not stated | free | released | 2023-01-01 | 2026-09-11 |
| [Silent Hill F](https://www.playinarabic.com/translations/silent-hill-f) | 2947440 | no | Play in Arabic | team site | not stated | not stated | not stated | not stated | paid | released | 2025-09-23 | 2026-09-11 |
| [Someday You WIll Return](https://www.playinarabic.com/translations/someday-you-will-return) | — | ? | Play in Arabic | team site | not stated | not stated | not stated | not stated | free | released | 2025-10-17 | 2026-09-11 |
| [Split Fiction](https://www.playinarabic.com/translations/split-fiction) | 2001120 | no | Play in Arabic | team site | not stated | not stated | not stated | not stated | paid | released | 2025-03-06 | 2026-09-11 |
| [Stardew Valley](https://www.playinarabic.com/translations/stardew-valley) | 413150 | no | Play in Arabic | team site | full | not stated | not stated | not stated | paid | released | 2026-01-21 | 2026-09-11 |
| [supraland](https://www.playinarabic.com/translations/supraland) | 813630 | no | Play in Arabic | team site | not stated | not stated | not stated | not stated | free | released | 2023-01-01 | 2026-09-11 |
| [Tales Beyond The Tomb - No Witnesses](https://www.playinarabic.com/translations/tales-beyond-the-tomb-no-witnesses) | 4483120 | no | Play in Arabic | team site | full | not stated | not stated | not stated | paid | released | 2026-08-06 | 2026-09-11 |
| [Tales Beyond The Tomb - The Farm's Secret](https://www.playinarabic.com/translations/the-farms-secret) | 3374720 | no | Play in Arabic | team site | full | not stated | not stated | not stated | paid | released | 2026-04-15 | 2026-09-11 |
| [Tales Beyond The Tomb : The Last Vigil](https://www.playinarabic.com/translations/tales-beyond-the-tomb-the-last-vigil) | 3416690 | no | Play in Arabic | team site | full | not stated | not stated | not stated | paid | released | 2026-06-23 | 2026-09-11 |
| [The Blood of Dawnwalker](https://www.playinarabic.com/translations/the-blood-of-dawnwalker) | 3751260 | no | Play in Arabic | team site | not stated | not stated | not stated | not stated | paid | initial | — | 2026-09-11 |
| [the cave](https://www.playinarabic.com/translations/the-cave) | 221810 | no | Play in Arabic | team site | not stated | not stated | not stated | not stated | free | released | 2022-01-01 | 2026-09-11 |
| [The First Berserker Khazan](https://www.playinarabic.com/translations/the-first-berserker-khazan) | 2676630 | ? | Play in Arabic | team site | not stated | not stated | not stated | not stated | paid | released | 2025-04-24 | 2026-09-11 |
| [The Last of Us 2](https://www.playinarabic.com/translations/the-last-of-us-2) | 2531310 | no | Play in Arabic | team site | dialogue | not stated | not stated | not stated | paid | released | 2025-08-06 | 2026-09-11 |
| [the room](https://www.playinarabic.com/translations/the-room) | 288160 | no | Play in Arabic | team site | not stated | not stated | not stated | not stated | free | released | 2021-01-01 | 2026-09-11 |
| [Valfaris](https://www.playinarabic.com/translations/valfaris) | 600130 | no | Play in Arabic | team site | not stated | not stated | not stated | not stated | free | released | 2022-01-01 | 2026-09-11 |

</details>

<details>
<summary><strong>[FLTAH VIP](https://www.fltah-translator.com/)</strong> — 24</summary>

| Game | Steam | Official Arabic | Author | Host | Coverage | Method | Technical form | Licence | Distribution | Status | Latest date | Checked |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [Alice: Madness Returns](https://www.fltah-translator.com/games/alice-madness-returns) | 19680 | no | FLTAH | team site | not stated | not stated | proprietary app | not stated | subscription | released | — | 2026-09-11 |
| [Bravely Default: Flying Fairy HD Remaster](https://www.fltah-translator.com/games/bravely-default-flying-fairy-hd-remaster) | 2833580 | no | FLTAH | team site | not stated | not stated | proprietary app | not stated | subscription | released | — | 2026-09-11 |
| [Cities: Skylines](https://www.fltah-translator.com/games/cities-skylines) | 255710 | no | FLTAH | team site | not stated | not stated | proprietary app | not stated | subscription | released | — | 2026-09-11 |
| [Creature Kitchen](https://www.fltah-translator.com/games/creature-kitchen) | 3097300 | no | FLTAH | team site | not stated | not stated | proprietary app | not stated | subscription | released | — | 2026-09-11 |
| [Dishonored](https://www.fltah-translator.com/games/dishonored) | 205100 | no | FLTAH | team site | not stated | not stated | proprietary app | not stated | subscription | released | — | 2026-09-11 |
| [Fairy Tail 2](https://www.fltah-translator.com/games/fairy-tail-2) | 3002850 | no | FLTAH | team site | not stated | not stated | proprietary app | not stated | subscription | released | — | 2026-09-11 |
| [Fields of Mistria](https://www.fltah-translator.com/games/fields-of-mistria) | 2142790 | no | FLTAH | team site | not stated | not stated | proprietary app | not stated | subscription | released | — | 2026-09-11 |
| [Final Fantasy XII: The Zodiac Age](https://www.fltah-translator.com/games/final-fantasy-xii-the-zodiac-age) | 595520 | no | FLTAH | team site | not stated | not stated | proprietary app | not stated | subscription | released | — | 2026-09-11 |
| [Folklands](https://www.fltah-translator.com/games/folklands) | 2282890 | no | FLTAH | team site | not stated | not stated | proprietary app | not stated | subscription | released | — | 2026-09-11 |
| [Highway Police Simulator](https://www.fltah-translator.com/games/highway-police-simulator) | 2789130 | no | FLTAH | team site | not stated | not stated | proprietary app | not stated | subscription | released | — | 2026-09-11 |
| [Honeycomb: The World Beyond](https://www.fltah-translator.com/games/honeycomb-the-world-beyond) | 1510440 | no | FLTAH | team site | not stated | not stated | proprietary app | not stated | subscription | released | — | 2026-09-11 |
| [L.A. Noire](https://www.fltah-translator.com/games/la-noire) | 110800 | no | FLTAH | team site | not stated | not stated | proprietary app | not stated | subscription | released | — | 2026-09-11 |
| [Life is Strange](https://www.fltah-translator.com/games/life-is-strange) | — | ? | FLTAH | team site | not stated | not stated | proprietary app | not stated | subscription | released | — | 2026-09-11 |
| [Mad Max](https://www.fltah-translator.com/games/mad-max) | 234140 | no | FLTAH | team site | not stated | not stated | proprietary app | not stated | subscription | released | — | 2026-09-11 |
| [No Rest for the Wicked](https://www.fltah-translator.com/games/no-rest-for-the-wicked) | 1371980 | no | FLTAH | team site | not stated | not stated | proprietary app | not stated | subscription | released | — | 2026-09-11 |
| [Shantae: Half-Genie Hero](https://www.fltah-translator.com/games/shantae-half-genie-hero) | 253840 | no | FLTAH | team site | not stated | not stated | proprietary app | not stated | subscription | released | — | 2026-09-11 |
| [Sniper Elite 5](https://www.fltah-translator.com/games/sniper-elite-5) | 1029690 | no | FLTAH | team site | not stated | not stated | proprietary app | not stated | subscription | released | — | 2026-09-11 |
| [Star Wars Outlaws](https://www.fltah-translator.com/games/star-wars-outlaws) | 2842040 | no | FLTAH | team site | not stated | not stated | proprietary app | not stated | subscription | released | — | 2026-09-11 |
| [Stardew Valley](https://www.fltah-translator.com/games/stardew-valley) | 413150 | no | FLTAH | team site | not stated | not stated | proprietary app | not stated | subscription | released | — | 2026-09-11 |
| [The Crust](https://www.fltah-translator.com/games/the-crust) | 1465470 | no | FLTAH | team site | not stated | not stated | proprietary app | not stated | subscription | released | — | 2026-09-11 |
| [Visions of Mana](https://www.fltah-translator.com/games/visions-of-mana) | 2490990 | no | FLTAH | team site | not stated | not stated | proprietary app | not stated | subscription | released | — | 2026-09-11 |
| [Wanderburg](https://www.fltah-translator.com/games/wanderburg) | 3624140 | no | FLTAH | team site | not stated | not stated | proprietary app | not stated | subscription | released | — | 2026-09-11 |
| [Welcome to Elderfield](https://www.fltah-translator.com/games/welcome-to-elderfield) | 3195440 | no | FLTAH | team site | not stated | not stated | proprietary app | not stated | subscription | released | — | 2026-09-11 |
| [Yes, Your Grace: Snowfall](https://www.fltah-translator.com/games/yes-your-grace-snowfall) | — | ? | FLTAH | team site | not stated | not stated | proprietary app | not stated | subscription | released | — | 2026-09-11 |

</details>

<details>
<summary><strong>[Arabic_Hesham (HeshamLocalization)](https://arabichesham.com/)</strong> — 20</summary>

| Game | Steam | Official Arabic | Author | Host | Coverage | Method | Technical form | Licence | Distribution | Status | Latest date | Checked |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [007 First Light](https://www.nexusmods.com/007firstlight/mods/11) | 3768760 | no | HeshamLocalization | Nexus Mods | full | not stated | installer, font | not stated | free | released | 2026-06-15 | 2026-09-11 |
| [Absolum](https://www.nexusmods.com/absolum/mods/12) | 1904480 | no | HeshamLocalization | Nexus Mods | full | not stated | file replacement, font | not stated | free | released | 2026-08-17 | 2026-09-11 |
| [Blasphemous 2](https://www.nexusmods.com/blasphemous2/mods/22) | 2114740 | no | HeshamLocalization | Nexus Mods | full | not stated | file replacement, font | not stated | free | released | 2026-08-17 | 2026-09-11 |
| [Dishonored 2](https://github.com/7akeem0/Arabic_Hesham-Downloads/releases) | 403640 | no | Hesham | GitHub | not stated | not stated | not stated | not stated | free | released | 2026-09-06 | 2026-09-11 |
| [Final Fantasy VII](https://github.com/7akeem0/Arabic_Hesham-Downloads/releases) | 39140 | no | Hesham | GitHub | not stated | not stated | not stated | not stated | free | released | 2026-09-06 | 2026-09-11 |
| [Forza Horizon 6](https://www.nexusmods.com/forzahorizon6/mods/65) | 2483190 | no | HeshamLocalization | Nexus Mods | full | not stated | file replacement, font | not stated | free | released | 2026-07-30 | 2026-09-11 |
| [Hades II](https://www.nexusmods.com/hades2/mods/121) | 1145350 | no | HeshamLocalization | Nexus Mods | full | not stated | file replacement, font | not stated | free | released | 2026-06-04 | 2026-09-11 |
| [Halo: Campaign Evolved](https://www.nexusmods.com/halocampaignevolved/mods/27) | 2806050 | no | HeshamLocalization | Nexus Mods | full | not stated | file replacement, font | not stated | free | released | 2026-07-27 | 2026-09-11 |
| [Hollow Knight: Silksong](https://www.nexusmods.com/hollowknightsilksong/mods/1105) | 1030300 | no | HeshamLocalization | Nexus Mods | full | not stated | BepInEx, font, shaping/RTL | not stated | free | released | 2026-09-02 | 2026-09-11 |
| [Inscryption](https://www.nexusmods.com/inscryption/mods/5) | 1092790 | no | X7akeem (uploaded by HeshamLocalization) | Nexus Mods | full | not stated | file replacement, font | not stated | free | released | 2026-07-27 | 2026-09-11 |
| [Kingdom Come: Deliverance](https://www.nexusmods.com/kingdomcomedeliverance/mods/2339) | 379430 | no | HeshamLocalization | Nexus Mods | full | not stated | file replacement, font | not stated | free | released | 2026-08-24 | 2026-09-11 |
| [Kingdom Come: Deliverance II](https://www.nexusmods.com/kingdomcomedeliverance2/mods/3542) | 1771300 | no | HeshamLocalization | Nexus Mods | full | not stated | file replacement, font | not stated | free | released | 2026-08-24 | 2026-09-11 |
| [Metaphor: ReFantazio](https://www.nexusmods.com/metaphorrefantazio/mods/86) | 2679460 | no | HeshamLocalization | Nexus Mods | full | not stated | installer, font | not stated | free | released | 2026-06-28 | 2026-09-11 |
| [Mina the Hollower](https://www.nexusmods.com/minathehollower/mods/7) | 1875580 | no | HeshamLocalization | Nexus Mods | full | not stated | installer, font | not stated | free | released | 2026-07-09 | 2026-09-11 |
| [MOUSE: P.I. For Hire](https://www.nexusmods.com/mousepiforhire/mods/20) | 2416450 | no | X7akeem (uploaded by HeshamLocalization) | Nexus Mods | full | not stated | file replacement, font | not stated | free | released | 2026-08-03 | 2026-09-11 |
| [Outer Wilds (with Echoes of the Eye)](https://outerwildsmods.com/mods/outerwildsarabictranslation/) | 753640 | no | Hesham (7akeem0) | outerwildsmods.com | full | machine, human-reviewed | OWML, font | MIT | free | released | — | 2026-09-11 |
| [Slay the Spire 2](https://www.nexusmods.com/slaythespire2/mods/759) | 2868840 | no | X7akeem (uploaded by HeshamLocalization) | Nexus Mods | full | not stated | installer, font | not stated | free | released | 2026-05-03 | 2026-09-11 |
| [Tears of Metal](https://www.nexusmods.com/tearsofmetal/mods/2) | 1913120 | no | HeshamLocalization | Nexus Mods | full | not stated | file replacement, font | not stated | free | released | 2026-08-02 | 2026-09-11 |
| [The Outer Worlds 2](https://www.nexusmods.com/theouterworlds2/mods/102) | 1449110 | no | X7akeem (uploaded by HeshamLocalization) | Nexus Mods | full | not stated | file replacement, font | not stated | free | released | 2026-05-03 | 2026-09-11 |
| [Undertale](https://www.nexusmods.com/undertale/mods/39) | 391540 | no | HeshamLocalization | Nexus Mods | full | not stated | file replacement, font | not stated | free | initial | 2026-05-15 | 2026-09-11 |

</details>

<details>
<summary><strong>[OK SHOP SA](https://okshopsa.net/games)</strong> — 19</summary>

| Game | Steam | Official Arabic | Author | Host | Coverage | Method | Technical form | Licence | Distribution | Status | Latest date | Checked |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [Baldur's Gate 3](https://okshopsa.net/games/baldurs-gate-3-okshop) | 1086940 | no | OK SHOP | team site | full | not stated | installer, font | stated | free | released | 2026-08-27 | 2026-09-11 |
| [Crimson Desert](https://okshopsa.net/games/crimson-desert-okshop) | — | ? | OK SHOP | team site | full | not stated | installer, font, language slot | stated | free | released | 2026-08-05 | 2026-09-11 |
| [Fallout 4](https://okshopsa.net/games/fallout-4-okshop) | 377160 | no | OK SHOP | team site | full | not stated | installer, font | stated | free | released | 2026-08-05 | 2026-09-11 |
| [Fallout: New Vegas — Ultimate Edition](https://okshopsa.net/games/fallout-new-vegas-okshop) | — | ? | OK SHOP | team site | full | not stated | installer, font | stated | free | released | 2026-08-22 | 2026-09-11 |
| [Kingdom Come: Deliverance](https://okshopsa.net/games/kingdom-come-deliverance-okshop) | 379430 | no | OK SHOP | team site | full | machine, human-reviewed | installer, font, language slot | stated | free | released | 2026-08-27 | 2026-09-11 |
| [Kingdom Come: Deliverance II](https://okshopsa.net/games/kingdom-come-deliverance-2-okshop) | 1771300 | no | OK SHOP | team site | full | not stated | installer, font, language slot | stated | free | released | 2026-08-23 | 2026-09-11 |
| [Lords of the Fallen](https://okshopsa.net/games/lords-of-the-fallen-okshop) | 1501750 | no | OK SHOP | team site | full | machine, human-reviewed | installer, font | stated | free | released | 2026-08-23 | 2026-09-11 |
| [Mass Effect Legendary Edition](https://okshopsa.net/games/mass-effect-legendary-edition-okshop) | 1328670 | no | OK SHOP | team site | full | not stated | installer, font | stated | free | released | 2026-08-25 | 2026-09-11 |
| [Mortal Shell II](https://okshopsa.net/games/mortal-shell-ii-okshop) | 2584270 | no | OK SHOP | team site | full | not stated | installer, font, language slot | stated | free | released | 2026-08-26 | 2026-09-11 |
| [Palworld](https://okshopsa.net/games/palworld-okshop) | 1623730 | no | OK SHOP | team site | full | not stated | installer, font | stated | free | released | 2026-08-05 | 2026-09-11 |
| [Sekiro: Shadows Die Twice](https://okshopsa.net/games/sekiro-okshop) | — | ? | OK SHOP | team site | full | not stated | installer, font | stated | free | released | 2026-08-05 | 2026-09-11 |
| [Stardew Valley](https://okshopsa.net/games/stardew-valley-okshop) | 413150 | no | OK SHOP | team site | full | machine, human-reviewed | installer, font, language slot | stated | free | released | 2026-08-22 | 2026-09-11 |
| [Starfield](https://okshopsa.net/games/starfield-okshop) | 1716740 | no | OK SHOP | team site | full | not stated | installer, font, language slot | stated | free | released | 2026-08-11 | 2026-09-11 |
| [State of Decay 2](https://okshopsa.net/games/state-of-decay-2-okshop) | — | ? | OK SHOP | team site | full | not stated | installer, font | stated | free | released | 2026-08-25 | 2026-09-11 |
| [The Blood of Dawnwalker](https://okshopsa.net/games/the-blood-of-dawnwalker-okshop) | 3751260 | no | OK SHOP | team site | full | not stated | installer, font, language slot | stated | free | released | 2026-09-09 | 2026-09-11 |
| [The Elder Scrolls IV: Oblivion Remastered](https://okshopsa.net/games/oblivion-remastered-okshop) | 2623190 | no | OK SHOP | team site | full | not stated | installer, font, language slot | stated | free | released | 2026-08-05 | 2026-09-11 |
| [The Elder Scrolls V: Skyrim Special Edition](https://okshopsa.net/games/skyrim-special-edition-okshop) | 489830 | no | OK SHOP | team site | full | not stated | installer, font, language slot | stated | free | released | 2026-08-05 | 2026-09-11 |
| [Warhammer 40,000: Space Marine 2](https://okshopsa.net/games/space-marine-2-okshop) | 2183900 | no | OK SHOP | team site | full | not stated | installer, font | stated | free | released | 2026-08-05 | 2026-09-11 |
| [Wo Long: Fallen Dynasty](https://okshopsa.net/games/wo-long-fallen-dynasty-okshop) | 1448440 | no | OK SHOP | team site | full | not stated | installer, font | stated | free | released | 2026-08-26 | 2026-09-11 |

</details>

<details>
<summary><strong>[Arabic Subtitles (Amr Shaheen)](https://arb-sub.blogspot.com/)</strong> — 9</summary>

| Game | Steam | Official Arabic | Author | Host | Coverage | Method | Technical form | Licence | Distribution | Status | Latest date | Checked |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [A Plague Tale: Innocence](https://arb-sub.blogspot.com/2023/07/plague-tale-innocence.html) | 752590 | no | Amr Shaheen | blog | not stated | not stated | not stated | not stated | free | released | 2023-07-01 | 2026-09-11 |
| [Call of Duty: Black Ops](https://arb-sub.blogspot.com/2025/08/call-of-duty-black-ops.html) | 42700 | no | Amr Shaheen | blog | not stated | not stated | not stated | not stated | free | released | 2025-08-01 | 2026-09-11 |
| [Far Cry 3](https://arb-sub.blogspot.com/2023/07/far-cry-3.html) | 220240 | no | Amr Shaheen | blog | not stated | not stated | not stated | not stated | free | released | 2023-07-01 | 2026-09-11 |
| [Mafia II: Definitive Edition](https://arb-sub.blogspot.com/2023/04/mafia-2-definitive-edition.html) | 1030830 | no | Amr Shaheen | blog | not stated | not stated | not stated | not stated | free | released | 2023-04-01 | 2026-09-11 |
| [Mafia: Definitive Edition](https://arb-sub.blogspot.com/2023/08/mafia-definitive-edition.html) | 1030840 | no | Amr Shaheen | blog | not stated | not stated | not stated | not stated | free | released | 2023-08-01 | 2026-09-11 |
| [Prince of Persia: The Forgotten Sands](https://arb-sub.blogspot.com/2023/07/prince-of-persia-forgotten-sands.html) | 33320 | no | Amr Shaheen | blog | not stated | not stated | not stated | not stated | free | released | 2023-07-01 | 2026-09-11 |
| [Shady Part of Me](https://arb-sub.blogspot.com/2023/12/shady-part-of-me.html) | 1116580 | no | Amr Shaheen | blog | not stated | not stated | not stated | not stated | free | released | 2023-12-01 | 2026-09-11 |
| [Sifu](https://arb-sub.blogspot.com/2023/07/sifu.html) | 2138710 | no | Amr Shaheen | blog | not stated | not stated | not stated | not stated | free | released | 2023-07-01 | 2026-09-11 |
| [Total Overdose](https://arb-sub.blogspot.com/2023/12/total-overdose.html) | — | ? | Amr Shaheen | blog | not stated | not stated | not stated | not stated | free | released | 2023-12-01 | 2026-09-11 |

</details>

<details>
<summary><strong>[Ters](https://github.com/DiNaSoR/Tersreleases/releases)</strong> — 6</summary>

| Game | Steam | Official Arabic | Author | Host | Coverage | Method | Technical form | Licence | Distribution | Status | Latest date | Checked |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [Diablo](https://github.com/DiNaSoR/Tersreleases/releases/tag/diablo1) | — | ? | Ters | GitHub | not stated | not stated | file replacement, dub | not stated | free | released | 2026-09-09 | 2026-09-11 |
| [Diablo II](https://github.com/DiNaSoR/Tersreleases/releases/tag/diablo2) | — | ? | Ters | GitHub | not stated | not stated | file replacement, dub | not stated | free | released | 2026-09-11 | 2026-09-11 |
| [DragonSword Awakening](https://github.com/DiNaSoR/Tersreleases/releases/tag/DragonSwordAwakening) | 4570720 | no | Ters | GitHub | not stated | not stated | not stated | not stated | free | released | 2026-08-01 | 2026-09-11 |
| [Graveyard Keeper](https://github.com/DiNaSoR/Tersreleases/releases/tag/graveyardkeeper) | 599140 | no | Ters | GitHub | not stated | not stated | not stated | not stated | free | released | 2026-08-03 | 2026-09-11 |
| [Ninja Gaiden 4](https://github.com/DiNaSoR/Tersreleases/releases/tag/NinjaGaiden4) | 2627260 | no | Ters | GitHub | not stated | not stated | file replacement, dub | not stated | free | released | 2026-09-08 | 2026-09-11 |
| [The Blood of Dawnwalker](https://github.com/DiNaSoR/Tersreleases/releases/tag/TheBloodofDawnwalker) | 3751260 | no | Ters | GitHub | not stated | not stated | not stated | not stated | free | released | 2026-09-03 | 2026-09-11 |

</details>

<details>
<summary><strong>[Arab Valve (saudi305 / Turki Al Mutairi)](https://gamebanana.com/mods/601841)</strong> — 4</summary>

| Game | Steam | Official Arabic | Author | Host | Coverage | Method | Technical form | Licence | Distribution | Status | Latest date | Checked |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [Half-Life](https://gamebanana.com/wips/87752) | 70 | no | saudi305 | GameBanana | interface | not stated | file replacement | CC-BY-NC-ND-4.0 | free | in progress | 2024-09-12 | 2026-09-11 |
| [Half-Life 2](https://gamebanana.com/mods/601841) | 220 | no | saudi305 (Turki Al Mutairi) | GameBanana | partial | human | file replacement, installer | CC-BY-NC-ND-4.0 | free | released | 2025-06-20 | 2026-09-11 |
| [Half-Life 2: Lost Coast](https://gamebanana.com/mods/477069) | 340 | no | saudi305 and Osamaisgood | GameBanana | full | human | file replacement | CC-BY-NC-ND-4.0 | free | released | 2024-04-10 | 2026-09-11 |
| [Papers, Please](https://gamebanana.com/mods/682074) | 239030 | no | saudi305, Hjbiki, Nasrallah Issa (Papers Please Arabic team) | GameBanana | full | human | file replacement, font | CC-BY-NC-ND-4.0 | free | initial | 2026-06-01 | 2026-09-11 |

</details>

<details>
<summary><strong>[Games in Arabic](https://www.nexusmods.com/sekiro/mods/431)</strong> — 4</summary>

| Game | Steam | Official Arabic | Author | Host | Coverage | Method | Technical form | Licence | Distribution | Status | Latest date | Checked |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [Resident Evil 2 (2019)](https://www.nexusmods.com/residentevil22019/mods/540) | 883710 | yes | Games in Arabic (uploaded by GamesinArabic) | Nexus Mods | full | not stated | file replacement | not stated | free | released | 2020-08-27 | 2026-09-11 |
| [Resident Evil 3 (2020)](https://www.nexusmods.com/residentevil32020/mods/145) | 952060 | yes | Games in Arabic (uploaded by GamesinArabic) | Nexus Mods | full | not stated | file replacement | not stated | free | released | 2020-10-02 | 2026-09-11 |
| [Sekiro: Shadows Die Twice](https://www.nexusmods.com/sekiro/mods/431) | 814380 | no | Games in Arabic (uploaded by GamesinArabic) | Nexus Mods | full | not stated | file replacement | not stated | free | released | 2020-12-17 | 2026-09-11 |
| [The Medium](https://www.nexusmods.com/themedium/mods/5) | 1293160 | no | Games in Arabic (uploaded by GamesinArabic) | Nexus Mods | full | not stated | file replacement | not stated | free | released | 2022-03-09 | 2026-09-11 |

</details>

<details>
<summary><strong>[Azaam](https://steamcommunity.com/sharedfiles/filedetails/?id=3641916210)</strong> — 3</summary>

| Game | Steam | Official Arabic | Author | Host | Coverage | Method | Technical form | Licence | Distribution | Status | Latest date | Checked |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [Don't Starve](https://steamcommunity.com/sharedfiles/filedetails/?id=3704921982) | 219740 | no | Azaam | Steam Workshop | full | human | Workshop | not stated | free | released | 2026-04-11 | 2026-09-11 |
| [Don't Starve Together](https://steamcommunity.com/sharedfiles/filedetails/?id=3641916210) | 322330 | no | Azaam | Steam Workshop | interface | human | Workshop | stated | free | released | 2026-01-08 | 2026-09-11 |
| [Mortal Shell II](https://www.nexusmods.com/mortalshell2/mods/210) | 2584270 | no | Azaam1 | Nexus Mods | full | human | pak, font | not stated | free | released | 2026-09-05 | 2026-09-11 |

</details>

<details>
<summary><strong>[Arabization Horizons](https://www.arhorizons.com/Projects)</strong> — 2</summary>

| Game | Steam | Official Arabic | Author | Host | Coverage | Method | Technical form | Licence | Distribution | Status | Latest date | Checked |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [Lies of P: Overture](https://www.arhorizons.com/Projects/lies-of-p-overture) | 1627720 | no | Arabization Horizons | team site | not stated | not stated | not stated | not stated | free | released | — | 2026-09-11 |
| [Portal](https://www.nexusmods.com/portal/mods/47) | 400 | no | Arabization Horizons | Nexus Mods | full | not stated | file replacement, installer | stated | free | released | 2025-04-13 | 2026-09-11 |

</details>

<details>
<summary><strong>[Besofh](https://besofh.wordpress.com/)</strong> — 2</summary>

| Game | Steam | Official Arabic | Author | Host | Coverage | Method | Technical form | Licence | Distribution | Status | Latest date | Checked |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [Metal Gear Solid (1998)](https://besofh.wordpress.com/2025/12/21/%d8%a7%d9%84%d8%b9%d8%aa%d8%a7%d8%af-%d8%a7%d9%84%d9%85%d8%b9%d8%af%d9%86%d9%8a-%d8%a7%d9%84%d8%b5%d9%84%d8%a8/) | — | ? | Besofh | blog | not stated | not stated | not stated | not stated | free | released | 2025-12-21 | 2026-09-11 |
| [Resident Evil 3: Nemesis (1999)](https://besofh.wordpress.com/2026/09/10/%d8%a7%d9%84%d8%b4%d8%b1-%d8%a7%d9%84%d9%85%d9%82%d9%8a%d9%85-3-%d9%86%d9%85%d8%b3%d9%8a%d8%b3-1999-resident-evil-3-nemisis/) | 4249120 | no | Besofh | blog | not stated | not stated | not stated | not stated | free | released | 2026-09-10 | 2026-09-11 |

</details>

<details>
<summary><strong>[Rihla team](https://steamcommunity.com/sharedfiles/filedetails/?id=3300660739)</strong> — 2</summary>

| Game | Steam | Official Arabic | Author | Host | Coverage | Method | Technical form | Licence | Distribution | Status | Latest date | Checked |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [Mount & Blade II: Bannerlord](https://www.nexusmods.com/mountandblade2bannerlord/mods/7137) | 261550 | no | rihla team (uploaded by lub131) | Nexus Mods | full | machine, human-reviewed | file replacement | not stated | free | released | 2026-01-10 | 2026-09-11 |
| [Mount & Blade II: Bannerlord](https://steamcommunity.com/sharedfiles/filedetails/?id=3300660739) | 261550 | no | Rihla team with translator Abu Dahim | Steam Workshop | full | machine, human-reviewed | Workshop | not stated | free | released | 2024-07-31 | 2026-09-11 |

</details>

<details>
<summary><strong>[Aldebaran](https://aldebaran.moe/)</strong> — 1</summary>

| Game | Steam | Official Arabic | Author | Host | Coverage | Method | Technical form | Licence | Distribution | Status | Latest date | Checked |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [Steins;Gate](https://aldebaran.moe/) | 412830 | no | Aldebaran (translator Salman, programming Abu Uqba, founder  | team site | full | human | file replacement, font | not stated | free | released | 2026-09-11 | 2026-09-11 |

</details>

<details>
<summary><strong>[Al-Wakr](https://arraqim.github.io/alwakr/)</strong> — 1</summary>

| Game | Steam | Official Arabic | Author | Host | Coverage | Method | Technical form | Licence | Distribution | Status | Latest date | Checked |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [Yakuza 0](https://arraqim.github.io/alwakr/zero) | 638970 | no | Al-Wakr | team site | not stated | not stated | not stated | not stated | free | released | — | 2026-09-11 |

</details>

<details>
<summary><strong>[ArabVikings](https://thunderstore.io/c/valheim/p/ArabVikings/Arab_Viking/)</strong> — 1</summary>

| Game | Steam | Official Arabic | Author | Host | Coverage | Method | Technical form | Licence | Distribution | Status | Latest date | Checked |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [Valheim](https://thunderstore.io/c/valheim/p/ArabVikings/Arab_Viking/) | 892970 | no | ArabVikings | Thunderstore | interface | not stated | BepInEx, Jötunn | not stated | free | released | 2025-08-07 | 2026-09-11 |

</details>

<details>
<summary><strong>[Arab Football Manager (AFM)](https://arabfm.net/)</strong> — 1</summary>

| Game | Steam | Official Arabic | Author | Host | Coverage | Method | Technical form | Licence | Distribution | Status | Latest date | Checked |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [Football Manager (2018 to 2026 language files)](https://arabfm.net/) | — | ? | AFM community | team site | interface | not stated | file replacement | not stated | free | released | 2025-11-17 | 2026-09-11 |

</details>

<details>
<summary><strong>[Asmar Library](https://asmar-ar.com/)</strong> — 1</summary>

| Game | Steam | Official Arabic | Author | Host | Coverage | Method | Technical form | Licence | Distribution | Status | Latest date | Checked |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [Subnautica 2](https://asmar-ar.com/) | 1962700 | no | Asmar | team site | not stated | not stated | installer | not stated | free | released | — | 2026-09-11 |

</details>

<details>
<summary><strong>[Better Rimworlds](https://github.com/BetterRimworlds/Rimworld-Arabic)</strong> — 1</summary>

| Game | Steam | Official Arabic | Author | Host | Coverage | Method | Technical form | Licence | Distribution | Status | Latest date | Checked |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [RimWorld](https://steamcommunity.com/sharedfiles/filedetails/?id=3687785648) | 294100 | no | Better Rimworlds (Autonomo AI) | Steam Workshop | full | machine | file replacement | MIT | free | released | 2026-03-19 | 2026-09-11 |

</details>

<details>
<summary><strong>[Castle of Fear](https://castle-of-fear.itch.io/misaoarabic)</strong> — 1</summary>

| Game | Steam | Official Arabic | Author | Host | Coverage | Method | Technical form | Licence | Distribution | Status | Latest date | Checked |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [Misao](https://castle-of-fear.itch.io/misaoarabic) | 1043270 | ? | Castle of Fear | itch.io | full | human | file replacement | stated | free | released | 2024-02-12 | 2026-09-11 |

</details>

<details>
<summary><strong>[Redemption Team and Emad Adel](https://emadadeldev.github.io/rtea/)</strong> — 1</summary>

| Game | Steam | Official Arabic | Author | Host | Coverage | Method | Technical form | Licence | Distribution | Status | Latest date | Checked |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [Red Dead Redemption 2](https://github.com/emadadeldev/rtea/releases) | 1174180 | no | Emad Adel (Redemption Team) | GitHub | not stated | not stated | installer | not stated | free | released | 2026-09-11 | 2026-09-11 |

</details>

<details>
<summary><strong>Individuals and teams without a team page</strong> — 47</summary>

| Game | Steam | Official Arabic | Author | Host | Coverage | Method | Technical form | Licence | Distribution | Status | Latest date | Checked |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [Balatro](https://github.com/BloodyARZ/BALATRO-ARABIC) | 2379780 | no | BloodyARZ | GitHub | partial | not stated | file replacement | CC0-1.0 | free | initial | 2026-01-27 | 2026-09-11 |
| [Baldur's Gate 3](https://www.nexusmods.com/baldursgate3/mods/5732) | 1086940 | no | ahmadmot (uploaded by ahmadmotx) | Nexus Mods | not stated | not stated | pak | not stated | free | released | 2024-01-07 | 2026-09-11 |
| [Bears In Space](https://github.com/M7MD-Zz/Bears-In-Space-Arabic) | 1309620 | no | M7MD-XD | GitHub | full | not stated | not stated | stated | free | released | 2026-09-07 | 2026-09-11 |
| [Black Mesa](https://steamcommunity.com/sharedfiles/filedetails/?id=2893890254) | 362890 | no | Workshop author (unnamed on the page) | Steam Workshop | dialogue | not stated | Workshop | not stated | free | initial | 2022-11-26 | 2026-09-11 |
| [Black Myth: Wukong](https://www.nexusmods.com/blackmythwukong/mods/69) | 2358720 | no | AG GROUP (uploaded by Salehalmsmary209) | Nexus Mods | not stated | not stated | pak | not stated | free | released | 2024-08-23 | 2026-09-11 |
| [Bum Simulator](https://github.com/M7MD-Zz/Bum-Simulator-Arabic) | 855740 | no | M7MD-XD | GitHub | full | not stated | not stated | stated | free | released | 2026-09-07 | 2026-09-11 |
| [Car Mechanic Simulator 2018](https://steamcommunity.com/sharedfiles/filedetails/?id=1381898351) | 645630 | no | Saud Arishi (سعود عريشي) | Steam Workshop | interface | human | Workshop | not stated | free | released | 2018-05-09 | 2026-09-11 |
| [Cities: Skylines II](https://www.nexusmods.com/citiesskylines2/mods/195) | 949230 | no | algammal | Nexus Mods | not stated | not stated | file replacement | not stated | free | released | 2026-06-29 | 2026-09-11 |
| [Cities: Skylines II](https://www.nexusmods.com/citiesskylines2/mods/94) | 949230 | no | Feras (uploaded by Fras1z) | Nexus Mods | not stated | machine | file replacement | not stated | free | initial | 2023-12-23 | 2026-09-11 |
| [Clair Obscur: Expedition 33](https://www.nexusmods.com/clairobscurexpedition33/mods/258) | 1903340 | yes | Majood7 aka Sharky (uploaded by majood7) | Nexus Mods | dialogue | not stated | pak, font | not stated | free | released | 2025-06-23 | 2026-09-11 |
| [Command & Conquer: Red Alert 2 - Yuri's Revenge](https://gamebanana.com/mods/609752) | — | ? | ATAA SY | GameBanana | full | not stated | file replacement, font | CC-BY-NC-ND-4.0 | free | released | 2025-07-27 | 2026-09-11 |
| [Crimson Moon](https://github.com/faisalkindi/CrimsonMoon-Arabic) | 4317690 | no | Faisal Al-Kindi (faisalkindi / kindiboy) | GitHub | full | not stated | pak, font, installer | not stated | free | released | 2026-09-02 | 2026-09-11 |
| [Crusader Kings III](https://steamcommunity.com/sharedfiles/filedetails/?id=2235954743) | 1158310 | no | Volunteers (unnamed on the page) | Steam Workshop | partial | not stated | Workshop | not stated | free | released | 2020-09-22 | 2026-09-11 |
| [Crusader Kings III](https://steamcommunity.com/sharedfiles/filedetails/?id=2556621728) | 1158310 | no | x7amtoGamer and xRover | Steam Workshop | partial | not stated | Workshop | not stated | free | released | 2021-07-24 | 2026-09-11 |
| [Dark Souls III](https://www.nexusmods.com/darksouls3/mods/929) | 374320 | no | Arabic Bonfire (uploaded by mido23dz) | Nexus Mods | full | not stated | ModEngine2, file replacement | not stated | free | released | 2025-10-17 | 2026-09-11 |
| [Dawn of Man](https://steamcommunity.com/sharedfiles/filedetails/?id=1672618199) | 858810 | no | Workshop author (unnamed on the page) | Steam Workshop | partial | human | Workshop | not stated | free | released | 2019-03-03 | 2026-09-11 |
| [Endzone 2](https://www.nexusmods.com/endzone2/mods/1) | 2144640 | no | Shinigami3361 | Nexus Mods | full | not stated | file replacement | not stated | free | released | 2025-02-10 | 2026-09-11 |
| [Factorio](https://github.com/mosa8899/-factorio) | 427520 | no | mosa8899 | GitHub | not stated | not stated | not stated | not stated | free | released | 2025-07-05 | 2026-09-11 |
| [Fallout 4](https://www.nexusmods.com/fallout4/mods/74914) | 377160 | no | ar (uploaded by JXnQ8) | Nexus Mods | full | not stated | file replacement | not stated | free | released | 2023-09-22 | 2026-09-11 |
| [Friday Night Funkin'](https://gamebanana.com/mods/374192) | — | ? | Abdragon Z | GameBanana | not stated | not stated | not stated | CC-BY-NC-ND-4.0 | free | released | 2022-04-28 | 2026-09-11 |
| [Grand Theft Auto V](https://arabictrilogy.blogspot.com/2023/02/grand-theft-auto-v.html) | 271590 | no | Hamza Al-Hamoud (ArabicTrilogy) | blog | full | human | file replacement | not stated | free | released | 2024-01-29 | 2026-09-11 |
| [Grand Theft Auto V Enhanced](https://www.nexusmods.com/gta5enhanced/mods/1136) | 3240220 | no | Nasser262 (uploaded by n262n) | Nexus Mods | full | not stated | file replacement, font | not stated | free | released | 2026-07-21 | 2026-09-11 |
| [Hearts of Iron IV](https://steamcommunity.com/sharedfiles/filedetails/?id=3402098254) | 394360 | no | Workshop author (unnamed on the page) | Steam Workshop | full | machine | Workshop | not stated | free | discontinued | 2025-01-06 | 2026-09-11 |
| [Hearts of Iron IV](https://steamcommunity.com/sharedfiles/filedetails/?id=3599864223) | 394360 | no | Gamer Arabic - Hamid Bouide | Steam Workshop | full | not stated | Workshop | not stated | free | released | 2025-11-04 | 2026-09-11 |
| [Kingdom Come: Deliverance II](https://www.nexusmods.com/kingdomcomedeliverance2/mods/133) | 1771300 | no | ARAB translation (uploaded by AliMeftah) | Nexus Mods | full | not stated | file replacement | not stated | free | released | 2025-02-06 | 2026-09-11 |
| [Kingdom Come: Deliverance II](https://www.nexusmods.com/kingdomcomedeliverance2/mods/3432) | 1771300 | no | yazeed5112 | Nexus Mods | full | not stated | file replacement | not stated | free | initial | 2026-08-01 | 2026-09-11 |
| [Lethal Company](https://thunderstore.io/c/lethal-company/p/KaTaKuri/ArabicTranslationBykatakuri98/) | 1966720 | no | KaTaKuri | Thunderstore | interface | not stated | BepInEx | not stated | free | released | — | 2026-09-11 |
| [Lethal Company](https://thunderstore.io/c/lethal-company/p/OmarElBanna/ArabicLanguageSupportPlus/) | 1966720 | no | OmarElBanna | Thunderstore | not stated | not stated | BepInEx | not stated | free | released | — | 2026-09-11 |
| [Manor Lords](https://www.nexusmods.com/manorlords/mods/190) | 1363080 | no | Shinigami3361 | Nexus Mods | not stated | not stated | pak | not stated | free | released | 2025-02-11 | 2026-09-11 |
| [Metal Gear Solid V: The Phantom Pain](https://www.nexusmods.com/metalgearsolidvtpp/mods/2224) | 287700 | no | VHussain and Yazed0071 (uploaded by yazed0071) | Nexus Mods | full | not stated | file replacement | not stated | free | released | 2026-05-07 | 2026-09-11 |
| [Mount & Blade II: Bannerlord](https://www.nexusmods.com/mountandblade2bannerlord/mods/7906) | 261550 | no | abuda7mx | Nexus Mods | full | not stated | file replacement, font, dub | not stated | free | released | 2025-04-25 | 2026-09-11 |
| [My Hero Ultra Rumble](https://www.nexusmods.com/myheroultrarumble/mods/303) | 1607250 | no | 1MHR | Nexus Mods | full | not stated | pak, font | not stated | free | released | 2026-04-17 | 2026-09-11 |
| [OMORI](https://omar-ibn-al-khattab-plus.itch.io/omori) | 1150690 | no | Omar ibn al-Khattab plus | itch.io | not stated | not stated | file replacement | not stated | free | in progress | — | 2026-09-11 |
| [OneShot](https://github.com/MO1-O1/oneshot-ar) | 420530 | no | MO1-O1 | GitHub | partial | not stated | not stated | not stated | free | in progress | 2026-08-21 | 2026-09-11 |
| [Palworld](https://www.nexusmods.com/palworld/mods/4369) | 1623730 | no | iqcp1 | Nexus Mods | full | not stated | pak, font | not stated | free | released | 2026-07-30 | 2026-09-11 |
| [Persona 3 Reload](https://github.com/AboSami1s/P3R_AR/releases) | 2161700 | no | AboSami1s | GitHub | not stated | not stated | pak | not stated | free | released | 2026-08-28 | 2026-09-11 |
| [Pizza Tower](https://gamebanana.com/wips/90033) | 2231450 | no | Fares_127 and Karrartheuhh (continuation of the KayMaw / Man | GameBanana | full | not stated | file replacement | CC-BY-NC-ND-4.0 | free | released | 2025-10-08 | 2026-09-11 |
| [Project Zomboid](https://steamcommunity.com/sharedfiles/filedetails/?id=3751112547) | 108600 | no | SA7 | Steam Workshop | full | not stated | Workshop | not stated | free | released | 2026-06-24 | 2026-09-11 |
| [RimWorld (with DLC)](https://github.com/mosa8899/-RimWorld-DLC) | 294100 | no | mosa8899 | GitHub | not stated | not stated | not stated | not stated | free | released | 2024-12-07 | 2026-09-11 |
| [Startup Company](https://steamcommunity.com/sharedfiles/filedetails/?id=2181994709) | 606800 | no | Workshop author (unnamed on the page) | Steam Workshop | not stated | not stated | Workshop | not stated | free | released | 2020-07-29 | 2026-09-11 |
| [Terraria](https://steamcommunity.com/sharedfiles/filedetails/?id=3427983380) | 105600 | no | Workshop author (unnamed on the page) | Steam Workshop | not stated | not stated | Workshop | not stated | free | released | 2025-02-15 | 2026-09-11 |
| [The Adventures of Elliot: The Millennium Tales](https://www.nexusmods.com/theadventuresofelliotthemilleniumtales/mods/1) | 3483510 | no | kindiboy | Nexus Mods | full | human | installer, font | not stated | free | released | 2026-06-23 | 2026-09-11 |
| [The First Berserker: Khazan](https://www.nexusmods.com/thefirstberserkerkhazan/mods/16) | 2680010 | no | MSH (uploaded by mshfm) | Nexus Mods | full | not stated | pak | not stated | free | released | 2026-07-26 | 2026-09-11 |
| [The Invincible](https://www.nexusmods.com/theinvincible/mods/5) | 731040 | no | MSH (uploaded by mshfm) | Nexus Mods | full | not stated | file replacement | not stated | free | initial | 2025-04-04 | 2026-09-11 |
| [The Planet Crafter](https://github.com/ishak10123/The-Planet-Crafter-arabic-translation) | 1284190 | no | ishak10123 | GitHub | full | machine | BepInEx, font, shaping/RTL | not stated | free | released | 2026-06-21 | 2026-09-11 |
| [Victoria 3](https://steamcommunity.com/sharedfiles/filedetails/?id=2880200030) | 529340 | no | Workshop author (unnamed on the page) | Steam Workshop | partial | not stated | Workshop | not stated | free | initial | 2022-10-26 | 2026-09-11 |
| [Vintage Story](https://github.com/mosa8899/-Vintage-Story) | — | ? | mosa8899 | GitHub | partial | not stated | not stated | not stated | free | released | 2025-05-19 | 2026-09-11 |

</details>

<!-- fahras:end -->

### Related places that are not indexed

- **muarrab.com** and **ta3reb.com** catalogue Arabic patches (official and
  fan-made) and were the best leads to authors' pages; ta3reb hosts files
  without consistent attribution.
- **taaribat.blogspot.com** is an archive of the history of Arabic game
  localization, official and grey, from the disc era onward.
- **Miqbas** (`github.com/aboali-hub/Miqbas`) is an automatic translation tool
  for RPG Maker, Ren'Py, Unity and Unreal games that runs a model on the
  player's own GPU; it produces translations rather than being one.
- **t3reeb.games** covers console patches only.

---

## Using the registry

### With Taarib

Nothing to install: a fresh client already points here. Settings → Sources
holds the three lists described above; set the forge to the raw-content root if
you want GitHub itself rather than the mirror to serve the index, add a
directory under *local sources* to read a clone or a network share, and turn on
the offline mode to never touch the network.

### As a mirror or an offline copy

```bash
git clone https://github.com/cc1a2b/taarib-registry.git
```

A clone is a complete registry. Point Taarib at the directory and the same
manifest, shards, revocation list and packages resolve from disk; copy it onto a
share and every machine that mounts it reads the same thing. Nothing in the
tree is host-specific except the two absolute asset URLs in the listing, and the
package they name is also inside the clone at `isdar/`.

### System requirements

- Any static file host that serves the tree as-is and answers `Range` requests
  for the packages (GitHub's release CDN and jsDelivr both do).
- For the tooling in this README: `git`, `python3` (3.10+), and optionally the
  `jsonschema` package; for the caster, the client repository's pinned Rust
  toolchain.

---

## Quick start

```bash
# the manifest: schema, sequence, and one hash per shard
curl -s https://cdn.jsdelivr.net/gh/cc1a2b/taarib-registry@main/bayan.json | jq '{isdar, tasalsul, waqt, shards: (.sharaih|length)}'

# the one non-empty shard, and the game it is keyed on
curl -s https://cdn.jsdelivr.net/gh/cc1a2b/taarib-registry@main/sharaih/67.json | jq '.ruqaa | keys'

# check a shard against the manifest yourself (b3sum from the blake3 project)
curl -s https://cdn.jsdelivr.net/gh/cc1a2b/taarib-registry@main/sharaih/67.json | b3sum
curl -s https://cdn.jsdelivr.net/gh/cc1a2b/taarib-registry@main/bayan.json | jq -r '.sharaih["103"]'
```

The two hashes must be identical; `103` is `0x67` in decimal, the shard index
the manifest keys on.

---

## Usage examples

```bash
# read the index: every free, released translation with a Steam app id
jq -r '.tarjamat[] | select(.tawzee=="majjani" and .hala=="nashita" and .steam_appid) | "\(.steam_appid)\t\(.luba.ism)\t\(.rabt)"' fahras/tarjamat.json

# which indexed games now ship official Arabic on Steam
jq -r '.tarjamat[] | select(.arabiya_rasmiya.hala=="naam") | .luba.ism' fahras/tarjamat.json | sort -u

# the entries that state a licence, and what it is
jq -r '.tarjamat[] | select(.rukhsa.naw!="ghayr_musarraha") | "\(.luba.ism): \(.rukhsa.muarrif // .rukhsa.nass)"' fahras/tarjamat.json

# validate the index and regenerate the README tables
python3 fahras/jadwal.py

# verify the package file against its listing
b3sum isdar/01a06d42-dc5d-74b2-b27d-5c4441a03a3f/r-e-p-o-r2.ruqaa
jq -r '.ruqaa[][0].basmat_muhtawa' sharaih/67.json
```

---

## Command reference

The caster, run from the client repository with the owner's (today: the
development) key in the machine's keychain:

```
سبك — cast the registry from sealed packages

  sabk --jidhr <repo> --tasalsul <n> --asas <https://base/>
       [--mira <https://mirror/>] [--ism-miftah <keychain account>]
       [--huzma <file.ruqaa> --luba <game-uuid> --ism <title> [--tajawuz <why>]]...
       [--mulgha <64-hex key> --sabab <why>]...

  --jidhr       the repository working tree to write into (required)
  --tasalsul    the manifest sequence number; increment it every time
  --asas        base for release assets: {ism} for a forge's flat release area,
                {masar} for a repository path, neither to append the path
  --mira        an optional second address for the same assets
  --ism-miftah  the keychain account holding the signing key
  --huzma       a sealed package to publish, followed by its --luba and --ism
  --tajawuz     publish over the package's own coverage gate, giving the reason
  --mulgha      a signing key to revoke, followed by its --sabab
```

The index tooling, run from a clone of this repository:

```
python3 fahras/jadwal.py            validate fahras/tarjamat.json, rewrite both README tables
python3 fahras/jadwal.py --check    validate only; exit 1 on any problem
```

---

## Advanced usage

### Serving your own copy

Any directory server works as a mirror root because the tree needs no rewriting:
the reader appends `bayan.json`, `sharaih/<xx>.json` and the manifest's
repository-relative revocation path to whatever root it is given. Release
assets are the exception: listings carry absolute URLs, so a mirror that wants to
serve packages too either keeps the `isdar/` directory in place (as jsDelivr
does) or re-casts with `--asas` pointing at itself.

### Forking the catalogue

A fork is a `git clone` plus a key. Re-cast with your own signing key, point a
client's sources at your root, and your client trusts your catalogue and refuses
this one, exactly as a release build refuses the development key. There is no
central registry to register with.

### Verifying the tree with the client's own reader

The checks quoted in this README were run by a small harness that links the
client's crates and calls the same functions the product does: manifest and
rollback guard, all 256 shards through the hash-before-parse constructor, the
revocation list through its verifying constructor (including a flipped byte and
a wrong owner key), the package through the pre-install signature check under
both anchors, the game identity derivation, and the full fetch path
(`jalb_fahras`, `jalb_qaimat_sahb`, cache hit) through a local directory, a
network share, the raw forge root, the mirror, and the product's literal default
chain, plus both release-asset URLs hashed against the listing. Its source is
not part of this repository because it path-depends on the client's crates; the
numbers it produced are in the commit message that added the index.

---

## Contributing

**Patches.** A patch reaches this registry only through the owner's signature.
Build and seal it in Taarib, then submit it for review; the studio's submission
flow uses GitHub's device authorization and is a local handoff until the
operator provisions the OAuth client id and the staging release
(`docs/mustawda.md` §7.2). Until then, open an issue on this repository with the
package attached and its `luba` identity stated; the maintainer reviews it,
runs the caster, and publishes under a new sequence. Nothing is auto-published,
and nothing is published under a key other than the owner's.

**Index entries.** Open a pull request that edits `fahras/tarjamat.json` and
run `python3 fahras/jadwal.py` so the schema check passes and the tables are
regenerated. An entry needs the page it came from in `rabt`, the date you read
it in `tahaqquq.waqt`, and nothing the page does not state; leave `rukhsa` as
`ghayr_musarraha` rather than guessing. Corrections from the authors of an
indexed translation are taken as-is.

**Bug reports** about the reader, the caster or the layout belong in the
[client repository](https://github.com/cc1a2b/Taarib/issues).

---

## License

Catalogue metadata, the index, and this documentation are released under
**CC0 1.0 Universal**; the full text with the dedication notice is in
[LICENSE](LICENSE).

```
taarib-registry — public domain under CC0 1.0 Universal
Author and maintainer: cc1a2b
```

Each `.ruqaa` package declares its own licence in its metadata (the one served
today declares CC0) and that licence covers the translated text and nothing
else. Every translation the index links to remains under its own authors'
terms, whatever they are.

---

## Support

If the registry or the index is useful to you: star the repository, follow
[cc1a2b](https://github.com/cc1a2b), and share it with the translation teams it
lists so they can correct their own entries.

---

<div align="center">

**taarib-registry — the catalogue Taarib reads, and the map of what exists beside it.**

Built by [cc1a2b](https://github.com/cc1a2b).

</div>
