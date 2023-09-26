---
title: Micropayments and Mental Transaction Costs
authors:
  - nick-szabo
date: 1999-05
formats:
  - pdf
categories:
  - economics
doctype: essay
external: http://szabo.best.vwh.net/berlinmentalmicro.pdf
mathjax: true
numbered_headers: true
---

We present intuitive arguments for why micropayments have not succeeded on the Internet. The "hassle factor" for customers asso ciated with such transactions is characterized. A framework of mental transaction costs and price granularity is then presented, and arguments ab out micropayments recast in its light. Finally, we make some suggestions for reducing the mental transaction costs of Internet commerce.

## Introduction

Some Internet payment system pro jects promise dramatically lower transaction costs, so that we can achieve micropayments (e.g. <a href="#fnBe95" id="refBe95">[Be95]</a>, <a href="#fnGMAGS95" id="refGMAGS95">[GMAGS95]</a>, <a href="#fnRS96" id="refRS96">[RS96]</a>). Other projects propose more sophisticated forms of microtransaction <a href="#fnMD88" id="refMD88-1">[MD88]</a>. To what extent can transction costs be reduced in these ways? This paper will argue that mental transaction costs raise fundamental barriers to customer acceptance of fine grained bundling and pricing. We will explore the problems both informally and through a closer examination of three sources of customer cognitive expenditures.

These mental accounting costs, not the physical or computation or amortized R&D costs of a payment or billing method, set the main lower bound on price granularity. Judging from price granularity is far above suggested micropayment levels of a few cents or even fractions of a cent. The mental accounting costs for a typical on-line consumer seem to be somewhat higher than those in more familiar areas of commerce.

Customer mental transaction costs come from at least three sources: uncertain cashflors, incomplete and costly observation of product attributes, and incomplete and costly decision making.

### Cognitive Versus Technological Transaction Costs

For electronic commerce economics, it's important to distinguish between technological and mental transaction costs. When technologists talk about transaction costs, they are usually talking about computation and network costs. Thus the claim that micropayment technologies, which dramatically reduce these costs, will reduce "transaction costs." The significance of such technological reductions depends on the accompanying cognitive costs already being very low, since these payments don't address cognitive costs.

Economists (e.g. <a href="#fnBz82" id="refBz82-1">[Bz82]</a>, <a href="#fnW85" id="refW85-1">[W85]</a>, <a href="#fnH89" id="refH89">[H89]</a>), on the other hand, usually, when using the term "transaction costs," refer implicitly to cognitive costs. One goal of this paper is to make these assumptions explicit. Sometimes these mental transaction costs can be reduced with the aid of technology: whence the claim that tools like Internet search engines can reduce the transaction costs associated with comparing the attributes of goods and services.

In examining micropayments, this paper will assume that the technological costs of the payment system itself are zero, and will examine what limits are set by the mental transaction costs associated with the retail transactions targeted by micropayments. We will explore the possibilities of, and barriers to, automating, and thus potentially greatly reducing, the mental processes which impose mental transaction costs.

This paper examines decision processes which take place in the mind of the customer rather than on a computer, as well as the bottlenecks which are caused by the need to communicate between a computer and that mental process. Also, we discuss some related basic barriers to automated shopping.

