"""
Page Dashboard pour l'application D-Tracker
"""

import streamlit as st
from datetime import datetime, timedelta
from database import ExpenseDatabase
from components.metrics import render_summary_metrics
from components.charts import render_category_progress, render_daily_evolution
from utils.date_utils import get_period_dates
from config.settings import CSS_STYLES

# Application du CSS personnalisé
st.markdown(CSS_STYLES, unsafe_allow_html=True)

st.header("Dashboard")

# Initialisation de la base de données
db = ExpenseDatabase()

# Sélecteur de période
col_title, col_select = st.columns([3, 1])

with col_title:
    st.subheader("Résumé")

with col_select:
    period_choice = st.selectbox(
        "",
        ["jour", "semaine", "mois", "année", "tout"],
        key="dashboard_period",
        label_visibility="collapsed"
    )

# Obtention des dates de période
start_date, end_date, prev_start, prev_end, period_label, prev_label = get_period_dates(period_choice)

# Obtention des données de la période actuelle et précédente
current_expenses = db.get_total_expenses(start_date, end_date)
previous_expenses = db.get_total_expenses(prev_start, prev_end)

current_expenses_list = db.get_expenses(start_date, end_date)
previous_expenses_list = db.get_expenses(prev_start, prev_end)

current_count = len(current_expenses_list)
previous_count = len(previous_expenses_list)

# Rendu des métriques de résumé
render_summary_metrics(current_expenses, previous_expenses, current_count, previous_count)

st.markdown("---")

# Répartition par catégorie
st.subheader("Répartition par Catégorie")
category_stats = db.get_stats_by_category(start_date, end_date)
print(category_stats)
render_category_progress(category_stats)

# Graphique d'évolution quotidienne
st.subheader("Évolution des 7 Derniers Jours")
end_date_7_days = datetime.now()
start_date_7_days = end_date_7_days - timedelta(days=6)

daily_expenses = db.get_daily_expenses(
    start_date_7_days.strftime("%Y-%m-%d"), 
    end_date_7_days.strftime("%Y-%m-%d")
)

render_daily_evolution(daily_expenses)

