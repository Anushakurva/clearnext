from datetime import datetime
from typing import Dict, Any, Optional

class User:
    """User model for ClearNext"""
    
    def __init__(self, user_id: str, name: str, status: str, confusion_area: str, 
                 struggle_type: str, journey_days: int = 7, user_type: str = "guest",
                 email: Optional[str] = None, preferred_time: str = "09:00"):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.status = status
        self.confusion_area = confusion_area
        self.struggle_type = struggle_type
        self.journey_days = journey_days
        self.current_day = 1
        self.user_type = user_type
        self.preferred_time = preferred_time
        self.ai_conversation_completed = False
        self.journey_completed = False
        self.last_active_date = datetime.utcnow()
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert user to dictionary"""
        return {
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'status': self.status,
            'confusion_area': self.confusion_area,
            'struggle_type': self.struggle_type,
            'journey_days': self.journey_days,
            'current_day': self.current_day,
            'user_type': self.user_type,
            'preferred_time': self.preferred_time,
            'ai_conversation_completed': self.ai_conversation_completed,
            'journey_completed': self.journey_completed,
            'last_active_date': self.last_active_date.isoformat(),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def update(self, **kwargs):
        """Update user attributes"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.utcnow()
    
    def advance_day(self):
        """Advance to next day in journey"""
        if self.current_day < self.journey_days:
            self.current_day += 1
            self.last_active_date = datetime.utcnow()
            self.updated_at = datetime.utcnow()
            return True
        return False
    
    def complete_journey(self):
        """Mark journey as completed"""
        self.journey_completed = True
        self.updated_at = datetime.utcnow()
    
    def is_journey_complete(self) -> bool:
        """Check if journey is complete"""
        return self.journey_completed or self.current_day > self.journey_days
