-- voos_limpos.sql
SELECT
    "empresa_aerea",
    "n_voo",
    "aeroporto_origem_nome_uf_pais_" AS aeroporto_origem,
    "aeroporto_destino_nome_uf_pais" AS aeroporto_destino,
    "etapas_previstas",

    -- Transforma o texto '3,23' em número 3.23
    CAST(REPLACE("percentuais_de_cancelamentos", ',', '.') AS NUMERIC) AS perc_cancelamentos,
    CAST(REPLACE("percentuais_de_atrasos_superiores_a_30_minutos", ',', '.') AS NUMERIC) AS perc_atrasos_30min,
    CAST(REPLACE("percentuais_de_atrasos_superiores_a_60_minutos", ',', '.') AS NUMERIC) AS perc_atrasos_60min

-- `source` é uma função do dbt para referenciar tabelas brutas
FROM {{ source('public', 'voos_brutos') }}