---
title: Bitcoin is Time
authors:
  - gigi
date: 2021-01-14
added: 2024-10-07
excerpt: What is a new idea — what Satoshi figured out — is how to indepen­dently agree upon a history of events without central coordi­na­tion.
original_site: dergigi.com
original_url: https://dergigi.com/2021/01/14/bitcoin-is-time/
image: bitcoin-is-time.jpg
image_alt: Bitcoin is Time
---

<figure>
  <blockquote>
    <p>One luminary clock against the sky<br />
    Proclaimed the time was neither wrong nor right.</p>
  </blockquote>
  <figcaption>Robert Frost, <em>Acquainted with the Night</em> (1928)</figcaption>
</figure>

<figure>
  <blockquote>
    <p>Time is still the great mystery to us. It is no more than a concept; we don’t know if it even exists…</p>
  </blockquote>
  <figcaption>Clifford D. Simak, <em>Shakespeare’s Planet</em> (1976)</figcaption>
</figure>

Time is money, or so the saying goes. It follows that money is also time: a repre­sen­ta­tion of the collec­tive economic energy stored by humanity. However, the link between time and money is more intri­cate than it might seem at first. If money requires no time to create, it doesn’t work as money very well, or not for long. More profoundly, as we shall see, keeping track of things in the infor­ma­tional realm always implies keeping track of time.

As soon as money goes digital, we have to agree on a *definition of time*, and herein lies the whole problem. You might think telling the time is as easy as glancing at whatever clock is nearby, and you would be right when it comes to everyday tasks. But when it comes to synchro­nizing the state of a global, adver­sarial, distrib­uted network, telling the time becomes an almost intractable problem. How do you tell the time if clocks can’t be trusted? How do you create the concept of a singular time if your system spans the galaxy? How do you measure time in a timeless realm? And what is time anyway?

To answer these questions, we will have to take a closer look at the concept of time itself and how Bitcoin makes up its own time: block time — more commonly known as _block height_. We will explore why the problem of timekeeping is intimately related to keeping records, why there is no absolute time in a decen­tral­ized system, and how Bitcoin uses causality and unpre­dictability to build its own sense of now.

Timekeeping devices have trans­formed civiliza­tions more than once. As Lewis Mumford pointed out in 1934: “The clock, not the steam-engine, is the key-machine of the modern indus­trial age.” Today, it is again a timekeeping device that is trans­forming our civiliza­tion: a clock, not computers, is the true key-machine of the modern infor­ma­tional age. And this clock is Bitcoin.

## Keeping Track of Things

<figure>
  <blockquote>
    <p>Let the child learn to count things, thus getting the notion of number. These things are, for the purpose of counting, consid­ered alike, and they may be single objects or groups.</p>
  </blockquote>
  <figcaption>David Eugene Smith, <em>The Teaching of Elemen­tary Mathe­matics</em> (1900)</figcaption>
</figure>

Very broadly speaking, there are two ways to keep track of things: physical tokens and ledgers. You can either use real-world artifacts directly, e.g., give someone a sea shell, a coin, or some other tangible _thing_, or you can repli­cate the state of the world by writing down what happened on a piece of paper.

Imagine you are a shepherd and want to make sure that your whole flock returned home. You can put a collar on each sheep, and as soon as a sheep returns home, you simply remove the collar and hang it up in your shed. If you have one hanger for every collar, you will know that every sheep returned safely as soon as all hangers are filled. Of course, you can also count them and keep a list. However, you will have to make sure to create a new list every time you start counting, and you will also have to make sure not to count a single sheep twice (or not at all).

Money is essen­tially a tool to keep track of who owes what to whom. Broadly speaking, every­thing we have used as money up to now falls into two categories: _physical_ artifacts and _infor­ma­tional_ lists. Or, to use more common parlance: tokens and ledgers.

<figure>
  <img src="/static/img/mempool/bitcoin-is-time/ledger-token.jpg" alt="Ledger vs. Token" />
</figure>

It is impor­tant to realize the inherent differ­ence of these categories, so let me point it out explic­itly: The first method — a physical token — *directly* repre­sents the state of things. The second one — a ledger — *indirectly* reflects the state of things. Each comes with advan­tages and disad­van­tages. For example, tokens are physical and distrib­uted; ledgers are infor­ma­tional and central­ized. Tokens are inher­ently trust­less; ledgers are not.

In the digital realm — no matter how intensely marketing gurus try to convince you of the opposite — we can only use ledgers. It is an _infor­ma­tional_ realm, not a physical one. Even if you call a certain kind of infor­ma­tion a “token,” it is still a malleable piece of infor­ma­tion, written down on a hard drive or some other medium that can hold infor­ma­tion, effec­tively rendering it an infor­ma­tional record.

The ledger-like nature of all digital infor­ma­tion is the root cause of the double-spend problem. Infor­ma­tion never repre­sents the state of the world _directly_. Further, the movement of infor­ma­tion implies copying. Infor­ma­tion exists in one place, and to “move” it, you have to copy it to another place and erase it at its origin. This problem doesn’t exist in the physical realm. In the physical realm, we can actually move things from A to B. The infor­ma­tional realm doesn’t have this property. If you want to “move” infor­ma­tion from list A to list B, you have to copy it from A to B. There is no other way.

Another way to think about it is in terms of unique­ness. Physical tokens are unique compos­ites of atoms whose assembly is not easily replic­able. Pure infor­ma­tion does not have this property. If you can read the infor­ma­tion, you can also copy it perfectly. Practi­cally speaking, it follows that physical tokens are unique, and digital tokens are not. I would even argue that “digital token” is a misnomer. A token might repre­sent secret infor­ma­tion, but it will never repre­sent unique, singular, uncopy­able infor­ma­tion.