This paper argues that customer mental transaction costs are significant and ubiquitous, so much so that in real world circumstance cognitive costs usually well outweight technological costs, and indeed technological resources are best applied towards the objective of reducing cognitive costs. Furthermore, technological costs will continue to fall while cognitive costs remain constant, and (more arguably) will fall faster than technological cost can be substituted for mental costs by discovering and automating the relevant mental processes. Customer mental transaction costs will soon dominate the technological transaction costs of the payment system used in the transaction (if they don't already), and micropayment technology efforts which stress technological savings over cognitive savings will become irrelevant. This paper will suggest some ways to achieve cognitive savings.

### Supplier Cost Structure

<a href="#fnBB97" id="refBB97">[BB97]</a> and <a href="#fnFOS97" id="refFOS97-1">[FOS97]</a> discuss bundling, and thus price granularity, from the supplier's point of view. When marginal costs are small compared to amortization of fixed cost (e.g. a particular content work, much Internet infrastructure, etc.) it makes no sense, in the face of customer preference for flat pricing, to charge fine per unit costs to amortize a one-time investment, except in some exceptional cases, such as where congestion pricing provides major improvements in service quality. This paper provides explanations for a strong customer preference for flat pricing. These are so significant, we suggest that customer cognitive costs outweigh congestion pricing and supplier cost structure issues at micropayment levels in almost all retail markets. In contrast to previous work, this paper focuses on costs imposed on customers by bundling and price granularity decisions.

## Informal Arguments Against Micropayments

Consider a feature fairly independent of the particular payment system: the statment of charges. Here lies a tradeoff etween completeness and complexity. On the one hand, merely summarizing changes creates the opportunity for salami frauds, allowing widely distributed false or exaggerated microcharges to go undetected. Furthermore, parties reading only the summaries get no feedback by which they can adjust their behavior to minimize costs. On the other hand, a statement too complex for customers to read also allows fraud, error, and inefficient usage to go undetected, because one or both parties cannot understand the rationale for the charges in relation to the presumed aggrement on terms of service and payment. The same kind of reasoning applies to working these things out in the head instead of on paper, as is often done in small cash transactions. A basic requirement for market pricing to work is that both sides to a transaction be able to map charges to value obtained or rendered, so that they can adjust their buying or selling behavior accordingly.

There seem here to be a fundamental cognitive bottleneck. One proposed solution to this has been "intelligent agents." But since these agents are programmed remotely, not by the consumer, it is difficult for the consumer to determine whether the agent is acting in the consumer's best interests, or in the best interests of the counterparty—perhaps, necessarily, at least as difficult as reading the corresponding full statement of charges. Furthermore, the user interface to enable consumer to simply express their sophisticated preferences to an agent is lacking, and may represent another fundamental cognitive bottleneck.

Communications companies have found billing to be a major bottleneck. By some estimates, up to 50% of the costs of a long distance call are for billing, and this is on the order of a $100 billion per year market worldwide[4]. Internet providers have been moving to a flat fee in order to minimize these costs, even though this creates the incentive for a network resource overusage.

A micropayments system assumes a solution to the mental accounting problem. If somebody could actually solve the problem, rather than merely claiming to have solved it via some mysterious mean ("intelligent agents", et. al.), the savings would be enormous even in existing business such as long distance and Internet service—not to mention all the new business models made possible by lower transaction costs (e.g., <a href="#fnMD88" id="refMD88-2">[MD88]</a>).

## Example - Electicity Bills

Sometimes statements accounts for transactions in gratuitously small increments, such as the 100 watt-hour resolution on some electricity bills. There are plenty of things most people normally don't work out regarding their electricity bills, which could improve the value they get for their electricity payments:

- Which appliances are using more electricity with less personal benefit (not available on the electricity bill—but one can conceive of a personal accounting program tied to smart appliances that let you do this).
- How to better balance electric vs. gas heat (you could compute this in detail and save a few bucks, but you'd earn extra money faster by moonlighting).
- If the electricity company was a less reliable and widely known entity, you also might not trust them with the billing and would recomputer it to the resolution you felt comfortable with, and accept fraud or fine-print trickery below that level. (Since electricity is fungible and the pricing ruleset is small you could have a program check the bill, which is efficient if it catches enough fine-print shenanigans for enough people to recoup software development and marketing costs).

The reason we don't do these things is that they're not worth the brain cycles: we have reached a mental accounting barrier.

## Price Granularity

We can characterize four ways to set prices:

1. negotiated price
2. congestion pricing (variable but posted price/small value unit)
3. fungible (one price/small value unit)
4. flat fee (one price/large value unit)

Each of these levels successively imposes fewer mental transaction costs on the customer than the previous level.

Haggling is a good example of the substantial role mental transaction costs play in economies. There occurs historically and across societies a great decline of retail bargaining as societies grow wealthier. Retail prices become a smaller total fraction of customer wealth. For similar reasons, which are the subject of this paper, prices themselves can become irrelevant at sufficiently small fractions of customer wealth.

### Attributes and Preferences

What does it mean when an economist says a person "prefers" good X to good Y? Often economists just measure this by how much the person is willing to pay for X versus how much for Y. We call this the "supplier observed explicit preference."

Barzel <a href="#fnBz82" id="refBz82-2">[Bz82]</a> gives the example of an apple: the customer prefers and apple that tastes good. The customer cannot adequately describe this taste to another person or to software <a href="#fnP58" id="refP58-1">[P58]</a>. Furthermore, this attribute cannot be observed while shopping. This we call a _tacit preference_. Instead the customer uses an observable attribute, e.g. the color, as a proxy attribute. We call this a _customer observed explicit preference_. Suppliers can often also observe these attributes mapped to the customer behavior, and thus the corresponding explicit (revealed) preference.

The differences between these kinds of preferences are usually glossed over. However, they become important if, for example, we wish to have the user choose among goods, or delegate this task to a software agent by communicating his preferences to that software.

This model of preferences will be developed further in subsequent sections.

### The Function of Prices

Our account of price granularity is based on a subjectivist (<a href="#fnM35" id="refM35">[M35]</a>, <a href="#fnH45" id="refH45">[H45]</a>) view of prices. The function of prices, from the point of view of a customer, is to let the shopepr map his personal resources (budget) to his tacit preferences (unique and not directly observable). This requires a significant cognitive effort, which sets the most basic lower bounds on transaction costs. For example, comparing the personal value of a large, diverse set of low-priced goods might require a mental expenditure greater than the prices of those goods (where mental expenditure may be measurable as the opportunity costs of not engaging in mental labor for wages, or of not shopping for a fewer number of more comparable goods with lower mental accounting costs). In this case it makes sense to put the goods together into bundles with a higher price and an intuitive synergy, until the mental accounting costs of shoppers are sufficiently low.

### Fungibility

Another fix is possible for fungible commodities: charge a fixed price per unit, which the shopper can evaluate from just the accumulated number of units and price information. As a concrete example, in a recent U.S. ad campaign AT&T is betting that its $.15 flat rate is more attractive than Sprint's $.10—who know variable rate—that it is worth the vendor foregoing deep discounts, in order to have a predictable rate, turning phone time into a fungible commodity, and thus saving on mental accounting costs.

Alas, most Internet commerce is not fungible: content, services, mail-order products, and so on. Some Internet Service Provider (ISP) services can be sold as fungible (e.g. disk space, connect time) only at the expense of foregoing congestion pricing and other pricing methods that, if it were not for mental accounting costs, might be quite efficient. Furthermore, even for fungible commodities each user has a unique curve of dimininishing returns.

Software would have to let the shopper determine and input his volume preference curve (in some intuitively familiar way, without presupposing the shopper is familiar with economic theory) before it could adequately act in his interests; not to mention the complications of temporal preferences, nonlinear interactions between commodities fungible when in isolation, and so on.

This user interface solution for the case of fungible commodities suggests a better strategy for tackling the more general problem of mental accounting in online commerce: develop better ways for the shopper to communicate his personal preferences to software. Marketers have long devised schemes to get this kind of information: detailed surveys, traicking of user behavior and responses, etc. Arguably Web services like www.firefly.com are the most advanced in this regard. Firefly creates a kind of "subjective space" of musical preferences in which the shopper can navigate and find new music that they are more likely to prefer.

Assuming that software can respresent certain preferences, it is a more straightforward problem for softare to map these representations to specific prices (or bids), engage in shopping (or haggling), and securely complete online transactions. These easier problem have been the focus of micropayments research, but the more fundamental problem of obtaining and representing preferences in the first place has gone largely unrecognized, perhaps due to an objectivist bias that posits mathematical laws rather than subjective preferences as the basis of a working economy, and due to the basic difficulties in discovering and specifying normally tacit preferences.

Given the solution of other transaction cost problems, mental accounting costs then become the subject to the limit on the process of communication preferences—whether via the mental accounting choice of one good over another, or through creating a unique and sufficiently accurate software simulacrum of a shopper's preferences which then completes the budgeting, bargining, and purchasing process. To what extent and with what efficiency can (a) a shopper communicate subjective preferences to software, and (b) can software represent and act in the interests of these objectified preferences? The presence of search engines, catalog order forms, marketing surveys, and more sophisticated interactions like firefly demonstrate that such communication and representation is both feasible and important, but seems to be costly and perhaps fundamentally limited in some way(s).

## Cash Flow Uncertainty and Insurance

The first source of customer mental transactions costs we will examine is his uncertainty over his future cash flows. We can characterize two kinds of uncertainty customer have about their future cash flows:

1. Uncertainty of income
2. Uncertainty of expenditure, i.e. uncertainty about future preferences and the tradeoffs between preferences in different time periods. This kind of uncertainty also plays a role in a subsequent section, "Incomplete and Costly Decision Making."

A flat fee constitutes an embedded, implicit insurance contract. <a href="#fnAL95" id="refAL95">[AL95]</a> disccuses some aspects of risk preferences implicitly embedded in economic transactions. Such implicit insurance is also a hypothesis of <a href="#fnCL79" id="refCL79-1">[CL79]</a> to explain customer preference for flat fees in the telephone industry.

Customer costs are especially high when customer has a fixed income and high cost of credit and/or lack of savings against variable, too costly to calculate or predict preferences for the amount or mix of trade items to be purchased.

The risk posed to the customer is not best understood as running out of money _per se_, but rather as the starvation of other preferences due to uncertainties in estimating future resources available to be expended on preferences to be satisfied in the future.

Unexpected lack of cash leads to unsatisfied preferences. Uncertainty about cash availability leads to cognitive cost and incompleteness in deciding how to normalize preferences between two time periods.

A simplifying appraoch to formalizing uncertainty of income would be to assume that attributes can be observed perfeclt and costlessly, and all attributes accounted for perfectly and costlessly, while the customer retains uncertainty about his future incomes.

This customer risk must be traded off against the risk to the vendor of resource overuse—analogous, in this implicit insurance contract, to moral hazard, but not hidden from vendor. In most retail situations, the vendor's ability to control these risks (by hedging, spreading costs, etc.) are usually much lower than the consumer's. A flat fee can also protect the customer against later opportunistic behavior by the supplier where customer switching costs are high.

### Delegation

When the customer delegates purchase of a product or service over a given period to an agent, a flat fee limits the exposure of the principle/customer (but not the supplier) to abuse of the resource by the agent. Against this can be desirable where the supplier is better able than the customer to plan these uses, and spread out the costs of such resource usage across many customers.

A per unit fee with a fixed upper limit (e.g. phone card) can make it easier to use variable rate systems while maintaining cash flow. This converts the implicit contract from risk spreading insurance with average price to just a big "deductible." This remedy maintains the risk of starving preferences for this good, but eliminates (at some cost) the risks of general preference starvation due to running out of cash.

## Attribute Observation Costs

The second source of customer mental transaction costs we will look at is the cost and error involved in observing the attributes of products and services. We introduced this problem above.

That customer verification of quality imposes a significant economic cost has been discussed since at least Charles Babbage <a href="#fnB1835" id="refB1835">[B1835]</a>. Recent attempts to clarify the nature of these costs include (<a href="#fnA70" id="refA70">[A70]</a>, <a href="#fnBz82" id="refBz82-3">[Bz82]</a>).

### Attribute Observation

Attributes observed are seldom the attributes truly valued. In a previous section we mentioned that Barzel <a href="#fnBz82" id="refBz82-4">[Bz82]</a> in particular has studied this issue. In this paper, we don't presume the observer summarizes observation as numerical values. So in contrast to Barzel's term _measurement_, we will stick with the more general _observation_. In a _proxy observation_, product or service X is observed by attributes $X_o$, whereas it is valued for attributes $X_v$ which are often tacit.

### Blind Selling With a Trusted Brand

<a href="#fnBz82" id="refBz82-5">[Bz82]</a> and <a href="#fnKK83" id="refKK83">[KK83]</a> developed the following scenario, which suggests the scenario below for Web micropayments.

Recall the apples. Assume that the proxy attribute of color is positively correlated with taste. In an open bin, customers would use this attribute to select the best colored apples, leaving the pale and spotted ones for the deep discount bin or waste.

A buyer who is convinced that he received a random selection from an optimally observe commodity will not use additional resources for observation. An example of blind selling is the sale of apples in an opaque bag. As long as the brand is trustworthy, the customers save on the costs of competing with each other for picking out the best colored apples.

Bling selling requires brand names trusted with either (1) uniformity of good or (2) representative randomness, suppressing particular information to force random choice on all buyers.

### A Pay-Per-Click Scheme

There has been floating for a while the idea of "pay per click," a micropayment for every click on the Web to pay its owner for content. However, since there has been no chance to browse the content, there is no way to directly ascertain whether it meets tacit preferences: there is no accurate customer observable explicit preference. Browsing a preview or book cover is still inaccurate, and entails increasing mental costs the more accurate it is.

One possible fix is for the shopper's software to compare purchase prices against a "consumer reports" service. We here examine a similar idea, that of branding the links.

As an example of how one might deal with attribute observation costs, we need to develop a proxy attribute of sufficiently high accuracy and low cost. To this end we introduce a scenario of branded links to micropriced content. A famous brand blesses the link with its logo. There might be different logos for different kinds of content, specialty content, etc. (e.g., an academic journal coul peer review and then brand articles in its specialty). Individual athors of sufficient repute might create their own brands. This entails an investment in a single author by a significant number (but proportionately only a very small market share) of customers of a substantial fraction of their "brand name tracking budget."

This highlights a problem with branding content: the brands take into account only widey shared values, not personal values. This doesn't work as well for content for which tastes are idiosyncratic in such a way that they can't be organized into a specialty. The more specialties branded per customer, the higher the cognitive costs of keeping track of all the brand names.

### Switching Costs

Another problem of branded links is that we haven't eliminated mental transaction costs. We've only changed their nature, hopefuly in the process reducing them. Brand name evaluation itself imposes cognitive costs. In particular, brands require customers to invest in observing and recalling the quality history of the brand. This investment creates "brand loyalty" or switching costs, studied by <a href="#fnK95" id="refK95">[K95]</a>.

Combined with uncertainty by the consumer about the future price, such investments incentivize the creation of long-term contracts in place of spot prices <a href="#fnW85" id="refW85-2">[W85]</a>, or flat fees instead of micropayments.

### Hidden Attributes in Transaction Processing Software

One important task of business transactions, that has been largely overlooked by traditional electronic commerce, is critical to "the meeting of the minds" that is at the heart of a contract: communicating the semantics of the protocols to the parties involved. There is ample opportunity in electronic commerce for "smart fine print": actions taken by the software hidden fro a party to the transaction. For example, grocery store POS machines don't tell customers whether or not their names are being linked to their purchases in a database. The clerks don't even know, and they've processed thousands of such transactions under their noses. Thus, via hidden action of the software, the customer is giving away information they might consider valuable or confidential, but the contract has been drafter, and transaction has been designed, in such a way as to hide those important parts of that transaction from the customer.

Without user interfaces electronic commerce is largely invisible, like the electronics in newer car engines. This is both a blessing—counterparties don't have to feel like they're dealing with user-hostile computers—and a curse—the "smart fine print" problem of hidden actions.

Here's a little example of smart fine print:

<pre><code>
if (x == true) {
    display("x is false");
}
</code></pre>

To properly communicate transaction semantics, we need good visual metaphors for the elements of the contract. These would hide the details of the protocol without surrendering control over the knowledge and execution of contract terms. This is discussed further in a subsequent section.

One way to guard against hidden actions is to specify more contractual detail to cover more exceptional situations and prevent more strategic opportunities. However, this is also both incomplete and costly <a href="#fnW85" id="refW85-3">[W85]</a>.

## Incomplete and Costly Decision Making

Assuming, for the moment, perfect information on the product at hand, and no uncertainty as to future cash flows, a third and more basic source of customer cognitive cost remains, namely the cost of making decisions with a large, but nevertheless very incomplete, set of alternatives.

### Decision Making

The incompleteness of decision making follows from the incompleteness of the observation of all the attributes in the world which might be preferred. It has also been argued on other grounds that decision theory, the basis for most economic theories of preferences, is incompletely, e.g. Pettit <a href="#fnP91" id="refP91">[P91]</a>.

When balancing a portfolio of preferences, the number of alternatives which might be considered, while miniscule compared to the number of alternatives actually in the world, is so vast as to be quite probably computationally infeasible to search through when making a decision about a particular trade item. The completeness with which preference tradeoffs can be made locally and efficiently is not clear <a href="#fnK88" id="refK88">[K88]</a>.

### Tacit Preferences

A model of making decisions, which encompasses everything from a highly heuristic computation to a complete table of alternatives, can be provided by positing a function from attributes and preferences to decisions:

- $T_c$: customer tacit preference rule
- $a_{c,s}$: customer and supplier observed attribute
- $p_{c,s}$: customer and supplier observed preference for attribute
- preference formation function (tacit preference rule): $T_c : a_c \rightarrow p_{c,s}$

A similar tacit rule can be specified for attributes as observed only by the customer.

We call this "tacit" because such rules need not be articulated to function properly, and probably are not in practice. In particular, "preference elicitation" in the economic literature elicits only the output, supplier observed explicit preferences, not the rule itself, nor alternative preferences foregone in the observed decision. Polanyi <a href="#fnP58" id="refP58-2">[P58]</a> among others has argued that most human decision making is tacit.

In practice there will be another function to precalculate information to feed into the tacit preference rule, to conserve on realtime cognitive costs which are more expensive than at-leisure cognitive costs.

Another source of incompleteness is the inability to predict preferences prior to being shown attributes which might be preferred—because the decision making process is based on an abstract tacit rule rather than knowledge of all the particular attributes which might be encountered. Due to incomplete induction from preferences for specific attributes to general rules, the customer often can't express preferences without the stimulus of observing attributes, even in cases where the attribute has been observed before in other contexts.

### Temporal Tacit Preferences

Preference formation, in this theory, occurs at least partially at the time novel attributes are observed. These attributes are fed into the tacit preference rule, resulting in decisions, or explicit preferences. How, then, can tradeoffs be made against future preferences when the nature of those preferences are often not yet well known? The tacit rule fires at time $t_1$, then against at $t_2$: how can these two evaluations of the rule be made commensurable?

Tacit preferences are a rich area for future work in characterizing mental transaction costs.

## Preferences and Visual Metaphors

To assess the desirability of a transaction, and to avoid being mischarged, the parties to a transaction have to count up, i.e. account for, the money paid for particular products and services—whether making sure that cash payments are made as promised (e.g. looking at the display as products are scanned at the store, or the receipt afterwards), or making sure the phone bill is proper. In this section "accounting" is used in this broad sense.

A customer may be paying in cash, but he'd often still like to keep track of how and why his cash is going in and out. A transaction log is the most used tool to assist in this task. There may be other metaphors more appropriate for some circumstances (e.g., absolute level gauges, rate gauges with high and low watermarks, etc.); this is a potentially fertile new field to explore. There may be agents that can do some of the accounts (e.g. comparing payments made to terms promised, payment limits, etc.), but for the vast majority of products and services software cannot judge the quality or personal desire for the product or service, and thus the net desirability of the transaction. The user must undertake this comparison with whatever information the computer can provide via the display. The user interface and the cognition of the user thus remain the bottleneck to transaction granularity.

A big task is to use the power of graphical user interface to come up with new metaphors to make this easier. It is the intuitive yet accurate metaphor that will lower accounting costs. Cryptographic protocols potentially lower only security-related transaction costs such as forgery and extortion. For the normal accounting transaction costs, which are currently too high for micropayments, we need better interactive visual metaphors.

For transactions free of records, we need transactions that can be fairly transacted once, immeditaly accounted for by the parties via a nice visual metaphor, then forgotten. The potential for unresolvable disputes in record-free systems is vast for transactions where this is not possible (probably most of desired commerce, where quality of a product or service cannot be well determined until after the purchase transaction is complete, or where credit is involved).

Price is one kind of contractual term; we also need nice metaphors to keep track of other kinds of contractual terms. Lack of observability of the protocol on the part of the user leads to the ability of the counterparty to engage in hidden actions. See <a href="#fnS97" id="refS97">[S97]</a> for further discussion of this and other computerized contracting issues.

One of the barries to creating good contracts is determining what the parties want in the first place. People tend to think in terms of standard or sterotyped conditions: payment in dollars, investing in stocks, etc. when there exist a far wider variety of alternative contractial structures that, combined properly, could better meet the parties' needs. It would be useful to have tools which allow parties to explore their desires interactively with the computer. In finance this might include interactive personal yield curves, determining the partial order of desires (as in decision theory) for particular alternate securities, derivatives, and synthetics; and so on. Software would then analyze this input, make recommendations, and even undertake automated contracting. Metaphors should be developed that make it easy for lay users to express such desires without extensive knowledge of finance or decision theory. Such metaphors would provide a friendly front end to automated exchanges, auctions, and other online contracting mechanisms.

One particular metaphor is the personal budget, such as the kind which can be kept in Quicken™ software. In writing down a budge, the customer creates a crude simulacra of his expected tacit preferences, expressed in a very abstract form.

## Conclusion

Some work has been done to determine customer preferences for usage versus flat rates. A recent attempt for Internet commerce is INDEX (the Internet Demand Experiment) <a href="#fnI99" id="refI99">[I99]</a>. The Internet in general (and AOL in particular is a good example) has seen movement away from hourly or usage fees to flat fees.

There was also work done in phone company studies during U.S. deregulation. <a href="#fnFOS97" id="refFOS97-2">[FOS97]</a> references and discusses some of the empirical evidence, originally presented in <a href="#fnCL79" id="refCL79-2">[CL79]</a> and related work, showing customer preference for flat fees in the telephone industry.

A lesson for micropayment efforts is that mental costs usually exceed, and often dwarf, the computation costs. Reductions in the per transaction computational costs of transactions may often be economically insignificant. Other transaction costs addressable by hardware or software, such as security concerns, as well as costs of better communicating product quality versus price tradeoffs in the user interface, are usually more important objectives for technological cost reduction than conserving on computational or network resources.

We have seen how customer mental transaction costs can derive from at least three sources: uncertain cashflows, incomplete and costly observation of product attributes, and incomplete and costly decision making. These costs will increasingly dominate the technological costs of payment systems, setting a limit on the granularity of bundling and pricing. Prices don't come for free.

## References

<ol class="references">
  <li id="fnA70">[A70] Akerlof, G. A., "The Market for 'Lemons': Quality Uncertainty and the Market Mechanism," Quarterly Journal of Economics, 84(3), 488-500.&nbsp;<a href="#refA70">↩</a></li>

  <li id="fnAL95">[AL95] Allen, D. W. and Lueck, D. (1995), "Risk Preferences and the Economics of Contracts," 5 American Economic Review, Papers and Proceedings, 447-451.&nbsp;<a href="#refAL95">↩</a></li>

  <li id="fnB1835">[B1835] Babbage, C. <em>On the economy of machinery and manufactures</em>, 4th ed. New York: Kelley, 1963. (Facsimile reprint of the edition published in London by Knight, 1835).&nbsp;<a href="#refB1835">↩</a></li>

  <li id="fnBe95">[Be95] Bellare, M. et. al., "A Family of Secure Electronic Payment Protocols," <em>Proceedings of the Usenix Electronic Commerce Workshop</em>, 1995&nbsp;<a href="#refBe95">↩</a></li>

  <li id="fnBz82">[Bz82] Barzel, Y., "Measurement Costs and the Organization of Markets," <em>Journal of Law and Economics</em>, 25, 27-48.&nbsp;<a href="#refBz82-1">↩</a>&nbsp;<a href="#refBz82-2">↩</a>&nbsp;<a href="#refBz82-3">↩</a>&nbsp;<a href="#refBz82-5">↩</a>&nbsp;<a href="#refBz82-5">↩</a></li>

  <li id="fnBB97">[BB97] Bakos, Y., and Brynjolfsson, E. "Aggregation and disaggregation of information goods: Implications for bundling, site licensing and micropayment systems." In <em>Internet Publishing and Beyond: The Economics of Digital Information and Intellectual Property</em>. D. Hurley, B. Kahin, and H. Varian, eds., MIT Press. Also at <a href="http://www.gsm.uci.edu/bakos/aig/aig.html">http://www.gsm.uci.edu/bakos/aig/aig.html</a>&nbsp;<a href="#refBB97">↩</a></li>

  <li id="fnCL79">[CL79] Cosgrove, J. G., and Linhart, P. B., "Customer choices under local measured telephone service," <em>Public Utilities Fortnightly</em>, Aug. 30, 27-31.&nbsp;<a href="#refCL79-1">↩</a>&nbsp;<a href="#refCL79-2">↩</a></li>

  <li id="fnFOS97">[FOS97] Fishburn, P., Odlyzko, A. M., and Siders, R. C., "Fixed fee versus unit pricing for information goods: competition, equilibria, and price wars," <em>First Monday</em>, Vol. 2 No. 7 - July 7th. 1997, <a href="https://journals.uic.edu/ojs/index.php/fm/article/download/535/456">https://journals.uic.edu/ojs/index.php/fm/article/download/535/456</a>&nbsp;<a href="#refFOS97-1">↩</a>&nbsp;<a href="#refFOS97-2">↩</a></li>

  <li id="fnGMAGS95">[GMAGS95] Glassman, S., Manasse, M., Abadi, M., Gauthier, P. S., "The MilliCent Protocol for Inexpensive Electronic Commerce," Proceedings of the 4th International World Wide Web Conference - December, 1995. For proposed uses, see <a href="https://web.archive.org/web/19991222022345/http://www.millicent.digital.com/works/white_papers/index.html">http://www.millicent.digital.com/works/white_papers/index.html</a>&nbsp;<a href="#refGMAGS95">↩</a></li>

  <li id="fnH45">[H45] Hayek, F. "The Use of Knowledge in Society," <em>American Economic Review</em>, 35 (September 1945): 519-530&nbsp;<a href="#refH45">↩</a></li>

  <li id="fnH89">[H89] Hart, O., "Incomplete Contracts," In: John Eatwell, Murray Milgate, and Peter Newman (eds.), <em>The New Palgrave: Allocation, Information, and Markets</em>. New York: Norton.&nbsp;<a href="#refH89">↩</a></li>

  <li id="fnI99">[I99] <a href="https://web.archive.org/web/19990429135034/http://www.index.berkeley.edu/public/index.phtml">http://www.index.berkeley.edu</a>&nbsp;<a href="#refI99">↩</a></li>

  <li id="fnK88">[K88] Kreps, D. M., <em>Notes on the Theory of Choice</em>, Westview, 1988&nbsp;<a href="#refK88">↩</a></li>

  <li id="fnK95">[K95] Klmeperer, P., "Competition When Consumers Have Switching Costs: An Overview with Applications to Industrial Organization, Macroeconomics, and International Trade," <em>Review of Economic Studies</em> 62(4) pages 515-39.&nbsp;<a href="#refK95">↩</a></li>

  <li id="fnKK83">[KK83] Kenney, R. W. and Klein, B., "The Economics of Block Booking," <em>Journal of Law and Economics</em>, 26, 497-541.&nbsp;<a href="#refKK83">↩</a></li>

  <li id="fnM35">[M35] Mises, L. v., <em>Human Action</em>, 3d edition (Regnery, 1996)&nbsp;<a href="#refM35">↩</a></li>

  <li id="fnMD88">[MD88] Miller, M. and Drexler, K. E., "Markets and Computation: Agorics Open Systems," in <em>The Ecology of Computation</em>, Bernardo Huberman (ed.), Elsevier Science Publishers/North-Holland, 1988.&nbsp;<a href="#refMD88-1">↩</a>&nbsp;<a href="#refMD88-2">↩</a></li>

  <li id="fnN98">[N98] Nielsen, J., "The Case for Micropayments," Jakob Nielsen's Alertbox for January 25, 1998, <a href="https://www.nngroup.com/articles/the-case-for-micropayments/">https://www.nngroup.com/articles/the-case-for-micropayments/</a>. See also sidebar "User Interfaces for Internet Payments" and reader comments.</li>

  <li id="fnP58">[P58] Polanyi, M. <em>Personal Knowledge</em>, University of Chicago Press, 1958&nbsp;<a href="#refP58-1">↩</a>&nbsp;<a href="#refP58-2">↩</a></li>

  <li id="fnP91">[P91] Pettit, P., "Decision Theory and Folk Psychology," in Bacharach, Michael and Hurley, Susan ed., <em>Foundations of Decision Theory</em>, Blackwell, 1991&nbsp;<a href="#refP91">↩</a></li>

  <li id="fnRS96">[RS96] Rivest, R. L. and Shamir, A. "PayWord and MicroMint—Two Simple Micropayment Schemes," <em>CryptoBytes</em>, volume 2, number 1 (RSA Laboratories, Spring 1996), 7-11&nbsp;<a href="#refRS96">↩</a></li>

  <li id="fnS97">[S97] Szabo, N. (1997) <a href="/formalizing-securing-relationships/">"Formalizing and Securing Relationships on Public Networks,"</a> First Monday, Vol. 2 No. 9 - September 1st. 1997, <a href="https://journals.uic.edu/ojs/index.php/fm/article/download/548/469">https://journals.uic.edu/ojs/index.php/fm/article/download/548/469</a>&nbsp;<a href="#refS97">↩</a></li>

  <li id="fnW85">[W85] Williamson, O. E. <em>The Economic Institutions of Capitalism</em>, Free Press/McMillan, 1985&nbsp;<a href="#refW85-1">↩</a>&nbsp;<a href="#refW85-2">↩</a>&nbsp;<a href="#refW85-3">↩</a></li>
</ol>

## Acknowledgements

My thanks to Robert Horn, Hal Varian, Doug Barnes, Ian Grigg, and others for their helpful comments.
