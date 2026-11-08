from pathlib import Path

from docx import Document
from docx.enum.section import WD_ORIENT, WD_SECTION
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Inches, Pt, RGBColor


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "document" / "Relatorio_AgroSmart_Fase7.docx"
DARK = "14231C"
GREEN = "176B45"
PALE = "F1F6F2"
GRAY = "D9E1DC"


def set_cell_shading(cell, fill):
    properties = cell._tc.get_or_add_tcPr()
    shading = properties.find(qn("w:shd"))
    if shading is None:
        shading = OxmlElement("w:shd")
        properties.append(shading)
    shading.set(qn("w:fill"), fill)


def set_cell_margins(cell, top=100, start=120, bottom=100, end=120):
    properties = cell._tc.get_or_add_tcPr()
    margins = properties.first_child_found_in("w:tcMar")
    if margins is None:
        margins = OxmlElement("w:tcMar")
        properties.append(margins)
    for name, value in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        item = margins.find(qn(f"w:{name}"))
        if item is None:
            item = OxmlElement(f"w:{name}")
            margins.append(item)
        item.set(qn("w:w"), str(value))
        item.set(qn("w:type"), "dxa")


def set_table_borders(table, color=GRAY):
    properties = table._tbl.tblPr
    borders = properties.first_child_found_in("w:tblBorders")
    if borders is None:
        borders = OxmlElement("w:tblBorders")
        properties.append(borders)
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        item = borders.find(qn(f"w:{edge}"))
        if item is None:
            item = OxmlElement(f"w:{edge}")
            borders.append(item)
        item.set(qn("w:val"), "single")
        item.set(qn("w:sz"), "4")
        item.set(qn("w:color"), color)


