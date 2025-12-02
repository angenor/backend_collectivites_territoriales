"""
Service d'audit pour l'enregistrement des modifications.
Journalise toutes les opérations CRUD sur les données sensibles.
"""

from datetime import datetime
from typing import Any, Optional

from sqlalchemy.orm import Session

from app.models.annexes import AuditLog
from app.models.enums import ActionAudit


class AuditService:
    """
    Service pour l'enregistrement des actions dans le journal d'audit.
    """

    def log(
        self,
        db: Session,
        table_name: str,
        record_id: int,
        action: ActionAudit,
        old_values: Optional[dict] = None,
        new_values: Optional[dict] = None,
        utilisateur_id: Optional[int] = None,
        ip_address: Optional[str] = None,
    ) -> AuditLog:
        """
        Enregistre une action dans le journal d'audit.

        Args:
            db: Session de base de données
            table_name: Nom de la table concernée
            record_id: ID de l'enregistrement modifié
            action: Type d'action (INSERT, UPDATE, DELETE)
            old_values: Anciennes valeurs (pour UPDATE et DELETE)
            new_values: Nouvelles valeurs (pour INSERT et UPDATE)
            utilisateur_id: ID de l'utilisateur effectuant l'action
            ip_address: Adresse IP de l'utilisateur

        Returns:
            L'entrée d'audit créée
        """
        # Nettoyer les valeurs pour éviter les problèmes de sérialisation
        clean_old = self._clean_values(old_values) if old_values else None
        clean_new = self._clean_values(new_values) if new_values else None

        audit_entry = AuditLog(
            table_name=table_name,
            record_id=record_id,
            action=action,
            old_values=clean_old,
            new_values=clean_new,
            utilisateur_id=utilisateur_id,
            ip_address=ip_address,
        )

        db.add(audit_entry)
        db.flush()  # Pour obtenir l'ID sans commit

        return audit_entry

    def log_insert(
        self,
        db: Session,
        table_name: str,
        record_id: int,
        new_values: dict,
        utilisateur_id: Optional[int] = None,
        ip_address: Optional[str] = None,
    ) -> AuditLog:
        """Raccourci pour enregistrer une insertion."""
        return self.log(
            db=db,
            table_name=table_name,
            record_id=record_id,
            action=ActionAudit.INSERT,
            old_values=None,
            new_values=new_values,
            utilisateur_id=utilisateur_id,
            ip_address=ip_address,
        )

    def log_update(
        self,
        db: Session,
        table_name: str,
        record_id: int,
        old_values: dict,
        new_values: dict,
        utilisateur_id: Optional[int] = None,
        ip_address: Optional[str] = None,
    ) -> AuditLog:
        """Raccourci pour enregistrer une modification."""
        return self.log(
            db=db,
            table_name=table_name,
            record_id=record_id,
            action=ActionAudit.UPDATE,
            old_values=old_values,
            new_values=new_values,
            utilisateur_id=utilisateur_id,
            ip_address=ip_address,
        )

    def log_delete(
        self,
        db: Session,
        table_name: str,
        record_id: int,
        old_values: dict,
        utilisateur_id: Optional[int] = None,
        ip_address: Optional[str] = None,
    ) -> AuditLog:
        """Raccourci pour enregistrer une suppression."""
        return self.log(
            db=db,
            table_name=table_name,
            record_id=record_id,
            action=ActionAudit.DELETE,
            old_values=old_values,
            new_values=None,
            utilisateur_id=utilisateur_id,
            ip_address=ip_address,
        )

    def get_history(
        self,
        db: Session,
        table_name: str,
        record_id: int,
        limit: int = 50,
    ) -> list[AuditLog]:
        """
        Récupère l'historique des modifications pour un enregistrement.

        Returns:
            Liste des entrées d'audit, les plus récentes en premier
        """
        return db.query(AuditLog).filter(
            AuditLog.table_name == table_name,
            AuditLog.record_id == record_id,
        ).order_by(AuditLog.created_at.desc()).limit(limit).all()

    def get_user_activity(
        self,
        db: Session,
        utilisateur_id: int,
        limit: int = 100,
    ) -> list[AuditLog]:
        """
        Récupère l'activité récente d'un utilisateur.

        Returns:
            Liste des actions de l'utilisateur
        """
        return db.query(AuditLog).filter(
            AuditLog.utilisateur_id == utilisateur_id,
        ).order_by(AuditLog.created_at.desc()).limit(limit).all()

    def get_recent_activity(
        self,
        db: Session,
        limit: int = 100,
        table_name: Optional[str] = None,
    ) -> list[AuditLog]:
        """
        Récupère l'activité récente globale.

        Returns:
            Liste des dernières actions
        """
        query = db.query(AuditLog)

        if table_name:
            query = query.filter(AuditLog.table_name == table_name)

        return query.order_by(AuditLog.created_at.desc()).limit(limit).all()

    def _clean_values(self, values: dict) -> dict:
        """
        Nettoie les valeurs pour la sérialisation JSON.

        Convertit les types non-sérialisables (datetime, Decimal, etc.)
        """
        if not values:
            return {}

        cleaned = {}
        for key, value in values.items():
            cleaned[key] = self._clean_value(value)

        return cleaned

    def _clean_value(self, value: Any) -> Any:
        """Convertit une valeur en type sérialisable."""
        if value is None:
            return None
        if isinstance(value, datetime):
            return value.isoformat()
        if hasattr(value, "value"):  # Enum
            return value.value
        if hasattr(value, "__decimal__") or str(type(value)) == "<class 'decimal.Decimal'>":
            return float(value)
        if isinstance(value, (list, tuple)):
            return [self._clean_value(v) for v in value]
        if isinstance(value, dict):
            return {k: self._clean_value(v) for k, v in value.items()}
        # Types de base (str, int, float, bool)
        return value

    def model_to_dict(self, model: Any, exclude: Optional[list[str]] = None) -> dict:
        """
        Convertit un modèle SQLAlchemy en dictionnaire pour l'audit.

        Args:
            model: Instance du modèle SQLAlchemy
            exclude: Liste des champs à exclure

        Returns:
            Dictionnaire des valeurs du modèle
        """
        exclude = exclude or []
        exclude.extend(["_sa_instance_state"])  # Toujours exclure l'état SQLAlchemy

        result = {}
        for column in model.__table__.columns:
            if column.name not in exclude:
                value = getattr(model, column.name, None)
                result[column.name] = self._clean_value(value)

        return result


# Singleton instance
audit_service = AuditService()
