from typing import Optional, List

from icometrix_sdk.models.base import BackendEntity


class Role(BackendEntity):
    id: str
    name: str
    user_id: str
    entity_id: str
    entity_type: str
    second_entity_id: Optional[str] = None


class User(BackendEntity):
    id: str
    firstname: str
    lastname: str
    email: str
    hospital: str
    country: str
    language: str
    region: str
    roles: List[Role]
    blocked: bool
    verified: bool
    type: str
    note: str
    refresh_token: str
    exp: int
    token_expire_time: str
    password_setup_required: bool
    otp_active: bool
