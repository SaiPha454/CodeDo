from fastapi import HTTPException, Request
from repositories.user_model import UserRole

class RoleMiddleware:
    @staticmethod
    def verify_role(request: Request, required_role: UserRole):
        user_role = request.session.get("role")
        if user_role != required_role.value:
            raise HTTPException(status_code=403, detail="Access forbidden")