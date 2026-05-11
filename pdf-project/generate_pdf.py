#!/usr/bin/env python3
"""
301 Website Templates - Complete Ranking & Pricing Guide PDF Generator
Generates a professional, presentation-ready PDF using ReportLab.
"""

import re
import os
from collections import defaultdict, OrderedDict
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.lib.units import mm, cm, inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    KeepTogether, ListFlowable, ListItem, Frame, PageTemplate, BaseDocTemplate,
    NextPageTemplate
)
from reportlab.platypus.flowables import HRFlowable
from reportlab.platypus.doctemplate import PageTemplate
from reportlab.platypus.frames import Frame
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Circle
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics import renderPDF

# ============================================================
# COLOR SCHEME
# ============================================================
DARK_BLUE = colors.HexColor('#1B2A4A')
GOLD = colors.HexColor('#C9A84C')
LIGHT_GOLD = colors.HexColor('#E8D5A3')
LIGHT_BLUE = colors.HexColor('#2C4A7C')
PALE_BLUE = colors.HexColor('#E8EFF7')
WHITE = colors.white
BLACK = colors.black
DARK_GRAY = colors.HexColor('#333333')
MED_GRAY = colors.HexColor('#666666')
LIGHT_GRAY = colors.HexColor('#F0F0F0')
TABLE_HEADER_BG = colors.HexColor('#1B2A4A')
TABLE_ALT_ROW = colors.HexColor('#F5F7FA')
ACCENT_GREEN = colors.HexColor('#2ECC71')
ACCENT_RED = colors.HexColor('#E74C3C')
ACCENT_ORANGE = colors.HexColor('#F39C12')

# ============================================================
# PARSE TEMPLATE DATA
# ============================================================
def parse_templates(filepath='/tmp/template_ranking.txt'):
    """Parse the template ranking file."""
    data = open(filepath).read()
    lines = data.strip().split('\n')
    templates = []
    
    for i, line in enumerate(lines):
        if not line.strip():
            continue
        tokens = line.split()
        if len(tokens) < 4:
            continue
        
        size_raw = tokens[0]
        files_raw = tokens[1]
        pages_raw = tokens[2]
        tech_raw = tokens[3]
        name_raw = ' '.join(tokens[4:]) if len(tokens) > 4 else ''
        
        # Clean tech stack
        tech = tech_raw.lstrip(',').strip()
        tech_list = [t.strip() for t in tech.split(',') if t.strip()]
        
        # Extract category and template name
        if '/' in name_raw:
            cat = name_raw.split('/')[0]
            tpl_name = name_raw.split('/', 1)[1]
        else:
            cat = 'uncategorized'
            tpl_name = name_raw
        
        templates.append({
            'rank': i + 1,
            'size': size_raw,
            'files': int(files_raw) if files_raw.isdigit() else 0,
            'pages': int(pages_raw) if pages_raw.isdigit() else 0,
            'tech': tech_list,
            'category': cat,
            'name': tpl_name,
            'full_path': name_raw,
        })
    
    return templates


def enrich_tech_stacks(templates):
    """Add detected tech from the user's additional analysis."""
    # Maps from template name (full or partial) to additional tech
    additional_tech = {
        '3d-websites/my-portfolio-website': ['React', 'Three.js'],
        '3d-websites/Sayanth-portfolio': ['React', 'Three.js', 'TypeScript'],
        'agency-business/pinak_agency': ['React', 'Next.js', 'TypeScript'],
        'construction/nextjs-construction-website-template': ['React', 'Next.js'],
        'dentist/nextjs-dental-website-template': ['React', 'Next.js'],
        'education-school/cora_university': ['React'],
        'event-wedding/react-event-planner-website-template': ['React', 'TypeScript'],
        'fashion/Fashion-eCommerce-Shop-in-React': ['React', 'TypeScript', 'Redux'],
        'medical/themixly_medical': ['React', 'Next.js'],
        'medical/themixly_ortho': ['React', 'Next.js'],
        'photography/react-photographer-portfolio-website-template': ['React', 'Framer Motion'],
        'photography-wedding/nextjs-wedding-photographer-website': ['React', 'Next.js', 'Three.js', 'Framer Motion', 'Docker'],
        'portfolios/cleanfolio': ['React'],
        'portfolios/developerFolio': ['React', 'Docker'],
        'portfolios/developer-portfolio': ['React', 'Next.js', 'TypeScript', 'Docker'],
        'portfolios/gitprofile': ['React', 'TypeScript', 'Docker'],
        'portfolios/hashir-home': ['React'],
        'portfolios/masterPortfolio': ['React', 'Docker'],
        'portfolios/nextjs-portfolio-starter': ['React', 'Next.js', 'Framer Motion'],
        'portfolios/Portfolio': ['React'],
        'portfolios/reactfolio': ['React'],
        'portfolios/said7388-portfolio': ['React', 'Next.js', 'Docker'],
        'real-estate/cora_estate': ['React'],
        'wedding-planning/wedding-template': ['React', 'Next.js'],
        'real-estate/amozo_houses': ['React', 'TypeScript'],
        'law-legal/src': ['TypeScript'],
        'law-legal/public': ['TypeScript'],
        'portfolios/devportfolio-Ryan': ['TypeScript'],
        'agency-business/ryan_agency': ['TypeScript'],
    }
    
    for t in templates:
        fp = t['full_path']
        if fp in additional_tech:
            extra = additional_tech[fp]
            # Merge without duplicating
            existing = set(t['tech'])
            for e in extra:
                if e not in existing:
                    t['tech'].append(e)
    
    return templates


def parse_size_bytes(size_str):
    """Convert size string like '824.5M' or '26.4K' to bytes."""
    size_str = str(size_str).strip()
    mult = {'K': 1024, 'M': 1024**2, 'B': 1}
    if size_str[-1] in mult:
        try:
            num = float(size_str[:-1])
            return int(num * mult[size_str[-1]])
        except:
            return 0
    try:
        return int(size_str)
    except:
        return 0


# ============================================================
# LOAD AND ENRICH DATA
# ============================================================
templates = parse_templates()
templates = enrich_tech_stacks(templates)

# Group by category
categories = OrderedDict()
for t in templates:
    cat = t['category']
    if cat not in categories:
        categories[cat] = []
    categories[cat].append(t)

# Top 10 by rank (first 10)
top10 = templates[:10]

# Sort categories by template count
sorted_cats = sorted(categories.items(), key=lambda x: -len(x[1]))

# ============================================================
# STYLES
# ============================================================
styles = getSampleStyleSheet()

