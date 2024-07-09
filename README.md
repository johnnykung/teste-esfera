# Teste Engenheiro de Dados - Esfera

1 - Construção do ETL

A orquestração dos arquivos python foi feita pelo Apache Airflow, foi feita uma DAG que orquestra a limpeza/tratamento dos dados com a task "clean_data_task" utilizando a biblioteca pandas para extração dos arquivos CSV e a limpeza/transformação dos respectivos dataframes, como inserção de colunas, limpeza de dados desnecessários, transformação dos valores para float, entre outros.

A segunda task é a "upload_task" que é responsável pela ingestão dos dados tratados em um bucket do s3, nesta task é utilizado o S3 Hook disponibilizado pelo próprio Airflow.

<img src="https://github.com/johnnykung/teste-esfera/blob/main/Captura%20de%20tela%202024-07-08%20012402.png?raw=true" alt="Imagem da interface gráfica do Airflow executando a DAG de ETL dos CSVs">


2 - Leitura dos dados no bucket S3 pelo AWS Athena

Nesta etapa, com os dados tratados e carregados no S3, é feita algumas consultas na linguagem SQL dentro do AWS Athena para construção do banco de dados que irá alimentar a ferramenta de data vizz AWS QuickSight.

Para isso foram implementados os cõdigos em SQL que estão na pasta: receita.sql, despesas.sql, inner_join.sql, margem.sql.

Com exceção do "inner_join.sql", todos os códigos são criação de tabelas a partir dos dados tratados dentro do S3, utilizando o SerDe para leitura desses arquivos em formato CSV. O código do "inner_join.sql" é um inner join entre as tabelas de receita e despesas a fim de coletar os dados para criação da tabela margem (margem.sql), com isso eu consigo calcular a coluna de "margem" a partir da fórmula: (receita - despesa)/receita.

Esse KPI é um insight novo que pode ajudar na tomada de decisão, pois o seu valor pode definir o quanto de "sobra" cada recurso oferece (descrição um pouco mais completa no dashboard).



3 – Visualização e análise de dados no AWS QuickSight

Após a criação das tabelas no AWS Athena, é feito o carregamento dentro do ambiente do AWS QuickSight das 3 tabelas: Receita, Despesas e Margem.

Depois disso é aplicado alguns recursos de storytelling, como a disposição dos cards otimizados para leitura em Z e recursos visuais como barras para identificar o tamanho relativo de cada número. Também é possível filtrar o valor de um dado específico da tabela nos cards acima, basta apenas selecionar o dado que você quiser

<img src="https://raw.githubusercontent.com/johnnykung/teste-esfera/main/Captura%20de%20tela%202024-07-09%20195957.png?token=GHSAT0AAAAAACSZHTCORKALMGW6NYDOUWLSZUNYFRQ" alt="Imagem da interface gráfica do Airflow executando a DAG de ETL dos CSVs">
