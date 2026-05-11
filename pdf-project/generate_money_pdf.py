#!/usr/bin/env python3
"""
MONEY.pdf - Complete Pricing Guide for All 263 Templates
Generates a dedicated PDF focused on pricing, price points, and revenue potential.
"""
import csv
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, white, black, Color
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, KeepTogether
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ─── Colors ───────────────────────────────────────────
NAVY = HexColor("#1B2A4A")
GOLD = HexColor("#C9A84C")
DARK_GOLD = HexColor("#A8882E")
LIGHT_GOLD = HexColor("#F5E6B0")
WHITE_SMOKE = HexColor("#F5F5F5")
MID_GRAY = HexColor("#666666")
LIGHT_GRAY = HexColor("#E8E8E8")
GREEN = HexColor("#2E7D32")
RED = HexColor("#C62828")
ORANGE = HexColor("#E65100")

# Tier colors
TIER_COLORS = {
    'S': HexColor("#1B2A4A"),
    'A': HexColor("#2E7D32"),
    'B': HexColor("#1565C0"),
    'C': HexColor("#E65100"),
    'D': HexColor("#6A1B9A"),
}

DATA_PATH = os.path.join(os.path.dirname(__file__), "template_data.csv")
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "Money.pdf")
CHARTS_DIR = os.path.join(os.path.dirname(__file__), "charts")

# ─── Load Data ─────────────────────────────────────────
def load_data():
    rows = []
    with open(DATA_PATH) as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['PriceMin'] = int(row['PriceMin'])
            row['PriceMax'] = int(row['PriceMax'])
            row['CompositeScore'] = float(row['CompositeScore'])
            rows.append(row)
    return rows

# ─── Styles ──────────────────────────────────────────
styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    'MoneyTitle', parent=styles['Title'],
    fontSize=44, leading=52, textColor=GOLD,
    fontName='Helvetica-Bold', alignment=TA_CENTER,
    spaceAfter=6
)
subtitle_style = ParagraphStyle(
    'MoneySubtitle', parent=styles['Normal'],
    fontSize=16, leading=22, textColor=white,
    fontName='Helvetica', alignment=TA_CENTER,
    spaceAfter=4
)
section_style = ParagraphStyle(
    'Section', parent=styles['Heading1'],
    fontSize=24, leading=30, textColor=NAVY,
    fontName='Helvetica-Bold', spaceAfter=12, spaceBefore=20
)
body_style = ParagraphStyle(
    'Body', parent=styles['Normal'],
    fontSize=10, leading=14, textColor=HexColor("#333333"),
    fontName='Helvetica', spaceAfter=6
)
small_style = ParagraphStyle(
    'Small', parent=styles['Normal'],
    fontSize=7.5, leading=9.5, textColor=HexColor("#444444"),
    fontName='Helvetica'
)
header_cell = ParagraphStyle(
    'HeaderCell', parent=styles['Normal'],
    fontSize=8, leading=10, textColor=white,
    fontName='Helvetica-Bold', alignment=TA_CENTER
)
data_cell = ParagraphStyle(
    'DataCell', parent=styles['Normal'],
    fontSize=7.5, leading=9, textColor=HexColor("#333333"),
    fontName='Helvetica', alignment=TA_CENTER
)
data_cell_left = ParagraphStyle(
    'DataCellLeft', parent=data_cell, alignment=TA_LEFT
)

# ─── Build Story ──────────────────────────────────────
def build_cover(story):
    """Cover page with gold-on-navy design"""
    cover_data = [[
        Paragraph("MONEY", title_style),
    ]]
    cover_table = Table(cover_data, colWidths=[170*mm])
    cover_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 60),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(Spacer(1, 30*mm))
    story.append(cover_table)
    
    story.append(Paragraph(
        "Complete Pricing Guide",
        ParagraphStyle('sub1', parent=subtitle_style, fontSize=28, leading=34, textColor=GOLD)
    ))
    story.append(Spacer(1, 8*mm))
    story.append(Paragraph(
        "263 Web Templates | Priced & Ranked",
        ParagraphStyle('sub2', parent=subtitle_style, fontSize=14, leading=18, textColor=LIGHT_GOLD)
    ))
    story.append(Spacer(1, 20*mm))
    
    # Price point highlight boxes
    tiers_data = [
        ["S-TIER", "A-TIER", "B-TIER", "C-TIER", "D-TIER"],
        ["$4,000-$10,000", "$2,000-$5,000", "$500-$2,000", "$100-$500", "$0-$100"],
        ["PREMIUM", "HIGH", "MID", "BASIC", "FREE"]
    ]
    tier_table = Table(tiers_data, colWidths=[32*mm]*5)
    tier_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), GOLD),
        ('TEXTCOLOR', (0,0), (-1,0), NAVY),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 12),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('BACKGROUND', (0,1), (-1,1), NAVY),
        ('TEXTCOLOR', (0,1), (-1,1), GOLD),
        ('FONTNAME', (0,1), (-1,1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,1), (-1,1), 10),
        ('BACKGROUND', (0,2), (-1,2), HexColor("#F0F0F0")),
        ('TEXTCOLOR', (0,2), (-1,2), NAVY),
        ('GRID', (0,0), (-1,-1), 0.5, GOLD),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(tier_table)
    
    story.append(Spacer(1, 15*mm))
    story.append(Paragraph(
        "Every template priced. Every opportunity mapped.",
        ParagraphStyle('tagline', parent=subtitle_style, fontSize=12, leading=16, textColor=GOLD, alignment=TA_CENTER)
    ))
    story.append(PageBreak())

