import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from database import ExpenseDatabase

# Configuration de la page
st.set_page_config(
    page_title="D-Tracker - Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialisation de la base de données
db = ExpenseDatabase()

# CSS personnalisé pour le dashboard
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    .metric-label {
        font-size: 1rem;
        opacity: 0.9;
    }
    .progress-container {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
    }
    .category-name {
        font-weight: bold;
        color: #333;
        margin-bottom: 0.5rem;
    }
    .progress-bar {
        background-color: #e9ecef;
        border-radius: 10px;
        height: 20px;
        overflow: hidden;
    }
    .progress-fill {
        height: 100%;
        border-radius: 10px;
        transition: width 0.3s ease;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    .delta-positive {
        color: #dc3545;
    }
    .delta-negative {
        color: #28a745;
    }
    .delta-neutral {
        color: #6c757d;
    }
    .nav-button {
        margin: 0.5rem 0;
        border-radius: 10px;
        font-weight: 500;
    }
    .nav-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Navigation latérale
with st.sidebar:
    st.markdown('<h1 class="main-header">💰 D-Tracker</h1>', unsafe_allow_html=True)
    
    # Menu de navigation avec boutons
    st.markdown("### Navigation")
    
    # Boutons de navigation
    if st.button("Dashboard", use_container_width=True, type="primary"):
        st.session_state.page = "Dashboard"
    
    if st.button("Nouvelle Dépense", use_container_width=True):
        st.session_state.page = "Nouvelle Dépense"
    
    if st.button("Analyses", use_container_width=True):
        st.session_state.page = "Analyses"
    
    if st.button("Historique", use_container_width=True):
        st.session_state.page = "Historique"
    
    if st.button("Gérer les Catégories", use_container_width=True):
        st.session_state.page = "Gérer les Catégories"
    
    # Initialiser la page par défaut
    if "page" not in st.session_state:
        st.session_state.page = "Dashboard"
    
    page = st.session_state.page
    
    st.markdown("---")
    
    # Dépenses récentes
    st.subheader("Dépenses Récentes")
    recent_expenses = db.get_expenses()
    if len(recent_expenses) > 0:
        for _, expense in recent_expenses.head(5).iterrows():
            st.write(f"• {expense['amount']:.2f}€ - {expense['category']}")
            st.caption(f"  {expense['date']}")
    else:
        st.info("Aucune dépense enregistrée")

# Contenu principal basé sur la navigation
if page == "Dashboard":
    st.header("Dashboard")
    
    # Métriques principales selon la période choisie
    col_title, col_select = st.columns([3, 1])
    
    with col_title:
        st.subheader("Résumé")
    
    with col_select:
        period_choice = st.selectbox(
            "",
            ["jour", "semaine", "mois", "année", "tout"],
            key="dashboard_period",
            label_visibility="collapsed"
        )
    
    # Calculer les dates selon la période choisie
    today = datetime.now()
    
    if period_choice == "jour":
        start_date = today.strftime("%Y-%m-%d")
        end_date = today.strftime("%Y-%m-%d")
        # Période précédente (hier)
        prev_start = (today - timedelta(days=1)).strftime("%Y-%m-%d")
        prev_end = (today - timedelta(days=1)).strftime("%Y-%m-%d")
        period_label = "Aujourd'hui"
        prev_label = "Hier"
        
    elif period_choice == "semaine":
        # Semaine actuelle (lundi à dimanche)
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        start_date = start_of_week.strftime("%Y-%m-%d")
        end_date = end_of_week.strftime("%Y-%m-%d")
        # Semaine précédente
        prev_start_of_week = start_of_week - timedelta(days=7)
        prev_end_of_week = prev_start_of_week + timedelta(days=6)
        prev_start = prev_start_of_week.strftime("%Y-%m-%d")
        prev_end = prev_end_of_week.strftime("%Y-%m-%d")
        period_label = "Cette Semaine"
        prev_label = "Semaine Précédente"
        
    elif period_choice == "mois":
        # Mois actuel
        start_date = today.strftime("%Y-%m-01")
        end_date = today.strftime("%Y-%m-%d")
        # Mois précédent
        prev_month = today.replace(day=1) - timedelta(days=1)
        prev_start = prev_month.strftime("%Y-%m-01")
        prev_end = prev_month.strftime("%Y-%m-%d")
        period_label = "Ce Mois"
        prev_label = "Mois Précédent"
        
    elif period_choice == "année":
        # Année actuelle
        start_date = today.strftime("%Y-01-01")
        end_date = today.strftime("%Y-%m-%d")
        # Année précédente
        prev_year = today.replace(year=today.year-1)
        prev_start = prev_year.strftime("%Y-01-01")
        prev_end = prev_year.strftime("%Y-12-31")
        period_label = "Cette Année"
        prev_label = "Année Précédente"
        
    else:  # tout
        # Toutes les données
        start_date = None
        end_date = None
        # Période précédente (même durée que la période actuelle)
        # Pour "tout", on compare avec la période précédente de même durée
        # On prend les 30 derniers jours vs les 30 jours précédents
        start_date = (today - timedelta(days=30)).strftime("%Y-%m-%d")
        end_date = today.strftime("%Y-%m-%d")
        prev_start = (today - timedelta(days=60)).strftime("%Y-%m-%d")
        prev_end = (today - timedelta(days=30)).strftime("%Y-%m-%d")
        period_label = "Toutes Périodes"
        prev_label = "Période Précédente"
    
    # Récupérer les données
    current_expenses = db.get_total_expenses(start_date, end_date)
    previous_expenses = db.get_total_expenses(prev_start, prev_end)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Comparaison avec la période précédente
        if previous_expenses > 0:
            variation_amount = current_expenses - previous_expenses
            variation_pct = (variation_amount / previous_expenses) * 100
            delta = f"{variation_pct:+.1f}%"
        else:
            delta = "Nouveau"
        
        st.metric(
            "Dépenses",
            f"{current_expenses:.2f} €",
            delta=delta
        )
    
    with col2:
        # Nombre de transactions pour la période actuelle
        current_count = len(db.get_expenses(start_date, end_date))
        previous_count = len(db.get_expenses(prev_start, prev_end))
        
        # Variation du nombre de transactions
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
    
    st.markdown("---")
    
    # Barres de progression par catégorie
    st.subheader("Répartition par Catégorie")
    
    # Récupérer les données des catégories pour la période sélectionnée
    category_stats = db.get_stats_by_category(start_date, end_date)
    
    if len(category_stats) > 0:
        # Calculer le total pour les pourcentages
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
        st.info(f"Aucune dépense enregistrée pour {period_label.lower()}")
    
    # Graphique de l'évolution des 7 derniers jours
    st.subheader("Évolution des 7 Derniers Jours")
    
    # Récupérer les données des 7 derniers jours
    end_date = datetime.now()
    start_date = end_date - timedelta(days=6)
    
    daily_data = []
    for i in range(7):
        date = (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
        amount = db.get_total_expenses(date, date)
        daily_data.append({
            'date': date,
            'amount': amount,
            'day_name': (start_date + timedelta(days=i)).strftime('%A')
        })
    
    df_daily = pd.DataFrame(daily_data)
    
    if df_daily['amount'].sum() > 0:
        fig = px.bar(
            df_daily, 
            x='day_name', 
            y='amount',
            title="Dépenses par Jour (7 derniers jours)",
            color='amount',
            color_continuous_scale='Blues'
        )
        fig.update_layout(
            xaxis_title="Jour",
            yaxis_title="Montant (€)",
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Aucune donnée disponible pour les 7 derniers jours")

elif page == "Nouvelle Dépense":
    st.header("Enregistrer une Nouvelle Dépense")
    
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
            # Récupérer les catégories
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
                    expense_id = db.add_expense(amount, description, category_id, date_str)
                    st.success(f"✅ Dépense de {amount:.2f} € enregistrée avec succès !")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Erreur lors de l'enregistrement : {str(e)}")
            else:
                st.error("❌ Le montant doit être supérieur à 0 €")

elif page == "Analyses":
    st.header("Analyses Détaillées")
    
    # Filtres pour les analyses
    col1, col2 = st.columns(2)
    
    with col1:
        analysis_start = st.date_input(
            "Date de début",
            value=datetime.now() - timedelta(days=30),
            key="analysis_start"
        )
    
    with col2:
        analysis_end = st.date_input(
            "Date de fin",
            value=datetime.now(),
            key="analysis_end"
        )
    
    analysis_start_str = analysis_start.strftime("%Y-%m-%d")
    analysis_end_str = analysis_end.strftime("%Y-%m-%d")
    
    # Analyses par catégorie
    st.subheader("Analyse par Catégorie")
    category_analysis = db.get_stats_by_category(analysis_start_str, analysis_end_str)
    
    if len(category_analysis) > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            # Graphique en barres
            fig_bar = px.bar(
                category_analysis,
                x='category',
                y='total',
                title="Dépenses par Catégorie",
                color='category',
                color_discrete_sequence=category_analysis['color'].tolist()
            )
            fig_bar.update_layout(xaxis_title="Catégorie", yaxis_title="Montant (€)")
            st.plotly_chart(fig_bar, use_container_width=True)
        
        with col2:
            # Graphique en camembert
            fig_pie = px.pie(
                category_analysis, 
                values='total', 
                names='category',
                title="Répartition par Catégorie",
                color_discrete_sequence=category_analysis['color'].tolist()
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)
        
        # Tableau détaillé
        st.subheader("Détail par Catégorie")
        display_df = category_analysis.copy()
        display_df['total'] = display_df['total'].round(2)
        display_df['count'] = display_df['count'].astype(int)
        display_df.columns = ['Catégorie', 'Couleur', 'Total (€)', 'Nombre de Transactions']
        display_df = display_df.drop('Couleur', axis=1)
        st.dataframe(display_df, use_container_width=True)
    else:
        st.info("Aucune donnée disponible pour cette période.")

elif page == "Historique":
    st.header("Historique des Dépenses")
    
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
        # Filtre par catégorie
        categories = db.get_categories()
        category_filter = st.selectbox(
            "Filtrer par catégorie",
            ["Toutes"] + [cat[1] for cat in categories]
        )
    
    # Récupérer les données
    history_start_str = history_start.strftime("%Y-%m-%d")
    history_end_str = history_end.strftime("%Y-%m-%d")
    
    expenses_history = db.get_expenses(history_start_str, history_end_str)
    
    if category_filter != "Toutes":
        expenses_history = expenses_history[expenses_history['category'] == category_filter]
    
    if len(expenses_history) > 0:
        # Afficher le tableau
        display_history = expenses_history.copy()
        display_history['amount'] = display_history['amount'].round(2)
        display_history = display_history[['date', 'amount', 'category', 'description']]
        display_history.columns = ['Date', 'Montant (€)', 'Catégorie', 'Description']
        
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

elif page == "Gérer les Catégories":
    st.header("Gérer les Catégories")
    
    # Onglets pour les différentes actions
    tab1, tab2, tab3 = st.tabs(["Liste des Catégories", "Ajouter une Catégorie", "Modifier une Catégorie"])
    
    with tab1:
        st.subheader("Catégories Existantes")
        
        # Récupérer toutes les catégories
        categories = db.get_categories()
        
        if len(categories) > 0:
            # Afficher les catégories dans un tableau
            st.markdown("**Liste des catégories :**")
            
            for cat in categories:
                col1, col2, col3 = st.columns([1, 2, 1])
                
                with col1:
                    st.markdown(f"""
                    <div style="
                        width: 20px; 
                        height: 20px; 
                        background-color: {cat[2]}; 
                        border-radius: 3px;
                        display: inline-block;
                    "></div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.write(f"**{cat[1]}**")
                
                with col3:
                    if st.button("🗑️", key=f"delete_{cat[0]}", help="Supprimer"):
                        success, message = db.delete_category(cat[0])
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
        else:
            st.info("Aucune catégorie trouvée.")
    
    with tab2:
        st.subheader("Ajouter une Nouvelle Catégorie")
        
        with st.form("add_category_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                new_name = st.text_input(
                    "Nom de la catégorie",
                    placeholder="Ex: Voyage, Sport, Électronique..."
                )
            
            with col2:
                new_color = st.color_picker(
                    "Couleur",
                    value="#1f77b4"
                )
            
            submitted = st.form_submit_button("Ajouter la Catégorie", type="primary")
            
            if submitted:
                if new_name.strip():
                    try:
                        category_id = db.add_category(new_name.strip(), new_color)
                        st.success(f"✅ Catégorie '{new_name}' ajoutée avec succès !")
                        st.rerun()
                    except Exception as e:
                        if "UNIQUE constraint failed" in str(e):
                            st.error("❌ Une catégorie avec ce nom existe déjà.")
                        else:
                            st.error(f"❌ Erreur lors de l'ajout : {str(e)}")
                else:
                    st.error("❌ Le nom de la catégorie ne peut pas être vide.")
    
    with tab3:
        st.subheader("Modifier une Catégorie")
        
        # Sélectionner la catégorie à modifier
        categories = db.get_categories()
        if len(categories) > 0:
            category_options = {f"{cat[1]}": cat[0] for cat in categories}
            selected_category_name = st.selectbox(
                "Sélectionner la catégorie à modifier",
                options=list(category_options.keys())
            )
            
            if selected_category_name:
                category_id = category_options[selected_category_name]
                category_info = db.get_category_by_id(category_id)
                
                if category_info:
                    with st.form("edit_category_form"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            edit_name = st.text_input(
                                "Nom de la catégorie",
                                value=category_info[1]
                            )
                        
                        with col2:
                            edit_color = st.color_picker(
                                "Couleur",
                                value=category_info[2]
                            )
                        
                        submitted = st.form_submit_button("Modifier la Catégorie", type="primary")
                        
                        if submitted:
                            if edit_name.strip():
                                try:
                                    db.update_category(category_id, edit_name.strip(), edit_color)
                                    st.success(f"✅ Catégorie modifiée avec succès !")
                                    st.rerun()
                                except Exception as e:
                                    if "UNIQUE constraint failed" in str(e):
                                        st.error("❌ Une catégorie avec ce nom existe déjà.")
                                    else:
                                        st.error(f"❌ Erreur lors de la modification : {str(e)}")
                            else:
                                st.error("❌ Le nom de la catégorie ne peut pas être vide.")
        else:
            st.info("Aucune catégorie à modifier.")

# Footer
st.markdown("---")
st.markdown(
    '<p style="text-align: center; color: #666;">Développé avec ❤️ en Python & Streamlit</p>',
    unsafe_allow_html=True
)