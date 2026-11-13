SPRINT 1 - DEFINIÇÃO DA PROPOSTA
Projeto: DespesaClara
 
 
1. IDENTIFICAÇÃO DO TRIO
 
Integrante 1: Eduardo Haag Piassa da Silva
Integrante 2: Gabriel Mancuso Bonfim
Integrante 3: Nathália Rodrigues Nunes Gonçalves
 
 
2. DESCRIÇÃO DO SISTEMA
 
O DespesaClara será um sistema em Python para analisar dados da execução da despesa pública federal por órgão. Seu público-alvo será formado por pessoas que consultam o Portal da Transparência de forma recorrente e precisam comparar órgãos sem refazer o tratamento da planilha a cada consulta, como jornalistas que apuram pautas sobre gastos federais, conselheiros e participantes de controle social que acompanham a execução da despesa e estudantes que usam esses dados em trabalhos sobre orçamento público. O problema abordado será a necessidade de transformar os registros do arquivo em informações resumidas para consulta e comparação. A entrada será um arquivo CSV do Portal da Transparência. O sistema verificará a estrutura do arquivo e a validade dos campos necessários à análise. Em seguida, permitirá selecionar órgãos e organizar seus valores de execução, respeitando o significado dos campos presentes na base. A saída será um relatório CSV com os resultados da análise, acompanhado de um resumo apresentado no terminal. O projeto não terá interface gráfica, não aceitará outros modelos de CSV e não realizará julgamentos sobre irregularidades nos gastos.
 
 
3. PESQUISA QUE JUSTIFICA O SISTEMA
 
O Portal da Transparência do Governo Federal disponibiliza informações sobre a execução orçamentária e financeira das despesas públicas. Entre suas possibilidades de consulta, apresenta uma visão por órgão ou entidade executora e permite baixar dados para a realização de cruzamentos e análises próprias (CGU, [s.d.]a; CGU, [s.d.]b).
 
Duas fontes ajudam a identificar quem usa esses dados. A primeira é uma notícia do Serpro sobre uma oficina de dados governamentais realizada para jornalistas em Brasília, em maio de 2011, na qual o Portal da Transparência é descrito como uma fonte muito usada em matérias jornalísticas. Na mesma notícia, uma jornalista de O Globo que trabalha com contas públicas afirma que a abertura de dados facilita a apuração e que é importante aprender a navegar nessas ferramentas (SERPRO, 2011). A segunda é a cartilha Controle Social, da Controladoria-Geral da União, que apresenta o Portal como ferramenta de apoio ao controle social e descreve o Programa Olho Vivo no Dinheiro Público, voltado à capacitação de conselheiros de políticas públicas, lideranças locais, agentes públicos municipais, professores, estudantes e cidadãos em geral (CGU, 2012). Juntas, as fontes indicam que o Portal é consultado por jornalistas e por pessoas envolvidas em controle social, e que estudantes fazem parte do público que a própria CGU busca capacitar para o uso dessas informações.
 
A cartilha da CGU também sustenta o cuidado do sistema com o significado dos campos. Ela explica que toda despesa pública passa por três estágios, empenho, liquidação e pagamento, e que o empenho cria a obrigação de pagar, mas não é o pagamento em si (CGU, 2012). Por isso, o DespesaClara não tratará todos os valores como uma única medida de gasto: as regras de cálculo seguirão as colunas e a documentação do arquivo, preservando a distinção entre informações orçamentárias e financeiras.
 
Com isso, o público-alvo do DespesaClara é o conjunto de pessoas que consultam o Portal com frequência e precisam produzir resumos e comparações por órgão. A contribuição esperada é tornar essa consulta mais organizada e reproduzível, sem precisar montar uma nova análise manual a cada vez. O projeto não substituirá o Portal da Transparência nem identificará fraudes ou avaliará a qualidade da gestão pública. As fontes demonstram a existência dos dados e o uso do Portal por esses perfis, mas não comprovam a necessidade específica de uma ferramenta como esta: essa necessidade é um recorte proposto pela equipe, e não uma conclusão de pesquisa com usuários já realizada.
 
 
4. REFERÊNCIAS
 
CONTROLADORIA-GERAL DA UNIÃO. Consulta de despesas públicas. Portal da Transparência do Governo Federal. [s.d.]a. Disponível em: https://portaldatransparencia.gov.br/despesas/lista-consultas. Acesso em: 30 out. 2026.
 
CONTROLADORIA-GERAL DA UNIÃO. Portal da Transparência do Governo Federal. [s.d.]b. Disponível em: https://portaldatransparencia.gov.br/. Acesso em: 30 out. 2026.
 
CONTROLADORIA-GERAL DA UNIÃO. Controle Social: orientações aos cidadãos para participação na gestão pública e exercício do controle social. 3. ed. reimpr. Brasília, DF: CGU, 2012. (Coleção Olho Vivo). Disponível em: https://www.gov.br/cgu/pt-br/centrais-de-conteudo/publicacoes/controle-social/arquivos/controlesocial2012.pdf. Acesso em: 30 out. 2026.
 
SERPRO. Serpro promove oficina de dados governamentais para jornalistas. Brasília, DF, 10 maio 2011. Disponível em: https://www.serpro.gov.br/menu/noticias/noticias-antigas/serpro-promove-oficina-de-dados-governamentais-para-jornalistas. Acesso em: 30 out. 2026.