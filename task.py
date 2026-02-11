from datetime import datetime
from typing import Dict, Any, Optional

class Task:
    """Task model for ClearNext"""
    
    def __init__(self, task_id: str, user_id: str, day_number: int, 
                 task_content: str, task_type: str = "learning", 
                 difficulty: str = "medium", mood_adapted: str = "okay"):
        self.task_id = task_id
        self.user_id = user_id
        self.day_number = day_number
        self.task_content = task_content
        self.task_type = task_type
        self.difficulty = difficulty
        self.mood_adapted = mood_adapted
        self.completed = False
        self.completed_at = None
        self.response = None
        self.response_at = None
        self.generated_at = datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary"""
        return {
            'task_id': self.task_id,
            'user_id': self.user_id,
            'day_number': self.day_number,
            'task_content': self.task_content,
            'task_type': self.task_type,
            'difficulty': self.difficulty,
            'mood_adapted': self.mood_adapted,
            'completed': self.completed,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'response': self.response,
            'response_at': self.response_at.isoformat() if self.response_at else None,
            'generated_at': self.generated_at.isoformat()
        }
    
    def complete(self, response: str = None):
        """Mark task as completed"""
        self.completed = True
        self.completed_at = datetime.utcnow()
        self.response = response
        self.response_at = datetime.utcnow()
    
    def is_completed(self) -> bool:
        """Check if task is completed"""
        return self.completed
    
    def update_content(self, new_content: str):
        """Update task content"""
        self.task_content = new_content
        self.generated_at = datetime.utcnow()

class Reflection:
    """Reflection model for ClearNext"""
    
    def __init__(self, reflection_id: str, user_id: str, task_id: str, 
                 day_number: int, learning: str, feeling: str, improvement: str,
                 mood_before: str = "okay", mood_after: str = "okay"):
        self.reflection_id = reflection_id
        self.user_id = user_id
        self.task_id = task_id
        self.day_number = day_number
        self.learning = learning
        self.feeling = feeling
        self.improvement = improvement
        self.mood_before = mood_before
        self.mood_after = mood_after
        self.honesty_confirmed = False
        self.word_count = len(learning.split()) + len(feeling.split()) + len(improvement.split())
        self.anti_cheat_score = 0.5
        self.micro_appreciation = ""
        self.created_at = datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert reflection to dictionary"""
        return {
            'reflection_id': self.reflection_id,
            'user_id': self.user_id,
            'task_id': self.task_id,
            'day_number': self.day_number,
            'learning': self.learning,
            'feeling': self.feeling,
            'improvement': self.improvement,
            'mood_before': self.mood_before,
            'mood_after': self.mood_after,
            'honesty_confirmed': self.honesty_confirmed,
            'word_count': self.word_count,
            'anti_cheat_score': self.anti_cheat_score,
            'micro_appreciation': self.micro_appreciation,
            'created_at': self.created_at.isoformat()
        }
    
    def confirm_honesty(self):
        """Confirm reflection honesty"""
        self.honesty_confirmed = True
    
    def calculate_quality_score(self) -> float:
        """Calculate reflection quality score"""
        from utils.validators import calculate_reflection_score
        
        total_text = f"{self.learning} {self.feeling} {self.improvement}"
        self.anti_cheat_score = calculate_reflection_score(total_text)
        return self.anti_cheat_score
    
    def generate_appreciation(self, mood: str = "okay") -> str:
        """Generate micro-appreciation message"""
        appreciations = {
            'low': [
                "Thank you for your honest reflection today.",
                "Every small step counts. Well done!",
                "Your effort today matters greatly."
            ],
            'okay': [
                "Great reflection! Keep going strong.",
                "Your insights are valuable. Thank you!",
                "Well done on your thoughtful response."
            ],
            'good': [
                "Excellent reflection! You're doing amazing!",
                "Fantastic insights! Keep this energy!",
                "Outstanding work! You're crushing it!"
            ]
        }
        
        mood_appreciations = appreciations.get(mood, appreciations['okay'])
        import random
        return random.choice(mood_appreciations)

class Progress:
    """Progress model for ClearNext"""
    
    def __init__(self, progress_id: str, user_id: str, journey_days: int = 7):
        self.progress_id = progress_id
        self.user_id = user_id
        self.current_streak = 0
        self.longest_streak = 0
        self.total_days_completed = 0
        self.journey_completion = 0.0
        self.total_characters_written = 0
        self.last_activity_date = datetime.utcnow()
        self.achievements = []
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.journey_days = journey_days
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert progress to dictionary"""
        return {
            'progress_id': self.progress_id,
            'user_id': self.user_id,
            'current_streak': self.current_streak,
            'longest_streak': self.longest_streak,
            'total_days_completed': self.total_days_completed,
            'journey_completion': self.journey_completion,
            'total_characters_written': self.total_characters_written,
            'last_activity_date': self.last_activity_date.isoformat(),
            'achievements': self.achievements,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def update_streak(self, is_consecutive_day: bool):
        """Update streak based on consecutive day completion"""
        if is_consecutive_day:
            self.current_streak += 1
            if self.current_streak > self.longest_streak:
                self.longest_streak = self.current_streak
        else:
            self.current_streak = 1
        self.updated_at = datetime.utcnow()
    
    def complete_day(self, characters_written: int = 0):
        """Mark a day as completed"""
        self.total_days_completed += 1
        self.total_characters_written += characters_written
        self.journey_completion = (self.total_days_completed / self.journey_days) * 100
        self.last_activity_date = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        
        # Check achievements
        self.check_achievements()
    
    def check_achievements(self):
        """Check and award achievements"""
        if self.current_streak >= 7 and 'first_week' not in self.achievements:
            self.achievements.append('first_week')
        
        if self.current_streak >= 30 and 'monthly_champion' not in self.achievements:
            self.achievements.append('monthly_champion')
        
        if self.journey_completion >= 100.0 and 'journey_complete' not in self.achievements:
            self.achievements.append('journey_complete')
