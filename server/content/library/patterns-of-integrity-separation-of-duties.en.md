---
title: "Patterns of Integrity: Separation of Duties"
authors:
  - nick-szabo
date: 2004
categories:
  - cryptography
  - security
doctype: essay
external: https://web.archive.org/web/20160306112755/http://szabo.best.vwh.net/separationofduties.html
---

## Introduction

This series of papers explores recurring and reusable patterns in human organization and relationships -- protocols that allow us to get along with people we don't know very well. In this article, we explore the pattern **separation of duties**.

## Table of Contents

[Separation of Duties](#separation-of-duties)  
[Example -- Handling Money](#example-handling-money)  
[Examples -- Statutory Laws](#example-statutory-laws)  
[References](#references)

<h2 id="separation-of-duties">Separation of Duties</h2>

<figure>
  <blockquote>
    <p>
      ...to provide for an equitable making of the laws, as well as for an impartial interpretation and a faithful execution of them; that every man may, at all times, find his security in them...in the government of this commonwealth, the legislative department shall never exercise the executive and judicial powers, or either of them: the executive shall never exercise the legislative and judicial powers, or either of them: the judicial shall never exercise the legislative and executive powers, or either of them: to the end it may be a government of laws not of men.
    </p>
    <figcaption><a href="https://malegislature.gov/Laws/Constitution">Massachusetts Constitution, Preamble, Pt. I Art. 30. (1780-today)</a></figcaption>
  </blockquote>
</figure>

### Pattern – Separation of Duties

1. **Start with a function that (a) is too valuable to dispense with, and (b) to be performed, requires power that can be abused.**
2. **Divide the function into separate steps, each necessary for the function to work or for the power that enables that function to be abused.** A function so divided can be called a cycle, and corresponds to a formal mathematical model called a state machine. (You do not need to know this mathematics to follow this discussion; just follow the cycle step by step).
3. **Assign each step to a different person or organization.** The different entities perform their particular roles in the cycle, and monitor and constrain each other, using **interparty integrity constraints**, to perform just their respective roles.

This pattern can also be called the strategy of **required conspiracy**, since abusing the power requires two or more of the separated entities to collude -- no entity can on its own abuse the power required by the function.

The **separation of duties** pattern is most useful for dangerous functions -- functions that entail having powers that can be abused. For such functions, the cost of abuse is substantially greater than the cost of sometimes failing to perform the function. This pattern improves the integrity (correctness) of the function, and the trustworthiness of the institution holding the required power, at the expense of its efficiency, timeliness, and reliability (that is, the odds the function will even get performed). Thus the two biggest examples of the separation of duties pattern -- structuring governments, and handling money within organizations.

<h2 id="example-handling-money">Example – Handling Money</h2>

In a large business, transactions are divided up so that no single person can commit fraud. This is often called "segregation of duties." Carol Brown<sup><a id="ref3" href="#fn3">[3]</a></sup> describes these as "ensur\[ing\] that no single individual is given too much responsibility no employee should be in a position to both perpetrate and conceal irregularities." Functions that should be separated include authorization, recording, and custody of assets.

For example, the functions of warehouse/delivery, sales, and receipt of payments are each performed by different parties, with a policy that each party reports every transaction to a fourth function, accounting. Any singular reported activity (e.g., delivery without receipt of payment) indicates potential fraud (e.g., a delivery was made to a customer and the payment pocketed instead of being put into t he corporate treasury). Separation of duties is the auditor's favorite tool. Where it is absent the auditor cries "foul", just as a good engineer would react to a single point of failure.

<figure>
  <img src="/static/img/library/patterns-of-integrity-separation-of-duties/purchase.gif" alt="">
  <figcaption>A purchase cycle between two large organizations.</figcaption>
</figure>

**Interparty integrity constraints** are verifiable assertions governing the interactions between separated entities. For example, an auditor might check the following assertions between two parties to a transaction: that the transaction took place at the same time, involved payment or receipt of the same amount of money, and involved shipping or receiving of the same good as indicated by product code. Once transactions are reported, they are out of the control of a single entity and require collusion (at least) to forge. From that time forward the transaction is securely committed so that nobody can forge its contents without being detected by an audit. Forging the transaction prior to commitment requires collusion between parties to falsify records consistently on all sides so that they pass the interparty integrity tests. Separating duties between several parties, and embedding them in a web of assertions, minimized the possibility of such collusion.

<!--
<p>Interparty integrity constraints are similar to what are called "invariants" in the database/transaction world. In transaction processing, consistency is required pre and post transaction. Consistency can be proven by protocol design or checked via interparty integrity constraints. Within a transaction we are allowed to be inconsistent.</p>
-->

<h2 id="example-statutory-laws">Example ­– Statutory Laws</h2>

In constitutional law the separation of duties pattern is often called "separation of powers." The dangerous power of being able to make and enforce statutes is divided into several branches, each responsible for only certain steps in the lawmaking and/or law implementation cycles. This pattern recurred, in a variety of ways, in the Athenian, Roman Republic, Venetian (and many other late medieval Italian city-states), Dutch, and many other constitutions of the relatively freer and more prosperous of the many governments to be found in history.<sup><a id="ref1" href="#fn1">[1]</a></sup> In England at least between 1688 (the Dutch invasion/Glorious Revolution) and 1720 (foundation of the Cabinet usurping the executive role of the monarch), and in the United States (in the colonies, and after the 1789 both in the federal and state governments severally) separation of powers took form as follows:

For a statute there are two primary cycles: making the statute and and implementing it.

A. **Adoption cycle** -- A statutory law is made by the following steps:

1. legislature enacts.
2. executive approves or vetoes.
3. the judiciary interprets.

B. **Implementation cycle** -- When a person is accused of a crime under a statute, the case goes through the following steps:

1. apprehended by the executive
2. judged by the judiciary, following the laws drafted under (A) above. the judiciary gets the final say on both what the law is and what the outcome (verdict and sentence) of the case is (necessary by definition, otherwise cases could be decided contrary to law). based on judicial precedent it can also follow common law where statutes do not cover a case.
3. sentence executed by the executive.

The Anglo-American tradition of separating powers in this way evolved roughly as follows. The legislature, from the time of the Magna Carta (1215), had the sole power to tax real property. It derived its authority to tax property from being elected by property owners. (For most of English and some of American history, there was no representation without taxation, as well as the more familiar no taxation without representation. The correspondence between real property ownership, tax paying, and the vote fell apart after mobile goods and income replaced real property as the primary source of tax revenue).

The legislature derived its power to enact legislation from its ability to withhold funds from the executive. In Britain, the power of the legislature kept growing until finally the Cabinet, elected directly from the legislature, usurped the role of the monarch in the 18th century. U.S. colonial practice did not continue this trend but instead reified the distinct and interdependent roles of legislative, executive, and judiciary. This pattern was well in place by the time of U.S. Constitution was drafted in 1789 . [Federalist #48](https://avalon.law.yale.edu/18th_century/fed48.asp) and the above quote from the [Massachusetts constitution](https://malegislature.gov/Laws/Constitution) capture the formal structures and goals of separation of powers. In England the legislature, by usurping the executive role, is probably too powerful; in the U.S. after the New Deal (and the rise of administrative lawmaking in the executive branch) it may too weak relative to the executive branch. To a first approximation, the ideal is to have power equally distributed among the branches so that all three are optimally necessary to the full cycle of adopting and implementing laws.

Interparty integrity constraints in the making and executing of statutory laws include constitutions (meta-statutes that the judiciary uses to constrain statutes and other laws), canons of construction (rules for interpreting statutory language), freedom of information acts, auditing functions, and the publication of judicial opinions and their use as precedent.

<h2 id="references">References</h2>

<ol class="references">
  <li id="fn1">[1] Scott Gordon, <em>Controlling the State: Constitutionalism from Ancient Athens to Today</em> (1999). <a href="#ref1">↩︎</a></li>
  <li id="fn2">[2] <a href="https://avalon.law.yale.edu/18th_century/fed48.asp">Federalist #48</a></li>
  <li id="fn3">[3] <a href="https://web.archive.org/web/19970808205719/http://www.bus.orst.edu/faculty/brownc/lectures/controls/control1.htm">Carol Brown, <em>Internal Control Concepts</em></a> <a href="#ref3">↩︎</a></li>
</ol>