def build_exec_summary(story, rows):
    """Executive summary with key pricing stats"""
    story.append(Paragraph("Executive Summary", section_style))
    story.append(Spacer(1, 3*mm))
    
    # Key metrics boxes
    total_val = sum(r['PriceMax'] for r in rows)
    s_count = sum(1 for r in rows if r['Tier'] == 'S')
    a_count = sum(1 for r in rows if r['Tier'] == 'A')
    b_count = sum(1 for r in rows if r['Tier'] == 'B')
    c_count = sum(1 for r in rows if r['Tier'] == 'C')
    d_count = sum(1 for r in rows if r['Tier'] == 'D')
    
    metrics = [
        ["Total Templates", "Total Portfolio Value", "Avg Price/Template", "Premium (S+A)"],
        [f"{len(rows)}", f"${total_val:,}", f"${total_val//len(rows):,}", f"{s_count + a_count}"],
        ["S-Tier Premium", "A-Tier High", "B-Tier Mid", "C-Tier Basic"],
        [f"{s_count}", f"{a_count}", f"{b_count}", f"{c_count + d_count}"]
    ]
    m_table = Table(metrics, colWidths=[40*mm]*4)
    m_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), GOLD),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 9),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('BACKGROUND', (0,1), (-1,1), HexColor("#F8F4E8")),
        ('FONTNAME', (0,1), (-1,1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,1), (-1,1), 14),
        ('BACKGROUND', (0,2), (-1,2), GOLD),
        ('TEXTCOLOR', (0,2), (-1,2), NAVY),
        ('FONTNAME', (0,2), (-1,2), 'Helvetica-Bold'),
        ('FONTSIZE', (0,2), (-1,2), 9),
        ('BACKGROUND', (0,3), (-1,3), HexColor("#F0F0F0")),
        ('FONTSIZE', (0,3), (-1,3), 12),
        ('GRID', (0,0), (-1,-1), 0.5, NAVY),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(m_table)
    story.append(Spacer(1, 5*mm))
    
    # Pricing breakdown text
    story.append(Paragraph(
        "<b>Pricing Overview:</b> Templates are graded S through D. "
        "S-Tier represents premium, fully-featured commercial projects ($4,000–$10,000). "
        "A-Tier is high-quality production-ready templates ($2,000–$5,000). "
        "B-Tier offers solid mid-range options ($500–$2,000). "
        "C-Tier covers basic templates ($100–$500) and D-Tier is free or near-free ($0–$100).",
        body_style
    ))
    story.append(PageBreak())

