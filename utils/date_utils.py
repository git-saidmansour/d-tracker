"""
Utilitaires de date pour l'application D-Tracker
"""

from datetime import datetime, timedelta

def get_period_dates(period_choice):
    """
    Obtient les dates de début et de fin pour un choix de période donné
    
    Args:
        period_choice (str): Choix de période (jour, semaine, mois, année, tout)
    
    Returns:
        tuple: (start_date, end_date, period_label, prev_label)
    """
    today = datetime.now()
    
    if period_choice == "jour":
        start_date = today.strftime("%Y-%m-%d")
        end_date = today.strftime("%Y-%m-%d")
        # Période précédente (hier)
        prev_start = (today - timedelta(days=1)).strftime("%Y-%m-%d")
        prev_end = (today - timedelta(days=1)).strftime("%Y-%m-%d")
        period_label = "Aujourd'hui"
        prev_label = "Hier"
        
    elif period_choice == "semaine":
        # Semaine actuelle (lundi à dimanche)
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        start_date = start_of_week.strftime("%Y-%m-%d")
        end_date = end_of_week.strftime("%Y-%m-%d")
        # Semaine précédente
        prev_start_of_week = start_of_week - timedelta(days=7)
        prev_end_of_week = prev_start_of_week + timedelta(days=6)
        prev_start = prev_start_of_week.strftime("%Y-%m-%d")
        prev_end = prev_end_of_week.strftime("%Y-%m-%d")
        period_label = "Cette Semaine"
        prev_label = "Semaine Précédente"
        
    elif period_choice == "mois":
        # Mois actuel
        start_date = today.strftime("%Y-%m-01")
        end_date = today.strftime("%Y-%m-%d")
        # Mois précédent
        prev_month = today.replace(day=1) - timedelta(days=1)
        prev_start = prev_month.strftime("%Y-%m-01")
        prev_end = prev_month.strftime("%Y-%m-%d")
        period_label = "Ce Mois"
        prev_label = "Mois Précédent"
        
    elif period_choice == "année":
        # Année actuelle
        start_date = today.strftime("%Y-01-01")
        end_date = today.strftime("%Y-%m-%d")
        # Année précédente
        prev_year = today.replace(year=today.year-1)
        prev_start = prev_year.strftime("%Y-01-01")
        prev_end = prev_year.strftime("%Y-12-31")
        period_label = "Cette Année"
        prev_label = "Année Précédente"
        
    else:  # tout
        # Toutes les données
        start_date = None
        end_date = None
        # Période précédente (même durée que la période actuelle)
        # Pour "tout", on compare avec la période précédente de même durée
        # On prend les 30 derniers jours vs les 30 jours précédents
        start_date = (today - timedelta(days=30)).strftime("%Y-%m-%d")
        end_date = today.strftime("%Y-%m-%d")
        prev_start = (today - timedelta(days=60)).strftime("%Y-%m-%d")
        prev_end = (today - timedelta(days=30)).strftime("%Y-%m-%d")
        period_label = "Toutes Périodes"
        prev_label = "Période Précédente"
    
    return start_date, end_date, prev_start, prev_end, period_label, prev_label

