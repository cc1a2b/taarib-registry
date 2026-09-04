# taarib-registry

The public catalogue [Taarib](https://github.com/cc1a2b/taarib) reads. It is a
repository of static JSON and release assets — no server, no database, no API.
A client resolves it over `raw.githubusercontent.com`, over a CDN mirror of this
same repository, or out of a directory copied onto a disk; none of the three is
privileged over the others, and `git clone` is a complete fork of the catalogue.

Nothing here is written by hand. The tree is cast by
`crates/taarib-mustawda/src/bin/sabk.rs` in the client repository, which derives
every listing field from the sealed package's own metadata, and the layout
contract it must satisfy is `docs/mustawda.md` there.

## Layout

```
bayan.json                     the manifest: schema, sequence, 256 shard hashes
sharaih/00.json … ff.json      the catalogue, split 256 ways; all of them, always
sahb/qaima.json                the revocation list, signed by the owner key
isdar/<patch-id>/<name>.ruqaa  the sealed packages, also attached to a release
```

A game falls in shard `blake3(game-uuid)[0]`, so a client fetches the manifest
plus one shard per bucket its own library touches, and nothing else. Empty
shards are published too — 23 bytes each — because a client treats a shard that
does not resolve as a failure of the whole index fetch, not as an empty answer.

`bayan.json` carries the BLAKE3 of every shard's bytes. A shard is hashed against
that entry before a single record inside it is parsed, so index content that has
not been checked against the manifest cannot be read at all. `tasalsul` only ever
increases; a client that has seen a higher number refuses a lower one forever.

## Packages

Each `.ruqaa` is a signed container: metadata, the string table, and whatever
fonts the patch bundles. A listing's `basmat_muhtawa` is the BLAKE3 of the file,
verified while it downloads, and `musahim` is the contributor's public signing
key taken from the package's own signature block — a listing cannot claim an
identity its seal does not back.

Packages here are currently signed with Taarib's **development** key
(`e4260a5f…4cea`), which is committed in the client repository and protects
nothing. A release build of Taarib names that key and refuses it. The catalogue
will be re-signed when the release key exists.

## Licence

Catalogue metadata: CC0-1.0. Each package carries its own licence in its
metadata, and bundled fonts keep theirs.
