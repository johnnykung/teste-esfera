CREATE EXTERNAL TABLE IF NOT EXISTS teste_esfera_despesas.despesas (
    fonte_de_recursos STRING,
    valor_despesas DOUBLE,
    indice_despesas STRING,
    nome_despesas STRING
)

ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
    'separatorChar' = ',',
    'quoteChar' = '"',
    'skip.header.line.count' = '1'
)
LOCATION 's3://curso-eng-vendas1234/teste-esfera/despesas/';