def build_tier_pricing_chart(story, rows):
    """Create a text-based tier pricing table"""
    story.append(Paragraph("Tier Pricing Breakdown", section_style))
    
    tiers = {}
    for r in rows:
        t = r['Tier']
        if t not in tiers:
            tiers[t] = {'count': 0, 'min_sum': 0, 'max_sum': 0, 'items': []}
        tiers[t]['count'] += 1
        tiers[t]['min_sum'] += r['PriceMin']
        tiers[t]['max_sum'] += r['PriceMax']
        tiers[t]['items'].append(r)
    
    header = [
        Paragraph("Tier", header_cell),
        Paragraph("Count", header_cell),
        Paragraph("Price Range", header_cell),
        Paragraph("Avg Price", header_cell),
        Paragraph("Portfolio Value", header_cell),
        Paragraph("Revenue Share", header_cell),
    ]
    rows_data = [header]
    
    grand_min = sum(r['PriceMin'] for r in rows)
    grand_max = sum(r['PriceMax'] for r in rows)
    
    for t in ['S', 'A', 'B', 'C', 'D']:
        if t not in tiers:
            continue
        info = tiers[t]
        avg_min = info['min_sum'] // info['count']
        avg_max = info['max_sum'] // info['count']
        share = (info['max_sum'] / grand_max * 100) if grand_max > 0 else 0
        
        if t == 'S':
            range_str = f"$4,000 - $10,000"
        elif t == 'A':
            range_str = f"$2,000 - $5,000"
        elif t == 'B':
            range_str = f"$500 - $2,000"
        elif t == 'C':
            range_str = f"$100 - $500"
        else:
            range_str = f"$0 - $100"
        
        rows_data.append([
            Paragraph(f"<b>{t}-TIER</b>", ParagraphStyle('tc', parent=data_cell, 
                       textColor=TIER_COLORS[t], fontName='Helvetica-Bold', fontSize=9)),
            Paragraph(str(info['count']), data_cell),
            Paragraph(range_str, data_cell),
            Paragraph(f"${avg_min:,} - ${avg_max:,}", data_cell),
            Paragraph(f"${info['min_sum']:,} - ${info['max_sum']:,}", data_cell),
            Paragraph(f"{share:.1f}%", data_cell),
        ])
    
    # Total row
    rows_data.append([
        Paragraph("<b>TOTAL</b>", ParagraphStyle('tt', parent=data_cell, fontName='Helvetica-Bold', fontSize=9)),
        Paragraph(str(len(rows)), ParagraphStyle('ttc', parent=data_cell, fontName='Helvetica-Bold')),
        Paragraph("$0 - $10,000", ParagraphStyle('ttr', parent=data_cell, fontName='Helvetica-Bold')),
        Paragraph(f"${grand_max//len(rows):,}", ParagraphStyle('tta', parent=data_cell, fontName='Helvetica-Bold')),
        Paragraph(f"${grand_min:,} - ${grand_max:,}", ParagraphStyle('ttp', parent=data_cell, fontName='Helvetica-Bold')),
        Paragraph("100%", ParagraphStyle('ttp2', parent=data_cell, fontName='Helvetica-Bold')),
    ])
    
    t = Table(rows_data, colWidths=[22*mm, 18*mm, 32*mm, 28*mm, 34*mm, 26*mm])
    style_cmds = [
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), white),
        ('GRID', (0,0), (-1,-1), 0.5, NAVY),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('FONTSIZE', (0,0), (-1,-1), 8.5),
    ]
    # Color tier rows
    for i, tier_code in enumerate(['S', 'A', 'B', 'C', 'D']):
        if tier_code in tiers:
            bg = HexColor("#F8F4E8") if i % 2 == 0 else white
            style_cmds.append(('BACKGROUND', (0, i+1), (-1, i+1), bg))
    
    # Total row background
    style_cmds.append(('BACKGROUND', (0, len(rows_data)-1), (-1, len(rows_data)-1), LIGHT_GOLD))
    
    t.setStyle(TableStyle(style_cmds))
    story.append(t)
    
    # Include chart image if available
    chart_path = os.path.join(CHARTS_DIR, "pie_tier_distribution.png")
    if os.path.exists(chart_path):
        story.append(Spacer(1, 5*mm))
        story.append(Paragraph("Tier Distribution", ParagraphStyle('chart_label', parent=body_style, alignment=TA_CENTER, fontSize=11, textColor=NAVY)))
        story.append(Image(chart_path, width=140*mm, height=100*mm))
    
    story.append(Spacer(1, 5*mm))
    story.append(Paragraph(
        "<b>Key Insight:</b> The S and A tiers (just 13 templates) represent <b>$31,000 - $73,000</b> "
        "of the total portfolio value — the top 5% of templates account for the majority of revenue potential. "
        "B-Tier (44 templates) offers the best value-for-money sweet spot.",
        body_style
    ))
    story.append(PageBreak())