This differ­ence in proper­ties shows that there really is no way to “hand over” infor­ma­tion. It is impos­sible to pass on a digital token like you would pass on a physical one since you can never be sure if the original owner destroyed the infor­ma­tion on his end. Digital tokens, like all infor­ma­tion, can only be spread, like an idea.

<figure>
  <blockquote>
    <p>… if you have an apple and I have an apple, and we swap apples — we each end up with only one apple. But if you and I have an idea and we swap ideas — we each end up with two ideas.</p>
  </blockquote>
  <figcaption>Charles F. Brannan (1949)</figcaption>
</figure>

Physical tokens — what we call physical bearer assets, or “cash” — are free from this dilemma. In the real world, if you hand me a coin, your coin is gone. There is no magical dupli­ca­tion of the coin, and the only way to give it to me is to physi­cally hand it over. The laws of physics do not allow you to double-spend it.

While double-spending does exist in the non-digital realm — George Parker, a con artist who famously “double-spent” the Brooklyn Bridge and other landmarks comes to mind — it requires elabo­rate decep­tion and gullible buyers. Not so in the digital realm.

In the digital realm, because we are always dealing with _infor­ma­tion,_ double-spending is an _inherent_ problem. As everyone who ever copied a file or used copy-and-paste knows, infor­ma­tion is something that you can copy _perfectly_, and it is not bound to the medium that hosts it. If you have a digital photo­graph, for example, you can copy it a million times, store some copies on a USB stick, and send it to thousands of different people. Perfect copies are possible because infor­ma­tion allows for flawless error correc­tion, which elimi­nates degra­da­tion. And to top things off, there is virtu­ally no cost to dupli­ca­tion and no way to tell what the original was.

Again: when it comes to infor­ma­tion, copying is all there is. There simply is no way to _move_ digital infor­ma­tion from A to B. Infor­ma­tion is always _copied_ from A to B, and if the copying process was successful, the original copy of A is deleted. This is why the double-spending problem is so tricky. Absent of a central authority, there is no way to move _anything_ from A to B in a trust­less manner. You always have to trust that the original will be deleted. A natural side-effect is that, when it comes to digital infor­ma­tion, it is _impos­sible_ to tell how many copies are in existence and where these copies might be.

Because of this, using digital “tokens” as money can not and will never work. Since tokens derive their relia­bility from being hard to repro­duce as a result of their unique physical construc­tion, this advan­tage disap­pears in the digital realm. In the digital realm, tokens cannot be trusted. As a result of the nature of infor­ma­tion’s intrinsic proper­ties, the only viable format for digital money is not a token but a ledger — which brings us to the problem of time.

## Tokens Are Timeless, Ledgers Are Not

<figure>
  <blockquote>
    <p>For the things seen are tempo­rary, but the things unseen are everlasting.</p>
  </blockquote>
  <figcaption>Paul of Tarsus, _Corinthians_ 4:18b</figcaption>
</figure>

When it comes to physical tokens, the time of a trans­ac­tion does not matter. You either have the coins in your pocket, or you don’t; you can either spend them, or you can’t. The simple act of posses­sion is the only prereq­ui­site for spending. The laws of nature take care of the rest. In that sense, physical tokens are trust­less and timeless.

When it comes to ledgers, physical posses­sion falls to the wayside. Whoever is in control of the ledger needs to make sure that things are _in order_. What is other­wise given by physical laws, namely that you can’t spend money that you don’t have and you can’t spend money that you have already spent previ­ously, has to be enforced by man-made rules. It is these rules that govern the orderly opera­tion and mainte­nance of a ledger, not physical laws.

Moving from physical laws to man-made rules is the crux of the matter. Man-made rules can be bent and broken, physical laws not so much. For example, you can’t simply “make up” a physical gold coin. You have to dig it out of the ground. You can, however, absolutely make up a gold coin on paper. To do this, you simply add an entry to the ledger and give yourself a couple of coins. Or, in the case of central banks, simply add a couple trillion with a few computer keystrokes. (Fancy finan­cial people call this “Rehypoth­e­ca­tion,” “Fractional Reserve Banking,” or “Quanti­ta­tive Easing” — but don’t be fooled, it’s all the same: making up money.)

To keep ledgers and those who manip­u­late them honest, regular, indepen­dent audits are required. The ability to account for every single entry in a ledger is not a luxury. Auditors need to be able to go over the books — backward in time — to keep ledgers honest and functioning. Without reliable timestamps, verifying the internal consis­tency of a ledger is impos­sible. A mecha­nism to estab­lish an unambiguous order is essen­tial.

Without an absolute sense of time, there is no way to have a defined order of trans­ac­tion. And without a defined order of trans­ac­tions, the rules of a ledger can not be followed. How else can you make sure how much money you actually have? How else can you make sure that things are _in order_?

The distinc­tion between tokens and ledgers highlights the neces­sity for keeping track of time. In the physical realm, coins are timeless artifacts that can be exchanged without oversight. In the digital realm, coinstamping requires timestamping.

## Centralized Coinstamping

<figure>
  <blockquote>
    <p>Time: a great engraver, or eraser.</p>
  </blockquote>
  <figcaption>Yahia Lababidi (b. 1973)</figcaption>
</figure>

