SELECT 
    SUM(r.valor_receita) AS receita,
    r.fonte_de_recursos AS fonte_receita,
    d.fonte_de_recursos AS fonte_despesas,
    SUM(d.valor_despesas) AS despesas,
    CASE 
        WHEN SUM(r.valor_receita) != 0 THEN (SUM(r.valor_receita) - SUM(d.valor_despesas)) / SUM(r.valor_receita)
        ELSE NULL
    END AS margem
FROM 
    teste_esfera_receita.receita AS r
INNER JOIN 
    teste_esfera_despesas.despesas AS d
ON 
    r.fonte_de_recursos = d.fonte_de_recursos
GROUP BY 
    r.fonte_de_recursos, d.fonte_de_recursos