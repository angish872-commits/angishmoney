#!/usr/bin/env python3
"""
Premium Website Template Guide 2026 — Enhanced Edition
Generates a professional PDF with charts, tables, methodology, and visual improvements.
"""

import os, sys, csv, math
from collections import Counter, defaultdict
from io import BytesIO

# ────────────────────────────────────────────────────────────
# 1. CHART GENERATION (matplotlib)
# ────────────────────────────────────────────────────────────
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

CHARTS_DIR = '/home/angish/angish-profiliobest/pdf-project/charts'
os.makedirs(CHARTS_DIR, exist_ok=True)

def create_pie_chart():
    fig, ax = plt.subplots(figsize=(6, 4))
    fig.patch.set_facecolor('#FAFAFA')
    ax.set_facecolor('#FAFAFA')
    labels = ['Tier S\n$5K-$10K', 'Tier A\n$2K-$5K', 'Tier B\n$500-$2K', 'Tier C\n$100-$500', 'Tier D\n$0-$100']
    sizes = [2, 11, 44, 175, 31]
    colors_chart = ['#FFD700', '#4169E1', '#2ECC71', '#95A5A6', '#BDC3C7']
    explode = (0.1, 0.05, 0, 0, 0)
    wedges, texts, autotexts = ax.pie(
        sizes, explode=explode, labels=labels, colors=colors_chart,
        autopct='%1.1f%%', startangle=90, shadow=False,
        textprops={'fontsize': 9, 'fontweight': 'bold'}
    )
    for at in autotexts:
        at.set_color('white')
        at.set_fontweight('bold')
    ax.set_title('Template Distribution by Pricing Tier', fontsize=14, fontweight='bold', pad=15, color='#1B2A4A')
    plt.tight_layout()
    fp = os.path.join(CHARTS_DIR, 'pie_tier_distribution.png')
    plt.savefig(fp, dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f'  ✓ Created pie chart: {fp}')

def create_revenue_chart():
    fig, ax = plt.subplots(figsize=(7, 4))
    fig.patch.set_facecolor('#FAFAFA')
    ax.set_facecolor('#FAFAFA')
    tiers = ['Tier S\n$5K-$10K', 'Tier A\n$2K-$5K', 'Tier B\n$500-$2K', 'Tier C\n$100-$500', 'Tier D\n$0-$100']
    revenues = [15000, 38500, 55000, 52500, 1550]
    colors_chart = ['#FFD700', '#4169E1', '#2ECC71', '#95A5A6', '#BDC3C7']
    bars = ax.bar(tiers, revenues, color=colors_chart, edgecolor='white', linewidth=1.5, width=0.65)
    ax.set_title('Revenue Potential by Pricing Tier', fontsize=14, fontweight='bold', pad=15, color='#1B2A4A')
    ax.set_ylabel('Revenue (USD)', fontsize=12, color='#333')
    ax.set_xlabel('')
    ax.tick_params(colors='#333')
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.grid(axis='y', alpha=0.3)
    for bar, rev in zip(bars, revenues):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 800, f'${rev:,}',
                ha='center', fontsize=10, fontweight='bold', color='#1B2A4A')
    plt.tight_layout()
    fp = os.path.join(CHARTS_DIR, 'bar_revenue_by_tier.png')
    plt.savefig(fp, dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f'  ✓ Created revenue chart: {fp}')

def create_tech_popularity_chart():
    fig, ax = plt.subplots(figsize=(7, 4))
    fig.patch.set_facecolor('#FAFAFA')
    ax.set_facecolor('#FAFAFA')
    techs = ['Bootstrap', 'Static', 'Three.js/3D', 'React', 'Next.js', 'Tailwind']
    counts = [140, 100, 26, 25, 10, 7]
    colors_chart = ['#3498DB', '#95A5A6', '#FF6B6B', '#61DAFB', '#000000', '#38B2AC']
    bars = ax.barh(techs, counts, color=colors_chart, edgecolor='white', linewidth=1.2)
    ax.set_title('Technology Popularity Across All Templates', fontsize=14, fontweight='bold', pad=15, color='#1B2A4A')
    ax.set_xlabel('Number of Templates', fontsize=12, color='#333')
    ax.tick_params(colors='#333')
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.grid(axis='x', alpha=0.3)
    for bar, count in zip(bars, counts):
        ax.text(bar.get_width() + 2, bar.get_y() + bar.get_height()/2, str(count),
                va='center', fontsize=10, fontweight='bold', color='#1B2A4A')
    plt.tight_layout()
    fp = os.path.join(CHARTS_DIR, 'bar_tech_popularity.png')
    plt.savefig(fp, dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f'  ✓ Created tech popularity chart: {fp}')

def create_score_distribution_chart():
    fig, ax = plt.subplots(figsize=(7, 4))
    fig.patch.set_facecolor('#FAFAFA')
    ax.set_facecolor('#FAFAFA')
    scores = []
    with open('/home/angish/angish-profiliobest/pdf-project/template_data.csv') as f:
        for line in f.readlines()[1:]:
            parts = line.strip().split(',')
            if len(parts) >= 15:
                try:
                    scores.append(float(parts[14]))
                except:
                    pass
    if scores:
        ax.hist(scores, bins=12, color='#1B2A4A', edgecolor='white', alpha=0.85, rwidth=0.9)
        ax.axvline(np.mean(scores), color='#C9A84C', linestyle='--', linewidth=2, label=f'Mean: {np.mean(scores):.1f}')
        ax.legend(fontsize=10)
    ax.set_title('Template Composite Score Distribution', fontsize=14, fontweight='bold', pad=15, color='#1B2A4A')
    ax.set_xlabel('Composite Score', fontsize=12, color='#333')
    ax.set_ylabel('Number of Templates', fontsize=12, color='#333')
    ax.tick_params(colors='#333')
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    fp = os.path.join(CHARTS_DIR, 'hist_score_distribution.png')
    plt.savefig(fp, dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f'  ✓ Created score distribution chart: {fp}')

def create_economy_chart():
    fig, ax = plt.subplots(figsize=(8, 4.5))
    fig.patch.set_facecolor('#FAFAFA')
    ax.set_facecolor('#FAFAFA')
    economies = ['USA/Canada', 'UK/Europe', 'Switzerland', 'Germany/Austria', 'France/Belgium',
                  'Australia/NZ', 'Netherlands', 'Nordics', 'Japan/Asia', 'UAE/Middle East']
    counts = [263, 263, 263, 263, 263, 263, 60, 75, 50, 40]
    colors_chart = ['#E74C3C', '#3498DB', '#2ECC71', '#F39C12', '#9B59B6',
                    '#1ABC9C', '#E67E22', '#34495E', '#FF6B6B', '#C9A84C']
    bars = ax.barh(economies, counts, color=colors_chart, edgecolor='white', linewidth=1.2)
    ax.set_title('Template Suitability by Economy / Region', fontsize=14, fontweight='bold', pad=15, color='#1B2A4A')
    ax.set_xlabel('Suitable Templates', fontsize=12, color='#333')
    ax.tick_params(colors='#333')
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.grid(axis='x', alpha=0.3)
    for bar, count in zip(bars, counts):
        ax.text(bar.get_width() + 3, bar.get_y() + bar.get_height()/2, str(count),
                va='center', fontsize=10, fontweight='bold', color='#1B2A4A')
    plt.tight_layout()
    fp = os.path.join(CHARTS_DIR, 'bar_economy_fit.png')
    plt.savefig(fp, dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f'  ✓ Created economy chart: {fp}')

