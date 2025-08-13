from dataclasses import dataclass, field
from typing import List, Optional, Dict, Union

Number = Union[int, float]

@dataclass
class BlockItem:
    exercise_id: str
    prescription: Dict[str, Number | str]  # reps|time|distance|calories|load
    notes: Optional[str] = None

@dataclass
class Block:
    block_id: str
    type: str                 # EMOM/AMRAP/FORTIME/TABATA/SETSxREPS
    duration_sec: int = 0
    rounds: int = 0
    work_sec: int = 0
    rest_sec: int = 0
    items: List[BlockItem] = field(default_factory=list)
    title: Optional[str] = None
    locked: bool = False

@dataclass
class Session:
    session_id: str
    mode: str                 # COLLECTIF / INDIVIDUEL
    label: str
    duration_sec: int
    blocks: List[Block] = field(default_factory=list)
    meta: Dict[str, Number | str] = field(default_factory=dict)
