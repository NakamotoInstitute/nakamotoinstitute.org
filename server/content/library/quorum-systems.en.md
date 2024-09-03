---
title: Quorum Systems
authors:
  - nick-szabo
date: 1998
categories:
  - cryptography
doctype: essay
external: https://web.archive.org/web/20160629221812/http://szabo.best.vwh.net/quorum.html
has_math: true
---

## Introduction

$N$ parties, comprising the set $U$ ("universe"), want to engage in a protocol. These parties can form coalitions to gang up on each other. The set of possible coalitions is just the set of all subsets of $U$, $\mathcal{C} = 2^U$.

The protocol designer should first specify what coalitions are to be allowed and forbidden. If the parties have rational self-interest, only coalitions whose members have an incentive to not collude, to either compute an incorrect result, or to violate the privacy of any player, should be allowed the potential to disrupt the protocol. Invoking "incentive" implies an economic or game-theoretic analysis of coalitions, which will be considered in a future article.

For now, we just observe that the protocol designer needs to draw from $C$ a set of allowed ("good") coalitions $\mathcal{G}$. Any set of parties in $\mathcal{G}$ is a coalition sufficient to successfully complete the protocol. Also, draw from $C$ a set disjoint from $\mathcal{G}$ of disallowed ("bad") coalitions $\mathcal{B}$ which cannot be allowed the opportunity to disrupt the protocol. If $\mathcal{G} \cup \mathcal{B} = \mathcal{C}$, then we say that the partition is unambiguous. Also, the sets in $\mathcal{G}$ are the complements of the sets in $\mathcal{B}$, and vice versa.

To produce a secure protocol, these coalitions need to meet certain criteria. Particularly interesting is the _quorum system_, a set of good coalitions, every member of which intersects in at least one party. Each quorum can act on behalf of the system to complete the protocol. Intersection facilitates consistency across quorums. For example, if an operation occurs in two quorums, then at least one party observes both. Indeed, a fault-tolerant or secure quorum system intersects in a set containing sufficiently many parties to guarantee correctness. See, for example, the masking and dissemination quorum systems used by Malkhi & Reiter <a id="refMR97" href="#fnMR97">[MR97]</a> to design a replicated database secure against Byzantine faults by bad coalitions.

<a id="refBW98-1" href="#fnBW98">[BW98]</a>, following the trail blazed by among others <a id="refHM97" href="#fnHM97">[HM97]</a> and <a id="refNW96" href="#fnNW96">[NW96]</a>, have shown that if any single party can be trusted with correctness, then a quorum system is necessary and sufficient for the privacy of inputs to a multiparty computation<a id="refS97" href="#fnS97">[S97]</a> against resource unbounded adversaries. Classical analysis of multiparty computation concluded that a threshold of more than half of the parties is necessary and sufficient for private computation. This is just a special case of <a id="refBW98-2" href="#fnBW98">[BW98]</a> result. Any threshold system whose threshold exceeds $N/2$ is also a quorum system -- there are only $N$ parties, so two coalitions of size $>N/2$ must contain at least one party in common, thus forming a quorum system.

The classical analysis also concluded that a majority threshold is necessary and sufficient for _correct_ multiparty computation, i.e. secure against active Byzantine faults in minorities with polynomial amounts of resources. A two-thirds majority is necessary against resource unbounded adversaries. I am aware of no correctness result as yet for quorum systems in multiparty computation.

## Constraint Families

### Masking

First let's consider quorum systems which intersect, not just in a single party, making them intolerant to any faults in these parties, but rather in enough parties to complete the protocol in a way tolerant of up to $f$ faults, $f>0$. One way to do this is called _masking_ which constrains quorum systems to satisfy the following:

M1: None of the sets of correct servers which contain the latest value is a bad coalition. To achieve this, any quorum intersection minus any bad coalition should not be a subset of any other bad coalition. Formally: **for all $Q_1, Q_2 \in \mathcal{G}$ and for all $B_1, B_2 \in \mathcal{B}$, $(Q_1 \cap Q_2) \setminus B_1$ is not a subset of $B_2$.**

M2: No bad coalition can disable all quorums. Formally: **for all $B \in \mathcal{B}$, there exists some $Q \in \mathcal{G}$ such that $B$ and $Q$ are disjoint.**

These constraints are sufficient to ensure that a replicated database is updated consistently and correctly, iff $|U| > 4f$.

### Dissemination

To get a _dissemination_ quorum system we relax the first constrain. Now we just want every intersection to not be contained in any bad coalition:

