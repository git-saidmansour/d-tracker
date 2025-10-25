"""
Composant de navigation de la barre latérale pour l'application D-Tracker
"""

import streamlit as st

def render_sidebar():
    """
    Rendu de la navigation de la barre latérale
    
    Returns:
        str: Page sélectionnée
    """
    st.sidebar.title("💰 D-Tracker")
    st.sidebar.markdown("---")
    
    # Boutons de navigation
    if st.sidebar.button("Dashboard", key="nav_dashboard", use_container_width=True):
        st.session_state.page = "Dashboard"
    
    if st.sidebar.button("Nouvelle Dépense", key="nav_new_expense", use_container_width=True):
        st.session_state.page = "Nouvelle Dépense"
    
    if st.sidebar.button("Analyses", key="nav_analyses", use_container_width=True):
        st.session_state.page = "Analyses"
    
    if st.sidebar.button("Historique", key="nav_history", use_container_width=True):
        st.session_state.page = "Historique"
    
    if st.sidebar.button("Gérer les Catégories", key="nav_categories", use_container_width=True):
        st.session_state.page = "Gérer les Catégories"
    
    st.sidebar.markdown("---")
    
    # Retour de la page actuelle
    return st.session_state.get("page", "Dashboard")

