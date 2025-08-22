from dataclasses import dataclass


@dataclass
class TrackedExerciseDTO:
    id: int
    name: str


@dataclass
class ExerciseProgressionDTO:
    dates: list[str]
    poids: list[float]
    repetitions: list[int]
    rpe: list[int]
