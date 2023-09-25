---
title: Ethereum is Doomed
author: daniel-krawisz
date: 2016-06-20
added: 2016-06-20
excerpt: "I fully support the attacker’s actions, and I wish I had thought of\
  \ it first."
image: programming-with-solidity.png
image_alt: Programming with Solidity
---

As [some have noted](https://twitter.com/jgarzik/status/736945669978525696), I
did not understand Ethereum very well when I wrote my [previous
article](/mempool/the-coming-demise-of-altcoins/) that touched on it. I
dismissed Ethereum as just another altcoin with extra bells and whistles.
However, there was a huge opportunity hiding in there, open to anyone who
understood the system well enough. I wish I had examined it further and much
more deeply because right now someone who did that, [someone whom I now
admire](http://pastebin.com/CcGUBgDG), is sitting on three million ethers.
_Update:_ the note is [probably
not](https://news.ycombinator.com/item?id=11927891) from the real hacker. I
still agree with its argument.

This person has developed a new investment strategy for the age of smart
contracts: You simply look for a way to exploit the smart contract which
causes it to send cash into your account, and then invest in it so as to
control it in a way that [extracts the
money](http://hackingdistributed.com/2016/06/18/analysis-of-the-dao-exploit/).

Ethereum truly is different from other altcoins. If I had looked into Ethereum
more carefully, I might have noticed that economics was not the only subject
that the Ethereum devs did not understand. They also don’t understand law and
software engineering. They created a situation in which bugs would be expected
to arise in an environment in which bugs are legally exploitable. That is
hacker heaven.

Let’s say that A wants to send ethers to B. I will write `A→B` as the atomic
operation which removes money from `A`'s balance and adds it to `B`’s. This
operation fails if `A`'s balance is not big enough. To send money in Ethereum,
it is as if we had a function that looked like this:

<pre>
send[f, x, y] = If[
	// Send funds to B and call f; roll back if an error is generated.
	Try[ A→B; f[]; True, False],
	// Call this if no error was generated.
	x[],
	// Call this if an error was generated.
	y[] ]
</pre>

where `x` and `y` are functions provided by `A`, and f is a function provided
by `B`. In other words, `A` sends the ethers to `B`, who immediately gets to
call a function that does whatever he wants with the money. That function is
`f`. If his function fails for some reason, `A→B` is rolled back and function
`y` is executed. Otherwise, `x` is executed. Anyone can provide _any_ function
to be executed upon receiving funds.[^1]

This is already enough of a nightmare, but suppose you have a public function
available to the hacker which is of the form

<pre>
hackMe[f] =
    // Use q to check whether we owe the attacker money.
    If[q[], send[f, x, y]]
</pre>

where `q` is a function that is supposed to fail if the attacker has no right
to demand funds.

Suppose that the hacker calls `hackMe`, and provides an `f` of the form

<pre>
f[] = p[]; hackMe[f]
</pre>

If the hacker can get `q` to succeed inappropriately, the following code is
executed upon calling `hackMe`:

<pre>
q[]; A→B; p[]; q[]; A→B; p[]; ... q[]; A→B; y[] ...
</pre>

If nothing else stops this execution, it will eventually stop when `A→B` fails
as a result of A not having enough funds. It can also fail if the call stack
fills up or if the computation runs out of
[gas](https://www.cryptocompare.com/coins/guides/what-is-the-gas-in-ethereum/),
but these are complications on top of the fundamental problem. A hacker can
try to ensure that only the last send fails so as to end up with everything.

<figure>
  <img src="/img/mempool/ethereum-is-doomed/the-dao-is-empty.png" alt="" />
  <figcaption>via <a href="https://twitter.com/KonradSGraf/status/743843080961409025">Twitter</a></figcaption>
</figure>

A naive approach to this bug would be to write `q` so that it keeps track of
how much is owed to `B` and fails if the money should already have been paid.
However, this approach is not good enough because in the mean time, from
function `p`, the attacker might run more code which you have made available
to him which creates further liabilities. The fix which the Ethereum team
released to upgrade DAO 1.0 to 1.1 takes this naive approach, as explained
[here](http://hackingdistributed.com/2016/06/18/analysis-of-the-dao-exploit/#was-1-1-vulnerable).

I've provided a scenario in which the result is to extract funds, but the
issue is much more general than that. You can think of an Ethereum smart
contract as being like a object in object-oriented programming, with a set of
public methods that any other contract can call. If you call another
contract's public methods, he can call any of _your_ public methods and
attempt to screw with your internal state. There are different names for this
depending on what the malicious contract does (such as [reentry and
solar-storm](https://blog.blockstack.org/solar-storm-a-serious-security-exploit-with-ethereum-not-just-the-dao-a03d797d98fa#.wpg35euyp)),
but the problem is really the same kind of problem you would have if you just
allowed people to run whatever code you wanted on your own computer.

This problem is so serious that it cannot be treated as a bug in the DAO. The
problem is with <s>Solidity itself, which is the scripting language used in
Ethereum.</s> _Update:_ The problem actually all the way down to the Ethereum
virtual machine. While reading the Solidity documentation, I noticed this:

> If `x` is a contract address, its code (more specifically: its fallback
> function, if present) will be executed together with the `send` call (this
> is a limitation of the EVM and cannot be prevented).

This means the same issue exists in
[Serpent](https://mc2-umd.github.io/ethereumlab/docs/serpent_tutorial.pdf),
another Ethereum scripting language, and every other one they might come up
with.

Imagine a bright eyed and bushy-tailed new programmer writing his first big
contract: "Now let’s see here…” he thinks. “I’m using the send function. That
means that I have to search for blocks of code that I’ve written which an
attacker could attempt to run in an infinite loop until there is no money
left. First of all, which possible blocks of code could be made to go in an
infinite loop? It could be any part that calls send, intermixed with anything
that the attacker wants to call in between… hmmm… " You have to think this
every time you send anyone money. It is totally ridiculous to expect anyone to
do this reliably. The only difference is that a novice would fail every single
time he tried to write a contract, whereas an expert wouldn't even bother
trying.

Now I have described this issue so as to make it very clear what is going on,
but in Solidity, the function I have called `f` is not very visible to the
programmer. It’s a method called the “default function” that can be defined on
every address. It executes automatically when you send to that address. So if
I was writing `hackMe` in Solidity, I wouldn’t have directly referenced the
function `f` as I wrote, but it executes anyway. It is very easy to write
`hackMe` in Solidity.

The [manual on Solidity](http://solidity.readthedocs.io/en/latest/) opens with
“Solidity is a high-level language whose syntax is similar to that of
JavaScript”, as if that were something to brag about. But apparently Solidity
has much more than just a superficial resemblance to JavaScript. Solidity is
like programming in JavaScript, except with your bank account accessible
through the Document Object Model.

A sign that no one is prepared to write smart contracts in Solidity is the
fact that the Ethereum dev team, the people who designed both Solidity and the
DAO, could not even fix their own bug. They don’t have the ability to approach
these bugs correctly, and neither, in my opinion, does anyone else. It may be
_possible_ to reliably write smart contracts that work correctly, but
currently no one knows how to do it. The dev team is not likely to figure it
out any time soon because they still think that this is just a bug in the DAO
rather than a serious problem with their entire system. If you want a smart
contract that you can actually use, you have to be _certain_ that it is
bug-free before it is deployed. there are no known tools or methods available
to Solidity developers which could provide an appropriate level of certainty.
Such tools will take years to be developed and until they are in common use,
no Ethereum smart contract should be trusted. Ethereum is doomed.

The legal implications of this hack are more interesting than the hack itself.
Because the code of the DAO is a legally-binding contract, how can you argue
so as to convince a judge that some behavior of the program is really a bug?
The DAO provides nothing other than its own code to specify how it is supposed
to work. For example, there is [no specification in a formal
language](https://www.reddit.com/r/ethereum/comments/4opjov/the_bug_which_the_dao_hacker_exploited_was_not/),
or proofs as to its correctness. If the Ethereum team knew how to test
software, they might have produced something like that, which also could have
provided corroborating evidence that any bug was unintended.

I fully support the attacker’s actions, and I wish I had thought of it first.
His ethers may become worthless before he can sell them for Bitcoin, but he
may also have [made a huge short on
ethers](http://hackingdistributed.com/2016/06/18/analysis-of-the-dao-exploit/#step-3-the-big-short)
just before executing the attack and made around $1 million that way.

For a final comment on the Ethereum team’s response, I provide an insightful
quote from [Emin Gün
Sirer](http://hackingdistributed.com/2016/06/17/thoughts-on-the-dao-hack/#what-s-a-hack-when-you-don-t-have-a-spec):

> Had the attacker lost money by mistake, I am sure the devs would have had no
> difficulty appropriating his funds and saying “this is what happens in the
> brave new world of programmatic money flows.” When he instead emptied out
> coins from The DAO, the only consistent response is to call it a job well
> done.

<figure>
  <img src="/img/mempool/ethereum-is-doomed/vitalik-rai-stones.jpg" alt="" />
  <figcaption>Artwork by <a href="https://twitter.com/BigLambda/status/891148584334245888">Big λ</a></figcaption>
</figure>

[^1]:
    If you don’t believe me read this analysis of the hack
    [here](http://hackingdistributed.com/2016/06/16/scanning-live-ethereum-contracts-for-bugs/):

    > To have a contract send Ether to some other address, the most
    > straightforward way is to use the send keyword. This acts like a method
    > that’s defined for every “address” object.

    I love how he says this in such a matter-of-fact way, like that's no big
    deal.

    Also note [this poor developer’s
    unease](http://vessenes.com/ethereum-griefing-wallets-send-w-throw-considered-harmful/)
    upon learning about this “feature”:

    > Here’s the deal. In Bitcoin, an address is the public key that
    > corresponds to a private key held by a wallet. I’m lying a bit to aid
    > comprehension. But, fundamentally, it’s just a bit of data. In Ethereum,
    > an address could be similar – not a contract, but a public key. But, it
    > could also be another smart contract’s address. The Mist client
    > encourages users to make a wallet contract as a first step after loading
    > up, for example. Users would then offer the address of that contract as
    > their ‘wallet address’. Other contracts do not typically utilize any
    > mechanism to distinguish between an address of a private key, and an
    > address of a wallet. It’s a fundamental transaction in Ethereum to send
    > money to a contract, and developers seem to expect it to ‘just work’
    > like in Bitcoin or other digital currencies, perhaps with a transaction
    > fee attached.
