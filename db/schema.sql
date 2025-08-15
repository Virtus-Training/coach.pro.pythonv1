DROP TABLE IF EXISTS resultats_exercices;
DROP TABLE IF EXISTS seances;
DROP TABLE IF EXISTS clients;
DROP TABLE IF EXISTS exercices;
DROP TABLE IF EXISTS portions;
DROP TABLE IF EXISTS aliments;

CREATE TABLE exercices (
    id INTEGER PRIMARY KEY,
    nom TEXT NOT NULL UNIQUE,
    groupe_musculaire_principal TEXT NOT NULL,
    equipement TEXT,
    tags TEXT,
    movement_pattern TEXT,
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

CREATE TABLE aliments (
    id INTEGER PRIMARY KEY,
    nom TEXT NOT NULL UNIQUE,
    categorie TEXT,
    type_alimentation TEXT,
    kcal_100g REAL NOT NULL,
    proteines_100g REAL NOT NULL,
    glucides_100g REAL NOT NULL,
    lipides_100g REAL NOT NULL,
    fibres_100g REAL,
    unite_base TEXT DEFAULT 'g',
    indice_healthy INTEGER,
    indice_commun INTEGER
);

CREATE TABLE portions (
    id INTEGER PRIMARY KEY,
    aliment_id INTEGER NOT NULL,
    description TEXT NOT NULL,
    grammes_equivalents REAL NOT NULL,
    FOREIGN KEY(aliment_id) REFERENCES aliments(id)
);

CREATE TABLE plans_alimentaires (
    id INTEGER PRIMARY KEY,
    nom TEXT NOT NULL,
    description TEXT,
    tags TEXT
);

CREATE TABLE repas (
    id INTEGER PRIMARY KEY,
    plan_id INTEGER NOT NULL,
    nom TEXT NOT NULL,
    ordre INTEGER DEFAULT 0,
    FOREIGN KEY(plan_id) REFERENCES plans_alimentaires(id)
);

CREATE TABLE repas_items (
    id INTEGER PRIMARY KEY,
    repas_id INTEGER NOT NULL,
    aliment_id INTEGER NOT NULL,
    portion_id INTEGER NOT NULL,
    quantite REAL DEFAULT 1.0,
    FOREIGN KEY(repas_id) REFERENCES repas(id),
    FOREIGN KEY(aliment_id) REFERENCES aliments(id),
    FOREIGN KEY(portion_id) REFERENCES portions(id)
);

