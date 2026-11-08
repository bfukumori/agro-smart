"""Gerador automatizado da Apresentação de Produto (Pitch Deck) em PowerPoint (.pptx).

Cria uma apresentação profissional de 9 slides cobrindo:
1. Capa e Identidade
2. O Problema Agronômico
3. A Solução AgroSmart
4. Proposta de Valor
5. Mercado e Público-Alvo (TAM/SAM/SOM)
6. Diferenciais Competitivos
7. Modelo de Negócios (Business Model)
8. Validação e Tração da Fase 7
9. Encerramento e Equipe
"""

from __future__ import annotations

from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PPTX = ROOT / "presentation" / "AgroSmart_Pitch_Deck.pptx"

# Cores da Paleta AgroSmart
DARK_GREEN = RGBColor(20, 35, 28)     # #14231C
ACCENT_GREEN = RGBColor(23, 107, 69)  # #176B45
LIGHT_BG = RGBColor(241, 246, 242)    # #F1F6F2
WHITE = RGBColor(255, 255, 255)
TEXT_DARK = RGBColor(30, 41, 59)
TEXT_MUTED = RGBColor(100, 116, 139)
ACCENT_GOLD = RGBColor(217, 119, 6)   # #D97706


def apply_background(slide, prs, color):
    """Cria um retângulo de fundo cobrindo o slide inteiro."""
    bg = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height
    )
    bg.fill.solid()
    bg.fill.fore_color.rgb = color
    bg.line.fill.background()
    return bg


def add_header(slide, title_text, category="AGROSMART · PRODUTO & PITCH"):
    """Adiciona cabeçalho padronizado nos slides internos."""
    # Categoria
    tx_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(8.5), Inches(0.4))
    tf = tx_box.text_frame
    tf.word_wrap = True
    p0 = tf.paragraphs[0]
    p0.text = category.upper()
    p0.font.name = "Arial"
    p0.font.size = Pt(10)
    p0.font.bold = True
    p0.font.color.rgb = ACCENT_GREEN

    # Título principal
    p1 = tf.add_paragraph()
    p1.text = title_text
    p1.font.name = "Arial"
    p1.font.size = Pt(22)
    p1.font.bold = True
    p1.font.color.rgb = DARK_GREEN
    p1.space_before = Pt(4)