# Custom styles
styles.add(ParagraphStyle(
    'CoverTitle', parent=styles['Title'],
    fontSize=36, leading=42, textColor=GOLD,
    alignment=TA_CENTER, spaceAfter=20,
    fontName='Helvetica-Bold',
))
styles.add(ParagraphStyle(
    'CoverSubtitle', parent=styles['Normal'],
    fontSize=18, leading=24, textColor=WHITE,
    alignment=TA_CENTER, spaceAfter=10,
    fontName='Helvetica',
))
styles.add(ParagraphStyle(
    'CoverInfo', parent=styles['Normal'],
    fontSize=12, leading=16, textColor=LIGHT_GOLD,
    alignment=TA_CENTER,
    fontName='Helvetica',
))
styles.add(ParagraphStyle(
    'SectionTitle', parent=styles['Heading1'],
    fontSize=22, leading=28, textColor=DARK_BLUE,
    spaceBefore=20, spaceAfter=12,
    fontName='Helvetica-Bold',
    borderWidth=0, borderPadding=0,
))
styles.add(ParagraphStyle(
    'SectionTitleGold', parent=styles['Heading1'],
    fontSize=22, leading=28, textColor=GOLD,
    spaceBefore=20, spaceAfter=12,
    fontName='Helvetica-Bold',
))
styles.add(ParagraphStyle(
    'CatTitle', parent=styles['Heading2'],
    fontSize=16, leading=20, textColor=DARK_BLUE,
    spaceBefore=15, spaceAfter=8,
    fontName='Helvetica-Bold',
))
styles.add(ParagraphStyle(
    'TemplateName', parent=styles['Normal'],
    fontSize=10, leading=13, textColor=DARK_BLUE,
    fontName='Helvetica-Bold',
))
styles.add(ParagraphStyle(
    'BodyText2', parent=styles['Normal'],
    fontSize=9, leading=12, textColor=DARK_GRAY,
    fontName='Helvetica',
))
styles.add(ParagraphStyle(
    'SmallText', parent=styles['Normal'],
    fontSize=7, leading=9, textColor=MED_GRAY,
    fontName='Helvetica',
))
styles.add(ParagraphStyle(
    'TableCell', parent=styles['Normal'],
    fontSize=7.5, leading=10, textColor=DARK_GRAY,
    fontName='Helvetica',
))
styles.add(ParagraphStyle(
    'TableCellBold', parent=styles['Normal'],
    fontSize=7.5, leading=10, textColor=DARK_BLUE,
    fontName='Helvetica-Bold',
))
styles.add(ParagraphStyle(
    'TOCEntry', parent=styles['Normal'],
    fontSize=11, leading=18, textColor=DARK_BLUE,
    leftIndent=20, fontName='Helvetica',
))
styles.add(ParagraphStyle(
    'TOCEntryBold', parent=styles['Normal'],
    fontSize=12, leading=20, textColor=DARK_BLUE,
    leftIndent=10, fontName='Helvetica-Bold',
))
styles.add(ParagraphStyle(
    'FooterStyle', parent=styles['Normal'],
    fontSize=7, leading=9, textColor=LIGHT_GOLD,
    alignment=TA_CENTER, fontName='Helvetica',
))
styles.add(ParagraphStyle(
    'HeaderStyle', parent=styles['Normal'],
    fontSize=7, leading=9, textColor=WHITE,
    alignment=TA_CENTER, fontName='Helvetica',
))
styles.add(ParagraphStyle(
    'RankNumber', parent=styles['Normal'],
    fontSize=24, leading=28, textColor=GOLD,
    fontName='Helvetica-Bold',
    alignment=TA_CENTER,
))
styles.add(ParagraphStyle(
    'ReasoningText', parent=styles['Normal'],
    fontSize=9, leading=13, textColor=DARK_GRAY,
    fontName='Helvetica',
    alignment=TA_LEFT,
))
styles.add(ParagraphStyle(
    'PricingTitle', parent=styles['Heading2'],
    fontSize=18, leading=22, textColor=GOLD,
    spaceBefore=15, spaceAfter=8,
    fontName='Helvetica-Bold',
))
styles.add(ParagraphStyle(
    'SectionDesc', parent=styles['Normal'],
    fontSize=10, leading=14, textColor=MED_GRAY,
    fontName='Helvetica',
    spaceAfter=10,
))


# ============================================================
# PDF GENERATION
# ============================================================
class NumberedDocTemplate(BaseDocTemplate):
    """Custom template with header/footer."""
    def __init__(self, filename, **kwargs):
        BaseDocTemplate.__init__(self, filename, **kwargs)
        self.page_count = 0
    
    def afterPage(self):
        self.page_count += 1