def add_table(doc, headers, rows, widths=None, font_size=9):
    table = doc.add_table(rows=1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    set_table_borders(table)
    for index, header in enumerate(headers):
        cell = table.rows[0].cells[index]
        cell.text = str(header)
        set_cell_shading(cell, DARK)
        set_cell_margins(cell)
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        for run in cell.paragraphs[0].runs:
            run.font.bold = True
            run.font.color.rgb = RGBColor(255, 255, 255)
            run.font.size = Pt(font_size)
    for row_index, values in enumerate(rows):
        cells = table.add_row().cells
        for index, value in enumerate(values):
            cells[index].text = str(value)
            set_cell_margins(cells[index])
            cells[index].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            if row_index % 2:
                set_cell_shading(cells[index], PALE)
            for paragraph in cells[index].paragraphs:
                paragraph.paragraph_format.space_after = Pt(0)
                for run in paragraph.runs:
                    run.font.size = Pt(font_size)
    if widths:
        for row in table.rows:
            for index, width in enumerate(widths):
                row.cells[index].width = Inches(width)
    spacer = doc.add_paragraph()
    spacer.paragraph_format.space_after = Pt(0)
    return table


def add_caption(doc, text):
    paragraph = doc.add_paragraph()
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    paragraph.paragraph_format.space_before = Pt(4)
    paragraph.paragraph_format.space_after = Pt(10)
    run = paragraph.add_run(text)
    run.italic = True
    run.font.size = Pt(9)
    run.font.color.rgb = RGBColor(90, 105, 97)


def add_steps(doc, items):
    for index, item in enumerate(items, start=1):
        paragraph = doc.add_paragraph()
        paragraph.paragraph_format.left_indent = Cm(0.45)
        paragraph.paragraph_format.first_line_indent = Cm(-0.35)
        paragraph.add_run(f"{index}. ").bold = True
        paragraph.add_run(item)


def add_code(doc, lines, size=8.5):
    for line in lines:
        paragraph = doc.add_paragraph()
        paragraph.paragraph_format.left_indent = Cm(0.45)
        paragraph.paragraph_format.space_after = Pt(1)
        run = paragraph.add_run(line)
        run.font.name = "Consolas"
        run.font.size = Pt(size)
        run.font.color.rgb = RGBColor.from_string(GREEN)


def add_path_paragraph(doc, label, path):
    paragraph = doc.add_paragraph()
    paragraph.add_run(label + ": ").bold = True
    path_run = paragraph.add_run(path)
    path_run.font.name = "Consolas"
    path_run.font.size = Pt(9.5)
    path_run.font.color.rgb = RGBColor.from_string(GREEN)


def page_break(doc):
    doc.add_page_break()


doc = Document()
section = doc.sections[0]
section.page_width = Inches(8.5)
section.page_height = Inches(11)
section.top_margin = Cm(2.0)
section.bottom_margin = Cm(1.9)
section.left_margin = Cm(2.1)
section.right_margin = Cm(2.1)

styles = doc.styles
styles["Normal"].font.name = "Aptos"
styles["Normal"].font.size = Pt(10.5)
styles["Normal"].font.color.rgb = RGBColor.from_string(DARK)
styles["Normal"].paragraph_format.space_after = Pt(7)
styles["Normal"].paragraph_format.line_spacing = 1.12
for name, size in (("Title", 27), ("Heading 1", 19), ("Heading 2", 13), ("Heading 3", 11)):
    style = styles[name]
    style.font.name = "Aptos Display"
    style.font.size = Pt(size)
    style.font.bold = True
    style.font.color.rgb = RGBColor(0, 0, 0)
    style.paragraph_format.space_before = Pt(11)
    style.paragraph_format.space_after = Pt(7)
    style.paragraph_format.keep_with_next = True

title_properties = styles["Title"]._element.get_or_add_pPr()
title_border = title_properties.find(qn("w:pBdr"))
if title_border is not None:
    title_properties.remove(title_border)

# ==========================================
# CAPA DO RELATÓRIO
# ==========================================
paragraph = doc.add_paragraph()
paragraph.paragraph_format.space_after = Pt(40)
run = paragraph.add_run("FIAP  ·  FASE 7  ·  AGROSMART")
run.font.size = Pt(10)
run.font.bold = True
run.font.color.rgb = RGBColor.from_string(GREEN)

title = doc.add_paragraph(style="Title")
title.add_run("Relatório Consolidado da Plataforma AgroSmart")
title.paragraph_format.space_after = Pt(12)

subtitle = doc.add_paragraph()
subtitle_run = subtitle.add_run(
    "Arquitetura Consolidada, Execução Funcional Ponta a Ponta, Pipeline DevSecOps, "
    "Monitoramento Contínuo, Mineração de Processos e Apresentação de Produto (Pitch)"
)
subtitle_run.font.size = Pt(14)
subtitle_run.font.color.rgb = RGBColor(88, 104, 95)
subtitle.paragraph_format.space_after = Pt(45)

doc.add_paragraph(
    "Este relatório documenta a entrega final da solução AgroSmart como uma plataforma completa, "
    "integrada e apresentável como produto comercial. O documento consolida a evolução arquitetural, "
    "as evidências de execução com IoT/simulação, o pipeline DevSecOps com SAST e linter, a observabilidade "
    "com logs estruturados, a análise de processos (Process Mining) e o pitch de mercado da solução."
)

add_table(
    doc,
    ["Requisito da Entrega", "Situação do Requisito", "Artefatos Comprobatórios"],
    [
        ("1. Arquitetura Final da Solução", "Concluído", "Diagrama consolidado, componentes e fluxo de dados"),
        ("2. Execução da Plataforma (Sistema)", "Concluído", "Simulação IoT, pipeline, regras e dashboard interativo"),
        ("3. Pipeline DevSecOps", "Concluído", "GitHub Actions, Docker non-root, flake8 e Bandit SAST"),
        ("4. Monitoramento e Execução", "Concluído", "Logs estruturados, healthcheck JSON e indicador de status"),
        ("5. Análise de Processos (Process Mining)", "Concluído", "Event Log (946 evts), DFG, gargalos e roteiro 5-8 min"),
        ("6. Apresentação do Produto (Pitch)", "Concluído", "Slides em PPTX e HTML, proposta de valor e roteiro 5 min"),
    ],
    [2.3, 1.2, 3.2],
)

paragraph = doc.add_paragraph()
paragraph.paragraph_format.space_before = Pt(25)
paragraph.add_run("Equipe de Desenvolvimento (FIAP)").bold = True
doc.add_paragraph(
    "Bruno Fukumori - RM 99486 · Victor Jaber - RM 550173\n"
    "Bruno Andrade Lima de Araújo - RM 550817 · Bruno Perdigão Santos - RM 98681\n"
    "Vinicius Messias dos Santos - RM 550463"
)

page_break(doc)

# ==========================================
# GUIA DE AVALIAÇÃO
# ==========================================
doc.add_heading("Guia Rápido de Reprodução e Avaliação", level=1)
doc.add_paragraph(
    "A solução foi concebida com máxima reproduzibilidade. A banca avaliadora pode executar e validar "
    "todos os requisitos da entrega utilizando exclusivamente o ecossistema fornecido."
)

doc.add_heading("Comandos de Execução Local", level=2)
add_code(
    doc,
    [
        "# 1. Executar o fluxo completo (Simulação + Pipeline + Process Mining + Healthcheck):",
        "python src/run_all.py",
        "",
        "# 2. Iniciar o Dashboard Web Analítico:",
        "python -m http.server 8080 --directory dashboard",
        "# Abrir http://localhost:8080 no navegador",
        "",
        "# 3. Executar a bateria de Testes Automatizados:",
        "python -m unittest discover -s tests -v",
        "",
        "# 4. Executar a Auditoria Completa DevSecOps (Linting + SAST + Testes):",
        "python tools/run_devsecops.py",
        "",
        "# 5. Executar múltiplos ciclos de Monitoramento Contínuo:",
        "python src/monitor.py --cycles 3 --delay 0.5",
    ],
)

doc.add_heading("Execução via Container Docker", level=2)
add_code(
    doc,
    [
        "docker compose up --build",
        "# Acessar http://localhost:8080 no navegador",
        "# O container opera com usuário não-root restrito e possui probe de healthcheck nativo.",
    ],
)

page_break(doc)

# ==========================================
# SEÇÃO 1: ARQUITETURA FINAL DA SOLUÇÃO
# ==========================================
doc.add_heading("1. Arquitetura Final da Solução", level=1)
doc.add_paragraph(
    "A arquitetura final do AgroSmart consolida a evolução de todo o projeto acadêmico em uma estrutura "
    "altamente coesa, escalável e desacoplada em cinco camadas principais. O fluxo conecta a telemetria na borda "
    "agrícola até o consumo analítico e a governança operacional."
)

doc.add_picture(str(ROOT / "evidencias" / "arquitetura_integrada.png"), width=Inches(6.2))
add_caption(doc, "Figura 1 - Arquitetura Integrada da Solução AgroSmart")

add_table(
    doc,
    ["Camada", "Componentes Principais", "Entrada", "Saída / Responsabilidade"],
    [
        ("Coleta (Edge)", "ESP32, DHT22, Solo Capacitivo, LDR", "Variáveis ambientais físicas", "Telemetria serial JSON"),
        ("Ingestão (Raw)", "sensor_readings.csv / Ingestion Buffer", "Payloads dos sensores", "Preservação da camada bruta"),
        ("Processamento", "pipeline.py / Data Validator", "Dataset Raw", "Tipagem, validação e higienização"),
        ("Decisão & Risco", "classify_risk / Rule Engine", "Dados processados limpos", "Scoring, alertas e comandos"),
        ("Analítica & Ação", "Dashboard Web, data.js, alerts.json", "Decisões e telemetria", "KPIs, gráficos e atuação"),
    ],
    [1.1, 1.8, 1.6, 2.2],
)

doc.add_heading("1.1 Explicação do Fluxo de Dados Ponta a Ponta", level=2)
add_steps(
    doc,
    [
        "Entrada: O microcontrolador ESP32 (ou simulador determinístico) amostra temperatura, umidade do ar, umidade do solo e luminosidade.",
        "Buffer Raw: Os dados são ingeridos na camada Raw preservando fielmente os valores brutos para auditoria.",
        "Higienização & Qualidade: O worker de validação checa limites físicos (-10 a 60 °C, 0 a 100% de umidade) e aplica quality_status=APROVADO.",
        "Inferência Agronômica: O motor de regras correlaciona umidade crítica do solo com previsão de chuva e temperatura, gerando ações automatizadas.",
        "Saída & Ação: O resultado enriquece a camada Silver, gera logs de alerta em JSON e atualiza o dashboard analítico em tempo real.",
    ],
)

detail_section = doc.add_section(WD_SECTION.NEW_PAGE)
detail_section.orientation = WD_ORIENT.LANDSCAPE
detail_section.page_width = Inches(11)
detail_section.page_height = Inches(8.5)
detail_section.top_margin = Cm(1.6)
detail_section.bottom_margin = Cm(1.6)
detail_section.left_margin = Cm(1.7)
detail_section.right_margin = Cm(1.7)

doc.add_heading("1.2 Arquitetura Detalhada e Contratos de Serviço", level=1)
doc.add_paragraph(
    "A visão detalhada em formato horizontal evidencia os contratos de dados e as fronteiras entre os componentes."
)
doc.add_picture(str(ROOT / "evidencias" / "arquitetura_detalhada.png"), width=Inches(9.55))
add_caption(doc, "Figura 2 - Diagrama Detalhado de Componentes, Entradas, Saídas e Interfaces")

port_section = doc.add_section(WD_SECTION.NEW_PAGE)
port_section.orientation = WD_ORIENT.PORTRAIT
port_section.page_width = Inches(8.5)
port_section.page_height = Inches(11)
port_section.top_margin = Cm(2.0)
port_section.bottom_margin = Cm(1.9)
port_section.left_margin = Cm(2.1)
port_section.right_margin = Cm(2.1)

# ==========================================
# SEÇÃO 2: EXECUÇÃO DA PLATAFORMA (SISTEMA FUNCIONAL)
# ==========================================
doc.add_heading("2. Execução da Plataforma (Sistema Funcional)", level=1)
doc.add_paragraph(
    "A solução demonstra funcionamento completo e integrado. A entrada é alimentada tanto pelo circuito físico "
    "simulado no Wokwi com código C++ para ESP32 quanto pelo gerador determinístico Python de 48 horas em 3 talhões."
)

doc.add_picture(str(ROOT / "evidencias" / "simulacao_sensores.png"), width=Inches(6.2))
add_caption(doc, "Figura 3 - Telemetria dos Sensores e Monitor Serial do ESP32")

doc.add_heading("2.1 Exemplo Concreto de Entrada e Saída", level=2)
doc.add_paragraph(
    "Abaixo é apresentado o ciclo de transformação de uma medição crítica no Talhão 3 (TLH-003):"
)

doc.add_paragraph("Entrada (Camada Raw - data/raw/sensor_readings.csv):").bold = True
add_code(
    doc,
    [
        '{"reading_id": "SIM-047-3", "timestamp": "2026-09-26T23:00:00Z", "plot_id": "TLH-003",',
        ' "temperature_c": 21.5, "air_humidity_pct": 68.9, "soil_moisture_pct": 4.5,',
        ' "luminosity_lux": 36.0, "rain_forecast": false}',
    ],
)

doc.add_paragraph("Saída (Decisão Automatizada - data/output/alerts.json):").bold = True
add_code(
    doc,
    [
        '{',
        '  "alert_id": "ALT-0104",',
        '  "timestamp": "2026-09-26T23:00:00Z",',
        '  "plot_id": "TLH-003",',
        '  "severity": "ATENCAO",',
        '  "risk_score": 55,',
        '  "action_type": "IRRIGACAO",',
        '  "recommendation": "Ativar irrigação por 30 minutos e medir novamente."',
        '}',
    ],
)

wokwi_section = doc.add_section(WD_SECTION.NEW_PAGE)
wokwi_section.orientation = WD_ORIENT.LANDSCAPE
wokwi_section.page_width = Inches(11)
wokwi_section.page_height = Inches(8.5)
wokwi_section.top_margin = Cm(1.6)
wokwi_section.bottom_margin = Cm(1.6)
wokwi_section.left_margin = Cm(1.7)
wokwi_section.right_margin = Cm(1.7)

doc.add_heading("2.2 Circuito Eletrônico do ESP32 no Wokwi", level=1)
doc.add_paragraph(
    "O circuito do ESP32 integra o sensor DHT22 aos pinos digitais, um potenciômetro simulando o sensor capacitivo "
    "de solo nas portas analógicas (ADC) e o módulo LDR para intensidade luminosa."
)
doc.add_picture(str(ROOT / "evidencias" / "wokwi_circuito.png"), width=Inches(9.55))
add_caption(doc, "Figura 4 - Circuito AgroSmart Montado e Operacional no Wokwi")

port_section2 = doc.add_section(WD_SECTION.NEW_PAGE)
port_section2.orientation = WD_ORIENT.PORTRAIT
port_section2.page_width = Inches(8.5)
port_section2.page_height = Inches(11)
port_section2.top_margin = Cm(2.0)
port_section2.bottom_margin = Cm(1.9)
port_section2.left_margin = Cm(2.1)
port_section2.right_margin = Cm(2.1)

# ==========================================
# SEÇÃO 3: PIPELINE DEVSECOPS DA SOLUÇÃO
# ==========================================
doc.add_heading("3. Pipeline DevSecOps da Solução", level=1)
doc.add_paragraph(
    "Em consonância com as melhores práticas de engenharia de software e segurança cibernética (Shift-Left Security), "
    "foi implementada uma esteira automatizada DevSecOps cobrindo linting, testes, análise estática de segurança "
    "e container hardening."
)

add_table(
    doc,
    ["Estágio do Pipeline", "Ferramenta", "Escopo da Verificação", "Status da Auditoria"],
    [
        ("Qualidade de Código", "flake8", "Auditoria de conformidade PEP 8 e complexidade", "100% APROVADO (0 erros)"),
        ("Segurança SAST", "Bandit", "Varredura estática de vulnerabilidades CWE", "APROVADO (0 vulnerabilidades)"),
        ("Auditoria de Pacotes", "pip-audit", "Verificação de CVEs conhecidas em dependências", "CONFORME"),
        ("Testes Automatizados", "unittest", "Bateria de 6 testes de regras e mineração", "100% OK (6/6 aprovados)"),
        ("Container Seguro", "Docker", "Build com usuário non-root restrito e healthcheck", "IMAGEM HARDENED"),
    ],
    [1.8, 1.2, 2.5, 1.5],
)

doc.add_heading("3.1 Configurações de Segurança e Container", level=2)
doc.add_paragraph(
    "O Dockerfile adota boas práticas de isolamento de privilégios com criação do usuário não-root appuser, "
    "eliminação de pacotes desnecessários e instrução nativa de HEALTHCHECK a cada 10 segundos:"
)
add_code(
    doc,
    [
        "# Trecho do Dockerfile Seguro:",
        "FROM python:3.12-alpine",
        "RUN addgroup -S appgroup && adduser -S appuser -G appgroup",
        "WORKDIR /app",
        "COPY . .",
        "RUN chown -R appuser:appgroup /app",
        "USER appuser",
        "HEALTHCHECK --interval=10s --timeout=3s --retries=3 \\",
        "  CMD wget -q --spider http://127.0.0.1:8080/ || exit 1",
    ],
)
add_path_paragraph(doc, "Workflow CI/CD", ".github/workflows/devsecops.yml")
add_path_paragraph(doc, "Script de Execução Local", "tools/run_devsecops.py")
add_path_paragraph(doc, "Evidência de Execução", "evidencias/devsecops_execution_log.txt")

page_break(doc)

# ==========================================
# SEÇÃO 4: MONITORAMENTO E EXECUÇÃO AUTOMATIZADA
# ==========================================
doc.add_heading("4. Monitoramento e Execução Automatizada", level=1)
doc.add_paragraph(
    "A plataforma dispõe de um módulo dedicado de observabilidade e monitoramento contínuo (src/monitor.py), "
    "capaz de executar ciclos recorrentes de amostragem, emitir logs estruturados em formato logfmt com timestamps "
    "UTC de alta precisão e expor métricas operacionais em JSON."
)

add_table(
    doc,
    ["Indicador Monitorado", "Valor Medido", "Interpretação Operacional"],
    [
        ("Taxa de Conformidade de Dados", "100,0%", "Zero rejeições nos limites físicos agronômicos"),
        ("Vazão de Processamento", "880 leituras/s", "Processamento em tempo real com altíssima eficiência"),
        ("Latência Média de Ciclo", "163,5 ms", "Ciclo ponta a ponta (coleta, regras, mineração e logs)"),
        ("Status de Saúde (Healthcheck)", "HEALTHY", "Todos os subsistemas operando normalmente sem erros"),
        ("Probe HTTP do Container", "HTTP 200 OK", "Servidor ativo e pronto para requisições de dashboard"),
    ],
    [2.3, 1.4, 3.1],
)

doc.add_heading("4.1 Exemplo de Log Estruturado e Healthcheck", level=2)
add_code(
    doc,
    [
        "[2026-10-30T18:34:44.189Z] [INFO] [component=AgroSmartMonitor] system=bootstrap event=monitor_started",
        "[2026-10-30T18:34:44.546Z] [INFO] [component=AgroSmartMonitor] cycle=1 records=144 alerts=2 status=QUALITY_VALIDATED",
        "[2026-10-30T18:34:44.717Z] [INFO] [component=AgroSmartMonitor] cycle=1 event=healthcheck_updated status=HEALTHY throughput=880 rec/s",
    ],
)
add_path_paragraph(doc, "Arquivo de Logs Contínuos", "data/output/agrosmart_system.log")
add_path_paragraph(doc, "Arquivo de Status Healthcheck", "data/output/health_status.json")
add_path_paragraph(doc, "Evidência Consolidada de Monitoramento", "evidencias/monitoramento_logs.txt")

page_break(doc)

# ==========================================
# SEÇÃO 5: ANÁLISE DE PROCESSOS (PROCESS MINING)
# ==========================================
doc.add_heading("5. Análise de Processos e Mineração (Process Mining)", level=1)
doc.add_paragraph(
    "A solução incorpora mineração de processos aplicada à telemetria agronômica. Cada leitura gera uma cadeia "
    "de eventos auditáveis em formato padronizado (case_id, activity, timestamp, resource, duration_ms)."
)

doc.add_picture(str(ROOT / "evidencias" / "process_mining_map.png"), width=Inches(6.2))
add_caption(doc, "Figura 5 - Mapa do Processo (DFG) com Variantes e Tempos de Transição")

doc.add_heading("5.1 Variantes de Processo Identificadas", level=2)
add_table(
    doc,
    ["Variante", "Trilha de Atividades Executadas", "Casos", "Frequência"],
    [
        ("VAR-01", "Coleta -> Ingestão -> Validação -> Risco -> Conformidade -> Dashboard", "62", "43,1%"),
        ("VAR-02", "Coleta -> Ingestão -> Validação -> Risco -> Alerta Atenção -> Dashboard -> Notificação", "45", "31,2%"),
        ("VAR-03", "Coleta -> Ingestão -> Validação -> Risco -> Ativar Irrigação -> Dashboard -> Notificação", "26", "18,1%"),
        ("VAR-04", "Coleta -> Ingestão -> Validação -> Risco -> Adiar Chuva -> Dashboard -> Notificação", "6", "4,2%"),
        ("VAR-05", "Coleta -> Ingestão -> Validação -> Risco -> Estresse Térmico -> Dashboard -> Notificação", "5", "3,5%"),
    ],
    [1.0, 4.3, 0.6, 0.9],
)

doc.add_heading("5.2 Análise de Gargalos e Oportunidades de Otimização", level=2)
doc.add_paragraph(
    "A mineração identificou que a atividade 'Decisao_Ativar_Irrigacao' é o principal gargalo de tempo (320 ms), "
    "devido ao handshake e confirmação de relés eletromecânicos de válvulas solenóides. "
    "A recomendação proposta é implementar protocolo de acionamento assíncrono via broker MQTT com QoS 1. "
    "Além disso, a oportunidade de melhoria de maior valor é o fechamento de malha (Closed-Loop Feedback), "
    "correlacionando a irrigação realizada com a elevação da umidade do solo no ciclo seguinte."
)
add_path_paragraph(doc, "Event Log Padronizado (946 eventos)", "data/output/event_log.csv")
add_path_paragraph(doc, "Insights de Mineração em JSON", "data/output/process_mining_insights.json")
add_path_paragraph(doc, "Roteiro do Vídeo de Demonstração (5 a 8 min)", "docs/roteiro_video_demonstracao.md")

page_break(doc)

# ==========================================
# SEÇÃO 6: APRESENTAÇÃO DO PRODUTO (PITCH DE MERCADO)
# ==========================================
doc.add_heading("6. Apresentação do Produto (Pitch Comercial)", level=1)
doc.add_paragraph(
    "A AgroSmart foi estruturada como um produto comercial viável, com forte apelo de sustentabilidade, "
    "retorno sobre investimento (ROI) acelerado e conformidade com métricas ambientais (ESG)."
)

add_table(
    doc,
    ["Dimensão Comercial", "Definição Estratégica do Produto AgroSmart"],
    [
        ("Problema Resolvido", "Desperdício de até 40% da água de irrigação e perdas de R$ 25 bilhões por estiagem não detectada."),
        ("Solução Proposta", "Plataforma integrada com sensores IoT, motor de regras autônomo e auditoria de processos."),
        ("Proposta de Valor", "Redução de até 35% no consumo hídrico, proteção de safra e histórico auditável para exportação."),
        ("Público-Alvo", "Médios e grandes produtores de grãos e café, cooperativas agrícolas e fruticultura irrigada."),
        ("Mercado Endereçável", "TAM: R$ 12,5 Bilhões (Smart Agro global); SAM: R$ 2,8 B (Brasil irrigado); SOM: R$ 240 M (Polos SP/PR/GO/MT)."),
        ("Modelo de Negócios", "HaaS (Hardware de campo em comodato) + SaaS recorrente (R$ 49 a R$ 89/hectare/mês)."),
    ],
    [2.0, 4.8],
)

doc.add_heading("6.1 Artefatos de Apresentação e Vídeos da Entrega", level=2)
doc.add_paragraph(
    "A entrega conta com apresentação profissional de slides e os roteiros detalhados para os vídeos solicitados:"
)
add_path_paragraph(doc, "Pitch Deck em PowerPoint (.pptx)", "presentation/AgroSmart_Pitch_Deck.pptx")
add_path_paragraph(doc, "Apresentação Interativa em HTML", "presentation/pitch_slides.html")
add_path_paragraph(doc, "Roteiro do Vídeo Pitch (Até 5 min)", "docs/roteiro_video_pitch.md")
add_path_paragraph(doc, "Roteiro do Vídeo Demonstrativo (5 a 8 min)", "docs/roteiro_video_demonstracao.md")
add_path_paragraph(doc, "Links dos Vídeos Gravados", "link_video.txt")

page_break(doc)

# ==========================================
# SEÇÃO 7: CONCLUSÃO E STATUS DA ENTREGA
# ==========================================
doc.add_heading("7. Validação Final e Conclusão", level=1)
doc.add_paragraph(
    "A solução AgroSmart atende integralmente a todos os requisitos exigidos para a entrega da Fase 7, "
    "estabelecendo uma base sólida, moderna e auditada como produto consolidado de AgTech."
)

add_table(
    doc,
    ["Critério de Avaliação", "Status Final", "Evidência Associada"],
    [
        ("Funcionamento ponta a ponta", "Validado", "144 leituras, 104+ decisões e dashboard interativo"),
        ("Arquitetura consolidada", "Validado", "Diagramas em 5 camadas, componentes e fluxos documentados"),
        ("Automação e execução real", "Validado", "Motor de regras, acionamento hídrico e alertas em alerts.json"),
        ("Controle de qualidade e segurança", "Validado", "Pipeline DevSecOps aprovado (flake8 PEP8 + Bandit SAST)"),
        ("Análise de processos", "Validado", "Event log de 946 eventos, 5 variantes e gargalos identificados"),
        ("Proposta de valor do produto", "Validado", "Pitch deck em PPTX/HTML, modelo de negócios e roteiros de vídeo"),
    ],
    [2.3, 1.2, 3.3],
)

doc.add_paragraph(
    "Conclui-se que o AgroSmart representa não apenas um exercício acadêmico de engenharia, mas um protótipo "
    "de produto com alto potencial de tração no ecossistema de AgTech brasileiro, alinhando automação agronômica, "
    "segurança cibernética e sustentabilidade ambiental."
)

configured_footers = set()
for current_section in doc.sections:
    footer = current_section.footer
    footer_key = str(footer.part.partname)
    if footer_key in configured_footers:
        continue
    configured_footers.add(footer_key)
    paragraph = footer.paragraphs[0]
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = paragraph.add_run("AgroSmart  ·  Fase 7  ·  Relatório Consolidado Oficial")
    run.font.size = Pt(8)
    run.font.color.rgb = RGBColor(100, 115, 107)

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
doc.save(OUTPUT)
print(f"[Relatório] Documento Word gerado com sucesso: {OUTPUT}")
