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
    antecedents_medicaux TEXT,
    sexe TEXT,
    poids_kg REAL,
    taille_cm REAL,
    niveau_activite TEXT
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
    session_id TEXT NOT NULL,
    exercice_id INTEGER NOT NULL,
    series_effectuees INTEGER,
    reps_effectuees INTEGER,
    charge_utilisee REAL,
    rpe INTEGER,
    feedback_client TEXT,
    FOREIGN KEY(session_id) REFERENCES sessions(session_id),
    FOREIGN KEY(exercice_id) REFERENCES exercices(id),
    UNIQUE(session_id, exercice_id)
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
    client_id INTEGER,
    nom TEXT NOT NULL,
    description TEXT,
    tags TEXT,
    FOREIGN KEY(client_id) REFERENCES clients(id)
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

CREATE TABLE fiches_nutrition (
    id INTEGER PRIMARY KEY,
    client_id INTEGER NOT NULL,
    date_creation DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    poids_kg_mesure REAL NOT NULL,
    objectif TEXT NOT NULL,
    proteines_cible_g_par_kg REAL NOT NULL,
    ratio_glucides_lipides_cible REAL NOT NULL,
    maintenance_kcal INTEGER NOT NULL,
    objectif_kcal INTEGER NOT NULL,
    proteines_g INTEGER NOT NULL,
    glucides_g INTEGER NOT NULL,
    lipides_g INTEGER NOT NULL,
    FOREIGN KEY(client_id) REFERENCES clients(id)
);

CREATE TABLE sessions (
    session_id TEXT PRIMARY KEY,
    client_id INTEGER,
    mode TEXT NOT NULL,
    label TEXT NOT NULL,
    duration_sec INTEGER NOT NULL,
    date_creation TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_template INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY(client_id) REFERENCES clients(id)
);

CREATE TABLE session_blocks (
    block_id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL,
    type TEXT NOT NULL,
    duration_sec INTEGER,
    rounds INTEGER,
    work_sec INTEGER,
    rest_sec INTEGER,
    title TEXT,
    locked INTEGER DEFAULT 0,
    FOREIGN KEY(session_id) REFERENCES sessions(session_id)
);

CREATE TABLE session_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    block_id TEXT NOT NULL,
    exercise_id TEXT NOT NULL,
    prescription TEXT NOT NULL,
    notes TEXT,
    FOREIGN KEY(block_id) REFERENCES session_blocks(block_id)
);