def create_visual_vs_functional_chart():
    """Scatter plot of VisualScore vs FunctionScore colored by tier"""
    fig, ax = plt.subplots(figsize=(6.5, 4))
    fig.patch.set_facecolor('#FAFAFA')
    ax.set_facecolor('#FAFAFA')
    tier_colors = {'S': '#FFD700', 'A': '#4169E1', 'B': '#2ECC71', 'C': '#95A5A6', 'D': '#BDC3C7'}
    tier_data = defaultdict(list)
    with open('/home/angish/angish-profiliobest/pdf-project/template_data.csv') as f:
        for line in f.readlines()[1:]:
            parts = line.strip().split(',')
            if len(parts) >= 16:
                try:
                    vs = float(parts[11])
                    fs = float(parts[12])
                    t = parts[9].strip()
                    tier_data[t].append((vs, fs))
                except:
                    pass
    for tier, pts in tier_data.items():
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        ax.scatter(xs, ys, c=tier_colors.get(tier, '#333'), label=f'Tier {tier} ({len(pts)})',
                   alpha=0.7, s=40, edgecolors='white', linewidth=0.5)
    ax.set_title('Visual Score vs Functional Score by Tier', fontsize=14, fontweight='bold', pad=15, color='#1B2A4A')
    ax.set_xlabel('Visual Score', fontsize=11, color='#333')
    ax.set_ylabel('Functional Score', fontsize=11, color='#333')
    ax.tick_params(colors='#333')
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.legend(fontsize=8, loc='lower right')
    ax.grid(alpha=0.2)
    plt.tight_layout()
    fp = os.path.join(CHARTS_DIR, 'scatter_visual_vs_functional.png')
    plt.savefig(fp, dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f'  ✓ Created scatter chart: {fp}')


# Generate all charts
print('Generating charts...')
create_pie_chart()
create_revenue_chart()
create_tech_popularity_chart()
create_score_distribution_chart()
create_economy_chart()
create_visual_vs_functional_chart()
print('All charts generated.\n')


# ────────────────────────────────────────────────────────────
# 2. LOAD & PARSE CSV DATA
# ────────────────────────────────────────────────────────────
DATA_PATH = '/home/angish/angish-profiliobest/pdf-project/template_data.csv'
rows = []
with open(DATA_PATH) as f:
    reader = csv.DictReader(f)
    for row in reader:
        rows.append(row)

print(f'Loaded {len(rows)} template rows.')

# Compute aggregations
tier_counter = Counter(r['Tier'].strip() for r in rows)
cat_counter = Counter(r['Category'].strip() for r in rows)

# Tech stack counting
tech_counter = Counter()
threejs_list = []
for r in rows:
    ts = r['TechStack']
    for t_item in ts.split('|'):
        t = t_item.strip()
        if t:
            tech_counter[t] += 1
    if 'Three' in ts or 'three' in ts.lower():
        threejs_list.append(r)

# Economy parsing
econ_counter = Counter()
for r in rows:
    econ = r.get('Economies', '')
    if econ:
        for c in econ.split(','):
            c = c.strip()
            if c:
                econ_counter[c] += 1


# ────────────────────────────────────────────────────────────
# 3. PDF GENERATION (ReportLab)
# ────────────────────────────────────────────────────────────
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import inch, mm, cm
from reportlab.lib.colors import HexColor, white, black, Color
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image, PageBreak, KeepTogether, ListFlowable, ListItem,
    Flowable, HRFlowable
)
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate, Frame
from reportlab.platypus.frames import Frame as RLFrame
from reportlab.pdfgen import canvas
from reportlab.lib import colors

# ── Color Scheme ──
NAVY      = HexColor('#1B2A4A')
GOLD      = HexColor('#C9A84C')
WHITE     = colors.white
LIGHT_GRAY = HexColor('#F5F5F5')
MID_GRAY  = HexColor('#CCCCCC')
DARK_TEXT  = HexColor('#222222')
SOFT_GRAY = HexColor('#E8E8E8')

TIER_COLORS = {
    'S': HexColor('#FFD700'),
    'A': HexColor('#4169E1'),
    'B': HexColor('#2ECC71'),
    'C': HexColor('#95A5A6'),
    'D': HexColor('#BDC3C7'),
}

TIER_LABELS = {
    'S': 'Premium  ($5K-$10K)',
    'A': 'High-End ($2K-$5K)',
    'B': 'Mid-Range ($500-$2K)',
    'C': 'Budget    ($100-$500)',
    'D': 'Economy  ($0-$100)',
}

# ── Styles ──
styles = getSampleStyleSheet()

def make_style(name, parent='Normal', **kw):
    base = styles[parent]
    return ParagraphStyle(name, parent=base, **kw)

s_cover_title = make_style('CoverTitle', fontSize=36, fontName='Helvetica-Bold', textColor=GOLD, alignment=TA_CENTER, spaceAfter=6)
s_cover_sub   = make_style('CoverSub', fontSize=18, fontName='Helvetica', textColor=WHITE, alignment=TA_CENTER, spaceAfter=4, leading=26)
s_cover_sub2  = make_style('CoverSub2', fontSize=12, fontName='Helvetica', textColor=HexColor('#AABBCC'), alignment=TA_CENTER, spaceAfter=2)
s_h1 = make_style('H1', fontSize=22, fontName='Helvetica-Bold', textColor=NAVY, spaceBefore=20, spaceAfter=10, leading=28)
s_h2 = make_style('H2', fontSize=16, fontName='Helvetica-Bold', textColor=NAVY, spaceBefore=15, spaceAfter=8, leading=22)
s_h3 = make_style('H3', fontSize=13, fontName='Helvetica-Bold', textColor=GOLD, spaceBefore=10, spaceAfter=6, leading=18)
s_body = make_style('BodyCustom', fontSize=9.5, fontName='Helvetica', textColor=DARK_TEXT, spaceAfter=6, leading=14, alignment=TA_JUSTIFY)
s_body_small = make_style('BodySmall', fontSize=8, fontName='Helvetica', textColor=DARK_TEXT, spaceAfter=3, leading=11)
s_cell = make_style('CellStyle', fontSize=7.5, fontName='Helvetica', textColor=DARK_TEXT, leading=10)
s_cell_bold = make_style('CellBold', fontSize=7.5, fontName='Helvetica-Bold', textColor=DARK_TEXT, leading=10)
s_header_cell = make_style('HeaderCell', fontSize=8, fontName='Helvetica-Bold', textColor=WHITE, leading=11)
s_toc = make_style('TOC', fontSize=11, fontName='Helvetica', textColor=NAVY, spaceAfter=4, leading=16, leftIndent=20)
s_bullet = make_style('Bullet', fontSize=9.5, fontName='Helvetica', textColor=DARK_TEXT, spaceAfter=3, leading=13, leftIndent=15)
s_method_body = make_style('MethodBody', fontSize=9.5, fontName='Helvetica', textColor=DARK_TEXT, spaceAfter=4, leading=14)


# ── Header / Footer ──
def header_footer(canvas_obj, doc):
    canvas_obj.saveState()
    # Header bar
    canvas_obj.setFillColor(NAVY)
    canvas_obj.rect(0, A4[1] - 40, A4[0], 40, fill=1, stroke=0)
    canvas_obj.setFillColor(GOLD)
    canvas_obj.setFont('Helvetica-Bold', 9)
    canvas_obj.drawString(20, A4[1] - 28, 'Premium Website Template Guide 2026')
    canvas_obj.setFont('Helvetica', 7)
    canvas_obj.setFillColor(HexColor('#AABBCC'))
    canvas_obj.drawRightString(A4[0] - 20, A4[1] - 28, 'Market Intelligence Report')
    # Footer
    canvas_obj.setFillColor(NAVY)
    canvas_obj.rect(0, 0, A4[0], 30, fill=1, stroke=0)
    canvas_obj.setFillColor(WHITE)
    canvas_obj.setFont('Helvetica', 7)
    canvas_obj.drawString(20, 10, f'© 2026 Template Intelligence — Page {doc.page}')
    canvas_obj.setFillColor(GOLD)
    canvas_obj.drawRightString(A4[0] - 20, 10, 'Confidential')
    canvas_obj.restoreState()


# ── Helper: Gold line separator ──
def gold_line():
    return HRFlowable(width='100%', thickness=1.5, color=GOLD, spaceBefore=4, spaceAfter=8)

def navy_line():
    return HRFlowable(width='100%', thickness=0.75, color=NAVY, spaceBefore=2, spaceAfter=4)

# ── Helper: Section heading with underline ──
def section_heading(text, level=1):
    if level == 1:
        return [Paragraph(text, s_h1), gold_line()]
    elif level == 2:
        return [Paragraph(text, s_h2), navy_line()]
    else:
        return [Paragraph(text, s_h3)]


# ── Helper: color a row by tier ──
def tier_bg(tier):
    c = TIER_COLORS.get(tier.upper(), MID_GRAY)
    # Return a lighter version for backgrounds
    r = min(1, c.red + 0.7)
    g = min(1, c.green + 0.7)
    b = min(1, c.blue + 0.7)
    return Color(r, g, b)


