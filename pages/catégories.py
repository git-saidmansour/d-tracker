"""
Page de gestion des catégories pour l'application D-Tracker
"""

import streamlit as st
from database import ExpenseDatabase
from config.settings import CSS_STYLES

# Application du CSS personnalisé
st.markdown(CSS_STYLES, unsafe_allow_html=True)

st.header("Gérer les Catégories")

# Initialisation de la base de données
db = ExpenseDatabase()