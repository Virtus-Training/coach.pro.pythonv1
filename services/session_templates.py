def pick_template(course_type: str, duration_min: int):
    # Tous incluent warm-up en premier bloc
    if course_type == "CAF":
        return caf(duration_min)
    if course_type == "Core & Glutes":
        return core_glutes(duration_min)
    if course_type == "Cross-Training":
        return cross_training(duration_min)
    if course_type == "Hyrox":
        return hyrox(duration_min)
    raise ValueError("Unknown course type")

def _pack(warmup_min: int, main_min: int, finisher_min: int, main_kind: str = "AMRAP"):
    tpl = [
        {"slot":"warmup", "type":"SETSxREPS", "duration_sec": warmup_min*60, "items": 3},
        {"slot":"main", "type": main_kind, "duration_sec": main_min*60, "items": 3},
    ]
    if finisher_min > 0:
        tpl.append({"slot":"finisher", "type":"TABATA", "rounds": 8, "work_sec":20, "rest_sec":10, "items":1})
    return tpl

def caf(duration_min: int):
    if duration_min == 45: return _pack(6, 36, 3, "AMRAP")
    return _pack(8, 48, 4, "AMRAP")

def core_glutes(duration_min: int):
    if duration_min == 45: return _pack(6, 35, 4, "EMOM")
    return _pack(8, 46, 6, "EMOM")

def cross_training(duration_min: int):
    if duration_min == 45: return _pack(8, 34, 3, "FORTIME")
    return _pack(8, 48, 4, "AMRAP")

def hyrox(duration_min: int):
    if duration_min == 45: return _pack(8, 35, 2, "FORTIME")
    return _pack(8, 48, 4, "FORTIME")
