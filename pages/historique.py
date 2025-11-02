# pages/historique.py
import os
import sqlite3
import pandas as pd
import streamlit as st
from database import ExpenseDatabase

st.set_page_config(page_title="Historique", page_icon="📜", layout="wide")

# Compat rerun
if not hasattr(st, "rerun"):
    st.rerun = st.experimental_rerun

db = ExpenseDatabase()

# ---------------- Helpers ----------------
def ensure_types(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or len(df) == 0:
        return pd.DataFrame(columns=["date", "category", "amount", "description"])
    colmap = {
        "categorie": "category",
        "cat": "category",
        "category_name": "category",
        "label": "description",
        "desc": "description",
        "libelle": "description",
    }
    df = df.rename(columns={k: v for k, v in colmap.items() if k in df.columns})
    for col in ["date", "category", "amount", "description"]:
        if col not in df.columns:
            df[col] = pd.NA
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    # On garde la date telle quelle pour un affichage simple
    try:
        df = df.sort_values("date", ascending=False)
    except Exception:
        pass
    return df[
        ["date", "category", "amount", "description"]
        + [c for c in df.columns if c not in {"date", "category", "amount", "description"}]
    ]

# ---------------- Sidebar : Filtres ----------------
st.sidebar.header("Filtres")

# Catégorie uniquement
cats = db.get_categories() or []  # [(id, name, color)]
cat_names = ["Toutes"] + [c[1] for c in cats]
sel_cat = st.sidebar.selectbox("Catégorie", cat_names)
category_filter = None if sel_cat == "Toutes" else sel_cat

# Bouton pour réinitialiser (ne fait que relancer)
if st.sidebar.button("🔄 Réinitialiser"):
    st.experimental_set_query_params()
    st.rerun()

# ---------------- Données ----------------
raw = db.get_expenses(start_date=None, end_date=None, category_name=category_filter)
df = ensure_types(raw.copy())

st.title("📜 Historique des Dépenses")

with st.expander("🎛️ Filtres actifs", expanded=False):
    st.write(f"**Catégorie :** {category_filter or 'Toutes'}")

if df.empty:
    st.info("Aucune dépense à afficher pour ce filtre.")
else:
    c1, c2 = st.columns(2)
    total = float(df["amount"].sum(skipna=True))
    count = int(df["amount"].count())
    c1.metric("💰 Total", f"{total:,.2f} €".replace(",", " "))
    c2.metric("🧾 Nombre de dépenses", f"{count}")

    view = df.copy()
    st.dataframe(
        view[["date", "category", "amount", "description"]],
        column_config={
            "date": st.column_config.Column("Date"),
            "category": st.column_config.Column("Catégorie"),
            "amount": st.column_config.NumberColumn("Montant (€)", format="%.2f"),
            "description": st.column_config.Column("Description"),
        },
        hide_index=True,
        width="stretch",   # plus de use_container_width
    )

    # Export CSV
    csv = view[["date", "category", "amount", "description"]].to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Exporter en CSV",
        data=csv,
        file_name="historique_depenses.csv",
        mime="text/csv",
    )

# ---------------- Diagnostic rapide ----------------
with st.expander("🔍 Diagnostic rapide", expanded=False):
    db_path = getattr(db, "db_path", "expenses.db")
    st.write("**Base utilisée :**", os.path.abspath(db_path))
    try:
        conn = sqlite3.connect(db_path)
        prev = pd.read_sql_query(
            "SELECT e.id, e.amount, e.description, e.date, c.name AS category "
            "FROM expenses e LEFT JOIN categories c ON e.category_id=c.id "
            "ORDER BY e.id DESC LIMIT 5", conn)
        conn.close()
    except Exception:
        prev = pd.DataFrame()
    st.dataframe(prev, hide_index=True, width="stretch")
