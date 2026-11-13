# Sprint 2 - Histórias de Usuário e Testes

- Projeto: DespesaClara

(IA usada para estruturação, complemento de ideias e formatação do arquivo .md)

## História de Usuário 1: Validação do Arquivo de Entrada
**Como** jornalista, 
**quero** informar o caminho de um arquivo CSV do Portal da Transparência, 
**para que** o sistema valide se a estrutura e os campos necessários estão corretos antes de iniciar a análise.

### Critérios de Aceitação:
1. O sistema deve receber o caminho do arquivo via linha de comando ou prompt de terminal de forma validável.
2. O sistema deve rejeitar o arquivo e exibir um erro se a extensão não for `.csv`.
3. O sistema deve ler o cabeçalho e verificar a presença de colunas obrigatórias (ex: "Órgão Superior", "Valor Empenhado", "Valor Liquidado", "Valor Pago").
4. O sistema deve exibir uma mensagem de erro clara no terminal especificando quais colunas estão faltando caso o CSV seja incompatível.
5. O sistema deve exibir uma mensagem de sucesso no terminal e prosseguir para a próxima etapa caso a validação do arquivo seja bem-sucedida.

---

## História de Usuário 2: Seleção e Filtragem de Órgãos
**Como** membro de controle social, 
**quero** filtrar os dados por um ou mais órgãos específicos, 
**para** focar a minha análise apenas nas instituições que estou monitorando.

### Critérios de Aceitação:
1. O sistema deve permitir a entrada de múltiplos nomes ou códigos de órgãos através do terminal.
2. O sistema deve ignorar diferenças entre letras maiúsculas e minúsculas ao buscar os órgãos na base.
3. O sistema deve exibir um aviso no terminal caso um órgão solicitado pelo usuário não seja encontrado nos registros do arquivo.
4. O sistema deve filtrar o conjunto de dados em memória para conter apenas as linhas correspondentes aos órgãos encontrados.
5. Se nenhum filtro for especificado pelo usuário, o sistema deve perguntar se deseja processar todos os órgãos do arquivo ou cancelar a operação.

---

## História de Usuário 3: Processamento e Separação de Estágios da Despesa
**Como** estudante de orçamento público, 
**quero** que o sistema calcule e sumarize separadamente os valores de empenho, liquidação e pagamento, 
**para** não misturar os conceitos orçamentários e financeiros na minha pesquisa.

### Critérios de Aceitação:
1. O sistema deve somar os valores agrupando-os por órgão executor.
2. O sistema deve manter os totais de "Empenho", "Liquidação" e "Pagamento" em variáveis ou colunas estritamente separadas, sem criar um valor genérico de gasto.
3. O sistema deve converter as strings de valores monetários do padrão brasileiro (com vírgulas e pontos) para o tipo numérico adequado antes da soma.
4. O sistema deve tratar campos vazios ou nulos nas colunas financeiras como valor zero (`0.00`) para não quebrar o cálculo.
5. O sistema deve garantir que os valores resultantes da soma mantenham precisão de duas casas decimais.

---

## História de Usuário 4: Geração de Relatório CSV
**Como** jornalista, 
**quero** exportar os resultados da análise sumarizada para um novo arquivo CSV, 
**para** abrir os dados limpos em planilhas e criar gráficos para a minha reportagem.

### Critérios de Aceitação:
1. O sistema deve gerar um arquivo `.csv` de saída contendo apenas as colunas de "Órgão", "Total Empenhado", "Total Liquidado" e "Total Pago".
2. O arquivo gerado deve ser salvo automaticamente na mesma pasta de execução do script com o prefixo `relatorio_`.
3. O arquivo de saída deve utilizar um delimitador (como ponto e vírgula `;`) que não conflite com os separadores decimais da formatação monetária.
4. O sistema deve exibir o caminho completo do arquivo salvo no terminal.
5. O sistema deve capturar falhas de permissão de escrita (ex: arquivo aberto em outro programa) e exibir uma mensagem de erro recomendando o fechamento do arquivo.

---

## História de Usuário 5: Resumo Analítico no Terminal
**Como** conselheiro de políticas públicas, 
**quero** visualizar um resumo direto no terminal ao final da execução, 
**para** ter uma visão rápida e comparativa dos órgãos sem precisar abrir o arquivo exportado imediatamente.

### Critérios de Aceitação:
1. O sistema deve imprimir no terminal os resultados sumarizados de cada órgão logo após a geração do relatório CSV.
2. A exibição no terminal deve estar estruturada em formato de tabela ou lista alinhada, separando os três estágios da despesa lado a lado.
3. Os valores no terminal devem ser formatados como moeda brasileira (ex: `R$ 1.500.250,00`) para facilitar a leitura visual.
4. O sistema deve calcular e exibir uma linha final contendo a soma total de todos os órgãos analisados naquela consulta.
5. O terminal deve truncar ou abreviar o nome do órgão caso ele ultrapasse 50 caracteres, garantindo que a formatação da tabela não quebre.# Sprint 2 - Histórias de Usuário e Testes
