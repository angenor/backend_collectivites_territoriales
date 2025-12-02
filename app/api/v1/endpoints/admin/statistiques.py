"""
Admin Statistics API endpoints.
Dashboard statistics and audit log viewing.
"""

from datetime import date, datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from app.api.deps import CurrentAdmin, get_db
from app.models.annexes import AuditLog, StatistiqueVisite
from app.models.comptabilite import DonneesDepenses, DonneesRecettes, Exercice
from app.models.documents import Document
from app.models.enums import ActionAudit
from app.models.geographie import Commune, Province, Region
from app.models.projets_miniers import ProjetMinier, RevenuMinier
from app.models.utilisateurs import Utilisateur
from app.schemas.documents import AuditLogRead

router = APIRouter(prefix="/statistiques", tags=["Admin - Statistiques"])


# =====================
# Dashboard Statistics
# =====================


@router.get(
    "/dashboard",
    response_model=dict,
    summary="Tableau de bord admin",
    description="Statistiques globales pour le tableau de bord administrateur.",
)
async def dashboard_stats(
    current_user: CurrentAdmin = None,
    db: Session = Depends(get_db),
):
    """
    Get admin dashboard statistics.
    """
    today = date.today()
    thirty_days_ago = today - timedelta(days=30)
    seven_days_ago = today - timedelta(days=7)

    # User stats
    total_users = db.query(func.count(Utilisateur.id)).scalar()
    active_users = db.query(func.count(Utilisateur.id)).filter(Utilisateur.actif == True).scalar()

    # Content stats
    total_exercices = db.query(func.count(Exercice.id)).scalar()
    exercices_publies = db.query(func.count(Exercice.id)).filter(Exercice.publie == True).scalar()
    total_documents = db.query(func.count(Document.id)).scalar()

    # Financial totals
    total_recettes = db.query(func.sum(DonneesRecettes.realisation)).scalar() or 0
    total_depenses = db.query(func.sum(DonneesDepenses.realisation)).scalar() or 0

    # Visit stats
    visites_30j = db.query(func.sum(StatistiqueVisite.nb_visites)).filter(
        StatistiqueVisite.date_visite >= thirty_days_ago
    ).scalar() or 0

    visites_7j = db.query(func.sum(StatistiqueVisite.nb_visites)).filter(
        StatistiqueVisite.date_visite >= seven_days_ago
    ).scalar() or 0

    telechargements_30j = db.query(func.sum(StatistiqueVisite.nb_telechargements)).filter(
        StatistiqueVisite.date_visite >= thirty_days_ago
    ).scalar() or 0

    # Recent activity
    recent_audit = db.query(func.count(AuditLog.id)).filter(
        AuditLog.created_at >= datetime.utcnow() - timedelta(days=7)
    ).scalar()

    return {
        "utilisateurs": {
            "total": total_users,
            "actifs": active_users,
        },
        "contenu": {
            "exercices_total": total_exercices,
            "exercices_publies": exercices_publies,
            "documents": total_documents,
        },
        "finances": {
            "recettes_totales": float(total_recettes),
            "depenses_totales": float(total_depenses),
            "solde_global": float(total_recettes - total_depenses),
        },
        "visites": {
            "dernieres_30_jours": visites_30j,
            "dernieres_7_jours": visites_7j,
            "telechargements_30_jours": telechargements_30j,
        },
        "activite": {
            "modifications_7_jours": recent_audit,
        },
    }


