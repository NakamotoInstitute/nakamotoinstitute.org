---
title: Intrapolynomial Cryptography
authors:
  - nick-szabo
date: 1999
categories:
  - cryptography
doctype: essay
external: http://szabo.best.vwh.net/intrapoly.html
---

Researchers have proposed a variety of “client puzzle” or “busy-work” proposals like hashcash, MicroMint, bit gold, and compute-cost postage to create independent currencies or make spamming costly. The mathematical implication of these proposals is that there is such a thing as intrapolynomial cryptography. Four motivations for intrapolynomial cryptography theory are (a) novel constructions such the aforementioned applications, (b) more accurate estimation of the computational cost of cracking a cipher, (c) it might be easier to prove lower bounds, rather than just conjecture them as is the case with superpolynomial (standard) cryptography, and (d) if there do not exist one-way functions, standard cryptography is intrapolynomial rather than superpolynomial.

I propose the following formalization:

<pre>
f: {0,1}* --> {0,1}* is called a strong k-benchmark function
for machine model M and k>=1 if the following hold:

1. f is computable in O(p(n)) time on M, where p is a polynomial.
2. f does not shrink the input more than q(n,k), where q(n,k)
is a polynomial of degree k.
3. For every randomized algorithm A running on M in time
less than q(n,k)p(n), there exists an N such that for n > N
        Pr[A(f(x)) = f^-1(f(x))] < 1/q(n,k)p(n)
</pre>

In other words, there is no algorithm running faster than q(n,k)p(n) which can invert f for more than a negligibly small number of values.

One can similarly define average-case, best-case, and worst-case k-degree benchmark functions, analogously to one-way functions. Open question (analogous to the open question in superpolynomial cryptography of whether one-way functions exist): can one prove (3) as lower and upper bounds for some function and k>=1 on some realizable machine model such as RAM-log?

Strong and average case are most apropos to cryptography related applications. Unfortunately for these purposes we'd also need:

<ol type="a">
  <li>a list of machine models which is comprehensive of all physically realizable machines, in the sense that any such machine can be simulated with a very small overhead, such as constant or O(log(n)), by some model on the list, and</li>
  <li>to prove lower bounds on a benchmark function for all models on the list</li>
</ol>

Since this is at least very tedious, one hopes we can in practice get away with a short list which covers all plausibly implemented machine architectures. This might work where for example the total exposure from cracking a protocol is less than the R&D costs of designing and building a novel machine architecture to defeat it. Cryptanalyis would include discovering the machine architectures optimal for breaking an intrapolynomial cipher.

There are at least two practical implications of the above analysis. One is that there is very little room for error in the analysis and implementation of compute-cost postage, hashcash, bit gold, MicroMint, and other such intrapolynomial cryptography schemes. Another is that, unless the opponent has a very low budget and is thus limited to standard personal computers, it does not make sense to analyze the security or cost of these schemes without reference to machine architecture. For example, spammers may be able to defeat compute-cost postage by using custom chips optimized for computing the particular puzzle function.
