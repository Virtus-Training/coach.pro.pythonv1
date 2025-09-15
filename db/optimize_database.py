"""
Module d'optimisation de la base de données pour les performances nutritionnelles
Crée les index appropriés pour des recherches sub-200ms
"""

import sqlite3
import time
from typing import Dict, List

from db.database_manager import db_manager


class DatabaseOptimizer:
    """Optimiseur de performance pour la base de données nutritionnelle"""

    def __init__(self):
        self.optimization_history = []

    def optimize_full_database(self) -> Dict[str, any]:
        """Optimisation complète de la base de données"""

        start_time = time.time()
        results = {}

        print("🚀 Début de l'optimisation de la base de données...")

        # 1. Création des index pour les aliments
        results["aliments_indexes"] = self._create_aliments_indexes()

        # 2. Création des index pour les profils nutritionnels
        results["profils_indexes"] = self._create_profils_indexes()

        # 3. Création des index pour les plans alimentaires
        results["plans_indexes"] = self._create_plans_indexes()

        # 4. Optimisation des index existants
        results["existing_optimization"] = self._optimize_existing_indexes()

        # 5. Analyse et statistiques
        results["statistics"] = self._analyze_database_stats()

        # 6. Configuration SQLite pour les performances
        results["sqlite_config"] = self._optimize_sqlite_settings()

        total_time = time.time() - start_time
        results["total_optimization_time"] = round(total_time, 2)

        print(f"✅ Optimisation terminée en {results['total_optimization_time']}s")

        return results

    def _create_aliments_indexes(self) -> Dict[str, bool]:
        """Crée les index optimaux pour la table aliments"""

        print("📊 Création des index pour la table 'aliments'...")

        indexes = {
            # Index de recherche textuelle (TRÈS IMPORTANT pour MyFitnessPal-like search)
            "idx_aliments_nom": "CREATE INDEX IF NOT EXISTS idx_aliments_nom ON aliments(nom COLLATE NOCASE)",
            "idx_aliments_nom_prefix": "CREATE INDEX IF NOT EXISTS idx_aliments_nom_prefix ON aliments(substr(nom, 1, 3))",
            # Index nutritionnels pour filtres rapides
            "idx_aliments_kcal": "CREATE INDEX IF NOT EXISTS idx_aliments_kcal ON aliments(kcal_100g)",
            "idx_aliments_proteines": "CREATE INDEX IF NOT EXISTS idx_aliments_proteines ON aliments(proteines_100g)",
            "idx_aliments_glucides": "CREATE INDEX IF NOT EXISTS idx_aliments_glucides ON aliments(glucides_100g)",
            "idx_aliments_lipides": "CREATE INDEX IF NOT EXISTS idx_aliments_lipides ON aliments(lipides_100g)",
            "idx_aliments_fibres": "CREATE INDEX IF NOT EXISTS idx_aliments_fibres ON aliments(fibres_100g)",
            # Index pour catégorisation et filtres
            "idx_aliments_categorie": "CREATE INDEX IF NOT EXISTS idx_aliments_categorie ON aliments(categorie)",
            "idx_aliments_type_alimentation": "CREATE INDEX IF NOT EXISTS idx_aliments_type_alimentation ON aliments(type_alimentation)",
            # Index pour les scores de qualité
            "idx_aliments_healthy": "CREATE INDEX IF NOT EXISTS idx_aliments_healthy ON aliments(indice_healthy DESC)",
            "idx_aliments_commun": "CREATE INDEX IF NOT EXISTS idx_aliments_commun ON aliments(indice_commun DESC)",
            # Index composés pour requêtes complexes (inspiré de Cronometer)
            "idx_aliments_cat_kcal": "CREATE INDEX IF NOT EXISTS idx_aliments_cat_kcal ON aliments(categorie, kcal_100g)",
            "idx_aliments_prot_healthy": "CREATE INDEX IF NOT EXISTS idx_aliments_prot_healthy ON aliments(proteines_100g DESC, indice_healthy DESC)",
            "idx_aliments_fibres_kcal": "CREATE INDEX IF NOT EXISTS idx_aliments_fibres_kcal ON aliments(fibres_100g DESC, kcal_100g ASC)",
            # Index pour tri par densité nutritionnelle (calcul rapide)
            "idx_aliments_densite_calc": """CREATE INDEX IF NOT EXISTS idx_aliments_densite_calc ON aliments(
                CASE WHEN kcal_100g > 0 THEN (proteines_100g * 4 + COALESCE(fibres_100g, 0) * 2) / kcal_100g ELSE 0 END DESC
            )""",
        }

        results = {}
        with db_manager.get_connection() as conn:
            for index_name, sql in indexes.items():
                try:
                    conn.execute(sql)
                    results[index_name] = True
                    print(f"  ✓ {index_name}")
                except Exception as e:
                    results[index_name] = False
                    print(f"  ✗ {index_name}: {str(e)}")

            conn.commit()

        return results

    def _create_profils_indexes(self) -> Dict[str, bool]:
        """Crée les index pour la table profils_nutritionnels"""

        print("👤 Création des index pour la table 'profils_nutritionnels'...")

        # S'assurer que la table existe d'abord
        with db_manager.get_connection() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS profils_nutritionnels (
                    id INTEGER PRIMARY KEY,
                    client_id INTEGER NOT NULL,
                    age INTEGER NOT NULL,
                    sexe TEXT NOT NULL,
                    poids_kg REAL NOT NULL,
                    taille_cm REAL NOT NULL,
                    objectif_principal TEXT NOT NULL,
                    niveau_activite TEXT NOT NULL,
                    restrictions_alimentaires TEXT DEFAULT '[]',
                    regimes_compatibles TEXT DEFAULT '[]',
                    aliments_preferes TEXT DEFAULT '[]',
                    aliments_exclus TEXT DEFAULT '[]',
                    nombre_repas_souhaite INTEGER DEFAULT 3,
                    metabolism_basal REAL,
                    besoins_caloriques REAL,
                    repartition_macros TEXT DEFAULT '{}',
                    date_creation TEXT NOT NULL,
                    date_mise_a_jour TEXT NOT NULL,
                    FOREIGN KEY(client_id) REFERENCES clients(id),
                    UNIQUE(client_id)
                )
                """
            )
            conn.commit()

        indexes = {
            # Index principal pour requêtes par client
            "idx_profils_client_id": "CREATE UNIQUE INDEX IF NOT EXISTS idx_profils_client_id ON profils_nutritionnels(client_id)",
            # Index pour filtres et analyses
            "idx_profils_objectif": "CREATE INDEX IF NOT EXISTS idx_profils_objectif ON profils_nutritionnels(objectif_principal)",
            "idx_profils_age_sexe": "CREATE INDEX IF NOT EXISTS idx_profils_age_sexe ON profils_nutritionnels(age, sexe)",
            "idx_profils_besoins_cal": "CREATE INDEX IF NOT EXISTS idx_profils_besoins_cal ON profils_nutritionnels(besoins_caloriques)",
            # Index pour analyses temporelles
            "idx_profils_date_maj": "CREATE INDEX IF NOT EXISTS idx_profils_date_maj ON profils_nutritionnels(date_mise_a_jour DESC)",
        }

        results = {}
        with db_manager.get_connection() as conn:
            for index_name, sql in indexes.items():
                try:
                    conn.execute(sql)
                    results[index_name] = True
                    print(f"  ✓ {index_name}")
                except Exception as e:
                    results[index_name] = False
                    print(f"  ✗ {index_name}: {str(e)}")

            conn.commit()

        return results

    def _create_plans_indexes(self) -> Dict[str, bool]:
        """Crée les index pour les tables de plans alimentaires"""

        print("🍽️ Création des index pour les tables de plans alimentaires...")

        indexes = {
            # Plans alimentaires
            "idx_plans_client_id": "CREATE INDEX IF NOT EXISTS idx_plans_client_id ON plans_alimentaires(client_id)",
            "idx_plans_tags": "CREATE INDEX IF NOT EXISTS idx_plans_tags ON plans_alimentaires(tags)",
            # Repas
            "idx_repas_plan_id": "CREATE INDEX IF NOT EXISTS idx_repas_plan_id ON repas(plan_id)",
            "idx_repas_plan_ordre": "CREATE INDEX IF NOT EXISTS idx_repas_plan_ordre ON repas(plan_id, ordre)",
            # Items de repas (critique pour performance)
            "idx_repas_items_repas_id": "CREATE INDEX IF NOT EXISTS idx_repas_items_repas_id ON repas_items(repas_id)",
            "idx_repas_items_aliment_id": "CREATE INDEX IF NOT EXISTS idx_repas_items_aliment_id ON repas_items(aliment_id)",
            "idx_repas_items_portion_id": "CREATE INDEX IF NOT EXISTS idx_repas_items_portion_id ON repas_items(portion_id)",
            # Portions (optimisation recherche)
            "idx_portions_aliment_id": "CREATE INDEX IF NOT EXISTS idx_portions_aliment_id ON portions(aliment_id)",
            "idx_portions_aliment_grammes": "CREATE INDEX IF NOT EXISTS idx_portions_aliment_grammes ON portions(aliment_id, grammes_equivalents)",
        }

        results = {}
        with db_manager.get_connection() as conn:
            for index_name, sql in indexes.items():
                try:
                    conn.execute(sql)
                    results[index_name] = True
                    print(f"  ✓ {index_name}")
                except Exception as e:
                    results[index_name] = False
                    print(f"  ✗ {index_name}: {str(e)}")

            conn.commit()

        return results

    def _optimize_existing_indexes(self) -> Dict[str, any]:
        """Optimise les index existants"""

        print("🔧 Optimisation des index existants...")

        with db_manager.get_connection() as conn:
            # Analyse et reconstruction si nécessaire
            conn.execute("ANALYZE")

            # Statistiques avant optimisation
            stats_before = self._get_index_stats(conn)

            # Reconstruction des index fragmentés (si SQLite le supportait)
            # Pour SQLite, on utilisera VACUUM au lieu
            conn.execute("VACUUM")

            # Statistiques après optimisation
            stats_after = self._get_index_stats(conn)

        return {
            "stats_before": stats_before,
            "stats_after": stats_after,
            "vacuum_executed": True,
        }

    def _get_index_stats(self, conn: sqlite3.Connection) -> Dict[str, any]:
        """Récupère les statistiques des index"""

        # Liste tous les index
        indexes = conn.execute(
            "SELECT name, tbl_name FROM sqlite_master WHERE type='index' AND name NOT LIKE 'sqlite_%'"
        ).fetchall()

        return {"total_indexes": len(indexes), "indexes_by_table": {}}

    def _analyze_database_stats(self) -> Dict[str, any]:
        """Analyse les statistiques de la base de données"""

        print("📈 Analyse des statistiques de la base de données...")

        with db_manager.get_connection() as conn:
            stats = {}

            # Taille de la base
            stats["database_size_pages"] = conn.execute("PRAGMA page_count").fetchone()[
                0
            ]
            stats["page_size_bytes"] = conn.execute("PRAGMA page_size").fetchone()[0]
            stats["database_size_mb"] = round(
                (stats["database_size_pages"] * stats["page_size_bytes"])
                / (1024 * 1024),
                2,
            )

            # Nombre d'enregistrements par table
            tables = [
                "aliments",
                "portions",
                "plans_alimentaires",
                "repas",
                "repas_items",
            ]
            for table in tables:
                try:
                    count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
                    stats[f"{table}_count"] = count
                except:
                    stats[f"{table}_count"] = 0

            # Test de performance sur requêtes critiques
            stats["performance_tests"] = self._run_performance_tests(conn)

        return stats

    def _run_performance_tests(self, conn: sqlite3.Connection) -> Dict[str, float]:
        """Exécute des tests de performance sur les requêtes critiques"""

        tests = {}

        # Test 1: Recherche d'aliment par nom
        start = time.time()
        conn.execute(
            "SELECT * FROM aliments WHERE nom LIKE '%poulet%' LIMIT 10"
        ).fetchall()
        tests["search_by_name_ms"] = round((time.time() - start) * 1000, 2)

        # Test 2: Recherche par catégorie et calories
        start = time.time()
        conn.execute(
            "SELECT * FROM aliments WHERE categorie = 'Viandes' AND kcal_100g < 200 ORDER BY proteines_100g DESC LIMIT 20"
        ).fetchall()
        tests["category_filter_ms"] = round((time.time() - start) * 1000, 2)

        # Test 3: Requête complexe avec jointures
        start = time.time()
        conn.execute(
            """
            SELECT a.nom, p.description, p.grammes_equivalents
            FROM aliments a
            JOIN portions p ON a.id = p.aliment_id
            WHERE a.proteines_100g > 20
            LIMIT 50
            """
        ).fetchall()
        tests["join_query_ms"] = round((time.time() - start) * 1000, 2)

        return tests

    def _optimize_sqlite_settings(self) -> Dict[str, any]:
        """Optimise les paramètres SQLite pour les performances"""

        print("⚙️ Configuration des paramètres SQLite...")

        optimizations = {
            # Cache plus important pour de meilleures performances
            "PRAGMA cache_size = -64000": "cache_size",  # 64MB de cache
            # Mode journal pour les performances (attention à la sécurité en prod)
            "PRAGMA journal_mode = WAL": "journal_mode",
            # Synchronisation optimisée
            "PRAGMA synchronous = NORMAL": "synchronous",
            # Optimisations de performance
            "PRAGMA temp_store = MEMORY": "temp_store",
            "PRAGMA mmap_size = 268435456": "mmap_size",  # 256MB memory-mapped I/O
            # Analyse automatique pour maintenir les statistiques
            "PRAGMA automatic_index = ON": "automatic_index",
        }

        results = {}
        with db_manager.get_connection() as conn:
            for pragma_sql, pragma_name in optimizations.items():
                try:
                    conn.execute(pragma_sql)
                    results[pragma_name] = "SUCCESS"
                    print(f"  ✓ {pragma_name}")
                except Exception as e:
                    results[pragma_name] = f"ERROR: {str(e)}"
                    print(f"  ✗ {pragma_name}: {str(e)}")

        return results

    def benchmark_critical_queries(self) -> Dict[str, float]:
        """Benchmark des requêtes critiques après optimisation"""

        print("🏁 Benchmark des requêtes critiques...")

        queries = {
            "simple_name_search": {
                "sql": "SELECT * FROM aliments WHERE nom LIKE ? ORDER BY nom LIMIT 20",
                "params": ("%tomate%",),
            },
            "advanced_filter": {
                "sql": """
                    SELECT * FROM aliments
                    WHERE categorie = ? AND proteines_100g >= ? AND kcal_100g <= ?
                    ORDER BY indice_healthy DESC, proteines_100g DESC
                    LIMIT 30
                """,
                "params": ("Viandes", 15.0, 300.0),
            },
            "nutritional_ranking": {
                "sql": """
                    SELECT *,
                           CASE WHEN kcal_100g > 0 THEN (proteines_100g * 4 + COALESCE(fibres_100g, 0) * 2) / kcal_100g ELSE 0 END as densite
                    FROM aliments
                    ORDER BY densite DESC
                    LIMIT 50
                """,
                "params": (),
            },
            "complementary_foods": {
                "sql": """
                    SELECT a.*,
                           ABS(a.proteines_100g - ?) + ABS(a.glucides_100g - ?) + ABS(a.lipides_100g - ?) as score
                    FROM aliments a
                    WHERE a.id != ?
                    ORDER BY score ASC
                    LIMIT 10
                """,
                "params": (25.0, 30.0, 15.0, 1),
            },
        }

        results = {}

        with db_manager.get_connection() as conn:
            for query_name, query_info in queries.items():
                # Mesure de performance (moyenne sur 3 exécutions)
                times = []

                for _ in range(3):
                    start = time.time()
                    conn.execute(query_info["sql"], query_info["params"]).fetchall()
                    times.append((time.time() - start) * 1000)

                avg_time = sum(times) / len(times)
                results[query_name] = round(avg_time, 2)

                # Vérification de l'objectif sub-200ms
                status = "✅" if avg_time < 200 else "⚠️" if avg_time < 500 else "❌"
                print(f"  {status} {query_name}: {avg_time:.2f}ms")

        return results

    def create_full_text_search_virtual_table(self) -> bool:
        """Crée une table virtuelle FTS pour la recherche textuelle avancée"""

        print("🔍 Création de la table FTS pour recherche avancée...")

        try:
            with db_manager.get_connection() as conn:
                # Création de la table FTS
                conn.execute(
                    """
                    CREATE VIRTUAL TABLE IF NOT EXISTS aliments_fts USING fts5(
                        nom,
                        categorie,
                        content='aliments',
                        content_rowid='id'
                    )
                    """
                )

                # Population de la table FTS
                conn.execute(
                    """
                    INSERT INTO aliments_fts(aliments_fts) VALUES('rebuild')
                    """
                )

                conn.commit()
                print("  ✅ Table FTS créée et populée")
                return True

        except Exception as e:
            print(f"  ❌ Erreur FTS: {str(e)}")
            return False

    def generate_optimization_report(self, results: Dict[str, any]) -> str:
        """Génère un rapport d'optimisation"""

        report = []
        report.append("=" * 60)
        report.append("📊 RAPPORT D'OPTIMISATION DE LA BASE DE DONNÉES")
        report.append("=" * 60)
        report.append("")

        # Résumé des performances
        if "statistics" in results and "performance_tests" in results["statistics"]:
            perf = results["statistics"]["performance_tests"]
            report.append("🏁 PERFORMANCES DES REQUÊTES CRITIQUES:")
            for test, time_ms in perf.items():
                status = "✅" if time_ms < 200 else "⚠️" if time_ms < 500 else "❌"
                report.append(f"  {status} {test}: {time_ms}ms")
            report.append("")

        # Statistiques de la base
        if "statistics" in results:
            stats = results["statistics"]
            report.append("📈 STATISTIQUES DE LA BASE:")
            report.append(f"  📏 Taille: {stats.get('database_size_mb', 'N/A')} MB")
            report.append(f"  🍎 Aliments: {stats.get('aliments_count', 'N/A')}")
            report.append(f"  📏 Portions: {stats.get('portions_count', 'N/A')}")
            report.append("")

        # Index créés
        total_indexes = 0
        for category, indexes in results.items():
            if isinstance(indexes, dict) and "indexes" in category:
                successful = sum(1 for success in indexes.values() if success)
                total = len(indexes)
                report.append(
                    f"📊 {category.upper()}: {successful}/{total} index créés"
                )
                total_indexes += successful

        report.append(f"\n🎯 TOTAL: {total_indexes} index optimisés")
        report.append(
            f"⏱️ Temps total: {results.get('total_optimization_time', 'N/A')}s"
        )
        report.append("")

        # Recommandations
        report.append("💡 RECOMMANDATIONS:")
        report.append("  • Exécuter ANALYZE périodiquement")
        report.append("  • Surveiller la croissance de la base")
        report.append("  • Considérer la compression pour les gros volumes")
        report.append("  • Tester les performances après ajout de données")

        return "\n".join(report)


def optimize_database_for_nutrition():
    """Point d'entrée principal pour l'optimisation"""

    optimizer = DatabaseOptimizer()

    # Optimisation complète
    results = optimizer.optimize_full_database()

    # Table FTS pour recherche avancée
    fts_success = optimizer.create_full_text_search_virtual_table()
    results["fts_created"] = fts_success

    # Benchmark final
    benchmark_results = optimizer.benchmark_critical_queries()
    results["final_benchmark"] = benchmark_results

    # Génération du rapport
    report = optimizer.generate_optimization_report(results)
    print("\n" + report)

    # Sauvegarde du rapport
    try:
        with open("database_optimization_report.txt", "w", encoding="utf-8") as f:
            f.write(report)
        print("\n📄 Rapport sauvegardé: database_optimization_report.txt")
    except Exception as e:
        print(f"\n⚠️ Impossible de sauvegarder le rapport: {e}")

    return results


if __name__ == "__main__":
    optimize_database_for_nutrition()
