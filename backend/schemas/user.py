from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, UUID
from datetime import datetime

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    phone_number: Optional[str] = Field(None, max_length=20)
    security_clearance_level: int = Field(..., ge=1, le=4)

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    agency_id: Optional[UUID] = None

class UserUpdate(UserBase):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    phone_number: Optional[str] = Field(None, max_length=20)
    security_clearance_level: Optional[int] = Field(None, ge=1, le=4)
    is_active: Optional[bool] = None

class UserInDB(UserBase):
    user_id: UUID
    agency_id: Optional[UUID] = None
    role_id: Optional[UUID] = None
    mfa_enabled: bool = False
    mfa_method: Optional[str] = None
    created_at: datetime
    last_login: Optional[datetime] = None
    is_active: bool = True
    failed_login_attempts: int = 0
    locked_until: Optional[datetime] = None

    class Config:
        orm_mode = True

class UserResponse(UserInDB):
    pass

class AgencyBase(BaseModel):
    agency_name: str = Field(..., min_length=1, max_length=100)
    agency_type: Optional[str] = Field(None, max_length=50)
    jurisdiction: Optional[str] = Field(None, max_length=100)
    contact_email: Optional[EmailStr] = None
    contact_phone: Optional[str] = Field(None, max_length=20)

class AgencyCreate(AgencyBase):
    pass

class AgencyUpdate(AgencyBase):
    agency_name: Optional[str] = Field(None, min_length=1, max_length=100)
    is_active: Optional[bool] = None

class AgencyInDB(AgencyBase):
    agency_id: UUID
    created_at: datetime
    is_active: bool = True

    class Config:
        orm_mode = True

class AgencyResponse(AgencyInDB):
    pass

class RoleBase(BaseModel):
    role_name: str = Field(..., min_length=1, max_length=50)
    role_description: Optional[str] = None
    access_level: int = Field(..., ge=1, le=4)

class RoleCreate(RoleBase):
    pass

class RoleUpdate(RoleBase):
    role_name: Optional[str] = Field(None, min_length=1, max_length=50)
    access_level: Optional[int] = Field(None, ge=1, le=4)

class RoleInDB(RoleBase):
    role_id: UUID
    created_at: datetime

    class Config:
        orm_mode = True

class RoleResponse(RoleInDB):
    pass

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[UUID] = None
    username: Optional[str] = None