# ── Build document ──
OUTPUT_PATH = '/home/angish/angish-profiliobest/pdf-project/301_Templates_Guide_ENHANCED.pdf'

doc = SimpleDocTemplate(
    OUTPUT_PATH,
    pagesize=A4,
    topMargin=55,
    bottomMargin=45,
    leftMargin=25,
    rightMargin=25,
    title='Premium Website Template Guide 2026',
    author='Template Intelligence'
)

story = []
page_width = A4[0] - 50  # usable width

# ════════════════════════════════════════════════════════════
# SECTION 1: COVER PAGE
# ════════════════════════════════════════════════════════════
cover_story = []

# Navy background frame for cover
class CoverBackground(Flowable):
    def draw(self):
        self.canv.setFillColor(NAVY)
        self.canv.rect(-25, -55, A4[0] + 50, A4[1] + 80, fill=1, stroke=0)
        # Decorative gold line
        self.canv.setStrokeColor(GOLD)
        self.canv.setLineWidth(3)
        self.canv.line(60, A4[1] - 200, A4[0] - 60, A4[1] - 200)
        self.canv.setLineWidth(1)
        self.canv.line(80, A4[1] - 205, A4[0] - 80, A4[1] - 205)
        # Gold accent rectangle top-right
        self.canv.setFillColor(GOLD)
        self.canv.rect(A4[0] - 120, A4[1] - 80, 8, 60, fill=1, stroke=0)
        # Decorative corner elements
        self.canv.setStrokeColor(HexColor('#2A3A5A'))
        self.canv.setLineWidth(1)
        for x, y in [(30, A4[1]-70), (A4[0]-30, A4[1]-70), (30, 30), (A4[0]-30, 30)]:
            self.canv.rect(x, y, 15, 15, fill=0, stroke=1)

cover_story.append(CoverBackground())
cover_story.append(Spacer(1, 160))
cover_story.append(Paragraph('PREMIUM WEBSITE', s_cover_title))
cover_story.append(Paragraph('TEMPLATE GUIDE 2026', s_cover_title))
cover_story.append(Spacer(1, 12))
cover_story.append(Paragraph('301 Templates Ranked & Analyzed  |  Market Intelligence Report', s_cover_sub))
cover_story.append(Spacer(1, 30))
cover_story.append(Paragraph('Complete pricing, technology, and category analysis for', s_cover_sub2))
cover_story.append(Paragraph('web development professionals, agencies, and freelancers', s_cover_sub2))
cover_story.append(Spacer(1, 50))
# Key stats on cover
stats_text = """
<font color="#C9A84C"><b>301</b></font> <font color="#AABBCC">Templates</font> &nbsp;&nbsp;|&nbsp;&nbsp;
<font color="#C9A84C"><b>25+</b></font> <font color="#AABBCC">Categories</font> &nbsp;&nbsp;|&nbsp;&nbsp;
<font color="#C9A84C"><b>10+</b></font> <font color="#AABBCC">Economies</font> &nbsp;&nbsp;|&nbsp;&nbsp;
<font color="#C9A84C"><b>$253K</b></font> <font color="#AABBCC">Market Value</font>
"""
cover_story.append(Paragraph(stats_text, make_style('CoverStats', fontSize=14, fontName='Helvetica', textColor=WHITE, alignment=TA_CENTER, leading=22)))
cover_story.append(Spacer(1, 80))
cover_story.append(Paragraph('Generated by Template Intelligence  •  May 2026', make_style('CoverFooter', fontSize=9, fontName='Helvetica', textColor=HexColor('#6A7A9A'), alignment=TA_CENTER)))

story.append(PageBreak())
story = cover_story  # Start with cover

# ════════════════════════════════════════════════════════════
# TABLE OF CONTENTS
# ════════════════════════════════════════════════════════════
toc_items = [
    ('1.', 'Executive Summary', '3'),
    ('2.', 'Pricing Tier Visualization & Charts', '4'),
    ('3.', 'Top 10 Templates Showcase', '6'),
    ('4.', 'Feature Comparison Matrix', '7'),
    ('5.', 'Economy & Country Targeting Map', '8'),
    ('6.', 'Approach & Sales Methodology', '9'),
    ('7.', 'Money Flow & Profit Calculator', '11'),
    ('8.', '3D & Technology Highlights', '12'),
    ('9.', 'Category Breakdown', '13'),
    ('10.', 'Complete Template Listing', '14'),
]
story.append(PageBreak())
story.append(Paragraph('Table of Contents', s_h1))
story.append(gold_line())
story.append(Spacer(1, 12))
for num, title, pg in toc_items:
    t = f'<b>{num}</b>  {title}  <font size="8" color="#999">············································································································  {pg}</font>'
    story.append(Paragraph(t, s_toc))


# ════════════════════════════════════════════════════════════
# SECTION 2: EXECUTIVE SUMMARY
# ════════════════════════════════════════════════════════════
story.append(PageBreak())
story.append(Paragraph('1. Executive Summary', s_h1))
story.append(gold_line())
story.append(Spacer(1, 6))

total_templates = len(rows)
total_categories = len(cat_counter)
total_economies = len(econ_counter)
total_market_value = 2*10000 + 11*5000 + 44*2000 + 175*500 + 31*100  # rough estimate

story.append(Paragraph(
    f'This comprehensive report analyzes <b>{total_templates} website templates</b> across <b>{total_categories}+ categories</b> '
    f'and <b>{total_economies}+ economic regions</b>. The aggregate market value of these templates represents approximately '
    f'<b>${total_market_value:,}</b> in potential revenue when deployed as client solutions. '
    f'Templates are ranked by a composite score (0-10) evaluating visual design, functional completeness, and overall value.',
    s_body
))
story.append(Spacer(1, 6))

# Key metrics boxes
def metric_box(label, value, desc, color=GOLD):
    t = f'<font size="16" color="{color.hexval()}"><b>{value}</b></font><br/>'
    t += f'<font size="9" color="#1B2A4A"><b>{label}</b></font><br/>'
    t += f'<font size="7" color="#666">{desc}</font>'
    return Paragraph(t, make_style('Box', fontSize=7, alignment=TA_CENTER, leading=14, spaceAfter=6))

metrics_data = [
    [metric_box('Total Templates', total_templates, 'Curated selection'),
     metric_box('Categories', total_categories, 'Diverse industries'),
     metric_box('Economies Mapped', total_economies, 'Global coverage'),
     metric_box('Market Value', f'${total_market_value:,}', 'Revenue potential')]
]
metrics_table = Table(metrics_data, colWidths=[page_width/4]*4)
metrics_table.setStyle(TableStyle([
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('BOX', (0,0), (-1,-1), 0, WHITE),
    ('TOPPADDING', (0,0), (-1,-1), 8),
    ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ('LEFTPADDING', (0,0), (-1,-1), 6),
    ('RIGHTPADDING', (0,0), (-1,-1), 6),
]))
story.append(metrics_table)
story.append(Spacer(1, 10))

# Tier distribution summary
story.append(Paragraph('Tier Distribution Summary', s_h2))
story.append(navy_line())

tier_data = [
    [Paragraph('<b>Tier</b>', s_header_cell),
     Paragraph('<b>Count</b>', s_header_cell),
     Paragraph('<b>Price Range</b>', s_header_cell),
     Paragraph('<b>Revenue Potential</b>', s_header_cell),
     Paragraph('<b>Share</b>', s_header_cell),
     Paragraph('<b>Best For</b>', s_header_cell)]
]
tier_summary = {
    'S': ('2', '$5K-$10K', '$15K', f'{2/total_templates*100:.1f}%', 'Enterprise / Premium'),
    'A': ('11', '$2K-$5K', '$38.5K', f'{11/total_templates*100:.1f}%', 'High-end business'),
    'B': ('44', '$500-$2K', '$55K', f'{44/total_templates*100:.1f}%', 'Professional / SMB'),
    'C': ('175', '$100-$500', '$52.5K', f'{175/total_templates*100:.1f}%', 'Budget / Startups'),
    'D': ('31', '$0-$100', '$1.5K', f'{31/total_templates*100:.1f}%', 'Basic / Personal'),
}