def create_deck() -> None:
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(5.625)  # 16:9 widescreen
    blank_layout = prs.slide_layouts[6]

    # ==========================================
    # SLIDE 1: CAPA
    # ==========================================
    slide1 = prs.slides.add_slide(blank_layout)
    apply_background(slide1, prs, DARK_GREEN)

    # Caixa de Título
    tb1 = slide1.shapes.add_textbox(Inches(1.0), Inches(1.2), Inches(8.0), Inches(3.2))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "FIAP · FASE 7 · PITCH DE PRODUTO"
    p.font.name = "Arial"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GOLD

    p = tf1.add_paragraph()
    p.text = "AgroSmart"
    p.font.name = "Arial"
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.space_before = Pt(10)

    p = tf1.add_paragraph()
    p.text = "A Inteligência Autônoma que Alimenta o Futuro do Campo"
    p.font.name = "Arial"
    p.font.size = Pt(18)
    p.font.color.rgb = RGBColor(167, 243, 208)
    p.space_before = Pt(8)

    p = tf1.add_paragraph()
    p.text = "Plataforma Integrada de IoT, Mineração de Processos e Decisão Agronômica em Tempo Real"
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.color.rgb = RGBColor(203, 213, 225)
    p.space_before = Pt(12)

    p = tf1.add_paragraph()
    p.text = "Bruno Fukumori · Victor Jaber · Bruno Araújo · Bruno Perdigão · Vinicius Messias"
    p.font.name = "Arial"
    p.font.size = Pt(10)
    p.font.color.rgb = RGBColor(148, 163, 184)
    p.space_before = Pt(20)

    # ==========================================
    # SLIDE 2: O PROBLEMA
    # ==========================================
    slide2 = prs.slides.add_slide(blank_layout)
    apply_background(slide2, prs, LIGHT_BG)
    add_header(slide2, "O Desafio do Agronegócio Moderno")

    # 3 Caixas de Dores
    cards_data = [
        ("Desperdício Hídrico Severo", "Até 40% da água de irrigação é perdida por decisões empíricas ou bombas ativadas antes de chuvas não previstas."),
        ("Perdas por Estresse Hídrico", "R$ 25 bilhões anuais em quebras de produtividade decorrentes de estiagens não detectadas em tempo hábil."),
        ("Deriva & Ineficiência Térmica", "Defensivos aplicados em temperaturas acima de 32°C sofrem evaporação precoce e dispersão inadequada.")
    ]

    for idx, (title, desc) in enumerate(cards_data):
        left = Inches(0.8 + idx * 2.9)
        card = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(1.6), Inches(2.7), Inches(3.2))
        card.fill.solid()
        card.fill.fore_color.rgb = WHITE
        card.line.color.rgb = RGBColor(203, 213, 225)
        card.line.width = Pt(1)

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_top = Inches(0.3)
        tf.margin_left = Inches(0.2)
        tf.margin_right = Inches(0.2)

        p = tf.paragraphs[0]
        p.text = f"0{idx+1}."
        p.font.name = "Arial"
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = ACCENT_GOLD

        p = tf.add_paragraph()
        p.text = title
        p.font.name = "Arial"
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = DARK_GREEN
        p.space_before = Pt(8)

        p = tf.add_paragraph()
        p.text = desc
        p.font.name = "Arial"
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(10)

    # ==========================================
    # SLIDE 3: A SOLUÇÃO AGROSMART
    # ==========================================
    slide3 = prs.slides.add_slide(blank_layout)
    apply_background(slide3, prs, WHITE)
    add_header(slide3, "A Solução AgroSmart: Autonomia Ponta a Ponta")

    steps = [
        ("1. Coleta na Borda (Edge IoT)", "ESP32 conectado a sensores de umidade do solo, temperatura, ar e luz medindo as condições reais do microclima."),
        ("2. Validação & Qualidade", "Pipeline em Python higieniza, valida limites físicos e elimina leituras ruidosas com 100% de conformidade."),
        ("3. Inteligência Agronômica", "Motor de regras cruza déficit hídrico com previsão meteorológica: aciona bombas ou suspende para colher a chuva."),
        ("4. Dashboard & Auditoria", "Operador visualiza telemetria, mapa de calor, indicadores em tempo real e rastreabilidade total via Process Mining.")
    ]

    for idx, (title, desc) in enumerate(steps):
        y = Inches(1.5 + idx * 0.95)
        box = slide3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), y, Inches(8.4), Inches(0.85))
        box.fill.solid()
        box.fill.fore_color.rgb = LIGHT_BG
        box.line.color.rgb = ACCENT_GREEN
        box.line.width = Pt(1)

        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.25)
        tf.margin_top = Inches(0.12)

        p = tf.paragraphs[0]
        p.text = title
        p.font.name = "Arial"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = ACCENT_GREEN

        p = tf.add_paragraph()
        p.text = desc
        p.font.name = "Arial"
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(2)

    # ==========================================
    # SLIDE 4: PROPOSTA DE VALOR
    # ==========================================
    slide4 = prs.slides.add_slide(blank_layout)
    apply_background(slide4, prs, LIGHT_BG)
    add_header(slide4, "Proposta de Valor: Retorno Real para o Produtor")

    pillars = [
        ("Economia de Água de até 35%", "Algoritmo preditivo de chuva suspende a irrigação artificial, preservando recursos hídricos e reduzindo custos operacionais."),
        ("Eficiência Energética Direcionada", "Acionamento de motobombas focado estritamente na necessidade do solo, evitando picos de consumo em horários de ponta."),
        ("Proteção da Safra em Tempo Real", "Alertas automáticos de estresse térmico orientam a suspensão de defensivos e reduzem o choque fisiológico das plantas."),
        ("Rastreabilidade & ESG Completo", "Histórico auditável em Event Log que comprova o uso racional de água para certificações internacionais de exportação.")
    ]

    for idx, (title, desc) in enumerate(pillars):
        row = idx // 2
        col = idx % 2
        left = Inches(0.8 + col * 4.3)
        top = Inches(1.6 + row * 1.7)

        card = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(4.1), Inches(1.5))
        card.fill.solid()
        card.fill.fore_color.rgb = WHITE
        card.line.color.rgb = RGBColor(226, 232, 240)
        card.line.width = Pt(1)

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.2)
        tf.margin_top = Inches(0.15)

        p = tf.paragraphs[0]
        p.text = title
        p.font.name = "Arial"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = ACCENT_GREEN

        p = tf.add_paragraph()
        p.text = desc
        p.font.name = "Arial"
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(4)

    # ==========================================
    # SLIDE 5: MERCADO E PÚBLICO-ALVO
    # ==========================================
    slide5 = prs.slides.add_slide(blank_layout)
    apply_background(slide5, prs, WHITE)
    add_header(slide5, "Público-Alvo e Dimensionamento de Mercado")

    # Métricas TAM SAM SOM
    market_data = [
        ("TAM · R$ 12,5 Bilhões", "Mercado global de Smart Agriculture e IoT no agronegócio."),
        ("SAM · R$ 2,8 Bilhões", "Propriedades agrícolas tecnificadas com pivôs e irrigação no Brasil."),
        ("SOM · R$ 240 Milhões", "Médios e grandes produtores e cooperativas nos polos SP, PR, GO e MT.")
    ]

    for idx, (m_title, m_desc) in enumerate(market_data):
        left = Inches(0.8 + idx * 2.9)
        box = slide5.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, Inches(1.6), Inches(2.7), Inches(1.3))
        box.fill.solid()
        box.fill.fore_color.rgb = DARK_GREEN
        box.line.fill.background()

        tf = box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = m_title
        p.font.name = "Arial"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = WHITE

        p = tf.add_paragraph()
        p.text = m_desc
        p.font.name = "Arial"
        p.font.size = Pt(9)
        p.font.color.rgb = RGBColor(203, 213, 225)
        p.space_before = Pt(4)

    # Perfil do cliente
    cust_box = slide5.shapes.add_textbox(Inches(0.8), Inches(3.2), Inches(8.4), Inches(1.8))
    tf_c = cust_box.text_frame
    tf_c.word_wrap = True

    p = tf_c.paragraphs[0]
    p.text = "Perfis Prioritários de Adoção:"
    p.font.name = "Arial"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GREEN

    p = tf_c.add_paragraph()
    p.text = "• Produtores de Grãos e Café: Buscam reduzir a conta de energia e água sem perder produtividade por saca."
    p.font.name = "Arial"
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_DARK
    p.space_before = Pt(4)

    p = tf_c.add_paragraph()
    p.text = "• Cooperativas Agrícolas: Exigem padronização de manejo e dashboards de conformidade para exportação."
    p.font.name = "Arial"
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_DARK
    p.space_before = Pt(2)

    p = tf_c.add_paragraph()
    p.text = "• Fruticultura Irrigada: Alta sensibilidade hídrica onde o déficit de poucas horas compromete a qualidade do fruto."
    p.font.name = "Arial"
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_DARK
    p.space_before = Pt(2)

    # ==========================================
    # SLIDE 6: DIFERENCIAIS COMPETITIVOS
    # ==========================================
    slide6 = prs.slides.add_slide(blank_layout)
    apply_background(slide6, prs, LIGHT_BG)
    add_header(slide6, "Diferencial Competitivo: Por que a AgroSmart Vence?")

    diffs = [
        ("Decisão Autônoma Fechada", "Não apenas monitoramos: acionamos solenóides e bombas com cálculo multivariável de risco."),
        ("Mineração de Processos (Process Mining)", "Pioneiros em mapear variantes operacionais e gargalos de latência no fluxo agrícola."),
        ("Operação Offline & Edge-Ready", "Funciona de forma autônoma mesmo com queda total do link de internet da propriedade."),
        ("DevSecOps & Engenharia de Classe Corporativa", "Código auditado por SAST, zero vulnerabilidades conhecidas, containers seguros non-root.")
    ]

    for idx, (title, desc) in enumerate(diffs):
        row = idx // 2
        col = idx % 2
        left = Inches(0.8 + col * 4.3)
        top = Inches(1.6 + row * 1.7)

        card = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(4.1), Inches(1.5))
        card.fill.solid()
        card.fill.fore_color.rgb = WHITE
        card.line.color.rgb = ACCENT_GOLD
        card.line.width = Pt(1.5)

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.2)
        tf.margin_top = Inches(0.15)

        p = tf.paragraphs[0]
        p.text = title
        p.font.name = "Arial"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = DARK_GREEN

        p = tf.add_paragraph()
        p.text = desc
        p.font.name = "Arial"
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(4)

    # ==========================================
    # SLIDE 7: MODELO DE NEGÓCIOS
    # ==========================================
    slide7 = prs.slides.add_slide(blank_layout)
    apply_background(slide7, prs, WHITE)
    add_header(slide7, "Modelo de Negócios e Monetização (SaaS + HaaS)")

    plans = [
        ("HaaS (Hardware em Comodato)", "Instalação dos kits de sensores ESP32 e atuadores sem custo inicial proibitivo para o produtor."),
        ("SaaS Recorrente (por Hectare)", "Assinatura mensal de R$ 49 a R$ 89/hectare/mês para acesso ao motor de regras e analytics em nuvem/local."),
        ("Módulos Corporativos & ESG", "Dashboards avançados de sustentabilidade para cooperativas, auditoria de processos e integração com ERPs (Totvs/SAP).")
    ]

    for idx, (p_title, p_desc) in enumerate(plans):
        left = Inches(0.8 + idx * 2.9)
        card = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(1.6), Inches(2.7), Inches(3.2))
        card.fill.solid()
        card.fill.fore_color.rgb = LIGHT_BG
        card.line.color.rgb = ACCENT_GREEN
        card.line.width = Pt(1)

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.2)
        tf.margin_top = Inches(0.3)

        p = tf.paragraphs[0]
        p.text = f"Pilar {idx+1}"
        p.font.name = "Arial"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = ACCENT_GREEN

        p = tf.add_paragraph()
        p.text = p_title
        p.font.name = "Arial"
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = DARK_GREEN
        p.space_before = Pt(8)

        p = tf.add_paragraph()
        p.text = p_desc
        p.font.name = "Arial"
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(10)

    # ==========================================
    # SLIDE 8: TRAÇÃO E VALIDAÇÃO FASE 7
    # ==========================================
    slide8 = prs.slides.add_slide(blank_layout)
    apply_background(slide8, prs, LIGHT_BG)
    add_header(slide8, "Validação Prática da Solução (Fase 7 Consolidada)")

    metrics_cards = [
        ("144", "Leituras Processadas", "Telemetria determinística cobrindo 48 horas em 3 talhões."),
        ("100%", "Conformidade de Qualidade", "Zero rejeições e validação rigorosa de limites físicos."),
        ("5", "Variantes de Processo", "Mapeamento em Process Mining com detecção de gargalos."),
        ("0", "Vulnerabilidades SAST", "Código 100% auditado pelo Bandit e conforme PEP 8 (flake8).")
    ]

    for idx, (val, title, sub) in enumerate(metrics_cards):
        left = Inches(0.8 + idx * 2.15)
        card = slide8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(1.6), Inches(2.0), Inches(2.4))
        card.fill.solid()
        card.fill.fore_color.rgb = WHITE
        card.line.color.rgb = RGBColor(203, 213, 225)
        card.line.width = Pt(1)

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.15)
        tf.margin_top = Inches(0.2)

        p = tf.paragraphs[0]
        p.text = val
        p.font.name = "Arial"
        p.font.size = Pt(28)
        p.font.bold = True
        p.font.color.rgb = ACCENT_GREEN

        p = tf.add_paragraph()
        p.text = title
        p.font.name = "Arial"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = DARK_GREEN
        p.space_before = Pt(4)

        p = tf.add_paragraph()
        p.text = sub
        p.font.name = "Arial"
        p.font.size = Pt(9)
        p.font.color.rgb = TEXT_MUTED
        p.space_before = Pt(6)

    # Rodapé status
    bot_box = slide8.shapes.add_textbox(Inches(0.8), Inches(4.3), Inches(8.4), Inches(0.8))
    tf_b = bot_box.text_frame
    p = tf_b.paragraphs[0]
    p.text = "Status Atual: Plataforma 100% funcional, container Docker operacional e testado, dashboard analítico ativo."
    p.font.name = "Arial"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GOLD

    # ==========================================
    # SLIDE 9: ENCERRAMENTO E EQUIPE
    # ==========================================
    slide9 = prs.slides.add_slide(blank_layout)
    apply_background(slide9, prs, DARK_GREEN)

    tb9 = slide9.shapes.add_textbox(Inches(1.0), Inches(1.3), Inches(8.0), Inches(3.2))
    tf9 = tb9.text_frame
    tf9.word_wrap = True

    p = tf9.paragraphs[0]
    p.text = "AGROSMART · FASE 7"
    p.font.name = "Arial"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GOLD

    p = tf9.add_paragraph()
    p.text = "Conectando a precisão da tecnologia à abundância da terra."
    p.font.name = "Arial"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.space_before = Pt(8)

    p = tf9.add_paragraph()
    p.text = "Equipe de Desenvolvimento:"
    p.font.name = "Arial"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = RGBColor(167, 243, 208)
    p.space_before = Pt(16)

    p = tf9.add_paragraph()
    p.text = "• Bruno Fukumori - RM 99486\n• Victor Jaber - RM 550173\n• Bruno Andrade Lima de Araújo - RM 550817\n• Bruno Perdigão Santos - RM 98681\n• Vinicius Messias dos Santos - RM 550463"
    p.font.name = "Arial"
    p.font.size = Pt(11)
    p.font.color.rgb = RGBColor(226, 232, 240)
    p.space_before = Pt(8)

    OUTPUT_PPTX.parent.mkdir(parents=True, exist_ok=True)
    prs.save(OUTPUT_PPTX)
    print(f"[Apresentação] Pitch Deck em PowerPoint gerado com sucesso: {OUTPUT_PPTX}")


if __name__ == "__main__":
    create_deck()
