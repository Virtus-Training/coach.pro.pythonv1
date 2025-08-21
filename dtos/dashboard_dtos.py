from dataclasses import dataclass


@dataclass
class DashboardDataDTO:
    active_clients: int
    sessions_this_month: int
    average_session_completion_rate: float
