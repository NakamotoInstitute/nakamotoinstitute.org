---
title: Mastercoin is a Nightmare of Insanity
authors:
  - daniel-krawisz
date: 2013-12-20
added: 2013-12-20
excerpt:
  No one should ever use Mastercoin under any circumstances or appraise their
  value as anything above zero.
image: spongebob-and-patrick.png
image_alt: Spongebob and Patrick
---

## An Altcoin in the Block Chain

Much undue attention has been given lately to [Mastercoin](http://www.mastercoin.org/ "Mastercoin"), an altcoin invented by J. R. Willett. Although Willett’s heart seems to be in the right place, Mastercoin is a deeply flawed system. Unlike other altcoins, Mastercoin is not mined and does not have its own blockchain; instead, it exists on the Bitcoin block chain as a set of prunable transactions that contain, in the addresses of their Bitcoin outputs, data representing Mastercoin calls.

While the idea of a new protocol layer that can be used with Bitcoin is interesting and potentially useful, it completely destroys any potential usefulness in Mastercoin because it means that Mastercoin is an entirely passive system. Because Mastercoin does not have its own block chain, all its transactions are simply extra pieces of data inserted into Bitcoin’s block chain, which, from the standpoint of the Bitcoin miners, are meaningless.

<figure>
  <img src="/static/img/mempool/mastercoin-is-a-nightmare-of-insanity/patrick-hammer.png" alt="Patrick and a Hammer" />
</figure>

Therefore, unlike Bitcoin or any altcoin that relies on its own block chain, Mastercoin is incapable of acting like a smart contract engine. There is nothing, for example, to prevent anyone from double-spending Mastercoins from a given address. Anyone can publish two conflicting Mastercoin transactions in the block chain, and all the Mastercoin system can do is define a rule by which one transaction is ignored.

This is not enough, however. Some of Mastercoin’s features require active participation by the users, but Mastercoin can do nothing to require them to behave correctly. For example, Mastercoin has a feature called “register a data stream”, by which the owner of a Bitcoin address declares that he will be publishing data hidden in transactions from it. For example, he could promise to post the price of gold every day to that stream. However, there is nothing to require him to post data on a regular schedule, and nothing preventing him from lying. This renders the datastream valueless as an input for a smart contract.

Of course that does not matter because, as I said, Mastercoin cannot do smart contracts. The only thing that could require Mastercoin users from behaving properly is a traditional human legal system that recognizes its features as legal contracts and which can set the police on anyone who doesn’t follow his promises. It is totally bizarre that Willett seems to think Mastercoin could be useful for anarcho-capitalist purposes. Eventually, platforms such as [Open Transactions](http://opentransactions.org/) will be able to do what Mastercoin claims, without the design flaws. OT will allow for [decentralized legal systems](http://bitcoinism.blogspot.com/2013/12/lex-cryptographia.html "Lex Cryptographia") and [voting pools](http://bitcoinism.blogspot.com/2013/12/voting-pools-how-to-stop-plague-of.html "Voting Pools") for consumer protection, and will allow these functions to integrate directly into the block chain instead of on top as the protocol development permits.

What’s the point of creating something like this? It’s really hard to understand what anybody was thinking. Anyway, this is the most fundamental reason Mastercoin fails.

## I Cannot Make Sense of Any of this Crap

Willett’s justification of his engineering decision is nonsensical and shows no understanding whatsoever. In [version 1.1 of the specification](https://e33ec872-a-62cb3a1a-s-sites.googlegroups.com/site/2ndbtcwpaper/MasterCoin%20Specification%201.1.pdf?attachauth=ANoY7cpVuaFAuVzPBJrOobfMxIFD4i-846pZmlRVKTwizeYgZDFSBoE3tEo7DKHX7wDg1yjsVk_lNjjg5Y8GssngzmkBXasXHGytZUGPX5UvDjKbvLeTs53Y0N7CZauZXMn7iCd) \[PDF\], he writes “Alternate block chains compete with bitcoins financially, confuse our message to the world, and dilute our efforts. \[...\] New protocol layers on top of the bitcoin protocol will increase bitcoin values, consolidate our message to the world, and concentrate our efforts, while still allowing individuals and groups to issue new currencies with experimental new rules.”

<figure>
  <img src="/static/img/mempool/mastercoin-is-a-nightmare-of-insanity/spongebob-hammer.png" alt="Spongebob and a Hammer" />
</figure>

However, the truth is almost the exact opposite of what Willett says. There is no reason that an alternate block chain should compete with Bitcoin financially because there are all kinds of things that can be done with a block chain that do not compete with Bitcoin’s function as a currency. As it happens, nearly all block chains are currencies, which _do_ compete with Bitcoin, but there is no reason that this is inherently necessary.

Furthermore _all_ currencies, crypto or not, compete with Bitcoin. The fact that mastercoins do not have their own block chain is irrelevant. They still compete with bitcoins and will reduce the value of bitcoins to the extent that people choose to use mastercoins over bitcoins. Anyone who likes Bitcoin really shouldn’t want _any_ new currencies to be created. As explained in [a previous article of mine](/mempool/the-problem-with-altcoins/ "The Problem with Altcoins"), the entire concept of an altcoin is fatally flawed. Because the value of a currency is caused by the network of people using it, a currency with a larger network should generally be seen as superior to one with a smaller network.

<figure>
  <img src="/static/img/mempool/mastercoin-is-a-nightmare-of-insanity/spongebob-patrick-fail.png" alt="Patrick and Spongebob Fail" />
</figure>

## Escrow-Backed User Currencies

In addition to the mastercoin currency, Mastercoin allows anyone to create new currencies at will that also use the Mastercoin protocol. Anyone who registers a new Mastercoin currency essentially becomes that new currency’s issuer and can create as much as he wants. Although Willett suggests that these new currencies can serve other functions, this is impossible as long as Mastercoin cannot be a smart contract engine. Until Mastercoin has its own block chain, all of user currencies are just tokens.

The most intricate layering of absurdities in the Mastercoin specification can be found in the feature called “escrow-backed user funds”. These are funds managed by a program that trade mastercoins and a user currency so as to attempt to track a real-world commodity. A Bitcoin address can be registered as an escrow-backed user fund with a transaction that specifies parameters describing the behavior of the program managing it. For example, someone could create one called cryptogold that was designed to track the price of gold.

First off, in order to create cryptogold, Mastercoin has to rely on a block chain datastream to determine what the price is. Yet, as I previously argued, there is no reason to expect any data stream to be reliable and therefore no way to know what the price of gold is.

Furthermore, there is no reason to expect the escrow fund to behave according to any rules at all. There is no reason that the fund will even attempt to track the price of gold because, as I have repeatedly emphasized, Mastercoin can require nothing of its users.

Let us assume, however, that a given fund manager is trustworthy and he does allow his fund to run by a program that follows the rules advertised in its declaration. In this case the fund is still not trustworthy and still cannot be expected to track the price of gold.

An ounce of cryptogold is not real gold or a claim on real gold, or anything. It is a completely different commodity that rational actors will treat differently from the commodity that it is supposed to track. Fundamentally, the fund is _a commodity that is traded for mastercoins by a computer program according to known rules_. Any relation to gold is incidental because people will choose to buy and sell it based on how they believe that the computer program will act. They will not just naively watch the price of gold and assume that the escrow-backed user fund is pretty much the same thing.

While one _could_ buy cryptogold simply because one believes that the price of gold will go up, one could also buy cryptogold as an attempt to manipulate the program. If you can know beforehand how a given trader will behave, you can always take advantage of him in a market. Thus, every fund that behaves fairly should be expected to go bankrupt eventually as people figure out how to profit from its predictable behavior.

There is no way to avoid this problem. As long as the program operates according to known rules, anyone can take advantage of its behavior. You could be playing chess with Deep Blue and you would always win if you had your _own_ duplicate of Deep Blue that you could use to predict every move it would make. This is effectively what everyone has for the fair escrow-backed user funds because the reference Mastercoin implementation is open source, so anyone can modify it to turn it to predict what other fair funds will do.

<figure>
  <img src="/static/img/mempool/mastercoin-is-a-nightmare-of-insanity/spongebob-wrench.png" alt="Spongebob and Wrench" />
</figure>

However, this point is purely esoteric because nothing forces the fund to behave according to any computer program and the creator of the fund has every reason not to follow the rules because if he did, the fund could not possibly remain healthy.

I have my qualms about Ripple, but at least it has _some_ useful purposes. The reason it is possible to trade real goods over Ripple is that ripple gateways are supposed to back the digital goods with real goods that they have on hand. The idea of linking a digital good to a real one any other way [is absurd](http://liftlight.tumblr.com/post/65086793819/it-isnt-possible-to-peg-a-digital-good-to-the-value-of). Mastercoin utterly utterly fails so badly that it is unfathomable.

## A Software Engineering Nightmare

In addition to failing economics, the Mastercoin developers also fail software engineering. As detailed in [this reddit thread](http://www.reddit.com/r/Bitcoin/comments/1rpx26/mastercoin_is_a_joke/), the Mastercoin specification is so poorly designed that it has several conflicting implementations, thus breaking the entire system.

<figure>
  <img src="/static/img/mempool/mastercoin-is-a-nightmare-of-insanity/patrick-thumb.png" alt="Patrick’s Thumb" />
</figure>

Because the different implementations disagree as to which transactions are considered valid, they can disagree as to the amount stored in a given address. For example, killerstorm, the author of the exposé, points to [an address](https://bitcointalk.org/index.php?topic=265488.msg3766604#msg3766604) which, on November 29, 2013, showed _four different_ balances depending on the implementation.

Since then, this problem has been resolved by [rewriting the specifications](https://github.com/mastercoin-MSC/spec) more carefully, but there are no doubt more ambiguities waiting to be discovered. This problem could not have been fixed without screwing over some people who think they own mastercoins.

As useless as I find Litecoin to be, at least it _functions_. At least it’s not riddled with bugs that break the entire system. The developers deserve eternal shame for having created this problem, no matter how they attempt to address it. Even if it is repaired, the fact that it happened at all reflects extremely poorly on the team building it. This is truly horrifying, and Willett should be excoriated for creating this monster.

## Please End the Madness

Everything about Mastercoin is completely insane. How can it be taken seriously? Its flaws are numerous, fundamental, and not difficult to understand. I do not even claim that my list of them is comprehensive. I would not be surprised if there were more that I did not discover when I did my research for this article. Mastercoin is a failure in just about every way. Nothing can redeem it and it is completely shocking that Mastercoins are actually being traded and have a price.

<figure>
  <img src="/static/img/mempool/mastercoin-is-a-nightmare-of-insanity/spongebob-new-home.png" alt="New Home" />
</figure>

Mastercoin is absolute garbage and it is just baffling to me that Willet commands any sort of respect for having created it. There is no excuse for how terribly designed and excuted they have been at every stage. All Mastercoin owners have been scammed because Mastercoin is incapable of delivering on its promises. No one should ever use Mastercoin under any circumstances or appraise their value as anything above zero.