The common way to solve the double-spending problem — the problem of making sure that a digital transfer only happens once — is to have a central list of trans­ac­tions. Once you have a central list of trans­ac­tions, you have a single ledger that can act as the sole source of truth. Solving the double-spending problem is as easy as going through the list and making sure that every­thing adds up correctly. This is how PayPal, Venmo, Alipay, and all the banks of this world — including central banks — solve the double-spending problem: via central authority.

<figure>
  <blockquote>
    <p>The problem of course is the payee can’t verify that one of the owners did not double-spend the coin. A common solution is to intro­duce a trusted central authority, or mint, that checks every trans­ac­tion for double-spending. \[…\] The problem with this solution is that the fate of the entire money system depends on the company running the mint, with every trans­ac­tion having to go through them, just like a bank.</p>
  </blockquote>
  <figcaption>Satoshi Nakamoto (2009)</figcaption>
</figure>

It is worth pointing out that Satoshi didn’t manage to make infor­ma­tion non-copyable. Every part of bitcoin — its source code, the ledger, your private key — can be copied. All of it can be dupli­cated and tampered with. However, Satoshi managed to build a system that makes rule-breaking copies completely and utterly useless. The Bitcoin network performs an intri­cate dance to decide which copies are useful and which aren’t, and it is this dance that brings scarcity into the digital realm. And like with every dance, a temporal measuring stick is required to dictate the rhythm.

Even a central­ized ledger can only solve the double-spending problem if it has a consis­tent way to keep track of time. You always need to know who gave how much to whom and, most impor­tantly: _when_. In the realm of infor­ma­tion, there is no coin-stamping without time-stamping.

<figure>
  <blockquote>
    <p>It must be stressed that the <em>impos­si­bility of associ­ating events with points in time</em> in distrib­uted systems was the unsolved problem that precluded a decen­tral­ized ledger from ever being possible until Satoshi Nakamoto invented a solution.</p>
  </blockquote>
  <figcaption>Gregory Trubet­skoy (2018)</figcaption>
</figure>

## Decentralized Time

<figure>
  <blockquote>
    <p>Time brings all things to pass.</p>
  </blockquote>
  <figcaption>Aeschylus (525 BC – 456 BC)</figcaption>
</figure>

Time and order have a very intimate relation­ship. As Leslie Lamport pointed out in his 1978 paper _Time, Clocks, and the Ordering of Events in a Distrib­uted System_: “The concept of time is funda­mental to our way of thinking. It is derived from the more basic concept of the order in which events occur.” Absent a central point of coordi­na­tion, seemingly intuitive notions of “before,” “after,” and “simul­ta­ne­ously” break down. In the words of Lamport: “the concept of ‘happening before’ defines an invariant partial ordering of the events in a distrib­uted multi­process system.”

Phrased differ­ently: Who should be in charge of time if putting someone in charge is not allowed? How can you have a reliable clock if there is no central frame of refer­ence?

You might think that solving this problem is easy because everyone could just use their own clock. This only works if every­one’s clock is accurate, and, more impor­tantly, everyone plays nice. In an adver­sarial system, relying on individual clocks would be a disaster. And, because of relativity, it does not work consis­tently across space.

As a thought exper­i­ment, imagine how you could cheat the system if everyone was in charge of keeping the time for themselves. You could pretend that the trans­ac­tion you’re sending now is actually from yesterday — it just got delayed for some reason — thus, you would still have all the money that you’ve spent today. Because of the asynchro­nous commu­ni­ca­tion that is inherent in every decen­tral­ized system, this scenario is more than a theoret­ical thought exper­i­ment. Messages do indeed get delayed, timestamps are inaccu­rate, and thanks to relativistic effects and the natural speed limit of our universe, it is anything but easy to tell apart the order of things absent of a central authority or observer.

<figure>
  <blockquote>
    <p>Who’s there? Knock knock.</p>
  </blockquote>
  <figcaption>An Asynchro­nous Joke</figcaption>
</figure>

To better illus­trate the impos­si­bility of the problem, let’s look at a concrete example. Imagine that you and your business partner both have access to your company bank account. You do business all over the world, so your bank account is in Switzer­land, you are in New York, and your business partner is in Sydney. For you, it is January 3^rd^, and you are enjoying a beautiful Sunday evening at your hotel. For her, it’s Monday morning already, so she decides to buy break­fast using the debit card of your shared bank account. The cost is $27. The avail­able balance is $615. The local time is 8:21 am.

At the same time, you are about to pay for your stay with another debit card linked to the same bank account. The cost is $599. The avail­able balance is $615. The local time is 5:21 pm.

<figure>
  <img src="/static/img/mempool/bitcoin-is-time/alice-bob-bank.jpg" alt="Alice and Bob at the Bank" />
</figure>

So it comes to be that — at exactly the same moment — you both swipe the card. What happens? (Dear physi­cists, please excuse my use of “the same moment” — we will ignore relativistic effects and the fact that there is no absolute time in our universe for now. We will also ignore that the concept of synchro­nous events doesn’t really exist. Bitcoin is compli­cated enough as it is!)

The central ledger at your bank will probably receive one trans­ac­tion before the other one, so one of you will be lucky, the other not so much. If the trans­ac­tions happen to arrive in the same *tick* — let’s say in the same millisecond — the bank would have to decide who gets to spend the money.

Now, what would happen if there was no bank? Who decides who was the first one to swipe? What if it wasn’t only you two, but hundreds or even thousands of people coordi­nating? What if you didn’t trust those people? What if some of those people are trying to cheat, e.g., by setting their clocks back so that it looks like they spent the money a couple of minutes earlier?

