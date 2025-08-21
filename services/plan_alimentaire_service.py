from models.plan_alimentaire import PlanAlimentaire, Repas, RepasItem
from repositories.plan_alimentaire_repo import PlanAlimentaireRepository


class PlanAlimentaireService:
    def __init__(self, repo: PlanAlimentaireRepository) -> None:
        self.repo = repo
        self._current_plan_id: int | None = None

    def get_or_create_plan_for_client(self, client_id: int) -> PlanAlimentaire:
        plan = self.repo.find_by_client_id(client_id)
        if plan:
            self._current_plan_id = plan.id
            return plan
        plan = PlanAlimentaire(
            id=0,
            client_id=client_id,
            nom="Plan alimentaire",
            repas=[
                Repas(id=0, plan_id=0, nom="Petit-déjeuner", ordre=0),
                Repas(id=0, plan_id=0, nom="Déjeuner", ordre=1),
                Repas(id=0, plan_id=0, nom="Collation", ordre=2),
                Repas(id=0, plan_id=0, nom="Dîner", ordre=3),
            ],
        )
        plan_id = self.repo.create_plan(plan)
        self._current_plan_id = plan_id
        return self.repo.get_plan(plan_id)

    def add_aliment_to_repas(
        self, repas_id: int, aliment_id: int, quantite: float
    ) -> PlanAlimentaire:
        item = RepasItem(
            id=0,
            repas_id=repas_id,
            aliment_id=aliment_id,
            portion_id=None,
            quantite=quantite,
        )
        self.repo.add_item(repas_id, item)
        return self.repo.get_plan(self._current_plan_id)

    def delete_item_from_repas(self, item_id: int) -> PlanAlimentaire:
        self.repo.delete_item(item_id)
        return self.repo.get_plan(self._current_plan_id)

    def compute_item_totals(self, item: RepasItem) -> dict[str, float]:
        return self.repo.compute_item_totals(item)

    def compute_meal_totals(self, repas: Repas) -> dict[str, float]:
        totals = {"kcal": 0.0, "proteines": 0.0, "glucides": 0.0, "lipides": 0.0}
        for item in repas.items:
            it = self.compute_item_totals(item)
            for k in totals:
                totals[k] += it[k]
        return totals

    def compute_plan_totals(self, plan: PlanAlimentaire) -> dict[str, float]:
        totals = {"kcal": 0.0, "proteines": 0.0, "glucides": 0.0, "lipides": 0.0}
        for repas in plan.repas:
            mt = self.compute_meal_totals(repas)
            for k in totals:
                totals[k] += mt[k]
        return totals
