---
title: Confidential Auditing
authors:
  - nick-szabo
date: 1998
categories:
  - economics
doctype: essay
external: https://web.archive.org/web/20160319150321/http://szabo.best.vwh.net/confidential.html
---

The auditing function is a vast and indispensable part of the modern economy. Auditing controls allow, among other things, employers to delegate resources and authority to employees, franchisors to delegate to franchisees, stockholders to delegate to management, advertisers to count eybeballs, marketers to gather more reliable data on customers, and make possible a wide variety of other such relationships. Auditing controls might fairly be called the security protocols of capitalism.

A recent general survey showed that **83%** of Americans are &quot;very concerned&quot; about their privacy on the Internet. One can expect even stronger figures from European customers, who have more first-hand experience with private data, much of it originally compiled for innocuous reasons, being used for political repression. Businesses recognize the shortcomings of NDAs and are looking for more reliable ways to protect confidential data. The vast majority of e-commerce customers are concerned about privacy.

Auditing is in deep conflict with efforts towards greater privacy. Auditors have an ethic of recording, investigating, and reporting as much as possible, and often see privacy efforts as attempts to prevent auditing and potentially cover up fraud. Indeed, the recent multi-$billion failures of Baring&#39;s Bank and the Long Term Capital hedge fund, and more generally the recent problems with &quot;crony capitalism&quot; which have shorn stockholders and creditors of over $1 trillion, have been ascribed to such secrecy<sup><a href="#fn3" id="ref3">[3]</a></sup>. At the top of the list of current IMF reforms is &quot;openness&quot;, a buzzword for the introduction of greater auditing controls and reporting requirements.

Since auditing controls are used to secure trillions of dollars of transactions every year, they are not going away, and indeed will likely grow more effective and intrusive. On the other hand, we now have at our disposal the many breakthroughs achieved over the last two decades in modern cryptography. Can we use these to strike a better balance between auditing and privacy? I have come up with an architecture which uses such protocols to greatly improve this tradeoff: confidential auditing.

We can achieve auditing logs unforgeable after commitment via secure timestamps<sup><a href="#fn1" id="ref1">[1]</a></sup>. We can then achieve to a great extent unforgeability prior to commitment, with segregation of duties via multiparty integrity constraints<sup><a href="#fn2" id="ref2">[2]</a></sup>. We then audit these commitments via multiparty private computations<sup><a href="#fn4" id="ref4">[4]</a></sup>. This combination allows a wide variety of transactions, conducted with normal efficiency, to be observed and verified by selected arbitrators or auditors, via more expensive private computations applied to randomly sampled commitments. This maintains a high degree of confidentiality for the inputs.

The participants in this mutually confidential auditing protocol can verify that the books match the details of transactions stored in a previously committed transaction log, and that the numbers add up correctly. The participants can compute summary statistics on their confidentially shared transaction logs, including cross-checking of the logs against counterparties to a transaction, without revealing those logs. They only learn what can be inferred from the statistics, can&#39;t see the details of the transactions.

Assuming many practical details I have glossed over in this sketch (such as the efficiency of auditing computations, the availability of digital transaction records in standard format, etc.), confidential auditing can bring a substantial improvement over current practices. Currently the details of all an organization&#39;s transactions, including for example medical records in an HMO and transactions in top-secret government programs, are either exposed directly to auditors, or are immune from auditing, allowing fraud.

With mutually confidential auditing we will be able to gain high confidence in the factuality of counterparties&#39; claims and reports without revealing identifying and other detailed information from the transactions underlying those reports. This will provide the basis for solid reputation systems, and other trusted third party systems, that maintain integrity across time, communications, summarization, and preserve confidentiality for transaction participants. With confidential auditing we will often be able to have both openness and privacy.

## Footnotes

<ol>
  <li id="fn1">
    <p>BLLV98  A. Buldas, P. Laud, H. Lipmaa, J. Villemson, "Time-Stamping with Binary Linking Schemes", Crypto 98&nbsp;<a href="#ref1">↩</a></p>
  </li>

  <li id="fn2">
    <p>Szabo, in progress&nbsp;<a href="#ref2">↩</a></p>
  </li>

  <li id="fn3">
    <p>See recent back issues of <em>The Wall Street Journal</em> and <em>The Economist</em>&nbsp;<a href="#ref3">↩</a></p>
  </li>

  <li id="fn4">
    <p><a href="/the-god-protocols/">Overview</a>; Quorum systems model, <a href="/library/quorum-systems/">“Quorum Systems”</a>&nbsp;<a href="#ref4">↩</a></p>
  </li>
</ol>

<h2>References</h2>

<ul class="references">
  <li id="fnB91">
    <p>[B91] D. Beaver, "Efficient Multiparty Protocols Using Circuit Randomization", ACM STOC 91</p>
  </li>

  <li id="fnRB89">
    <p>[RB89] T. Rabin & M. Ben-Or, "Verifiable Secret Sharing and Multiparty Protocols with Honest Majority", ACM STOC 89</p>
  </li>

  <li id="fnGRR98">
    <p>[GRR98] R. Gennaro, T. Rabin, & M. Rabin: "Simplified VSS and Fast-Track Multiparty Computations", PODC 98</p>
  </li>
</ul>