<figure>
  <blockquote>
    <p>A time-related tool [is] needed to estab­lish a canon­ical ordering and to enforce a unique history in the absence of any central coordi­nator.</p>
  </blockquote>
  <figcaption>Giacomo Zucco, <a href="https://bitcoinmagazine.com/articles/discovering-bitcoin-a-brief-overview-from-cavemen-to-the-lightning-network">“Discov­ering Bitcoin”</a> (2019)</figcaption>
</figure>

This problem is _precisely_ why all previous attempts of digital cash required a central­ized registry. You always had to trust someone to correctly identify the order of things. A central­ized party was required to keep the time.

Bitcoin solves this problem by re-inventing time itself. It says no to seconds and yes to blocks.

## Keeping the Time, One Block at a Time

<figure>
  <blockquote>
    <p>Time’s glory is to calm contending kings,<br />
    To unmask false­hood and bring truth to light,<br />
    To stamp the seal of time in aged things,<br />
    To wake the morn and sentinel the night,<br />
    To wrong the wronger till he render right;</p>
  </blockquote>
  <figcaption>William Shake­speare, <em>The Rape of Lucrece</em> (1594)</figcaption>
</figure>

All clocks rely on periodic processes, something that we might call a “tick.” The familiar _tick-tock_ of a grand­fa­ther’s clock is, in essence, the same as the molec­ular-atomic buzzing of our modern Quartz and Caesium clocks. Something swings — or oscil­lates — and we simply count these swings until it adds up to a minute or a second.

For large pendulum clocks, these swings are long and easy to see. For smaller and more special­ized clocks, special equip­ment is required. The frequency of a clock — how often it ticks — depends on its use-case.

Most clocks have a fixed frequency. After all, we want to know the time _precisely_. There are, however, clocks that have a variable frequency. A metronome, for example, has a variable frequency that you can set before you make it tick. While a metronome keeps its pace constant once it is set, Bitcoin’s time varies for each tick because its internal mecha­nism is proba­bilistic. The purpose, however, is all the same: keep the music alive, so the dance can continue.

<figure>
  <table>
    <thead>
      <tr>
        <th>Clock</th>
        <th>Tick Frequency</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Grandfather’s clock</td>
        <td>~0.5 Hz</td>
      </tr>
      <tr>
        <td>Metronome</td>
        <td>~0.67 Hz to ~4.67 Hz</td>
      </tr>
      <tr>
        <td>Quartz watch</td>
        <td>32,768 Hz</td>
      </tr>
      <tr>
        <td>Caesium-133 atomic clock</td>
        <td>9,192,631,770 Hz</td>
      </tr>
      <tr>
        <td>Bitcoin</td>
        <td>1 block (0.00000192901 Hz* to ∞ Hz**)</td>
      </tr>
    </tbody>
  </table>
  <figcaption>* first block<br />** timestamps between blocks can show a negative delta</figcaption>
</figure>

The fact that Bitcoin is a clock is hiding in plain sight. Indeed, Satoshi points out that the Bitcoin network as a whole acts as a clock, or, in his words: a distrib­uted timestamp server.

<figure>
  <blockquote>
    <p>In this paper, we propose a solution to the double-spending problem using a peer-to-peer distrib­uted timestamp server to generate compu­ta­tional proof of the chrono­log­ical order of trans­ac­tions.</p>
  </blockquote>
  <figcaption>Satoshi Nakamoto (2009)</figcaption>
</figure>

That timestamping was the root problem to be solved is also apparent by examining the refer­ence at the end of the Bitcoin whitepaper. Out of the eight refer­ences in total, three are about timestamping:

- “How to time-stamp a digital document” by S. Haber, W.S. Stornetta (1991)
- “Improving the efficiency and relia­bility of digital time-stamping” by D. Bayer, S. Haber, W.S. Stornetta (1992)
- “Design of a secure timestamping service with minimal trust require­ments” by H. Massias, X.S. Avila, and J.-J. Quisquater (May 1999)

As Haber and Stornetta outlined in 1991, digital time-stamping is about compu­ta­tion­ally practical proce­dures that make it infea­sible for a user — or an adver­sary, for that matter — to either back-date or forward-date a digital document. Contrary to physical documents, digital documents are easy to tamper with, and the change doesn’t neces­sarily leave any tell-tale signs on the physical medium itself. In the digital realm, forgeries and manip­u­la­tions can be perfect.

The malleable nature of infor­ma­tion makes time-stamping digital documents an elabo­rate and sophis­ti­cated process. Naive solutions do not work. Take a text document, for example. You can’t simply add the date at the end of the document since everyone — including yourself — could simply change the date in the future. You could also make up any date in the first place.

## Time is a Causal Chain

<figure>
  <blockquote>
    <p>In an extreme view, the world can be seen as only connec­tions, nothing else.</p>
  </blockquote>
  <figcaption>Tim Berners-Lee, <em>Weaving the Web</em> (1999)</figcaption>
</figure>

Making up dates is a general problem, even in the non-digital realm. What is known in the kidnap­ping world as “Authen­ti­ca­tion by Newspaper” is a general solution to the problem of arbitrary timestamps.

<figure>
  <img src="/static/img/mempool/bitcoin-is-time/proof-of-time.jpg" alt="Proof of Time" />
  <figcaption>Proof of Time</figcaption>
</figure>

This works because a newspaper is hard to fake and easy to verify. It is hard to fake because today’s front page refers to yester­day’s events, events that could not have been predicted by the kidnapper if the picture would be weeks old. By proxy of these events, the picture is proof that the hostage was still alive on the day the newspaper came out.

