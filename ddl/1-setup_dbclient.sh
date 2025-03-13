#!/bin/bash

# Définir les variables de connexion PostgreSQL
DB_NAME="db_client"
DB_USER="postgres"
DB_HOST="localhost"
DB_PWD="temp123"
SQL_SCRIPT="1-creation_dbclient.sql"

# Vérifier le système d'exploitation
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "MacOS détecté."
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    echo "Windows détecté."
else
    echo "Système non reconnu. Exécution sous Linux probable."
fi

# Affichage du message de début
echo "Création de la base de données et insertion des données..."

# Définition du mot de passe PostgreSQL temporairement
export PGPASSWORD=$DB_PWD

# Lancer la commande en arrière-plan et capturer son PID
psql -h $DB_HOST -U $DB_USER -f $SQL_SCRIPT > /dev/null 2>&1 &
SQL_PID=$!

# Barre de progression simulée
while kill -0 $SQL_PID 2> /dev/null; do
    for i in '|' '/' '-' '\'; do
        echo -ne "\rCréation en cours... $i"
        sleep 0.2
    done
done

# Vérifier le succès de la commande
if wait $SQL_PID; then
    echo -e "\rLa base de données a été créée avec succès ! ✅"
else
    echo -e "\rErreur lors de la création de la base de données ❌"
fi

# Nettoyage du mot de passe
unset PGPASSWORD
