from repositories.client_repo import ClientRepository
from repositories.sessions_repo import SessionsRepository


class DashboardService:
    def __init__(
        self, client_repo: ClientRepository, sessions_repo: SessionsRepository
    ) -> None:
        self.client_repo = client_repo
        self.sessions_repo = sessions_repo

    def get_active_clients_count(self) -> int:
        return self.client_repo.count_all()

    def get_sessions_this_month_count(self) -> int:
        return self.sessions_repo.count_sessions_this_month()

    def get_average_session_completion_rate(self) -> float:
        return 0.78
