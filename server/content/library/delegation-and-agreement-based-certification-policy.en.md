---
title: Delegation and Agreement Based Certification Policy
authors:
  - nick-szabo
date: 1997
doctype: essay
categories:
  - cryptography
external: https://web.archive.org/web/20161002031400/http://szabo.best.vwh.net/trust.html
---

In this article I discuss trust, delegation, and policy issues related to the [Simple Public Key Infrastructure](https://web.archive.org/web/20161002031400/http://www.clark.net/pub/cme/html/spki.html), Matt Blaze's [PolicyMaker](https://web.archive.org/web/20161002031400/ftp://research.att.com/dist/mab/policymaker.ps), and [PGP's Web of Trust](https://web.archive.org/web/20161002031400/http://www.pgp.com/). Some understanding of SPKI by the reader is assumed.

Whether trust is transitive, and whether it is a leap of faith to delegate, depends on who we are trusting with what. "Public key X is bound to Alice" is clearly different than "I trust Alice to certify public key Y is bound to Bob", not to mention trusting Alice to certify anybody, much less trusting Alice generally with anything. The lack of specificity in discussions about "trust" often ends up implying far more trust than is really needed to solve a problem, as well as far more than can be realistically expected on the global Internet.

But "I trust Alice to use authorization for service X only once" can be the same as "I trust Bob to use authorization service X only once", since the server can enforce the use-once policy regardless of who the user is, via maintaing an issued-but-unused certificates list. Whether trust is transitive depends only sometimes on who or what the person or object authorized is, but always on what we are trusting the person or object with.

For many, but by no means all, of the proposed uses of certificates, trust is not transitive. But these proposed uses are problematic for just this reason. As Bill Frantz well observes, non-delegation is difficult to enforce. Keeping track of who is using an authorization, and for what purpose, is not strongly enforceable and doesn't scale. On the other hand, if we worry only about whether or not an authorization gets used, how many times, and other factors controllable locally by the service provider, issuer, and/or verifier, these policies are strongly enforceable and scale well.

In commercial terminology, delegable authorization certificates act like bearer certificates. They authorize whatever object holds the certificate, regardless of that object's identity. I think this proactive method is a great way to go, but observe that we are not used to solving problems this way. We are used to solving problems in a reactive manner, by [blacklisting](/library/negative-reputations/), or hunting down and punishing, the perpetrator. Blacklisting is still a very useful technique with software; witness virus scanning and firewall blockading by port number. But as Bill Frantz points out, punishing software is silly.

I suggest a Byzantine, contract based paradigm based on that discussed in [Smart Contracts](https://web.archive.org/web/20161002031400/http://szabo.best.vwh.net/smart.contracts.2.html). Instead of giving "permission" to delegate, (which makes the mighty assumption that no one in the world is going to do anything unless I give them my permission!) assume that any entity (and, in particular, the beneficiary of an authorization) will do whatever it likes unless (a) it promises not to (or the specification promises that it won't), and (b) this promise is enforceable by the verifier, or at least non-performance on this promise is verifiable (there is an auditing scheme such that breaches of promise will become known). Policy management becomes agreement management. Agreements may be with bearer, in which case delegation-agnostic authorization certificates are fine, or with particular entities, in which case we also need [identity certificates](https://web.archive.org/web/20161002031400/http://www.clark.net/pub/cme/usenix.html). Assume as well that third parties will do whatever they like unless prevented. This is the pessimistic "Byzantine generals" assumption used in general distributed computation theory; it applies all the more when dealing in the security of distributed systems.

I will argue for this secure contractual paradigm and discuss combining authorization certificates with identity certificates. "Fraud", poorly defined in other security methodologies, is well defined in the contractual paradigm as being a breach of a specific agreement.

In some cases authorization policies are self-enforcing, and we can rely on bearer certificates. Otherwise, verification and enforcement rely on observation of the behavior of an object, often persistence of behavior across many authorizations to it. One method of facilitating this observation is via public key-object bindings. These bindings may be certified by some [authority](/library/distributing-authorities-and-verifying-their-claims/), but this is a weak (not self enforcing, and not even strongly verifiable) kind of authorization due to a variety of identification frauds: identity lending, identity theft, man-in-the-middle, etc. To be useful these bindings must be further associated with "reputation" information, via observing the persistence of behavior associated with the public key. With such bindings we can have non-bearer, or identified, certificates. We can then make authorizations which are non-delegable up to the non-delegability of the public key-object binding.

To partake of such a non-delegatory service one must hold not only an authorization certificate, but also an identity certificate. If either the specific authorization or the authentication via identity certificate fails, the authorization fails. This combination gives an identified authorization certificate. With identified certificates we've reduced a wide variety of possible delegation frauds down to identification fraud. Of course, solving the several varieties identification fraud is still difficult, but at least we've reduce a bunch of nebulous delegation problems down to a well-defined one. Besides the weakness of solutions to identification fraud, and the need to further bind to reputation information for identity to be useful, identity certificates also introduce a major source of confidentiality loss, especially due to traffic analysis. But many consider these prices worth paying due to the lack of bearer certificate solutions to security problems.

Non-bearer certificates require the verifier to have trustworthy verifications chains for the identity certificates of all entities to be verified, as well as the chain(s) for the particular authorization itself. The identification certificates cannot, as far as way know, ever be made as strongly secure as delegable authorizations.

In many situations we don't really care about delegation. If for example we are only interested in limiting the usage of a service or associated resources, the identity of the user is irrelevant. In these cases we can issue bearer certificates, usable N times. This is strongly enforceable via clearing lists, with no delegation problems.

I suggest the follow principles for determining when certificate chains should be automatically followed:

- "Trust" cast in narrow, very specific terms: "trust to specifically X"
- These specific terms converted into proactive, self-enforcing protocols when possible
- When a self-enforcing protocol is not possible, strong verification of these specific terms through unforgeable auditing trails and frequent verification checks should be instituted.
- Otherwise, the "chain of trust" is in computer security terms very weak, relying on ill-defined human trust and institutions rather than on the security properties of the software. The user interface should prominently make this known to the users, and allow the users to input their judgements regarding these people and institutions. Confusing human with computer security makes great deceptions possible.

More general application of the idea of using agreement to set policy can be found in [Smart Contracts](https://web.archive.org/web/20161002031400/http://szabo.best.vwh.net/smart.contracts.2.html).

---

## References

[Simple Public Key Infrastructure](https://web.archive.org/web/20161002031400/http://www.clark.net/pub/cme/html/spki.html)

Matt Blaze, [PolicyMaker](https://web.archive.org/web/20161002031400/ftp://research.att.com/dist/mab/policymaker.ps)

Carl Ellison, [Identity Without Certificate Authorities](https://web.archive.org/web/20161002031400/http://www.clark.net/pub/cme/usenix.html).

Nick Szabo, [Negative Reputations](/library/negative-reputations/)

Nick Szabo, [Smart Contracts](https://web.archive.org/web/20161002031400/http://szabo.best.vwh.net/smart.contracts.2.html)

---

Please send your comments to nszabo (at) law (dot) gwu (dot) edu
