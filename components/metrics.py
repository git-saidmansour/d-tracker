"""
Composants de métriques pour l'application D-Tracker
"""

import streamlit as st
from utils.formatters import format_currency, format_percentage, format_delta, get_delta_class

def render_metric_card(title, value, delta=None, delta_label=None):
    """
    Rendu d'une carte de métrique avec delta optionnel
    
    Args:
        title (str): Titre de la métrique
        value (float): Valeur de la métrique
        delta (float, optional): Valeur du delta
        delta_label (str, optional): Label du delta
    """
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.metric(
            title,
            format_currency(value),
            delta=format_delta(delta) if delta is not None else None,
            delta_color="normal"
        )
    
    if delta_label:
        with col2:
            st.markdown(f"<div class='{get_delta_class(delta)}'>{delta_label}</div>", unsafe_allow_html=True)

def render_summary_metrics(current_expenses, previous_expenses, current_count, previous_count):
    """
    Rendu des métriques de résumé pour le dashboard
    
    Args:
        current_expenses (float): Dépenses de la période actuelle
        previous_expenses (float): Dépenses de la période précédente
        current_count (int): Nombre de transactions de la période actuelle
        previous_count (int): Nombre de transactions de la période précédente
    """
    col1, col2 = st.columns(2)
    
    with col1:
        # Calcul de la variation des dépenses
        if previous_expenses > 0:
            variation_amount = current_expenses - previous_expenses
            variation_pct = (variation_amount / previous_expenses) * 100
            delta = f"{variation_pct:+.1f}%"
        else:
            delta = "Nouveau"
        
        st.metric(
            "Dépenses",
            format_currency(current_expenses),
            delta=delta
        )
    
    with col2:
        # Calcul de la variation du nombre de transactions
        if previous_count > 0:
            count_variation = current_count - previous_count
            count_delta = f"{count_variation:+d}"
        else:
            count_delta = "Nouveau"
        
        st.metric(
            "Transactions",
            f"{current_count}",
            delta=count_delta
        )

