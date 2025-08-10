from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID

class SecureMessageBase(BaseModel):
    sender_id: Optional[UUID] = None
    recipient_id: Optional[UUID] = None
    message_content: Optional[str] = None
    message_type: Optional[str] = Field(None, max_length=20)

class SecureMessageCreate(SecureMessageBase):
    recipient_id: UUID
    message_content: str
    message_type: str = "TEXT"

class SecureMessageUpdate(SecureMessageBase):
    is_deleted: Optional[bool] = None

class SecureMessageInDB(SecureMessageBase):
    message_id: UUID
    message_hash: Optional[str] = Field(None, max_length=64)
    sent_at: datetime
    delivered_at: Optional[datetime] = None
    read_at: Optional[datetime] = None
    is_deleted: bool = False
    encryption_key_id: Optional[UUID] = None
    message_type: str = "TEXT"

    class Config:
        orm_mode = True

class SecureMessageResponse(SecureMessageInDB):
    pass

class CommunicationChannelBase(BaseModel):
    channel_name: str = Field(..., min_length=1, max_length=100)
    channel_type: Optional[str] = Field(None, max_length=20)

class CommunicationChannelCreate(CommunicationChannelBase):
    pass

class CommunicationChannelUpdate(CommunicationChannelBase):
    channel_name: Optional[str] = Field(None, min_length=1, max_length=100)
    channel_type: Optional[str] = Field(None, max_length=20)
    is_active: Optional[bool] = None

class CommunicationChannelInDB(CommunicationChannelBase):
    channel_id: UUID
    created_by: Optional[UUID] = None
    created_at: datetime
    is_active: bool = True

    class Config:
        orm_mode = True

class CommunicationChannelResponse(CommunicationChannelInDB):
    pass

class ChannelMemberBase(BaseModel):
    channel_id: UUID
    user_id: UUID

class ChannelMemberCreate(ChannelMemberBase):
    pass

class ChannelMemberUpdate(BaseModel):
    role_in_channel: Optional[str] = Field(None, max_length=20)

class ChannelMemberInDB(ChannelMemberBase):
    joined_at: datetime
    role_in_channel: str = "MEMBER"

    class Config:
        orm_mode = True

class ChannelMemberResponse(ChannelMemberInDB):
    pass