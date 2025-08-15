import time, random, uuid
from typing import Dict, Any, List
from models.session import Session, Block, BlockItem
from models.exercices import Exercise
from repositories.exercices_repo import ExerciseRepository
import services.session_templates as T

def rest_from_density(density_1_10: int) -> int:
    # 1 = repos long, 10 = repos très court
    return max(15, int(150 - (density_1_10 - 1) * 15))  # 150s → 15s

def reps_from_intensity(intensity_1_10: int, base: int) -> int:
    # Echelle grossière : intensité ↑ = reps ↑ pour AMRAP/EMOM; reps ↓ pour force
    return max(3, int(base * (0.8 + (intensity_1_10/10)*0.6)))  # 0.8x .. 1.4x

def map_slider_to_entropy(v: int) -> float:
    # 0..100 -> 0.0..1.0 (courbe douce)
    return max(0.0, min(1.0, (v / 100.0) ** 0.75))

def filter_pool(repo: ExerciseRepository, params: Dict[str, Any]) -> List[Exercise]:
    tags = []
    if params["course_type"] == "Hyrox": tags.append("hyrox")
    if params["course_type"] == "Cross-Training": tags.append("cross")
    return repo.filter(equipment=params["equipment"], tags=tags or None)

def weighted_choice(rng: random.Random, items: List[Exercise], entropy: float) -> Exercise:
    if not items: raise ValueError("Pool is empty")
    if entropy <= 0.05:  # quasi déterministe = tri par (polyarticulaire/tag match?) — simplifié ici
        return items[0]
    return rng.choice(items)
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
    return [max(4*60, a), max(4*60, b)]  # chaque bloc >= 4'
    
def allowed_formats_for_course(course_type: str) -> list[str]:
    by_course = {
        "CAF": ["AMRAP", "EMOM", "Tabata"],
        "Core & Glutes": ["EMOM", "AMRAP", "Tabata"],
        "Cross-Training": ["AMRAP", "EMOM", "For Time", "Tabata"],
        "Hyrox": ["For Time", "AMRAP", "EMOM"],  # Tabata en finisher court, généralement
    }
    return by_course.get(course_type, ["AMRAP","EMOM","For Time","Tabata"])

def choose_format(rng: random.Random, enabled: list[str], allowed: list[str], entropy: float) -> str:
    pool = [f for f in enabled if f in allowed] or allowed
    if entropy < 0.15:
        return pool[0]  # plus déterministe
    return rng.choice(pool)

def build_block(slot: Dict[str, Any], pool: List[Exercise], rng: random.Random, entropy: float, params=None) -> Block:
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
        candidates2 = [ex for ex in candidates if ex.movement_pattern != last_pattern] or candidates
        ex = weighted_choice(rng, candidates2, entropy)

        if block.type in ("SETSxREPS", "AMRAP"):
            base_reps = 12 if getattr(ex, "category", "") != "Plyo/Power" else 8
            presc = {"reps": reps_from_intensity(intensity, base_reps), "rest_sec": default_rest}
        elif block.type == "FORTIME":
            presc = {"reps": reps_from_intensity(intensity, 15), "rest_sec": max(30, default_rest)}
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
    tpl = T.pick_template(params["course_type"], params["duration_min"])
    repo = ExerciseRepository()
    pool = filter_pool(repo, params)
    rng = random.Random(params.get("seed") or int(time.time()))
    entropy = map_slider_to_entropy(params.get("variability", 50))

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
        main_secs = main["duration_sec"]
        n_main = pick_main_block_count(params["duration_min"], entropy)
        parts = split_minutes(main_secs, n_main, rng)

        main_blocks: List[Block] = []
        for i in range(n_main):
            chosen_type = choose_format(rng, enabled, allowed, entropy)
            slot_dyn = dict(main)  # copie
            slot_dyn["type"] = chosen_type
            slot_dyn["duration_sec"] = parts[i]
            # varier aussi le nombre d'items (2 à 4) selon le format
            slot_dyn["items"] = 3 if chosen_type in ("AMRAP","EMOM") else 2 + rng.randint(0,1)
            blk = build_block(slot_dyn, pool, rng, entropy, params)
            main_blocks.append(blk)

        rng.shuffle(main_blocks)           # << ORDRE ALÉATOIRE
        blocks.extend(main_blocks)

    # 3) Finisher – optionnel selon template; format possiblement changé
    fin = next((s for s in tpl if s.get("slot") == "finisher"), None)
    if fin:
        # Si entropy haute et formats cochés incluent Tabata/EMOM, on peut varier
        fin_dyn = dict(fin)
        fin_candidates = [f for f in ("Tabata","EMOM") if f in enabled] or [fin["type"]]
        fin_dyn["type"] = rng.choice(fin_candidates) if entropy >= 0.25 else fin["type"]
        blocks.append(build_block(fin_dyn, pool, rng, entropy, params))

    s = Session(
        session_id=str(uuid.uuid4()),
        mode="COLLECTIF",
        label=f'{params["course_type"]} {params["duration_min"]}\'',
        duration_sec=params["duration_min"] * 60,
        blocks=blocks,
        meta={"intensity": params.get("intensity", "Medium")}
    )
    # Pas d’ajustement fin ici (on est déjà ~au budget). On pourra peaufiner si besoin.
    return s

