"""
Page d'analyses pour l'application D-Tracker
"""

import streamlit as st
from database import ExpenseDatabase
from components.charts import render_category_analysis, render_category_evolution
from utils.date_utils import get_period_dates
from config.settings import CSS_STYLES

# Application du CSS personnalisé
st.markdown(CSS_STYLES, unsafe_allow_html=True)

st.header("Analyses Détaillées")

# Initialisation de la base de données
db = ExpenseDatabase()

# Sélecteur de période
period_options = ["jour", "semaine", "mois", "année", "tout"]
selected_period = st.selectbox(
    "Période",
    options=period_options,
    index=3,  # Par défaut sur "mois"
    key="analysis_period"
)

# Calculer les dates selon la période sélectionnée
start_date, end_date, _, _, period_label, _ = get_period_dates(selected_period)
analysis_start_str = start_date
analysis_end_str = end_date

# Affichage de la période sélectionnée
st.caption(f"Période : {period_label}")

# Récupérer toutes les catégories disponibles pour cette période
category_analysis = db.get_stats_by_category(analysis_start_str, analysis_end_str)
available_categories = category_analysis['category'].tolist() if len(category_analysis) > 0 else []

# Sélecteur de catégories pour le graphique en courbes
if available_categories:
    st.subheader("Évolution des Dépenses par Catégorie")
    
    # Multi-sélecteur de catégories
    selected_categories = st.multiselect(
        "Sélectionner les catégories à afficher",
        options=available_categories,
        default=available_categories[:min(5, len(available_categories))],  # Par défaut, afficher les 5 premières
        key="selected_categories_evolution"
    )
    
    if selected_categories:
        # Récupérer les dépenses quotidiennes par catégorie
        daily_by_category = db.get_daily_expenses_by_category(
            analysis_start_str,
            analysis_end_str,
            selected_categories
        )
        
        # Afficher le graphique en courbes
        render_category_evolution(daily_by_category, selected_categories)
    else:
        st.info("Veuillez sélectionner au moins une catégorie pour afficher le graphique.")
    
    st.divider()

# Analyse par catégorie (graphiques barres et camembert)
st.subheader("Analyse par Catégorie")
render_category_analysis(category_analysis)
