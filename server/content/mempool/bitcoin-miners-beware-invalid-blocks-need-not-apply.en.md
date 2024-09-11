---
title: "Bitcoin Miners Beware: Invalid Blocks Need Not Apply"
authors:
  - stop-and-decrypt
date: 2018-06-01
added: 2024-09-13
image: invalid-blocks-need-not-apply.jpg
image_alt: Invalid blocks need not apply
original_site: HackerNoon
original_url: https://hackernoon.com/bitcoin-miners-beware-invalid-blocks-need-not-apply-51c293ee278b
excerpt: Bitcoin is an impenetrable fortress of validation.
---

## Bitcoin is an impenetrable fortress of validation.

_Like my [Moore’s Law article](https://hackernoon.com/moores-observation-35f7b25e5773), this is an excerpt from a [much larger article](https://hackernoon.com/sharding-centralizes-ethereum-by-selling-you-scaling-in-disguised-as-scaling-out-266c136fc55d). It’s good enough to serve as a standalone piece because the misconception this aims to put to rest is a commonly raised one that becomes annoyingly repetitive._

### Understanding the Bitcoin network without math.

Bitcoin is more than just a chain of blocks. I want to help you understand how Bitcoin’s blockchain _network_ is designed because it’ll help you fill in some gaps as you begin to acquire more knowledge in this field. I say _blockchain_ network because Bitcoin also has a _payment channel_ network _(lightning)_ layered on top of it that doesn’t effect the structure of the blockchain network. I won’t be discussing Bitcoin’s lightning network in this article though, as it’s not that relevant to the points I’ll make.

Below is a rough example of the Bitcoin network scaled down to 1000 fully validating nodes _(there’s really 115,000 currently)_. Each node here has 8 connections to other nodes, because this is the default amount of connections the client makes without any changes made to it. My node is in here somewhere, and if you’re running one, it’s in there too. Coinbase’s nodes are in there, Bitmain’s nodes are in there, and if Satoshi is still around, Satoshi’s node is in there too.

_Please note that this is just a diagram, and that the real network topology can (and probably does) vary from this. Some nodes have more than the default amount of connections while others may opt to connect to a limited number or stay behind just one other node. There’s no way to know what it actually looks like because **it’s designed with privacy in mind** (although some monitoring companies certainly try to get very close approximations) and nodes can routinely changed who their peers are._

<figure>
  <img src="/static/img/mempool/bitcoin-miners-beware-invalid-blocks-need-not-apply/figure-1.png" alt="">
</figure>

<figure>
  <img src="/static/img/mempool/bitcoin-miners-beware-invalid-blocks-need-not-apply/figure-2.gif" alt="">
</figure>

I started with that diagram because I want you to understand that there are no differences in these nodes because **they all fully validate.** This means they all check the entire chain to make sure each and every transaction and block follow the rules. This will prove to be important as I explain further.

The ones on the inside are no different than the ones on the outside, they all have the same amount of connections. When you start up a brand new node, it finds peers and becomes one of the hive. The longest distance _in this graph_ from any of these nodes to another is 6. In real life there are some deviations to this distance because [finding new peers](https://en.bitcoin.it/wiki/Satoshi_Client_Node_Discovery) isn’t a perfectly automated process that distributes everyone evenly, but generally, adding more nodes to the network doesn’t change this. There are 6 degrees of Kevin Bacon, and in 6 hops my transaction is in the hands of _(almost)_ every node, **if it’s valid.**

I’m going to select “my” node from this group and drag it out, so I can demonstrate what happens when I create a transaction and announce it to the network. Below you’ll see my node all the way to the right, and then you’ll see the 8 other nodes _(peers)_ that mine is connected to.

<figure>
  <img src="/static/img/mempool/bitcoin-miners-beware-invalid-blocks-need-not-apply/figure-3.png" alt="">
</figure>

When I create a transaction and “send it out to the world”, it’s actually only going to these 8 peers. Since Bitcoin is designed from the ground up to make every node a fully validating node, when these 8 nodes receive my transaction they check to see if it’s valid before sending it out to _their_ 8 peers. **If my transaction is invalid it will never break the “surface” of the network.** My peers will never send that bad transactions to their peers. They actually don’t even know that I created that transaction. There’s no way for them to tell, and they treat all data as equal, but if I were to keep sending invalid transaction to any of my 8 peers, they would all eventually block me. This is done by them automatically to prevent me from spamming my connection to them. No matter who you are, or how big your company is, **your transaction won’t propagate if it’s invalid.**

Now let’s say you’re not running a full-node, but you’re using a [light-client](https://en.bitcoin.it/wiki/Thin_Client_Security) instead. Various light-clients exist for the desktop, and for your mobile phone. Some of them are Electrum, Armory, Bread, and Samourai Wallet. Light-clients tether to a specific node. Some can be set up to change the one they connect to over time, but they are still ultimately tethered. This is what tethering looks like:

<figure>
  <img src="/static/img/mempool/bitcoin-miners-beware-invalid-blocks-need-not-apply/figure-4.png" alt="">
</figure>

I want you to note that this is just a diagram, and it’s easy to demonstrate tethering using a node that _happens_ to be on the rim, but there is no _real_ rim, and tethering is tethering wherever that node happens to be within this diagram. I’ve highlighted this in yellow. The nodes being tethered to are green, and the blue dots are light-clients. All information going to or coming from the light-client goes through the node they’re tethered to. They depend on that node. **They are not part of the network. They’re not nodes.**

Here’s where it gets fun, and where other people try to misrepresent how the network actually works: **What if I wanted to start mining?**

_Mining_ a block is the act of _creating_ a block. Much like a transaction you want to send, you must create the block and announce it to the network. Any node can announce a new block, there’s nothing special about that process, _you just need a new block_. Mining has gotten increasingly difficult, but if you want you can purchase specialized hardware and connect it to your personal node.

<figure>
  <img src="/static/img/mempool/bitcoin-miners-beware-invalid-blocks-need-not-apply/figure-5.png" alt="">
</figure>

Remember that bit about invalid transactions? Same goes for blocks, but you need to understand something very specific about how blocks are created.

First watch this video. I skipped to the important part about hashing, using nonces _(random value)_ and appending the chain with that new block **header**:

<figure>
  <img src="/static/img/mempool/bitcoin-miners-beware-invalid-blocks-need-not-apply/figure-6.jpg" alt="">
</figure>

Please watch the entire thing if you have time. It’s personally my favorite video explaining how mining works.

When you get to the following part in the video where the labels “Prev hash” are applied, those are the block headers:

<figure>
  <img src="/static/img/mempool/bitcoin-miners-beware-invalid-blocks-need-not-apply/figure-7.png" alt="">
</figure>

What’s not mentioned in this video is you can create valid blocks headers **even if all the transactions inside the block are invalid**. It still requires the same amount of time to mine blocks with invalid transactions as it does to mine a block with valid transactions. The incentive to spend all that time and energy creating such a block would be to push through a transaction that rewards you with Bitcoin that aren’t yours. This is why it’s important that all nodes check not just the block headers, **but the transactions as well**. This is what stops miners from spending that time. Because **all** nodes check, **no** miners can cheat the system. If all nodes didn’t check you’d have to rely on the ones that _do_ check. This would separate nodes into “types”, and the only type that would matter would be the ones that check.

So what if you join a mining pool? You might do this because mining is too difficult for you to do alone, or if you’re a slightly larger entity you might prefer a steady income as opposed to a sporadic one. Many miners do this, and they connected their specialized hardware directly to a mining pool using an entirely different protocol call the [Stratum mining protocol](https://en.bitcoin.it/wiki/Stratum_mining_protocol). Just like creating a transaction with your non-node cellphone, **you don’t have to run a node to connect your hardware to a mining pool.** You can mine without running a node, and many miners do exactly that. Here’s what that looks like below in blue. I’ve used Slush Pool for this example:

<figure>
  <img src="/static/img/mempool/bitcoin-miners-beware-invalid-blocks-need-not-apply/figure-8.png" alt="">
</figure>

Remember, I dragged these pool-run nodes out of the diagram for demonstration purposes. Just like any other node, these pool-run nodes need peers. They need peers to receive transactions & blocks, and they need peers to announce blocks they create. Allow me to reiterate again: **All nodes validate all blocks and all transactions.**

If any of these pools announce an invalid block, their peers will know **because they fully-validate**, and they won’t send it out to other nodes. Just like transactions, **invalid blocks do not enter the network.**

Here’s another way to look at this without pulling these nodes out from the diagram. Below is a private miner who doesn’t want to be known, it has 8 random peers, and **none of those peers knows that it’s a miner**. Again, this is intensionally designed this way for privacy reasons. There’s no way for any node in the network to know that the block they received was _created_ by their peer, or _relayed_ by their peer. All they know is if it’s valid or not, and if it is they send it along, if it’s not, they don’t.

<figure>
  <img src="/static/img/mempool/bitcoin-miners-beware-invalid-blocks-need-not-apply/figure-9.png" alt="">
</figure>

Hopefully you’re getting the picture, and I don’t believe I used any fancy math or equations to get here. I’d like to move on because I feel like this is complete coverage, but there is one final thing I’d like to address because it’s this final aspect that is used to confuse others who don’t fully understand everything I just explained. It’s so rampantly used that I need to address it.

<figure>
  <img src="/static/img/mempool/bitcoin-miners-beware-invalid-blocks-need-not-apply/figure-10.png" alt="">
  <figcaption>
    <a href="https://twitter.com/VitalikButerin/status/1000232465540136960">https://twitter.com/VitalikButerin/status/1000232465540136960</a>
  </figcaption>
</figure>

My original comment was talking about light-clients, also called SPV clients, and how they aren’t part of the network. I demonstrated this above with the blue tethered dots. His follow-up comment tries to imply that nodes that mine are the only nodes who’s rejection matters. _Remember: nodes have no way of knowing which other nodes mined a block versus who relayed a block, **this was designed intentionally.**_

Now for a final diagram so I can try and explain the logic that’s used when people say “only mining nodes matter”. Some miners connect directly to other miners so that out of their peer list with the network, some of them are also other miners. **Not all miners do this**. Some of these miners that connect directly also use _optional_ relay networks like the FIBRE network [being designed](http://bluematt.bitcoin.ninja/2016/07/07/relay-networks/) by Bitcoin Core developer [Matt Corallo](https://twitter.com/TheBlueMatt), but even this side-network isn’t exclusive to miners, anyone can join including you or me and it’s just there to help block relay across the network. Either way, people try to argue that this interconnectivity of “nodes that mine” _(whether using something like FIBRE or not)_ implies they’re the only ones that matter, and it’s absurd:

<figure>
  <img src="/static/img/mempool/bitcoin-miners-beware-invalid-blocks-need-not-apply/figure-11.png" alt="">
</figure>

In this example I left the node’s peers inside the diagram. You should get the point by now. They reject invalid blocks. That group of nodes inside the green circles are most definitely not the only set of nodes that matter in this network.

<figure>
  <blockquote>
    <p>Bitcoin is an impenetrable fortress of validation.</p>
    <p>It doesn't matter if you created the transaction/block, or if someone else sent it to you: If it's not valid it's not getting in.</p>
    <p>All nodes enforce validation in tandem.</p>
    <p>Some people still don't seem to understand this concept.</p>
  </blockquote>
  <figcaption>— <cite>@StopAndDecrypt</cite>, <time datetime="2018-06-01">June 1, 2018</time></figcaption>
</figure>