This method highlights one of the key concepts when it comes to time: _causality_. The arrow of time describes the causal relation­ship of events. No causality, no time. Causality is also the reason why crypto­graphic hash functions are so crucial when it comes to timestamping documents in cyber­space: they intro­duce a causal relation­ship. Since it is practi­cally impos­sible to create a valid crypto­graphic hash without having the document in the first place, a causal relation­ship between the document and the hash is intro­duced: the data in question existed first, the hash was gener­ated later. In other words: without the compu­ta­tional irreversibility of one-way functions, there would be no causality in cyber­space.

<figure>
  <img src="/static/img/mempool/bitcoin-is-time/sha256.jpg" alt="SHA-256" />
  <figcaption>A before B</figcaption>
</figure>

With this causal building block in place, one can come up with schemes that create a chain of events, causally linking A to B to C and so on. In that sense, secure digital timestamping moves us from a timeless place in the ether into the realm of digital history.

<figure>
  <blockquote>
    <p>Causality fixes events in time. If an event was deter­mined by certain earlier events, and deter­mines certain subse­quent events, then the event is sandwiched securely into its place in history.</p>
  </blockquote>
  <figcaption>Bayer, Haber, Stornetta (1992)</figcaption>
</figure>

It goes without saying that causality is of the utmost impor­tance when it comes to economic calcu­la­tions. And since a ledger is nothing but the embod­i­ment of economic calcu­la­tions of multiple cooper­ating partic­i­pants, causality is essen­tial for every ledger.

<figure>
  <blockquote>
    <p>We need a system for partic­i­pants to agree on a single history \[…\]. The solution we propose begins with a timestamp server.</p>
  </blockquote>
  <figcaption>Satoshi Nakamoto (2009)</figcaption>
</figure>

It is fasci­nating that all of the puzzle pieces that make Bitcoin work did already exist. As early as 1991, Haber and Stornetta intro­duced two schemes that make it “diffi­cult or impos­sible to produce false time-stamps.” The first relies on a trusted third party; the second, more elabo­rate “distrib­uted trust” scheme, does not. The authors even identi­fied the inherent problems of trusting a causal chain of events and what would be required to rewrite history. In their words, “the only possible spoof is to prepare a fake chain of time-stamps, long enough to exhaust the most suspi­cious challenger that one antic­i­pates.” A similar attack vector exists in Bitcoin today, in the form of a 51% attack (more on that in a later chapter).

One year later, Bayer, Haber, and Stornetta built upon their previous work and proposed to use trees instead of simple linked lists to tie events together. What we know as _Merkle Trees_ today are simply efficient data struc­tures to create a hash from multiple hashes deter­min­is­ti­cally. For timestamping, this means that you can efficiently bundle multiple events into one “tick.” In the same paper, the authors propose that the distrib­uted trust model intro­duced in 1991 could be improved by carrying out a recur­ring “world champi­onship tourna­ment” to deter­mine a single “winner” who widely publishes the resulting hash somewhere public, like a newspaper. Sounds familiar?

As we shall see, it turns out that newspa­pers are also an excel­lent way to think about the second ingre­dient of time: unpre­dictability.

## Causality and Unpredictability

<figure>
  <blockquote>
    <p>Time is not a reality [<em>hupostasis</em>], but a concept [<em>noêma</em>] or a measure [<em>metron</em>].</p>
  </blockquote>
  <figcaption>Antiphon the Sophist, <em>On Truth</em> (3rd century AD)</figcaption>
</figure>

While causality is essen­tial, it is not suffi­cient. We also need _unpre­dictability_ for time to flow. In the physical realm, we observe natural processes to describe the flow of time. We observe a general increase in entropy and call that the arrow of time. Even though the laws of nature seem to be obliv­ious in regards to the direc­tion of this arrow in most cases, certain things can’t be undone, practi­cally speaking. You can’t unscramble an egg, as they say.

Similarly, entropy-increasing functions are required to estab­lish an arrow of time in the digital realm. Just like it is practi­cally impos­sible to unscramble an egg, it is practi­cally impos­sible to unscramble a SHA256 hash or crypto­graphic signa­ture.

Without this increase in entropy, we could go forward and backward in time willy-nilly. The sequence of Fibonacci Numbers, for example, is causal but not entropic. Every number in the sequence is caused by the two numbers that came before it. In that sense, it is a causal chain. However, it is not useful to tell the time because it is entirely predictable. In the same way that a kidnapper can’t simply stand in front of a calendar that shows the current date, we can’t use predictable processes as proof of time. We always have to rely on something that can’t be predicted in advance, like the front page of today’s newspaper.

Bitcoin relies upon two sources of unpre­dictability: trans­ac­tions and proof-of-work. Just like nobody can predict what tomor­row’s newspaper will look like, nobody can predict what the next Bitcoin block will look like. You can’t predict what trans­ac­tions are going to be included because you can’t predict what trans­ac­tions are going to be broad­cast in the future. And, more impor­tantly, you can’t predict who will find the solution to the current proof-of-work puzzle and what this solution will be.

In contrast to the kidnap­per’s newspaper, however, proof-of-work is physi­cally linked to what happened _directly_. It is not just a record of an event — it is the event itself. It is the proba­bilistic direct­ness of proof-of-work that removes trust from the equation. The only way to find a valid proof-of-work is by making a lot of guesses, and making a single guess takes a little bit of time. The proba­bilistic sum of these guesses is what builds up the timechain that is Bitcoin.

By utilizing the causality of hash-chains and the unpre­dictability of proof-of-work, the Bitcoin network provides a mecha­nism for estab­lishing an indis­putable history of events witnessed. Without causality, what came before and what came after is impos­sible to tease apart. Without unpre­dictability, causality is meaning­less.

