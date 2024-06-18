---
title: Governança do Bitcoin
slug: governanca-do-bitcoin
excerpt: Comprometer a dispensabilidade de confiança pode ajudar o preço do Bitcoin a achar um máximo local, às custas de achar um máximo global muito maior.
original_site: blog do Medium de Pierre Rochard
translators:
  - luis-schwab
---

## Por que nos importamos?

A governança do Bitcoin importa porque o Bitcoin é a primeira bem-sucedida, mas líquida, e mais conhecida criptomoeda. Nas palavras de [Michael Goldstein](https://x.com/bitstein/status/968913787628740608), "Dinheiro sólido é um pilar fundamental da civilização, e o Bitcoin restaura essa poderosa ferramenta de coordenação social." Se o modelo de governança do Bitcoin é falho, ele pode impedir que o Bitcoin alcance seu pleno potencial. Se a governança do Bitcoin é falha, os seus "acionistas" deveriam trabalhar para consertá-lo.

Discussões sobre a governança do Bitcoin tendem a focar em quem de fato toma as decisões, candidatos perenes incluem mineradores, nós e investidores. A razão e mecânica da governança são muitas vezes simplesmente implícitas ou até mesmo desconexas da realidade. Opiniões sobre a eficácia da governança passada são muitas influenciadas por quem "ganhou" ou "perdeu" a decisão específica, em vez de quão adequado o processo de decisão é.

## O que é a governança do Bitcoin?

A governança do Bitcoin é o processo pelo qual um conjunto de transações e regras de verificação de bloco são decididas, implementadas e aplicadas, de modo que indivíduos adotem essas regras para verificar se pagamentos que eles receberam em transações e blocos estão de acordo com sua definição subjetiva de "Bitcoin". Se dois ou mais indivíduos adotam o mesmo conjunto de regras de validação, eles formam um consenso social intersubjetivo sobre o que o "Bitcoin" é.

## Qual é a razão da governança do Bitcoin?

Existe um grande espectro de visões sobre qual razão da governança do Bitcoin deve ser.Quais resultados a governança deve otimizar?

- Matt Corallo [argumenta](http://bluematt.bitcoin.ninja/2017/02/28/bitcoin-trustlessness/) que a dispensabilidade de confiança é a propriedade mais importante do Bitcoin. Matt define dispensabilidade de confiança como "a habilidade de usar o Bitcoin sem confiar em nada exceto o software aberto que você executa". Sem a propriedade de dispensabilidade de confiança, todos os outros resultados positivos são colocados em risco.
- Daniel Krawisz [argumenta](/mempool/who-controls-bitcoin) que maximizar o valor de um bitcoin é o que a governança de fato otimiza. Daniel diz que "a regra geral sobre melhorias no Bitcoin […] é que melhorias que aumentam o valor do Bitcoin serão adotadas e aquelas que não, não serão.

No contexto da governança do Bitcoin, essas duas visões imitam a clássica divisão entre as éticas [deontológica](https://pt.wikipedia.org/wiki/Deontologia) e [consequencialista](https://pt.wikipedia.org/wiki/Consequencialismo), respectivamente. Eu sou a favor da abordagem deontológica do Matt, focando na dispensabilidade de confiança. Ao longo da história monetária, desde os antigos produtores de moedas até bancos centrais modernos, confiar em outros para produzir dinheiro resultou no abuso dessa confiança. Comprometer a dispensabilidade de confiança poderia ajudar o Bitcoin a achar um máximo local, ao custo de achar um máximo global muito mais alto. Além disso, não existe evidência de que o preço tenha correlação com melhorias ao protocolo do Bitcoin. Talvez o valor fundamental do Bitcoin seja afetado por melhorias, mas o Bitcoin é tão ilíquido e volátil que o preço não reflete de forma confiável seu valor fundamental. Se não pudermos observar as consequências de uma melhoria no valor do Bitcoin, a abordagem consequencialista parece ser inadequada.

Antes de podermos avaliar o atual processo de governança do Bitcoin em relação aos objetivos declarados de manter a dispensabilidade de confiança ou aumentar o valor do Bitcoin, deveríamos tentat definir como o atual processo de governança de fato funciona.

## Como o atual processo de governança no Bitcoin funciona?

O processo de governança do Bitcoin mantém um conjunto de regras de verificação. Em alto nível, esse longo conjunto de regras de verificação cobre sintaxe, estruturas de dados, limites para utilização de recursos, verificações de sanidade, bloqueios de tempo, reconciliação com a piscina de memória e ramo principal, a recompensa coinbase e cálculo de taxas, e verificação do cabeçalho de blocos. Reformar essas regras sem que consequências negativas surjam não é fácil.

A maioria dessas regras foram herdadas de Satoshi Nakamoto. Algumas foram adicionadas ou reformadas para consertar bugs ou vulnerabilidades de negação de serviço. Outras regras foram alteradas para permitir projetos novos e inovadores. Por exemplo, o novo opcode Check Sequence Verify foi adicionado para [permitir](https://github.com/bitcoin/bips/blob/master/bip-0112.mediawiki) novos scripts.

## Pesquisa

Cada alteração de regra começa com pesquisa. Por exemplo, o SegWit começou com pesquisa sobre consertar a maleabilidade de transações. A maleabilidade de transações havia se tornado um problema sério porque impedia que a Lightning Network fosse implantada no Bitcoin. Pesquisadores independentes e da indústria colaboraram em o que eventualmente se tornou o SegWit.

Críticos já apontaram ocasionais desconexões entre o que pesquisadores querem pesquisar, expectativas de usuários, e o que é bom para as propriedades da rede. Além disso, acadêmicos da ciência da computação preferem "simulações científicas" à "experimentos de engenharia". Isso tem sido uma fonte de tensão na comunidade de pesquisa.

## Proposta

Quando um pesquisador descobre a solução de um problema, ele compartilha sua mudanças propostas com outros desenvolvedores do protocolo. Isso pode ser na forma de um email para a lista de correio bitcoin-dev, um whitepaper formal, e/ou uma Bitcoin Improvement Proposal (BIP).

## Implementação

A proposta é implementada no software do nó pelo(s) pesquisador(es) que a propuseram, ou por outros desenvolvedores do protocolo que estão interessados nela. Se um pesquisador não consegue implementar uma proposta, ou se a proposta não atrai crítica favorável, ela permanecerá nessa fase até ser abandonada ou revisada.

Enquanto isso pode passar a impressão que contribuidores ao desenvolvimento do protocolo do Bitcoin podem vetar uma proposta, um pesquisador pode defender seu caso ao público e contornar os desenvolvedores existentes. Nesse cenário, o pesquisador fica em desvantagem se ele não tem reputação e credibilidade.

Outro problema na fase de implementação é que os mantenedores da [implementação de referência](https://github.com/bitcoin/bitcoin) não irão "mergear" uma implementação se ela for amplamente vista como controversa pelos desenvolvedores do protocolo Bitcoin e a mais ampla comunidade do Bitcoin. Os mantenedores da implementação de referência tem uma política deliberada de seguir as mudanças nas normas de consenso em vez de tentar impô-las. A implementação de referências em C++, hospedado em [github.com/bitcoin/bitcoin](github.com/bitcoin/bitcoin), é o sucessor direto da codebase de Satoshi. Ela continua sendo a implementação de nó mais popular devido à sua maturidade e dependabilidade.

Para driblar os mantenedores da implementação de referência e fazer mudanças no consenso mesmo assim, é tão simples quanto copiar a codebase do Bitcoin e lançar as mudanças propostas. Isso aconteceu com o User Activated Soft Fork (UASF) da [BIP-148](https://github.com/bitcoin/bips/blob/master/bip-148.mediawiki).

Uma proposta para mudar regras de validação pode ser implementada como um softfork ou um hardfork. Algumas propostas podem ser implementadas apenas como um hardfork. Da perspectiva de nós pré-fork, uma implementação softfork é compatível com versões futuras. Com um softfork, nós pré-fork não precisam atualizar seu software para continuar validando as regras de consenso pré-fork. Porém, esses nós pré-fork não estão validando mudanças nas regras feitas pelo soft-fork. Da perspectiva de nós pré-fork, um hardfork **não** é compatível com versões futuras. Nós pré-fork ficarão em uma rede diferente dos nós pós-fork.

Tem existido controvérsia sobre os efeitos de hard e softforks sobre a rede e seus usuários. Softforks são vistos como sendo mais seguros que hardforks, porque eles não requerem uma aceitação explícita, mas isso também pode ser visto como sendo coercivo. Alguém que não concorda com um softfork deve criar um hardfork para revertê-lo.

## Implantação

Uma vez que o software do nó é implementado, usuários devem ser convencidos a usar o software do nó. Nem todos usuários de nó tem a mesma importância. Por exemplo, "exploradores de blockchain" tem mais poder, já que muitos usuários dependem do seu nó. Adicionalmente, uma corretora pode determinar qual conjunto de regras de validação pertence à qual símbolo de ticker. Traders especuladores, grandes acionistas, e outras corretoras providenciam um contrapeso nesse poder sobre símbolos de ticker.

Usuários podem sinalizar em redes sociais que eles estão usando certa versão de software de nó, mas isso pode sofrer um [ataque Sybil](https://pt.wikipedia.org/wiki/Ataque_Sybil). O melhor teste de consenso é se o seu software de nó pode receber pagamentos os quais você considera ser bitcoins, e se você pode enviar pagamentos que o software de nó de suas contrapartes consideram ser bitcoins.

Softforks possuem um recurso de governança on-chain chamado [BIP-9 Bits de versão com timeout e atraso](https://github.com/bitcoin/bips/blob/master/bip-0009.mediawiki). Esse recurso mede o suporte de mineradores a um softfork de forma contínua. O suporte de mineradores a uma proposta é usada como uma medida proxy para o suporte da comunidade em geral. Infelizmente essa medida proxy pode ser imprecisa devido à centralização de mineração e conflitos de interesse entre mineradores e usuários. "Votação" on-chain por mineradores também perpetua o mito de que o Bitcoin é uma democracia de mineradores, e que apenas os mineradores decidem sobre a validade de transações e blocos. A BIP-9 é útil na medida em que reconhecemos e aceitamos as limitações de medidas proxy.

## Aplicação

Mudanças nas regras de validação são aplicadas pela rede descentralizada P2P de nós validadores. Nós usam as regras de verificação para verificar independentemente que pagamentos recebidas pelo operador do nó estão transações validadas do Bitcoin e estão incluídas em blocos do Bitcoin. Nós não irão propagar transações e blocos que quebram as regras. Na verdade, nós irão se desconectar de, e banir peers que estão mandando transações e blocos inválidos. Como [StopAndDecrypt](https://twitter.com/StopAndDecrypt/status/1002666361489969153) colocou, "O Bitcoin é uma fortaleza impenetrável de validação." Se todos determinarem que um bloco minerado é inválido, então a recompensa coinbase + taxas do minerador não tem valor algum.

O papel dos mineradores é prover uma função de time-stamping protegida por prova de trabalho. A quantidade de hashrate provida é baseada por um lado no custo de hardware e eletricidade, e a receita da recompensa coinbase + taxas do outro. Mineradores são mercenários, e no passado eles proveram sua função de time-stamping [sem validação completa](https://bitcoin.stackexchange.com/questions/38437/what-is-spv-mining-and-how-did-it-inadvertently-cause-the-fork-after-bip66-wa). Devido à centralização da mineração, mineradores não podem ser confiados para aplicar as regras de validação sozinhos.

## O atual modelo de governança do Bitcoin resultou em mais dispensabilidade de confiança?

Na minha opinião, o atual modelo de governança do Bitcoin impediu a degradação da dispensabilidade de confiança. O dramático aumento do número de transações on-chain nos últimos 5 anos parecia não ter fim. Se o modelo de governança não fosse resistente à sinalização dos mineradores no ano passado para duplicar o peso máximo do bloco, um precedente teria sido estabelecido que colocava vazão de transações acima da dispensabilidade de confiança.

## O atual modelo de governança do Bitcoin resultou em atualizações que aumentam o valor do Bitcoin?

Eu acho que é impossível estabelecer uma relação causal. O preço é muito maior do que era 2 anos atrás, mas parece ser um processo endógeno impulsionado pela psicologia dos traders, e não fundamentos tecnológicos. A respeito dos fundamentais, é inegável que a governança do Bitcoin permitiu as mudanças no consenso as quais a Lightning Network depende para operar. Eu estive experimentando estabelecer canais e fazer pagamentos Lightning: não há dúvida na minha mente que a LN aumenta o valor do Bitcoin.

---

Esse post foi inspirado na minha apresentação na conferência Chain-In:

<figure>
  <iframe class="w-full aspect-video" src="https://www.youtube.com/embed/yzQ4OPjPPP0?rel=0" allowfullscreen></iframe>
</figure>