@router.get(
    "/visites",
    response_model=dict,
    summary="Statistiques de visites détaillées",
    description="Statistiques de visites avec filtres et agrégations.",
)
async def visit_stats(
    date_debut: Optional[date] = Query(None, description="Date de début"),
    date_fin: Optional[date] = Query(None, description="Date de fin"),
    commune_id: Optional[int] = Query(None, description="Filtrer par commune"),
    group_by: str = Query("day", description="Grouper par: day, week, month"),
    current_user: CurrentAdmin = None,
    db: Session = Depends(get_db),
):
    """
    Get detailed visit statistics.
    """
    # Default to last 30 days
    if not date_fin:
        date_fin = date.today()
    if not date_debut:
        date_debut = date_fin - timedelta(days=30)

    query = db.query(StatistiqueVisite).filter(
        StatistiqueVisite.date_visite >= date_debut,
        StatistiqueVisite.date_visite <= date_fin,
    )

    if commune_id:
        query = query.filter(StatistiqueVisite.commune_id == commune_id)

    # Get raw data
    stats = query.all()

    # Aggregate by period
    if group_by == "month":
        truncate_func = func.date_trunc('month', StatistiqueVisite.date_visite)
    elif group_by == "week":
        truncate_func = func.date_trunc('week', StatistiqueVisite.date_visite)
    else:
        truncate_func = StatistiqueVisite.date_visite

    grouped_query = db.query(
        truncate_func.label('periode'),
        func.sum(StatistiqueVisite.nb_visites).label('visites'),
        func.sum(StatistiqueVisite.nb_telechargements).label('telechargements'),
    ).filter(
        StatistiqueVisite.date_visite >= date_debut,
        StatistiqueVisite.date_visite <= date_fin,
    )

    if commune_id:
        grouped_query = grouped_query.filter(StatistiqueVisite.commune_id == commune_id)

    grouped = grouped_query.group_by(truncate_func).order_by(truncate_func).all()

    # Top pages
    top_pages = db.query(
        StatistiqueVisite.page,
        func.sum(StatistiqueVisite.nb_visites).label('visites'),
    ).filter(
        StatistiqueVisite.date_visite >= date_debut,
        StatistiqueVisite.date_visite <= date_fin,
    ).group_by(
        StatistiqueVisite.page
    ).order_by(
        func.sum(StatistiqueVisite.nb_visites).desc()
    ).limit(10).all()

    # Top communes
    top_communes = db.query(
        Commune.nom,
        func.sum(StatistiqueVisite.nb_visites).label('visites'),
    ).join(
        StatistiqueVisite,
        StatistiqueVisite.commune_id == Commune.id
    ).filter(
        StatistiqueVisite.date_visite >= date_debut,
        StatistiqueVisite.date_visite <= date_fin,
    ).group_by(
        Commune.id, Commune.nom
    ).order_by(
        func.sum(StatistiqueVisite.nb_visites).desc()
    ).limit(10).all()

    return {
        "periode": {
            "debut": date_debut.isoformat(),
            "fin": date_fin.isoformat(),
        },
        "totaux": {
            "visites": sum(s.nb_visites for s in stats),
            "telechargements": sum(s.nb_telechargements for s in stats),
        },
        "evolution": [
            {
                "periode": p.isoformat() if hasattr(p, 'isoformat') else str(p),
                "visites": v,
                "telechargements": t,
            }
            for p, v, t in grouped
        ],
        "top_pages": [
            {"page": p, "visites": v}
            for p, v in top_pages if p
        ],
        "top_communes": [
            {"commune": n, "visites": v}
            for n, v in top_communes
        ],
    }


@router.get(
    "/telechargements",
    response_model=dict,
    summary="Statistiques de téléchargements",
    description="Statistiques des téléchargements de documents.",
)
async def download_stats(
    date_debut: Optional[date] = Query(None, description="Date de début"),
    date_fin: Optional[date] = Query(None, description="Date de fin"),
    current_user: CurrentAdmin = None,
    db: Session = Depends(get_db),
):
    """
    Get document download statistics.
    """
    if not date_fin:
        date_fin = date.today()
    if not date_debut:
        date_debut = date_fin - timedelta(days=30)

    # Most downloaded documents
    top_documents = db.query(
        Document.id,
        Document.titre,
        Document.type_document,
        Document.nb_telechargements,
    ).filter(
        Document.nb_telechargements > 0
    ).order_by(
        Document.nb_telechargements.desc()
    ).limit(20).all()

    # Downloads by type
    by_type = db.query(
        Document.type_document,
        func.sum(Document.nb_telechargements).label('total'),
    ).group_by(
        Document.type_document
    ).all()

    # Total downloads
    total_downloads = db.query(func.sum(Document.nb_telechargements)).scalar() or 0

    return {
        "periode": {
            "debut": date_debut.isoformat(),
            "fin": date_fin.isoformat(),
        },
        "total_telechargements": total_downloads,
        "par_type": {
            t.value if hasattr(t, 'value') else str(t): d
            for t, d in by_type if d
        },
        "top_documents": [
            {
                "id": d.id,
                "titre": d.titre,
                "type": d.type_document.value if hasattr(d.type_document, 'value') else str(d.type_document),
                "telechargements": d.nb_telechargements,
            }
            for d in top_documents
        ],
    }


# =====================
# Audit Log
# =====================


