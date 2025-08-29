import random
import time
import uuid
from typing import Any, Dict, List, Tuple

import services.session_templates as T
from models.exercices import Exercise
from models.session import Block, BlockItem, Session
from repositories.exercices_repo import ExerciseRepository


def rest_from_density(density_1_10: int) -> int:
    # 1 = repos long, 10 = repos très court
    return max(15, int(150 - (density_1_10 - 1) * 15))  # 150s → 15s


def reps_from_intensity(intensity_1_10: int, base: int) -> int:
    # Echelle grossière : intensité ↑ = reps ↑ pour AMRAP/EMOM; reps ↓ pour force
    return max(3, int(base * (0.8 + (intensity_1_10 / 10) * 0.6)))  # 0.8x .. 1.4x


def map_slider_to_entropy(v: int) -> float:
    # 0..100 -> 0.0..1.0 (courbe douce)
    return max(0.0, min(1.0, (v / 100.0) ** 0.75))


def filter_and_score_pool(
    repo: ExerciseRepository, params: Dict[str, Any]
) -> List[Tuple[Exercise, float]]:
    tags = []
    if params.get("course_type") == "Hyrox":
        tags.append("hyrox")
    if params.get("course_type") == "Cross-Training":
        tags.append("cross")

    exercises = repo.filter(equipment=params.get("equipment"), tags=tags or None)

    continuum = params.get("continuum_cardio_renfo", 0)
    focus = params.get("focus", "Full-body")
    objectif = params.get("objectif", "Force")

    focus_map = {
        "Upper": ["push", "pull", "carry"],
        "Lower": ["squat", "hinge"],
        "Push": ["push"],
        "Pull": ["pull"],
    }
    objectif_map = {
        "Force": ["force"],
        "Endurance": ["cardio", "conditionning", "endurance"],
        "Technique": ["technique"],
        "Hypertrophie": ["hypertrophie", "muscle"],
    }

    out: List[Tuple[Exercise, float]] = []
    for ex in exercises:
        weight = 1.0
        ex_tags = [t.strip().lower() for t in (ex.tags or "").split(",")]
        pattern = (ex.movement_pattern or "").lower()

        if continuum > 0:  # cardio → poids ↑ pour tags cardio/conditionning
            if "cardio" in ex_tags or "conditionning" in ex_tags:
                weight *= 1 + continuum / 100.0
            else:
                weight *= 1 - continuum / 200.0
        elif continuum < 0:  # renfo
            if (
                "force" in ex_tags
                or pattern in ["hinge", "squat", "push", "pull", "carry"]
            ):
                weight *= 1 + abs(continuum) / 100.0
            else:
                weight *= 1 - abs(continuum) / 200.0

        patterns_focus = focus_map.get(focus, [])
        if patterns_focus:
            if pattern in patterns_focus:
                weight *= 1.5
            else:
                weight *= 0.7

        obj_tags = objectif_map.get(objectif, [])
        if obj_tags:
            if any(t in ex_tags for t in obj_tags):
                weight *= 1.5
            else:
                weight *= 0.8

        out.append((ex, max(weight, 0.1)))

    out.sort(key=lambda x: x[1], reverse=True)
    return out


def weighted_choice(
    rng: random.Random, items: List[Tuple[Exercise, float]], entropy: float
) -> Exercise:
    if not items:
        raise ValueError("Pool is empty")
    if entropy <= 0.05:
        return sorted(items, key=lambda x: x[1], reverse=True)[0][0]
    exercises, weights = zip(*items)
    return rng.choices(exercises, weights=weights, k=1)[0]


def pick_main_block_count(duration_min: int, entropy: float) -> int:
    """1 bloc quand variabilité faible / temps serré, 2 blocs sinon."""
    if duration_min <= 45 and entropy < 0.35:
        return 1
    # plus de variété quand séance plus longue ou entropy plus haute
    return 2 if entropy >= 0.35 else 1


def split_minutes(total_sec: int, parts: int, rng: random.Random) -> list[int]:
    """Split aléatoire mais raisonnable (±20%)."""
    if parts == 1:
        return [total_sec]
    base = total_sec // parts
    jitter = int(base * 0.2)
    a = base + rng.randint(-jitter, jitter)
    b = total_sec - a
    return [max(4 * 60, a), max(4 * 60, b)]  # chaque bloc >= 4'


def allowed_formats_for_course(course_type: str) -> list[str]:
    by_course = {
        "CAF": ["AMRAP", "EMOM", "Tabata"],
        "Core & Glutes": ["EMOM", "AMRAP", "Tabata"],
        "Cross-Training": ["AMRAP", "EMOM", "For Time", "Tabata"],
        "Hyrox": [
            "For Time",
            "AMRAP",
            "EMOM",
        ],  # Tabata en finisher court, généralement
    }
    return by_course.get(course_type, ["AMRAP", "EMOM", "For Time", "Tabata"])


def choose_format(
    rng: random.Random, enabled: list[str], allowed: list[str], entropy: float
) -> str:
    pool = [f for f in enabled if f in allowed] or allowed
    if entropy < 0.15:
        return pool[0]  # plus déterministe
    return rng.choice(pool)


