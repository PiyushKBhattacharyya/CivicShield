from sqlalchemy import Column, String, Boolean, Integer, DateTime, ForeignKey, UUID, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.sql import func
import uuid
from backend.database import Base
from passlib.context import CryptContext

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"
    
    user_id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    agency_id = Column(PG_UUID(as_uuid=True), ForeignKey("agencies.agency_id"))
    role_id = Column(PG_UUID(as_uuid=True), ForeignKey("roles.role_id"))
    security_clearance_level = Column(Integer, nullable=False)
    phone_number = Column(String(20))
    mfa_enabled = Column(Boolean, default=False)
    mfa_method = Column(String(20))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True))
    is_active = Column(Boolean, default=True)
    failed_login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime(timezone=True))
    
    # Password field (not stored directly)
    _password_hash = Column("password_hash", String(255), nullable=False)
    
    @property
    def password(self):
        return self._password_hash
    
    @password.setter
    def password(self, plain_password):
        self._password_hash = pwd_context.hash(plain_password)
    
    def verify_password(self, plain_password):
        return pwd_context.verify(plain_password, self._password_hash)

class Agency(Base):
    __tablename__ = "agencies"
    
    agency_id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agency_name = Column(String(100), nullable=False)
    agency_type = Column(String(50))
    jurisdiction = Column(String(100))
    contact_email = Column(String(100))
    contact_phone = Column(String(20))
    address = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)

class Role(Base):
    __tablename__ = "roles"
    
    role_id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    role_name = Column(String(50), nullable=False)
    role_description = Column(Text)
    access_level = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class UserRole(Base):
    __tablename__ = "user_roles"
    
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.user_id"), primary_key=True)
    role_id = Column(PG_UUID(as_uuid=True), ForeignKey("roles.role_id"), primary_key=True)
    assigned_at = Column(DateTime(timezone=True), server_default=func.now())
    assigned_by = Column(PG_UUID(as_uuid=True), ForeignKey("users.user_id"))