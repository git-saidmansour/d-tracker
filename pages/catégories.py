# pages/categories.py
import streamlit as st
from database import ExpenseDatabase

st.set_page_config(page_title="Catégories", page_icon="🗂️", layout="wide")

if not hasattr(st, "rerun"):
    st.rerun = st.experimental_rerun

db = ExpenseDatabase()

def load_categories():
    rows = db.get_categories() or []
    return [{"id": r[0], "name": (r[1] or "").strip(), "color": r[2]} for r in rows]

st.title("🗂️ Catégories")

# ---------- 🆕 Bouton de restauration ----------
with st.expander("⚙️ Outils de maintenance", expanded=False):
    if st.button("🔄 Restaurer les catégories par défaut (ajoute celles manquantes)"):
        ok, msg = db.ensure_default_categories()
        st.toast(msg, icon="✅" if ok else "❌")
        st.rerun()

# ---------- Création ----------
st.subheader("➕ Créer une catégorie")
with st.form("add_category_form", clear_on_submit=True):
    new_name = st.text_input("Nom", placeholder="ex. Alimentation")
    new_color = st.color_picker("Couleur", "#1f77b4")
    add_ok = st.form_submit_button("Ajouter", type="primary")

if add_ok:
    name = (new_name or "").strip()
    if not name:
        st.warning("Le nom ne peut pas être vide.")
    elif any(c["name"].lower() == name.lower() for c in load_categories()):
        st.warning("Cette catégorie existe déjà.")
    else:
        db.add_category(name, new_color)
        st.toast("Catégorie ajoutée ✅", icon="✅")
        st.rerun()

st.divider()

# ---------- Liste existante ----------
st.subheader("📋 Catégories existantes")

cats = load_categories()
if not cats:
    st.info("Aucune catégorie pour le moment.")
else:
    st.markdown("""
    <style>
      .row {display:flex; align-items:center; padding:8px 6px; border-bottom:1px solid rgba(0,0,0,0.06);}
      .cell-name {flex: 1 1 auto; font-weight:600}
      .dot {display:inline-block; width:12px; height:12px; border-radius:50%; margin-right:6px; vertical-align:middle;}
    </style>
    """, unsafe_allow_html=True)

    h1, h2, h3 = st.columns([7, 1, 1])
    h1.markdown("**Nom & Couleur**")
    h2.markdown("**Modifier**")
    h3.markdown("**Supprimer**")

    for c in cats:
        col1, col2, col3 = st.columns([7, 1, 1])

        with col1:
            st.markdown(
                f"<div class='row'>"
                f"<span class='dot' style='background:{c['color']}'></span>"
                f"<span class='cell-name'>{c['name']}</span>"
                f"<code>{c['color']}</code>"
                f"</div>", unsafe_allow_html=True
            )

        # --- Modifier ---
        with col2.popover("✏️"):
            st.write(f"Modifier **{c['name']}**")
            new_name = st.text_input("Nom", value=c["name"], key=f"edit_name_{c['id']}")
            new_color = st.color_picker("Couleur", value=c["color"], key=f"edit_color_{c['id']}")
            if st.button("💾 Enregistrer", key=f"save_{c['id']}", type="primary"):
                ok, msg = db.update_category(c["id"], new_name, new_color)
                st.toast(msg, icon="✅" if ok else "❌")
                st.rerun()

        # --- Supprimer ---
        with col3.popover("🗑️"):
            count = db.get_expense_count_by_category(c["id"])
            if count > 0:
                st.warning(f"Cette catégorie contient {count} dépense(s).")
                others = [x for x in cats if x["id"] != c["id"]]
                if others:
                    target = st.selectbox(
                        "Réassigner vers :",
                        [o["name"] for o in others],
                        key=f"target_{c['id']}"
                    )
                    target_id = next(o["id"] for o in others if o["name"] == target)
                    if st.button("🔁 Réassigner puis supprimer", key=f"reas_del_{c['id']}", type="primary"):
                        ok, msg = db.delete_category_reassign(c["id"], target_id)
                        st.toast(msg, icon="✅" if ok else "❌")
                        st.rerun()
                else:
                    st.info("Aucune autre catégorie disponible pour réassigner.")
                st.divider()

            if st.button("🗑️ Supprimer définitivement", key=f"del_{c['id']}", type="secondary"):
                ok, msg = db.delete_category(c["id"])
                st.toast(msg, icon="✅" if ok else "❌")
                st.rerun()
