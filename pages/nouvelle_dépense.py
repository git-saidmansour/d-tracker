"""
Page de nouvelle dépense pour l'application D-Tracker
"""

import streamlit as st
from datetime import datetime
from database import ExpenseDatabase
from config.settings import CSS_STYLES

# Application du CSS personnalisé
st.markdown(CSS_STYLES, unsafe_allow_html=True)

st.header("Enregistrer une Nouvelle Dépense")

# Initialisation de la base de données
db = ExpenseDatabase()

with st.form("expense_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        amount = st.number_input(
            "Montant (€)",
            min_value=0.01,
            step=0.01,
            format="%.2f"
        )
        
        date = st.date_input(
            "Date",
            value=datetime.now()
        )
    
    with col2:
        categories = db.get_categories()
        category_options = {f"{cat[1]}": cat[0] for cat in categories}
        
        category_name = st.selectbox(
            "Catégorie",
            options=list(category_options.keys())
        )
        
        description = st.text_area(
            "Description (optionnel)",
            placeholder="Ex: Déjeuner au restaurant, Essence, Courses..."
        )
    
    submitted = st.form_submit_button("Enregistrer la Dépense", type="primary")
    
    if submitted:
        if amount > 0:
            category_id = category_options[category_name]
            date_str = date.strftime("%Y-%m-%d")
            try:
                db.add_expense(amount, description, category_id, date_str)
                st.success(f"✅ Dépense de {amount:.2f} € enregistrée dans '{category_name}' !")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Erreur lors de l'enregistrement : {str(e)}")
        else:
            st.error("❌ Le montant doit être supérieur à 0 €")
