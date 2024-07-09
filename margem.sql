CREATE EXTERNAL TABLE IF NOT EXISTS margem (
    receita DOUBLE,
    fonte_receita STRING,
    fonte_despesas STRING,
    despesas DOUBLE,
    margem DOUBLE
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
WITH SERDEPROPERTIES (
    'serialization.format' = ',',
    'field.delim' = ',',
    'skip.header.line.count' = '1'
) 
STORED AS TEXTFILE
LOCATION 's3://curso-eng-vendas1234/athena-resultados/Inner%20Join%20Receita%20%2B%20Despesa/2024/07/08/'
TBLPROPERTIES ('has_encrypted_data'='false');