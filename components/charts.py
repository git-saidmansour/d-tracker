"""
Composants de graphiques pour l'application D-Tracker
"""

import streamlit as st
import plotly.express as px
import pandas as pd

def render_category_progress(category_stats):
    """
    Rendu des barres de progression par catégorie
    
    Args:
        category_stats (DataFrame): Statistiques par catégorie
    """
    if len(category_stats) > 0:
        total_period = category_stats['total'].sum()
        
        for _, row in category_stats.iterrows():
            percentage = (row['total'] / total_period) * 100 if total_period > 0 else 0
            
            st.markdown(f"""
            <div class="progress-container">
                <div class="category-name">
                    {row['category']} - {row['total']:.2f}€ ({percentage:.1f}%)
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {percentage}%; background-color: {row['color']};"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Aucune dépense enregistrée pour cette période")

def render_daily_evolution(daily_expenses):
    """
    Rendu du graphique d'évolution quotidienne
    
    Args:
        daily_expenses (DataFrame): Données des dépenses quotidiennes
    """
    if len(daily_expenses) > 0:
        fig = px.bar(
            daily_expenses,
            x='date',
            y='total',
            title='Évolution des dépenses sur les 7 derniers jours',
            labels={'date': 'Date', 'total': 'Montant (€)'},
            color_discrete_sequence=px.colors.sequential.Viridis
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Aucune donnée disponible pour les 7 derniers jours")
