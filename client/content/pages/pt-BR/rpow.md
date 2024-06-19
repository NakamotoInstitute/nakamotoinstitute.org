Prova-de-Trabalho Reutilizável (Reusable Proof-of-Work (RPOW) em inglês) foi inventada por Hal Finney como sendo um protótipo de dinheiro digital com base na [teoria de colecionáveis](/library/shelling-out/) de Nick Szabo. O RPOW foi um passo inicial significativo na história do dinheiro digital e foi um precursor do Bitcoin. Embora nunca se pretendeu ser mais do que um protótipo, o RPOW era um software muito sofisticado que teria sido capaz de servir uma enorme rede se tivesse pegado.

## Contexto Histórico

Nos anos 1990 os Cypherpunks começaram a brincar com a ideia de um dinheiro digital cujo valor não fosse dependente na organizaram que o emitiu. Depois de Nick Szabo, esta forma de dinheiro digital seria reconhecida como sendo limitada na oferta, e, consequentemente, utilizável como dinheiro, sendo, de forma verificável, difícil de criar. Isso poderia ser feito definindo unidades do dinheiro digital em termos de prova-de-trabalho. Algumas propostas de colecionáveis digitais circularam na lista de correio cypherpunk, incluindo [b-money](/library/b-money/) por Wei Dai e [Bit Gold](/library/bit-gold/) por Nick Szabo. RPOW era o único digital colecionável para funcionar como um pedaço de software.

## Como Funciona

Um cliente RPOW cria um token RPOW fornecendo uma string de proof-work de uma determinada dificuldade, assinada por sua chave privada. O servidor em seguida registra esse token como pertencente à chave de assinatura. O cliente pode então dar o token para outra chave assinando uma ordem de transferência para uma chave pública. O servidor então registra devidamente o token como pertencente à chave privada correspondente.

O problema do gasto duplo é fundamental para todo o dinheiro digital. RPOW resolve este problema mantendo a propriedade dos tokens registrados em um servidor confiável. No entanto, o RPOW foi construído com um modelo de segurança sofisticado destinado a tornar o servidor que gerencia o registo de todos os tokens RPOW mais confiável do que um banco comum. Os servidores deveriam ser executados no processador criptográfico seguro IBM 4758, que é capaz de verificar com segurança o hash do software que está sendo executado. Servidores RPOW são capazes de cooperar para atender mais requisições.

Para mais informações, por favor veja a [página original](/finney/rpow/index.html) de Hal Finney, que inclui um [overview](/finney/rpow/index.html), um [FAQ](/finney/rpow/faqs.html), uma [página de teoria](/finney/rpow/theory. tml), uma [apresentação](/finney/rpow/slides/slide001.html), e uma página muito interessante chamada [World of RPOW](/finney/rpow/world. tml) que explica como o RPOW teria escalado para servir o planeta inteiro.

O código original pode ser encontrado no GitHub [aqui](https://github.com/NakamotoInstitute/RPOW).

_Um agradecimento especial a Fran e Jason Finney, esposa e filho de Hal, por compartilharem o código original do RPOW e arquivos do site._
