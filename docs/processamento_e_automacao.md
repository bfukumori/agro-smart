# Processamento de dados e automação inteligente

## Fluxo de preparação

O arquivo `src/pipeline.py` executa as seguintes etapas:

1. lê o CSV da camada Raw;
2. converte tipos numéricos e booleanos;
3. valida timestamp, identificação do talhão e faixas físicas;
4. separa registros inválidos para auditoria;
5. ordena as leituras por horário e talhão;
6. calcula score e categoria de risco;
7. grava o dataset processado, alertas e resumo do dashboard.

As faixas aceitas são temperatura de -10 °C a 60 °C, umidade de 0% a 100% e luminosidade de 0 a 150.000 lux. Cada linha válida recebe `quality_status=APROVADO`.

## Regras de decisão

| Condição | Pontos | Decisão automática |
|---|---:|---|
| Umidade do solo menor que 20% sem previsão de chuva | 55 | Ativar irrigação por 30 minutos e medir novamente |
| Umidade do solo menor que 20% com previsão de chuva | 55 | Adiar irrigação e reavaliar após a chuva |
| Umidade do solo entre 20% e 30% | 30 | Gerar alerta de atenção |
| Temperatura maior que 32 °C | 25 | Evitar defensivos no horário |
| Luz acima de 75.000 lux e temperatura acima de 30 °C | 15 | Alertar para estresse térmico |

O score final determina a classificação: `NORMAL` abaixo de 30 pontos, `ATENCAO` de 30 a 59 e `CRITICO` a partir de 60. As regras são transparentes e não substituem a avaliação de um profissional agrônomo.

## Saídas

- `data/processed/telemetry_processed.csv`: dataset limpo e enriquecido.
- `data/output/alerts.json`: log das decisões automatizadas.
- `data/output/dashboard_summary.json`: visão consolidada para análise.
- `dashboard/data.js`: dados publicados no dashboard offline.
