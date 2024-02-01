from typing import Optional, List

from pydantic import BaseModel


class Role(BaseModel):
    id: str
    name: str
    user_id: str
    entity_id: str
    entity_type: str
    creation_timestamp: str
    second_entity_id: Optional[str] = None


class User(BaseModel):
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
