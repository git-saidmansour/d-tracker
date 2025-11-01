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

def render_category_analysis(category_analysis):
    """
    Rendu des graphiques d'analyse par catégorie
    
    Args:
        category_analysis (DataFrame): Données d'analyse par catégorie
    """
    if len(category_analysis) > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            fig_bar = px.bar(
                category_analysis,
                x='category',
                y='total',
                title='Dépenses par Catégorie',
                labels={'category': 'Catégorie', 'total': 'Montant (€)'},
                color='category',
                color_discrete_sequence=category_analysis['color'].tolist()
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        
        with col2:
            fig_pie = px.pie(
                category_analysis,
                values='total',
                names='category',
                title='Répartition des Dépenses',
                color='category',
                color_discrete_sequence=category_analysis['color'].tolist()
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)
        
        # Tableau de détail par catégorie
        st.subheader("Détail par Catégorie")
        display_df = category_analysis.copy()
        display_df['total'] = display_df['total'].round(2)
        display_df['count'] = display_df['count'].astype(int)
        display_df.columns = ['Catégorie', 'Couleur', 'Total (€)', 'Nombre de Transactions']
        display_df = display_df.drop('Couleur', axis=1)
        st.dataframe(display_df, use_container_width=True)
    else:
        st.info("Aucune donnée disponible pour cette période.")

def render_category_evolution(daily_by_category, selected_categories=None):
    """
    Rendu du graphique d'évolution en courbes par catégorie
    
    Args:
        daily_by_category (DataFrame): Données des dépenses quotidiennes par catégorie
        selected_categories (list): Liste des catégories sélectionnées à afficher
    """
    if len(daily_by_category) > 0:
        # Filtrer par catégories sélectionnées si nécessaire
        df_filtered = daily_by_category.copy()
        if selected_categories:
            df_filtered = df_filtered[df_filtered['category'].isin(selected_categories)]
        
        if len(df_filtered) > 0:
            # Convertir la date en datetime pour un meilleur affichage
            df_filtered['date'] = pd.to_datetime(df_filtered['date'])
            
            # Créer un dictionnaire des couleurs par catégorie
            category_colors = {}
            if 'color' in df_filtered.columns:
                category_colors = df_filtered.groupby('category')['color'].first().to_dict()
            
            # Créer le graphique en courbes avec le format long
            fig = px.line(
                df_filtered,
                x='date',
                y='total',
                color='category',
                title='Évolution des Dépenses par Catégorie',
                labels={'date': 'Date', 'total': 'Montant (€)', 'category': 'Catégorie'},
                color_discrete_map=category_colors if category_colors else None
            )
            
            fig.update_layout(
                hovermode='x unified',
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Aucune donnée disponible pour les catégories sélectionnées")
    else:
        st.info("Aucune donnée disponible pour cette période")