---
title: Elektronik Paranın Güzelliği
translators:
  - efe-cini
translation_url: https://www.nakamotoenstitusu.com/post/elektronik-para
---

Aklıma dijital paranın bir koleksiyon parçası olabileceği fikri geldi. Kâğıt paralar da madenî paralar gibi yaygın olarak koleksiyonu yapılan şeylerdir. Kütüphanede eski Amerikan kâğıt paraları üzerine bir kitap bulmuştum ve eski banknotların çoğu şaşırtıcı derecede güzel görünüyordu. İlginçtir ki, eski paralar hâlâ yasal ödeme aracıdır, dolayısıyla topladığınız kâğıt paraların değerini belirleyen bir dayanak vardır.

1861 yılına kadar ABD kâğıt para basmıyordu, sadece madenî para basıyordu. O günlerde kâğıt para özel bankalar tarafından (genellikle eyalet tüzükleri ve imtiyazları ile) ihraç ediliyordu. Bu kâğıt para, bankanın sahip olduğu dolar cinsinden madenî paralarla destekleniyordu. Ne var ki, kapitalizm dinamik bir sistemdir ve o günlerde banka iflasları da günümüzdeki şirket iflasları kadar sıradandı. Bu gerçekleştiğinde, bankanın banknotları değersiz hâle geliyordu. Banknot basan binlerce farklı bankanın varlığı nedeniyle de kalpazanlık büyük bir sorun teşkil ediyordu. Dijital paranın o eski günlere benzer bir elektronik sisteme yol açabileceğini düşünmek ise hayli ilginç olabilir.

Dijital para koleksiyonu yapmanın bazı sorunları var. Koleksiyoncular genellikle güzel, ilginç ve nadir bulunan nesnelere ilgi duyarlar. Dijital para bir hayli ilginçtir, ancak güzelliği oldukça soyuttur. Nadirliği değerlendirmek de zordur; her bir banknotun benzersiz bir seri numarası vardır ve kendi değerindeki diğer banknotlarla ortak noktası bağlı oldukları banka anahtarı ve üstel değerdir. Tedavüle girmemiş banknotlar kâğıt dünyasında genellikle diğerlerinden daha değerlidir; dijital banknotlarda “tedavüle girip girmediğini” anlamanın tek yolu bankanın kullanılmış banknotlar veri tabanına erişerek banknotun hiç yatırılmadığını doğrulamaktır.

Nadirlik bankanın anahtarı ve üstel değeri ile belirlenebilir. Magic Money sisteminde, bankanın (banknot veri tabanının boyutunun çok büyümesini önlemek adına) aynı değerdeki banknotları temsil etmek üzere periyodik olarak başka bir üstel değer setine geçmesi için bir provizyon bulunmaktadır. Eğer bankalar bunu düzenli aralıklarla yaparlarsa, o zaman özellikle ilk ihraçlar nispeten nadir olacaktır. Hatta erken dönem bir banknotun noter onaylı (ya da dijital olarak zaman damgalı) olması ve böylece daha sonraki yıllarda değerinin kanıtlanması bile mümkün olabilir.

Güzellik ile uğraşmak ise daha zordur. Açık konuşmak gerekirse, dijital para görünmezdir, yalnızca RAM çiplerinde veya bir diskte bulunan bir bilgi deseninden oluşur. Yine de parayı temsil eden sayıların çıktısı alınabilir ve bu temsil belki bir miktar güzelliğe sahip olabilir. Ne yazık ki, bana göre birkaç satırlık rastgele hex rakamları güzel sayılmaz.

Dijital paradaki bilgileri daha estetik olabilecek başka bir şekilde görüntülemek için bazı fikirler üzerinde çalışıyorum. Ekranın bir nevi sadece doğru şekilde imzalanmış nakit paralar için çalışması, sahte paralar içinse güzel bir şey göstermemesi iyi olurdu. Benim genel fikrim, her bir banknotun “parmak izini”, yani o banknota özgü olan ve bir tür güzelliğe sahip olan bir şeyi görüntülemesi yönündedir.

Üzerinde çalıştığım fikirlerden biri, dijital paraya dayalı bir bit desenine sahip 1 boyutlu bir hücresel otomatın tohumunu yerleştirmek üzerineydi. Bu tohum daha sonra CA [Certificate Authority; Sertifika Otoritesi] algoritması tarafından işlenerek her satırın bir önceki satırın bir fonksiyonu olduğu bir desen üretilecek. Benim düşüncem CA’yı ekranın üstünden ve altından, paraya uygulanan ve paranın doğrulanması durumunda (bir yandan sayıyı uygun üstel değere getirirken, diğer yandan Magic Money durumunda seri numarasının MD5 özet fonksiyonunu uygulayarak) eşit olması gereken iki farklı işlevle çalıştırmaktı. Daha sonra iki tohumla içe doğru çalışırız. Doğru [sahte olmayan] nakit simetrik bir desen üretecektir. İyi CA kuralları seçildiğinde, desenler her banknot için farklı olacak, bazıları diğerlerinden daha güzel olacak ve birçok banknot için göz alıcı fraktal görünümlü desenler ortaya çıkacaktır. “Paranıza bakmak” istediğinizde programı dijital nakit üzerinde çalıştırabilirsiniz. İnsanlar özellikle çekici banknotlar için takas bile yapabilirler.

Benzer bir fikir de parayı bazı fraktal algoritmalar için temel olarak kullanmaktır. Birçok fraktal, düzlemin çoğunun düz olması, sadece bir kısmının gerçekten fraktal görünmesi özelliğine sahiptir. Dijital para, üstelleştirildiğinde çoğu biti sabit olan ancak az sayıda değişken biti olan bir sayıya yol açma özelliğine sahiptir. Eğer sabit dijital nakit bitlerini fraktalın ilginç kısımlarına yerleştiren bir eşleme yapsaydık, sahte nakit güzel resimler üretmezken, gerçek nakit güzel bir fraktalın bir kısmını üretirdi. Yine, doğrulama ve güzellik birbirine bağlanmış olurdu.

Güzel bir şey üretmeyi umarak ilk fikirle bazı deneyler yapıyorum. Biraz daha düşünerek Magic Money’niz için onun doğal güzelliğini ve nadirliğini ortaya çıkaracak bir görüntüleyici bulmayı umuyorum. Bu, tüm ciddi Digicash koleksiyoncuları için olmazsa olmaz olacaktır.

Hal Finney  
hal@rain.org