def build_price_chart(story, rows):
    """Revenue bar chart and price distribution"""
    story.append(Paragraph("Revenue Analysis", section_style))
    
    rev_chart = os.path.join(CHARTS_DIR, "bar_revenue_by_tier.png")
    if os.path.exists(rev_chart):
        story.append(Image(rev_chart, width=170*mm, height=90*mm))
        story.append(Spacer(1, 3*mm))
    
    # Price points summary table
    story.append(Paragraph("Price Point Summary", ParagraphStyle('subsec', parent=section_style, fontSize=16, leading=20)))
    
    # Top 10 most valuable templates
    sorted_rows = sorted(rows, key=lambda r: -r['PriceMax'])
    header2 = [
        Paragraph("Rank", header_cell),
        Paragraph("Template", ParagraphStyle('hc2', parent=header_cell, alignment=TA_LEFT)),
        Paragraph("Tier", header_cell),
        Paragraph("Price Range", header_cell),
        Paragraph("Value", header_cell),
    ]
    top_data = [header2]
    
    for i, r in enumerate(sorted_rows[:15]):
        tier_color = TIER_COLORS.get(r['Tier'], MID_GRAY)
        top_data.append([
            Paragraph(f"#{i+1}", data_cell),
            Paragraph(r['Template'], ParagraphStyle('tn', parent=data_cell_left, fontSize=7.5)),
            Paragraph(f"<b>{r['Tier']}</b>", ParagraphStyle('tc2', parent=data_cell, textColor=tier_color, fontSize=8)),
            Paragraph(f"${r['PriceMin']:,} - ${r['PriceMax']:,}", data_cell),
            Paragraph(f"${r['PriceMax']:,}", ParagraphStyle('tv', parent=data_cell, fontName='Helvetica-Bold')),
        ])
    
    t2 = Table(top_data, colWidths=[14*mm, 68*mm, 14*mm, 34*mm, 20*mm])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), white),
        ('GRID', (0,0), (-1,-1), 0.4, NAVY),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, HexColor("#F8F8F8")]),
    ]))
    story.append(t2)
    story.append(PageBreak())

def build_all_prices(story, rows):
    """Complete listing of ALL templates with prices"""
    story.append(Paragraph("Complete Price Directory", section_style))
    story.append(Paragraph(
        f"All {len(rows)} templates with full pricing — sorted by tier then alphabetically.",
        body_style
    ))
    story.append(Spacer(1, 3*mm))
    
    # Sort by tier (S first) then name
    tier_order = {'S': 0, 'A': 1, 'B': 2, 'C': 3, 'D': 4}
    sorted_all = sorted(rows, key=lambda r: (tier_order.get(r['Tier'], 9), r['Template']))
    
    # Group by tier
    current_tier = None
    items_in_page = 0
    
    for r in sorted_all:
        if r['Tier'] != current_tier:
            current_tier = r['Tier']
            tier_color = TIER_COLORS.get(current_tier, MID_GRAY)
            story.append(Spacer(1, 4*mm))
            story.append(Paragraph(
                f"<b>{current_tier}-TIER</b>  —  ${r['PriceMin']:,} - ${r['PriceMax']:,} range",
                ParagraphStyle('tier_hdr', parent=body_style, fontSize=12, leading=16,
                             textColor=tier_color, fontName='Helvetica-Bold', spaceBefore=6, spaceAfter=3)
            ))
            items_in_page = 0
        
        price_range = f"${r['PriceMin']:,} - ${r['PriceMax']:,}"
        story.append(Paragraph(
            f"<b>{r['Template']}</b>  —  {price_range}  |  {r['Category']}  |  Score: {r['CompositeScore']}",
            ParagraphStyle('item', parent=body_style, fontSize=8, leading=10, spaceAfter=2, spaceBefore=1)
        ))
        items_in_page += 1
        
        # Page break every ~60 items
        if items_in_page >= 60:
            story.append(PageBreak())
            items_in_page = 0

