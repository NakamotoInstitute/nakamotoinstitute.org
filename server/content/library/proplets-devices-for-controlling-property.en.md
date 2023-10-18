---
title: "Proplets: Devices for Controlling Property"
authors:
  - nick-szabo
date: 2001
categories:
  - cryptography
  - property
doctype: essay
external: http://web.archive.org/web/20160806221938/http://szabo.best.vwh.net/proplets.html
---

Civilization has highly evolved practices for determining whether certain actions are allowable or not, or who should prevail in a dispute, namely law. Such a body of knowledge cannot be reinvented from scratch, so instead e-commerce security should draw heavily on it—building property rights, contract and tort law into technology at a very basic level. Proplets define the basic security architecture for local evidence gathering, enforcement, and negotiation of such laws.

Proplets do not rely on central planning, AI, or a single trusted third party for any function. Central planning is not able to account for the [distributed and diverse knowledge and preferences](http://www.virtualschool.edu/mon/Economics/HayekEconomicsAndKnowledge.html) of different people. A "trusted third party" is a nice-sounding synonym for a wide-open [security hole](/trusted-third-parties/) that a designer chooses to overlook. Proplet design places strong emphasis on eliminating such exposures.

The key is building in, at the most basic level of technology, code (in both the legal and software sense) that allows a widely distributed people, each person having his own unique information, circumstances, and preferences, to cooperate within well known, mutually agreeable, and strongly enforced constraints. With these constraints the risks and benefits of technology are balanced, weapons are monitored and securely restricted in their use to only very narrow, specific, lawful conditions, and for every person there is more profit from peace than from destruction.

The goal of proplet design is to control physical objects with digital protocols. Proplets protect its structure and function from non-owners, and observe the environment for phenomena impinging on a region, on matter, or on its owner. A proplet is an electromechanical device (e.g. a MEMS device) with the following core abilities:

- It knows who owns it
- It knows where it is in space and time
- It can communicate securely with nearby proplets, over a public network, and with its owner
- It contains a computer, called the ownership module, that is a secure extension of the owner's trusted computing base
- The ownership module securely exercises control over a machine via entanglement (explained below), or over nearby inanimate matter via sensors, effectors, public registration, and law.
- It can securely recognize nearby proplets owned by the same owner

A proplet may optionally also have the following abilities:

- It can cooperate with nearby proplets, especially those owned by the same owner or under contract with the owner. This can include the manufacture of larger structures and machinery.
- Guest computation modules—extensions of the trusted computing base of a non-owner of the proplet for purposes of rapid protocol communications. The guest can store proprietary data and programs on the proplet in his guest modules where they are inaccessible to the owner, except through services designed by the guest. The guest modules also can locally execute [smart contracts](/the-idea-of-smart-contracts/) with the owner.
- Deed modules—these operate the smart contracts, or deeds, created by previous owners to bind future owners.

No computational module can be read or controlled by physical tampering—it will shut down, erase itself, or even self-destruct depending on the severity of tampering. Computational modules are "transparent" to their publically registered controller and opaque to other entities.

Only protocols that are simple and composable with provable security govern the communications between the security kernel (private key operations), control box, sandbox, and other components of a computation modules. Similarly for communications between modules and between proplets.

<figure>
  <img src="/img/library/proplets-devices-for-controlling-property/proplet.gif" alt="" />
<figure>

How does a proplet find out who owns it, or a guest module who controls it? There are two basic ways:

- It looks up the public key of its current owner or guest in a public [title registry](/secure-property-titles/), and follows instructions signed with the corresponding private key, or
- It follows instructions signed by the private key held by home proplets. Home proplets live on or inside the owner or guest. Transfer of remote proplets (or guest modules) occur with the transfer of the home proplets that govern the remotes.

A proplet's guest modules are publicly listed and transferred independently of each other and of the proplet's ownership module.

With the home proplet alternative, biometric control of the home proplets may replace public ownership records.

<figure>
  <img src="/img/library/proplets-devices-for-controlling-property/propletsystem.gif" alt="" />
</figure>

Proplets control electronics directly from ownership or guest modules. Proplets control machinery via entanglement. Entanglement can take at least two forms:

- Firing sequences, without which the machinery cannot work. (Digitally timed high performance automobile engines and nuclear explosives are two contemporary examples).
- Direct nanomechanical linkages.

Entanglment designs have in common that they make it too expensive for the attacker to steal the electronics or machinery by severing it from the controlling proplet.

## Tort

_Deeds_, in the context of replicated property titles and proplets, are smart contracts executed by a deed module. The current owner may add new deeds agreed to (but not remove old ones) by drafting signing and signing such a smart contract with other current property owners. The deed binds both properties (perhaps to different terms, depending on what the two current owners have negotiatied). The deed modules can be audited at any time by the contemporary owners of other proplets bound to the deeds. Founders of competing property title registries define master deeds, or tort laws, to govern disputes within registry properties. They also define tort law for disputes between their properties and properties defined by other registires, by coming to agreements with those registry founders. Founders also create the initial allocations.

Founders are often the manufacturers of proplets. They build in a particular registry as authoratative for their proplets as well as designing an accompanying tort law.

For example, the founder of registry of fixtures in a spatial region can sign an agreement with a movable property (chattel) registry, governing the behavior of chattel moving through space and interacting with fixtures. The manufacturers of chattel and fixtures program their proplets to respect the appropriate registries and constrain their sensors and effectors to follow the tort law that has been agreed to.

## Conclusion

Proplets combine our most highly evolved practices for cooperation on a large scale with a technology architecture suitable for advances well into the future, even well into posthuman civilization. Proplets provide a much sounder footing for solving the problems of high technology cooperation including problems such as privacy, weapons of mass destruction, and other abuses of the power of advanced technology.

## References

["Computer Security as the Future of Law"](http://www.caplet.com/security/futurelaw/index.htm), Mark Miller\
["Formalizing and Securing Relationships on Public Networks"](/formalizing-securing-relationships/), Nick Szabo\
["Secure Property Titles"](/secure-property-titles/), Nick Szabo

## Acknowledgements

My thanks to Gregory Burch, J.D. for his helpful questions.

---

Please send your comments to nszabo (at) law (dot) gwu (dot) edu