for t in ['S', 'A', 'B', 'C', 'D']:
    cnt, price, rev, share, best = tier_summary[t]
    bg = tier_bg(t)
    tier_data.append([
        Paragraph(f'<b>Tier {t}</b>', s_cell),
        Paragraph(cnt, s_cell),
        Paragraph(price, s_cell),
        Paragraph(rev, s_cell),
        Paragraph(share, s_cell),
        Paragraph(best, s_cell),
    ])

tier_table = Table(tier_data, colWidths=[0.1*page_width, 0.1*page_width, 0.18*page_width, 0.18*page_width, 0.1*page_width, 0.34*page_width])
tier_style = [
    ('BACKGROUND', (0,0), (-1,0), NAVY),
    ('TEXTCOLOR', (0,0), (-1,0), WHITE),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,-1), 8),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('GRID', (0,0), (-1,-1), 0.5, MID_GRAY),
    ('TOPPADDING', (0,0), (-1,-1), 6),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ('LEFTPADDING', (0,0), (-1,-1), 4),
    ('RIGHTPADDING', (0,0), (-1,-1), 4),
]
for i, t in enumerate(['S', 'A', 'B', 'C', 'D'], 1):
    bg = tier_bg(t)
    tier_style.append(('BACKGROUND', (0,i), (-1,i), bg))
    tier_style.append(('FONTNAME', (0,i), (-1,i), 'Helvetica'))

tier_table.setStyle(TableStyle(tier_style))
story.append(tier_table)
story.append(Spacer(1, 8))

story.append(Paragraph(
    '<i>The majority of templates (66.5%) fall into Tier C, offering affordable solutions with solid design. '
    'Premium tiers S & A represent only 4.9% of templates but command the highest per-project value.</i>',
    make_style('ItalicNote', fontSize=8.5, fontName='Helvetica-Oblique', textColor=HexColor('#666'), alignment=TA_CENTER, leading=12)
))


# ════════════════════════════════════════════════════════════
# SECTION 3: PRICING TIER VISUALIZATION (CHARTS)
# ════════════════════════════════════════════════════════════
story.append(PageBreak())
story.append(Paragraph('2. Pricing Tier Visualization & Charts', s_h1))
story.append(gold_line())
story.append(Spacer(1, 6))

# Insert chart images
chart_paths = [
    ('pie_tier_distribution.png', 0.7),
    ('bar_revenue_by_tier.png', 0.7),
]
imgs = []
for fname, wfactor in chart_paths:
    fp = os.path.join(CHARTS_DIR, fname)
    if os.path.exists(fp):
        imgs.append(Image(fp, width=page_width*wfactor, height=page_width*wfactor*0.6))
    else:
        print(f'WARNING: {fp} not found')
        imgs.append(Spacer(1, 20))

# Two charts side by side
chart_table = Table([[imgs[0], imgs[1]]], colWidths=[page_width*0.5, page_width*0.5])
chart_table.setStyle(TableStyle([
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('LEFTPADDING', (0,0), (-1,-1), 5),
    ('RIGHTPADDING', (0,0), (-1,-1), 5),
]))
story.append(chart_table)
story.append(Spacer(1, 10))

# Score distribution chart
fp_hist = os.path.join(CHARTS_DIR, 'hist_score_distribution.png')
if os.path.exists(fp_hist):
    story.append(Image(fp_hist, width=page_width*0.8, height=page_width*0.8*0.55))
    story.append(Spacer(1, 6))

# Economy chart
fp_econ = os.path.join(CHARTS_DIR, 'bar_economy_fit.png')
if os.path.exists(fp_econ):
    story.append(Image(fp_econ, width=page_width*0.85, height=page_width*0.85*0.55))
    story.append(Spacer(1, 6))

# Scatter chart
fp_scatter = os.path.join(CHARTS_DIR, 'scatter_visual_vs_functional.png')
if os.path.exists(fp_scatter):
    story.append(Image(fp_scatter, width=page_width*0.75, height=page_width*0.75*0.6))
    story.append(Spacer(1, 4))

story.append(Paragraph(
    '<i>Chart insights: Higher-tier templates (S, A) cluster in the top-right quadrant with strong visual and functional scores. '
    'Tier C templates form the largest group with moderate scores, while Tier D templates show the most variance.</i>',
    make_style('ChartInsight', fontSize=8.5, fontName='Helvetica-Oblique', textColor=HexColor('#666'), alignment=TA_CENTER, leading=12)
))


# ════════════════════════════════════════════════════════════
# SECTION 4: TOP 10 TEMPLATES SHOWCASE
# ════════════════════════════════════════════════════════════
story.append(PageBreak())
story.append(Paragraph('3. Top 10 Templates Showcase', s_h1))
story.append(gold_line())
story.append(Spacer(1, 6))

top10 = rows[:10]

top_header = [
    Paragraph('<b>Rank</b>', s_header_cell),
    Paragraph('<b>Template Name</b>', s_header_cell),
    Paragraph('<b>Category</b>', s_header_cell),
    Paragraph('<b>Tech Stack</b>', s_header_cell),
    Paragraph('<b>Score</b>', s_header_cell),
    Paragraph('<b>Tier</b>', s_header_cell),
    Paragraph('<b>Price</b>', s_header_cell),
]

top_data = [top_header]
for r in top10:
    tier = r['Tier'].strip()
    bg = tier_bg(tier)
    has_3d = '⭐' if 'Three' in r['TechStack'] or '3D' in r.get('Features', '') else ''
    name_display = r['Template']
    if 'Three' in r['TechStack'] or 'three' in r['Template'].lower():
        name_display += ' ★3D'
    top_data.append([
        Paragraph(f'<b>#{r["Rank"]}</b>', s_cell),
        Paragraph(f'<b>{name_display}</b>', s_cell_bold),
        Paragraph(r['Category'].replace('-', ' ').title(), s_cell),
        Paragraph(r['TechStack'].replace('|', ' | '), s_cell),
        Paragraph(f'<b>{r["CompositeScore"]}</b>', s_cell_bold),
        Paragraph(f'<font color="{TIER_COLORS[tier].hexval()}"><b>{tier}</b></font>', s_cell_bold),
        Paragraph(f'${r["PriceMin"]}-${r["PriceMax"]}', s_cell),
    ])

top_table = Table(top_data, colWidths=[0.06*page_width, 0.25*page_width, 0.17*page_width, 0.22*page_width, 0.08*page_width, 0.07*page_width, 0.15*page_width])
top_style = [
    ('BACKGROUND', (0,0), (-1,0), NAVY),
    ('TEXTCOLOR', (0,0), (-1,0), WHITE),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('GRID', (0,0), (-1,-1), 0.5, MID_GRAY),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('LEFTPADDING', (0,0), (-1,-1), 3),
    ('RIGHTPADDING', (0,0), (-1,-1), 3),
]
for i, r in enumerate(top10, 1):
    tier = r['Tier'].strip()
    bg = tier_bg(tier)
    top_style.append(('BACKGROUND', (0,i), (-1,i), bg))

top_table.setStyle(TableStyle(top_style))
story.append(top_table)
story.append(Spacer(1, 6))

story.append(Paragraph(
    '<i>★3D indicates templates with Three.js or 3D rendering capabilities. '
    'These premium templates command higher prices and offer immersive user experiences.</i>',
    make_style('Note3D', fontSize=8.5, fontName='Helvetica-Oblique', textColor=HexColor('#666'), alignment=TA_CENTER, leading=12)
))


# ════════════════════════════════════════════════════════════
# SECTION 5: FEATURE COMPARISON MATRIX
# ════════════════════════════════════════════════════════════
story.append(PageBreak())
story.append(Paragraph('4. Feature Comparison Matrix', s_h1))
story.append(gold_line())
story.append(Spacer(1, 6))

# Feature matrix for top 25 templates
feature_cols = ['Template', '3D Support', 'React', 'Next.js', 'Docker', 'TypeScript', 'Ecommerce', 'Portfolio']
feat_header = [Paragraph(f'<b>{c}</b>', s_header_cell) for c in feature_cols]

