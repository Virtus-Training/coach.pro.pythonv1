from services.exercise_importer import _paged, _pick_fr_translation, _build_muscle_id_to_group_fr, _map_primary_group
from services.exercise_importer import WGER_BASE

mm = _build_muscle_id_to_group_fr()
base = f"{WGER_BASE}/exerciseinfo/?language=12&status=2&limit=20"
count=0
for item in _paged(base):
    trans = _pick_fr_translation(item.get("translations", []) or [])
    if not trans or not trans.get("name"):
        print('SKIP(no-name) id', item.get('id'))
        continue
    name = trans['name']
    w_category = (item.get('category') or {}).get('name')
    muscle_ids = [int(m.get('id')) for m in (item.get('muscles') or [])]
    group = _map_primary_group(muscle_ids, mm, w_category)
    print('NAME:', name, '| cat:', w_category, '| muscles:', muscle_ids, '| group->', group)
    count += 1
    if count>=10:
        break

