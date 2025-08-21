from dtos.dashboard_dtos import DashboardDataDTO
from services.dashboard_service import DashboardService


class DashboardController:
    def __init__(self, service: DashboardService) -> None:
        self.service = service

    def get_dashboard_data(self) -> DashboardDataDTO:
        return DashboardDataDTO(
            active_clients=self.service.get_active_clients_count(),
            sessions_this_month=self.service.get_sessions_this_month_count(),
            average_session_completion_rate=self.service.get_average_session_completion_rate(),
        )