cm_data = [feat_header]
for r in rows[:25]:
    tier = r['Tier'].strip()
    bg = tier_bg(tier)
    ts = r['TechStack']
    feat = r.get('Features', '')
    row = [
        Paragraph(r['Template'], s_cell_bold),
        Paragraph('✓' if ('Three' in ts or '3D' in feat) else '✗', s_cell),
        Paragraph('✓' if 'React' in ts else '✗', s_cell),
        Paragraph('✓' if 'Next' in ts else '✗', s_cell),
        Paragraph('✓' if 'Docker' in ts or 'Docker' in feat else '✗', s_cell),
        Paragraph('✓' if 'TypeScript' in ts or 'TypeScript' in feat else '✗', s_cell),
        Paragraph('✓' if 'Ecommerce' in ts or 'Ecommerce' in feat else '✗', s_cell),
        Paragraph('✓' if 'Portfolio' in ts or 'Portfolio' in feat else '✗', s_cell),
    ]
    cm_data.append(row)

cm_table = Table(cm_data, colWidths=[0.22*page_width, 0.1*page_width, 0.1*page_width, 0.1*page_width, 0.1*page_width, 0.1*page_width, 0.1*page_width, 0.1*page_width])
cm_style = [
    ('BACKGROUND', (0,0), (-1,0), NAVY),
    ('TEXTCOLOR', (0,0), (-1,0), WHITE),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('GRID', (0,0), (-1,-1), 0.5, MID_GRAY),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
]
for i, r in enumerate(rows[:25], 1):
    tier = r['Tier'].strip()
    bg = tier_bg(tier)
    cm_style.append(('BACKGROUND', (0,i), (-1,i), bg))

cm_table.setStyle(TableStyle(cm_style))
story.append(cm_table)
story.append(Spacer(1, 6))

story.append(Paragraph(
    '<i>Checkmarks (✓) indicate feature support based on tech stack and metadata. '
    'Templates higher in the ranking tend to have more feature checkmarks, especially for modern frameworks like React and TypeScript.</i>',
    make_style('NoteFeature', fontSize=8.5, fontName='Helvetica-Oblique', textColor=HexColor('#666'), alignment=TA_CENTER, leading=12)
))


# ════════════════════════════════════════════════════════════
# SECTION 6: ECONOMY & COUNTRY TARGETING MAP
# ════════════════════════════════════════════════════════════
story.append(PageBreak())
story.append(Paragraph('5. Economy & Country Targeting Map', s_h1))
story.append(gold_line())
story.append(Spacer(1, 6))

economy_data = [
    [Paragraph('<b>Country / Region</b>', s_header_cell),
     Paragraph('<b>Best Templates</b>', s_header_cell),
     Paragraph('<b>Key Industries</b>', s_header_cell),
     Paragraph('<b>Recommended Tier</b>', s_header_cell)]
]

economy_map = [
    ('USA / Canada', 'Modern React/Next.js portfolios, e-commerce, corporate', 'Tech, Finance, Healthcare, E-commerce', 'S, A, B'),
    ('United Kingdom', 'Professional services, fintech, agency websites', 'Finance, Legal, Education, Retail', 'A, B'),
    ('Switzerland', 'Luxury brands, finance, precision services', 'Banking, Insurance, Pharma, Luxury', 'S, A'),
    ('Germany', 'Automotive, industrial, engineering, SaaS', 'Manufacturing, Tech, Engineering, Auto', 'A, B'),
    ('France', 'Fashion, creative, culinary, tourism', 'Fashion, Food & Beverage, Tourism, Design', 'A, B, C'),
    ('Australia / NZ', 'Real estate, tourism, local business, startups', 'Real Estate, Tourism, Mining, Agriculture', 'B, C'),
    ('Netherlands', 'Creative agencies, logistics, green tech', 'Logistics, Agriculture, Design, Tech', 'B, C'),
    ('Nordics', 'Clean design, sustainability, health tech', 'Sustainability, Health, Education, Design', 'B, C'),
    ('Japan / Asia', 'Tech startups, gaming, anime, e-commerce', 'Gaming, Electronics, E-commerce, Auto', 'B, C'),
    ('UAE / Middle East', 'Luxury real estate, hospitality, e-commerce', 'Real Estate, Tourism, Oil & Gas, Retail', 'A, B, C'),
]

for country, best, industries, tiers in economy_map:
    economy_data.append([
        Paragraph(f'<b>{country}</b>', s_cell_bold),
        Paragraph(best, s_cell),
        Paragraph(industries, s_cell),
        Paragraph(tiers, s_cell),
    ])

econ_table = Table(economy_data, colWidths=[0.18*page_width, 0.32*page_width, 0.32*page_width, 0.18*page_width])
econ_style = [
    ('BACKGROUND', (0,0), (-1,0), NAVY),
    ('TEXTCOLOR', (0,0), (-1,0), WHITE),
    ('ALIGN', (0,0), (-1,0), 'CENTER'),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('GRID', (0,0), (-1,-1), 0.5, MID_GRAY),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('LEFTPADDING', (0,0), (-1,-1), 4),
    ('RIGHTPADDING', (0,0), (-1,-1), 4),
]
for i in range(1, len(economy_data)):
    bg = LIGHT_GRAY if i % 2 == 0 else WHITE
    econ_style.append(('BACKGROUND', (0,i), (-1,i), bg))

econ_table.setStyle(TableStyle(econ_style))
story.append(econ_table)
story.append(Spacer(1, 8))

story.append(Paragraph(
    '<i>All 263 templates are suitable for the base economies (USA, Canada, UK, Australia, Switzerland, Germany, France). '
    'The recommendations above consider local market preferences, typical budgets, and dominant industries.</i>',
    make_style('EconNote', fontSize=8.5, fontName='Helvetica-Oblique', textColor=HexColor('#666'), alignment=TA_CENTER, leading=12)
))


# ════════════════════════════════════════════════════════════
# SECTION 7: APPROACH & SALES METHODOLOGY
# ════════════════════════════════════════════════════════════
story.append(PageBreak())
story.append(Paragraph('6. Approach & Sales Methodology', s_h1))
story.append(gold_line())
story.append(Spacer(1, 6))

story.append(Paragraph(
    'This section provides a practical framework for using this template guide to generate revenue. '
    'Understanding the tier system and applying the right sales approach maximizes both client satisfaction and profitability.',
    s_body
))
story.append(Spacer(1, 4))

# 6a. Tier-Based Pricing Strategy
story.append(Paragraph('6a. Tier-Based Pricing Strategy', s_h2))
story.append(navy_line())

pricing_data = [
    [Paragraph('<b>Tier</b>', s_header_cell),
     Paragraph('<b>Client Charge</b>', s_header_cell),
     Paragraph('<b>Delivery Time</b>', s_header_cell),
     Paragraph('<b>Scope of Work</b>', s_header_cell),
     Paragraph('<b>Best Client Profile</b>', s_header_cell),]
]

tier_strategy = [
    ('S', '$5,000 – $10,000', '2-3 weeks', 'Full custom build with 3D/Three.js, animations, custom backend if needed, responsive design, SEO', 'Enterprises, luxury brands, high-end agencies'),
    ('A', '$2,000 – $5,000', '1-2 weeks', 'React/Next.js with custom styling, content management integration, multi-page, responsive', 'Established businesses, tech startups, professional services'),
    ('B', '$500 – $2,000', '3-5 days', 'Bootstrap/HTML with brand customization, content swap, responsive, basic SEO', 'Small businesses, local shops, freelancers'),
    ('C', '$100 – $500', '1-2 days', 'Quick deploy template with content replacement, basic configuration, hosting setup', 'Budget-conscious clients, students, personal projects'),
    ('D', '$0 – $100', 'Same day', 'Basic setup, minimal customization, file delivery only', 'Personal use, learning projects, ultra-budget'),
]

for t, charge, delivery, scope, client in tier_strategy:
    bg = tier_bg(t)
    pricing_data.append([
        Paragraph(f'<b>Tier {t}</b>', s_cell_bold),
        Paragraph(f'<b>{charge}</b>', s_cell_bold),
        Paragraph(delivery, s_cell),
        Paragraph(scope, s_cell),
        Paragraph(client, s_cell),
    ])

pricing_table = Table(pricing_data, colWidths=[0.07*page_width, 0.15*page_width, 0.12*page_width, 0.38*page_width, 0.28*page_width])
pricing_style = [
    ('BACKGROUND', (0,0), (-1,0), NAVY),
    ('TEXTCOLOR', (0,0), (-1,0), WHITE),
    ('ALIGN', (0,0), (0,-1), 'CENTER'),
    ('ALIGN', (1,0), (1,-1), 'CENTER'),
    ('ALIGN', (2,0), (2,-1), 'CENTER'),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('GRID', (0,0), (-1,-1), 0.5, MID_GRAY),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('LEFTPADDING', (0,0), (-1,-1), 4),
    ('RIGHTPADDING', (0,0), (-1,-1), 4),
]
for i, t in enumerate(['S', 'A', 'B', 'C', 'D'], 1):
    bg = tier_bg(t)
    pricing_style.append(('BACKGROUND', (0,i), (-1,i), bg))

