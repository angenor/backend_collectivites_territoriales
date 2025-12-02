"""
Service de validation des données financières.
Vérifie la cohérence comptable et les règles métier.
"""

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional

from sqlalchemy.orm import Session

from app.models.comptabilite import DonneesDepenses, DonneesRecettes, Exercice, PlanComptable
from app.models.enums import TypeMouvement


@dataclass
class ValidationError:
    """Erreur de validation."""
    code: str
    message: str
    champ: Optional[str] = None
    valeur: Optional[str] = None


@dataclass
class ValidationResult:
    """Résultat de validation."""
    valide: bool
    erreurs: list[ValidationError] = field(default_factory=list)
    avertissements: list[ValidationError] = field(default_factory=list)


class ValidationService:
    """
    Service pour la validation des données saisies.
    Vérifie les règles métier et la cohérence comptable.
    """

    # Règles métier
    MONTANT_MIN = Decimal("0")
    MONTANT_MAX = Decimal("999999999999.99")  # 999 milliards max

    def valider_montant(
        self,
        montant: Optional[Decimal],
        champ: str = "montant",
        obligatoire: bool = False,
    ) -> list[ValidationError]:
        """
        Valide un montant financier.

        Règles:
        - Doit être positif ou nul
        - Ne doit pas dépasser le maximum autorisé
        - Peut être obligatoire
        """
        erreurs = []

        if montant is None:
            if obligatoire:
                erreurs.append(ValidationError(
                    code="MONTANT_REQUIS",
                    message=f"Le champ {champ} est obligatoire",
                    champ=champ,
                ))
            return erreurs

        if montant < self.MONTANT_MIN:
            erreurs.append(ValidationError(
                code="MONTANT_NEGATIF",
                message=f"Le {champ} ne peut pas être négatif",
                champ=champ,
                valeur=str(montant),
            ))

        if montant > self.MONTANT_MAX:
            erreurs.append(ValidationError(
                code="MONTANT_TROP_GRAND",
                message=f"Le {champ} dépasse le maximum autorisé",
                champ=champ,
                valeur=str(montant),
            ))

        return erreurs

    def valider_coherence_budget(
        self,
        budget_primitif: Optional[Decimal],
        budget_supplementaire: Optional[Decimal],
        realisation: Optional[Decimal],
    ) -> list[ValidationError]:
        """
        Valide la cohérence entre les différents montants budgétaires.

        Avertissements (pas d'erreurs bloquantes):
        - Réalisation > Prévision définitive (sur-exécution)
        - Budget supplémentaire > Budget primitif (modification importante)
        """
        avertissements = []

        bp = budget_primitif or Decimal("0")
        bs = budget_supplementaire or Decimal("0")
        real = realisation or Decimal("0")
        prevision_def = bp + bs

        # Sur-exécution
        if real > prevision_def and prevision_def > Decimal("0"):
            taux = (real / prevision_def - 1) * 100
            avertissements.append(ValidationError(
                code="SUR_EXECUTION",
                message=f"Réalisation supérieure à la prévision (+{taux:.1f}%)",
                champ="realisation",
                valeur=str(real),
            ))

        # Modification budgétaire importante
        if bp > Decimal("0") and abs(bs) > bp * Decimal("0.5"):
            avertissements.append(ValidationError(
                code="MODIFICATION_IMPORTANTE",
                message="Budget supplémentaire représente plus de 50% du budget primitif",
                champ="budget_supplementaire",
                valeur=str(bs),
            ))

        return avertissements

    def valider_compte_existe(
        self,
        db: Session,
        compte_code: str,
        type_mouvement: TypeMouvement,
    ) -> list[ValidationError]:
        """
        Vérifie que le compte existe et correspond au type de mouvement.
        """
        erreurs = []

        compte = db.query(PlanComptable).filter(
            PlanComptable.code == compte_code
        ).first()

        if not compte:
            erreurs.append(ValidationError(
                code="COMPTE_INEXISTANT",
                message=f"Le compte {compte_code} n'existe pas dans le plan comptable",
                champ="compte_code",
                valeur=compte_code,
            ))
            return erreurs

        # Vérifier le type de mouvement
        if compte.type_mouvement != type_mouvement:
            erreurs.append(ValidationError(
                code="TYPE_MOUVEMENT_INCORRECT",
                message=f"Le compte {compte_code} est de type {compte.type_mouvement.value}, "
                        f"attendu {type_mouvement.value}",
                champ="compte_code",
                valeur=compte_code,
            ))

        # Vérifier que c'est un compte de niveau 3 (saisie autorisée)
        if compte.niveau != 3:
            erreurs.append(ValidationError(
                code="NIVEAU_COMPTE_INCORRECT",
                message=f"Seuls les comptes de niveau 3 peuvent être saisis "
                        f"(compte {compte_code} est de niveau {compte.niveau})",
                champ="compte_code",
                valeur=compte_code,
            ))

        return erreurs

    def valider_exercice_ouvert(
        self,
        db: Session,
        exercice_id: int,
    ) -> list[ValidationError]:
        """
        Vérifie que l'exercice n'est pas clôturé.
        """
        erreurs = []

        exercice = db.query(Exercice).filter(Exercice.id == exercice_id).first()

        if not exercice:
            erreurs.append(ValidationError(
                code="EXERCICE_INEXISTANT",
                message="L'exercice spécifié n'existe pas",
                champ="exercice_id",
                valeur=str(exercice_id),
            ))
            return erreurs

        if exercice.cloture:
            erreurs.append(ValidationError(
                code="EXERCICE_CLOTURE",
                message=f"L'exercice {exercice.annee} est clôturé et ne peut plus être modifié",
                champ="exercice_id",
                valeur=str(exercice_id),
            ))

        return erreurs

    def valider_unicite_saisie(
        self,
        db: Session,
        commune_id: int,
        exercice_id: int,
        compte_code: str,
        type_mouvement: TypeMouvement,
        exclude_id: Optional[int] = None,
    ) -> list[ValidationError]:
        """
        Vérifie qu'il n'existe pas déjà une saisie pour ce compte/commune/exercice.
        """
        erreurs = []

        if type_mouvement == TypeMouvement.RECETTE:
            query = db.query(DonneesRecettes).filter(
                DonneesRecettes.commune_id == commune_id,
                DonneesRecettes.exercice_id == exercice_id,
                DonneesRecettes.compte_code == compte_code,
            )
            if exclude_id:
                query = query.filter(DonneesRecettes.id != exclude_id)
            existing = query.first()
        else:
            query = db.query(DonneesDepenses).filter(
                DonneesDepenses.commune_id == commune_id,
                DonneesDepenses.exercice_id == exercice_id,
                DonneesDepenses.compte_code == compte_code,
            )
            if exclude_id:
                query = query.filter(DonneesDepenses.id != exclude_id)
            existing = query.first()

        if existing:
            erreurs.append(ValidationError(
                code="SAISIE_DUPLIQUEE",
                message=f"Une saisie existe déjà pour le compte {compte_code} "
                        f"sur cet exercice et cette commune",
                champ="compte_code",
                valeur=compte_code,
            ))

        return erreurs

    def valider_recette(
        self,
        db: Session,
        commune_id: int,
        exercice_id: int,
        compte_code: str,
        budget_primitif: Optional[Decimal],
        budget_supplementaire: Optional[Decimal],
        realisation: Optional[Decimal],
        exclude_id: Optional[int] = None,
    ) -> ValidationResult:
        """
        Validation complète d'une ligne de recette.
        """
        erreurs = []
        avertissements = []

        # Validation des montants
        erreurs.extend(self.valider_montant(budget_primitif, "budget_primitif"))
        erreurs.extend(self.valider_montant(budget_supplementaire, "budget_supplementaire"))
        erreurs.extend(self.valider_montant(realisation, "realisation"))

        # Validation du compte
        erreurs.extend(self.valider_compte_existe(db, compte_code, TypeMouvement.RECETTE))

        # Validation de l'exercice
        erreurs.extend(self.valider_exercice_ouvert(db, exercice_id))

        # Validation unicité
        erreurs.extend(self.valider_unicite_saisie(
            db, commune_id, exercice_id, compte_code, TypeMouvement.RECETTE, exclude_id
        ))

        # Cohérence budgétaire (avertissements)
        avertissements.extend(self.valider_coherence_budget(
            budget_primitif, budget_supplementaire, realisation
        ))

        return ValidationResult(
            valide=len(erreurs) == 0,
            erreurs=erreurs,
            avertissements=avertissements,
        )

    def valider_depense(
        self,
        db: Session,
        commune_id: int,
        exercice_id: int,
        compte_code: str,
        budget_primitif: Optional[Decimal],
        budget_supplementaire: Optional[Decimal],
        realisation: Optional[Decimal],
        exclude_id: Optional[int] = None,
    ) -> ValidationResult:
        """
        Validation complète d'une ligne de dépense.
        """
        erreurs = []
        avertissements = []

        # Validation des montants
        erreurs.extend(self.valider_montant(budget_primitif, "budget_primitif"))
        erreurs.extend(self.valider_montant(budget_supplementaire, "budget_supplementaire"))
        erreurs.extend(self.valider_montant(realisation, "realisation"))

        # Validation du compte
        erreurs.extend(self.valider_compte_existe(db, compte_code, TypeMouvement.DEPENSE))

        # Validation de l'exercice
        erreurs.extend(self.valider_exercice_ouvert(db, exercice_id))

        # Validation unicité
        erreurs.extend(self.valider_unicite_saisie(
            db, commune_id, exercice_id, compte_code, TypeMouvement.DEPENSE, exclude_id
        ))

        # Cohérence budgétaire (avertissements)
        avertissements.extend(self.valider_coherence_budget(
            budget_primitif, budget_supplementaire, realisation
        ))

        return ValidationResult(
            valide=len(erreurs) == 0,
            erreurs=erreurs,
            avertissements=avertissements,
        )

    def valider_cloture_exercice(
        self,
        db: Session,
        exercice_id: int,
    ) -> ValidationResult:
        """
        Valide qu'un exercice peut être clôturé.

        Vérifie:
        - Toutes les données sont validées
        - Au moins une commune a des données
        """
        erreurs = []
        avertissements = []

        exercice = db.query(Exercice).filter(Exercice.id == exercice_id).first()
        if not exercice:
            erreurs.append(ValidationError(
                code="EXERCICE_INEXISTANT",
                message="L'exercice n'existe pas",
                champ="exercice_id",
            ))
            return ValidationResult(valide=False, erreurs=erreurs)

        if exercice.cloture:
            erreurs.append(ValidationError(
                code="DEJA_CLOTURE",
                message="L'exercice est déjà clôturé",
                champ="exercice_id",
            ))
            return ValidationResult(valide=False, erreurs=erreurs)

        # Vérifier qu'il y a des données
        nb_recettes = db.query(DonneesRecettes).filter(
            DonneesRecettes.exercice_id == exercice_id
        ).count()
        nb_depenses = db.query(DonneesDepenses).filter(
            DonneesDepenses.exercice_id == exercice_id
        ).count()

        if nb_recettes == 0 and nb_depenses == 0:
            erreurs.append(ValidationError(
                code="EXERCICE_VIDE",
                message="Aucune donnée n'a été saisie pour cet exercice",
            ))

        # Vérifier les données non validées
        recettes_non_validees = db.query(DonneesRecettes).filter(
            DonneesRecettes.exercice_id == exercice_id,
            DonneesRecettes.valide == False,
        ).count()
        depenses_non_validees = db.query(DonneesDepenses).filter(
            DonneesDepenses.exercice_id == exercice_id,
            DonneesDepenses.valide == False,
        ).count()

        if recettes_non_validees > 0 or depenses_non_validees > 0:
            avertissements.append(ValidationError(
                code="DONNEES_NON_VALIDEES",
                message=f"{recettes_non_validees} recettes et {depenses_non_validees} dépenses "
                        f"n'ont pas été validées",
            ))

        return ValidationResult(
            valide=len(erreurs) == 0,
            erreurs=erreurs,
            avertissements=avertissements,
        )


# Singleton instance
validation_service = ValidationService()