def build_block(
    slot: Dict[str, Any],
    pool: List[Tuple[Exercise, float]],
    rng: random.Random,
    entropy: float,
    params=None,
) -> Block:
    block = Block(block_id=str(uuid.uuid4()), type=slot["type"])
    block.duration_sec = slot.get("duration_sec", 0)
    block.rounds = slot.get("rounds", 0)
    block.work_sec = slot.get("work_sec", 0)
    block.rest_sec = slot.get("rest_sec", 0)

    density = (params or {}).get("density", 5)
    intensity = (params or {}).get("intensity_cont", 6)
    default_rest = rest_from_density(density)

    n_items = slot.get("items", 1)
    candidates = pool[:]
    rng.shuffle(candidates)

    last_pattern = None
    for _ in range(n_items):
        # filtre doux : éviter de reprendre le même pattern si possible
        candidates2 = [
            (ex, w) for ex, w in candidates if ex.movement_pattern != last_pattern
        ] or candidates
        ex = weighted_choice(rng, candidates2, entropy)

        if block.type in ("SETSxREPS", "AMRAP"):
            base_reps = 12 if getattr(ex, "category", "") != "Plyo/Power" else 8
            presc = {
                "reps": reps_from_intensity(intensity, base_reps),
                "rest_sec": default_rest,
            }
        elif block.type == "FORTIME":
            presc = {
                "reps": reps_from_intensity(intensity, 15),
                "rest_sec": max(30, default_rest),
            }
        elif block.type == "EMOM":
            presc = {"reps": reps_from_intensity(intensity, 10)}
        elif block.type == "TABATA":
            presc = {"work_sec": block.work_sec, "rest_sec": block.rest_sec}
        else:
            presc = {}
        block.items.append(BlockItem(exercise_id=ex.id, prescription=presc))
        last_pattern = ex.movement_pattern
    return block


def adjust_to_time_budget(blocks: List[Block], duration_min: int) -> List[Block]:
    # V1 : confiance sur templates; on garde une tolérance ±2'
    return blocks


def generate_collectif(params: Dict[str, Any]) -> Session:
    """Generate a collective session from form parameters."""
    params = params.copy()
    params.setdefault("variabilite", 50)
    params.setdefault("volume", 50)
    params.setdefault("enabled_formats", params.pop("formats", []))
    params.setdefault("continuum_cardio_renfo", 0)
    params.setdefault("focus", "Full-body")
    params.setdefault("objectif", "Force")
    params.setdefault("auto_include", [])
    params.setdefault("course_type", "Cross-Training")
    params.setdefault("intensity", "Moyenne")
    params["duration_min"] = int(
        params.get("duration") or params.get("duration_min", 0)
    )
    intensity_map = {"Faible": 4, "Moyenne": 6, "Haute": 8}
    intensity = params.get("intensity", "Moyenne")
    params["intensity"] = intensity
    params["intensity_cont"] = intensity_map.get(intensity, 6)

    tpl = T.pick_template(params["course_type"], params["duration_min"])
    repo = ExerciseRepository()
    pool = filter_and_score_pool(repo, params)
    if not pool:
        raise ValueError(
            "Impossible de générer une séance : la base de données d'exercices est vide."
        )
    variabilite = params.get("variabilite", 50)
    if variabilite <= 10:
        seed = 42
    else:
        seed = int(time.time())
    rng = random.Random(seed)
    entropy = map_slider_to_entropy(variabilite)

    blocks: List[Block] = []

    # 1) Warm-up (obligatoire, d'abord)
    warm = next((s for s in tpl if s["slot"] == "warmup"), None)
    if warm:
        blocks.append(build_block(warm, pool, rng, entropy, params))

    # 2) Main – déstructuré : 1 ou 2 sous-blocs, formats aléatoires, ordre aléatoire
    main = next((s for s in tpl if s["slot"] == "main"), None)
    enabled = params.get("enabled_formats", [])  # depuis l’UI
    allowed = allowed_formats_for_course(params["course_type"])

    if main:
        work_minutes = params["duration_min"] * (0.45 + 0.5 * params["volume"] / 100)
        main_secs = int(work_minutes * 60)
        n_main = pick_main_block_count(params["duration_min"], entropy)
        parts = split_minutes(main_secs, n_main, rng)

        main_blocks: List[Block] = []
        for i in range(n_main):
            chosen_type = choose_format(rng, enabled, allowed, entropy)
            slot_dyn = dict(main)  # copie
            slot_dyn["type"] = chosen_type
            slot_dyn["duration_sec"] = parts[i]
            # varier aussi le nombre d'items (2 à 4) selon le format
            slot_dyn["items"] = (
                3 if chosen_type in ("AMRAP", "EMOM") else 2 + rng.randint(0, 1)
            )
            blk = build_block(slot_dyn, pool, rng, entropy, params)
            main_blocks.append(blk)

        rng.shuffle(main_blocks)  # << ORDRE ALÉATOIRE
        blocks.extend(main_blocks)

    # 3) Finisher – optionnel selon template; format possiblement changé
    fin = next((s for s in tpl if s.get("slot") == "finisher"), None)
    if fin:
        # Si entropy haute et formats cochés incluent Tabata/EMOM, on peut varier
        fin_dyn = dict(fin)
        fin_candidates = [f for f in ("Tabata", "EMOM") if f in enabled] or [
            fin["type"]
        ]
        fin_dyn["type"] = rng.choice(fin_candidates) if entropy >= 0.25 else fin["type"]
        blocks.append(build_block(fin_dyn, pool, rng, entropy, params))

    s = Session(
        session_id=str(uuid.uuid4()),
        mode="COLLECTIF",
        label=f"{params['course_type']} {params['duration_min']}'",
        duration_sec=params["duration_min"] * 60,
        blocks=blocks,
        meta={"intensity": params.get("intensity", "Medium")},
    )
    # Pas d’ajustement fin ici (on est déjà ~au budget). On pourra peaufiner si besoin.
    return s