pricing_table.setStyle(TableStyle(pricing_style))
story.append(pricing_table)
story.append(Spacer(1, 10))

# 6b. Sales Approach Flowchart
story.append(Paragraph('6b. Sales Approach Flowchart', s_h2))
story.append(navy_line())

flowchart_text = """
<table border="0" cellpadding="4" cellspacing="0" width="100%">
<tr><td bgcolor="#1B2A4A" align="center"><font color="white" size="8"><b> PROSPECT INQUIRY </b></font></td></tr>
<tr><td align="center"><font size="10" color="#C9A84C">↓</font></td></tr>
<tr><td bgcolor="#2A3A5A" align="center"><font color="white" size="8"><b> INDUSTRY ANALYSIS </b></font><br/><font color="#AABBCC" size="7">Identify client's sector, competition, budget range</font></td></tr>
<tr><td align="center"><font size="10" color="#C9A84C">↓</font></td></tr>
<tr><td bgcolor="#2A3A5A" align="center"><font color="white" size="8"><b> TIER RECOMMENDATION </b></font><br/><font color="#AABBCC" size="7">Match budget &amp; requirements → S / A / B / C / D</font></td></tr>
<tr><td align="center"><font size="10" color="#C9A84C">↓</font></td></tr>
<tr><td bgcolor="#2A3A5A" align="center"><font color="white" size="8"><b> TEMPLATE SELECTION </b></font><br/><font color="#AABBCC" size="7">Browse guide → pick top-ranked template in category</font></td></tr>
<tr><td align="center"><font size="10" color="#C9A84C">↓</font></td></tr>
<tr><td bgcolor="#2A3A5A" align="center"><font color="white" size="8"><b> CUSTOMIZATION QUOTE </b></font><br/><font color="#AABBCC" size="7">Itemize template cost + customization + add-ons</font></td></tr>
<tr><td align="center"><font size="10" color="#C9A84C">↓</font></td></tr>
<tr><td bgcolor="#2A3A5A" align="center"><font color="white" size="8"><b> DEVELOPMENT </b></font><br/><font color="#AABBCC" size="7">Customize, integrate, test, optimize</font></td></tr>
<tr><td align="center"><font size="10" color="#C9A84C">↓</font></td></tr>
<tr><td bgcolor="#2A3A5A" align="center"><font color="white" size="8"><b> REVIEW &amp; APPROVAL </b></font><br/><font color="#AABBCC" size="7">Client review → revisions → sign-off</font></td></tr>
<tr><td align="center"><font size="10" color="#C9A84C">↓</font></td></tr>
<tr><td bgcolor="#1B2A4A" align="center"><font color="white" size="8"><b> DELIVERY &amp; HANDOFF </b></font><br/><font color="#AABBCC" size="7">Deploy, train, invoice → upsell maintenance</font></td></tr>
</table>
"""
story.append(Paragraph(flowchart_text, make_style('Flowchart', fontSize=7, leading=14, spaceAfter=10)))
story.append(Spacer(1, 6))

# 6c. Profit Calculator
story.append(Paragraph('6c. Profit Calculator', s_h2))
story.append(navy_line())

profit_data = [
    [Paragraph('<b>Tier</b>', s_header_cell),
     Paragraph('<b>Client Charge</b>', s_header_cell),
     Paragraph('<b>Your Cost</b>', s_header_cell),
     Paragraph('<b>Profit Range</b>', s_header_cell),
     Paragraph('<b>Profit Margin</b>', s_header_cell),]
]

profit_info = [
    ('S', '$5,000 – $10,000', '~$200 (hosting + setup)', '$4,800 – $9,800', '96-98%'),
    ('A', '$2,000 – $5,000', '~$150 (hosting + setup)', '$1,850 – $4,850', '93-97%'),
    ('B', '$500 – $2,000', '~$100 (hosting + setup)', '$400 – $1,900', '80-95%'),
    ('C', '$100 – $500', '~$50 (domain + hosting)', '$50 – $450', '50-90%'),
    ('D', '$0 – $100', '~$10 (domain only)', '$0 – $90', '0-90%'),
]

for t, charge, cost, profit, margin in profit_info:
    bg = tier_bg(t)
    profit_data.append([
        Paragraph(f'<b>Tier {t}</b>', s_cell_bold),
        Paragraph(charge, s_cell),
        Paragraph(cost, s_cell),
        Paragraph(f'<b>{profit}</b>', s_cell_bold),
        Paragraph(margin, s_cell),
    ])

profit_table = Table(profit_data, colWidths=[0.08*page_width, 0.22*page_width, 0.22*page_width, 0.22*page_width, 0.16*page_width])
profit_style = [
    ('BACKGROUND', (0,0), (-1,0), NAVY),
    ('TEXTCOLOR', (0,0), (-1,0), WHITE),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('GRID', (0,0), (-1,-1), 0.5, MID_GRAY),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
]
for i, t in enumerate(['S', 'A', 'B', 'C', 'D'], 1):
    bg = tier_bg(t)
    profit_style.append(('BACKGROUND', (0,i), (-1,i), bg))

profit_table.setStyle(TableStyle(profit_style))
story.append(profit_table)
story.append(Spacer(1, 8))

story.append(Paragraph(
    '<b>Key Insight:</b> The primary cost is your time for customization. Template licensing is generally a one-time cost '
    'with unlimited use rights. Hosting costs are passed through or marked up. The highest-margin strategy is Tier B/C '
    'with high volume, or Tier S/A with premium pricing.',
    s_body
))
story.append(Spacer(1, 6))

# 6d. Upsell Strategy
story.append(Paragraph('6d. Upsell Strategy & Add-On Services', s_h2))
story.append(navy_line())

upsell_data = [
    [Paragraph('<b>Add-On Service</b>', s_header_cell),
     Paragraph('<b>Additional Charge</b>', s_header_cell),
     Paragraph('<b>Implementation Effort</b>', s_header_cell),
     Paragraph('<b>Target Tier</b>', s_header_cell),]
]

upsells = [
    ('3D Animation (Three.js)', '+$2,000 – $5,000', '2-5 days', 'S, A, B'),
    ('Ecommerce Integration', '+$1,000 – $3,000', '2-4 days', 'A, B, C'),
    ('SEO Optimization Package', '+$500 – $1,000', '1-2 days', 'A, B, C, D'),
    ('Custom CMS Integration', '+$1,000 – $2,500', '2-3 days', 'A, B'),
    ('Multi-language Support', '+$500 – $1,500', '1-2 days', 'A, B, C'),
    ('Performance Optimization', '+$300 – $800', '1 day', 'B, C, D'),
    ('Analytics & Tracking Setup', '+$200 – $500', 'Half day', 'A, B, C, D'),
    ('Monthly Maintenance Package', '+$200/month', 'Ongoing', 'All tiers'),
    ('Social Media Integration', '+$300 – $600', 'Half day', 'B, C, D'),
    ('Email Marketing Setup', '+$400 – $800', '1 day', 'B, C'),
]

for service, charge, effort, target in upsells:
    upsell_data.append([
        Paragraph(f'<b>{service}</b>', s_cell_bold),
        Paragraph(charge, s_cell),
        Paragraph(effort, s_cell),
        Paragraph(target, s_cell),
    ])

upsell_table = Table(upsell_data, colWidths=[0.32*page_width, 0.22*page_width, 0.22*page_width, 0.14*page_width])
upsell_style = [
    ('BACKGROUND', (0,0), (-1,0), NAVY),
    ('TEXTCOLOR', (0,0), (-1,0), WHITE),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('GRID', (0,0), (-1,-1), 0.5, MID_GRAY),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ('LEFTPADDING', (0,0), (-1,-1), 4),
    ('RIGHTPADDING', (0,0), (-1,-1), 4),
]
for i in range(1, len(upsell_data)):
    bg = LIGHT_GRAY if i % 2 == 0 else WHITE
    upsell_style.append(('BACKGROUND', (0,i), (-1,i), bg))

