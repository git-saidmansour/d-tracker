"""
Page d'analyses pour l'application D-Tracker
"""

import streamlit as st
from datetime import datetime, timedelta
from database import ExpenseDatabase
from components.charts import render_category_analysis, render_category_evolution
from utils.date_utils import get_period_dates
from config.settings import CSS_STYLES

# Application du CSS personnalisé
st.markdown(CSS_STYLES, unsafe_allow_html=True)

st.header("Analyses Détaillées")

# Initialisation de la base de données
db = ExpenseDatabase()

# Sélecteur de période pour la section "Analyse par Catégorie"
st.subheader("Analyse par Catégorie")
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

# Graphiques barres et camembert
render_category_analysis(category_analysis)

st.divider()

# Section Évolution des Dépenses par Catégorie avec intervalle personnalisé
if available_categories:
    st.subheader("Évolution des Dépenses par Catégorie")
    
    # Choix du type de période pour le graphique en courbes
    evolution_period_type = st.radio(
        "Type de période",
        options=["Période prédéfinie", "Intervalle personnalisé"],
        index=0,
        key="evolution_period_type",
        horizontal=True
    )
    
    # Dates pour le graphique en courbes
    if evolution_period_type == "Période prédéfinie":
        # Utiliser les mêmes dates que la section précédente
        evolution_start_str = analysis_start_str
        evolution_end_str = analysis_end_str
        evolution_label = period_label
        st.caption(f"Période : {evolution_label}")
    else:
        # Intervalle personnalisé
        col1, col2 = st.columns(2)
        with col1:
            evolution_start = st.date_input(
                "Date de début",
                value=datetime.now() - timedelta(days=30),
                key="evolution_start_date"
            )
        with col2:
            evolution_end = st.date_input(
                "Date de fin",
                value=datetime.now(),
                key="evolution_end_date"
            )
        
        # Vérifier que la date de fin est après la date de début
        if evolution_end < evolution_start:
            st.error("La date de fin doit être postérieure à la date de début.")
            evolution_start_str = None
            evolution_end_str = None
        else:
            evolution_start_str = evolution_start.strftime("%Y-%m-%d")
            evolution_end_str = evolution_end.strftime("%Y-%m-%d")
            evolution_label = f"Du {evolution_start.strftime('%d/%m/%Y')} au {evolution_end.strftime('%d/%m/%Y')}"
            st.caption(f"Période : {evolution_label}")
        
        if evolution_start_str and evolution_end_str:
            # Récupérer les catégories disponibles pour cette période personnalisée
            evolution_category_analysis = db.get_stats_by_category(evolution_start_str, evolution_end_str)
            available_categories = evolution_category_analysis['category'].tolist() if len(evolution_category_analysis) > 0 else []
    
    # Multi-sélecteur de catégories
    if evolution_start_str and evolution_end_str:
        selected_categories = st.multiselect(
            "Sélectionner les catégories à afficher",
            options=available_categories,
            default=available_categories[:min(5, len(available_categories))] if available_categories else [],
            key="selected_categories_evolution"
        )
        
        if selected_categories:
            # Récupérer les dépenses quotidiennes par catégorie
            daily_by_category = db.get_daily_expenses_by_category(
                evolution_start_str,
                evolution_end_str,
                selected_categories
            )
            
            # Afficher le graphique en courbes
            render_category_evolution(daily_by_category, selected_categories)
        else:
            st.info("Veuillez sélectionner au moins une catégorie pour afficher le graphique.")
    else:
        st.info("Veuillez sélectionner un intervalle de dates valide.")
