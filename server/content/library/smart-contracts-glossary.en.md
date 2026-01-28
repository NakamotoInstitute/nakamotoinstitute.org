---
title: Smart Contracts Glossary
authors:
  - nick-szabo
date: 1995
display_date: Originally published in 1995
categories:
  - cryptography
  - economics
  - law
doctype: essay
external: http://web.archive.org/web/20160620184813/http://szabo.best.vwh.net/smart_contracts_glossary.html
---

<a name="agent"></a>_Agent_: A person or organization, usually represented by a true name or nym. Also, a computer program controlled by, and acting on behalf of, an agent. More generally, a combination of a nym with a persistent pattern of behavior, upon which can be based a reputation. Note that this differs from the legal and business definitions of "agent", but corresponds more closely to the economics and computer science uses of the term.

<a name="contract"></a>_Contract_: A set of agreements or promises between agents.

<a name="parties"></a>_Parties (aka Principals)_: Agents who have agreed to the contracting question.

<a name="thirdparties"></a>_Third Parties_: Agents who have not agreed to the contract in question.

<a name="performance"></a>_Performance_: Carrying out the promises specified in a contract.

<a name="contractualsecurity"></a>_Contractual Security_: A paradigm for making security arrangements between organizations, based on two claims: (1) the primary goal of inter-organization security is to protect and enforce the performance of contracts, and (2) where this goal is achieved, dependence on reputation, outside enforcement, and other factors for the secure performance of that organization's contracts is minimized.

<a name="contractualkeydistribution"></a>_Contractual Key Distribution_: a paradigm for distributing keys among individuals and organizations, in which the key distribution and certificate structure reflects the contractual arrangements between parties.

<a name="protocol"></a>_Protocol_: A sequence of messages between multiple agents.

<a name="smartcontract"></a>_Smart contract_: A set of promises, including protocols within which the parties perform on the other promises. The protocols are usually implemented with programs on a computer network, or in other forms of digital electronics, thus these contracts are "smarter" than their paper-based ancestors. No use of artificial intelligence is implied.

<a name="aliceandbob"></a>_Alice and Bob_: Our exemplar parties to a smart contract.

<a name="eve"></a>_Eve_: Our exemplar eavesdropper, whose objective is to find out valuable information about a contract and its performance without being a party to that contract.

<a name="mallet"></a>_Mallet_: Our exemplar active attacker. His objective might either be stealing something of value involved in the performance of a smart contract, or denying it to the parties to the contract. He might either be an economically rational agent, out for pure personal gain, or Byzantine, a worst-case attacker who inflicts the greatest possible damage on one or more of the parties regardless of personal loss.

<a name="mediator"></a>_Mediator_: A third party involved realtime in the protocols between smart contract parties, trusted with some of the contents and/or performance of that contract.

<a name="arbitrator"></a>_Arbitrator_: A third party trusted with some of the contents, and some of the history of performance, of a contract, and trusted by contracted parties to resolve disputes arising from that contract fairly.

<a name="unbundling"></a>_Unbundling_: The principle of distribution of trust. Unbundling of mediation and arbitration functions separates tasks, spreads risk, minimizes vulnerability, and reduces linkability, but often at the cost of greater complexity.

<a name="enemy"></a>_Enemy (aka attacker)_: An agent whose preferences could cause another agent harm; a third party who influences performance of a contract to the detriment of one or both parties.

<a name="object"></a>_Object_: Herein used to refer generically to any kind of digital data, which could be a key, a credential, a contract, a program, or a wide variety of other things.

<a name="credential"></a>_Credential_: A claim made by one agent about another.

<a name="positivecredential"></a>_Positive credential_: A claim made about an agent, that the agent would prefer to reveal, such as a degree from a prestigious school.

<a name="negativecredential"></a>_Negative credential_: A claim made about an agent, that the agent would prefer not to reveal, such as a bad credit rating.

<a name="cryptographicprotocol"></a>_Cryptographic protocol_: A protocol that uses mathematical principles and keys to accomplish smart contract objectives.

<a name="privity"></a>_Privity_: The principle that only the parties to a contract, including its designated arbitrators, need to have knowledge of or control over the contents and performance of that contract. Privity as an objective of smart contract is a generalization of the legal principle of privity. It formalizes the tradition of "it's none of your business". Attacks against privity are epitomized by Eve the eavesdropper, a passive observer of contents or performance, and malicious vandal Mallet, who actively interferes with performance or steals value. Privacy and confidentiality, or protecting the value of information about a contract, its parties, and its performance from Eve, is thus subsumed under privity. Privity often comes into conflict with observability and verifiability.

