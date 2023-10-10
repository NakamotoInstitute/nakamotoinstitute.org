---
title: Online Cash Checks
authors:
  - david-chaum
date: 1989
categories:
  - cryptography
doctype: essay
external: http://www.chaum.com/publications/Online_Cash_Checks.html
---

## Introduction

Savings of roughly an order of magnitude in space, storage, and bandwidth over previously published online electronic cash protocols are achieved by the techniques introduced here. In addition, these techniques can increase convenience, make more efficient use of funds, and improve privacy.

"Offline" electronic money<sup><a href="#fnCFN88" id="refCFN88">[CFN88]</a></sup> is suitable for low value transactions where "accountability after the fact" is sufficient to deter abuse; online payment,<sup><a href="#fnC89" id="refC89-1">[C89]</a></sup> however, remains necessary for transactions that require "prior restraint" against persons spending beyond their available funds.

Three online schemes are presented here. Each relies on the same techniques for encoding denominations in signatures and for "devaluing" signatures to the exact amount chosen at the time of payment. They differ in how the unspent value is returned to the payer. In the first, all change is accumulated by the payer in a single "cookie jar," which might be deposited at the bank during the next withdrawal transaction. The second and third schemes allow change to be distributed among unspent notes, which can themselves later be spent. The second scheme reveals to the shop and bank the maximum amount for which a note can be spent; the third does not disclose this information.

## Denominations and devaluing