@router.get(
    "/audit",
    response_model=list[AuditLogRead],
    summary="Journal d'audit",
    description="Consulte le journal des modifications.",
)
async def list_audit_logs(
    table_name: Optional[str] = Query(None, description="Filtrer par table"),
    record_id: Optional[int] = Query(None, description="Filtrer par ID d'enregistrement"),
    action: Optional[ActionAudit] = Query(None, description="Filtrer par action"),
    utilisateur_id: Optional[int] = Query(None, description="Filtrer par utilisateur"),
    date_debut: Optional[datetime] = Query(None, description="Date de début"),
    date_fin: Optional[datetime] = Query(None, description="Date de fin"),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    current_user: CurrentAdmin = None,
    db: Session = Depends(get_db),
):
    """
    List audit log entries with filters.
    """
    query = db.query(AuditLog).options(joinedload(AuditLog.utilisateur))

    if table_name:
        query = query.filter(AuditLog.table_name == table_name)
    if record_id:
        query = query.filter(AuditLog.record_id == record_id)
    if action:
        query = query.filter(AuditLog.action == action)
    if utilisateur_id:
        query = query.filter(AuditLog.utilisateur_id == utilisateur_id)
    if date_debut:
        query = query.filter(AuditLog.created_at >= date_debut)
    if date_fin:
        query = query.filter(AuditLog.created_at <= date_fin)

    logs = query.order_by(AuditLog.created_at.desc()).offset(offset).limit(limit).all()

    return [
        AuditLogRead(
            id=log.id,
            table_name=log.table_name,
            record_id=log.record_id,
            action=log.action.value,
            old_values=log.old_values,
            new_values=log.new_values,
            utilisateur_id=log.utilisateur_id,
            ip_address=log.ip_address,
            created_at=log.created_at,
            utilisateur_email=log.utilisateur.email if log.utilisateur else None,
        )
        for log in logs
    ]


@router.get(
    "/audit/{log_id}",
    response_model=AuditLogRead,
    summary="Détails d'une entrée d'audit",
    description="Retourne les détails d'une entrée du journal d'audit.",
)
async def get_audit_log(
    log_id: int,
    current_user: CurrentAdmin = None,
    db: Session = Depends(get_db),
):
    """
    Get audit log entry details.
    """
    log = db.query(AuditLog).options(
        joinedload(AuditLog.utilisateur)
    ).filter(AuditLog.id == log_id).first()

    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entrée d'audit non trouvée.",
        )

    return AuditLogRead(
        id=log.id,
        table_name=log.table_name,
        record_id=log.record_id,
        action=log.action.value,
        old_values=log.old_values,
        new_values=log.new_values,
        utilisateur_id=log.utilisateur_id,
        ip_address=log.ip_address,
        created_at=log.created_at,
        utilisateur_email=log.utilisateur.email if log.utilisateur else None,
    )


@router.get(
    "/audit/tables",
    response_model=list[str],
    summary="Liste des tables auditées",
    description="Retourne la liste des tables présentes dans le journal d'audit.",
)
async def list_audited_tables(
    current_user: CurrentAdmin = None,
    db: Session = Depends(get_db),
):
    """
    List tables that have audit entries.
    """
    tables = db.query(func.distinct(AuditLog.table_name)).order_by(AuditLog.table_name).all()
    return [t[0] for t in tables]


@router.get(
    "/audit/summary",
    response_model=dict,
    summary="Résumé de l'audit",
    description="Résumé statistique du journal d'audit.",
)
async def audit_summary(
    days: int = Query(30, ge=1, le=365, description="Nombre de jours à analyser"),
    current_user: CurrentAdmin = None,
    db: Session = Depends(get_db),
):
    """
    Get audit log summary statistics.
    """
    since = datetime.utcnow() - timedelta(days=days)

    # Total entries
    total = db.query(func.count(AuditLog.id)).filter(
        AuditLog.created_at >= since
    ).scalar()

    # By action
    by_action = db.query(
        AuditLog.action,
        func.count(AuditLog.id).label('count')
    ).filter(
        AuditLog.created_at >= since
    ).group_by(AuditLog.action).all()

    # By table
    by_table = db.query(
        AuditLog.table_name,
        func.count(AuditLog.id).label('count')
    ).filter(
        AuditLog.created_at >= since
    ).group_by(AuditLog.table_name).order_by(
        func.count(AuditLog.id).desc()
    ).limit(10).all()

    # Most active users
    top_users = db.query(
        Utilisateur.email,
        func.count(AuditLog.id).label('count')
    ).join(
        AuditLog,
        AuditLog.utilisateur_id == Utilisateur.id
    ).filter(
        AuditLog.created_at >= since
    ).group_by(
        Utilisateur.id, Utilisateur.email
    ).order_by(
        func.count(AuditLog.id).desc()
    ).limit(10).all()

    return {
        "periode_jours": days,
        "total_entries": total,
        "par_action": {
            a.value if hasattr(a, 'value') else str(a): c
            for a, c in by_action
        },
        "par_table": {
            t: c for t, c in by_table
        },
        "utilisateurs_actifs": [
            {"email": e, "modifications": c}
            for e, c in top_users
        ],
    }
