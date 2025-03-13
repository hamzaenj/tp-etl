import pandas as pd
from sqlalchemy import create_engine
from config import *

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

try:
    # Récupérer uniquement les transactions récentes
    query = """ """

    df = pd.read_sql(query, engine)

    if not df.empty:  # Vérifier s'il y a de nouvelles transactions
        df.to_sql("final_transactions", engine, schema="transactions", if_exists="append", index=False)
        print(f"✅ {len(df)} nouvelles transactions ajoutées dans transactions.final_transactions !")
    else:
        print("⚠️ Aucune nouvelle transaction à charger.")

except Exception as e:
    print(f"❌ Erreur lors du chargement des données : {e}")
