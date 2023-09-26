---
title: RPOW - Reusable Proofs of Work
authors:
  - hal-finney
date: 2004-08-15
categories:
  - cryptography
doctype: email
external: http://cryptome.org/rpow.htm
---

<pre>
To: cypherpunks@al-qaeda.net
Subject: RPOW - Reusable Proofs of Work
Date: Sun, 15 Aug 2004 10:43:09 -0700 (PDT)
From: hal at finney dot org ("Hal Finney")
</pre>

I'd like to invite members of this list to try out my new hashcash-based server, [rpow.net](/finney/rpow/index.html).

This system receives hashcash as a Proof of Work (POW) token, and in exchange creates RSA-signed tokens which I call Reusable Proof of Work (RPOW) tokens. RPOWs can then be transferred from person to person and exchanged for new RPOWs at each step. Each RPOW or POW token can only be used once but since it gives birth to a new one, it is as though the same token can be handed from person to person.

Because RPOWs are only created from equal-value POWs or RPOWs, they are as rare and "valuable" as the hashcash that was used to create them. But they are reusable, unlike hashcash.

The new concept in the server is the security model. The RPOW server is running on a high-security processor card, the IBM 4758 Secure Cryptographic Coprocessor, validated to FIPS-140 level 4. This card has the capability to deliver a signed attestation of the software configuration on the board, which any (sufficiently motivated) user can verify against the published source code of the system. This lets everyone see that the system has no back doors and will only create RPOW tokens when supplied with POW/RPOW tokens of equal value.

This is what creates trust in RPOWs as actually embodying their claimed values, the knowledge that they were in fact created based on an equal value POW (hashcash) token.

I have a lot more information about the system at [rpow.net](/finney/rpow/index.html), along with downloadable source code. There is also a crude web interface which lets you exchange POWs for RPOWs without downloading the client.

This system is in early beta right now so I'd appreciate any feedback if anyone has a chance to try it out. Please keep in mind that if there are problems I may need to reload the server code, which will invalidate any RPOW tokens which people have previously created. So don't go too crazy hoarding up RPOWs quite yet.

Thanks very much -

Hal Finney
