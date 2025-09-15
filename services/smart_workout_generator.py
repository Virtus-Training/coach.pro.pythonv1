"""
Générateur de séances intelligent avec logique métier avancée.
Intègre les règles CrossFit/Hyrox et les préférences configurables.
"""

import logging
import random
import time
import uuid
from collections import defaultdict
from datetime import date
from typing import Any, Dict, List, Optional, Set, Tuple

import services.session_templates as T
from models.exercices import Exercise
from models.session import Block, BlockItem, Session
from repositories.exercices_repo import ExerciseRepository
from services.workout_config_service import WorkoutConfigService


class SmartWorkoutGenerator:
    """Générateur de séances avec intelligence métier avancée."""

    def __init__(self, exercise_service=None, config_service: Optional[WorkoutConfigService] = None, exercise_repo: Optional[ExerciseRepository] = None):
        self.config_service = config_service or WorkoutConfigService()
        self.repo = exercise_repo or ExerciseRepository()
        self.exercise_service = exercise_service
        self.logger = logging.getLogger(__name__)

    def generate_collectif_smart(self, params: Dict[str, Any]) -> Session:
        """Génère une séance collective avec intelligence métier."""

        # Validation et préparation des paramètres avec defaults intelligents
        if not self._validate_input_params(params):
            raise ValueError("Paramètres d'entrée invalides pour la génération")

        smart_params = self._prepare_smart_params(params)

        # Obtenir recommandations basées sur historique
        context = {
            'course_type': smart_params['course_type'],
            'format': smart_params.get('primary_format', 'AMRAP'),
            'duration': smart_params['duration_min'],
            'equipment': smart_params.get('equipment', []),
        }
        recommendations = self.config_service.get_smart_recommendations(context)

        # Construire pool d'exercices avec pondération intelligente
        pool = self._build_intelligent_exercise_pool(smart_params, recommendations)

        if not pool:
            raise ValueError("Impossible de générer une séance : pool d'exercices insuffisant.")

        # Configurer randomisation
        variabilite = smart_params.get('variabilite', 50)
        seed = 42 if variabilite <= 10 else int(time.time())
        rng = random.Random(seed)
        entropy = self._calculate_entropy(variabilite)

        # Générer structure de séance avec règles métier
        session_structure = self._design_smart_session_structure(smart_params, rng, entropy)

        # Construire blocs avec contraintes physiologiques
        blocks = self._build_physiological_blocks(
            session_structure, pool, rng, entropy, smart_params, recommendations
        )

        # Validation et ajustements finaux avec optimisations professionnelles
        blocks = self._validate_and_adjust_session(blocks, smart_params)
        blocks = self._apply_professional_optimizations(blocks, smart_params)

        # Créer session finale
        session = Session(
            session_id=str(uuid.uuid4()),
            mode="COLLECTIF",
            label=self._generate_smart_session_name(smart_params),
            duration_sec=smart_params["duration_min"] * 60,
            date_creation=date.today().isoformat(),
            blocks=blocks,
            meta=self._build_session_metadata(smart_params, recommendations),
        )

        # Marquer comme généré par le système intelligent
        session._smart_generated = True

        # Analytics et feedback pour amélioration continue
        self._log_generation_metrics(session, smart_params, recommendations)

        self.logger.info(f"Séance générée: {session.label} - {len(blocks)} blocs")
        return session

    def _prepare_smart_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Prépare les paramètres avec intelligence et validations."""
        config = self.config_service.get_config()

        smart_params = params.copy()
        # Harmonisation des clés UI -> interne
        if "variability" in smart_params and "variabilite" not in smart_params:
            try:
                smart_params["variabilite"] = int(smart_params.get("variability", 50))
            except Exception:
                smart_params["variabilite"] = 50
        if "continuum" in smart_params and "continuum_cardio_renfo" not in smart_params:
            try:
                smart_params["continuum_cardio_renfo"] = int(smart_params.get("continuum", 0))
            except Exception:
                smart_params["continuum_cardio_renfo"] = 0
        if "objective" in smart_params and "objectif" not in smart_params:
            smart_params["objectif"] = smart_params.get("objective")
        smart_params.setdefault("variabilite", 50)
        smart_params.setdefault("volume", 50)
        smart_params.setdefault("continuum_cardio_renfo", 0)
        smart_params.setdefault("focus", "Full-body")
        smart_params.setdefault("objectif", "Conditioning")
        smart_params.setdefault("course_type", "Cross-Training")
        smart_params.setdefault("intensity", "Moyenne")
        smart_params.setdefault("user_level", "intermediate")

        # Conversion durée
        smart_params["duration_min"] = int(
            smart_params.get("duration") or smart_params.get("duration_min", 45)
        )

        # Mapping intensité
        intensity_map = {"Faible": 4, "Moyenne": 6, "Haute": 8, "Maximale": 9}
        intensity = smart_params.get("intensity", "Moyenne")
        smart_params["intensity_numeric"] = intensity_map.get(intensity, 6)

        # Formats enabled avec validation
        enabled_formats = smart_params.get("enabled_formats", smart_params.get("formats", []))
        allowed_formats = self._get_allowed_formats_for_course(smart_params["course_type"])
        smart_params["validated_formats"] = [f for f in enabled_formats if f in allowed_formats] or allowed_formats

        # Équipement disponible
        equipment = smart_params.get("equipment", [])
        equipment_config = config.equipment_management.get("available_equipment", [])
        smart_params["available_equipment"] = equipment or equipment_config

        return smart_params

    def _build_intelligent_exercise_pool(
        self, params: Dict[str, Any], recommendations: Dict[str, Any]
    ) -> List[Tuple[Exercise, float]]:
        """Construit un pool d'exercices avec pondération intelligente."""

        config = self.config_service.get_config()
        restrictions = self.config_service.get_exercise_restrictions_for_generation()

        # Filtrage initial
        equipment = params.get("equipment", [])  # Corrigé : utiliser la clé correcte du formulaire
        course_type = params.get("course_type", "Cross-Training")

        self.logger.info(f"Filtrage avec équipement: {equipment}")

        # Tags associés au type de cours
        course_tags = self._get_course_tags(course_type)

        # Récupérer exercices depuis repo
        exercises = self.repo.filter(equipment=equipment, tags=course_tags)

        self.logger.info(f"Exercices trouvés avec équipement {equipment}: {len(exercises)}")

        # Si pas d'exercices avec l'équipement spécifique, fallback plus intelligent
        if not exercises and equipment:
            self.logger.info("Peu d'exercices avec l'équipement spécifié, ajout du poids du corps")
            # Ajouter "Poids du corps" si pas déjà présent
            extended_equipment = equipment.copy()
            if "Poids du corps" not in extended_equipment:
                extended_equipment.append("Poids du corps")
            exercises = self.repo.filter(equipment=extended_equipment, tags=course_tags)

        if not exercises:
            self.logger.info("Aucun exercice avec équipement étendu, fallback vers tags uniquement")
            exercises = self.repo.filter(tags=course_tags)

        if not exercises:
            self.logger.info("Aucun exercice avec tags, utilisation de tous les exercices")
            exercises = self.repo.list_all()

        # Filtrer selon restrictions
        valid_exercises = []
        user_level = params.get("user_level", "beginner")

        for ex in exercises:
            if self.config_service.validate_exercise_for_context(ex.nom, course_type, user_level):
                valid_exercises.append(ex)

        if not valid_exercises:
            self.logger.info("Aucun exercice valide trouvé après validation, utilisation du pool complet")
            # Fallback amélioré respectant l'équipement
            if equipment:
                # Essayer d'abord avec l'équipement demandé
                fallback_exercises = self.repo.filter(equipment=equipment)
                if not fallback_exercises:
                    # Si rien, ajouter poids du corps
                    extended_equipment = equipment + ["Poids du corps"]
                    fallback_exercises = self.repo.filter(equipment=extended_equipment)

                if fallback_exercises:
                    valid_exercises = fallback_exercises[:50]
                else:
                    self.logger.warning("Impossible de respecter l'équipement, utilisation pool complet")
                    valid_exercises = self.repo.list_all()[:50]
            else:
                valid_exercises = self.repo.list_all()[:50]

        # Pondération intelligente
        weighted_pool = []
        for ex in valid_exercises:
            weight = self._calculate_intelligent_weight(ex, params, recommendations, config)
            if weight > 0.1:  # Seuil minimal
                weighted_pool.append((ex, weight))

        # Trier par poids décroissant
        weighted_pool.sort(key=lambda x: x[1], reverse=True)

        self.logger.info(f"Pool d'exercices construit: {len(weighted_pool)} exercices valides")
        return weighted_pool

    def _calculate_intelligent_weight(
        self,
        exercise: Exercise,
        params: Dict[str, Any],
        recommendations: Dict[str, Any],
        config
    ) -> float:
        """Calcule un poids intelligent pour un exercice selon contexte."""

        weight = 1.0
        ex_tags = [t.strip().lower() for t in (exercise.tags or "").split(",")]
        pattern = (exercise.movement_pattern or "").lower()
        muscle_group = (exercise.groupe_musculaire_principal or "").lower()

        # === BONUS SELON OBJECTIF ===
        objectif = (params.get("objectif") or "").lower()
        if objectif in ["force", "strength"] and exercise.est_chargeable:
            weight *= 1.4
        elif objectif in ["cardio", "conditioning"] and any(tag in ex_tags for tag in ["cardio", "conditioning"]):
            weight *= 1.3
        elif objectif in ["technique", "skill"] and any(tag in ex_tags for tag in ["technique", "skill"]):
            weight *= 1.2

        # === BONUS SELON CONTINUUM CARDIO-RENFO ===
        continuum = params.get("continuum_cardio_renfo", 0)
        if continuum > 20:  # Plus cardio
            if any(tag in ex_tags for tag in ["cardio", "conditioning", "metabolic"]):
                weight *= 1 + (continuum / 100)
            elif exercise.est_chargeable and pattern in ["squat", "hinge"]:
                weight *= 0.8
        elif continuum < -20:  # Plus renforcement
            if exercise.est_chargeable or pattern in ["push", "pull", "squat", "hinge"]:
                weight *= 1 + (abs(continuum) / 100)
            elif any(tag in ex_tags for tag in ["cardio", "plyometric"]):
                weight *= 0.7

        # === BONUS SELON FOCUS ===
        focus = params.get("focus", "Full-body")
        focus_patterns = {
            "Upper": ["push", "pull", "carry"],
            "Lower": ["squat", "hinge", "lunge"],
            "Push": ["push"],
            "Pull": ["pull"],
            "Core": ["twist", "carry"],
        }

        if focus in focus_patterns and pattern in focus_patterns[focus]:
            weight *= 1.5
        elif focus != "Full-body" and pattern not in focus_patterns.get(focus, []):
            weight *= 0.6

        # === BONUS EXERCICES FAVORIS ===
        favorites = config.favorite_exercises
        for context, fav_list in favorites.items():
            if exercise.nom in fav_list:
                weight *= 1.2
                break

        # === MALUS RESTRICTIONS FRÉQUENCE ===
        limited_freq = config.exercise_restrictions.get("limited_frequency", {})
        if exercise.nom in limited_freq:
            # Réduire poids selon restriction (0.3 = 30% max -> poids * 0.7)
            freq_limit = limited_freq[exercise.nom]
            weight *= (1 - freq_limit + 0.1)  # +0.1 pour éviter poids = 0

        # === BONUS SELON RECOMMANDATIONS HISTORIQUES ===
        suggested = recommendations.get("suggested_exercises", [])
        for suggestion_list in suggested:
            if exercise.nom in suggestion_list:
                weight *= 1.3
                break

        # === MALUS COMPLEXITÉ VS INTENSITÉ ===
        intensity = params.get("intensity_numeric", 6)
        if hasattr(exercise, "complexity_level"):
            complexity = getattr(exercise, "complexity_level", "moderate")
            if complexity == "high" and intensity >= 8:
                weight *= 0.8  # Éviter exercices complexes Ã  haute intensité

        return max(weight, 0.05)  # Poids minimum

    def _design_smart_session_structure(
        self, params: Dict[str, Any], rng: random.Random, entropy: float
    ) -> List[Dict[str, Any]]:
        """Conçoit une structure de séance intelligente."""

        # Prise en charge d'une structure personnalisée transmise par l'UI
        custom_blocks = params.get("custom_blocks") or []
        if isinstance(custom_blocks, list) and custom_blocks:
            smart_structure: List[Dict[str, Any]] = []
            for blk in custom_blocks:
                fmt = str(blk.get("type", "AMRAP"))
                try:
                    dur_min = int(blk.get("duration_min", 10))
                except Exception:
                    dur_min = 10
                fmt_rules = self.config_service.get_config().format_rules.get(fmt, {})
                base_items = int(fmt_rules.get("optimal_exercises", 4))
                # Variation 2-5 exercices avec logique intelligente
                if dur_min <= 8:
                    items = max(2, min(base_items - 1, 3))  # Séances courtes: 2-3 exos
                elif dur_min >= 20:
                    items = max(3, min(base_items + 1, 5))  # Séances longues: 3-5 exos
                else:
                    items = max(2, min(base_items, 5))      # Séances normales: 2-5 selon format
                # Calculer rounds intelligemment selon le format et la durée
                rounds = self._calculate_intelligent_rounds(fmt, dur_min, items)

                smart_structure.append({
                    "slot": "custom",
                    "type": fmt,
                    "duration_sec": max(60, dur_min * 60),
                    "items": items,
                    "rounds": rounds,
                })
            return smart_structure

        duration_min = params["duration_min"]
        course_type = params["course_type"]
        validated_formats = params["validated_formats"]
        auto_include = params.get("auto_include", [])

        # Récupérer template de base
        base_template = T.pick_template(course_type, duration_min)

        # Améliorer template avec logique métier selon auto_include
        smart_structure = []

        # Mapping des noms UI vers les slots techniques
        include_mapping = {
            "Échauffement": "warmup",
            "Finisher": "finisher",
            "Retour au calme": "cooldown"
        }

        for slot in base_template:
            slot_name = slot.get("slot", "main")

            # Vérifier si ce slot doit être inclus selon auto_include
            should_include = True
            for ui_name, tech_name in include_mapping.items():
                if tech_name == slot_name and ui_name not in auto_include:
                    should_include = False
                    break

            if not should_include:
                continue  # Ignorer ce slot
            smart_slot = slot.copy()

            # === AMÉLIORATION WARMUP ===
            if slot.get("slot") == "warmup":
                # Ajuster durée selon durée totale
                warmup_ratio = 0.15 if duration_min >= 60 else 0.12
                smart_slot["duration_sec"] = int(duration_min * 60 * warmup_ratio)
                smart_slot["items"] = 4 if duration_min >= 60 else 3
                smart_slot["focus"] = "activation"
                # Warmup généralement en circuit simple
                smart_slot["rounds"] = self._calculate_intelligent_rounds(
                    smart_slot.get("type", "Circuit"),
                    smart_slot["duration_sec"] // 60,
                    smart_slot["items"]
                )

            # === AMÉLIORATION MAIN ===
            elif slot.get("slot") == "main":
                # Choisir format optimal selon paramètres
                optimal_format = self._choose_optimal_format(
                    validated_formats, course_type, params, rng, entropy
                )
                smart_slot["type"] = optimal_format

                # Ajuster nombre d'exercices selon format
                format_rules = self.config_service.get_config().format_rules.get(optimal_format, {})
                base_items = format_rules.get("optimal_exercises", 4)

                # Ajustement intelligent 2-5 exercices selon durée et format
                slot_duration_min = smart_slot.get("duration_sec", 0) // 60

                if optimal_format == "TABATA":
                    items = 1  # Tabata reste à 1 exercice
                elif optimal_format == "AMRAP":
                    items = max(3, min(5, 3 + (slot_duration_min // 8)))  # 3-5 selon durée
                elif optimal_format == "EMOM":
                    items = max(2, min(4, 2 + (slot_duration_min // 6)))  # 2-4 pour EMOM
                elif optimal_format == "For Time":
                    items = max(3, min(5, 4 + (slot_duration_min // 10))) # 3-5 pour For Time
                elif optimal_format == "Skill":
                    items = max(1, min(3, 1 + (slot_duration_min // 5)))  # 1-3 pour Skill
                else:
                    items = max(2, min(5, base_items))  # 2-5 par défaut

                smart_slot["items"] = items

                # Calculer durée main en fonction du volume
                volume = params.get("volume", 50)
                main_ratio = 0.6 + (volume / 100) * 0.2  # 0.6 Ã  0.8 selon volume
                smart_slot["duration_sec"] = int(duration_min * 60 * main_ratio)

                # Calculer rounds pour le bloc principal
                smart_slot["rounds"] = self._calculate_intelligent_rounds(
                    optimal_format,
                    smart_slot["duration_sec"] // 60,
                    smart_slot["items"]
                )

            # === AMÉLIORATION FINISHER ===
            elif slot.get("slot") == "finisher":
                # Choisir format finisher approprié
                finisher_formats = ["Tabata", "EMOM", "Max Effort"]
                if entropy >= 0.3 and "Tabata" in validated_formats:
                    smart_slot["type"] = "Tabata"
                elif "EMOM" in validated_formats:
                    smart_slot["type"] = "EMOM"
                    smart_slot["duration_sec"] = 300  # 5 minutes EMOM
                else:
                    smart_slot["type"] = "Max Effort"
                    smart_slot["duration_sec"] = 180  # 3 minutes max effort

                smart_slot["items"] = 1  # Finisher = 1 exercice intense
                smart_slot["focus"] = "metabolic"

                # Calculer rounds pour le finisher
                smart_slot["rounds"] = self._calculate_intelligent_rounds(
                    smart_slot["type"],
                    smart_slot["duration_sec"] // 60,
                    smart_slot["items"]
                )

            smart_structure.append(smart_slot)

        return smart_structure

    def _choose_optimal_format(
        self,
        available_formats: List[str],
        course_type: str,
        params: Dict[str, Any],
        rng: random.Random,
        entropy: float
    ) -> str:
        """Choisit le format optimal selon le contexte."""

        intensity = params.get("intensity_numeric", 6)
        duration = params.get("duration_min", 45)

        # Règles métier par format
        format_scores = {}

        for fmt in available_formats:
            score = 1.0

            # AMRAP : idéal pour conditioning, durées moyennes
            if fmt == "AMRAP":
                if 45 <= duration <= 60:
                    score *= 1.3
                if course_type in ["Cross-Training", "CAF"]:
                    score *= 1.2
                if 5 <= intensity <= 7:
                    score *= 1.1

            # EMOM : idéal pour technique et force-endurance
            elif fmt == "EMOM":
                if course_type in ["Core & Glutes", "TRX"]:
                    score *= 1.4
                if intensity >= 7:
                    score *= 1.2
                if duration >= 50:
                    score *= 1.1

            # For Time : idéal pour Hyrox et intensité haute
            elif fmt == "For Time":
                if course_type == "Hyrox":
                    score *= 1.5
                if intensity >= 8:
                    score *= 1.3
                if duration <= 50:
                    score *= 1.1

            # Tabata : idéal pour finishers et haute intensité
            elif fmt == "Tabata":
                if intensity >= 8:
                    score *= 1.2
                else:
                    score *= 0.7  # Moins adapté pour faible intensité

            format_scores[fmt] = score

        # Choix selon entropy
        if entropy < 0.2:
            # Déterministe : meilleur score
            return max(format_scores.items(), key=lambda x: x[1])[0]
        else:
            # Pondéré aléatoire
            formats, scores = zip(*format_scores.items())
            return rng.choices(formats, weights=scores)[0]

    def _build_physiological_blocks(
        self,
        structure: List[Dict[str, Any]],
        pool: List[Tuple[Exercise, float]],
        rng: random.Random,
        entropy: float,
        params: Dict[str, Any],
        recommendations: Dict[str, Any]
    ) -> List[Block]:
        """Construit des blocs avec contraintes physiologiques."""

        config = self.config_service.get_config()
        physiological_rules = config.physiological_rules

        blocks = []
        used_exercises: Set[int] = set()
        muscle_usage_count = defaultdict(int)
        last_patterns = []

        for slot in structure:
            block = self._build_physiological_block(
                slot, pool, rng, entropy, params,
                used_exercises, muscle_usage_count, last_patterns,
                physiological_rules, recommendations
            )
            blocks.append(block)

            # Mettre Ã  jour historique
            for item in block.items:
                used_exercises.add(item.exercise_id)
                # Trouver l'exercice pour récupérer infos
                for ex, _ in pool:
                    if ex.id == item.exercise_id:
                        if ex.groupe_musculaire_principal:
                            muscle_usage_count[ex.groupe_musculaire_principal] += 1
                        if ex.movement_pattern:
                            last_patterns.append(ex.movement_pattern)
                            if len(last_patterns) > 3:
                                last_patterns.pop(0)  # Garder seulement 3 derniers
                        break

        return blocks

    def _build_physiological_block(
        self,
        slot: Dict[str, Any],
        pool: List[Tuple[Exercise, float]],
        rng: random.Random,
        entropy: float,
        params: Dict[str, Any],
        used_exercises: Set[int],
        muscle_usage_count: defaultdict,
        last_patterns: List[str],
        physiological_rules: Dict[str, Any],
        recommendations: Dict[str, Any]
    ) -> Block:
        """Construit un bloc avec contraintes physiologiques avancées."""

        block = Block(block_id=str(uuid.uuid4()), type=slot["type"])
        block.duration_sec = slot.get("duration_sec", 0)
        block.rounds = slot.get("rounds", 0)
        block.work_sec = slot.get("work_sec", 0)
        block.rest_sec = slot.get("rest_sec", 0)

        n_items = slot.get("items", 1)
        slot_focus = slot.get("focus", "general")

        # Contraintes physiologiques
        max_consecutive = physiological_rules["fatigue_management"]["max_consecutive_high_intensity"]

        selected_exercises = []
        consecutive_high_intensity = 0

        for i in range(n_items):
            # Construire pool candidat avec contraintes
            candidate_pool = self._build_candidate_pool(
                pool, slot_focus, used_exercises, muscle_usage_count,
                last_patterns, consecutive_high_intensity, max_consecutive,
                physiological_rules
            )

            if not candidate_pool:
                self.logger.warning("Pool candidat vide, utilisation pool complet")
                candidate_pool = pool

            # Sélection avec entropy et anti-répétition
            used_exercise_names = {ex.nom for ex in selected_exercises}  # Exercices déjà dans ce bloc
            exercise = self._weighted_choice_entropy(rng, candidate_pool, entropy, used_exercise_names)
            selected_exercises.append(exercise)

            # Mise Ã  jour des contraintes pour prochaine itération
            used_exercises.add(exercise.id)
            if exercise.groupe_musculaire_principal:
                muscle_usage_count[exercise.groupe_musculaire_principal] += 1
            if exercise.movement_pattern:
                last_patterns.append(exercise.movement_pattern)

            # Vérifier intensité (approximation via tags)
            ex_tags = [t.strip().lower() for t in (exercise.tags or "").split(",")]
            if any(tag in ex_tags for tag in ["high_intensity", "explosive", "cardio"]):
                consecutive_high_intensity += 1
            else:
                consecutive_high_intensity = 0

            # Créer prescription
            prescription = self._create_smart_prescription(
                exercise, slot, params, recommendations
            )

            block.items.append(BlockItem(
                exercise_id=exercise.id,
                prescription=prescription
            ))

        return block

    def _build_candidate_pool(
        self,
        pool: List[Tuple[Exercise, float]],
        slot_focus: str,
        used_exercises: Set[int],
        muscle_usage_count: defaultdict,
        last_patterns: List[str],
        consecutive_high_intensity: int,
        max_consecutive: int,
        physiological_rules: Dict[str, Any]
    ) -> List[Tuple[Exercise, float]]:
        """Construit un pool de candidats selon contraintes physiologiques."""

        candidates = []

        for exercise, weight in pool:
            # Éviter répétition d'exercices
            if exercise.id in used_exercises:
                weight *= 0.2  # Forte pénalité mais pas exclusion totale

            # Éviter répétition de patterns récents
            if exercise.movement_pattern in last_patterns[-2:]:  # 2 derniers
                weight *= 0.5

            # Équilibrage musculaire
            muscle = exercise.groupe_musculaire_principal
            muscle_count = muscle_usage_count.get(muscle, 0)
            if muscle_count >= 2:  # DéjÃ  utilisé 2 fois
                weight *= 0.3
            elif muscle_count >= 1:
                weight *= 0.7

            # Gestion fatigue/intensité
            ex_tags = [t.strip().lower() for t in (exercise.tags or "").split(",")]
            is_high_intensity = any(tag in ex_tags for tag in ["high_intensity", "explosive", "cardio"])

            if consecutive_high_intensity >= max_consecutive and is_high_intensity:
                weight *= 0.1  # Éviter surcharge

            # Bonus selon focus du slot
            if slot_focus == "activation" and any(tag in ex_tags for tag in ["mobility", "activation"]):
                weight *= 1.3
            elif slot_focus == "metabolic" and any(tag in ex_tags for tag in ["cardio", "metabolic"]):
                weight *= 1.4

            if weight > 0.05:  # Seuil minimal
                candidates.append((exercise, weight))

        return candidates

    def _create_smart_prescription(
        self,
        exercise: Exercise,
        slot: Dict[str, Any],
        params: Dict[str, Any],
        recommendations: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Crée une prescription intelligente pour l'exercice."""

        block_type = slot["type"]
        intensity = params.get("intensity_numeric", 6)

        # Obtenir fourchette de reps optimale
        complexity = self._assess_exercise_complexity(exercise)
        rep_range = self.config_service.get_optimal_rep_range(block_type, complexity)

        # Calculer reps selon intensité
        base_reps = (rep_range[0] + rep_range[1]) // 2
        intensity_factor = 0.8 + (intensity / 10) * 0.4  # 0.8 Ã  1.2
        final_reps = int(base_reps * intensity_factor)
        final_reps = max(rep_range[0], min(rep_range[1], final_reps))

        # Prescription selon format
        config = self.config_service.get_config()
        timing_rules = config.timing_rules
        base_rest = self._calculate_smart_rest(intensity, exercise, timing_rules)

        prescription = {}

        if block_type in ["AMRAP", "SETSxREPS"]:
            prescription = {
                "reps": final_reps,
                "rest_sec": base_rest,
            }
        elif block_type == "For Time":
            # Ajuster pour temps chronométré
            prescription = {
                "reps": final_reps + 3,  # Plus de reps pour For Time
                "rest_sec": max(30, base_rest),
            }
        elif block_type == "EMOM":
            # Moins de reps pour EMOM (doit finir dans la minute)
            prescription = {
                "reps": max(3, final_reps - 2),
            }
        elif block_type == "Tabata":
            prescription = {
                "work_sec": slot.get("work_sec", 20),
                "rest_sec": slot.get("rest_sec", 10),
            }
        elif block_type == "Skill":
            # Pour le travail technique, privilégier la qualité
            prescription = {
                "reps": max(3, min(8, final_reps - 3)),  # Moins de reps pour la qualité
                "rest_sec": max(60, base_rest * 2),      # Plus de repos pour récupération
                "focus": "qualité",                     # Indication spéciale
            }
        else:
            prescription = {"reps": final_reps}

        # Ajouts spéciaux pour exercices chargés
        if exercise.est_chargeable:
            prescription["weight_suggestion"] = self._suggest_weight_percentage(exercise, intensity)

        return prescription

    def _assess_exercise_complexity(self, exercise: Exercise) -> str:
        """Évalue la complexité d'un exercice."""
        ex_tags = [t.strip().lower() for t in (exercise.tags or "").split(",")]

        if any(tag in ex_tags for tag in ["olympic", "complex", "technical"]):
            return "complex"
        elif any(tag in ex_tags for tag in ["basic", "simple", "beginner"]):
            return "simple"
        else:
            return "moderate"

    def _calculate_smart_rest(self, intensity: int, exercise: Exercise, timing_rules: Dict[str, Any]) -> int:
        """Calcule un temps de repos intelligent."""

        base_rest = timing_rules.get("transition_time_sec", 30)

        # Ajuster selon intensité
        if intensity >= 8:
            base_rest = int(base_rest * 1.5)  # Plus de repos Ã  haute intensité
        elif intensity <= 4:
            base_rest = int(base_rest * 0.8)  # Moins de repos Ã  faible intensité

        # Ajuster selon type d'exercice
        ex_tags = [t.strip().lower() for t in (exercise.tags or "").split(",")]

        if exercise.est_chargeable or any(tag in ex_tags for tag in ["strength", "heavy"]):
            base_rest += 30  # Plus de repos pour exercices lourds
        elif any(tag in ex_tags for tag in ["cardio", "light", "bodyweight"]):
            base_rest = max(15, base_rest - 15)  # Moins de repos pour cardio

        return base_rest

    def _suggest_weight_percentage(self, exercise: Exercise, intensity: int) -> str:
        """Suggère un pourcentage de charge."""

        # Mapping intensité -> pourcentage 1RM approximatif
        intensity_to_percent = {
            4: "60-65%",   # Faible
            5: "65-70%",   # Faible-moyenne
            6: "70-75%",   # Moyenne
            7: "75-80%",   # Moyenne-haute
            8: "80-85%",   # Haute
            9: "85-90%",   # Très haute
            10: "90-95%",  # Maximale
        }

        return intensity_to_percent.get(intensity, "70-75%")

    def _weighted_choice_entropy(
        self, rng: random.Random, items: List[Tuple[Exercise, float]], entropy: float,
        used_exercises: Optional[Set[str]] = None
    ) -> Exercise:
        """Sélection pondérée avec entropy et anti-répétition."""
        if not items:
            raise ValueError("Pool vide")

        # Filtrer les exercices déjà utilisés pour améliorer la diversité
        if used_exercises:
            unused_items = [(ex, w) for ex, w in items if ex.nom not in used_exercises]
            # Si il reste des exercices non utilisés, les privilégier
            if unused_items and len(unused_items) >= len(items) * 0.3:  # Au moins 30% de nouveau
                items = unused_items
                # Booster le poids des exercices non utilisés
                items = [(ex, w * 1.5) for ex, w in items]

        if entropy <= 0.05:
            # Déterministe : meilleur poids
            return max(items, key=lambda x: x[1])[0]
        else:
            # Pondéré aléatoire avec diversité améliorée
            exercises, weights = zip(*items)
            return rng.choices(exercises, weights=weights)[0]

    def _validate_and_adjust_session(self, blocks: List[Block], params: Dict[str, Any]) -> List[Block]:
        """Valide et ajuste la séance selon contraintes finales."""

        config = self.config_service.get_config()
        balance_rules = config.muscle_balance_rules

        # Validation équilibrage musculaire
        muscle_counts = defaultdict(int)
        total_exercises = 0

        for block in blocks:
            for item in block.items:
                # Trouver exercice pour récupérer muscle group
                exercise = self.repo.get_by_id(item.exercise_id)
                if exercise:
                    muscle_group = exercise.groupe_musculaire_principal
                    if muscle_group:
                        muscle_counts[muscle_group.strip().lower()] += 1
                    total_exercises += 1

        # Vérification ratios
        if total_exercises > 0:
            # Push/Pull ratio
            push_keys = {"poitrine", "épaules", "epaules", "deltoides", "deltoids", "chest", "triceps"}
            pull_keys = {"dos", "back", "biceps"}
            push_count = sum(muscle_counts.get(k, 0) for k in push_keys)
            pull_count = sum(muscle_counts.get(k, 0) for k in pull_keys)

            if push_count + pull_count > 0:
                actual_ratio = push_count / (push_count + pull_count)
                target_ratio = balance_rules.get("push_pull_ratio", 0.6)

                if abs(actual_ratio - target_ratio) > 0.3:
                    self.logger.debug(f"Déséquilibre push/pull détecté: {actual_ratio:.2f} vs {target_ratio:.2f}")

        # Ajustements temporels
        total_planned = sum(block.duration_sec for block in blocks)
        target_duration = params["duration_min"] * 60

        if abs(total_planned - target_duration) > 300:  # Plus de 5 min d'écart
            adjustment_factor = target_duration / total_planned
            for block in blocks:
                block.duration_sec = int(block.duration_sec * adjustment_factor)

            self.logger.info(f"Ajustement temporel appliqué: facteur {adjustment_factor:.2f}")

        return blocks

    def _calculate_entropy(self, variabilite: int) -> float:
        """Calcule l'entropy selon la variabilité demandée."""
        return max(0.0, min(1.0, (variabilite / 100.0) ** 0.75))

    def _get_course_tags(self, course_type: str) -> List[str]:
        """Retourne les tags associés Ã  un type de cours."""
        tag_map = {
            "Cross-Training": ["cross-training", "functional"],
            "Hyrox": ["hyrox", "endurance", "functional"],
            "CAF": ["caf", "core", "glutes"],
            "Core & Glutes": ["core", "glutes", "stability"],
            "TRX": ["trx", "suspension", "functional"],
        }
        return tag_map.get(course_type, ["functional"])

    def _get_allowed_formats_for_course(self, course_type: str) -> List[str]:
        """Retourne les formats autorisés pour un type de cours."""
        format_map = {
            "CAF": ["AMRAP", "EMOM", "Tabata"],
            "Core & Glutes": ["EMOM", "AMRAP", "Tabata"],
            "Cross-Training": ["AMRAP", "EMOM", "For Time", "Tabata"],
            "Hyrox": ["For Time", "AMRAP", "EMOM"],
            "TRX": ["EMOM", "AMRAP", "Tabata"],
        }
        return format_map.get(course_type, ["AMRAP", "EMOM", "For Time", "Tabata"])

    def _generate_smart_session_name(self, params: Dict[str, Any]) -> str:
        """Génère un nom intelligent pour la séance."""
        course_type = params.get("course_type", "Workout")
        duration = params.get("duration_min", 45)
        intensity = params.get("intensity", "Moyenne")
        focus = params.get("focus", "Full-body")

        if focus != "Full-body":
            return f"{course_type} {focus} - {duration}' ({intensity})"
        else:
            return f"{course_type} {duration}' - {intensity}"

    def _build_session_metadata(self, params: Dict[str, Any], recommendations: Dict[str, Any]) -> Dict[str, Any]:
        """Construit les métadonnées de la séance."""
        return {
            "intensity": params.get("intensity", "Moyenne"),
            "course_type": params.get("course_type", "Cross-Training"),
            "focus": params.get("focus", "Full-body"),
            "generated_with": "SmartWorkoutGenerator",
            "generation_version": "1.0",
            "recommendations_used": bool(recommendations.get("suggested_exercises")),
            "config_applied": True,
        }

    def _validate_input_params(self, params: Dict[str, Any]) -> bool:
        """Valide les paramètres d'entrée avant génération (inspired by fitness apps validation)."""
        try:
            # Validation durée
            duration = params.get("duration", 0)
            if isinstance(duration, str):
                duration = int(duration)
            if not (10 <= duration <= 120):  # Entre 10min et 2h
                self.logger.warning(f"Durée invalide: {duration}min")
                return False

            # Validation équipement
            equipment = params.get("equipment", [])
            if not isinstance(equipment, list):
                return False

            # Validation continuum
            continuum = params.get("continuum", 0)
            if isinstance(continuum, str):
                try:
                    continuum = int(float(continuum))
                except ValueError:
                    continuum = 0
            if not (-100 <= continuum <= 100):
                return False

            return True
        except Exception as e:
            self.logger.error(f"Erreur validation params: {e}")
            return False

    def _apply_professional_optimizations(self, blocks: List[Block], params: Dict[str, Any]) -> List[Block]:
        """Applique des optimisations professionnelles comme dans MyFitnessPal/Nike Training."""
        optimized_blocks = []

        for i, block in enumerate(blocks):
            optimized_block = self._optimize_single_block(block, i, len(blocks), params)
            optimized_blocks.append(optimized_block)

        # Optimisation globale : équilibrage de l'intensité
        optimized_blocks = self._balance_session_intensity(optimized_blocks, params)

        # Optimisation transitions entre blocs
        optimized_blocks = self._optimize_block_transitions(optimized_blocks)

        return optimized_blocks

    def _optimize_single_block(self, block: Block, position: int, total_blocks: int, params: Dict[str, Any]) -> Block:
        """Optimise un bloc individuel selon sa position dans la séance."""
        intensity = params.get("intensity", "Moyenne")

        # Ajustement repos selon intensité et position
        intensity_multiplier = {
            "Légère": 0.8,
            "Moyenne": 1.0,
            "Élevée": 1.2,
            "Maximale": 1.5
        }.get(intensity, 1.0)

        # Position multiplier (début plus conservateur, fin plus intense)
        position_factor = 0.8 + (position / max(1, total_blocks - 1)) * 0.4

        for item in block.items:
            if item.prescription and "rest_sec" in item.prescription:
                current_rest = item.prescription["rest_sec"]
                adjusted_rest = int(current_rest * intensity_multiplier * position_factor)
                item.prescription["rest_sec"] = max(15, min(120, adjusted_rest))  # Entre 15s et 2min

        return block

    def _balance_session_intensity(self, blocks: List[Block], params: Dict[str, Any]) -> List[Block]:
        """Assure un profil d'intensité équilibré sur la séance."""
        if len(blocks) <= 1:
            return blocks

        # Pattern d'intensité selon type de cours
        course_type = params.get("course_type", "Cross-Training")

        if course_type == "Hyrox":
            # Pattern équilibré avec pic au milieu
            intensity_pattern = [0.7, 0.9, 1.0, 0.8] if len(blocks) >= 4 else [0.8, 1.0, 0.8]
        elif course_type == "CAF":
            # Pattern progressif
            intensity_pattern = [0.6, 0.8, 1.0]
        else:
            # Pattern classique
            intensity_pattern = [0.7, 1.0, 0.9, 0.7] if len(blocks) >= 4 else [0.8, 1.0, 0.8]

        # Appliquer le pattern
        for i, block in enumerate(blocks):
            pattern_index = min(i, len(intensity_pattern) - 1)
            factor = intensity_pattern[pattern_index]

            # Ajuster la durée selon le facteur d'intensité
            if hasattr(block, 'duration_sec'):
                block.duration_sec = max(300, int(block.duration_sec * factor))  # Min 5min

        return blocks

    def _optimize_block_transitions(self, blocks: List[Block]) -> List[Block]:
        """Optimise les transitions entre blocs pour la fluidité."""
        if len(blocks) <= 1:
            return blocks

        for i in range(len(blocks) - 1):
            current_block = blocks[i]
            next_block = blocks[i + 1]

            # Analyser les groupes musculaires pour éviter les conflits
            current_muscles = self._get_block_muscle_groups(current_block)
            next_muscles = self._get_block_muscle_groups(next_block)

            # Si même groupe musculaire principal, ajouter repos supplémentaire
            overlap = current_muscles.intersection(next_muscles)
            if overlap and len(overlap) > 0:
                # Ajouter 15-30s de repos supplémentaire au début du bloc suivant
                for item in next_block.items[:1]:  # Premier exercice du bloc suivant
                    if item.prescription and "rest_sec" in item.prescription:
                        item.prescription["rest_sec"] += 20

        return blocks

    def _get_block_muscle_groups(self, block: Block) -> Set[str]:
        """Récupère les groupes musculaires d'un bloc."""
        muscle_groups = set()

        for item in block.items:
            exercise = self.repo.get_by_id(item.exercise_id)
            if exercise and exercise.groupe_musculaire_principal:
                muscle_groups.add(exercise.groupe_musculaire_principal.lower().strip())

        return muscle_groups

    def _log_generation_metrics(self, session: Session, params: Dict[str, Any], recommendations: Dict[str, Any]) -> None:
        """Log des métriques pour l'amélioration continue du système."""
        metrics = {
            "session_duration": session.duration_sec // 60,
            "blocks_count": len(session.blocks),
            "total_exercises": sum(len(block.items) for block in session.blocks),
            "course_type": params.get("course_type"),
            "intensity": params.get("intensity"),
            "equipment_count": len(params.get("equipment", [])),
            "recommendations_applied": bool(recommendations.get("suggested_exercises")),
            "custom_blocks_used": bool(params.get("custom_blocks")),
        }

        self.logger.info(f"Métriques génération: {metrics}")

        # Ici on pourrait envoyer à un service d'analytics pour amélioration continue
        # analytics_service.track_generation(metrics)

    def _calculate_intelligent_rounds(self, format_type: str, duration_min: int, items: int) -> int:
        """Calcule un nombre de tours intelligent selon le format et la durée."""

        format_upper = format_type.upper()

        # AMRAP n'a pas de rounds fixes
        if format_upper == "AMRAP":
            return 0

        # Pour les autres formats, calculer selon la durée et le nombre d'exercices
        if format_upper == "EMOM":
            # Pour EMOM : exercices × tours = temps total (en minutes)
            # Donc tours = temps_total / nombre_exercices
            return max(1, duration_min // items) if items > 0 else duration_min

        elif format_upper == "TABATA":
            # Tabata classique: 8 tours de 20s work / 10s rest
            return 8

        elif format_upper in ["FOR_TIME", "For Time"]:
            # For Time: nombre de rounds basé sur durée et complexité
            base_rounds = max(2, min(6, duration_min // 3))  # 2-6 rounds selon durée
            # Ajuster selon nombre d'exercices (plus d'exos = moins de rounds)
            if items >= 6:
                return max(2, base_rounds - 1)
            elif items <= 3:
                return min(6, base_rounds + 1)
            return base_rounds

        elif format_upper == "SETSxREPS":
            # Sets x Reps: généralement 3-5 tours
            if duration_min <= 10:
                return 3
            elif duration_min >= 20:
                return 5
            else:
                return 4

        # Format non reconnu, retour par défaut
        # Pour Skill, pas de tours fixes mais du temps de pratique
        if format_upper == "SKILL":
            return 0  # Travail en temps continu, pas en tours

        # Format non reconnu, retour par défaut
        return max(2, min(5, duration_min // 4))