For simplicity and concreteness, but without loss of generality, a particular denomination scheme will be used here. It assigns the value of 1 cent to public exponent 3 in an RSA system, the value of 2 cents to exponent 5, 4 cents to exponent 7, and so on; each successive power-of-two value is represented by the corresponding odd prime public exponent, all with the same modulus. Much as in [C89], a third root of an image under the one-way function f (together with the pre-image modulo the bank's RSA composite) is worth 1 cent, a 7th root is worth 4 cents, and a 21st root 5 cents. In other words, a distinct public prime exponent is associated with each digit of the binary integer representation of an amount of payment; for a particular amount of payment, the product of all those prime exponents corresponding to 1 's in the binary representation of the amount is the public exponent of the signature.

A signature on an image under f is "devalued" by raising it to the public powers corresponding to the coin values that should be removed. For instance, a note having a 21st root could be devalued from its 5 cent value, to 1 cent, simply by raising it to the 7th power.

In earlier online payment systems,<sup><a href="#fnC89" id="refC89-2">[C89]</a></sup> the number of separate signatures needed for a payment was in general the Hamming weight of the binary representation of the amount. Since online systems would be used for higher-value payments (as mentioned above), and extra resolution may be desired to provide interest for unspent funds,<sup><a href="#fnC89" id="refC89-3">[C89]</a></sup> an average of roughly an order of magnitude is saved here.

## Cookie jar

In this first scheme the payer periodically withdraws a supply of notes from the bank, each with the system-wide maximum value. Consider an example, shown in Figure 1.1, in which two notes are withdrawn. The n and ri are random. The ri "blind" (from the bank) the images under the public, one-way function f. The bank's signature corresponds to taking the h-th root, where h = 3*5*7\*11. As in all the figures, the payer sends messages from the left and the bank sends from the right.

<pre>
                    h             h
          f(n1) * r1 ,  f(n2) * r2
     -----------------------------------------&gt;
PAYER                                        BANK
     &lt;------------------------------------------
               1/h            1/h
          f(n1)    * r1, f(n2)    * r2

           Fig. 1.1. Cookie-jar withdrawal
</pre>

In preparing the first payment, the payer divides r1 out. The signature is then raised to the 55th power to devalue it from 15 cents to 5 cents. Figure 1.2 shows this first payment. Of course the shop is an intermediary between the payer (left) and the bank (right) in every online payment, but this is not indicated explicitly. Also not shown in the figures are messages used to agree on the amounts of payment.

<pre>
                   1/(3*7)           5*11
          n1, f(n1)       , f(j) * s1
     -----------------------------------------&gt;
PAYER                                        BANK
     &lt;------------------------------------------
              1/(5*11)
          f(j)         * s1

           Fig. 1.2. First cookie-jar payment
</pre>

The first two residues sent in paying, n1 and its signed image under f, are easily verified by the bank to be worth 5 cents. The third residue is a blinded "cookie jar," a blinded image under f of a randomly chosen value j. This cookie jar is modulo a second RSA composite that is only used for cookie jars. Once the bank verifies the funds received, and that n1 has not been spent previously, it signs and returns the blinded cookie jar (under the cookie jar modulus) with public exponents corresponding to the change due.

The second payment, shown in figure 1.3, is essentially the same as the first, except that the amount is 3 cents and the cookie jar now has some roots already on it. If more payments were to be made using the same cookie jar, all resulting signatures for change would accumulate.

<pre>
                   1/(3*5)      1/(5*11)    7*11
          n2, f(n2)       , f(j)        * s2
     -----------------------------------------&gt;
PAYER                                        BANK
     &lt;------------------------------------------
              1/(5*11*7*11)
          f(j)              * s2

           Fig. 1.3. Second cookie-jar payment
</pre>

The cookie jar might conveniently be deposited, as shown in figure 1.4, during the withdrawal of the next batch of notes. It is verified by the bank much as a payment note would be: the roots must be present in the claimed multiplicity and the pre-image under f must not have been deposited before.

<pre>
                 1/(5*7*11*11)
          j, f(j)
     -----------------------------------------&gt;
PAYER                                        BANK

           Fig. 1.4. Cookie-jar deposit
</pre>

The cookie jar approach gives the effect of an online form of "offline checks",<sup><a href="#fnC89" id="refC89-4">[C89]</a></sup> in that notes of a fixed value are withdrawn and the unspent parts later credited to the payer during a refund transaction.

## Declared note value

Figure 2 depicts a somewhat different scheme, which allows change to be spent without an intervening withdrawal transaction. Withdrawals can be just as in the cookie-jar scheme, but here a single modulus is used for everything in the system. The products of public exponents representing the various amounts are as follows: d is the amount paid, g is the note value, the "change" c is g/d, and h is again the maximal amount, where d | g | h. A payment (still to the bank through a shop) includes first and second components that are the same as in the cookie-jar scheme. The third component is the amount of change c the payer claims should be returned. The fourth is a (blinded) number m, which could be an image under f used in a later payment just as n is used in this one.

<pre>
                 1/d        c
          n, f(n)   , c, m*s
     -----------------------------------------&gt;
PAYER                                        BANK
     &lt;------------------------------------------
                     +------------+
           1/c       |       1/c  | (Graphic padlock)
          m    * s * | f(f(n)   ) |
                     +------------+

           Fig. 2. Declared note value payment
</pre>

The signature returned contains a "protection" factor (shown inside the padlock). This factor ensures that the payer actually has the c-th root of f(n), by requiring that the payer apply f to it before dividing the result out of the signature. Without such protection, a payer could get the systemwide maximum change, regardless of how much change is actually due; with it, the change claimed can only be recovered if the corresponding roots on n are in fact known to the payer.

## Distributing change

The change returned in a payment can be divided into parts that fill in missing denominations in notes not yet spent. Suppose, for example, that the last payment is spent with d = 5*11, c = 3*7, and that m is formed by the payer as shown in the first line of Figure 3.1. Then unblinding after the payment yields the a shown in the second line.

(Use === for "is equivalent to")

<pre>
                         3        7
              m === f(n1)  * f(n2)

                     1/21
              a === m

           Fig. 3.1. Form of change returned
</pre>

From a, the two roots shown in the last two lines of Figure 3.2 are readily computed. (This technique is easily extended to include any number of separate roots.) Thus the values unused in the last payment fill in roots missing in notes n1 and n2.

<pre>
                   -1
              u = 3   mod 7

              v = 3u div 7

          1/7       3        -1  u        -v
     f(n1)    === (a  * f(n2)   )  * f(n1)

          1/3              -1/7
     f(n2)    === a * f(n1)

           Fig. 3.2. Distributing the change
</pre>

Because overpayment allows change to be returned in any chosen denominations (not shown), the payer has extra flexibility and is able to use all funds held. This also increases convenience by reducing the need for withdrawals.

## Hidden note value

Although the combination of the previous two subsections is quite workable, it may be desirable for the payer not to have to reveal c to the shop or the bank. Figure 4 shows a system allowing this. The payment message is just as in the declared note value protocol above, except that c is not sent. The protection factor (shown again in a lock) is also placed under the signature, but it is missing the extra f and is raised to a random power z chosen by the bank

<pre>
                 1/d     c
          n, f(n)   , m*s
     -----------------------------------------&gt;
PAYER                                        BANK
     &lt;------------------------------------------
                        +----------+
           d/h    g/h   |     zd/h |
          m    * s    * | f(n)     |, z
                        +----------+

           Fig. 4. Hidden note value payment
</pre>

If z were known to the payer before payment, then the payer could cheat by including f(n) in the third component; this would yield the payer the system-wide maximum change, even if none were due. Consider a single change exponent q. If z mod q is guessed correctly by a cheating payer, then the payer improperly gets the corresponding coin value. Thus the chance of successful cheating is 1/q. If, however, the divisors of h are chosen sufficiently large, quite practical security can be achieved. When the possibilities of distributing change and refunding are included, this scheme's privacy surpasses that of a coin system.

## Conclusion

Combining online coins improves efficiency, use of funds, convenience, and privacy.

## References

<ol class="references">
  <li id="fnC89">
    <p>Chaum, D., "Privacy Protected Payments: Unconditional Payer and/or Payee Anonymity," in Smart Card 2000, North-Holland, 1989, pp. 69-92.&nbsp;<a href="#refC89-1">↩</a>&nbsp;<a href="#refC89-2">↩</a>&nbsp;<a href="#refC89-3">↩</a>&nbsp;<a href="#refC89-4">↩</a></p>
  </li>

  <li id="fnCFN88">
    <p>Chaum, D., A. Fiat, & M. Naor, "Offline Electronic Cash," Proceedings of Crypto '88.&nbsp;<a href="#refCFN88">↩</a></p>
  </li>
</ol>
