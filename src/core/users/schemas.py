from src.core.common.schemas import BaseSchema

class SUser(BaseSchema):
    id: int
    name: str | None = None
    group_name: str | None = None
    department_name: str | None = None
    is_admin: bool = False

class SGroup(BaseSchema):
    name: str
    users: list[SUser]