# Arquitetura integrada da solução AgroSmart

## Visão geral

A Fase 7 consolida a coleta, o processamento, a decisão e a visualização em um fluxo executável. A origem dos dados é uma simulação determinística de sensores IoT. O pipeline em Python preserva a camada bruta, valida e transforma as leituras, aplica regras agronômicas e publica um resumo analítico consumido pelo dashboard web.

```mermaid
flowchart LR
  A[ESP32 ou simulador Python] -->|temperatura, ar, solo, luz| B[(Raw CSV)]
  B --> C[Validação e transformação Python]
  C --> D[(Processed CSV)]
  D --> E[Motor de regras e score]
  E --> F[(Alertas e resumo JSON)]
  F --> G[Dashboard web]
  G --> H[Indicadores, histórico e recomendações]
```

## Componentes

| Componente | Responsabilidade | Entrada | Saída |
|---|---|---|---|
| ESP32 e sensores | Ler condições do ambiente | DHT22, sensor de solo e LDR | Telemetria serial em JSON |
| Simulador Python | Produzir uma massa reproduzível para demonstração | Perfis de três talhões e semente fixa | `sensor_readings.csv` |
| Camada Raw | Preservar os dados de origem | Leituras simuladas | CSV sem enriquecimento |
| Pipeline de preparação | Validar faixa, tipo, identificador e timestamp | CSV Raw | CSV processado e rejeições |
| Motor de regras | Interpretar os valores e gerar ações | Dados processados | Risco, alertas e recomendações |
| Camada analítica | Consolidar os dados para consumo | Histórico e decisões | JSON de resumo e `data.js` |
| Dashboard | Apoiar a decisão do operador | Dados da camada analítica | KPIs, gráficos, status e logs |

## Implantação

A aplicação pode ser executada diretamente com Python e navegador ou em um contêiner Docker. Como os dados do dashboard são publicados como JavaScript estático, a demonstração não depende de serviços externos nem de credenciais.
