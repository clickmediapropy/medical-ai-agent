#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convierte el informe markdown a PDF usando markdown2 y weasyprint o reportlab
"""

import os
import sys
try:
    import markdown2
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
    from reportlab.platypus import KeepTogether, Image
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfbase.pdfmetrics import registerFontFamily
    from datetime import datetime
    import re
    import html

    def escape_xml(text):
        """Escapa caracteres especiales para XML/ReportLab"""
        text = str(text)
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        text = text.replace('"', '&quot;')
        text = text.replace("'", '&apos;')
        return text

    def clean_text(text):
        """Limpia y prepara el texto para PDF manteniendo acentos"""
        # Mantener acentos pero eliminar emojis
        text = re.sub(r'[^\x00-\x7F\xC0-\xFF]+', '', text)
        # Asegurar que los acentos estén correctamente codificados
        return text

    def convert_md_to_pdf():
        # Leer el archivo markdown
        md_file = "INFORME_CONSOLIDADO_CRISIS_TIROIDEA.md"
        pdf_file = "INFORME_CONSOLIDADO_CRISIS_TIROIDEA.pdf"

        if not os.path.exists(md_file):
            print(f"❌ Error: No se encuentra {md_file}")
            return

        with open(md_file, 'r', encoding='utf-8') as f:
            md_content = f.read()

        # Crear el documento PDF
        doc = SimpleDocTemplate(
            pdf_file,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=48
        )

        # Contenedor para los elementos del PDF
        story = []

        # Estilos
        styles = getSampleStyleSheet()

        # Estilos personalizados
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Title'],
            fontSize=20,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=TA_CENTER,
            bold=True
        )

        heading1_style = ParagraphStyle(
            'CustomHeading1',
            parent=styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=12,
            spaceBefore=20,
            bold=True
        )

        heading2_style = ParagraphStyle(
            'CustomHeading2',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=10,
            spaceBefore=15,
            bold=True
        )

        heading3_style = ParagraphStyle(
            'CustomHeading3',
            parent=styles['Heading3'],
            fontSize=12,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=8,
            spaceBefore=10,
            bold=True
        )

        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['BodyText'],
            fontSize=11,
            alignment=TA_JUSTIFY,
            spaceAfter=8
        )

        alert_style = ParagraphStyle(
            'Alert',
            parent=styles['BodyText'],
            fontSize=11,
            textColor=colors.HexColor('#c0392b'),
            bold=True,
            spaceAfter=8
        )

        success_style = ParagraphStyle(
            'Success',
            parent=styles['BodyText'],
            fontSize=11,
            textColor=colors.HexColor('#27ae60'),
            bold=True,
            spaceAfter=8
        )

        # Procesar línea por línea
        lines = md_content.split('\n')
        in_table = False
        table_data = []
        in_code_block = False
        code_lines = []

        for line in lines:
            # Ignorar líneas de separación
            if line.strip() == '---':
                story.append(Spacer(1, 0.2*inch))
                continue

            # Código en bloque
            if line.strip().startswith('```'):
                if not in_code_block:
                    in_code_block = True
                    code_lines = []
                else:
                    in_code_block = False
                    # Procesar el bloque de código
                    code_text = '<br/>'.join(code_lines)
                    code_style = ParagraphStyle(
                        'Code',
                        parent=styles['Code'],
                        fontSize=10,
                        leftIndent=20,
                        rightIndent=20,
                        backColor=colors.HexColor('#f5f5f5'),
                        borderColor=colors.HexColor('#ddd'),
                        borderWidth=1,
                        borderPadding=10,
                        spaceAfter=10
                    )
                    story.append(Paragraph(code_text, code_style))
                continue

            if in_code_block:
                code_lines.append(line)
                continue

            # Detectar tablas
            if '|' in line and not in_table:
                in_table = True
                table_data = []

            if in_table:
                if '|' in line:
                    # Procesar fila de tabla
                    cells = [cell.strip() for cell in line.split('|') if cell.strip()]
                    if not all(c == '-' or c.startswith(':') or c.endswith(':') for c in cells[0]):
                        table_data.append(cells)
                else:
                    # Fin de tabla
                    if table_data:
                        # Crear tabla
                        t = Table(table_data)
                        t.setStyle(TableStyle([
                            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('FONTSIZE', (0, 0), (-1, 0), 11),
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ecf0f1')),
                            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#95a5a6')),
                            ('FONTSIZE', (0, 1), (-1, -1), 10),
                            ('PADDING', (0, 0), (-1, -1), 6),
                        ]))
                        story.append(t)
                        story.append(Spacer(1, 0.2*inch))
                    in_table = False
                    table_data = []
                continue

            # Títulos y encabezados
            if line.startswith('# '):
                text = line[2:].strip()
                text = clean_text(text)
                story.append(Paragraph(text, title_style))

            elif line.startswith('## '):
                text = line[3:].strip()
                text = clean_text(text)
                story.append(Paragraph(text, heading1_style))

            elif line.startswith('### '):
                text = line[4:].strip()
                text = clean_text(text)
                story.append(Paragraph(text, heading2_style))

            elif line.startswith('#### '):
                text = line[5:].strip()
                text = clean_text(text)
                story.append(Paragraph(text, heading3_style))

            # Listas
            elif line.strip().startswith('- ') or line.strip().startswith('* '):
                text = line.strip()[2:]
                # Detectar checkmarks
                if '✅' in text or 'NORMAL' in text:
                    text = text.replace('✅', '[OK]')
                    text = clean_text(text)
                    story.append(Paragraph(f"• {text}", success_style))
                elif '⚠️' in text or 'elevad' in text.lower():
                    text = text.replace('⚠️', '[!]')
                    text = clean_text(text)
                    story.append(Paragraph(f"• {text}", alert_style))
                elif '🔴' in text:
                    text = text.replace('🔴', '[ALERTA]')
                    text = clean_text(text)
                    story.append(Paragraph(f"• {text}", alert_style))
                else:
                    text = clean_text(text)
                    story.append(Paragraph(f"• {text}", body_style))

            elif line.strip().startswith('1. ') or line.strip().startswith('2. ') or line.strip().startswith('3. '):
                text = clean_text(line.strip())
                story.append(Paragraph(text, body_style))

            # Texto en negrita
            elif line.startswith('**') and line.endswith('**'):
                text = line[2:-2]
                text = clean_text(text)
                bold_style = ParagraphStyle(
                    'Bold',
                    parent=body_style,
                    bold=True,
                    fontSize=12
                )
                story.append(Paragraph(text, bold_style))

            # Blockquote
            elif line.startswith('>'):
                text = line[1:].strip()
                text = clean_text(text)
                quote_style = ParagraphStyle(
                    'Quote',
                    parent=body_style,
                    leftIndent=30,
                    rightIndent=30,
                    textColor=colors.HexColor('#555'),
                    italic=True
                )
                story.append(Paragraph(text, quote_style))

            # Párrafos normales
            elif line.strip():
                # Procesar formato inline
                text = line.strip()
                # Convertir **texto** a <b>texto</b>
                text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
                # Convertir *texto* a <i>texto</i>
                text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
                # Convertir `código` a formato de código
                text = re.sub(r'`(.+?)`', r'<font name="Courier">\1</font>', text)

                # Limpiar texto manteniendo acentos
                text = clean_text(text)

                # Detectar si es una alerta especial
                if 'CRÍTICO' in text or 'URGENTE' in text or 'INMEDIATO' in text:
                    story.append(Paragraph(text, alert_style))
                elif 'NORMAL' in text or 'Excelente' in text or '✅' in text:
                    text = text.replace('✅', '[OK]')
                    story.append(Paragraph(text, success_style))
                else:
                    story.append(Paragraph(text, body_style))

        # Agregar footer
        story.append(Spacer(1, 0.5*inch))
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#777'),
            alignment=TA_CENTER
        )
        story.append(Paragraph(
            f"Documento generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
            footer_style
        ))

        # Construir PDF
        try:
            doc.build(story)
            print(f"✅ PDF creado exitosamente: {pdf_file}")

            # Verificar tamaño del archivo
            size = os.path.getsize(pdf_file)
            print(f"📄 Tamaño del archivo: {size:,} bytes")

            # Abrir el PDF automáticamente
            if sys.platform == "darwin":  # macOS
                os.system(f"open {pdf_file}")
            elif sys.platform == "win32":  # Windows
                os.system(f"start {pdf_file}")
            else:  # Linux
                os.system(f"xdg-open {pdf_file}")

        except Exception as e:
            print(f"❌ Error al crear PDF: {e}")

    convert_md_to_pdf()

except ImportError as e:
    print(f"❌ Error: Faltan librerías necesarias")
    print(f"   {e}")
    print("\n📦 Instalar con:")
    print("   pip install markdown2 reportlab")