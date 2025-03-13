import requests
import pandas as pd
from sqlalchemy import create_engine, text
import urllib3

# Désactiver les avertissements SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Connexion à PostgreSQL
engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")


# Appel à l'API REST avec SSL désactivé
response = requests.get(API_URL)
response.raise_for_status()
data = response.json()

# Extraction des taux de change
rates = data["conversion_rates"]
df_rates = pd.DataFrame(rates.items(), columns=["currency", "rate"])

# Création d'une table pour stocker les taux de change (avec correction)
create_table_query = text("""
    CREATE TABLE IF NOT EXISTS transactions.exchange_rates (
        currency VARCHAR(10) PRIMARY KEY,
        rate DECIMAL(10,6),
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
""")

with engine.connect() as conn:
    conn.execute(create_table_query)
    conn.commit()

# Insérer les taux dans PostgreSQL
df_rates.to_sql("exchange_rates", engine, schema="transactions", if_exists="replace", index=False)




