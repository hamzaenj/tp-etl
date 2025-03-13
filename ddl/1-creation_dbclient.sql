

-- Création de la base de données
DROP DATABASE IF EXISTS db_client;
CREATE DATABASE db_client;

\c db_client

-- Création du schéma clients
CREATE SCHEMA IF NOT EXISTS clients AUTHORIZATION postgres;

CREATE TABLE clients.customers (
    client_id SERIAL PRIMARY KEY,
    client_name VARCHAR(100),
    email VARCHAR(100),
    country VARCHAR(50)
);

-- Création du schéma transactions
CREATE SCHEMA IF NOT EXISTS transactions AUTHORIZATION postgres;

CREATE TABLE transactions.transactions (
    transaction_id SERIAL PRIMARY KEY,
    client_id INT REFERENCES clients.customers(client_id),
    amount DECIMAL(10,2),
    currency VARCHAR(10),
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS transactions.exchange_rates (
        currency VARCHAR(10) PRIMARY KEY,
        rate DECIMAL(10,6),
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
CREATE TABLE IF NOT EXISTS transactions.final_transactions (
    transaction_id SERIAL PRIMARY KEY,
    client_id INT REFERENCES clients.customers(client_id),
    amount_eur DECIMAL(10,2),
    category VARCHAR(10),
    transaction_date TIMESTAMP
);
-- Insertion de données fictives dans customers
INSERT INTO clients.customers (client_name, email, country) VALUES
('Rami AL KHATEEB', 'rami.alkhateeb@example.com', 'Germany'),
('Sew BANAY', 'sew.banay@example.com', 'Japan'),
('Alexandre BOSSE', 'alexandre.bosse@example.com', 'Canada'),
('Lynda BOUKIRF', 'lynda.boukirf@example.com', 'Sweden'),
('Zahir DALLA', 'zahir.dalla@example.com', 'USA'),
('Bilal EL ABDELILLOUI', 'bilal.elabdelilloui@example.com', 'France'),
('Douwels GASPARO', 'douwels.gasparo@example.com', 'Italy'),
('Lamia HADJARAB', 'lamia.hadjarab@example.com', 'Australia'),
('Laura HORLOCH', 'laura.horloch@example.com', 'Netherlands'),
('Dali ISMAIL', 'dali.ismail@example.com', 'Switzerland'),
('Hakim KISMOUNE', 'hakim.kismoune@example.com', 'Denmark'),
('Oumama LAUBERNE', 'oumama.lauberne@example.com', 'Norway'),
('Fritz MALLET', 'fritz.mallet@example.com', 'Austria'),
('Anastasia MESQUIAK', 'anastasia.mesquiak@example.com', 'Russia'),
('Slimane MOUSTANE', 'slimane.moustane@example.com', 'Finland'),
('Mohamed PHAN', 'mohamed.phan@example.com', 'South Korea'),
('Alexis PHOMADY', 'alexis.phomady@example.com', 'New Zealand'),
('Papin TEMOGOBOGO', 'papin.temogobogo@example.com', 'Belgium');



-- Insertion de données fictives dans transactions
INSERT INTO transactions.transactions (client_id, amount, currency) VALUES
(1, 150.50, 'EUR'),    -- Crédit
(2, -200.75, 'USD'),   -- Débit
(3, 99.99, 'EUR'),     -- Crédit
(4, -500.00, 'CNY'),   -- Débit
(5, 45.20, 'JPY'),     -- Crédit
(6, -120.30, 'CHF'),   -- Débit
(7, 300.00, 'USD'),    -- Crédit
(8, -85.60, 'CNY'),    -- Débit
(9, 210.00, 'GBP'),    -- Crédit
(10, -55.75, 'EUR'),   -- Débit
(11, 400.00, 'CAD'),   -- Crédit
(12, -300.25, 'EUR'),  -- Débit
(13, 180.60, 'USD'),   -- Crédit
(14, -220.00, 'JPY'),  -- Débit
(15, 99.99, 'EUR'),    -- Crédit
(16, -75.30, 'AUD'),   -- Débit
(17, 500.00, 'CNY'),   -- Crédit
(18, -95.45, 'NZD');   -- Débit