<a name="observability"></a>_Observability_: The ability of the parties to a contract to observe each other's performance of that contract, or to prove their performance to the other party. Also, the ability to differentiate between intentional violations of the contract and good faith errors. An important objective of smart contract design that often comes into conflict with privity.

<a name="verifiability"></a>_Verifiability_: The ability of a party to prove to an arbitrator that a contract has been performed or breached, and to differentiate between intentional violation and good faith errors. An important objective of smart contract design that often comes into conflict with privity.

<a name="reputablename"></a>_Reputable name_: A nym or true name that has a good reputation, usually because it carries many positive credentials, has a good credit rating, or is otherwise highly regarded. Companies strive to carry reputable brand names, while professionals such as doctors and lawyers strive to have many good personal recommendations of their name. Reputable names can be difficult to transfer between agents, because reputation assumes persistence of behavior, but such transfer can sometimes occur (for example, the sale of brand names between companies).

<a name="truename"></a>_True name_: An identifier that links many different kinds of information about an agent, such as a full birth name or social security number. As in magick, knowing a true name can confer tremendous power to one's enemies. It also can have major economic value among those who cooperate peacefully, as in the use of direct marketing to target product information to those agents most likely to be interested in those particular products.

<a name="mix"></a>_Mix_: A cryptographic protocol for messaging, in which analysis of who is talking to whom (traffic analysis) by Eve is prevented by the Russian-doll encryption of the message by the sender with the public keys of each mix operator in the chain, and the mixing of messages by each operator, so that panoptic wiretapper Eve loses track of the messages. Only 1 out of N of the operators needs to be trusted with the traffic information, although Eve can sometimes gather statistics over large numbers of messages to eventually guess who is talking to whom. The communicating parties can also be mutually anonymous, and with normal encryption need trust no other parties with the content of messages. Confidential messaging is necessary for the some of the privity features of Chaumian credentials and bearer securities to be strongly implemented on an actual network. Another confidential messaging system is the "Dining Cryptographers" net, also invented by Chaum.

<a name="nym"></a>_Nym_: An identifier that links only a small amount of related information about a person, usually that information deemed by the nym holder to be relevant to a particular organization or community. Examples of nyms include electronic bulletin board nicknames, pen names, aliases, and brand names. A nym may gain reputation within its community. For example, a conglomerate may sell a wide variety of brand names, each reputable in its own market niche. With Chaumian credentials, a nym can take advantage of the positive credentials of the holder's other nyms, as provably linked by the is-a-person credential.

<a name="namespace"></a>_Name space_: a set of short identifiers with a simple syntax, such as telephone numbers, computer-readable Internet address numbers, human-readable Internet domain names, etc.

<a name="chaumiancredentials"></a>_Chaumian credentials_: a cryptographic protocol for proving one possesses claims made about oneself by other nyms, without revealing linkages between those nyms.

<a name="is-a-personcredential"></a>_Is-a-person credential_: In Chaumian credentials, the true name credential, used to prove the linkage of otherwise unlinkable nyms, and to prevent the transfer of nyms between agents.

<a name="key"></a>_Key_: A focus of obscurity and control; a random number drawn from a name space so large that a lucky guess is vastly improbable. The public key half of an asymmetric key pair can also act as a nym.

<a name="biometric"></a>_Biometric_: Information pattern used to identify a particular body, such as a fingerprint, autograph, retina scan, password, etc.

<a name="authentication"></a>_Authentication_: Proof that one is communicating with an agent that possesses a particular key.

<a name="secretkeycryptography"></a>_Secret key (symmetric) cryptography_: Uses a key shared between agents to communicate with confidentiality and authentication.

<a name="publickeycryptography"></a>_Public key (asymmetric) cryptography_: Uses two keys, the private key and the public key. The public key is used to encrypt objects, and to verify digital signatures. The private key is used to decrypt and sign objects, and is typically kept secret by one or more key holders. Allows key distribution without exposing the key.

<a name="secretsharing"></a>_Secret sharing_: method of splitting a key (and thus, in effect, any object encrypted with that key) into N parts, of which only M are needed to recreate the key, but less than M of the parts provide no information about the key. A potent tool for distributing control over objects between agents.

<a name="digitalsignature"></a>_Digital signature_: Cryptographic protocol, based on public key cryptography, that proves that an object was in active contact with the private key corresponding to the signature: the object was actively "signed" with that key. Probably should have been called a "digital stamp" or "digital seal" since its function resembles more those methods than an autograph.

