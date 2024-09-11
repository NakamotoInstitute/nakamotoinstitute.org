---
title: Bitcoin, what took ye so long?
authors:
  - nick-szabo
date: 2011-05-28
categories:
  - bitcoin
doctype: essay
external: https://unenumerated.blogspot.com/2011/05/bitcoin-what-took-ye-so-long.html
---

So asks [gwern](/library/bitcoin-is-worse-is-better/) in a spectacular display of hindsight.

The short answer about why it took so long is that the bit gold/Bitcoin ideas were nowhere remotely close to being as obvious gwern suggests. They required a very substantial amount of unconventional thought, not just about the security technologies gwern lists (and I'm afraid the list misses one of the biggest ones, Byzantine-resilient peer-to-peer replication), but about how to choose and put together these protocols and why. Bitcoin is not a list of cryptographic features, it's a very complex system of interacting mathematics and protocols in pursuit of what was a very unpopular goal.

While the security technology is very far from trivial, the "why" was by far the biggest stumbling block -- nearly everybody who heard the general idea thought it was a very bad idea. Myself, Wei Dai, and Hal Finney were the only people I know of who liked the idea (or in Dai's case his related idea) enough to pursue it to any significant extent until Nakamoto (assuming Nakamoto is not really Finney or Dai). Only Finney ([RPOW](/finney/rpow/index.html)) and Nakamoto were motivated enough to actually implement such a scheme.

The "why" requires coming to an accurate understanding of the nature of two difficult and almost always misunderstood topics, namely [trust](/library/trusted-third-parties/) and the nature of money. The overlap between cryptographic experts and libertarians who might sympathize with such a "gold bug" idea is already rather small, since most cryptographic experts earn their living in academia and share its political biases. Even among this uncommon intersection as stated very few people thought it was a good idea. Even [gold bugs](https://web.archive.org/web/20080515022027/http://www.poorandstupid.com/2008_04_13_chronArchive.asp#3079142232624095259) didn't care for it because we already have real gold rather than mere bits and we can pay online simply by issuing digital certificates based on real gold stored in real vaults, a la the formerly popular [e-gold](http://en.wikipedia.org/wiki/E-gold). On top of the plethora of these misguided reactions and criticisms, there remain many open questions and arguable points about these kinds of technologies and currencies, many of which can only be settled by actually fielding them and seeing how they work in practice, both in economic and security terms.

Here are some more specific reasons why the ideas behind Bitcoin were very far from obvious:

(1) only a few people had read of the bit gold ideas, which although I came up with them in 1998 (at the same time and on the same private mailing list where Dai was coming up with b-money -- it's a long story) were mostly not described in public until [2005](/library/bit-gold/), although various pieces of it I described earlier, for example the crucial Byzantine-replicated chain-of-signed-transactions part of it which I generalized into what I call [secure property titles](/library/secure-property-titles/).

(2) Hardly anybody actually understands money. Money just doesn't work like that, I was told fervently and often. Gold couldn't work as money until it was already shiny or useful for electronics or something else besides money, they told me. (Do insurance services also have to start out useful for something else, maybe as power plants?) This common argument coming ironically from libertarians who misinterpreted Menger's account of the origin of money as being the only way it could arise (rather than an account of how it could arise) and, in the same way misapplying Mises' regression theorem. Even though I had rebutted these arguments in my study of the [origins of money](/library/shelling-out/), which I humbly suggest should be should be required reading for anybody debating the economics of Bitcoin.

There's nothing like Nakamoto's incentive-to-market scheme to change minds about these issues. :-) Thanks to RAMs full of coin with "scheduled deflation", there are now no shortage of people willing to argue in its favor.

(3) Nakamoto improved a significant security shortcoming that my design had, namely by requiring a proof-of-work to be a node in the Byzantine-resilient peer-to-peer system to lessen the threat of an untrustworthy party controlling the majority of nodes and thus corrupting a number of important security features. Yet another feature obvious in hindsight, quite non-obvious in foresight.

(4) Instead of my automated [market](/library/bit-gold-markets/) to account for the fact that the difficulty of puzzles can often radically change based on hardware improvements and cryptographic breakthroughs (i.e. discovering algorithms that can solve proofs-of-work faster), and the unpredictability of demand, Nakamoto designed a Byzantine-agreed algorithm adjusting the difficulty of puzzles. I can't decide whether this aspect of Bitcoin is more feature or more bug, but it does make it simpler.
