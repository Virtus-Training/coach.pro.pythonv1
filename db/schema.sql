DROP TABLE IF EXISTS resultats_exercices;
DROP TABLE IF EXISTS seances;
DROP TABLE IF EXISTS clients;
DROP TABLE IF EXISTS exercices;

CREATE TABLE exercices (
    id INTEGER PRIMARY KEY,
    nom TEXT NOT NULL UNIQUE,
    groupe_musculaire_principal TEXT NOT NULL,
    equipement TEXT,
    tags TEXT,
    type_effort TEXT NOT NULL,
    coefficient_volume REAL DEFAULT 1.0,
    est_chargeable BOOLEAN NOT NULL
);

CREATE TABLE clients (
    id INTEGER PRIMARY KEY,
    nom TEXT NOT NULL,
    prenom TEXT NOT NULL,
    email TEXT UNIQUE,
    date_naissance DATE,
    objectifs TEXT,
    antecedents_medicaux TEXT
);

CREATE TABLE client_exercice_exclusions (
    client_id INTEGER NOT NULL,
    exercice_id INTEGER NOT NULL,
    PRIMARY KEY (client_id, exercice_id),
    FOREIGN KEY(client_id) REFERENCES clients(id),
    FOREIGN KEY(exercice_id) REFERENCES exercices(id)
);

CREATE TABLE seances (
    id INTEGER PRIMARY KEY,
    client_id INTEGER,
    type_seance TEXT NOT NULL,
    titre TEXT NOT NULL,
    date_creation DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(client_id) REFERENCES clients(id)
);

CREATE TABLE resultats_exercices (
    id INTEGER PRIMARY KEY,
    seance_id INTEGER NOT NULL,
    exercice_id INTEGER NOT NULL,
    series_effectuees INTEGER,
    reps_effectuees INTEGER,
    charge_utilisee REAL,
    feedback_client TEXT,
    FOREIGN KEY(seance_id) REFERENCES seances(id),
    FOREIGN KEY(exercice_id) REFERENCES exercices(id)
);