D1: Any quorum intersection is not a subset of any bad coalition. Formally: **for all $Q_1, Q_2 \in \mathcal{G}$ and for all $B \in \mathcal{B}$, $(Q_1 \cap Q_2)$ is not a subset of $B$.**

D2: No bad coalition can disable all quorums. Formally: **for all $B \in \mathcal{B}$, there exists some $Q \in \mathcal{G}$ such that $B$ and $Q$ are disjoint.**

These constrains are sufficient to ensure that a replicated database is updated consistently, iff $|U| > 3f$. Correctness of the data must be ensured by some other means, e.g. external signing and verification of digital signatures.

## Particular Classes

### Threshold

If **$\mathcal{B} = \{B \subseteq U : |B| = f\}, n > 4f$**, then **$\mathcal{Q} = \{Q \subseteq U : |Q| = \lceil \frac{n + 2f + 1}{2} \rceil\}$** is the threshold masking quorum system for $\mathcal{B}$. If $n > 3f$, then the threshold dissemination quorum system for $\mathcal{B}$ is given by **$|Q| = \lceil \frac{n + f + 1}{2} \rceil$**.

### Grid

Suppose $|U| = k^2$. The parties can be arranged into a $k \times k$ grid. Then a grid masking quorum system for **$\mathcal{B} = \{B \subseteq U : |B| = f\}, 3f + 1 < k$** is given by **$\mathcal{Q} = \{C_j \cup \bigcup_{i \in I} R_i : I, \{j\} \subseteq \{1, \ldots, k\}, |I| = 2f + 1\}$**. A grid dissemination quorum system is the same as in the masking case, except $|I| = f + 1$.

### Partition

Here we partition $U$ into $m$ clusters and express the assumption that at any time, at most one cluster is faulty. Thus $\mathcal{B} = \{B_1, \ldots, B_m\}$ is a partition of $U$. Then the partition masking quorum system is given by $m > 4, \mathcal{Q} = \{\bigcup_{i \in I} B_i : I \subseteq \{1, \ldots, m\}, |I| = \lceil \frac{m + 3}{2} \rceil\}$, and the dissemination quorum system is given by $m > 3, \mathcal{Q} = \{\bigcup_{i \in I} B_i : I \subseteq \{1, \ldots, m\}, |I| = \lceil \frac{m + 3}{2} \rceil\}$.

### Crumbling Wall

This falls short of dissemination or masking but is also more efficient. The parties are arranged in rows of various widths. A quorum is the union of one full row and one party from every row below the full row. Many of the quorums in a crumbling wall are small minorities; often of $O(\log|U|)$.

## Conclusion

The study of coalitions, and in particular quorum systems, provides a seemingly comprehensive theory of multiparty protocols which goes well beyond the confining linear world of thresholds.

## References

<ol class="references">
 <li id="fnBW98">[BW98] D. Beaver and A. Wool, "Quorum-based Secure Multi-Party Computation", Eurocrypt '98, also at <a href="https://doi.org/10.1007/BFb0054140">https://doi.org/10.1007/BFb0054140</a> <a href="#refBW98-1">↩</a> <a href="#refBW98-2">↩</a></li>
 <li id="fnHM97">[HM97] M. Hirt and U. Maurer, "Complete characterization of adversaries tolerable in secure multi-party computation", 16th ACM PODC <a href="#refHM97">↩</a></li>
 <li id="fnM91">[M91] R. Myerson, <em>Game Theory: Analysis of Conflict</em></li>
 <li id="fnMR97">[MR97] D. Maklhi & M. Reiter, "Byzantine Quorum Systems", 21st ACM STOC, also at <a href="https://malkhi.com/">https://malkhi.com/</a>; For an important application of Byzantine tolerant replication, see <a href="#fnS98">[S98]</a> <a href="#refMR97">↩</a></li>
 <li id="fnNW96">[NW96] M. Naor and A. Wool, "Access control and signatures via quorum secret sharing", 3rd ACM Conf. on Computer and Communications Security <a href="#refNW96">↩</a></li>
 <li id="fnS96">[S96] On secure credit reporting, virus list distribution, etc.: <a href="/library/negative-reputations/">“Negative Reputations”</a></li>
 <li id="fnS97">[S97] A gentle introduction to multiparty computation and its potential applications: <a href="/library/the-god-protocols/">“The God Protocols”</a> <a href="#refS97">↩</a></li>
 <li id="fnS98">[S98] <a href="/library/secure-property-titles/">“Secure Property Titles with Owner Authority”</a></li>
</ol>