What is intuitively under­stood by every kidnapper was explic­itly pointed out by Bayer, Haber, and Stornetta in 1992: “To estab­lish that a document was created after a given moment in time, it is neces­sary to report events that could not have been predicted before they happened.”

<figure>
  <img src="/static/img/mempool/bitcoin-is-time/proof-of-publication.jpg" alt="Proof of Publication" />
  <figcaption>Proof of Publication</figcaption>
</figure>

It is the combi­na­tion of causality and unpre­dictability that allows the creation of an artifi­cial “now” in the other­wise timeless digital realm. As Bayer, Haber, and Stornetta point out in their 1991 paper: “the sequence of clients requesting time-stamps and the hashes they submit cannot be known in advance. So if we include bits from the previous sequence of client requests in the signed certifi­cate, then we know that the time-stamping occurred after these requests. \[…\] But the require­ment of including bits from previous documents in the certifi­cate also can be used to solve the problem of constraining the time in the other direc­tion, because the time-stamping company cannot issue later certifi­cates unless it has the current request in hand.”

All the puzzle pieces were already there. What Satoshi managed to do is put them together in a way that removes the “time-stamping company” from the equation.

## Proof of Time

<figure>
  <blockquote>
    <p><em>Causa latet: vis est notis­sima.</em></p>
    <p>The cause is hidden, but the result is known.</p>
  </blockquote>
  <figcaption>Ovid, <em>Metamor­phoses</em>, IV. 287 (8 AD)</figcaption>
</figure>

Let us recapit­u­late: to use money in the digital realm, we have to rely on ledgers. To make ledgers reliable, unambiguous order is required. To estab­lish order, timestamps are neces­sary. Thus, if we want to have _trust­less_ money in the digital realm, we must remove any entity that creates and manages timestamps and any single entity that is in charge of time itself.

It took a genius like Satoshi Nakamoto to realize the solution: “To imple­ment a distrib­uted timestamp server on a peer-to-peer basis, we will need to use a proof-of-work system similar to Adam Back’s Hashcash.”

We need to use a proof-of-work system because we need something that is native to the digital realm. Once you under­stand that the digital realm is infor­ma­tional in nature, the obvious conclu­sion is that compu­ta­tion is all we have. If your world is made of data, manip­u­la­tion of data is all there is.

Proof-of-work works in a peer-to-peer setting because it is _trust­less_, and it is trust­less because it is discon­nected from all external inputs — such as the readings of clocks (or newspa­pers, for that matter). It relies on one thing and one thing only: compu­ta­tion requires work, and in our universe, work requires energy and time.

## Bridging Times

<figure>
  <blockquote>
    <p>I know it works for me.<br />
    As we cross the bridge — the burning bridge —<br />
    With flames behind us,<br />
    We front the line.<br />
    It’s you and me, baby, against the world.</p>
  </blockquote>
  <figcaption>Kate Bush, “Burning Bridge” (1985)</figcaption>
</figure>

Without proof-of-work, one would always run into the Oracle problem because the physical realm and the infor­ma­tional realm are eternally discon­nected. The markings on your list of sheep aren’t your sheep, the map is not the terri­tory, and whatever was written in yester­day’s newspaper isn’t neces­sarily what happened in the real world. In the same manner, just because you use a real-world clock to write down a timestamp doesn’t mean that this is actually what the time was.

Put bluntly, there simply is no way to trust that data repre­sents reality, except if the reality in question is inherent in the data itself. The brilliant thing about Bitcoin’s diffi­culty-adjusted proof-of-work is that it creates its own reality, along with its own space and time.

Proof-of-work provides a direct connec­tion between the digital realm and the physical realm. More profoundly, it is the only connec­tion that can be estab­lished in a trust­less manner. Every­thing else will always rely on external inputs.

The diffi­culty to mine a new Bitcoin block is adjusted to make sure that the thin thread between Bitcoin’s time and our time remains intact. Like clock­work, the mining diffi­culty readjusts every 2016 ticks. The goal of this readjust­ment is to keep the _average_ time between ticks at ten minutes. It is these ten minutes that maintain a stable connec­tion between the physical and the infor­ma­tional realm. Conse­quently, a sense of human time is required to readjust the ticks of the Bitcoin clock. A purely block-based readjust­ment wouldn’t work since it would be completely discon­nected from our human world, and the whole purpose of the readjust­ment is to stop us ingenious humans from finding blocks too fast (or too slow).

As Einstein has shown us, time is not a static thing. There is no such thing as a universal time we could rely upon. Time is relative, and simul­taneity is nonex­is­tent. This fact alone makes all timestamps — especially across large distances — inher­ently unreli­able, even without adver­sarial actors. (This is why timestamps of GPS satel­lites have to be adjusted constantly, by the way.)

For Bitcoin, the fact that our human timestamps are impre­cise doesn’t matter too much. It also doesn’t matter that we have no absolute refer­ence frame in the first place. They only have to be precise enough to calcu­late a somewhat reliable average across 2016 blocks. To guarantee that, a block’s “meatspace” timestamp is only accepted if it fulfills two criteria:

1. The timestamp has to be greater than the median timestamp of the previous 11 blocks.
2. The timestamp has to be less than the network-adjusted time plus two hours. (The “network-adjusted time” is simply the median of the timestamps returned by all nodes connected to you.)

