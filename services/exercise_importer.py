"""
Import d'exercices depuis l'API wger (source ouverte et fiable).

- N'ajoute que des exercices validés (status=2) avec une traduction FR
- Mappe muscles/équipements vers les valeurs UI existantes
- Déduit pattern, catégorie de mouvement, tags et chargeabilité
- Trace la provenance et la licence dans des colonnes dédiées

Utilise uniquement la stdlib (urllib) pour éviter toute dépendance.
"""
from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

from db.database_manager import db_manager


WGER_BASE = "https://wger.de/api/v2"


def _http_get_json(url: str) -> Dict[str, Any]:
    req = urllib.request.Request(url, headers={"User-Agent": "coach.pro/1.0"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = resp.read()
    return json.loads(data.decode("utf-8", errors="replace"))


def _paged(url: str) -> Iterable[Dict[str, Any]]:
    """Iterate paginated endpoints returning objects in 'results'."""
    next_url = url
    while next_url:
        payload = _http_get_json(next_url)
        for item in payload.get("results", []):
            yield item
        next_url = payload.get("next")
        if next_url:
            # be polite with the public API
            time.sleep(0.2)


def _build_muscle_id_to_group_fr() -> Dict[int, str]:
    # Map muscles (name_en) -> groupe FR de l'UI
    en_to_fr = {
        "Shoulders": "Épaules",
        "Biceps": "Biceps",
        "Triceps": "Triceps",
        "Abs": "Abdominaux",
        "Lats": "Dos",
        "Chest": "Poitrine",
        "Quads": "Jambes",
        "Hamstrings": "Jambes",
        "Glutes": "Fessiers",
        "Calves": "Mollets",
        "Soleus": "Mollets",
        "Trapezius": "Dos",
        "Serratus anterior": "Poitrine",
        "Obliquus externus abdominis": "Abdominaux",
        "Brachialis": "Biceps",
    }
    out: Dict[int, str] = {}
    data = _http_get_json(f"{WGER_BASE}/muscle/")
    for m in data.get("results", []):
        gid = int(m["id"])  # type: ignore[index]
        en = (m.get("name_en") or "").strip()
        fr = en_to_fr.get(en)
        if fr:
            out[gid] = fr
    return out


def _build_equipment_id_to_label_fr() -> Dict[int, str]:
    # Map équipements (wger -> libellés FR utilisés dans l'UI)
    en_to_fr = {
        "Barbell": "Barre",
        "Bench": "Banc",
        "Dumbbell": "Haltères",
        "Gym mat": "Machine",
        "Incline bench": "Banc",
        "Kettlebell": "Kettlebell",
        "Pull-up bar": "Barre",
        "Resistance band": "Élastiques",
        "SZ-Bar": "Barre",
        "Swiss Ball": "Machine",
        "none (bodyweight exercise)": "Poids du corps",
    }
    out: Dict[int, str] = {}
    data = _http_get_json(f"{WGER_BASE}/equipment/")
    for e in data.get("results", []):
        out[int(e["id"]) ] = en_to_fr.get(e.get("name", ""), e.get("name", ""))  # type: ignore[index]
    return out


_KW = {
    "push": re.compile(r"\b(press|push|bench|dip|dips|pompe|developpe)\b", re.I),
    "pull": re.compile(r"\b(row|pull(?!-?over)|chin|face pull|pulldown)\b", re.I),
    "squat": re.compile(r"\b(squat|pistol)\b", re.I),
    "hinge": re.compile(r"\b(deadlift|good\s*morning|hip\s*thrust|swing|hinge|rdl|romanian)\b", re.I),
    "lunge": re.compile(r"\b(lunge|fente|step[- ]?up|split\s*squat|bulgarian)\b", re.I),
    "carry": re.compile(r"\b(carry|farmer|suitcase|waiter)\b", re.I),
    "twist": re.compile(r"\b(twist|rotation|wood\s*chop|wood-?chop|russian\s*twist)\b", re.I),
    "gait": re.compile(r"\b(run|sprint|walk|marche)\b", re.I),
    "jump": re.compile(r"\b(jump|plyo|box\s*jump|bond)\b", re.I),
    "iso": re.compile(r"\b(curl|extension|raise|fly|pullover|calf)\b", re.I),
    "core": re.compile(r"\b(plank|gainage|hollow|dead\s*bug|bird\s*dog|pallof)\b", re.I),
}


def _derive_pattern(name: str) -> Optional[str]:
    n = name.lower()
    if _KW["jump"].search(n):
        return "Jump"
    if _KW["gait"].search(n):
        return "Gait"
    if _KW["lunge"].search(n):
        return "Lunge"
    if _KW["squat"].search(n):
        return "Squat"
    if _KW["hinge"].search(n):
        return "Hinge"
    if _KW["carry"].search(n):
        return "Carry"
    if _KW["twist"].search(n):
        return "Twist"
    if _KW["pull"].search(n):
        return "Pull"
    if _KW["push"].search(n):
        return "Push"
    return None


def _derive_category(name: str, pattern: Optional[str]) -> Optional[str]:
    n = name.lower()
    if _KW["core"].search(n) or "plank" in n:
        return "Gainage"
    if _KW["iso"].search(n):
        return "Isolation"
    if pattern in {"Push", "Pull", "Squat", "Hinge", "Carry", "Lunge", "Twist", "Gait", "Jump"}:
        return "Polyarticulaire"
    return None


def _derive_type_effort(name: str, pattern: Optional[str], category: Optional[str]) -> str:
    n = name.lower()
    if pattern in {"Gait", "Jump"}:
        return "Cardio"
    if category == "Gainage":
        return "Technique"
    if re.search(r"\b(deadlift|squat|bench|press|pull[- ]?up|row)\b", n):
        return "Force"
    return "Hypertrophie"


def _derive_tags(name: str) -> List[str]:
    n = name.lower()
    tags: List[str] = []
    if re.search(r"\b(one[- ]?arm|single[- ]?arm|one[- ]?leg|single[- ]?leg|unilat)\b", n) or _KW["lunge"].search(n):
        tags.append("Unilatéral")
    if _KW["jump"].search(n) or re.search(r"\b(snatch|clean|jerk|plyo|sprint)\b", n):
        tags.append("Explosif")
    if re.search(r"\b(hold|isometric)\b", n) or "plank" in n:
        tags.append("Isométrie")
    if re.search(r"\b(stretch|mobility|mobilit)\b", n):
        tags.append("Mobilité")
    return tags


def _is_loadable(equipment_labels: List[str]) -> bool:
    loadables = {"Haltères", "Barre", "Kettlebell", "Machine", "Poulie", "Élastiques"}
    return any(lbl in loadables for lbl in equipment_labels)


@dataclass
class ImportedExercise:
    nom: str
    groupe: str
    equipements: List[str]
    tags: List[str]
    pattern: Optional[str]
    category: Optional[str]
    type_effort: str
    coeff: float
    chargeable: bool
    source_uuid: str
    source_url: str
    license_name: Optional[str]
    license_url: Optional[str]


def _pick_fr_translation(translations: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    # language 12 = fr; fallback to en (2)
    fr = [t for t in translations if int(t.get("language", 0)) == 12 and t.get("name")]
    if fr:
        return fr[0]
    en = [t for t in translations if int(t.get("language", 0)) == 2 and t.get("name")]
    return en[0] if en else None


def _map_primary_group(muscle_ids: List[int], id_to_group: Dict[int, str], fallback_category: Optional[str]) -> Optional[str]:
    for mid in muscle_ids:
        grp = id_to_group.get(int(mid))
        if grp:
            return grp
    if fallback_category:
        cat = fallback_category.lower()
        if "back" in cat:
            return "Dos"
        if "chest" in cat:
            return "Poitrine"
        if "shoulder" in cat:
            return "Épaules"
        if "leg" in cat:
            return "Jambes"
        if "arm" in cat:
            return "Biceps"  # meilleur que "Bras" qui n'existe pas dans l'UI
        if "abs" in cat or "core" in cat:
            return "Abdominaux"
        if "calf" in cat:
            return "Mollets"
    return None


def _map_equipment(ids: List[int], id_to_label: Dict[int, str]) -> List[str]:
    labels = [id_to_label.get(int(i)) for i in ids]
    return sorted({l for l in labels if l})  # type: ignore[return-value]


ProgressCb = Callable[[int, int, int, Optional[int]], None]


def import_from_wger(
    max_items: Optional[int] = None,
    on_progress: Optional[ProgressCb] = None,
) -> Tuple[int, int]:
    """
    Importe des exercices wger (FR) et les insère s'ils n'existent pas encore.

    Returns: (importés, ignorés)
    """
    muscles_map = _build_muscle_id_to_group_fr()
    equip_map = _build_equipment_id_to_label_fr()

    base = f"{WGER_BASE}/exerciseinfo/?language=12&status=2&limit=50"
    imported = 0
    skipped = 0
    seen = 0

    if on_progress:
        try:
            on_progress(0, 0, 0, max_items)
        except Exception:
            pass

    with db_manager.get_connection() as conn:
        for item in _paged(base):
            if max_items is not None and seen >= max_items:
                break
            seen += 1

            trans = _pick_fr_translation(item.get("translations", []) or [])
            if not trans or not trans.get("name"):
                skipped += 1
                continue
            name: str = str(trans["name"]).strip()

            # données wger
            w_category = (item.get("category") or {}).get("name")  # en
            muscle_ids = [int(m.get("id")) for m in (item.get("muscles") or [])]
            equip_ids = [int(e.get("id")) for e in (item.get("equipment") or [])]
            license_obj = item.get("license") or {}

            # mappage
            group = _map_primary_group(muscle_ids, muscles_map, w_category)
            if not group:
                skipped += 1
                continue
            equipment_labels = _map_equipment(equip_ids, equip_map)
            pattern = _derive_pattern(name)
            category = _derive_category(name, pattern)
            type_effort = _derive_type_effort(name, pattern, category)
            tags = _derive_tags(name)
            chargeable = _is_loadable(equipment_labels)

            src_uuid = str(item.get("uuid") or item.get("id"))
            src_url = f"https://wger.de/exercise/{item.get('id')}"

            try:
                cur = conn.execute(
                    (
                        "INSERT OR IGNORE INTO exercices (nom, groupe_musculaire_principal, equipement, tags, "
                        "movement_pattern, movement_category, type_effort, coefficient_volume, est_chargeable, "
                        "source, source_uuid, source_url, license_name, license_url) "
                        "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
                    ),
                    (
                        name,
                        group,
                        ", ".join(equipment_labels) or None,
                        ", ".join(tags) or None,
                        pattern,
                        category,
                        type_effort,
                        1.0,
                        1 if chargeable else 0,
                        "wger",
                        src_uuid,
                        src_url,
                        (license_obj.get("full_name") or license_obj.get("short_name") or None),
                        (license_obj.get("url") or None),
                    ),
                )
                if getattr(cur, "rowcount", -1) and cur.rowcount > 0:
                    imported += 1
                else:
                    skipped += 1
            except Exception:
                skipped += 1
            # progress callback (per item)
            if on_progress:
                try:
                    on_progress(seen, imported, skipped, max_items)
                except Exception:
                    pass
        conn.commit()

    return imported, skipped


if __name__ == "__main__":
    done, skip = import_from_wger()
    print(f"Import wger terminé: {done} insérés, {skip} ignorés")