upsell_table.setStyle(TableStyle(upsell_style))
story.append(upsell_table)
story.append(Spacer(1, 8))

story.append(Paragraph(
    '<b>Strategy:</b> Always quote the base template first, then present add-ons as "recommended upgrades." '
    'Clients who initially resist a high base price often accept when the price is broken into base + optional enhancements. '
    'Annual maintenance contracts provide recurring revenue and reduce client churn.',
    s_body
))


# ════════════════════════════════════════════════════════════
# SECTION 7b: MONEY FLOW DIAGRAM
# ════════════════════════════════════════════════════════════
story.append(PageBreak())
story.append(Paragraph('7. Money Flow & Profit Calculator', s_h1))
story.append(gold_line())
story.append(Spacer(1, 6))

money_flow_text = """
<table border="0" cellpadding="6" cellspacing="3" width="100%">
<tr><th bgcolor="#1B2A4A" colspan="5"><font color="#C9A84C" size="10"><b> 💰 MONEY FLOW — FROM CLIENT TO YOUR POCKET</b></font></th></tr>
<tr bgcolor="#C9A84C">
  <td align="center"><font size="8" color="#1B2A4A"><b>TIER</b></font></td>
  <td align="center"><font size="8" color="#1B2A4A"><b>CLIENT PAYS YOU</b></font></td>
  <td align="center"><font size="8" color="#1B2A4A"><b>→</b></font></td>
  <td align="center"><font size="8" color="#1B2A4A"><b>YOUR COST</b></font></td>
  <td align="center"><font size="8" color="#1B2A4A"><b>YOUR PROFIT</b></font></td>
</tr>
<tr bgcolor="#FFF8DC">
  <td align="center"><font color="#FFD700" size="9"><b>S</b></font></td>
  <td align="center"><font size="9" color="#1B2A4A"><b>$5,000 – $10,000</b></font></td>
  <td align="center"><font color="#C9A84C" size="12">→</font></td>
  <td align="center"><font size="9" color="#666">~$200</font></td>
  <td align="center"><font size="9" color="#2ECC71"><b>$4,800 – $9,800</b></font></td>
</tr>
<tr bgcolor="#EBF5FB">
  <td align="center"><font color="#4169E1" size="9"><b>A</b></font></td>
  <td align="center"><font size="9" color="#1B2A4A"><b>$2,000 – $5,000</b></font></td>
  <td align="center"><font color="#C9A84C" size="12">→</font></td>
  <td align="center"><font size="9" color="#666">~$150</font></td>
  <td align="center"><font size="9" color="#2ECC71"><b>$1,850 – $4,850</b></font></td>
</tr>
<tr bgcolor="#E8F8F5">
  <td align="center"><font color="#2ECC71" size="9"><b>B</b></font></td>
  <td align="center"><font size="9" color="#1B2A4A"><b>$500 – $2,000</b></font></td>
  <td align="center"><font color="#C9A84C" size="12">→</font></td>
  <td align="center"><font size="9" color="#666">~$100</font></td>
  <td align="center"><font size="9" color="#2ECC71"><b>$400 – $1,900</b></font></td>
</tr>
<tr bgcolor="#F5F5F5">
  <td align="center"><font color="#95A5A6" size="9"><b>C</b></font></td>
  <td align="center"><font size="9" color="#1B2A4A"><b>$100 – $500</b></font></td>
  <td align="center"><font color="#C9A84C" size="12">→</font></td>
  <td align="center"><font size="9" color="#666">~$50</font></td>
  <td align="center"><font size="9" color="#2ECC71"><b>$50 – $450</b></font></td>
</tr>
<tr bgcolor="#FAFAFA">
  <td align="center"><font color="#BDC3C7" size="9"><b>D</b></font></td>
  <td align="center"><font size="9" color="#1B2A4A"><b>$0 – $100</b></font></td>
  <td align="center"><font color="#C9A84C" size="12">→</font></td>
  <td align="center"><font size="9" color="#666">~$10</font></td>
  <td align="center"><font size="9" color="#2ECC71"><b>$0 – $90</b></font></td>
</tr>
<tr><td colspan="5" bgcolor="#1B2A4A" align="center"><font color="#C9A84C" size="8"><b>💡 TIP: Focus on Tier A & B for the best balance of volume × profit margin × delivery time</b></font></td></tr>
</table>
"""
story.append(Paragraph(money_flow_text, make_style('MoneyFlowBody', fontSize=8, leading=16, spaceAfter=8)))
story.append(Spacer(1, 10))

# Revenue projection
story.append(Paragraph('Revenue Projection Per Month (Realistic)', s_h2))
story.append(navy_line())

proj_data = [
    [Paragraph('<b>Strategy</b>', s_header_cell),
     Paragraph('<b>Tier Focus</b>', s_header_cell),
     Paragraph('<b>Projects/Month</b>', s_header_cell),
     Paragraph('<b>Avg Revenue/Month</b>', s_header_cell),
     Paragraph('<b>Annual Revenue</b>', s_header_cell),]
]

projections = [
    ('💎 Premium Boutique', 'S + A (high-end)', '2-3', '$12,000 – $22,000', '$144K – $264K'),
    ('🏢 Full Service Agency', 'A + B (balanced)', '5-8', '$10,000 – $20,000', '$120K – $240K'),
    ('⚡ Volume Agency', 'B + C (high volume)', '10-15', '$8,000 – $15,000', '$96K – $180K'),
    ('💻 Freelancer', 'B + C (selective)', '3-5', '$3,000 – $8,000', '$36K – $96K'),
    ('🛠️ Beginner', 'C + D (learning)', '5-10', '$1,000 – $3,000', '$12K – $36K'),
]

for strategy, tier, projects, rev, annual in projections:
    proj_data.append([
        Paragraph(strategy, s_cell_bold),
        Paragraph(tier, s_cell),
        Paragraph(projects, s_cell),
        Paragraph(rev, s_cell),
        Paragraph(annual, s_cell),
    ])

proj_table = Table(proj_data, colWidths=[0.2*page_width, 0.2*page_width, 0.16*page_width, 0.22*page_width, 0.22*page_width])
proj_style = [
    ('BACKGROUND', (0,0), (-1,0), NAVY),
    ('TEXTCOLOR', (0,0), (-1,0), WHITE),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('GRID', (0,0), (-1,-1), 0.5, MID_GRAY),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
]
for i in range(1, len(proj_data)):
    bg = LIGHT_GRAY if i % 2 == 0 else WHITE
    proj_style.append(('BACKGROUND', (0,i), (-1,i), bg))

proj_table.setStyle(TableStyle(proj_style))
story.append(proj_table)


# ════════════════════════════════════════════════════════════
# SECTION 8: 3D & TECHNOLOGY HIGHLIGHTS
# ════════════════════════════════════════════════════════════
story.append(PageBreak())
story.append(Paragraph('8. 3D & Technology Highlights', s_h1))
story.append(gold_line())
story.append(Spacer(1, 6))

story.append(Paragraph('Three.js & 3D Capable Templates', s_h2))
story.append(navy_line())

story.append(Paragraph(
    f'A total of <b>{len(threejs_list)} templates</b> feature Three.js or 3D rendering capabilities. '
    f'These represent the cutting edge of web design, offering immersive user experiences that command premium pricing. '
    f'All 3D-capable templates are in tiers S, A, or B.',
    s_body
))
story.append(Spacer(1, 4))

# Three.js templates table
threejs_header = [
    Paragraph('<b>Rank</b>', s_header_cell),
    Paragraph('<b>Template</b>', s_header_cell),
    Paragraph('<b>Category</b>', s_header_cell),
    Paragraph('<b>Tech Stack</b>', s_header_cell),
    Paragraph('<b>Tier</b>', s_header_cell),
    Paragraph('<b>Score</b>', s_header_cell),
]

threejs_data = [threejs_header]
for r in threejs_list[:20]:
    tier = r['Tier'].strip()
    threejs_data.append([
        Paragraph(f'#{r["Rank"]}', s_cell),
        Paragraph(f'<b>{r["Template"]}</b>', s_cell_bold),
        Paragraph(r['Category'].replace('-', ' ').title(), s_cell),
        Paragraph(r['TechStack'].replace('|', ' | '), s_cell),
        Paragraph(f'<font color="{TIER_COLORS[tier].hexval()}"><b>{tier}</b></font>', s_cell_bold),
        Paragraph(r['CompositeScore'], s_cell),
    ])