def build_methodology(story):
    """Quick pricing methodology"""
    story.append(Paragraph("Pricing Methodology", section_style))
    story.append(Paragraph(
        "<b>How prices are determined:</b> Each template is evaluated on Visual Quality, "
        "Functional Completeness, and Market Value. These scores combine into a Composite Score "
        "that determines the tier placement.",
        body_style
    ))
    story.append(Spacer(1, 3*mm))
    
    pricing = [
        ["Factor", "Weight", "What it measures"],
        ["Visual Score", "35%", "Design quality, UI/UX, visual appeal"],
        ["Functional Score", "35%", "Features, code quality, responsiveness"],
        ["Value Score", "30%", "Market positioning, uniqueness, scalability"],
    ]
    pt = Table(pricing, colWidths=[45*mm, 30*mm, 85*mm])
    pt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), GOLD),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 10),
        ('GRID', (0,0), (-1,-1), 0.5, NAVY),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, HexColor("#F8F4E8")]),
    ]))
    story.append(pt)
    story.append(Spacer(1, 5*mm))
    
    tiet_pt = [
        ["Tier", "Score Range", "Price Range"],
        ["S", "90-100", "$4,000 - $10,000"],
        ["A", "75-89", "$2,000 - $5,000"],
        ["B", "55-74", "$500 - $2,000"],
        ["C", "30-54", "$100 - $500"],
        ["D", "0-29", "$0 - $100"],
    ]
    t2 = Table(tiet_pt, colWidths=[35*mm, 35*mm, 40*mm])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), GOLD),
        ('TEXTCOLOR', (0,0), (-1,0), NAVY),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, NAVY),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    # Color tier rows
    for i, t in enumerate(['S', 'A', 'B', 'C', 'D']):
        t2.setStyle(TableStyle([
            ('BACKGROUND', (0, i+1), (-1, i+1), HexColor("#F8F4E8") if i % 2 == 0 else white),
            ('TEXTCOLOR', (0, i+1), (-1, i+1), TIER_COLORS.get(t, MID_GRAY)),
            ('FONTNAME', (0, i+1), (0, i+1), 'Helvetica-Bold'),
        ]))
    story.append(t2)
    story.append(Spacer(1, 5*mm))
    
    story.append(Paragraph(
        "<b>Profit Potential:</b> Buy a template at its listed price, customize it for a client, "
        "and charge 2-5x the template cost. S-Tier templates yield the highest absolute profit "
        "($5,000-$15,000 per project), while B-Tier offers the best ROI (300-500% margin).",
        body_style
    ))

def build_profit_calculator(story):
    """Simple profit potential calculator"""
    story.append(Paragraph("Profit Calculator", section_style))
    
    calc_data = [
        ["Tier", "Template Cost", "Client Price (3x)", "Client Price (5x)", "Profit (3x)", "Profit (5x)"],
        ["S", "$4,000-$10,000", "$12,000-$30,000", "$20,000-$50,000", "$8,000-$20,000", "$16,000-$40,000"],
        ["A", "$2,000-$5,000", "$6,000-$15,000", "$10,000-$25,000", "$4,000-$10,000", "$8,000-$20,000"],
        ["B", "$500-$2,000", "$1,500-$6,000", "$2,500-$10,000", "$1,000-$4,000", "$2,000-$8,000"],
        ["C", "$100-$500", "$300-$1,500", "$500-$2,500", "$200-$1,000", "$400-$2,000"],
        ["D", "$0-$100", "$0-$300", "$0-$500", "$0-$200", "$0-$400"],
    ]
    ct = Table(calc_data, colWidths=[22*mm]*6)
    ct.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), GOLD),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 8),
        ('GRID', (0,0), (-1,-1), 0.5, NAVY),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, HexColor("#F8F4E8")]),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-1), 8),
    ]))
    # Bold first column
    tier_labels = ['', 'S', 'A', 'B', 'C', 'D']
    for i in range(1, min(7, len(calc_data))):
        if i < len(tier_labels):
            ct.setStyle(TableStyle([
                ('FONTNAME', (0,i), (0,i), 'Helvetica-Bold'),
                ('TEXTCOLOR', (0,i), (0,i), TIER_COLORS.get(tier_labels[i], NAVY)),
            ]))
    story.append(ct)
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph(
        "<b>Example:</b> Buy an A-Tier template for $3,000 → customize for a client → charge $12,000 "
        "→ <b>$9,000 profit</b> per project. Do 10 projects a year = <b>$90,000 annual revenue</b>.",
        ParagraphStyle('example', parent=body_style, fontSize=10, leading=14, textColor=GREEN, fontName='Helvetica-Bold')
    ))
    story.append(PageBreak())

# ─── Main ─────────────────────────────────────────────
def main():
    rows = load_data()
    
    doc = SimpleDocTemplate(
        OUTPUT_PATH,
        pagesize=A4,
        leftMargin=18*mm, rightMargin=18*mm,
        topMargin=18*mm, bottomMargin=18*mm,
        title="MONEY - Complete Pricing Guide",
        author="Template Pricing Guide"
    )
    
    story = []
    
    # Build all sections
    build_cover(story)
    build_exec_summary(story, rows)
    build_tier_pricing_chart(story, rows)
    build_price_chart(story, rows)
    build_methodology(story)
    build_profit_calculator(story)
    build_all_prices(story, rows)
    
    doc.build(story)
    size_kb = os.path.getsize(OUTPUT_PATH) // 1024
    print(f"✅ Money.pdf generated: {OUTPUT_PATH} ({size_kb}KB)")

if __name__ == '__main__':
    main()
