# coach.pro.python
Logiciel de coaching en python pour coach sportif indépendant en local.


Arborescence:
coach.pro/
│
├── main.py                      # Point d’entrée, lanceur de l’app
├── app.py                       # Gère l'affichage de la fenêtre principale + navigation
│
├── assets/                      # Images, icônes, illustrations
│   ├── icons/
│   ├── images/
│   └── logo.png
│
├── ui/                          # TOUS les composants visuels uniquement (UI)
│   ├── layout/                  # Éléments de layout général
│   │   ├── sidebar.py           # Menu latéral avec boutons/icônes
│   │   ├── header.py            # Titre, logo, user icon
│   │   └── container.py         # Zone d’affichage principale
│   │
│   ├── pages/                   # Pages graphiques (navigation OK, contenu placeholder)
│   │   ├── dashboard_page.py
│   │   ├── program_page.py
│   │   ├── session_page.py
│   │   ├── calendar_page.py
│   │   ├── nutrition_page.py
│   │   ├── exercises_page.py
│   │   ├── progress_page.py
│   │   ├── pdf_page.py
│   │   ├── clients_page.py
│   │   ├── messaging_page.py
│   │   └── billing_page.py
│   │
│   ├── components/              # Composants visuels réutilisables (pas de logique)
│   │   ├── card.py              # Bloc avec icône + texte
│   │   ├── title.py             # Label stylisé de section
│   │   └── button.py            # Boutons personnalisés
│   │
│   └── theme/                   # Styles visuels (dark mode, couleurs, fonts)
│       ├── colors.py
│       ├── fonts.py
│       └── theme.py
│
├── navigation/                 # Fichier central de gestion des routes internes
│   └── router.py
│
├── utils/                      # Fonctions utilitaires simples pour la maquette
│   └── icon_loader.py
│
└── README.md
