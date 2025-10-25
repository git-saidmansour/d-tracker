"""
D-Tracker - Application de suivi des dépenses
Page d'accueil
"""

import streamlit as st
from config.settings import CSS_STYLES

# Configuration de la page
st.set_page_config(
    page_title="D-Tracker - Suivi des Dépenses",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Application du CSS personnalisé
st.markdown(CSS_STYLES, unsafe_allow_html=True)

# Page d'accueil
st.title("D-Tracker")
st.markdown("### Application de suivi des dépenses")

st.markdown("""
Bienvenue dans D-Tracker, votre application de suivi des dépenses personnelles !

**Fonctionnalités disponibles :**
- **Dashboard** : Vue d'ensemble de vos dépenses
- **Nouvelle Dépense** : Enregistrer une nouvelle dépense
- **Analyses** : Analyses détaillées par catégorie
- **Historique** : Consulter l'historique des dépenses
- **Catégories** : Créer et modifier les catégories

Utilisez la barre latérale pour naviguer entre les différentes sections.
""")

# Pied de page
st.markdown("---")
st.markdown(
    '<p style="text-align: center; color: #666;">Développé par Saîd & Maqs</p>',
    unsafe_allow_html=True
)
