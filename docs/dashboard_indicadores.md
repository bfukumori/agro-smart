# Dashboard analítico

O dashboard web foi desenvolvido como ferramenta equivalente de Business Intelligence. Ele funciona offline e contém quatro áreas navegáveis.

## Indicadores

- **Leituras processadas:** volume de registros aprovados no pipeline.
- **Talhões monitorados:** quantidade de unidades produtivas com telemetria.
- **Alertas ativos:** talhões cuja leitura mais recente exige atenção.
- **Talhões críticos:** unidades com score igual ou superior a 60.
- **Umidade nas últimas 24 horas:** gráfico comparativo da evolução temporal.
- **Condição por talhão:** status, umidade e temperatura da última leitura.
- **Decisões automatizadas:** ação, recomendação, horário e score de risco.

## Interação

A seção Telemetria possui um simulador visual do ESP32. O botão **Iniciar simulação** reproduz as leituras do dataset, atualiza os cartões dos sensores e registra cada evento no monitor serial. As seções Automação e Arquitetura apresentam, respectivamente, as regras rastreáveis e o fluxo completo da solução.
