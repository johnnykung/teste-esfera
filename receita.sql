CREATE EXTERNAL TABLE IF NOT EXISTS teste_esfera_receita.receita (
    fonte_de_recursos STRING,
    valor_receita DOUBLE,
    indice_receita STRING,
    nome_receita STRING
)

ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
    'separatorChar' = ',',
    'quoteChar' = '"',
    'skip.header.line.count' = '1'
)
LOCATION 's3://curso-eng-vendas1234/teste-esfera/receita/';