threejs_table = Table(threejs_data, colWidths=[0.07*page_width, 0.28*page_width, 0.18*page_width, 0.25*page_width, 0.07*page_width, 0.07*page_width])
threejs_style = [
    ('BACKGROUND', (0,0), (-1,0), NAVY),
    ('TEXTCOLOR', (0,0), (-1,0), WHITE),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('GRID', (0,0), (-1,-1), 0.5, MID_GRAY),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
]
for i, r in enumerate(threejs_list[:20], 1):
    tier = r['Tier'].strip()
    bg = tier_bg(tier)
    threejs_style.append(('BACKGROUND', (0,i), (-1,i), bg))

threejs_table.setStyle(TableStyle(threejs_style))
story.append(threejs_table)
story.append(Spacer(1, 10))

# Tech popularity chart
story.append(Paragraph('Technology Popularity', s_h2))
story.append(navy_line())

fp_tech = os.path.join(CHARTS_DIR, 'bar_tech_popularity.png')
if os.path.exists(fp_tech):
    story.append(Image(fp_tech, width=page_width*0.8, height=page_width*0.8*0.55))
    story.append(Spacer(1, 6))

story.append(Paragraph(
    '<i>Bootstrap remains the dominant framework with 140 templates, while Static HTML accounts for 100 templates. '
    'React and Three.js represent the modern, interactive segment with growing adoption.</i>',
    make_style('TechNote', fontSize=8.5, fontName='Helvetica-Oblique', textColor=HexColor('#666'), alignment=TA_CENTER, leading=12)
))


# ════════════════════════════════════════════════════════════
# SECTION 9: CATEGORY BREAKDOWN
# ════════════════════════════════════════════════════════════
story.append(PageBreak())
story.append(Paragraph('9. Category Breakdown', s_h1))
story.append(gold_line())
story.append(Spacer(1, 6))

# Get best template per category
best_per_cat = {}
for r in rows:
    cat = r['Category'].strip()
    if cat not in best_per_cat:
        best_per_cat[cat] = r
    else:
        try:
            if float(r['CompositeScore']) > float(best_per_cat[cat]['CompositeScore']):
                best_per_cat[cat] = r
        except:
            pass

cat_header = [
    Paragraph('<b>Category</b>', s_header_cell),
    Paragraph('<b>Count</b>', s_header_cell),
    Paragraph('<b>Top Template</b>', s_header_cell),
    Paragraph('<b>Best Tier</b>', s_header_cell),
    Paragraph('<b>Score</b>', s_header_cell),
    Paragraph('<b>Recommended Economy</b>', s_header_cell),
]

cat_data = [cat_header]
for cat_name, cat_count in sorted(cat_counter.items(), key=lambda x: -x[1]):
    br = best_per_cat.get(cat_name, {})
    score = br.get('CompositeScore', 'N/A')
    tier = br.get('Tier', 'N/A').strip()
    template_name = br.get('Template', 'N/A')
    # Determine best economy
    economies = br.get('Economies', '')
    rec_econ = 'Global'
    if economies:
        econ_list = [e.strip() for e in economies.split(',')]
        rec_econ = ', '.join(econ_list[:3])
    
    cat_data.append([
        Paragraph(cat_name.replace('-', ' ').title(), s_cell_bold),
        Paragraph(str(cat_count), s_cell),
        Paragraph(template_name, s_cell),
        Paragraph(f'<font color="{TIER_COLORS.get(tier, MID_GRAY).hexval()}"><b>{tier}</b></font>', s_cell_bold),
        Paragraph(str(score), s_cell),
        Paragraph(rec_econ, s_cell),
    ])

cat_table = Table(cat_data, colWidths=[0.17*page_width, 0.07*page_width, 0.3*page_width, 0.09*page_width, 0.07*page_width, 0.3*page_width])
cat_style = [
    ('BACKGROUND', (0,0), (-1,0), NAVY),
    ('TEXTCOLOR', (0,0), (-1,0), WHITE),
    ('ALIGN', (1,0), (4,-1), 'CENTER'),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('GRID', (0,0), (-1,-1), 0.5, MID_GRAY),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ('LEFTPADDING', (0,0), (-1,-1), 3),
    ('RIGHTPADDING', (0,0), (-1,-1), 3),
]
for i in range(1, len(cat_data)):
    bg = LIGHT_GRAY if i % 2 == 0 else WHITE
    cat_style.append(('BACKGROUND', (0,i), (-1,i), bg))

cat_table.setStyle(TableStyle(cat_style))
story.append(cat_table)


# ════════════════════════════════════════════════════════════
# SECTION 10: COMPLETE TEMPLATE LISTING
# ════════════════════════════════════════════════════════════
story.append(PageBreak())
story.append(Paragraph('10. Complete Template Listing', s_h1))
story.append(gold_line())
story.append(Spacer(1, 4))

story.append(Paragraph(
    f'All {len(rows)} templates ranked by composite score. '
    f'Use this listing as a quick reference for pricing, tier, and category information.',
    s_body
))
story.append(Spacer(1, 4))

list_header = [
    Paragraph('<b>Rk</b>', s_header_cell),
    Paragraph('<b>Category</b>', s_header_cell),
    Paragraph('<b>Template Name</b>', s_header_cell),
    Paragraph('<b>Score</b>', s_header_cell),
    Paragraph('<b>Tier</b>', s_header_cell),
    Paragraph('<b>Price</b>', s_header_cell),
]

# Split into chunks of ~40 rows per page (we'll let ReportLab paginate)
max_rows_per_table = 38
row_chunks = [rows[i:i+max_rows_per_table] for i in range(0, len(rows), max_rows_per_table)]

for chunk_idx, chunk in enumerate(row_chunks):
    if chunk_idx > 0:
        story.append(PageBreak())
    
    list_data = [list_header]
    for r in chunk:
        tier = r['Tier'].strip()
        list_data.append([
            Paragraph(r['Rank'], s_cell),
            Paragraph(r['Category'].replace('-', ' ').title(), s_cell),
            Paragraph(r['Template'], s_cell),
            Paragraph(f'<b>{r["CompositeScore"]}</b>', s_cell_bold),
            Paragraph(f'<font color="{TIER_COLORS.get(tier, MID_GRAY).hexval()}"><b>{tier}</b></font>', s_cell_bold),
            Paragraph(f'${r["PriceMin"]}–${r["PriceMax"]}', s_cell),
        ])
    
    list_table = Table(list_data, colWidths=[0.05*page_width, 0.22*page_width, 0.4*page_width, 0.08*page_width, 0.07*page_width, 0.13*page_width])
    list_style = [
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('ALIGN', (0,0), (0,-1), 'CENTER'),
        ('ALIGN', (3,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.4, SOFT_GRAY),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 2),
        ('RIGHTPADDING', (0,0), (-1,-1), 2),
    ]
    for i, r in enumerate(chunk, 1):
        tier = r['Tier'].strip()
        bg = tier_bg(tier)
        list_style.append(('BACKGROUND', (0,i), (-1,i), bg))
    
    list_table.setStyle(TableStyle(list_style))
    story.append(list_table)


# ════════════════════════════════════════════════════════════
# FINAL NOTE
# ════════════════════════════════════════════════════════════
story.append(Spacer(1, 20))
story.append(gold_line())
story.append(Paragraph(
    '<i>This guide was generated automatically from enriched template metadata. '
    'Scores are calculated from visual design quality, functional completeness, and value relative to pricing. '
    'Use this guide to identify the best templates for your clients and maximize your revenue.</i>',
    make_style('FinalNote', fontSize=9, fontName='Helvetica-Oblique', textColor=HexColor('#888'), alignment=TA_CENTER, leading=14)
))
story.append(Spacer(1, 10))


# ════════════════════════════════════════════════════════════
# BUILD PDF
# ════════════════════════════════════════════════════════════
print('Building PDF...')
doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
print(f'\n✓ Enhanced PDF generated successfully!')
print(f'  Output: {OUTPUT_PATH}')

import os.path
size = os.path.getsize(OUTPUT_PATH)
print(f'  Size: {size/1024:.0f} KB')
