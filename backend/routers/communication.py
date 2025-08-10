from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid
from datetime import datetime

from backend import schemas, models
from backend.database import get_db
from backend.routers.users import get_current_user

router = APIRouter(prefix="/api/v1/communication", tags=["communication"])

@router.post("/messages", response_model=schemas.SecureMessageResponse)
def send_message(
    message: schemas.SecureMessageCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Send a secure message."""
    # Check if recipient exists
    recipient = db.query(models.User).filter(models.User.user_id == message.recipient_id).first()
    if not recipient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipient not found"
        )
    
    # Check if recipient is in the same agency or user has high clearance
    if (current_user.agency_id != recipient.agency_id and 
        current_user.security_clearance_level < 3):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to message this user"
        )
    
    # In a real implementation, we would encrypt the message content
    # For now, we'll store it as plain text
    db_message = models.SecureMessage(
        message_id=uuid.uuid4(),
        sender_id=current_user.user_id,
        recipient_id=message.recipient_id,
        message_content=message.message_content,
        message_type=message.message_type,
        sent_at=datetime.utcnow()
    )
    
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    
    return db_message

@router.get("/messages", response_model=List[schemas.SecureMessageResponse])
def get_messages(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get messages for the current user."""
    messages = db.query(models.SecureMessage).filter(
        (models.SecureMessage.sender_id == current_user.user_id) |
        (models.SecureMessage.recipient_id == current_user.user_id)
    ).offset(skip).limit(limit).all()
    
    return messages

@router.get("/messages/{message_id}", response_model=schemas.SecureMessageResponse)
def get_message(
    message_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get a specific message."""
    db_message = db.query(models.SecureMessage).filter(models.SecureMessage.message_id == message_id).first()
    if not db_message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )
    
    # Check if user has permission to access this message
    if (current_user.user_id != db_message.sender_id and 
        current_user.user_id != db_message.recipient_id and
        current_user.security_clearance_level < 4):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to access this message"
        )
    
    # Mark message as read if recipient is accessing it
    if current_user.user_id == db_message.recipient_id and not db_message.read_at:
        db_message.read_at = datetime.utcnow()
        db.commit()
        db.refresh(db_message)
    
    return db_message

@router.delete("/messages/{message_id}")
def delete_message(
    message_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Delete a message."""
    db_message = db.query(models.SecureMessage).filter(models.SecureMessage.message_id == message_id).first()
    if not db_message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )
    
    # Check if user has permission to delete this message
    if (current_user.user_id != db_message.sender_id and 
        current_user.user_id != db_message.recipient_id and
        current_user.security_clearance_level < 4):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to delete this message"
        )
    
    # Mark as deleted instead of actually deleting
    db_message.is_deleted = True
    db.commit()
    
    return {"message": "Message deleted successfully"}

@router.post("/channels", response_model=schemas.CommunicationChannelResponse)
def create_channel(
    channel: schemas.CommunicationChannelCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Create a new communication channel."""
    # Check if user has permission to create channels
    if current_user.security_clearance_level < 2:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to create channels"
        )
    
    db_channel = models.CommunicationChannel(
        channel_id=uuid.uuid4(),
        channel_name=channel.channel_name,
        channel_type=channel.channel_type,
        created_by=current_user.user_id
    )
    
    db.add(db_channel)
    db.commit()
    db.refresh(db_channel)
    
    # Add creator as channel member
    db_member = models.ChannelMember(
        channel_id=db_channel.channel_id,
        user_id=current_user.user_id,
        role_in_channel="ADMIN"
    )
    
    db.add(db_member)
    db.commit()
    
    return db_channel

@router.post("/channels/{channel_id}/members", response_model=schemas.ChannelMemberResponse)
def add_channel_member(
    channel_id: uuid.UUID,
    member: schemas.ChannelMemberCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Add a member to a communication channel."""
    # Check if channel exists
    db_channel = db.query(models.CommunicationChannel).filter(
        models.CommunicationChannel.channel_id == channel_id
    ).first()
    
    if not db_channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Channel not found"
        )
    
    # Check if user has permission to add members
    db_member = db.query(models.ChannelMember).filter(
        models.ChannelMember.channel_id == channel_id,
        models.ChannelMember.user_id == current_user.user_id
    ).first()
    
    if not db_member or (db_member.role_in_channel != "ADMIN" and 
                         current_user.security_clearance_level < 3):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to add members to this channel"
        )
    
    # Check if user to be added exists
    user_to_add = db.query(models.User).filter(models.User.user_id == member.user_id).first()
    if not user_to_add:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if user is already a member
    existing_member = db.query(models.ChannelMember).filter(
        models.ChannelMember.channel_id == channel_id,
        models.ChannelMember.user_id == member.user_id
    ).first()
    
    if existing_member:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already a member of this channel"
        )
    
    # Add member to channel
    db_new_member = models.ChannelMember(
        channel_id=channel_id,
        user_id=member.user_id
    )
    
    db.add(db_new_member)
    db.commit()
    db.refresh(db_new_member)
    
    return db_new_member

@router.get("/channels", response_model=List[schemas.CommunicationChannelResponse])
def get_channels(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get channels the user is a member of."""
    # Get channel IDs where user is a member
    member_channels = db.query(models.ChannelMember.channel_id).filter(
        models.ChannelMember.user_id == current_user.user_id
    ).subquery()
    
    # Get channels
    channels = db.query(models.CommunicationChannel).filter(
        models.CommunicationChannel.channel_id.in_(member_channels)
    ).offset(skip).limit(limit).all()
    
    return channels