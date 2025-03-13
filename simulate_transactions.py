import time
import random
import psycopg2
from sqlalchemy import create_engine, text

# Connexion à PostgreSQL
DB_HOST = "localhost"
DB_PORT = "5432"
DB_USER = "postgres"
DB_PASSWORD = "temp123"
DB_NAME = "db_client"

# Liste des devises disponibles
CURRENCIES = ['EUR', 'USD', 'CNY', 'JPY', 'CHF', 'GBP', 'CAD', 'AUD', 'NZD']

# Connexion à la base de données avec SQLAlchemy
engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

def get_random_client_id():
    """Récupère un client_id existant aléatoire."""
    query = text("SELECT client_id FROM clients.customers ORDER BY RANDOM() LIMIT 1;")
    with engine.connect() as conn:
        result = conn.execute(query)
        client_id = result.scalar()  # Récupère un seul ID
    return client_id

def insert_random_transaction():
    """Insère une transaction aléatoire dans la base de données."""
    client_id = get_random_client_id()
    amount = round(random.uniform(-500, 500), 2)  # Montant entre -500 et +500
    currency = random.choice(CURRENCIES)  # Choisir une devise aléatoire

    query = text("""
    INSERT INTO transactions.transactions (client_id, amount, currency)
    VALUES (:client_id, :amount, :currency);
    """)

    try:
        with engine.connect() as conn:
            conn.execute(query, {"client_id": client_id, "amount": amount, "currency": currency})
            conn.commit()
        print(f"✅ Transaction ajoutée : Client {client_id}, Montant {amount} {currency}")
    except Exception as e:
        print(f"❌ Erreur lors de l'insertion de la transaction : {e}")

# Boucle infinie pour insérer une transaction toutes les 30 secondes
while True:
    insert_random_transaction()
    time.sleep(30)  # Attendre 30 secondes avant d'insérer une nouvelle transaction
