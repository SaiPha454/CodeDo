from fastapi import Request

class DashboardLogic:
    @staticmethod
    def is_logged_in(request: Request):
        return request.session.get("user_id") is not None
