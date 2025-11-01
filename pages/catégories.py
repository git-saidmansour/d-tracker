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

# Initialisation de l'onglet actif
if 'category_tab' not in st.session_state:
    st.session_state.category_tab = "Liste des Catégories"

# Onglets pour les différentes actions
tab1, tab2, tab3 = st.tabs(["Liste des Catégories", "Ajouter une Catégorie", "Modifier une Catégorie"])

with tab1:
    st.subheader("Catégories Existantes")
    
    # Récupération de toutes les catégories
    categories = db.get_categories()
    
    if len(categories) > 0:
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
    
    # Sélection de la catégorie à modifier
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
