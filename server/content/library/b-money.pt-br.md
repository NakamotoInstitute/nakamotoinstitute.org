---
title: b-money
translators:
  - luis-schwab
---

Estou fascinado pela cripto-anarquia de Tim May. Diferente das comunidades comumente associadas com a palavra "anarquia", na cripto-anarquia o governo não é temporariamente destruído, e sim permanentemente proibido de e permanentemente desnecessário. É uma comunidade onde a ameaça de violência é impotente porque violência é impossível, e violência é impossível porque seus participantes não podem ser vinculados aos seus nomes verdadeiros ou localizações físicas.

Até agora não é claro, até mesmo em teoria, como tal comunidade poderia funcionar. A comunidade é definida pela cooperação de seus participantes, e cooperação eficiente precisa de um meio de troca (dinheiro) e uma maneira de impor contratos. Tradicionalmente, esses servidor são providos pelo governo ou instituições financiadas pelo governo e apenas para entidades legais. Nesse artigo eu descrevo um protocolo pelo qual esses serviços podem ser oferecidos para e por entidades irrastreáveis.

Irei na verdade descrever dois protocolos. O primeiro é imprático, porque ele faz uso pesado de um canal de transmissão síncrono e imbloqueável. Ele irá porém motivar o segundo protocolo, mais prático. Em ambos os casos assumirei a existência de uma rede irrastreável, onde destinatários e remetentes são identificados apenas por pseudônimos digitais (ou seja, chaves públicas) e cada mensagem é assinada pelo remetente e criptografada para o destinatário.

No primeiro protocolo, cada participante mantém um registro (separado) de quanto cada pseudônimo detém. Essas contas definem coletivamente a propriedade do dinheiro, e como essas contas são atualizadas é o conteúdo deste protocolo.

1. Da criação do dinheiro. Qualquer um pode criar dinheiro ao transmitir a solução para um problema computacional que antes não tinha resolução. As únicas condições são que deve ser fácil determinar quanto esforço computacional foi despendido para resolver o problema e que a solução não deve ter valor, tanto prático como intelectual. O número de unidades monetárias criadas é igual a ao esforço computacional em termos de uma cesta padrão de commodities. Por exemplo, se um problema leva 100 horas para resolver em um computador que o resolve de maneira mais econômica, e são necessárias 3 cestas padrão para comprar 100 horas de tempo de computação naquele computador no mercado aberto, então assim que for transmitida a solução do problema todos creditam a conta do transmissor em 3 unidades.

2. Da transferência do dinheiro. Se Alice (dono do pseudônimo K<sub>a</sub>) quer transferir X unidades de dinheiro para Bob (dono do pseudônimo K<sub>b</sub>), ela transmite a mensagem "Eu dou X unidades de dinheiro para K<sub>b</sub>" assinada por K<sub>a</sub>. Após a transmissão, todos debitam a conta de K<sub>a</sub> de X unidades e creditam a conta de K<sub>b</sub> em X unidades, a não ser que isso criasse um saldo negativo na conta de K<sub>a</sub>. Nesse caso a mensagem seria ignorada.

3. Da efetivação de contratos. Um contrato válido deve incluir uma reparação máxima no caso de inadimplência para cada parte do contrato. Deve também incluir uma parte que exercerá arbitração caso haja uma disputa. Todas as partes do contrato incluindo o arbitrador devem transmitir suas assinaturas dele para que ele seja considerado válido.Ao transmitir o contrato e todas as assinaturas, cada participante debita da conta de cada parte o valor de sua reparação máxima e credita uma conta especial identificada por um hash seguro do contrato no valor da soma das reparações máximas. O contrato se torna efetivo se os débitos são concluídos em todas as partes sem gerar um saldo negativo, do contrário o contrato é ignorado e as contas voltam ao estado anterior. Um exemplo de contrato pode parecer com algo do tipo:

K<sub>a</sub> concorda em mandar a K<sub>b</sub> a solução do problema P antes de 00:00:00 01/01/2000. K<sub>b</sub> concorda em pagar K<sub>a</sub> 10 UM (Unidades Monetárias) antes de 00:00:00 01/01/2000. K<sub>c</sub> concorda em arbitrar em caso de disputa. K<sub>a</sub> concorda em pagar no máximo 1000 UM em caso de inadimplência. K<sub>b</sub> concorda em pagar no máximo 200 UM em caso de inadimplência. K<sub>c</sub> concorda em pagar no máximo 500 UM em caso de inadimplência.

