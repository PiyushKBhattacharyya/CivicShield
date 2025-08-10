from sqlalchemy import Column, String, Text, DateTime, ForeignKey, UUID, Boolean
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.sql import func
import uuid
from backend.database import Base

class SecureMessage(Base):
    __tablename__ = "secure_messages"
    
    message_id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sender_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.user_id"))
    recipient_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.user_id"))
    message_content = Column(Text)  # Encrypted content
    message_hash = Column(String(64))  # For integrity verification
    sent_at = Column(DateTime(timezone=True), server_default=func.now())
    delivered_at = Column(DateTime(timezone=True))
    read_at = Column(DateTime(timezone=True))
    is_deleted = Column(Boolean, default=False)
    encryption_key_id = Column(UUID)  # Reference to key used for encryption
    message_type = Column(String(20), default="TEXT")  # TEXT, FILE, IMAGE, AUDIO, VIDEO

class CommunicationChannel(Base):
    __tablename__ = "communication_channels"
    
    channel_id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    channel_name = Column(String(100), nullable=False)
    channel_type = Column(String(20))  # GROUP, DIRECT, BROADCAST
    created_by = Column(PG_UUID(as_uuid=True), ForeignKey("users.user_id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)

class ChannelMember(Base):
    __tablename__ = "channel_members"
    
    channel_id = Column(PG_UUID(as_uuid=True), ForeignKey("communication_channels.channel_id"), primary_key=True)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.user_id"), primary_key=True)
    joined_at = Column(DateTime(timezone=True), server_default=func.now())
    role_in_channel = Column(String(20), default="MEMBER")  # MEMBER, ADMIN, MODERATOR