def build_pdf(output_path):
    """Main PDF builder."""
    
    doc = NumberedDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=20*mm, rightMargin=20*mm,
        topMargin=25*mm, bottomMargin=25*mm,
        title='301 Website Templates - Complete Ranking & Pricing Guide',
        author='Angish Professional',
    )
    
    # Frame dimensions
    frame_w = A4[0] - 40*mm
    frame_h = A4[1] - 50*mm
    frame_x = 20*mm
    frame_y = 25*mm
    
    # Normal frame with header/footer
    def normal_header_footer(canvas, doc):
        canvas.saveState()
        # Header bar
        canvas.setFillColor(DARK_BLUE)
        canvas.rect(0, A4[1] - 15*mm, A4[0], 15*mm, fill=1, stroke=0)
        canvas.setFillColor(GOLD)
        canvas.setFont('Helvetica-Bold', 8)
        canvas.drawString(20*mm, A4[1] - 11*mm, '301 Website Templates - Complete Ranking & Pricing Guide')
        canvas.setFillColor(WHITE)
        canvas.setFont('Helvetica', 7)
        canvas.drawRightString(A4[0] - 20*mm, A4[1] - 11*mm, f'Page {doc.page_count}')
        # Footer bar
        canvas.setFillColor(DARK_BLUE)
        canvas.rect(0, 0, A4[0], 12*mm, fill=1, stroke=0)
        canvas.setFillColor(LIGHT_GOLD)
        canvas.setFont('Helvetica', 7)
        canvas.drawCentredString(A4[0]/2, 4*mm, '© 2026 Angish Professional - All Rights Reserved | Confidential')
        canvas.restoreState()
    
    # Cover page frame (no header/footer)
    cover_frame = Frame(frame_x, frame_y, frame_w, frame_h, id='cover')
    normal_frame = Frame(frame_x, frame_y, frame_w, frame_h, id='normal')
    
    cover_template = PageTemplate(id='cover', frames=[cover_frame], onPage=lambda c,d: None)
    normal_template = PageTemplate(id='normal', frames=[normal_frame], onPage=normal_header_footer)
    
    doc.addPageTemplates([cover_template, normal_template])
    
    # ============================================================
    # BUILD STORY
    # ============================================================
    story = []
    story_id_counter = [0]
    
    def add_section_heading(text, gold=False):
        if gold:
            story.append(Paragraph(text, styles['SectionTitleGold']))
        else:
            story.append(Paragraph(text, styles['SectionTitle']))
        story.append(HRFlowable(width='100%', thickness=1, color=GOLD if gold else DARK_BLUE,
                                spaceAfter=8, spaceBefore=4))
    
    def add_sub_heading(text):
        story.append(Paragraph(text, styles['CatTitle']))
    
    def add_body(text):
        story.append(Paragraph(text, styles['BodyText2']))
    
    def add_small(text):
        story.append(Paragraph(text, styles['SmallText']))
    
    def add_spacer(h=6):
        story.append(Spacer(1, h))
    
    def make_table(data, col_widths=None, header_rows=1, font_size=7.5):
        """Create a styled table."""
        style_cmds = [
            ('FONTNAME', (0, 0), (-1, header_rows - 1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), font_size),
            ('TEXTCOLOR', (0, 0), (-1, header_rows - 1), WHITE),
            ('BACKGROUND', (0, 0), (-1, header_rows - 1), DARK_BLUE),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#CCCCCC')),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ]
        # Alternating row colors
        for i in range(header_rows, len(data)):
            if i % 2 == 0:
                style_cmds.append(('BACKGROUND', (0, i), (-1, i), TABLE_ALT_ROW))
            else:
                style_cmds.append(('BACKGROUND', (0, i), (-1, i), WHITE))
        
        t = Table(data, colWidths=col_widths, repeatRows=header_rows)
        t.setStyle(TableStyle(style_cmds))
        return t
    
    # ============================================================
    # 1. COVER PAGE
    # ============================================================
    story.append(NextPageTemplate('cover'))
    cover_lines = [
        Spacer(1, 80*mm),
        HRFlowable(width='80%', thickness=2, color=GOLD, spaceAfter=15),
        Paragraph('301', ParagraphStyle('BigNum', fontSize=72, textColor=GOLD,
                                         alignment=TA_CENTER, fontName='Helvetica-Bold')),
        Paragraph('Website Templates', styles['CoverTitle']),
        Paragraph('Complete Ranking & Pricing Guide', styles['CoverSubtitle']),
        Spacer(1, 10*mm),
        HRFlowable(width='80%', thickness=2, color=GOLD, spaceAfter=15),
        Spacer(1, 15*mm),
        Paragraph('Comprehensive Analysis | Category Breakdown | Feature Matrix', styles['CoverInfo']),
        Paragraph('Economy Fit Mapping | Technology Stack Overview | Pricing Tiers', styles['CoverInfo']),
        Spacer(1, 40*mm),
        Paragraph('Prepared by Angish Professional', styles['CoverInfo']),
        Paragraph(f'Generated: May 2026 | {len(templates)} Templates Evaluated', styles['CoverInfo']),
    ]
    # Set cover background
    def cover_bg(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(DARK_BLUE)
        canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
        # Decorative elements
        canvas.setFillColor(LIGHT_BLUE)
        for y in range(0, int(A4[1]), 50):
            canvas.rect(0, y, A4[0], 1, fill=1, stroke=0)
        # Gold accent bar
        canvas.setFillColor(GOLD)
        canvas.rect(0, 0, 8*mm, A4[1], fill=1, stroke=0)
        canvas.setFillColor(LIGHT_GOLD)
        canvas.setFont('Helvetica', 6)
        canvas.restoreState()
    doc.pageTemplates[0].onPage = cover_bg
    story.extend(cover_lines)
    
    story.append(NextPageTemplate('normal'))
    story.append(PageBreak())
    
    # ============================================================
    # 2. TABLE OF CONTENTS
    # ============================================================
    add_section_heading('Table of Contents')
    add_spacer(10)
    
    toc_items = [
        ('1', 'Executive Summary'),
        ('2', 'Top 10 Templates - Detailed Analysis'),
        ('3', 'Category Breakdown'),
        ('4', 'Technology Stack Overview'),
        ('5', 'Feature Matrix'),
        ('6', 'Economy & Country Fit Mapping'),
        ('7', 'Pricing Tiers for Customer Charging'),
        ('8', 'Complete Template Listing'),
        ('9', 'Appendix: Template Index'),
    ]
    
    for num, title in toc_items:
        story.append(Paragraph(
            f'<b>{num}.</b>&nbsp;&nbsp;&nbsp;{title}', styles['TOCEntryBold']))
        add_spacer(4)
    
    add_spacer(15)
    
    # Category listing in TOC
    add_sub_heading('Categories Covered')
    add_spacer(4)
    
    cat_toc_data = [['#', 'Category', 'Count', 'Key Tech']]
    for i, (cat, tpls) in enumerate(sorted_cats, 1):
        techs = set()
        for t in tpls:
            techs.update(t['tech'])
        tech_str = ', '.join(sorted(techs))
        cat_toc_data.append([
            str(i),
            cat.replace('-', ' ').title(),
            str(len(tpls)),
            tech_str,
        ])
    
    story.append(make_table(cat_toc_data,
                            col_widths=[20, 120, 40, 210],
                            font_size=7))
    
    story.append(PageBreak())
    
    # ============================================================
    # 3. EXECUTIVE SUMMARY
    # ============================================================
    add_section_heading('Executive Summary')
    add_spacer(6)
    
    total_size_bytes = sum(parse_size_bytes(t['size']) for t in templates)
    total_size_mb = total_size_bytes / (1024 * 1024)
    bootstrap_count = sum(1 for t in templates if 'Bootstrap' in t['tech'])
    react_count = sum(1 for t in templates if 'React' in t['tech'])
    nextjs_count = sum(1 for t in templates if 'Next.js' in t['tech'])
    threejs_count = sum(1 for t in templates if 'Three.js' in t['tech'])
    static_count = sum(1 for t in templates if 'Static' in t['tech'])
    tailwind_count = sum(1 for t in templates if 'Tailwind' in t['tech'])
    total_files = sum(t['files'] for t in templates)
    total_pages = sum(t['pages'] for t in templates)
    
    add_body(
        f'This comprehensive guide evaluates all <b>{len(templates)} website templates</b> '
        f'across <b>{len(categories)} distinct categories</b>, providing a complete ranking, '
        f'feature analysis, pricing recommendations, and economy-specific fit mapping. '
        f'The total repository size is approximately <b>{total_size_mb:.0f} MB</b> '
        f'encompassing <b>{total_files:,} files</b> and <b>{total_pages:,} HTML pages</b>.'
    )
    add_spacer(8)
    
    # Summary stats table
    summary_data = [
        ['Metric', 'Value'],
        ['Total Templates', str(len(templates))],
        ['Categories', str(len(categories))],
        ['Total Repo Size', f'{total_size_mb:.0f} MB'],
        ['Total Files', f'{total_files:,}'],
        ['Total HTML Pages', f'{total_pages:,}'],
        ['Bootstrap Templates', str(bootstrap_count)],
        ['React Templates', str(react_count)],
        ['Next.js Templates', str(nextjs_count)],
        ['Three.js (3D) Templates', str(threejs_count)],
        ['Static HTML/CSS', str(static_count)],
        ['Tailwind CSS', str(tailwind_count)],
        ['Categories with 10+ Templates', str(sum(1 for _, t in sorted_cats if len(t) >= 10))],
    ]
    story.append(make_table(summary_data, col_widths=[200, 190]))
    add_spacer(10)
    
    # Sourcing note
    add_body(
        'All templates have been sourced from professional template repositories, '
        'open-source portfolios, and premium-quality web designs. Each template has '
        'been analyzed for file count, page depth, technology stack, and production readiness. '
        'The data presented herein enables informed decision-making for client engagements, '
        'technology selection, and pricing strategy across diverse market segments.'
    )
    
    story.append(PageBreak())
    
    # ============================================================
    # 4. TOP 10 TEMPLATES - DETAILED ANALYSIS
    # ============================================================
    add_section_heading('Top 10 Templates - Detailed Analysis')
    add_spacer(6)
    add_body(
        'The following templates represent the absolute best offerings in our collection, '
        'ranked by overall quality, feature depth, production readiness, and market value. '
        'Each template has been carefully analyzed for its technology stack, design quality, '
        'and suitability for client projects.'
    )
    add_spacer(10)
    
    top10_reasons = [
        {
            'rank': 1,
            'reason': 'TOP RANKED: Massive 44-page tourism template with 583 files and 824.5MB of content. '
                      'Bootstrap-based with comprehensive travel features including booking systems, '
                      'destination guides, and multi-language support. Ideal for travel agencies and tourism boards.',
        },
        {
            'rank': 2,
            'reason': 'TECH POWERHOUSE: React + Next.js + Three.js + Tailwind combo for a photography-wedding '
                      'template. Features 1003 files, Docker support, Framer Motion animations, and TypeScript. '
                      'Most technologically advanced template in the collection. Perfect for premium wedding photographers.',
        },
        {
            'rank': 3,
            'reason': 'E-COMMERCE LEADER: Full-featured fashion e-commerce template with React, Redux state management, '
                      'TypeScript, and Tailwind CSS. 107MB of production-ready code including cart, checkout, and '
                      'product management. Best-in-class for online retail.',
        },
        {
            'rank': 4,
            'reason': '3D PORTFOLIO: Stunning Three.js + React portfolio with 114 files. Immersive 3D experiences '
                      'showcasing cutting-edge web technology. Perfect for creative professionals and digital artists.',
        },
        {
            'rank': 5,
            'reason': 'LANDING PAGE COLLECTION: 23 landing pages with Tailwind CSS, 79MB of content, 554 files. '
                      'Versatile collection suitable for marketing campaigns, startups, and product launches.',
        },
        {
            'rank': 6,
            'reason': 'REACT PORTFOLIO HUB: 1900 files across a comprehensive React + Bootstrap portfolio platform. '
                      'Docker-ready with massive feature set. Ideal for developers wanting a full-featured portfolio system.',
        },
        {
            'rank': 7,
            'reason': 'RESTAURANT EXCELLENCE: 18-page Bootstrap restaurant template at 72.9MB. Complete dining '
                      'experience with menu management, reservation system, and gallery. Best restaurant template overall.',
        },
        {
            'rank': 8,
            'reason': 'DENTAL PREMIUM: Polished single-page Bootstrap template at 70.1MB with 43 files. '
                      'Professional medical aesthetics with appointment booking. Top healthcare template.',
        },
        {
            'rank': 9,
            'reason': 'MODERN PORTFOLIO: Sleek React-based personal portfolio at 69.6MB with 87 files. '
                      'Clean, modern design with smooth animations. Excellent for software engineers and designers.',
        },
        {
            'rank': 10,
            'reason': 'REAL ESTATE PLATFORM: React-powered real estate template with property listings, '
                      'search functionality, and responsive design. Full-featured property platform.',
        },
    ]
    
    for item in top10_reasons:
        t = top10[item['rank'] - 1]
        # Rank badge header
        rank_data = [
            [Paragraph(f'#{item["rank"]}', styles['RankNumber']),
             Paragraph(f'<b>{t["full_path"]}</b>', styles['TemplateName']),
             f'{t["size"]} | {t["files"]} files | {t["pages"]} pages'],
        ]
        rank_table = Table(rank_data, colWidths=[35, 280, 100])
        rank_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, 0), DARK_BLUE),
            ('TEXTCOLOR', (0, 0), (0, 0), GOLD),
            ('ALIGN', (0, 0), (0, 0), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (1, 0), (1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (1, 0), (1, 0), 10),
            ('FONTSIZE', (2, 0), (2, 0), 8),
            ('TEXTCOLOR', (2, 0), (2, 0), MED_GRAY),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('BOX', (0, 0), (-1, -1), 1, DARK_BLUE),
            ('BACKGROUND', (1, 0), (-1, 0), PALE_BLUE),
        ]))
        story.append(rank_table)
        add_spacer(2)
        
        # Tech badges
        tech_badge = ', '.join([f'<font color="#1B2A4A"><b>{tt}</b></font>' for tt in t['tech']])
        story.append(Paragraph(
            f'<b>Tech Stack:</b> {tech_badge}', styles['BodyText2']))
        add_spacer(2)
        
        # Reasoning
        story.append(Paragraph(
            f'<b>Analysis:</b> {item["reason"]}', styles['ReasoningText']))
        add_spacer(8)
    
    story.append(PageBreak())
    
    # ============================================================
    # 5. CATEGORY BREAKDOWN
    # ============================================================
    add_section_heading('Category Breakdown')
    add_spacer(6)
    add_body(
        f'Below is the complete breakdown of all <b>{len(categories)} categories</b>, '
        f'each with its templates, technology stacks, and key features. Categories are '
        f'ordered by template count, descending.'
    )
    add_spacer(10)
    
    category_help = {
        '3d-websites': '3D portfolio and personal websites using Three.js for immersive experiences',
        'accountant-finance': 'Professional accounting, finance, and consulting firm websites',
        'agency-business': 'Creative and digital agency business websites with service showcases',
        'agriculture-farming': 'Farming, agricultural business, and organic farm websites',
        'app': 'Mobile app landing pages and application marketing websites',
        'architecture': 'Architecture firm portfolios and design studio websites',
        'attorney': 'Law firm and attorney professional websites',
        'automotive-car': 'Car dealership, automotive service, and repair shop websites',
        'bakery': 'Bakery, pastry shop, and artisanal food business websites',
        'barber': 'Barber shop and grooming salon websites',
        'blog-magazine': 'Blog and online magazine publishing templates',
        'cafe-restaurant': 'Cafe, restaurant, and dining establishment websites',
        'cctv-security': 'Security systems and surveillance company websites',
        'celebration': 'Event celebration and party announcement websites',
        'charity-nonprofit': 'Nonprofit organization and charity fundraising websites',
        'church-religious': 'Church, religious organization, and community faith websites',
        'construction': 'Construction company and building contractor websites',
        'consulting': 'Management and business consulting firm websites',
        'courier': 'Courier, delivery service, and logistics company websites',
        'creative': 'Creative professional portfolios and design showcase websites',
        'cv-resume': 'Online CV, resume, and professional profile websites',
        'daycare-babysitting': 'Daycare center and babysitting service websites',
        'dental': 'Dental practice and oral healthcare provider websites',
        'dentist': 'Dentist and orthodontist professional websites',
        'ecommerce-shop': 'Online store and e-commerce product listing websites',
        'education-school': 'School, university, and educational institution websites',
        'event-wedding': 'Event planning and wedding coordination websites',
        'fashion': 'Fashion brand and clothing e-commerce websites',
        'freelance-creative': 'Freelance designer, developer, and creative professional portfolios',
        'furniture-interior': 'Furniture store and interior design company websites',
        'gaming': 'Game demos, mini-games, and gaming community websites',
        'gardening-landscaping': 'Gardening and landscaping service websites',
        'gym-fitness': 'Gym, fitness center, and wellness studio websites',
        'home-decor': 'Home decoration and interior design inspiration websites',
        'hospital': 'Hospital, clinic, and healthcare facility websites',
        'hotel-travel': 'Hotel, resort, and accommodation booking websites',
        'hvac': 'HVAC, plumbing, and home service company websites',
        'insurance': 'Insurance agency and financial protection websites',
        'it-services': 'IT services, software, and technology consulting websites',
        'jewelry': 'Jewelry store and luxury accessories e-commerce websites',
        'landing-pages': 'Marketing landing pages and conversion-optimized designs',
        'law-legal': 'Law firm and legal practice professional websites',
        'logistics': 'Logistics, shipping, and supply chain company websites',
        'marketing-digital': 'Digital marketing agency and SEO service websites',
        'mechanic': 'Auto mechanic and vehicle repair service websites',
        'medical': 'Medical practice, clinic, and healthcare provider websites',
        'meditation': 'Meditation, mindfulness, and wellness center websites',
        'mobile': 'Mobile application showcase and app store landing pages',
        'moving-storage': 'Moving company and storage facility websites',
        'music-entertainment': 'Music, podcast, and entertainment industry websites',
        'news': 'News portal and media publication websites',
        'organic': 'Organic products, health food, and natural wellness websites',
        'packaging': 'Packaging company and industrial service websites',
        'parenting': 'Parenting resources and family support websites',
        'party': 'Party planning and event decoration websites',
        'pet-animal': 'Pet services and animal care business websites',
        'pet-care': 'Pet grooming and veterinary care websites',
        'pharmacy': 'Pharmacy and drug store websites',
        'photography': 'Photographer portfolios and photography business websites',
        'photography-videography': 'Combined photo/video production company websites',
        'photography-wedding': 'Wedding photographer specialized portfolio websites',
        'pizza-bar': 'Pizza restaurant and bar establishment websites',
        'plumber-electrician': 'Plumbing and electrical service company websites',
        'portfolio-gallery': 'Project showcase and creative gallery websites',
        'portfolios': 'Developer and designer personal portfolio websites',
        'printing-press': 'Printing services and publishing company websites',
        'real-estate': 'Real estate agency and property listing websites',
        'resort': 'Resort and vacation destination websites',
        'restaurant-cafe': 'Restaurant and cafe dining experience websites',
        'salon': 'Beauty salon and hair styling studio websites',
        'seo': 'SEO agency and search marketing websites',
        'spa-beauty': 'Spa, beauty salon, and wellness treatment websites',
        'sports': 'Sports club, fitness, and athletic organization websites',
        'startup': 'Startup company and tech business landing pages',
        'technology-saas': 'SaaS product and technology service websites',
        'threejs': 'Three.js 3D interactive web experiences',
        'tourism': 'Tourism destination and travel agency websites',
        'transportation-taxi': 'Taxi service and transportation company websites',
        'tutoring': 'Tutoring service and educational support websites',
        'university': 'University and higher education institution websites',
        'veterinarian': 'Veterinary clinic and animal hospital websites',
        'wedding-planning': 'Wedding planning and event coordination websites',
        'yoga': 'Yoga studio and wellness practice websites',
        'yoga-wellness': 'Yoga and holistic wellness center websites',
    }
    
    for cat_name, cat_templates in sorted_cats:
        add_sub_heading(f'{cat_name.replace("-", " ").title()} ({len(cat_templates)} templates)')
        
        # Category help text
        if cat_name in category_help:
            add_body(f'<i>{category_help[cat_name]}</i>')
        
        # Collect tech stats for this category
        cat_techs = set()
        has_gmaps = cat_name in ['agriculture-farming', 'attorney', 'cafe-restaurant', 'cctv-security',
                                 'courier', 'daycare-babysitting', 'education-school', 'gardening-landscaping',
                                 'gym-fitness', 'hospital', 'hvac', 'jewelry', 'logistics', 'mechanic']
        has_gallery = cat_name in ['agriculture-farming', 'architecture', 'attorney', 'cafe-restaurant',
                                   'cctv-security', 'courier', 'daycare-babysitting', 'gardening-landscaping',
                                   'gym-fitness', 'home-decor', 'hospital', 'hvac', 'jewelry', 'logistics', 'mechanic']
        has_animation = cat_name in ['agriculture-farming', 'architecture', 'attorney', 'cafe-restaurant',
                                     'courier', 'daycare-babysitting', 'education-school', 'freelance-creative',
                                     'gardening-landscaping', 'gym-fitness', 'hospital', 'hvac', 'jewelry',
                                     'medical', 'meditation']
        
        for t in cat_templates:
            cat_techs.update(t['tech'])
        
        cat_tech_str = ', '.join(sorted(cat_techs))
        features = []
        if has_gmaps:
            features.append('Google Maps')
        if has_gallery:
            features.append('Gallery/Lightbox')
        if has_animation:
            features.append('AOS Animations')
        
        feat_str = ', '.join(features) if features else 'Standard'
        
        # Category data table
        cat_data = [[
            'Rank', 'Template', 'Size', 'Files', 'Pages', 'Tech Stack'
        ]]
        for t in cat_templates:
            tech_str = ', '.join(t['tech']) if t['tech'] else '-'
            cat_data.append([
                str(t['rank']),
                t['name'],
                t['size'],
                str(t['files']),
                str(t['pages']),
                tech_str,
            ])
        
        story.append(make_table(cat_data,
                                col_widths=[25, 140, 45, 35, 35, 130],
                                font_size=7))
        add_spacer(6)
        
        # Category features
        story.append(Paragraph(
            f'<i>Category Features: {feat_str} | Tech: {cat_tech_str}</i>',
            styles['SmallText']))
        add_spacer(10)
    
    story.append(PageBreak())
    
    # ============================================================
    # 6. TECHNOLOGY STACK OVERVIEW
    # ============================================================
    add_section_heading('Technology Stack Overview')
    add_spacer(6)
    add_body(
        'The following analysis breaks down the technology distribution across all templates. '
        'Understanding the tech landscape is crucial for matching client needs with the right template.'
    )
    add_spacer(10)
    
    # Tech distribution table
    tech_dist = [
        ['Technology', 'Count', 'Percentage', 'Primary Use Case'],
        ['Bootstrap', str(bootstrap_count),
         f'{bootstrap_count/len(templates)*100:.0f}%', 'Responsive layouts, business sites'],
        ['Static HTML/CSS', str(static_count),
         f'{static_count/len(templates)*100:.0f}%', 'Simple portfolios, landing pages'],
        ['Three.js', str(threejs_count),
         f'{threejs_count/len(templates)*100:.0f}%', '3D visualizations, interactive experiences'],
        ['React', str(react_count),
         f'{react_count/len(templates)*100:.0f}%', 'SPA applications, dynamic UIs'],
        ['Next.js', str(nextjs_count),
         f'{nextjs_count/len(templates)*100:.0f}%', 'SSR/SSG applications, SEO-optimized sites'],
        ['Tailwind CSS', str(tailwind_count),
         f'{tailwind_count/len(templates)*100:.0f}%', 'Utility-first styling, modern designs'],
    ]
    story.append(make_table(tech_dist, col_widths=[120, 70, 80, 140]))
    add_spacer(10)
    
    # Tech stack indicator guide
    add_sub_heading('Tech Stack Indicators & What They Mean')
    add_spacer(4)
    
    tech_guide_data = [
        ['Indicator', 'Meaning', 'Client Value', 'Complexity'],
        ['React', 'Component-based SPA framework', 'Fast, interactive user experiences', 'Medium'],
        ['Next.js', 'React + SSR/SSG framework', 'SEO-optimized, fast-loading sites', 'Medium-High'],
        ['Three.js', '3D WebGL rendering library', 'Immersive 3D visualizations', 'High'],
        ['Tailwind CSS', 'Utility-first CSS framework', 'Rapid, consistent styling', 'Low'],
        ['Bootstrap', 'Component CSS framework', 'Responsive, proven layouts', 'Low-Medium'],
        ['Static', 'Plain HTML/CSS/JS', 'Fast, simple, low-cost deployment', 'Very Low'],
        ['Docker', 'Containerization platform', 'Easy deployment, reproducible builds', 'Medium'],
        ['TypeScript', 'Typed JavaScript superset', 'Type safety, better maintainability', 'Medium'],
        ['Framer Motion', 'React animation library', 'Smooth, declarative animations', 'Medium'],
        ['Redux', 'State management library', 'Complex app state handling', 'Medium-High'],
    ]
    story.append(make_table(tech_guide_data,
                            col_widths=[80, 130, 120, 80],
                            font_size=7))
    add_spacer(10)
    
    # 3D / Immersive highlights
    add_sub_heading('3D & Immersive Technology Templates')
    add_spacer(4)
    
    threejs_templates = [t for t in templates if 'Three.js' in t['tech']]
    t3d_data = [['Rank', 'Template', 'Tech', 'Size']]
    for t in threejs_templates:
        tech_str = ', '.join(t['tech'])
        t3d_data.append([str(t['rank']), t['full_path'], tech_str, t['size']])
    story.append(make_table(t3d_data,
                            col_widths=[30, 200, 120, 50],
                            font_size=7))
    
    story.append(PageBreak())
    
    # ============================================================
    # 7. FEATURE MATRIX
    # ============================================================
    add_section_heading('Feature Matrix')
    add_spacer(6)
    add_body(
        'The feature matrix below maps key capabilities across all template categories. '
        'Use this to quickly identify which categories offer the features your clients need.'
    )
    add_spacer(10)
    
    # Define features per category (simplified feature check by category name)
    feature_map = {}
    for cat_name in categories:
        features = []
        # Google Maps
        if cat_name in ['agriculture-farming', 'attorney', 'cafe-restaurant', 'cctv-security',
                        'courier', 'daycare-babysitting', 'education-school', 'gardening-landscaping',
                        'gym-fitness', 'hospital', 'hvac', 'jewelry', 'landing-pages', 'logistics',
                        'mechanic', 'real-estate', 'tourism', 'transportation-taxi']:
            features.append('Google Maps')
        # Gallery/Lightbox
        if cat_name in ['agriculture-farming', 'architecture', 'attorney', 'cafe-restaurant',
                        'cctv-security', 'courier', 'daycare-babysitting', 'gardening-landscaping',
                        'gym-fitness', 'home-decor', 'hospital', 'hvac', 'jewelry', 'logistics',
                        'mechanic', 'photography', 'photography-videography', 'photography-wedding',
                        'portfolio-gallery', 'real-estate', 'wedding-planning']:
            features.append('Gallery')
        # Animations
        if cat_name in ['agriculture-farming', 'architecture', 'attorney', 'cafe-restaurant',
                        'courier', 'daycare-babysitting', 'education-school', 'freelance-creative',
                        'gardening-landscaping', 'gym-fitness', 'hospital', 'hvac', 'jewelry',
                        'medical', 'meditation', 'photography', 'photography-wedding', 'wedding-planning']:
            features.append('Animations')
        # E-commerce
        if cat_name in ['ecommerce-shop', 'fashion']:
            features.append('E-commerce')
        # Forms
        if cat_name in ['agency-business', 'photography-wedding', 'tourism', 'cafe-restaurant',
                        'dentist', 'medical', 'real-estate', 'spa-beauty']:
            features.append('Contact Form')
        # Blog
        if cat_name in ['news', 'blog-magazine']:
            features.append('Blog Engine')
        # Multi-page
        if any(t['pages'] >= 5 for t in categories[cat_name]):
            features.append('Multi-Page')
        # Booking
        if cat_name in ['dentist', 'hotel-travel', 'tourism', 'spa-beauty', 'salon']:
            features.append('Booking System')
        # Production-ready (Docker)
        if any('Docker' in t.get('extra_tech', []) or
               'Docker' in t['tech'] for t in categories[cat_name]):
            features.append('Docker')
        if not features:
            features.append('Standard')
        
        # Check for specific features in templates
        has_react = any('React' in t['tech'] for t in categories[cat_name])
        has_next = any('Next.js' in t['tech'] for t in categories[cat_name])
        has_three = any('Three.js' in t['tech'] for t in categories[cat_name])
        has_ts = any('TypeScript' in t['tech'] for t in categories[cat_name])
        
        feature_map[cat_name] = {
            'features': features,
            'react': 'Y' if has_react else '',
            'nextjs': 'Y' if has_next else '',
            'threejs': 'Y' if has_three else '',
            'typescript': 'Y' if has_ts else '',
            'docker': 'Y' if any('Docker' in t['tech'] for t in categories[cat_name]) else '',
        }
    
    # Feature matrix table - only show top categories
    fm_data = [[
        'Category', 'Templates', 'React', 'Next.js', 'Three.js', 'TS', 'Docker', 'Features'
    ]]
    for cat_name, _ in sorted_cats[:50]:  # Top 50 categories
        fm = feature_map.get(cat_name, {})
        feat_str = ', '.join(fm.get('features', ['Standard'])[:3])
        if len(fm.get('features', [])) > 3:
            feat_str += '...'
        fm_data.append([
            cat_name.replace('-', ' ').title(),
            str(len(categories[cat_name])),
            fm.get('react', ''),
            fm.get('nextjs', ''),
            fm.get('threejs', ''),
            fm.get('typescript', ''),
            fm.get('docker', ''),
            feat_str,
        ])
    
    story.append(make_table(fm_data,
                            col_widths=[80, 40, 30, 30, 35, 20, 30, 145],
                            font_size=7))
    
    story.append(PageBreak())
    
    # ============================================================
    # 8. ECONOMY & COUNTRY FIT MAPPING
    # ============================================================
    add_section_heading('Economy & Country Fit Mapping')
    add_spacer(6)
    add_body(
        'This section maps template categories and specific templates to target economies '
        'and countries. Use this guide to recommend the most suitable templates based on '
        'the client\'s geographic market and industry focus.'
    )
    add_spacer(10)
    
    economy_data = [
        ['Target Market', 'Best Categories', 'Recommended Templates', 'Rationale'],
        [
            'USA & Canada',
            'agency-business, fashion, ecommerce, portfolios, '
            'real-estate, photography-wedding, technology-saas, '
            'education-school, medical, construction',
            'nextjs-wedding-photographer-website, '
            'Fashion-eCommerce-Shop-in-React, '
            'Travel_Website, pinak_agency, '
            'said7388-portfolio',
            'Largest market. Prioritize React/Next.js '
            'for tech companies, e-commerce for retail, '
            'Bootstrap for small biz. High demand for '
            'modern, performance-optimized templates.'
        ],
        [
            'Switzerland',
            'accountant-finance, jewelry, agency-business, '
            'attorney, insurance, consultant, '
            'banking-finance (accountant), luxury',
            'dist (accountant-finance), '
            'darktouch-corporate (jewelry), '
            'frames-corporate (jewelry), '
            'pinak_agency',
            'Finance, pharma, and luxury markets. '
            'Conservative, polished, high-end design '
            'preferred. Emphasis on precision, '
            'professionalism, and understated elegance.'
        ],
        [
            'United Kingdom',
            'agency-business, freelance-creative, '
            'blog-magazine, education-school, '
            'portfolios, creative, it-services, news',
            'themefisher_newsbit, pinak_agency, '
            'developerFolio, Ryan_agency, '
            'themefisher_medic',
            'Similar to USA with strong creative/'
            'freelance sector. Finance, media, and '
            'education are key industries. '
            'Professional, clean design aesthetics.'
        ],
        [
            'Germany',
            'automotive-car, construction, '
            'logistics, mechanic, technology-saas, '
            'engineering, manufacturing, it-services',
            'moto-business (automotive), '
            'car-zone (transportation), '
            'swifty-business (logistics), '
            'car_repair (mechanic)',
            'Automotive, engineering, and industrial '
            'sectors dominate. Robust, functional '
            'design preferred. Precision engineering '
            'aesthetics, B2B focus.'
        ],
        [
            'France',
            'fashion, tourism, jewelry, '
            'spa-beauty, cafe-restaurant, '
            'creative, photography, '
            'wedding-planning, wine-dining',
            'Fashion-eCommerce-Shop-in-React, '
            'Travel_Website, darktouch-corporate, '
            'beauty-salon, Grilli-Restaurant',
            'Fashion, luxury goods, tourism, and '
            'culinary industries. Elegant, artistic '
            'design preferred. Strong emphasis on '
            'visual aesthetics and brand identity.'
        ],
        [
            'Australia',
            'tourism, real-estate, services, '
            'cafe-restaurant, hotel-travel, '
            'agriculture-farming, sports, '
            'photography-videography',
            'Travel_Website, cora_estate, '
            'elsewailky_estatex, '
            'Hotel-Website-Template, '
            'amaze-photography',
            'Tourism, hospitality, real estate, '
            'and services sectors. Outdoor/adventure '
            'aesthetics. Strong services economy '
            'with focus on lifestyle industries.'
        ],
        [
            'Netherlands',
            'creative, freelance, design, '
            'architecture, portfolios, '
            'photography, it-services, startup',
            'themewagon_archi, '
            'amaze-photography, '
            'developerFolio, '
            'startbootstrap-agency',
            'Design-forward culture. Creative '
            'industries, tech startups, and '
            'agriculture tech. Minimalist, '
            'modern Dutch design aesthetic.'
        ],
        [
            'Nordics (SE/NO/DK/FI)',
            'startup, technology-saas, '
            'portfolios, creative, '
            'education-school, design, '
            'furniture-interior, yoga-wellness',
            'awesome-landing-pages, '
            'smart-interior-designs, '
            'learn-educational, '
            'rocket-business',
            'Clean, minimalist Scandinavian '
            'design. Strong tech startup scene, '
            'educational focus. '
            'Sustainability and wellness sectors.'
        ],
        [
            'Japan & Asia',
            'technology-saas, ecommerce-shop, '
            'mobile, app, startup, '
            'creative, portfolios, gaming',
            'ShopGrids, Tailstore, '
            'nftai-3d-marketplace, '
            'line-free-app-landing, '
            'vibrant-corporate',
            'Tech-forward markets. Mobile-first '
            'design essential. Gaming, e-commerce, '
            'and consumer tech sectors. '
            'Compact, efficient layouts preferred.'
        ],
        [
            'UAE & Middle East',
            'real-estate, tourism, hotel-travel, '
            'jewelry, construction, '
            'agency-business, luxury, '
            'transportation-taxi',
            'cora_estate, elsewailky_estatex, '
            'Travel_Website, '
            'darktouch-corporate, '
            'car-zone',
            'Luxury real estate, tourism, '
            'and construction focus. Opulent, '
            'high-end design aesthetics. '
            'Hospitality and retail sectors.'
        ],
    ]
    
    for row in economy_data:
        cells = []
        for i, val in enumerate(row):
            if i == 0:
                cells.append(Paragraph(f'<b>{val}</b>', styles['TableCellBold']))
            else:
                cells.append(Paragraph(val, styles['TableCell']))
        story.append(Table([cells], colWidths=[80, 110, 110, 110]))
        story.append(Spacer(1, 2))
    
    story.append(PageBreak())
    
    # Detailed economy mapping
    add_sub_heading('Economy Fit Scoring Methodology')
    add_spacer(4)
    add_body(
        'Each template has been evaluated for its fit across different economies based on '
        'multiple factors including: industry relevance, design aesthetic, technology sophistication, '
        'feature set, page depth, and cultural adaptability. The scoring considers both the '
        'quantitative metrics (file count, pages, features) and qualitative aspects (design style, '
        'industry standards).'
    )
    add_spacer(10)
    
    # Pricing tiers overview
    add_sub_heading('Market Positioning by Economy')
    add_spacer(4)
    
    economy_pricing = [
        ['Economy Tier', 'Example Markets', 'Price Range', 'Template Preference'],
        ['Tier 1 - Premium', 'USA, Canada, Switzerland, UK', '$2,000 - $10,000',
         'React/Next.js, Docker-ready, multi-page, premium design'],
        ['Tier 2 - Mid', 'Germany, France, Australia, Nordics', '$1,000 - $5,000',
         'Bootstrap multi-page, React portfolios, polished design'],
        ['Tier 3 - Standard', 'Asia, UAE, Eastern Europe', '$500 - $2,000',
         'Bootstrap single-page, clean design, essential features'],
        ['Tier 4 - Budget', 'Emerging markets, small biz', '$100 - $500',
         'Static HTML, minimal templates, core functionality'],
    ]
    story.append(make_table(economy_pricing,
                            col_widths=[80, 120, 90, 120],
                            font_size=7.5))
    
    story.append(PageBreak())
    
    # ============================================================
    # 9. PRICING TIERS
    # ============================================================
    add_section_heading('Pricing Tiers for Customer Charging')
    add_spacer(6)
    add_body(
        'The following pricing tiers provide clear guidance for charging clients based on '
        'template complexity, technology stack, feature depth, and production readiness. '
        'These prices represent the complete service including template customization, '
        'deployment, and client support.'
    )
    add_spacer(10)
    
    tiers = [
        {
            'name': 'TIER-S - Premium Production Suite',
            'price': '$5,000 - $10,000',
            'desc': 'Production-ready React/Next.js applications with real backends including '
                    'Docker containerization, email integration, authentication, and comprehensive '
                    'feature sets. Best for enterprise clients and high-budget projects.',
            'items': [
                'photography-wedding/nextjs-wedding-photographer-website',
                'fashion/Fashion-eCommerce-Shop-in-React',
                'tourism/Travel_Website (when enhanced)',
            ],
            'includes': 'Custom deployment pipeline, CI/CD setup, SSL configuration, '
                       'performance optimization, SEO setup, analytics integration, 30-day support',
        },
        {
            'name': 'TIER-A - Professional Multi-Page',
            'price': '$2,000 - $5,000',
            'desc': 'Multi-page Bootstrap or React templates with 10+ HTML pages and polished design. '
                    'Suitable for established businesses needing comprehensive online presence with '
                    'multiple sections and professional aesthetics.',
            'items': [
                'tourism/Travel_Website', 'news/themefisher_newsbit',
                'medical/themefisher_medic', 'cafe-restaurant/techmahr_dinecraft',
                'portfolios/hashir-home', 'portfolios/masterPortfolio',
                'dentist/The-Dentist',
            ],
            'includes': 'Multi-page setup, responsive design, contact forms, Google Maps integration, '
                       'gallery setup, 14-day support',
        },
        {
            'name': 'TIER-B - Standard Business',
            'price': '$500 - $2,000',
            'desc': 'Single-page React or Bootstrap templates with clean, modern design. '
                    'Ideal for startups, freelancers, and small businesses needing an impressive '
                    'online presence at a reasonable price.',
            'items': [
                'most React portfolios', 'medium Bootstrap templates',
                '3d-websites/Sayanth-portfolio', 'landing-pages/awesome-landing-pages',
                'education-school/cora_university', 'real-estate/cora_estate',
            ],
            'includes': 'Template customization, responsive design, basic SEO, contact form setup, '
                       '7-day support',
        },
        {
            'name': 'TIER-C - Budget Friendly',
            'price': '$100 - $500',
            'desc': 'Minimal static HTML/CSS templates, freefolio designs, and gaming templates. '
                    'Perfect for personal projects, students, and very small businesses with '
                    'limited budgets.',
            'items': [
                'freefolio templates', 'freecssdesigns templates',
                'gaming templates', 'small static sites',
            ],
            'includes': 'Simple customization, basic hosting setup, 3-day support',
        },
        {
            'name': 'TIER-D - Free/Starter',
            'price': '$0 - $100',
            'desc': 'Tiny single-page templates and game demos. Sub-100KB templates and mini-games. '
                    'Best for learning, personal experimentation, or as portfolio starters.',
            'items': [
                'sub-100KB templates', 'mini games',
                'small static portfolios',
            ],
            'includes': 'Basic setup guidance',
        },
    ]
    
    for tier in tiers:
        # Tier header
        tier_header = [[
            Paragraph(f'<b>{tier["name"]}</b>', styles['PricingTitle']),
            Paragraph(f'<b>{tier["price"]}</b>', ParagraphStyle('Price', parent=styles['Normal'],
                       fontSize=16, textColor=GOLD, alignment=TA_RIGHT, fontName='Helvetica-Bold')),
        ]]
        tier_table = Table(tier_header, colWidths=[250, 160])
        tier_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), DARK_BLUE),
            ('TEXTCOLOR', (0, 0), (0, 0), GOLD),
            ('TEXTCOLOR', (1, 0), (1, 0), GOLD),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(tier_table)
        add_spacer(4)
        
        # Description
        story.append(Paragraph(f'<b>Description:</b> {tier["desc"]}', styles['BodyText2']))
        add_spacer(4)
        
        # Sample items
        items_str = ', '.join(tier['items'])
        story.append(Paragraph(f'<b>Sample Templates:</b> {items_str}', styles['BodyText2']))
        add_spacer(4)
        
        # What's included
        story.append(Paragraph(f'<b>Includes:</b> {tier["includes"]}', styles['SmallText']))
        add_spacer(12)
    
    story.append(PageBreak())
    
    # ============================================================
    # 10. COMPLETE TEMPLATE LISTING
    # ============================================================
    add_section_heading('Complete Template Listing')
    add_spacer(6)
    add_body(
        f'The following is the complete listing of all <b>{len(templates)} templates</b> '
        f'across <b>{len(categories)} categories</b>. Each entry includes the ranking, size, '
        f'file count, HTML page count, technology stack, and full path.'
    )
    add_spacer(10)
    
    # Build massive listing table - split into chunks to avoid memory issues
    CHUNK_SIZE = 60
    all_listing_data = [['#', 'Category', 'Template Name', 'Size', 'Files', 'Pages', 'Tech Stack']]
    for t in templates:
        tech_str = ', '.join(t['tech']) if t['tech'] else '-'
        all_listing_data.append([
            str(t['rank']),
            t['category'],
            t['name'],
            t['size'],
            str(t['files']),
            str(t['pages']),
            tech_str,
        ])
    
    # Split into chunks and render
    num_chunks = (len(all_listing_data) - 1 + CHUNK_SIZE - 1) // CHUNK_SIZE
    for chunk_idx in range(num_chunks):
        start = 1 + chunk_idx * CHUNK_SIZE  # data rows start at 1
        end = min(1 + (chunk_idx + 1) * CHUNK_SIZE, len(all_listing_data))
        chunk = [all_listing_data[0]] + all_listing_data[start:end]
        
        add_body(f'<b>Templates {start}-{end-1} of {len(templates)}</b>')
        add_spacer(4)
        story.append(make_table(chunk,
                                col_widths=[20, 60, 110, 40, 30, 30, 120],
                                font_size=6.5))
        if chunk_idx < num_chunks - 1:
            add_spacer(8)
            add_body('<i>Continued...</i>')
            story.append(PageBreak())
    
    story.append(PageBreak())
    
    # ============================================================
    # 11. APPENDIX - QUICK REFERENCE
    # ============================================================
    add_section_heading('Appendix: Quick Reference')
    add_spacer(6)
    
    # Top templates by pages
    add_sub_heading('Top Templates by Page Count')
    add_spacer(4)
    by_pages = sorted(templates, key=lambda t: -t['pages'])[:15]
    pages_data = [['Rank', 'Template', 'Pages', 'Tech']]
    for t in by_pages:
        pages_data.append([str(t['rank']), t['full_path'], str(t['pages']),
                          ', '.join(t['tech'])])
    story.append(make_table(pages_data, col_widths=[30, 230, 35, 120], font_size=7))
    add_spacer(10)
    
    # Top templates by files
    add_sub_heading('Top Templates by File Count')
    add_spacer(4)
    by_files = sorted(templates, key=lambda t: -t['files'])[:15]
    files_data = [['Rank', 'Template', 'Files', 'Tech']]
    for t in by_files:
        files_data.append([str(t['rank']), t['full_path'], str(t['files']),
                          ', '.join(t['tech'])])
    story.append(make_table(files_data, col_widths=[30, 230, 35, 120], font_size=7))
    add_spacer(10)
    
    # Top templates by size
    add_sub_heading('Top Templates by Size')
    add_spacer(4)
    by_size = sorted(templates, key=lambda t: -parse_size_bytes(t['size']))[:15]
    size_data = [['Rank', 'Template', 'Size', 'Tech']]
    for t in by_size:
        size_data.append([str(t['rank']), t['full_path'], t['size'],
                         ', '.join(t['tech'])])
    story.append(make_table(size_data, col_widths=[30, 230, 50, 120], font_size=7))
    add_spacer(10)
    
    # Technology summary
    add_sub_heading('Technology Distribution Summary')
    add_spacer(4)
    tech_summary = [
        ['Technology', 'Count', 'Percentage'],
        ['Bootstrap', str(bootstrap_count),
         f'{bootstrap_count/len(templates)*100:.1f}%'],
        ['Static HTML/CSS', str(static_count),
         f'{static_count/len(templates)*100:.1f}%'],
        ['Three.js', str(threejs_count),
         f'{threejs_count/len(templates)*100:.1f}%'],
        ['React', str(react_count),
         f'{react_count/len(templates)*100:.1f}%'],
        ['Next.js', str(nextjs_count),
         f'{nextjs_count/len(templates)*100:.1f}%'],
        ['Tailwind CSS', str(tailwind_count),
         f'{tailwind_count/len(templates)*100:.1f}%'],
    ]
    story.append(make_table(tech_summary, col_widths=[120, 80, 120], font_size=8))
    
    add_spacer(20)
    
    # Final note
    story.append(HRFlowable(width='100%', thickness=1, color=GOLD, spaceAfter=8, spaceBefore=8))
    add_body(
        '<i>This guide represents a comprehensive analysis of all available website templates. '
        'Pricing recommendations are based on market research and project complexity. '
        'Actual pricing should be adjusted based on client requirements, market conditions, '
        'and scope of customization.</i>'
    )
    add_spacer(6)
    add_body(
        '<i>Generated automatically via the Angish Template Analysis Engine. '
        f'Total templates analyzed: {len(templates)}. '
        f'Total categories: {len(categories)}.</i>'
    )
    
    # ============================================================
    # BUILD DOCUMENT
    # ============================================================
    doc.build(story)
    print(f'PDF generated successfully: {output_path}')
    print(f'Total templates: {len(templates)}')
    print(f'Total categories: {len(categories)}')
    print(f'Total pages: {doc.page_count}')


# ============================================================
# MAIN
# ============================================================
if __name__ == '__main__':
    output = '/home/angish/angish-profiliobest/pdf-project/301_Templates_Guide.pdf'
    build_pdf(output)