4. Da conclusão de contratos. Se um contrato é concluído sem disputa, cada parte transmite uma mensagem assinada "O contrato com hash SHA-1 H conclui-se sem reparações." ou possivelmente "O contrato com hash SHA-1 H conclui-se com as seguintes reparações: ...". Depois de transmitidas todas as assinaturas, cada participante credita a conta de cada parte do valor de sua reparação máxima, remove a conta especial do contrato, e então credita ou debita a conta de cada parte de acordo com a rotina de reparação, se houver.

5. Da execução de contratos. Se as partes do contrato não estão em consenso a respeito de uma conclusão apropriada, mesmo com a ajuda de um árbitro, cada parte transmite uma reparação sugerida/rotina e quaisquer argumentos e evidências a seu favor. Cada participante faz a determinação a respeito da reparação e/ou multas, e modifica as contas de acordo.

No segundo protocolo, as contas de quem tem quanto dinheiro são mantidas por um subconjunto dos participantes (chamados a partir de agora de servidores) ao invés de todos. Esses servidores são conectados entre si por meio de um canal de transmissão no estilo da Usenet. O formato das mensagens de transação transmitidas permanece igual ao primeiro protocolo, mas os participantes afetados em cada transação devem verificar que a mensagem foi recebida e processada com sucesso em um subconjunto selecionado de servidores.

Já que têm-se que confiar nos servidores até certo ponto, algum mecanismo é necessário para mantê-los honestos. Cada servidor deve então depositar certa quantidade de dinheiro em uma conta especial para ser usado em possíveis multas ou recompensas para provas de conduta desonesta. Além disso, cada servidor deve publicar periodicamente e se comprometer com sua atual criação de dinheiro e registros de propriedade de dinheiro. Cada participante deve verificar que seu saldo está correto e que a soma de todos os saldos não é maior que a quantidade de dinheiro criado. Isso impede que servidores, até mesmo em total conspiração entre si, expandam permanentemente e sem custo algum a base monetária. Novos servidores podem usar os registros publicados para sincronizar com os servidores já existentes.

## Apêndice A: criação alternativa de b-money

Uma das partes mais problemáticas no protocolo b-money é a criação de dinheiro. Essa parte do protocolo requer que todos os mantenedores de contas decidam e concordem no custo de computações em particular. Infelizmente, pelo fato da tecnologia de computação avançar rapidamente e nem sempre em público, essa informação pode estar indisponível, imprecisa ou obsoleta, todas as quais causariam sérios problemas ao protocolo.

Então proponho um subprotocolo alternativo de criação de dinheiro, onde mantenedores de contas (todos no primeiro protocolo, ou servidores no segundo) decidam e concordem na quantidade de b-money a ser criado em determinado período, com o custo de criar aquele dinheiro determinado por um leilão. Cada período de criação de dinheiro é dividido em quatro fases, da seguinte maneira:

1. Planejamento. Os mantenedores de conta computam e negociam entre si para determinar um aumento ótimo da base monetária para o próximo período. Independente de um consenso ser atingido, cada um transmite sua cota de criação de dinheiro e quaisquer cálculos macroeconômicos feitos para suportar seus resultados.

2. Licitação. Qualquer um que desejar criar b-money transmite um lance na forma &lt;x,y&gt; onde x é a quantidade de b-money que ele quer criar, e y é um problema não resolvido de uma classe de problemas predeterminada. Cada problema dessa classe deve ter um custo nominal (em anos-MIPS, digamos) que seja aceito publicamente.

3. Computação. Depois de ver os lances, aqueles que fizeram lances na fase de licitação podem agora resolver os problemas contidos em seus lances e transmitir a solução.

4. Criação de dinheiro. Cada mantenedor de conta aceita os lances mais altos (entre aqueles que de fato transmitiram suas soluções) em termos de custo nominal por unidade de b-money criado e credita as contas dos licitantes de acordo.
