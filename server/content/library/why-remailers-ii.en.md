---
title: Why Remailers II
authors:
  - hal-finney
date: 1993-02-24
categories:
  - cryptography
  - privacy
doctype: essay
external: https://web.archive.org/web/20130513043044/http://finney.org/~hal/why_rem2.html
---

Paul Ferguson asks:

> Now, I'd like to ask the cypherpunk readership to clarify the need (or perhaps a better term may be "desire") for anonymous remailers? Maybe I'm not getting the "big picture", but it would appear to me that insurance of private communications is the area of intended interest here. I know that someone may declare my query as naive, but if you feel strongly enough about a topic, why wouldn't you want the recipient to know who you are, where you are and who they can respond to?

There are several different advantages provided by anonymous remailers. One of the simplest and least controversial would be to defeat traffic analysis on ordinary email.

Two people who wish to communicate privately can use PGP or some other encryption system to hide the content of their messages. But the fact that they are communicating with each other is still visible to many people: sysops at their sites and possibly at intervening sites, as well as various net snoopers. It would be natural for them to desire an additional amount of privacy which would disguise who they were communicating with as well as what they were saying.

Anonymous remailers make this possible. By forwarding mail between themselves through remailers, while still identifying themselves in the (encrypted) message contents, they have even more communications privacy than with simple encryption.

(The Cypherpunk vision includes a world in which literally hundreds or thousands of such remailers operate. Mail could be bounced through dozens of these services, mixing in with tens of thousands of other messages, re-encrypted at each step of the way. This should make traffic analysis virtually impossible. By sending periodic dummy messages which just get swallowed up at some step, people can even disguise when they are communicating.)

The more controversial vision associated with anonymous remailers is expressed in such science fiction stories as "True Names," by Vernor Vinge, or "Ender's Game," by Orson Scott Card. These depict worlds in which computer networks are in widespread use, but in which many people choose to participate through pseudonyms. In this way they can make unpopular arguments or participate in frowned-upon transactions without their activities being linked to their true identities. It also allows people to develop reputations based on the quality of their ideas, rather than their job, wealth, age, or status.

The idea here is that the ultimate solution to the low signal-to-noise ratio on the nets is not a matter of forcing people to "stand behind their words." People can stand behind all kinds of idiotic ideas. Rather, there will need to be developed better systems for filtering news and mail, for developing "digital reputations" which can be stamped on one's postings to pass through these smart filters, and even applying these reputations to pseudonyms. In such a system, the fact that someone is posting or mailing pseudonymously is not a problem, since nuisance posters won't be able to get through.

Other advantages of this approach include its extension to electronic on-line transactions. Already today many records are kept of our financial dealings - each time we purchase an item over the phone using a credit card, this is recorded by the credit card company. In time, even more of this kind of information may be collected and possibly sold. One Cypherpunk vision includes the ability to engage in transactions anonymously, using "digital cash," which would not be traceable to the participants. Particularly for buying "soft" products, like music, video, and software (which all may be deliverable over the net eventually), it should be possible to engage in such transactions anonymously. So this is another area where anonymous mail is important.

We anticipate that computer networks will play a more and more important role in many parts of our lives. But this increased computerization brings tremendous dangers for infringing privacy. Cypherpunks seek to put into place structures which will allow people to preserve their privacy if they choose. No one will be forced to use pseudonyms or post anonymously. But it should be a matter of choice how much information a person chooses to reveal about himself when he communicates. Right now, the nets don't give you that much choice. We are trying to give this power to people.

Hal Finney  
_hal@rain.org_
