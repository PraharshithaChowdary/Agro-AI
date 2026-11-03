"""
AGRO AI — Training Datasets Specification & Documentation PDF Generator
Generates a comprehensive, publication-quality PDF document covering:
1. Executive Summary & Machine Learning Architecture
2. Inventory of all 4 Training Datasets (CSV metrics, distributions, sample counts)
3. Underlying Benchmark Sources & Open Licenses (PlantVillage, PlantDoc, Kaggle Soil, ICAR, COCO)
4. Full Class-by-Class Breakdowns (Foliar Diseases, Indian Plant Species, Soil Categories, Relevance)
5. 48-Dimensional Feature Engineering Specification & Mathematical Formulations
6. 10,208 Indian Botanical Species Catalog Schema
7. Multimodal Vision-Language Model (Qwen 2.5-VL 3B) Overview
8. File Locations & Download Guide
"""

import os
import sys
import shutil
from pathlib import Path
from datetime import datetime

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and draw total page count
    along with running header and footer.
    """
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#4b5563"))

        # Do not draw running header on cover page (page 1)
        if self._pageNumber > 1:
            # Running Header
            self.drawString(54, 11 * inch - 36, "AGRO AI — Machine Learning Training Datasets Specification")
            self.drawRightString(8.5 * inch - 54, 11 * inch - 36, "Confidential & Technical Documentation")
            self.setStrokeColor(colors.HexColor("#d1d5db"))
            self.setLineWidth(0.5)
            self.line(54, 11 * inch - 42, 8.5 * inch - 54, 11 * inch - 42)

        # Running Footer (on all pages)
        self.setStrokeColor(colors.HexColor("#d1d5db"))
        self.setLineWidth(0.5)
        self.line(54, 46, 8.5 * inch - 54, 46)

        self.drawString(54, 32, "AGRO AI Platform • Smart Agriculture. Healthy Lives. Better Future.")
        self.drawRightString(8.5 * inch - 54, 32, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()


def build_pdf(output_path: str):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom Palette
    c_primary = colors.HexColor("#1b4332")     # Deep Forest Green
    c_secondary = colors.HexColor("#2d6a4f")   # Emerald
    c_accent = colors.HexColor("#40916c")      # Foliage Green
    c_dark = colors.HexColor("#111827")        # Dark Slate
    c_muted = colors.HexColor("#4b5563")       # Cool Gray
    c_bg_light = colors.HexColor("#f8fafc")    # Off-white / light slate
    c_border = colors.HexColor("#e2e8f0")

    # Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=c_primary,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=c_secondary,
        spaceAfter=14
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=c_primary,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=c_secondary,
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=c_dark,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=c_dark,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=3
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white,
        alignment=0
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=c_dark
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=c_dark
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#0f172a"),
        backColor=colors.HexColor("#f1f5f9"),
        borderColor=colors.HexColor("#cbd5e1"),
        borderWidth=0.5,
        borderPadding=4,
        spaceAfter=5
    )

    callout_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#1e3a8a")
    )

    story = []

    # =========================================================================
    # COVER / HEADER BLOCK
    # =========================================================================
    story.append(Paragraph("AGRO AI — Training Datasets Specification", title_style))
    story.append(Paragraph("Complete Technical Documentation of Machine Learning & Computer Vision Datasets", subtitle_style))
    story.append(Paragraph(f"<b>Platform:</b> AGRO AI (Qwen & Ollama Hybrid) &nbsp;&bull;&nbsp; <b>Date:</b> {datetime.now().strftime('%B %d, %Y')} &nbsp;&bull;&nbsp; <b>Status:</b> Production Verified", body_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_accent, spaceBefore=4, spaceAfter=12))

    # Executive Summary Box
    summary_text = (
        "<b>Executive Summary:</b> This technical specification document details the complete suite of datasets "
        "engineered and utilized to train, calibrate, and benchmark the machine learning and computer vision models "
        "powering the <b>AGRO AI</b> intelligent agriculture platform. It covers 4 primary structured tabular CSV datasets "
        "(comprising <b>63,900 balanced samples</b> across <b>48 numerical feature dimensions</b>), underlying open-access "
        "raw vision datasets (PlantVillage, PlantDoc, Kaggle Pedological Soil, ICAR collections), the 10,208-taxa Indian "
        "botanical reference directory, and the multimodal vision-language foundation model (Qwen 2.5-VL 3B)."
    )
    summary_table = Table(
        [[Paragraph(summary_text, callout_style)]],
        colWidths=[504]
    )
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#eff6ff")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#93c5fd")),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 14))

    # =========================================================================
    # SECTION 1: MASTER DATASET INVENTORY
    # =========================================================================
    story.append(Paragraph("1. Master Dataset Inventory & Core Metrics", h1_style))
    story.append(Paragraph(
        "AGRO AI operates a stratified multi-tier architecture consisting of edge-ready Random Forest / Gradient Boosting "
        "ensemble classifiers, an ONNX convolutional vision pipeline, an authoritative PostgreSQL botanical database, "
        "and an on-premise multimodal vision LLM:", body_style
    ))

    inv_data = [
        [
            Paragraph("Dataset File", table_header_style),
            Paragraph("Target Model / Task", table_header_style),
            Paragraph("Total Rows", table_header_style),
            Paragraph("Features", table_header_style),
            Paragraph("Classes", table_header_style),
            Paragraph("File Size", table_header_style)
        ],
        [
            Paragraph("<b>agricultural_relevance_dataset.csv</b>", table_cell_style),
            Paragraph("Input Gatekeeper (Relevance Filter)", table_cell_style),
            Paragraph("9,000", table_cell_style),
            Paragraph("48 (Color/Texture/Edge)", table_cell_style),
            Paragraph("3 classes", table_cell_style),
            Paragraph("2.25 MB", table_cell_style)
        ],
        [
            Paragraph("<b>crop_disease_dataset.csv</b>", table_cell_style),
            Paragraph("Crop Foliar Pathogen Detection", table_cell_style),
            Paragraph("31,200", table_cell_style),
            Paragraph("48 (Pathology/Spectral)", table_cell_style),
            Paragraph("39 classes", table_cell_style),
            Paragraph("8.78 MB", table_cell_style)
        ],
        [
            Paragraph("<b>plant_species_dataset.csv</b>", table_cell_style),
            Paragraph("Botanical Species Identification", table_cell_style),
            Paragraph("14,700", table_cell_style),
            Paragraph("48 + 4 Metadata", table_cell_style),
            Paragraph("98 species", table_cell_style),
            Paragraph("7.61 MB", table_cell_style)
        ],
        [
            Paragraph("<b>soil_pedological_dataset.csv</b>", table_cell_style),
            Paragraph("Pedological Soil Classification", table_cell_style),
            Paragraph("9,000", table_cell_style),
            Paragraph("48 (Granulometry/Tone)", table_cell_style),
            Paragraph("6 soil types", table_cell_style),
            Paragraph("2.32 MB", table_cell_style)
        ],
        [
            Paragraph("<b>Plant Species Master Directory</b>", table_cell_bold),
            Paragraph("Database Reference Catalog", table_cell_bold),
            Paragraph("10,208 taxa", table_cell_bold),
            Paragraph("16 schema attributes", table_cell_bold),
            Paragraph("All India Flora", table_cell_bold),
            Paragraph("14.5 MB", table_cell_bold)
        ],
        [
            Paragraph("<b>Qwen 2.5-VL 3B Model</b>", table_cell_bold),
            Paragraph("Zero-Shot Visual Diagnostic LLM", table_cell_bold),
            Paragraph("3.0 Billion Param", table_cell_bold),
            Paragraph("Multimodal Vision Tensor", table_cell_bold),
            Paragraph("Open Vocabulary", table_cell_bold),
            Paragraph("1.9 GB", table_cell_bold)
        ]
    ]

    t_inv = Table(inv_data, colWidths=[130, 134, 55, 65, 60, 60])
    t_inv.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_primary),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_light]),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_inv)
    story.append(Spacer(1, 14))

    # =========================================================================
    # SECTION 2: RAW IMAGE BENCHMARKS & LICENSES
    # =========================================================================
    story.append(Paragraph("2. Underlying Raw Datasets, Benchmarks & Open Licenses", h1_style))
    story.append(Paragraph(
        "The engineered feature datasets and pretrained weights originate from internationally recognized agricultural "
        "and botanical research repositories:", body_style
    ))

    benchmarks = [
        ("PlantVillage Dataset (CrowdAI / Penn State)",
         "Contains 54,306 laboratory and controlled-condition photographs of healthy and infected plant leaves across 14 crop species and 38 distinct disease/pest classes. Open Access / CC BY-SA 4.0 license."),
        ("PlantDoc Dataset (IIT Delhi)",
         "A benchmark dataset of 2,598 real-world field-condition photographs spanning 13 plant species and 17 pathological classes. Captures natural illumination variations, background occlusions, soil interference, and multi-leaf scenes for domain robustness. Academic and Research Open Use."),
        ("Kaggle & ICAR Pedological Soil Collections",
         "Surface photography of Indian soil orders across diverse agricultural topographies (Alluvial plains, Deccan black cotton soil, coastal laterites, red sandy loams). Sampled from ICAR (Indian Council of Agricultural Research) regional institutes and open Kaggle pedological datasets."),
        ("Microsoft COCO & Pascal VOC Subsets (Non-Agricultural Distractors)",
         "To train the Agricultural Relevance Gatekeeper, negative distractor images (motor vehicles, electronic consumer goods, interior rooms, selfies, processed fast foods) were sampled from Microsoft COCO and Pascal VOC benchmarks to ensure strict rejection of invalid uploads."),
        ("Alibaba Cloud Qwen 2.5-VL Multimodal Vision-Language Dataset",
         "Large-scale multimodal visual instruction and document tuning dataset powering Qwen2.5-VL:3B, enabling zero-shot symptom localization, anatomical plant part recognition (leaf, flower, fruit, stem, root), and agronomic reasoning.")
    ]

    for title, desc in benchmarks:
        story.append(Paragraph(f"&bull;&nbsp; <b>{title}:</b> {desc}", bullet_style))

    story.append(Spacer(1, 14))

    # =========================================================================
    # SECTION 3: IN-DEPTH DATASET SPECIFICATIONS
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("3. Detailed Dataset Specifications", h1_style))

    # --- DATASET A ---
    story.append(Paragraph("3.1. Agricultural Relevance Gatekeeper Dataset (agricultural_relevance_dataset.csv)", h2_style))
    story.append(Paragraph(
        "<b>Purpose:</b> Acts as the primary security and relevance filter at the API entry point. It evaluates uploaded "
        "images and immediately filters out non-agricultural inputs before they reach compute-intensive disease models.", body_style
    ))

    rel_table_data = [
        [Paragraph("Target Class", table_header_style), Paragraph("Samples", table_header_style), Paragraph("Description & Visual Archetype", table_header_style)],
        [Paragraph("<b>plant</b>", table_cell_style), Paragraph("3,000", table_cell_style), Paragraph("Crops, foliar leaves, botanical flowers, horticultural plants, vegetative canopy.", table_cell_style)],
        [Paragraph("<b>soil</b>", table_cell_style), Paragraph("3,000", table_cell_style), Paragraph("Exposed agricultural topsoil, tilled fields, compost, seedbeds, potting soil.", table_cell_style)],
        [Paragraph("<b>non_agricultural</b>", table_cell_style), Paragraph("3,000", table_cell_style), Paragraph("Automobiles, smartphones, human faces, furniture, architecture, processed snacks.", table_cell_style)],
    ]
    t_rel = Table(rel_table_data, colWidths=[110, 60, 334])
    t_rel.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_secondary),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_light]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_rel)
    story.append(Spacer(1, 10))

    # --- DATASET B ---
    story.append(Paragraph("3.2. Crop Foliar Pathogen & Disease Dataset (crop_disease_dataset.csv)", h2_style))
    story.append(Paragraph(
        "<b>Purpose:</b> Multi-class foliar diagnostic model capable of recognizing 38 pathological conditions "
        "and healthy leaf stages across 14 economically critical agricultural crops (31,200 stratified records; 800 samples per class):", body_style
    ))

    disease_classes_data = [
        [Paragraph("Crop Host", table_header_style), Paragraph("Supported Pathological / Healthy Classes", table_header_style), Paragraph("Count", table_header_style)],
        [Paragraph("<b>Apple</b>", table_cell_style), Paragraph("Apple Scab (<i>Venturia inaequalis</i>), Black Rot (<i>Botryosphaeria obtusa</i>), Cedar Apple Rust (<i>Gymnosporangium</i>), Healthy", table_cell_style), Paragraph("3,200", table_cell_style)],
        [Paragraph("<b>Blueberry</b>", table_cell_style), Paragraph("Healthy Foliage", table_cell_style), Paragraph("800", table_cell_style)],
        [Paragraph("<b>Cherry</b>", table_cell_style), Paragraph("Powdery Mildew (<i>Podosphaera clandestina</i>), Healthy", table_cell_style), Paragraph("1,600", table_cell_style)],
        [Paragraph("<b>Corn (Maize)</b>", table_cell_style), Paragraph("Cercospora Leaf Spot (Gray leaf spot), Common Rust (<i>Puccinia sorghi</i>), Northern Leaf Blight (<i>Exserohilum</i>), Healthy", table_cell_style), Paragraph("3,200", table_cell_style)],
        [Paragraph("<b>Grape</b>", table_cell_style), Paragraph("Black Rot (<i>Guignardia bidwellii</i>), Esca (Black Measles), Leaf Blight (<i>Isariopsis clavispora</i>), Healthy", table_cell_style), Paragraph("3,200", table_cell_style)],
        [Paragraph("<b>Orange / Citrus</b>", table_cell_style), Paragraph("Citrus Greening / Huanglongbing (<i>Candidatus Liberibacter</i>)", table_cell_style), Paragraph("800", table_cell_style)],
        [Paragraph("<b>Peach</b>", table_cell_style), Paragraph("Bacterial Spot (<i>Xanthomonas campestris</i>), Healthy", table_cell_style), Paragraph("1,600", table_cell_style)],
        [Paragraph("<b>Bell Pepper</b>", table_cell_style), Paragraph("Bacterial Spot (<i>Xanthomonas vesicatoria</i>), Healthy", table_cell_style), Paragraph("1,600", table_cell_style)],
        [Paragraph("<b>Potato</b>", table_cell_style), Paragraph("Early Blight (<i>Alternaria solani</i>), Late Blight (<i>Phytophthora infestans</i>), Healthy", table_cell_style), Paragraph("2,400", table_cell_style)],
        [Paragraph("<b>Raspberry</b>", table_cell_style), Paragraph("Healthy Foliage", table_cell_style), Paragraph("800", table_cell_style)],
        [Paragraph("<b>Soybean</b>", table_cell_style), Paragraph("Healthy Foliage", table_cell_style), Paragraph("800", table_cell_style)],
        [Paragraph("<b>Squash</b>", table_cell_style), Paragraph("Powdery Mildew (<i>Erysiphe cichoracearum</i>)", table_cell_style), Paragraph("800", table_cell_style)],
        [Paragraph("<b>Strawberry</b>", table_cell_style), Paragraph("Leaf Scorch (<i>Diplocarpon earlianum</i>), Healthy", table_cell_style), Paragraph("1,600", table_cell_style)],
        [Paragraph("<b>Tomato</b>", table_cell_style), Paragraph("Bacterial Spot, Early Blight, Late Blight, Leaf Mold, Septoria Leaf Spot, Two-spotted Spider Mite, Target Spot, Tomato Yellow Leaf Curl Virus, Mosaic Virus, Healthy", table_cell_style), Paragraph("8,000", table_cell_style)],
        [Paragraph("<b>Negative Control</b>", table_cell_style), Paragraph("General Agricultural Background / Soil", table_cell_style), Paragraph("800", table_cell_style)],
    ]
    t_dis = Table(disease_classes_data, colWidths=[90, 360, 54])
    t_dis.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_secondary),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_light]),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    story.append(t_dis)
    story.append(Spacer(1, 10))

    # --- DATASET C ---
    story.append(PageBreak())
    story.append(Paragraph("3.3. Botanical Plant Species Dataset (plant_species_dataset.csv)", h2_style))
    story.append(Paragraph(
        "<b>Purpose:</b> Multi-species visual recognition representing 98 distinct Indian agricultural, horticultural, "
        "and medicinal botanical species (14,700 samples; 150 per species) spanning cereals, pulses, vegetables, fruits, "
        "spices, trees, and floriculture:", body_style
    ))

    species_summary_data = [
        [Paragraph("Category", table_header_style), Paragraph("Key Representative Botanical Species", table_header_style), Paragraph("Species Count", table_header_style)],
        [Paragraph("<b>Medicinal & Herbal</b>", table_cell_style), Paragraph("<i>Azadirachta indica</i> (Neem), <i>Ocimum tenuiflorum</i> (Tulsi), <i>Aloe barbadensis</i> (Aloe Vera), <i>Bacopa monnieri</i> (Brahmi), <i>Catharanthus roseus</i> (Sadabahar), <i>Mentha arvensis</i> (Mint), <i>Piper betle</i> (Paan)", table_cell_style), Paragraph("18 species", table_cell_style)],
        [Paragraph("<b>Crops & Cereals</b>", table_cell_style), Paragraph("<i>Oryza sativa</i> (Paddy Rice), <i>Triticum aestivum</i> (Wheat), <i>Zea mays</i> (Maize/Corn), <i>Eleusine coracana</i> (Ragi), <i>Cicer arietinum</i> (Chickpea), <i>Cajanus cajan</i> (Pigeon Pea)", table_cell_style), Paragraph("16 species", table_cell_style)],
        [Paragraph("<b>Vegetables</b>", table_cell_style), Paragraph("<i>Solanum lycopersicum</i> (Tomato), <i>Solanum melongena</i> (Brinjal), <i>Abelmoschus esculentus</i> (Okra/Bhindi), <i>Allium cepa</i> (Onion), <i>Allium sativum</i> (Garlic), <i>Capsicum annuum</i> (Chilli)", table_cell_style), Paragraph("22 species", table_cell_style)],
        [Paragraph("<b>Fruit Crops</b>", table_cell_style), Paragraph("<i>Mangifera indica</i> (Mango), <i>Carica papaya</i> (Papaya), <i>Psidium guajava</i> (Guava), <i>Citrus limon</i> (Lemon), <i>Musa acuminata</i> (Banana), <i>Punica granatum</i> (Pomegranate), <i>Syzygium cumini</i> (Jamun)", table_cell_style), Paragraph("20 species", table_cell_style)],
        [Paragraph("<b>Flowers & Ornamentals</b>", table_cell_style), Paragraph("<i>Rosa indica</i> (Rose), <i>Helianthus annuus</i> (Sunflower), <i>Hibiscus rosa-sinensis</i> (China Rose), <i>Jasminum sambac</i> (Mogra/Jasmine), <i>Tagetes erecta</i> (Marigold), <i>Nelumbo nucifera</i> (Lotus)", table_cell_style), Paragraph("12 species", table_cell_style)],
        [Paragraph("<b>Agroforestry Trees</b>", table_cell_style), Paragraph("<i>Ficus religiosa</i> (Peepal), <i>Ficus benghalensis</i> (Banyan), <i>Cocos nucifera</i> (Coconut), <i>Moringa oleifera</i> (Drumstick), <i>Bambusa vulgaris</i> (Bamboo), <i>Eucalyptus globulus</i>", table_cell_style), Paragraph("10 species", table_cell_style)],
    ]
    t_spec = Table(species_summary_data, colWidths=[110, 334, 60])
    t_spec.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_secondary),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_light]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_spec)
    story.append(Spacer(1, 10))

    # --- DATASET D ---
    story.append(Paragraph("3.4. Pedological Soil Classification Dataset (soil_pedological_dataset.csv)", h2_style))
    story.append(Paragraph(
        "<b>Purpose:</b> Classifies agricultural surface soil into 6 major Indian pedological categories (9,000 samples; "
        "1,500 samples per class) to determine irrigation capacity, soil organic carbon (SOC), and crop suitability:", body_style
    ))

    soil_data = [
        [Paragraph("Soil Category", table_header_style), Paragraph("Geographic Distribution in India", table_header_style), Paragraph("Agronomic Traits & Typical Crops", table_header_style), Paragraph("Samples", table_header_style)],
        [Paragraph("<b>Alluvial Soil</b>", table_cell_style), Paragraph("Indo-Gangetic plains, Punjab, UP, Bihar, West Bengal, coastal deltas", table_cell_style), Paragraph("High fertility, loamy texture, rich in potash/phosphoric acid. Ideal for Rice, Wheat, Sugarcane, Jute.", table_cell_style), Paragraph("1,500", table_cell_style)],
        [Paragraph("<b>Black (Regur) Soil</b>", table_cell_style), Paragraph("Deccan plateau, Maharashtra, Gujarat, MP, northern Karnataka", table_cell_style), Paragraph("High clay content, swelling/shrinkage self-ploughing, moisture retentive. Ideal for Cotton, Soybean, Sorghum.", table_cell_style), Paragraph("1,500", table_cell_style)],
        [Paragraph("<b>Red Soil</b>", table_cell_style), Paragraph("Tamil Nadu, Karnataka, Andhra Pradesh, Odisha, Chota Nagpur", table_cell_style), Paragraph("Rich in ferric oxides, porous, low nitrogen and humus. Ideal for Groundnut, Millets, Pulses, Tobacco.", table_cell_style), Paragraph("1,500", table_cell_style)],
        [Paragraph("<b>Laterite Soil</b>", table_cell_style), Paragraph("Western Ghats summits, Kerala, coastal Karnataka, Assam hills", table_cell_style), Paragraph("Intensely leached by heavy rainfall, acidic, high iron/aluminum. Ideal for Tea, Coffee, Cashew, Rubber.", table_cell_style), Paragraph("1,500", table_cell_style)],
        [Paragraph("<b>Heavy Clay Soil</b>", table_cell_style), Paragraph("River backwaters, wetlands, lake beds, canal commanded tracts", table_cell_style), Paragraph("Extremely fine grain, low drainage, high waterlogging risk. Ideal for Paddy Rice, Lotus, Water Chestnut.", table_cell_style), Paragraph("1,500", table_cell_style)],
        [Paragraph("<b>Sandy Loam Soil</b>", table_cell_style), Paragraph("Rajasthan arid zones, south-west Haryana, coastal sand dunes", table_cell_style), Paragraph("Coarse texture, high permeability, rapid leaching. Ideal for Bajra, Mustard, Watermelon, Guar.", table_cell_style), Paragraph("1,500", table_cell_style)],
    ]
    t_soil = Table(soil_data, colWidths=[80, 120, 250, 54])
    t_soil.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_secondary),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_light]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_soil)
    story.append(Spacer(1, 14))

    # =========================================================================
    # SECTION 4: 48-DIMENSIONAL FEATURE ENGINEERING ARCHITECTURE
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("4. 48-Dimensional Computer Vision Feature Engineering", h1_style))
    story.append(Paragraph(
        "Each tabular dataset row consists of 48 engineered numerical feature descriptors (<b>feat_0</b> through <b>feat_47</b>) "
        "extracted through specialized computer vision operations. These features enable ultralight (under 5 MB), ultra-fast "
        "(sub-50 millisecond) inference on standard CPUs without requiring expensive GPU hardware:", body_style
    ))

    feat_data = [
        [Paragraph("Feature Indices", table_header_style), Paragraph("Mathematical Extraction Method", table_header_style), Paragraph("Agronomic & Physiological Purpose", table_header_style)],
        [
            Paragraph("<b>feat_0 &ndash; feat_2</b>", table_cell_style),
            Paragraph("<b>RGB Channel Color Moments:</b> First-order mean and variance across R, G, B channels after illumination normalization.", table_cell_style),
            Paragraph("Separates dark foliage from light/glaucous leaves and distinguishes red/anthocyanin-rich vegetation.", table_cell_style)
        ],
        [
            Paragraph("<b>feat_3 &ndash; feat_8</b>", table_cell_style),
            Paragraph("<b>Perceptual Color Spaces (HSV & CIELAB):</b> Hue angle circular mean, Saturation mean, Lightness L*, Green-Red chromaticity a*, Blue-Yellow b*.", table_cell_style),
            Paragraph("Captures foliar chlorosis (yellowing), necrosis (browning), and diagnostic leaf pigmentation invariant to shadow.", table_cell_style)
        ],
        [
            Paragraph("<b>feat_9 &ndash; feat_16</b>", table_cell_style),
            Paragraph("<b>Morphological Geometry:</b> Contour elongation aspect ratio (major/minor axis), circularity (4&pi;A/P&sup2;), solidity, compactness, convex hull ratio.", table_cell_style),
            Paragraph("Differentiates linear grass blades (wheat/paddy) from broad ovate leaves (mango/guava) and lobed dicots (papaya).", table_cell_style)
        ],
        [
            Paragraph("<b>feat_17 &ndash; feat_24</b>", table_cell_style),
            Paragraph("<b>Boundary Margin & Edge Density:</b> Sobel gradient magnitude histogram, Canny edge pixel density, and high-frequency boundary waviness.", table_cell_style),
            Paragraph("Detects serrated margin teeth (rose/neem) vs smooth entire margins (banyan/mango) vs wavy undulating margins.", table_cell_style)
        ],
        [
            Paragraph("<b>feat_25 &ndash; feat_36</b>", table_cell_style),
            Paragraph("<b>GLCM Texture & Venation Moments:</b> Gray-Level Co-occurrence Matrix Haralick descriptors (Energy, Contrast, Correlation, Homogeneity) at 0&deg;, 45&deg;, 90&deg;.", table_cell_style),
            Paragraph("Identifies parallel monocot venation vs reticulate dicot network, foliar pubescence (hairs), and surface smoothness.", table_cell_style)
        ],
        [
            Paragraph("<b>feat_37 &ndash; feat_47</b>", table_cell_style),
            Paragraph("<b>Pathology & Symptom Ratios:</b> Calibrated pixel color thresholding for Chlorosis Index (% yellow), Necrosis Index (% brown), and Powdery Mildew Index (% white/gray).", table_cell_style),
            Paragraph("Direct symptom quantifiers feeding the crop disease classifier and plant health score assessment algorithm.", table_cell_style)
        ],
    ]
    t_feat = Table(feat_data, colWidths=[100, 204, 200])
    t_feat.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_primary),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_light]),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
    ]))
    story.append(t_feat)
    story.append(Spacer(1, 14))

    # =========================================================================
    # SECTION 5: BOTANICAL DATABASE & VISION LLM SPECIFICATION
    # =========================================================================
    story.append(Paragraph("5. Integrated Indian Botanical Database & Multimodal Vision LLM", h1_style))
    story.append(Paragraph(
        "In addition to the 4 CSV files, AGRO AI bundles two foundational knowledge bases to ensure accurate identification "
        "and agronomic management:", body_style
    ))

    story.append(Paragraph("5.1. 10,208 Indian Botanical Species Catalog (Supabase PostgreSQL / SQLite)", h2_style))
    story.append(Paragraph(
        "A curated master taxonomy database covering India's agricultural, horticultural, and indigenous flora. "
        "Every species record contains 16 verified attributes: Common English Name, Scientific Binomial, Hindi Name, Telugu Name, "
        "Tamil Name, Botanical Family, Plant Category, Status in India (Native/Endemic/Introduced), Soil Preferences, "
        "Watering Requirements, Sunlight Tolerances, Growth Cycle, and Leaf Morphology JSON.", body_style
    ))

    story.append(Paragraph("5.2. Qwen 2.5-VL 3B Multimodal Vision-Language Foundation Model", h2_style))
    story.append(Paragraph(
        "Integrated via local Ollama runtime (<code>qwen2.5vl:3b</code>). This 3-billion-parameter vision-language model "
        "performs deep visual screening on raw uncompressed image uploads. It analyzes organ type (flower, leaf, fruit, stem, root), "
        "evaluates ripeness and spoilage indicators, identifies visible foliar stress symptoms, and generates actionable, "
        "chemical-safe recommendations in structured JSON format.", body_style
    ))
    story.append(Spacer(1, 14))

    # =========================================================================
    # SECTION 6: FILE LOCATIONS & DOWNLOAD GUIDE
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("6. Dataset Files, Models & Download Locations", h1_style))
    story.append(Paragraph(
        "All dataset CSV files, trained models, and reproduction scripts are persisted within your local AGRO AI installation "
        "and accessible at the following absolute paths:", body_style
    ))

    file_paths_data = [
        [Paragraph("Artifact / Dataset", table_header_style), Paragraph("Local File System Path", table_header_style), Paragraph("Format & Size", table_header_style)],
        [
            Paragraph("<b>Agricultural Relevance Dataset</b>", table_cell_style),
            Paragraph("<code>datasets/agricultural_relevance_dataset.csv</code>", table_cell_style),
            Paragraph("CSV (2.25 MB)", table_cell_style)
        ],
        [
            Paragraph("<b>Crop Disease Dataset</b>", table_cell_style),
            Paragraph("<code>datasets/crop_disease_dataset.csv</code>", table_cell_style),
            Paragraph("CSV (8.78 MB)", table_cell_style)
        ],
        [
            Paragraph("<b>Plant Species Dataset</b>", table_cell_style),
            Paragraph("<code>datasets/plant_species_dataset.csv</code>", table_cell_style),
            Paragraph("CSV (7.61 MB)", table_cell_style)
        ],
        [
            Paragraph("<b>Soil Pedological Dataset</b>", table_cell_style),
            Paragraph("<code>datasets/soil_pedological_dataset.csv</code>", table_cell_style),
            Paragraph("CSV (2.32 MB)", table_cell_style)
        ],
        [
            Paragraph("<b>ONNX Plant Vision Model</b>", table_cell_style),
            Paragraph("<code>backend/models/plant_identifier.onnx</code>", table_cell_style),
            Paragraph("ONNX (10.9 MB)", table_cell_style)
        ],
        [
            Paragraph("<b>Joblib Ensemble Models</b>", table_cell_style),
            Paragraph("<code>backend/models/{crop_disease, soil_classifier, agricultural_relevance}.joblib</code>", table_cell_style),
            Paragraph("Joblib (3 files)", table_cell_style)
        ],
        [
            Paragraph("<b>Model Metadata Spec</b>", table_cell_style),
            Paragraph("<code>backend/models/model_metadata.json</code>", table_cell_style),
            Paragraph("JSON Spec", table_cell_style)
        ],
        [
            Paragraph("<b>Dataset Preparation Script</b>", table_cell_style),
            Paragraph("<code>training/prepare_dataset.py</code>", table_cell_style),
            Paragraph("Python Script", table_cell_style)
        ],
        [
            Paragraph("<b>Full Retraining Pipeline</b>", table_cell_style),
            Paragraph("<code>training/train_all_models.py</code>", table_cell_style),
            Paragraph("Python Script", table_cell_style)
        ],
    ]
    t_paths = Table(file_paths_data, colWidths=[140, 274, 90])
    t_paths.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_primary),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_light]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_paths)
    story.append(Spacer(1, 14))

    # Verification & Reproducibility Command Box
    story.append(Paragraph("Reproducing and Retraining Models from Datasets:", h2_style))
    repro_code = (
        "# 1. Verify Dataset Integrity & File Formats:\n"
        "python training/prepare_dataset.py\n\n"
        "# 2. Train and export all models directly from CSV files:\n"
        "python training/train_all_models.py\n\n"
        "# 3. Verify Model Weights and Metadata Alignment:\n"
        "python training/verify_trained_model.py"
    )
    story.append(Paragraph(repro_code.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style))
    story.append(Spacer(1, 14))

    # Sign-off box
    signoff_table = Table(
        [[
            Paragraph(
                "<b>AGRO AI Engineering & Machine Learning Team</b><br/>"
                "This document serves as the formal specification and reference manual for all datasets used in AGRO AI. "
                "For research questions, license verification, or dataset extensions, consult the project repository.",
                table_cell_style
            )
        ]],
        colWidths=[504]
    )
    signoff_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ('BOX', (0, 0), (-1, -1), 1, c_secondary),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(signoff_table)

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[SUCCESS] PDF generated at: {output_path}")

if __name__ == "__main__":
    out_dir = Path(__file__).resolve().parent.parent / "datasets"
    target_pdf = out_dir / "AGRO_AI_Training_Datasets_Documentation.pdf"
    build_pdf(str(target_pdf))

