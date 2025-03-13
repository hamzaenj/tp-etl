import pandas as pd
from sqlalchemy import create_engine
from config import *

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

try:
    # 1️⃣ EXTRACTION : Récupérer les transactions brutes et les taux de change
    transactions_query = "SELECT * FROM transactions.transactions"
    exchange_rates_query = "SELECT * FROM transactions.exchange_rates"

    df_transactions = pd.read_sql(transactions_query, engine)
    df_exchange_rates = pd.read_sql(exchange_rates_query, engine)

    # 2️⃣ TRANSFORMATION : Conversion de devise et ajout de catégorie
    # Fusionner transactions et taux de change
    df = df_transactions.merge(df_exchange_rates, left_on="currency", right_on="currency", how="left")

    #************************************** reponse *************************
    # Ajouter la colonne catégorie

    # Convertir le montant en EUR
    # ***********************************************************************

    # Sélectionner uniquement les colonnes nécessaires
    df = df[["transaction_id", "client_id", "amount_eur", "category", "transaction_date"]]

    # 3️⃣ CHARGEMENT : Sauvegarde dans PostgreSQL en mode append
    df.to_sql("transformed_transactions", engine, schema="transactions", if_exists="replace", index=False)

    print(f"✅ {len(df)} transactions transformées et chargées avec succès !")

except Exception as e:
    print(f"❌ Erreur lors de la transformation des données : {e}")
