---
title: "Cuidado, Mineradores de Bitcoin: Blocos Inválidos Não Precisam Aplicar"
slug: blocos-invalidos-nao-precisam-aplicar
excerpt: O Bitcoin é uma fortaleza impenetrável de validação.
translators:
  - luis-schwab
---

## O Bitcoin é uma fortaleza impenetrável de validação.

_Assim como meu artigo sobre a [Lei de Moore](https://hackernoon.com/moores-observation-35f7b25e5773), esse é um trecho de um [artigo muito maior](https://hackernoon.com/sharding-centralizes-ethereum-by-selling-you-scaling-in-disguised-as-scaling-out-266c136fc55d). É bom o suficiente para servir como uma peça independente porque o equívoco que isso pretende acabar é um equívoco comumente levantado que se torna irritantemente repetitivo._

### Entendendo a rede Bitcoin sem matemática.

O Bitcoin é mais do que apenas uma cadeia de blocos. Quero ajudar você a entender como a _rede_ blockchain do Bitcoin é projetada porque isso ajudará você a preencher algumas lacunas à medida que você começa a adquirir mais conhecimento neste campo. Eu digo _rede blockchain_ porque o Bitcoin também tem uma rede de _canais de pagamento_ _(lightning)_ sobre ele que não afeta a estrutura da rede blockchain. Não vou discutir a rede lightning do Bitcoin neste artigo, pois não é tão relevante para os pontos que farei.

Abaixo está um exemplo aproximado da rede Bitcoin reduzida para 1000 nós de validação completa _(na verdade, há 115.000 atualmente)_. Cada nó aqui tem 8 conexões com outros nós, porque esta é a quantidade padrão de conexões que o cliente faz sem nenhuma alteração feita nele. Meu nó está aqui em algum lugar, e se você estiver executando um, ele também está lá. Os nós da Coinbase estão lá, os nós da Bitmain estão lá, e se Satoshi ainda estiver por aí, o nó de Satoshi também está lá.

_Observe que este é apenas um diagrama, e que a topologia de rede real pode (e provavelmente varia) disto. Alguns nós têm mais do que a quantidade padrão de conexões, enquanto outros podem optar por se conectar a um número limitado ou ficar atrás de apenas um outro nó. Não há como saber como ela realmente se parece porque **ela foi projetada com a privacidade em mente** (embora algumas empresas de monitoramento certamente tentem obter aproximações muito próximas) e os nós podem rotineiramente mudar quem são seus pares._

<figure>
  <img src="/static/img/mempool/bitcoin-miners-beware-invalid-blocks-need-not-apply/figure-1.png" alt="">
</figure>

<figure>
  <img src="/static/img/mempool/bitcoin-miners-beware-invalid-blocks-need-not-apply/figure-2.gif" alt="">
</figure>

Comecei com esse diagrama porque quero que você entenda que não há diferenças nesses nós porque **todos eles são validadores completos.** Isso significa que todos eles verificam toda a cadeia para garantir que cada transação e bloco sigam as regras. Isso será importante conforme eu explicar mais.

Os de dentro não são diferentes dos de fora, todos têm a mesma quantidade de conexões. Quando você inicia um novo nó, ele encontra pares e se torna mais um na colmeia. A maior distância _neste gráfico_ de qualquer um desses nós para outro é 6. Na vida real, há alguns desvios nessa distância porque [encontrar novos pares](https://en.bitcoin.it/wiki/Satoshi_Client_Node_Discovery) não é um processo perfeitamente automatizado que distribui todos uniformemente, mas geralmente, adicionar mais nós à rede não muda isso. Existem 6 graus de Kevin Bacon, e em 6 saltos minha transação está nas mãos de _(quase)_ todos os nós, **se for válida.**

Vou selecionar “meu” nó deste grupo e arrastá-lo para fora, para que eu possa demonstrar o que acontece quando eu crio uma transação e anuncio para a rede. Abaixo, você verá meu nó bem à direita, e então verá os outros 8 nós _(meus pares)_ aos quais o meu está conectado.

<figure>
  <img src="/static/img/mempool/bitcoin-miners-beware-invalid-blocks-need-not-apply/figure-3.png" alt="">
</figure>

Quando eu crio uma transação e "envio para o mundo", ela na verdade vai apenas para esses 8 pares. Como o Bitcoin é projetado do zero para tornar cada nó um nó totalmente validador, quando esses 8 nós recebem minha transação, eles verificam se ela é válida antes de enviá-la para _seus_ 8 pares. **Se minha transação for inválida, ela nunca quebrará a "superfície" da rede.** Meus pares nunca enviarão essas transações ruins para seus pares. Na verdade, eles nem sabem que eu criei essa transação. Não há como eles saberem, e eles tratam todos os dados como iguais, mas se eu continuasse enviando transações inválidas para qualquer um dos meus 8 pares, eles acabariam me bloqueando. Isso é feito por eles automaticamente para evitar que eu envie spam da minha conexão com eles. Não importa quem você é, ou quão grande é sua empresa, **sua transação não será propagada se for inválida.**

Agora, digamos que você não esteja executando um nó completo, mas esteja usando um [cliente SPV](https://en.bitcoin.it/wiki/Thin_Client_Security). Existem vários clientes SPV para o desktop e para seu celular. Alguns deles são Electrum, Armory, Bread e Samourai Wallet. Clientes SPV são vinculados a um nó específico. Alguns podem ser configurados para alterar aquele ao qual se conectam ao longo do tempo, mas eles ainda são vinculados. É assim que o tethering se parece:

<figure>
  <img src="/static/img/mempool/bitcoin-miners-beware-invalid-blocks-need-not-apply/figure-4.png" alt="">
</figure>

Quero que você observe que este é apenas um diagrama, e é fácil demonstrar tethering usando um nó que _aparenta_ estar na borda, mas não há uma borda _real_, e tethering é tethering onde quer que esse nó esteja dentro deste diagrama. Eu destaquei isso em amarelo. Os nós aos quais estão sendo amarrados são verdes, e os pontos azuis são clientes SPV. Todas as informações que vão ou vêm do cliente SPV passam pelo nó ao qual estão amarrados. Eles dependem desse nó. **Eles não fazem parte da rede. Eles não são nós.**

É aqui que fica divertido, e onde outras pessoas tentam deturpar como a rede realmente funciona: **E se eu quisesse começar a minerar?**

_Minerar_ um bloco é o ato de _criar_ um bloco. Assim como uma transação que você deseja enviar, você deve criar o bloco e anunciá-lo à rede. Qualquer nó pode anunciar um novo bloco, não há nada de especial nesse processo, _você só precisa de um novo bloco_. A mineração tem se tornado cada vez mais difícil, mas se você quiser, pode comprar hardware especializado e conectá-lo ao seu nó pessoal.

<figure>
  <img src="/static/img/mempool/bitcoin-miners-beware-invalid-blocks-need-not-apply/figure-5.png" alt="">
</figure>

Lembra daquela parte sobre transações inválidas? O mesmo vale para blocos, mas você precisa entender algo muito específico sobre como os blocos são criados.

Primeiro assista a este vídeo. Pulei para a parte importante sobre hashing, usando nonces _(valor aleatório)_ e anexando a cadeia com esse novo **cabeçalho** de bloco:

<figure>
  <img src="/static/img/mempool/bitcoin-miners-beware-invalid-blocks-need-not-apply/figure-6.jpg" alt="">
</figure>

Por favor, assista a coisa toda se tiver tempo. É pessoalmente meu vídeo favorito explicando como a mineração funciona.

Quando você chega à parte seguinte do vídeo onde os rótulos “Prev hash” são aplicados, esses são os cabeçalhos de bloco:

<figure>
  <img src="/static/img/mempool/bitcoin-miners-beware-invalid-blocks-need-not-apply/figure-7.png" alt="">
</figure>

O que não é mencionado neste vídeo é que você pode criar cabeçalhos de blocos válidos **mesmo se todas as transações dentro do bloco forem inválidas**. Ainda requer a mesma quantidade de tempo para minerar blocos com transações inválidas como para minerar um bloco com transações válidas. O incentivo para gastar todo esse tempo e energia criando tal bloco seria forçar uma transação que o recompensa com Bitcoin que não é seu. É por isso que é importante que todos os nós verifiquem não apenas os cabeçalhos de bloco, **mas as transações também**. É isso que impede os mineradores de gastar esse tempo. Como **todos** os nós verificam, **nenhum** minerador pode enganar o sistema. Se todos os nós não verificassem, você teria que confiar naqueles que _verificam_. Isso separaria os nós em "tipos", e o único tipo que importaria seriam aqueles que verificam.

E se você se juntar a um pool de mineração? Você pode fazer isso porque a mineração é muito difícil para você fazer sozinho, ou se você for uma entidade um pouco maior, pode preferir uma renda estável em vez de uma esporádica. Muitos mineradores fazem isso, e eles conectam seu hardware especializado diretamente a um pool de mineração usando um protocolo totalmente diferente chamado [protocolo de mineração Stratum](https://en.bitcoin.it/wiki/Stratum_mining_protocol). Assim como criar uma transação com seu celular sem nó, **você não precisa executar um nó para conectar seu hardware a um pool de mineração.** Você pode minerar sem executar um nó, e muitos mineradores fazem exatamente isso. Aqui está o que parece abaixo em azul. Eu usei o Slush Pool para este exemplo:

<figure>
  <img src="/static/img/mempool/bitcoin-miners-beware-invalid-blocks-need-not-apply/figure-8.png" alt="">
</figure>

Lembre-se, eu arrastei esses nós executados em pool para fora do diagrama para fins de demonstração. Assim como qualquer outro nó, esses nós executados em pool precisam de pares. Eles precisam de pares para receber transações e blocos, e precisam de pares para anunciar os blocos que eles criam. Permita-me reiterar novamente: **Todos os nós validam todos os blocos e todas as transações.**

Se qualquer um desses pools anunciar um bloco inválido, seus pares saberão **porque eles validam completamente**, e eles não o enviarão para outros nós. Assim como as transações, **blocos inválidos não entram na rede.**

Aqui está outra maneira de ver isso sem retirar esses nós do diagrama. Abaixo está um minerador privado que não quer ser conhecido, ele tem 8 pares aleatórios, e **nenhum desses pares sabe que é um minerador**. Novamente, isso é intencionalmente projetado dessa forma por razões de privacidade. Não há como nenhum nó na rede saber que o bloco que recebeu foi _criado_ por seu par, ou _retransmitido_ por seu par. Tudo o que eles sabem é se é válido ou não, e se for, eles enviam, se não for, eles não enviam.

<figure>
  <img src="/static/img/mempool/bitcoin-miners-beware-invalid-blocks-need-not-apply/figure-9.png" alt="">
</figure>

Espero que você esteja entendendo, e não acredito que usei nenhuma matemática ou equação sofisticada para chegar aqui. Gostaria de prosseguir porque sinto que esta é uma cobertura completa, mas há uma coisa final que gostaria de abordar porque é este aspecto final que é usado para confundir outros que não entendem completamente tudo o que acabei de explicar. É usado de forma tão desenfreada que preciso abordá-lo.

<figure>
  <img src="/static/img/mempool/bitcoin-miners-beware-invalid-blocks-need-not-apply/figure-10.png" alt="">
  <figcaption>
    <a href="https://x.com/VitalikButerin/status/1000232465540136960">https://twitter.com/VitalikButerin/status/1000232465540136960</a>
  </figcaption>
</figure>

Meu comentário original estava falando sobre clientes leves, também chamados de clientes SPV, e como eles não fazem parte da rede. Eu demonstrei isso acima com os pontos azuis amarrados. Sua resposta tenta implicar que os nós que mineram são os únicos nós cuja rejeição importa. _Lembre-se: os nós não têm como saber quais outros nós mineraram um bloco versus quem retransmitiu um bloco, **isso foi projetado intencionalmente.**_

Agora, um diagrama final para que eu possa tentar explicar a lógica que é usada quando as pessoas dizem "apenas os nós de mineração importam". Alguns mineradores se conectam diretamente a outros mineradores para que, de sua lista de pares com a rede, alguns deles também sejam outros mineradores. **Nem todos os mineradores fazem isso**. Alguns desses mineradores que se conectam diretamente também usam redes de retransmissão _opcionais_ como a rede FIBRE [sendo projetada](http://bluematt.bitcoin.ninja/2016/07/07/relay-networks/) pelo desenvolvedor do Bitcoin Core [Matt Corallo](https://x.com/TheBlueMatt), mas mesmo essa rede secundária não é exclusiva para mineradores, qualquer um pode participar, incluindo você ou eu, e ela está lá apenas para ajudar a bloquear a retransmissão pela rede. De qualquer forma, as pessoas tentam argumentar que essa interconectividade de “nós que mineram” _(seja usando algo como FIBRE ou não)_ implica que eles são os únicos que importam, e isso é absurdo:

<figure>
  <img src="/static/img/mempool/bitcoin-miners-beware-invalid-blocks-need-not-apply/figure-11.png" alt="">
</figure>

Neste exemplo, deixei os pares do nó dentro do diagrama. Você já deve ter entendido. Eles rejeitam blocos inválidos. Esse grupo de nós dentro dos círculos verdes definitivamente não é o único conjunto de nós que importa nessa rede.

<figure>
  <blockquote>
    <p>O Bitcoin é uma fortaleza impenetrável de verificação.</p>
    <p>Não importa se você criou a transação/bloco, ou se outra pessoa o mandou para você: Se não é válido não vai entrar.</p>
    <p>Todos os nós impõem validação em conjunto..</p>
    <p>Algumas pessoas ainda parecem não entender esse conceito.</p>
  </blockquote>
  <figcaption>— <cite>@StopAndDecrypt</cite>, <time datetime="2018-06-01">June 1, 2018</time></figcaption>
</figure>
