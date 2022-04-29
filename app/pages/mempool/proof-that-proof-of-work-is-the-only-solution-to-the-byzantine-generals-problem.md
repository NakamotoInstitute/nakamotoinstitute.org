---
original_link: https://gist.github.com/oleganza/8cc921e48f396515c6d6
original_site: Oleg Andreev's GitHub
---

In reply to "@Vlad_Roberto: No, not a programmer. I just know there's better ways to doing anything without massive energy consumption & Banks."

Imagine you are sitting in a bunker. You have no idea what people are out there and what are their intentions. You only receive some incoming messages from strangers that may contain anything. They can be just random garbage or deliberately crafted messages to confuse you or lie to you. You never know. You cannot trust anyone.

The problem of "money" or any other "social contract" is that everyone should be able to know what the majority agrees to without trusting some intermediaries (otherwise they can easily abuse their special position). If everyone votes for "X", then you sitting in a bunker must somehow independently figure out that all those other people indeed voted for "X" and not for "Y" or "Z". But remember: you cannot trust anyone's message and messages are the only thing you get from the outside world.

When two propositions arrive into your bunker, "X" and "Y", we have no trusted reference point to figure out which one is supported by the majority of other people. We only have "data in itself" to judge which one we should choose as the main one. To make things simpler we are not trying to apply subjective judgement to either proposition, but only trying to make everyone agree to a single option. In case of Bitcoin it is a reasonable assumption: everyone is owner of their money, so no one really cares which version of the history is chosen as long as their own balance is respected.

So how X should be distinct from Y that we know for sure that no one can accidentally choose Y, Z or W? First property: this data should be "recent". So we know that we are not sitting on some old agreement while everyone else has moved onto something else. Second property: any "recent" alternative should be impossible to produce. Because if it was possible to produce, then there is always a chance that some number of people could see it and accept that alternative. And you have no way to estimate how many such alternatives exist and how many people accepted it (because you are sitting in a bunker and you cannot trust incoming messages or know how many message did you miss).

How do we define "impossible"? It means either of two things: either it is logically impossible, or it is practically (economically) impossible. If it is logically impossible, than we can know all future agreements in advance (like a deterministic chain of numbers), just by using induction. But this does not work because we'd have to have some agreement about starting point in the first place. So we end up with requiring practical impossibility. In other words we need the following:

**Message X should be provably recent and alternatives should be practically impossible to produce.**

Practical impossibility can be reframed in terms of "opportunity cost": there are limited physical resources and those should have been largely allocated to X than to Y so we can see that X sucked in all resources from any alternatives. Because if it didn't, then there is a huge uncertainty about whether remaining resources are used for alternative Y or they do not interfere with the voting process. Is it possible that X did not suck in a lot of resources while alternatives are still not possible? Then it would mean that X logically follows from whatever previous state of the system and there is no voting process needed.

Therefore: message X should be provably recent and should have employed provably big amount of resources, big enough that there are not enough resources left for any alternative Y to produce in a reasonably short time frame. Also, the message X should be always "recent" and always outcompete any alternative. Because we cannot reliably compare "old" messages: is Y an "old" one that was just delivered now, or was it produced just now after resources spent on X were released?

This logically leads us to the following: we should accept only the messages with the biggest Proof-of-Work attached, and that proof-of-work should be the greatest possible ever, so there would not be any possibility for any alternative to be produce in the short window of time. And that proof-of-work must be constantly reinforced or the value of previous consensus begins to fade quickly as the opportunity for alternatives grows.

Expensive, highly specialized computer farms is the most reliable way to achieve consensus. If we were to use non-specialized resources, it would be harder to gauge whether the majority of them are indeed used for proof-of-work computations. By observing that enormous amount of work happens in a very specific, easy-to-observe part of the economy, we can estimate how expensive it is to produce an alternative, equally difficult message. In case of Bitcoin mining farms, such an alternative would require a very expensive and complex production chain, requiring either outcompeting other firms that use chip foundries or building single use data centers in the most cost-effective locations on the planet (with the cheapest electricity, coldest weather, low latency connectivity etc.)

## Conclusion.

If achieving consensus in a non-trust manner is ever possible in practice, then it is only possible with a Proof-of-Work scheme and highly specialized expensive production chains. Also, consensus is only valuable for a short period of time so it must be constantly reinforced.
