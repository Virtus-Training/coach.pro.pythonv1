from models.plan_alimentaire import PlanAlimentaire, Repas
from repositories.plan_alimentaire_repo import PlanAlimentaireRepository


class PlanAlimentaireService:
    def __init__(self, repo: PlanAlimentaireRepository) -> None:
        self.repo = repo

    def get_or_create_plan_for_client(self, client_id: int) -> PlanAlimentaire:
        plan = self.repo.find_by_client_id(client_id)
        if plan:
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
        return self.repo.get_plan(plan_id)