<a name="bitcommitment"></a>_Bit commitment_: A variant of digital signatures, used to commit an object, such as a promise or prediction, without revealing that object until later. It is impossible to unobservably violate the protocol, or to modify the object after it has been committed.

<a name="blindsignature"></a>_Blind signature_: digital signature and secret-key encryption protocols that together have the mathematical property of commutativity, so that they can be stripped in reverse of the order they were applied. The effect is that Bob "signs" an object, for which he can verify its general form, but cannot see its specific content. Typically the key of the signature defines the meaning of the signed object, rather than the contents of the object signed, so that Bob doesn't end up signing a blank check. Used in digital bearer instruments, where Bob is the clearing agent, and Chaumian credentials, where Bob is the credential issuer.

<a name="digitalbearerinstruments"></a>_Digital bearer instruments_: Objects identified by a unique key, and issued, cleared, and redeemed by a clearing agent. When an object is transferred, the transferee can request the clearing agent to verify that the key has never before been cleared, and issue a new key. The clearing agent prevents multiple clearing of particular objects, but can be prevented from linking particular objects one or both of the clearing nyms who transferred that object. These instruments come in an "online" variety, cleared during every transfer, and thus both verifiable and observable, and an "offline" variety, which can be transferred without being cleared, but is only verifiable when finally cleared, by revealing any the clearing nym of any intermediate holder who transferred the object multiple times (a breach of contract). Privacy from the clearing agent can take the form of transferree-unlinkability, transferrer-unlinkability, or "double blinded" where both transferrer and transferee are unlinkable by the clearing agent. Digital cash is a popular form of digital bearer instrument.

<a name="locality"></a>_Locality_: _ immediacy, such as that provided by online clearing of digital bearer instruments _ dealing with the agents one knows best \* dealing in one's area of specialty

<a name="hotbackup"></a>_Hot Backup_: A backup service which comes online upon failure of the current service. Usually triggered by a dead-man switch.

<a name="zkip"></a>_Zero-Knowledge Interactive Proof (ZKIP)_: A cryptographic protocol that can be used to prove that an agent possesses a key (and by weaker implication, that otherwise normally functioning agents who have an incentive to respond properly to the challenge, but fail to do so, do not possess the key), without revealing any information about that key. Currently used for authentication, and in smart weapons for Identification Friend or Foe (IFF).

<a name="smartproperty"></a>_Smart Property_: Software or physical devices with the desired characteristics of ownership embedded into them; for example devices that can be rendered of far less value to agents who lack possession of a key, as demonstrated via a zero knowledge interactive proof. Methods of implementing smart property might include OND (cf.), and engrained immobilizing or destructive devices to foil attempts to hot-wire the property.

<a name="ond"></a>_Operation Necessary Data (OND)_: Data necessary to the operation of smart property. For example, a complex, proprietary firing sequence needed to operate a computerized engine, a CAD file needed to manufacture a specialized part, etc. To avoid theft of service, ZKIP is required to open an encrypted channel to the device. To avoid leaking the OND to Eve, tamper detection combined with a dead-man switch can be used on the device end of the channel.

<a name="smartlien"></a>_Smart Lien_: Sharing control of smart property between parties, usually two parties called the owner and the lien holder. This property may be in the proximate possession of the owner or the lien holder, corresponding to the common-law notions of "artisan's lien" and "innkeeper's lien" respectively. Might be used to secure lines of credit, insurance policies, and many other kinds of contracts that involve smart property.

<a name="security"></a>_Security_: Represents a basic asset, such as a share of ownership (stock) or a claim debt (bonds, cash).

<a name="contingentcontract"></a>_Contingent contract_: Contains terms which depend on the choice of a party or a state of the world. An option is an example of a contingent contract.

<a name="derivative"></a>_Derivative_: A call or put option, future, or synthetic asset; such a contract is "derived" from a basic underlying security.

<a name="syntheticasset"></a>_Synthetic asset_: A derivative constructed, or "synthesized", by combining securities and other derivatives. Cash flows for sophisticated synthetics can be calculated to high precision, by means of finely grained decision trees.

<a name="cashflow"></a>_Cash flow_: The expected sequence of payments according to the terms of a contract. From cash flow can be computed the basic financial objectives of a contract, such as net present value.

---

Please send your comments to nszabo (at) law (dot) gwu (dot) edu

Copyright &copy; 1995 by Nick Szabo\
Permission to redistribute without alteration hereby granted
