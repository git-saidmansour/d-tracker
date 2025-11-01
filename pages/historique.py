"""
Page d'historique pour l'application D-Tracker
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from database import ExpenseDatabase
from config.settings import CSS_STYLES

# Application du CSS personnalisé
st.markdown(CSS_STYLES, unsafe_allow_html=True)

st.header("Historique des Dépenses")

# Initialisation de la base de données
db = ExpenseDatabase()

# Filtres
col1, col2, col3 = st.columns(3)

with col1:
    history_start = st.date_input(
        "Depuis",
        value=datetime.now() - timedelta(days=30),
        key="history_start"
    )

with col2:
    history_end = st.date_input(
        "Jusqu'à",
        value=datetime.now(),
        key="history_end"
    )

with col3:
    categories = db.get_categories()
    category_filter = st.selectbox(
        "Filtrer par catégorie",
        ["Toutes"] + [cat[1] for cat in categories]
    )

history_start_str = history_start.strftime("%Y-%m-%d")
history_end_str = history_end.strftime("%Y-%m-%d")

# Obtention des dépenses
expenses_history = db.get_expenses(
    history_start_str, 
    history_end_str, 
    category_filter if category_filter != "Toutes" else None
)

if len(expenses_history) > 0:
    # Formatage des données pour l'affichage
    display_history = expenses_history.copy()
    display_history['amount'] = display_history['amount'].round(2)
    display_history['date'] = pd.to_datetime(display_history['date']).dt.strftime('%d/%m/%Y')
    display_history = display_history[['date', 'category', 'amount', 'description']]
    display_history.columns = ['Date', 'Catégorie', 'Montant (€)', 'Description']
    
    # Affichage du tableau
    st.dataframe(
        display_history,
        use_container_width=True,
        hide_index=True
    )
    
    # Bouton d'export
    if st.button("Exporter en CSV"):
        csv = expenses_history.to_csv(index=False)
        st.download_button(
            label="Télécharger le fichier CSV",
            data=csv,
            file_name=f"depenses_{history_start_str}_{history_end_str}.csv",
            mime="text/csv"
        )
else:
    st.info("Aucune dépense trouvée pour les critères sélectionnés.")
