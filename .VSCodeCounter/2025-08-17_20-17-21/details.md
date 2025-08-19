# Details

Date : 2025-08-17 20:17:21

Directory c:\\Users\\Eric\\Desktop\\coach.pro.python

Total : 84 files,  3982 codes, 100 comments, 797 blanks, all 4879 lines

[Summary](results.md) / Details / [Diff Summary](diff.md) / [Diff Details](diff-details.md)

## Files
| filename | language | code | comment | blank | total |
| :--- | :--- | ---: | ---: | ---: | ---: |
| [.github/workflows/ci.yml](/.github/workflows/ci.yml) | YAML | 27 | 0 | 3 | 30 |
| [README.md](/README.md) | Markdown | 2 | 0 | 1 | 3 |
| [README_patch.md](/README_patch.md) | Markdown | 9 | 0 | 2 | 11 |
| [app.py](/app.py) | Python | 85 | 4 | 18 | 107 |
| [controllers/__init__.py](/controllers/__init__.py) | Python | 0 | 0 | 1 | 1 |
| [controllers/session_controller.py](/controllers/session_controller.py) | Python | 71 | 0 | 10 | 81 |
| [db/database_manager.py](/db/database_manager.py) | Python | 10 | 0 | 7 | 17 |
| [db/database_setup.py](/db/database_setup.py) | Python | 12 | 0 | 6 | 18 |
| [db/schema.sql](/db/schema.sql) | MS SQL | 115 | 0 | 13 | 128 |
| [db/seed.py](/db/seed.py) | Python | 141 | 0 | 23 | 164 |
| [main.py](/main.py) | Python | 5 | 0 | 2 | 7 |
| [models/__init__.py](/models/__init__.py) | Python | 10 | 0 | 2 | 12 |
| [models/aliment.py](/models/aliment.py) | Python | 16 | 0 | 3 | 19 |
| [models/client.py](/models/client.py) | Python | 15 | 0 | 3 | 18 |
| [models/exercices.py](/models/exercices.py) | Python | 13 | 0 | 3 | 16 |
| [models/fiche_nutrition.py](/models/fiche_nutrition.py) | Python | 16 | 0 | 3 | 19 |
| [models/plan_alimentaire.py](/models/plan_alimentaire.py) | Python | 23 | 0 | 7 | 30 |
| [models/portion.py](/models/portion.py) | Python | 7 | 0 | 3 | 10 |
| [models/resultat_exercice.py](/models/resultat_exercice.py) | Python | 11 | 0 | 3 | 14 |
| [models/seance.py](/models/seance.py) | Python | 12 | 0 | 5 | 17 |
| [models/session.py](/models/session.py) | Python | 27 | 0 | 8 | 35 |
| [navigation/router.py](/navigation/router.py) | Python | 0 | 0 | 2 | 2 |
| [repositories/__init__.py](/repositories/__init__.py) | Python | 0 | 0 | 1 | 1 |
| [repositories/aliment_repo.py](/repositories/aliment_repo.py) | Python | 53 | 0 | 7 | 60 |
| [repositories/client_repo.py](/repositories/client_repo.py) | Python | 101 | 1 | 14 | 116 |
| [repositories/exercices_repo.py](/repositories/exercices_repo.py) | Python | 104 | 0 | 16 | 120 |
| [repositories/fiche_nutrition_repo.py](/repositories/fiche_nutrition_repo.py) | Python | 53 | 0 | 6 | 59 |
| [repositories/plan_alimentaire_repo.py](/repositories/plan_alimentaire_repo.py) | Python | 196 | 4 | 16 | 216 |
| [repositories/seance_repo.py](/repositories/seance_repo.py) | Python | 99 | 0 | 7 | 106 |
| [repositories/sessions_repo.py](/repositories/sessions_repo.py) | Python | 39 | 0 | 4 | 43 |
| [requirements.txt](/requirements.txt) | pip requirements | 37 | 0 | 0 | 37 |
| [services/__init__.py](/services/__init__.py) | Python | 0 | 0 | 1 | 1 |
| [services/nutrition_service.py](/services/nutrition_service.py) | Python | 61 | 1 | 13 | 75 |
| [services/pdf_generator.py](/services/pdf_generator.py) | Python | 51 | 1 | 9 | 61 |
| [services/session_generator.py](/services/session_generator.py) | Python | 157 | 12 | 38 | 207 |
| [services/session_templates.py](/services/session_templates.py) | Python | 48 | 1 | 11 | 60 |
| [tree-maker/filetree.md](/tree-maker/filetree.md) | Markdown | 117 | 0 | 0 | 117 |
| [ui/components/button.py](/ui/components/button.py) | Python | 15 | 1 | 5 | 21 |
| [ui/components/card.py](/ui/components/card.py) | Python | 22 | 1 | 6 | 29 |
| [ui/components/design_system/__init__.py](/ui/components/design_system/__init__.py) | Python | 4 | 0 | 2 | 6 |
| [ui/components/design_system/buttons.py](/ui/components/design_system/buttons.py) | Python | 31 | 1 | 9 | 41 |
| [ui/components/design_system/cards.py](/ui/components/design_system/cards.py) | Python | 13 | 1 | 6 | 20 |
| [ui/components/design_system/typography.py](/ui/components/design_system/typography.py) | Python | 11 | 1 | 9 | 21 |
| [ui/components/exclusion_selector.py](/ui/components/exclusion_selector.py) | Python | 63 | 0 | 16 | 79 |
| [ui/components/layout.py](/ui/components/layout.py) | Python | 15 | 0 | 8 | 23 |
| [ui/components/tabbar.py](/ui/components/tabbar.py) | Python | 50 | 1 | 12 | 63 |
| [ui/components/title.py](/ui/components/title.py) | Python | 6 | 1 | 5 | 12 |
| [ui/components/workout_block.py](/ui/components/workout_block.py) | Python | 63 | 1 | 17 | 81 |
| [ui/layout/container.py](/ui/layout/container.py) | Python | 0 | 0 | 2 | 2 |
| [ui/layout/header.py](/ui/layout/header.py) | Python | 23 | 4 | 9 | 36 |
| [ui/layout/sidebar.py](/ui/layout/sidebar.py) | Python | 57 | 1 | 12 | 70 |
| [ui/modals/__init__.py](/ui/modals/__init__.py) | Python | 0 | 0 | 1 | 1 |
| [ui/modals/client_form_modal.py](/ui/modals/client_form_modal.py) | Python | 88 | 4 | 20 | 112 |
| [ui/modals/session_log_modal.py](/ui/modals/session_log_modal.py) | Python | 129 | 0 | 21 | 150 |
| [ui/pages/billing_page.py](/ui/pages/billing_page.py) | Python | 6 | 0 | 4 | 10 |
| [ui/pages/calendar_page.py](/ui/pages/calendar_page.py) | Python | 6 | 0 | 4 | 10 |
| [ui/pages/client_detail_page.py](/ui/pages/client_detail_page.py) | Python | 49 | 0 | 10 | 59 |
| [ui/pages/client_detail_page_components/__init__.py](/ui/pages/client_detail_page_components/__init__.py) | Python | 0 | 0 | 1 | 1 |
| [ui/pages/client_detail_page_components/anamnese_tab.py](/ui/pages/client_detail_page_components/anamnese_tab.py) | Python | 45 | 0 | 14 | 59 |
| [ui/pages/client_detail_page_components/fiche_nutrition_tab.py](/ui/pages/client_detail_page_components/fiche_nutrition_tab.py) | Python | 203 | 1 | 28 | 232 |
| [ui/pages/client_detail_page_components/stats_tab.py](/ui/pages/client_detail_page_components/stats_tab.py) | Python | 76 | 0 | 16 | 92 |
| [ui/pages/client_detail_page_components/suivi_tab.py](/ui/pages/client_detail_page_components/suivi_tab.py) | Python | 41 | 0 | 10 | 51 |
| [ui/pages/clients_page.py](/ui/pages/clients_page.py) | Python | 74 | 3 | 21 | 98 |
| [ui/pages/dashboard_page.py](/ui/pages/dashboard_page.py) | Python | 186 | 13 | 41 | 240 |
| [ui/pages/database_page.py](/ui/pages/database_page.py) | Python | 42 | 2 | 12 | 56 |
| [ui/pages/database_page_tabs/__init__.py](/ui/pages/database_page_tabs/__init__.py) | Python | 0 | 0 | 1 | 1 |
| [ui/pages/database_page_tabs/aliments_tab.py](/ui/pages/database_page_tabs/aliments_tab.py) | Python | 49 | 0 | 12 | 61 |
| [ui/pages/messaging_page.py](/ui/pages/messaging_page.py) | Python | 6 | 0 | 4 | 10 |
| [ui/pages/nutrition_page.py](/ui/pages/nutrition_page.py) | Python | 226 | 4 | 36 | 266 |
| [ui/pages/pdf_page.py](/ui/pages/pdf_page.py) | Python | 6 | 0 | 4 | 10 |
| [ui/pages/program_page.py](/ui/pages/program_page.py) | Python | 6 | 0 | 4 | 10 |
| [ui/pages/progress_page.py](/ui/pages/progress_page.py) | Python | 6 | 0 | 4 | 10 |
| [ui/pages/session_page.py](/ui/pages/session_page.py) | Python | 107 | 1 | 26 | 134 |
| [ui/pages/session_page_components/__init__.py](/ui/pages/session_page_components/__init__.py) | Python | 0 | 1 | 1 | 2 |
| [ui/pages/session_page_components/block_card.py](/ui/pages/session_page_components/block_card.py) | Python | 91 | 5 | 19 | 115 |
| [ui/pages/session_page_components/form_collectif.py](/ui/pages/session_page_components/form_collectif.py) | Python | 151 | 8 | 13 | 172 |
| [ui/pages/session_page_components/form_individuel.py](/ui/pages/session_page_components/form_individuel.py) | Python | 54 | 3 | 11 | 68 |
| [ui/pages/session_page_components/session_preview.py](/ui/pages/session_page_components/session_preview.py) | Python | 86 | 6 | 18 | 110 |
| [ui/pages/session_page_components/ui_helpers.py](/ui/pages/session_page_components/ui_helpers.py) | Python | 53 | 3 | 12 | 68 |
| [ui/pages/session_preview_panel.py](/ui/pages/session_preview_panel.py) | Python | 48 | 0 | 14 | 62 |
| [ui/theme/colors.py](/ui/theme/colors.py) | Python | 14 | 7 | 7 | 28 |
| [ui/theme/fonts.py](/ui/theme/fonts.py) | Python | 14 | 1 | 13 | 28 |
| [ui/theme/theme.py](/ui/theme/theme.py) | Python | 4 | 1 | 4 | 9 |
| [utils/icon_loader.py](/utils/icon_loader.py) | Python | 0 | 0 | 2 | 2 |

[Summary](results.md) / Details / [Diff Summary](diff.md) / [Diff Details](diff-details.md)