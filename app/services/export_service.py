"""
Service pour la génération des exports (Excel, Word, PDF)
"""

from io import BytesIO
from typing import Dict, Any, List
from decimal import Decimal
from datetime import datetime

# Note: Ces imports seront disponibles après installation des packages
# pip install openpyxl python-docx reportlab

try:
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter
    EXCEL_AVAILABLE = True
except ImportError:
    EXCEL_AVAILABLE = False

try:
    from docx import Document
    from docx.shared import Inches, Pt, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    WORD_AVAILABLE = True
except ImportError:
    WORD_AVAILABLE = False

try:
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib import colors
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False


class ExportService:
    """Service pour générer les exports dans différents formats"""

    @staticmethod
    def generate_excel(tableau_data: Dict[str, Any]) -> BytesIO:
        """
        Génère un fichier Excel à partir des données du tableau

        Args:
            tableau_data: Dictionnaire contenant commune, exercice, periodes, rubriques, donnees, totaux

        Returns:
            BytesIO contenant le fichier Excel
        """
        if not EXCEL_AVAILABLE:
            raise ImportError("openpyxl n'est pas installé. Installez-le avec: pip install openpyxl")

        commune = tableau_data["commune"]
        exercice = tableau_data["exercice"]
        periodes = tableau_data["periodes"]
        rubriques = tableau_data["rubriques"]
        donnees = tableau_data["donnees"]
        totaux = tableau_data.get("totaux", {})

        # Créer un workbook
        wb = Workbook()
        ws = wb.active
        ws.title = "Compte Administratif"

        # Styles
        header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
        header_font = Font(color="FFFFFF", bold=True, size=12)
        title_font = Font(bold=True, size=14)
        bold_font = Font(bold=True)
        center_alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )

        # Titre
        ws.merge_cells('A1:F1')
        title_cell = ws['A1']
        title_cell.value = f"TABLEAU DE COMPTE ADMINISTRATIF - {exercice.annee}"
        title_cell.font = title_font
        title_cell.alignment = center_alignment

        # Informations commune
        ws['A2'] = "Commune:"
        ws['B2'] = commune.nom
        ws['A3'] = "Région:"
        ws['B3'] = commune.region.nom if hasattr(commune, 'region') else ""
        ws['A4'] = "Département:"
        ws['B4'] = commune.departement.nom if hasattr(commune, 'departement') else ""

        # En-têtes de tableau
        row = 6
        ws[f'A{row}'] = "Code"
        ws[f'B{row}'] = "Rubrique"

        col = 3  # Colonne C
        for periode in periodes:
            cell = ws.cell(row=row, column=col)
            cell.value = periode.nom
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = center_alignment
            cell.border = border
            col += 1

        # Total
        cell = ws.cell(row=row, column=col)
        cell.value = "TOTAL"
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = center_alignment
        cell.border = border

        # Appliquer le style aux en-têtes de gauche
        ws[f'A{row}'].fill = header_fill
        ws[f'A{row}'].font = header_font
        ws[f'A{row}'].border = border
        ws[f'B{row}'].fill = header_fill
        ws[f'B{row}'].font = header_font
        ws[f'B{row}'].border = border

        # Données des rubriques
        row += 1
        for rubrique in rubriques:
            ws.cell(row=row, column=1, value=rubrique.code).border = border
            ws.cell(row=row, column=2, value=rubrique.nom).border = border

            # Si c'est une rubrique parent, mettre en gras
            if rubrique.niveau == 1:
                ws.cell(row=row, column=1).font = bold_font
                ws.cell(row=row, column=2).font = bold_font

            # Indentation selon le niveau
            if rubrique.niveau > 1:
                ws.cell(row=row, column=2).value = "  " * (rubrique.niveau - 1) + rubrique.nom

            col = 3
            for periode in periodes:
                # Récupérer le montant
                montant = 0
                if rubrique.id in donnees and periode.id in donnees[rubrique.id]:
                    revenu = donnees[rubrique.id][periode.id]
                    montant = float(revenu.montant) if revenu.montant else 0

                cell = ws.cell(row=row, column=col, value=montant if montant != 0 else "")
                cell.number_format = '#,##0.00'
                cell.border = border
                cell.alignment = Alignment(horizontal="right")
                col += 1

            # Total de la rubrique
            total = float(totaux.get(rubrique.id, 0))
            cell = ws.cell(row=row, column=col, value=total if total != 0 else "")
            cell.number_format = '#,##0.00'
            cell.border = border
            cell.font = bold_font
            cell.alignment = Alignment(horizontal="right")

            row += 1

        # Ajuster la largeur des colonnes
        ws.column_dimensions['A'].width = 12
        ws.column_dimensions['B'].width = 40
        for col in range(3, 3 + len(periodes) + 1):
            ws.column_dimensions[get_column_letter(col)].width = 15

        # Sauvegarder dans un BytesIO
        output = BytesIO()
        wb.save(output)
        output.seek(0)
        return output

    @staticmethod
    def generate_word(tableau_data: Dict[str, Any]) -> BytesIO:
        """
        Génère un fichier Word à partir des données du tableau

        Args:
            tableau_data: Dictionnaire contenant commune, exercice, periodes, rubriques, donnees, totaux

        Returns:
            BytesIO contenant le fichier Word
        """
        if not WORD_AVAILABLE:
            raise ImportError("python-docx n'est pas installé. Installez-le avec: pip install python-docx")

        commune = tableau_data["commune"]
        exercice = tableau_data["exercice"]
        periodes = tableau_data["periodes"]
        rubriques = tableau_data["rubriques"]
        donnees = tableau_data["donnees"]
        totaux = tableau_data.get("totaux", {})

        # Créer un document
        doc = Document()

        # Titre
        title = doc.add_heading(f"TABLEAU DE COMPTE ADMINISTRATIF - {exercice.annee}", 0)
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER

        # Informations commune
        doc.add_paragraph(f"Commune: {commune.nom}", style='Heading 2')
        if hasattr(commune, 'region'):
            doc.add_paragraph(f"Région: {commune.region.nom}")
        if hasattr(commune, 'departement'):
            doc.add_paragraph(f"Département: {commune.departement.nom}")

        doc.add_paragraph()  # Espace

        # Créer le tableau
        num_cols = 2 + len(periodes) + 1  # Code + Rubrique + Périodes + Total
        table = doc.add_table(rows=1, cols=num_cols)
        table.style = 'Light Grid Accent 1'

        # En-têtes
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = 'Code'
        hdr_cells[1].text = 'Rubrique'

        for idx, periode in enumerate(periodes):
            hdr_cells[2 + idx].text = periode.nom

        hdr_cells[-1].text = 'TOTAL'

        # Données
        for rubrique in rubriques:
            row_cells = table.add_row().cells
            row_cells[0].text = rubrique.code
            row_cells[1].text = "  " * (rubrique.niveau - 1) + rubrique.nom

            for idx, periode in enumerate(periodes):
                montant = 0
                if rubrique.id in donnees and periode.id in donnees[rubrique.id]:
                    revenu = donnees[rubrique.id][periode.id]
                    montant = float(revenu.montant) if revenu.montant else 0

                row_cells[2 + idx].text = f"{montant:,.2f}" if montant != 0 else ""

            # Total
            total = float(totaux.get(rubrique.id, 0))
            row_cells[-1].text = f"{total:,.2f}" if total != 0 else ""

        # Pied de page
        doc.add_paragraph()
        footer = doc.add_paragraph(f"Document généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}")
        footer.alignment = WD_ALIGN_PARAGRAPH.RIGHT

        # Sauvegarder
        output = BytesIO()
        doc.save(output)
        output.seek(0)
        return output

    @staticmethod
    def generate_pdf(tableau_data: Dict[str, Any]) -> BytesIO:
        """
        Génère un fichier PDF à partir des données du tableau

        Args:
            tableau_data: Dictionnaire contenant commune, exercice, periodes, rubriques, donnees, totaux

        Returns:
            BytesIO contenant le fichier PDF
        """
        if not PDF_AVAILABLE:
            raise ImportError("reportlab n'est pas installé. Installez-le avec: pip install reportlab")

        commune = tableau_data["commune"]
        exercice = tableau_data["exercice"]
        periodes = tableau_data["periodes"]
        rubriques = tableau_data["rubriques"]
        donnees = tableau_data["donnees"]
        totaux = tableau_data.get("totaux", {})

        # Créer le PDF en mode paysage
        output = BytesIO()
        doc = SimpleDocTemplate(output, pagesize=landscape(A4))
        elements = []

        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#366092'),
            spaceAfter=30,
            alignment=1  # Center
        )

        # Titre
        title_text = f"TABLEAU DE COMPTE ADMINISTRATIF - {exercice.annee}"
        elements.append(Paragraph(title_text, title_style))

        # Info commune
        info_text = f"<b>Commune:</b> {commune.nom}<br/>"
        if hasattr(commune, 'region'):
            info_text += f"<b>Région:</b> {commune.region.nom}<br/>"
        if hasattr(commune, 'departement'):
            info_text += f"<b>Département:</b> {commune.departement.nom}"

        elements.append(Paragraph(info_text, styles['Normal']))
        elements.append(Spacer(1, 20))

        # Préparer les données du tableau
        table_data = []

        # En-têtes
        headers = ['Code', 'Rubrique'] + [p.nom for p in periodes] + ['TOTAL']
        table_data.append(headers)

        # Données
        for rubrique in rubriques:
            row = [
                rubrique.code,
                "  " * (rubrique.niveau - 1) + rubrique.nom[:50]  # Limiter la longueur
            ]

            for periode in periodes:
                montant = 0
                if rubrique.id in donnees and periode.id in donnees[rubrique.id]:
                    revenu = donnees[rubrique.id][periode.id]
                    montant = float(revenu.montant) if revenu.montant else 0

                row.append(f"{montant:,.2f}" if montant != 0 else "")

            total = float(totaux.get(rubrique.id, 0))
            row.append(f"{total:,.2f}" if total != 0 else "")

            table_data.append(row)

        # Créer le tableau
        table = Table(table_data)

        # Style du tableau
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#366092')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),  # Aligner les montants à droite
        ]))

        elements.append(table)

        # Pied de page
        elements.append(Spacer(1, 20))
        footer_text = f"Document généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}"
        elements.append(Paragraph(footer_text, styles['Normal']))

        # Construire le PDF
        doc.build(elements)

        output.seek(0)
        return output
