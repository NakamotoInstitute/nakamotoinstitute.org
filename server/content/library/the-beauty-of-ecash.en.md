---
title: The Beauty of ECash
authors:
  - hal-finney
date: 1994-03-16
categories:
  - cryptography
doctype: essay
external: https://web.archive.org/web/20140421063207/http://www.finney.org/~hal/beauty_ecash.html
---

It occurs to me that digital cash could be a collector's item. Paper money is widely collected, as are coins. I got a book out of the library on old American paper money, and many of the old bills are startlingly beautiful. Interestingly, the old money is still legal tender so there is a floor under the value of the bills that you collect.

Until 1861, the U.S. did not issue any paper money, only coins. In those days, paper money was issued by private banks (usually with state charters). The money was backed by dollars, coins, which the bank owned. Unfortunately, capitalism is a dynamic system and in those days bank failures were no more unusual than corporate failures are today. When this happened, the bank's notes became worthless. Counterfeiting was also a big problem with the thousands of different banks issuing notes. It is interesting to speculate that digital cash might lead to an electronic system with some similarities to those old days.

Collecting digital cash has some problems. Collectors are generally attracted to items that are beautiful, interesting, and rare. Digital cash is interesting enough, but its beauty is rather abstract. Rarity is also hard to evaluate; each individual note has a unique serial number, and what it has in common with other notes of its denomination is the bank key and the exponent. Uncirculated notes are generally more valuable than others in the paper world; with digital banknotes the only way to tell whether it has been "circulated" would be to have access to the bank's database of spent notes, to verify that the note had never been deposited.

Rarity could be determined by the bank's key and exponent. The Magic Money system has a provision for the bank to periodically move to another set of exponents to represent the same denominations (in order to keep the size of the note database from growing too large). If banks would do this at regular intervals, then particularly the early issues would be relatively rare. One might even have an early banknote notarized (digitally timestamped) so that one could prove its value in later years.

Beauty is harder to deal with. Strictly speaking, digital cash is invisible, consisting only of an information pattern in RAM chips or on a disk. The numbers which represent the cash can be printed out, though, and this representation could perhaps have some beauty. Unfortunately, in my opinion several lines of random hex digits are not beautiful.

I have been working on ideas to display the information in digital cash in some other way that is more esthetic. It would be nice if the display somehow only worked for correctly signed cash notes, with forged cash not displaying anything nice. My general idea is to display a "fingerprint" of each individual banknote, something that is unique to that note and which has a sort of beauty.

One idea I have worked on is to seed a 1-D cellular automaton with a bit pattern based on the digital cash. This seed is then processed by the CA algorithm to produce some pattern, with each row being a function of the previous row. My thought was to start the CA at the top and the bottom of the screen with the two different functions applied to the cash which should be equal if the cash validates (taking the number to the proper exponent on one hand, and applying the MD5 hash of the serial number on the other, for the case of magic money). Then we work inwards with the two seeds. Proper cash will produce a symmetrical pattern. By choosing good CA rules, the patterns will be different for each bill, some nicer than others, leading to attractive fractal-looking patterns for many bills. When you wanted to "look at your money" you could run the program on the digital cash. People might even trade for especially attractive bills.

A similar idea is to use the cash as the basis for some fractal algorithm. Many fractals have the property that most of the plane is plain, while only a fraction looks really fractal. Digital cash has the property that when exponentiated it leads to a number most of whose bits are fixed but which has a small number of varying bits. If we had a mapping which took the fixed digicash bits onto the interesting parts of the fractal, then fake cash would not produce pretty pictures, while real cash would produce some part of a beautiful fractal. Again, you would have validation and beauty being tied together.

I've been doing some experiments with the first idea, hoping to produce something nice. With a little more thought I hope to come up with a viewer for your Magic Money that will bring out its natural beauty and rarity. This will be a must for all serious collectors of digicash.

Hal Finney  
hal@rain.org
