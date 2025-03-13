import pandas as pd
from sqlalchemy import create_engine

# Connexion PostgreSQL
DB_HOST = "localhost"
DB_PORT = "5432"
DB_USER = "postgres"
DB_PASSWORD = "temp123"
DB_NAME = "db_client"

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

try:
    # Récupérer uniquement les transactions récentes
    query = """
    SELECT transaction_id, client_id, amount_eur, category, transaction_date 
    FROM transactions.transformed_transactions
    WHERE transaction_id NOT IN (SELECT transaction_id FROM transactions.final_transactions);
    """

    df = pd.read_sql(query, engine)

    if not df.empty:  # Vérifier s'il y a de nouvelles transactions
        df.to_sql("final_transactions", engine, schema="transactions", if_exists="append", index=False)
        print(f"✅ {len(df)} nouvelles transactions ajoutées dans transactions.final_transactions !")
    else:
        print("⚠️ Aucune nouvelle transaction à charger.")

except Exception as e:
    print(f"❌ Erreur lors du chargement des données : {e}")
