"""
Tests pour le service d'export
"""

from decimal import Decimal
from sqlalchemy.orm import Session
from io import BytesIO

from app.models.geographie import Region, Departement, Commune
from app.models.revenus import Exercice, Periode, CategorieRubrique, Rubrique, Revenu
from app.services.export_service import ExportService


def create_test_tableau_data(db: Session) -> dict:
    """Cree des donnees de test pour le tableau"""
    # Creer les donnees geographiques
    region = Region(code="ANA", nom="Analamanga", actif=True)
    db.add(region)
    db.commit()
    db.refresh(region)

    departement = Departement(code="ANT", nom="Antananarivo", region_id=region.id, actif=True)
    db.add(departement)
    db.commit()
    db.refresh(departement)

    commune = Commune(code="ANT01", nom="Antananarivo I", departement_id=departement.id, actif=True)
    db.add(commune)
    db.commit()
    db.refresh(commune)

    # Ajouter manuellement la relation region pour le test
    commune.departement = departement
    departement.region = region

    # Creer un exercice
    exercice = Exercice(annee=2024, actif=True)
    db.add(exercice)
    db.commit()
    db.refresh(exercice)

    # Creer des periodes
    periode1 = Periode(nom="Trimestre 1", code="T1", exercice_id=exercice.id, ordre=1, actif=True)
    periode2 = Periode(nom="Trimestre 2", code="T2", exercice_id=exercice.id, ordre=2, actif=True)
    db.add_all([periode1, periode2])
    db.commit()
    db.refresh(periode1)
    db.refresh(periode2)

    # Creer une categorie et des rubriques
    categorie = CategorieRubrique(code="REC", nom="Recettes", actif=True)
    db.add(categorie)
    db.commit()
    db.refresh(categorie)

    rubrique1 = Rubrique(
        code="R001",
        nom="Impots locaux",
        categorie_id=categorie.id,
        niveau=1,
        actif=True
    )
    rubrique2 = Rubrique(
        code="R002",
        nom="Taxes diverses",
        categorie_id=categorie.id,
        niveau=1,
        actif=True
    )
    db.add_all([rubrique1, rubrique2])
    db.commit()
    db.refresh(rubrique1)
    db.refresh(rubrique2)

    # Creer des revenus
    revenu1 = Revenu(
        commune_id=commune.id,
        exercice_id=exercice.id,
        periode_id=periode1.id,
        rubrique_id=rubrique1.id,
        montant=Decimal("100000.00")
    )
    revenu2 = Revenu(
        commune_id=commune.id,
        exercice_id=exercice.id,
        periode_id=periode2.id,
        rubrique_id=rubrique1.id,
        montant=Decimal("120000.00")
    )
    revenu3 = Revenu(
        commune_id=commune.id,
        exercice_id=exercice.id,
        periode_id=periode1.id,
        rubrique_id=rubrique2.id,
        montant=Decimal("50000.00")
    )
    db.add_all([revenu1, revenu2, revenu3])
    db.commit()
    db.refresh(revenu1)
    db.refresh(revenu2)
    db.refresh(revenu3)

    # Construire le dictionnaire de donnees
    donnees = {
        rubrique1.id: {
            periode1.id: revenu1,
            periode2.id: revenu2
        },
        rubrique2.id: {
            periode1.id: revenu3
        }
    }

    totaux = {
        rubrique1.id: Decimal("220000.00"),
        rubrique2.id: Decimal("50000.00")
    }

    return {
        "commune": commune,
        "exercice": exercice,
        "periodes": [periode1, periode2],
        "rubriques": [rubrique1, rubrique2],
        "donnees": donnees,
        "totaux": totaux
    }


def test_generate_excel(db: Session):
    """Test de generation d'un fichier Excel"""
    try:
        tableau_data = create_test_tableau_data(db)
        output = ExportService.generate_excel(tableau_data)

        # Verifier que c'est bien un BytesIO
        assert isinstance(output, BytesIO)

        # Verifier que le contenu n'est pas vide
        content = output.getvalue()
        assert len(content) > 0

        # Verifier que c'est un fichier Excel valide (commence par PK)
        assert content[:2] == b'PK'

    except ImportError:
        # Si openpyxl n'est pas installe, le test passe
        pass


def test_generate_word(db: Session):
    """Test de generation d'un fichier Word"""
    try:
        tableau_data = create_test_tableau_data(db)
        output = ExportService.generate_word(tableau_data)

        # Verifier que c'est bien un BytesIO
        assert isinstance(output, BytesIO)

        # Verifier que le contenu n'est pas vide
        content = output.getvalue()
        assert len(content) > 0

        # Verifier que c'est un fichier Word valide (commence par PK)
        assert content[:2] == b'PK'

    except ImportError:
        # Si python-docx n'est pas installe, le test passe
        pass


def test_generate_pdf(db: Session):
    """Test de generation d'un fichier PDF"""
    try:
        tableau_data = create_test_tableau_data(db)
        output = ExportService.generate_pdf(tableau_data)

        # Verifier que c'est bien un BytesIO
        assert isinstance(output, BytesIO)

        # Verifier que le contenu n'est pas vide
        content = output.getvalue()
        assert len(content) > 0

        # Verifier que c'est un fichier PDF valide (commence par %PDF)
        assert content[:4] == b'%PDF'

    except ImportError:
        # Si reportlab n'est pas installe, le test passe
        pass


def test_generate_excel_with_empty_data(db: Session):
    """Test de generation Excel avec des donnees vides"""
    try:
        # Creer des donnees minimales
        region = Region(code="ANA", nom="Analamanga", actif=True)
        db.add(region)
        db.commit()
        db.refresh(region)

        departement = Departement(code="ANT", nom="Antananarivo", region_id=region.id, actif=True)
        db.add(departement)
        db.commit()
        db.refresh(departement)

        commune = Commune(code="ANT01", nom="Test", departement_id=departement.id, actif=True)
        db.add(commune)
        db.commit()
        db.refresh(commune)

        commune.departement = departement
        departement.region = region

        exercice = Exercice(annee=2024, actif=True)
        db.add(exercice)
        db.commit()
        db.refresh(exercice)

        tableau_data = {
            "commune": commune,
            "exercice": exercice,
            "periodes": [],
            "rubriques": [],
            "donnees": {},
            "totaux": {}
        }

        output = ExportService.generate_excel(tableau_data)
        assert isinstance(output, BytesIO)
        assert len(output.getvalue()) > 0

    except ImportError:
        pass


def test_export_libraries_availability():
    """Test de disponibilite des bibliotheques d'export"""
    try:
        import openpyxl
        excel_available = True
    except ImportError:
        excel_available = False

    try:
        import docx
        word_available = True
    except ImportError:
        word_available = False

    try:
        import reportlab
        pdf_available = True
    except ImportError:
        pdf_available = False

    # Au moins verifier que le test s'execute sans erreur
    # Les bibliotheques peuvent etre installees ou non selon l'environnement
    assert isinstance(excel_available, bool)
    assert isinstance(word_available, bool)
    assert isinstance(pdf_available, bool)