In other words, the diffi­culty-adjust­ment is about keeping a constant time, _not_ a constant level of security, diffi­culty, or energy expen­di­ture. This is ingenious because good money _has_ to be costly in time, not energy. Linking money to energy alone is not suffi­cient to produce absolute scarcity since every improve­ment in energy gener­a­tion would allow us to create more money. Time is the only thing we will never be able to make more of. It is _The Ultimate Resource_, as Julian Simon points out. This makes Bitcoin the ultimate form of money because its issuance is directly linked to the ultimate resource of our universe: time.

The diffi­culty adjust­ment is essen­tial because, without it, the internal clock of Bitcoin would tend to go faster and faster as more miners join the network or the efficiency of mining devices improves. We would quickly run into the coordi­na­tion problem that Bitcoin sets out to solve. As soon as the block time falls below a certain threshold, say, 50 millisec­onds, it would be impos­sible to agree on a shared state, even in theory. It takes light around 66 millisec­onds to travel from one side of the earth to the other. Thus, even if our computers and routers were perfect, we would be back at square one: given two events, it would be futile to tell which event happened before and which event happened after. Without a periodic adjust­ment of Bitcoin’s ticks, we would run into the hopeless problem of solving the coordi­na­tion problem faster than the speed of light. Time is also at the root of the problem of crypto­graphic insta­bility, which was outlined in [Chapter 1](https://21-ways.com/1/). Cryptog­raphy works because of an asymmetry in time: it takes a short time to build a crypto­graphic wall and a long time to break it down — unless you have a key.

Thus, in some sense, proof-of-work — and the diffi­culty adjust­ment that goes along with it — artifi­cially slows down time, at least from the perspec­tive of the Bitcoin network. In other words: Bitcoin enforces an internal rhythm whose low frequency allows ample buffer for the latency of commu­ni­ca­tions between peers. Every 2016 blocks, Bitcoin’s internal clock readjusts, so that — on average — only one valid block will be found every 10 minutes.

From an outside perspec­tive, Bitcoin funnels the chaotic mess of globally broad­cast asynchro­nous messages into a parallel universe, restricted by its own rules and its own sense of space and time. Trans­ac­tions in the mempool are timeless from the point-of-view of the Bitcoin network. Only when a trans­ac­tion is included in a valid block does it get assigned a time: the number of the block it is included in.

<figure>
  <img src="/static/img/mempool/bitcoin-is-time/timechain.png" alt="Timechain" />
  <figcaption>BitCoin v0.01 ALPHA (2009)</figcaption>
</figure>

It is hard to overstate how elegant a solution this is. Once you are able to create your own defin­i­tion of time, deciphering what came before and what came after is trivial. In turn, agreeing on what happened, in what order, and, conse­quently, who owes what to whom, becomes trivial as well.

The diffi­culty adjust­ment makes sure that the _ticks_ of Bitcoin’s internal metronome are somewhat constant. It is the conductor of the Bitcoin orchestra. It is what keeps the music alive.

But why can we rely on work in the first place? The answer is three­fold. We can rely on it because compu­ta­tion requires work, work requires time, and the work in question — guessing random numbers — can not be done efficiently.

## Probabilistic Time

<figure>
  <blockquote>
    <p>Time forks perpet­u­ally toward innumer­able futures.</p>
  </blockquote>
  <figcaption>Jorge Luis Borges, <em>The Garden of Forking Paths</em> (1941)</figcaption>
</figure>

Finding a valid nonce for a Bitcoin block is a guessing game. It is very much like rolling a die, or flipping a coin, or spinning a roulette wheel. You are, in essence, trying to find a beyond-astro­nom­i­cally large random number. There is no progress toward finding a solution. You either hit the jackpot, or you don’t.

Every time you flip a coin, the chance of it coming up heads or tails is 50% — even if you flipped it twenty times before, and it came up heads every time. Similarly, every time you wait for a bitcoin block to come in, the chance that it will be found _this second_ is ~0.16%. It doesn’t matter when the last block was found. The approx­i­mate waiting time for the next block is always the same: ~10 minutes.

It follows that every individual tick of this clock is unpre­dictable. Relative to our human clocks, this clock appears to be sponta­neous and impre­cise. This is irrel­e­vant, as Gregory Trubet­skoy points out: “It doesn’t matter that this clock is impre­cise. What matters is that it is the same clock for everyone and that the state of the chain can be tied unambigu­ously to the ticks of this clock.” Bitcoin’s clock might be proba­bilistic, but it isn’t illusory.

<figure>
  <blockquote>
    <p>Time is an illusion,<br />
    lunchtime doubly so.</p>
  </blockquote>
  <figcaption>Douglas Adams (1979)</figcaption>
</figure>

The present moment, however, can absolutely be an illusion in Bitcoin. Since there is no central authority in the network, strange situa­tions can arise. While unlikely, it is possible that two valid blocks are found at the same time (again: apolo­gies to all physi­cists), which will make the clock tick forward in two different places at once. However, since the two different blocks will very likely differ in their content, they will contain two different histo­ries, both equally valid.

This is known as a chain split and is a natural process of Nakamoto consensus. Like a flock of birds that briefly splits in two only to merge again, nodes on the Bitcoin network will eventu­ally converge to a shared history after some time, thanks to the proba­bilistic nature of guessing.

Nakamoto consensus simply states that the correct history is to be found in the heaviest chain, i.e., the chain with the most amount of proof-of-work embedded in it. Thus, if we have two histo­ries A and B, some miners will try to build upon history A, others will try to build upon history B. As soon as one of them finds the next valid block, the other group is programmed to accept that they were on the wrong side of history and switch over to the heaviest chain — the chain that repre­sents what actually happened, by defin­i­tion. In Bitcoin, history is truly written by the victors.

<figure>
  <blockquote>
    <p>The payee needs proof that at the time of each trans­ac­tion, the majority of nodes agreed it was the first received. […] When there are multiple double-spent versions of the same trans­ac­tion, one and only one will become valid. The receiver of a payment must wait an hour or so before believing that it’s valid. The network will resolve any possible double-spend races by then.</p>
  </blockquote>
  <figcaption>Satoshi Nakamoto (2009)</figcaption>
</figure>

In this simple state­ment lies the secret of the distrib­uted coordi­na­tion problem. This is how Satoshi solved the problem of the “simul­ta­neous payment” our ficti­tious business partners encoun­tered previ­ously. He solved it once and for all, relativistic effects be damned!

Because of this proba­bilistic nature of Bitcoin’s clock, the present moment — what we call the chain tip — is always uncer­tain. The past — blocks buried below the chain tip — is ever more certain.

<figure>
  <blockquote>
    <p>The more thorough the under­standing needed, the further back in time one must go.</p>
  </blockquote>
  <figcaption>Gordon Clark, <em>A Chris­tian View of Men and Things</em>, p. 58. (1951)</figcaption>
</figure>

Conse­quently, the Bitcoin clock might rewind from time to time, for some peers, for a tick or two. If your chain tip — the present moment — happens to lose to a competing chain tip, your clock will first rewind and then jump forward, overriding the last few ticks that you thought were history already. If your clock is proba­bilistic, your under­standing of the past has to be too.

<figure>
  <blockquote>
    <p>Tick tock tick tock tick — what is the time?<br />
    Tick tock tick tock… it ends in <a href="https://www.blockstream.info/block/000000000000000000095eaf76a73a7986ea2e6a3b0d190fb10ab986b683c619">c619</a>.<br />
    Are you sure this is fine? Are we probably late?<br />
    Absolutes do not matter: before nine there comes <a href="https://www.blockstream.info/block/0000000000000000000318291249db2c9b658d087e4f06bcd2ed24481e81533c">eight</a>.<br />
    The clock isn’t exact; it sometimes goes in reverse.<br />
    Exact time implies center; that’s the root of this curse!<br />
    Yet this clock keeps on ticking, tock-tick and tick-tock,<br />
    there’s no profit in tricking; just tick-tock and next block.</p>
  </blockquote>
  <figcaption>A Funny Little Rhyme on Bitcoin and Time (2020)</figcaption>
</figure>

## Conclusion

<figure>
  <blockquote>
    <p>Time is still one of the great mysteries in physics, one that calls into question the very defin­i­tion of what physics is.</p>
  </blockquote>
  <figcaption>Jorge Cham and Daniel Whiteson: <em>We Have No Idea: A Guide to the Unknown Universe</em>, pp. 117 – 118 (2017)</figcaption>
</figure>

Keeping track of things in the infor­ma­tional realm implies keeping track of a sequence of events, which in turn requires keeping track of time. Keeping track of time requires agreeing on a “now” — a moment in time that eternally links the settled past with the uncer­tain future. In Bitcoin, this “now” is the tip of the heaviest proof-of-work chain.

Two building blocks are essen­tial for the struc­ture of time: causal links and unpre­dictable events. Causal links are required to define a past, and unpre­dictable events are required to build a future. If the sequence of events would be predictable, it would be possible to skip ahead. If the individual steps of the sequence aren’t linked, it would be trivial to change the past. Because of its internal sense of time, it is insanely diffi­cult to cheat Bitcoin. One would have to rewrite the past or predict the future. Bitcoin’s timechain prevents both.

Viewing Bitcoin through the lens of time should make clear that the “block chain” — the data struc­ture that causally links multiple events together — is not the main innova­tion. It is not even a new idea, as is evident by studying the timestamp liter­a­ture of the past.

<figure>
  <blockquote>
    <p>A blockchain is a chain of blocks.</p>
  </blockquote>
  <figcaption>Peter Todd (2014)</figcaption>
</figure>

What is a new idea — what Satoshi figured out — is how to indepen­dently agree upon a history of events without central coordi­na­tion. He found a way to imple­ment a decen­tralised timestamping scheme that (a) doesn’t require a time-stamping company or server, (b) doesn’t require a newspaper or any other physical medium as proof, and (c) can keep the _ticks_ more-or-less constant, even when operating in an environ­ment of ever-faster CPU clock times.

Timekeeping requires _causality_, _unpre­dictability_, and _coordi­na­tion_. In Bitcoin, _causality_ is provided by one-way functions: the crypto­graphic hash functions and digital signa­tures that are at the core of the protocol. _Unpre­dictability_ is provided by both the proof-of-work puzzle as well as the inter­ac­tion with other peers: you can’t know in advance what others are doing, and you can’t know in advance what the solution to the proof-of-work puzzle will be. _Coordi­na­tion_ is made possible by the diffi­culty adjust­ment, the magic sauce that links Bitcoin’s time to ours. Without this bridge between the physical and the infor­ma­tional realm, it would be impos­sible to agree on a time by relying on nothing but data.

**Bitcoin is time** in more ways than one. Its units are stored time because they are money, and its network is time because it is a decen­tral­ized clock. The relent­less beating of this clock is what gives rise to all the magical proper­ties of Bitcoin. Without it, Bitcoin’s intri­cate dance would fall apart. But with it, everyone on earth has access to something truly marvelous: Magic Internet Money.

---

[_Bitcoin Is Time_](https://21-ways.com/2) is a chapter of my upcoming book [21 Ways](https://21-ways.com/).
