---
title: P2P Filename Integrity
authors:
  - nick-szabo
date: 2005
categories:
  - technology
  - property
doctype: essay
external: https://web.archive.org/web/20160514124505/http://szabo.best.vwh.net/nameintegrity.html
---

I propose a secure and fully decentralized directory for p2p networks. Such a directory will improve filename integrity and will provide reputational benefits to file creators and uploaders, addressing problems with [file pollution and poisoning](https://web.archive.org/web/20160514124505/http://p2pecon.berkeley.edu/pub/CWC-EC05.pdf) in p2p file sharing networks. The proposal is a variation on [secure property titles](/secure-property-titles/).

The directory is based on [Byzantine quorum systems](/library/quorum-systems/), or [similar](/advances-in-distributed-security/), and digital signatures to identify the original uploaders and namers ("owners") of files via (filename, file hash, file owner nym, logo, digital signature chain, endorsments) tuples. The owners also claim nyms and logos via (nym, digital signature chain) and (logo, digital signature chain) tuples. The directory replicates these tuples in a Byzantine fault-tolerant fashion. Every person who wants to upload original files can obtain a public/private keypair from the p2p software. They then create a new nym and logo and claim title to them by signing them and adding it to the nym and logo title database. Public keys are the ultimate identifiers of an entity; everything else is claimed as "property" by public keys.

Nym owners who upload a new file (i.e. a file that is not a bit-for-bit duplicate of a file already claimed) can at the same time name the file and claim the file hash, using the tuple above, and thereby become the owner of that file. (No legal ownership is implied here, but it's a fairly accurate metaphor, and the "property rights" are enforced by the Byzantine fault tolerance and digital signature).

A nym and icon represent a reputable entity (i.e., an entity whose reputation for accurately naming files is known, either to filtering software or the end user). The reputation that comes from owning a file benefits the owner, and benefits users by increasing the quality of naming.

Because of this reputational effect persons won't typically want to transfer their nyms to the keys of other persons. However, due to the finite life of keypairs we still want titles to be transferable from one key to another, as in other kinds of [secure property title system](/secure-property-titles/).

Note that this directory operates in parallel with the file propagation component of the p2p system. In some cases the file may propagate first, in some cases the name first, and a file isn't usable until both have propagated. How much delay in the directory information (beyond that of the file) is tolerable depends on the relative values placed by users and uploaders on propagation time, filename integrity, and owner reputation.

In addition to having owners, the "endorsments" field can be used by third parties who also want to vouch for the accuracy of a name in referring to the hashed file.

The resulting incentives on filename forgers, uploaders, etc. are very interesting and left as an exercise for the reader, as is a "reputation system" if automatic filtering is desired.
