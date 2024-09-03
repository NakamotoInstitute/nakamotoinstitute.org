---
title: Credit with Privity
authors:
  - nick-szabo
date: 1996
display_date: Originally published in 1996
categories:
  - economics
  - technology
doctype: essay
external: https://web.archive.org/web/20160323114322/http://szabo.best.vwh.net/garnishment.html
---

One of the basic outstanding problems in [smart contracts](https://web.archive.org/web/20160323114322/http://szabo.best.vwh.net/smart_contracts_2.html) is the ensurement of credit. This comes up not only in loans, but in any other contract which involves a temporal lag between performance and reciprocal performance of the contractual terms. Currently there are several partially effective processes for ensuring such performance:

- Reputation (especially credit reports): often effective, but only to a point, as it is often hard for the debtor to accurately judge the future reputational effects of an action (eg failure to pay a bill, taking out too large a loan, etc.) that has clear, local, beneficial effects today. There is more imbalance in knowledge between current and distant consequences among individual consumers, but even among large organizations with high credit ratings it is not an irrelevant factor.
- Secured transactions: liens, escrow, etc.
- Garnishment of future income
- Law enforcement, especially to enforce transfer of control over liened assets, garnishment, etc.

These processes have a fundamental property in common—they violate the [privity](/smart-contracts-glossary/#privity) of credit transactions—they bring in third parties to track reputations or enforce repayment. Credit transactions seem to entail a fundamental imbalance in incentives that can only be redressed by bringing in third parties.

## Kinds of Credit

In thinking about how distributed security protocols might assist with credit enforcement issues, it will help to categorize the kinds of credit. I'm not sure this classification is exhaustive or makes all the right distinctions, but it's a good start.

<pre>
Performance Bonds
    Bond controlled by counterparty
    Bond controlled by third party
        Digital ripped instruments
        Escrows
Unsecured Loans
    student loans
    some business loans
Secured Loans
    Against property held by debtor
        consumer: auto, home, etc.
        business assets
    Against property held by creditor
        balance (margin, insurance, etc.)
        pawning
</pre>

It's reasonable that performance bonds and loans secured by property held by the creditor can be anonymous. It's less precedented, but plausible, that small unsecured loans may be made to highly reputed pseudonyms even in case of lack of recourse to real people or property.

To make loans secured against property held by the debtor, we would need protocols that allow shared control over that property, protocols which allow the debtor to operate the property unless payments are defaulted, in which case full control reverts to the creditor. This may be plausible for some kinds of digitally controlled machinery, for example [automobiles](/the-idea-of-smart-contracts/).

## Secured Credit

Secured credit need not violate privity if the physical control over the securing property can be shared. So that, for example, automobile credit can be secured as long as reposession is possible. The trick is to make repossession by the creditor easy but theft by third parties difficult. I have proposed [smart liens](https://web.archive.org/web/20160323114322/http://szabo.best.vwh.net/smart_contracts_2.html#smartlien), electronic security measures strong against third parties but with a &quot;back door&quot; for creditors. This well-specified, shared control over smart property more accurately reflects the agreement involving that property, so that there is less need for third parties. To even more accurately reflect the contract, we need a mechanism to eliminate the credit control once the auto loan has been payed off.

Markus Jakobsson has proposed a system of trustees for shielding the identity of borrowers from lenders, with the trustees issuing [digital cash like tokens](/contracts-with-bearer/). A property owner registers his property as a potential security by signing over to trustees the right to seize it under certain conditions, or to reveal the identity of the owner to law enforcement in order that the property be seized. The trustees would share among them (I propose using [threshold cryptography](https://web.archive.org/web/20160323114322/http://theory.stanford.edu/~dabo/ITTC/) for this purpose) a list of all property one might wish to ever use as an anonymous security. To secure a loan, the borrower "spends" the token with the lender. If the borrower fails to pay off the loan, the trustee seizes the property for the creditor, or revokes anonymity in order that the property beseized. Whether one can construct a [quorum system](https://web.archive.org/web/20160323055901/http://szabo.best.vwh.net/coalition.html) of trustees trustworthy to both borrowers and creditorsis an open question. The trustees must continue to monitor, or have legal or [digital](/the-idea-of-smart-contracts/) control over property for which it has issued tokens, to makesure it is not covertly resold. Such trustees could effectively unbundle the timing and amounts of anonymous loans and repaymentsfrom identified collection enforcement, similar to the [loan mix](#mix) idea.

## Performance Bonds — Ripped Instruments

Alice wants a New York City cab ride for which she's willing to pay $100, but she doesn't trust Bob the taxi driver to get her there on time if she pays up front. Bob in turn doesn't trust Alice to pay at the end of the trip. Commerce can be consumated by Alice tearing a $100 bill and giving half to Bob. After the trip she gives the other half to Bob, which he can then reassemble into a negotiable $100 bill. Alice loses her incentive to not pay. Bob gains incentive to get her there on time as promised. Both have made what economists call a &quot;credible commitment&quot; to perform their respective parts of the contract. [Markus Jacobsson](https://web.archive.org/web/20070813222103/http://www.cse.ucsd.edu/users/markus/) has digitized this idea, coming up with a protocol for [ripped digital cash](https://web.archive.org/web/20070615111511/http://www.informatics.indiana.edu/markus/papers/rip.pdf). As with many other aspects of digital cash, the idea can be further generalized to rip some other kinds of bearer instruments—specifically, those whose value can be divided roughly in half. If the transfer is double-blinded the clearing agent has no knowledge of the participants and therefore no bias to favor one over the other. The clearing agent must, however, be able to assess proof of performance, and the protocol is only workable where such proof (in the form of proof of receipt of a message, for example) is available.

Financially, the ripped bill is equivalent to using the clearing agent as an escrow agent. An advantage over using an escrow agent is that the need for extra anonymous channels between the parties and the escrow is avoided. A disadvantage is that the clearing agent now has taken on the major additional job of acting as an arbitrator, assessing proofs of performance (or at the very least, must be responsible for subcontracting out this job and implementing the arbitrator's judgement).

## Unsecured Credit — Garnishment

Similar mechanisms might be possible for other kinds of security (houses, escrow accounts, etc.), but many valuable kinds of credit are unsecured, and we run into privity problems when it comes to garnishment of future income. Here, we are invoking third parties, namely the debtor's future contract counterparties. Any mechanism seemingly needs to involve them, but both principals to these contracts have an incentive to enter a private, ungarnished contract in preference to one involving the creditor. (ie, the amount of garnishment is a surplus to be divided between principals who can route around it).

A way to a solution, if it were feasible, would be to give the creditor shared control over the entire scope of of the debtor's income capabilities - or, a bit closer to practicality, over the entire scope of his digital income capabilities. A secondary solution is some combination of wide scope and limited compromise of privity. After all, money itself is a compromise of privity, since the contract parties rely on third parties to clear and maintain the value of the currency. Money's [compromise of privity is well-defined](/library/delegation-and-agreement-based-certification-policy/), however, not an open-ended release of information and physical control, even over one's own person, as often occurs with credit reports and law enforcement respectively. Our challenge is to find privity compromises with such well-defined limits to ensure credit transactions.

One possibility here is a &quot;garnishable currency&quot;. All banks have an interest in enforcing credit, so they can make deals with each other to ensure credit via the garnishment of debtor bank account deposits at any participating bank. However, substantial amounts of garnishment (and if it provides a lower cost way of enforcing credit the amounts will be substantial) gives rise to an incentive for banks to fail to participate. Here the need to commonly clear a currency between banks can be used as a barrier to entry for such defectors. The currency is simply declared garnishable, and any banks who wish to deal in the currency must participate in the garnishing process. This currency wins against competitor currencies in a free-banking market because it provides a better means to ensure credit, allowing greater credit expansion at lower risk.

On the other hand, traditional coin and currency transfers, and some kinds of digital cash transfers, need not involve deposits to bank accounts linked (usually by [True Name](/smart-contracts-glossary/#truename), but a &quot;debtor nym&quot; could also work) to one's unsecured debts, and given that there is a market for these kinds of transfers for other reasons, its existence allows banks to defeat auditing of garnishment by other banks participating in that currency. Abuses of financial auditing for the purposes of extortion, inside information, etc. will likely maintain a major market for the non-deposit payment methods. We need a way for banks (and perhaps other third parties) to audit garnishing without violating the privity of the particular loan and garnishment transactions—a [confidential auditing protocol](/distributing-authorities-and-verifying-their-claims/#mutually-confidential-auditing). Such auditing protocols are already needed for the clearing itself.

## Interval Instruments

Tim May has proposed a &quot;time release&quot; form of money that becomes good only after a certain date. &quot;Interval money&quot; that would expire after a certain date has also been proposed. These can probably be implemented by a digital mint expiring or activating special issues of digital cash, or by a third party issuing escrowed keys at specific times (since these keys are encrypted against the escrow agent, and that agent doesn't know what they will be used for, the escrow agent has no incentive to cheat). A generalization of this is that transfer and redeemability are each associated with interval sets, or validity periods when each can and cannot be performed. Clipping coupons on bonds is an example of this.

<h2 name="mix">Known Borrowers of Unknown Amounts</h2>

Hal Finney and Wei Dai have described a loan mix, similar to the instrument transfer and message mixes invented by David Chaum, to unlink borrowers from amount borrowed. The identity of the borrowers is still public, as well as the system for enforcing payment, but the actual amount borrowed remains unknown. The system starts with participants putting unknown amounts into a pot and getting receipts (bearer certificates) for these amount. All participants then borrow a standard amount. Whether a participant is a net borrower or a net creditor, and of what amount, remains private. When the loan is due borrowers repay the standard amount, and the creditors reclaim the amounts on their bearer certificates. The amount actually borrowed (or, if negative, loaned) is the public amount borrowed minus the amount put into the pot. One consequence is that while [negative reputation information](/negative-reputations/) can still be accumulated when participants fail to pay back the standard amount, positive reputation information cannot, since participants who borrow and loan are indistinguishable.

## References

Markus Jacobsonn, [&quot;Ripping Coins for a Fair Exchange&quot;](https://web.archive.org/web/20070615111511/http://www.informatics.indiana.edu/markus/papers/rip.pdf)

---

Please send your comments to nszabo (at) law (dot) gwu (dot) edu

---

_Editor's note: Some links may be broken._
