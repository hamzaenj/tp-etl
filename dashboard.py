import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# Configuration de la base de données PostgreSQL
DB_HOST = "localhost"
DB_PORT = "5432"
DB_USER = "postgres"
DB_PASSWORD = "temp123"
DB_NAME = "db_client"

# Connexion à PostgreSQL
engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")


# Fonction pour récupérer les données avec les noms des clients
def get_data():
    query = """
    SELECT t.transaction_id, c.client_name, t.amount_eur, t.category, t.transaction_date
    FROM transactions.final_transactions t
    JOIN clients.customers c ON t.client_id = c.client_id
    ORDER BY t.transaction_date DESC
    LIMIT 50;
    """
    return pd.read_sql(query, engine)


# Fonction pour afficher les statistiques financières
def display_statistics(df):
    st.subheader("📊 Statistiques Financières")

    total_credit = df[df["amount_eur"] > 0]["amount_eur"].sum()
    total_debit = df[df["amount_eur"] < 0]["amount_eur"].sum()
    balance = total_credit + total_debit

    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Total Crédit", f"{total_credit:,.2f} EUR")
    col2.metric("📉 Total Débit", f"{total_debit:,.2f} EUR")
    col3.metric("🏦 Solde Net", f"{balance:,.2f} EUR")


# Fonction pour afficher un graphique avec échelle ajustée
def display_chart(df):
    st.subheader("📈 Évolution des Transactions")

    # Convertir la date en format datetime
    df["transaction_date"] = pd.to_datetime(df["transaction_date"])

    # Regrouper les transactions par heure pour lisibilité
    df_grouped = df.resample('H', on='transaction_date')["amount_eur"].sum().reset_index()

    st.line_chart(df_grouped, x="transaction_date", y="amount_eur")


# Fonction pour afficher le tableau des transactions avec noms des clients
def display_transactions(df):
    st.subheader("📜 Liste des Dernières Transactions")
    st.dataframe(df)


# 🎨 Personnalisation du thème Streamlit
st.set_page_config(
    page_title="Tableau de Bord Financier",
    page_icon="💰",
    layout="wide"
)

# 🏦 En-tête du Dashboard
st.title("💰 Tableau de Bord des Transactions Bancaires")

# ⏳ Rafraîchissement manuel et automatique
if st.button("🔄 Actualiser les données"):
    st.experimental_rerun()

st_autorefresh = st.empty()
st_autorefresh.markdown("<small>Rafraîchissement auto toutes les 60s</small>", unsafe_allow_html=True)

# 📡 Charger les données
df = get_data()

# Afficher les statistiques, graphiques et tableau des transactions
display_statistics(df)
display_chart(df)
display_transactions(df)
