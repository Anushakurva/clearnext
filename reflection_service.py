from datetime import datetime
from typing import Dict, Any, List
from models.task import Reflection, Progress
from utils.validators import generate_reflection_id

class ReflectionService:
    """Service for managing reflections and progress tracking"""
    
    def __init__(self, db):
        self.db = db
    
    def create_reflection(self, reflection_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new reflection"""
        return self.db.create_reflection(reflection_data)
    
    def get_user_reflections(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all reflections for a user"""
        return self.db.get_user_reflections(user_id)
    
    def update_user_progress(self, user_id: str, characters_written: int) -> bool:
        """Update user progress after reflection"""
        # Get existing progress
        progress = self.db.get_progress(user_id)
        
        if not progress:
            # Create new progress record
            new_progress = Progress(
                progress_id=f"prog_{user_id}",
                user_id=user_id
            )
            new_progress.complete_day(characters_written)
            self.db.create_progress(new_progress.to_dict())
            return True
        
        # Update existing progress
        progress_data = {
            'total_days_completed': progress.get('total_days_completed', 0) + 1,
            'total_characters_written': progress.get('total_characters_written', 0) + characters_written,
            'last_activity_date': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat()
        }
        
        # Calculate journey completion
        user = self.db.get_user(user_id)
        if user:
            journey_days = user.get('journey_days', 7)
            progress_data['journey_completion'] = (progress_data['total_days_completed'] / journey_days) * 100
        
        # Update streak
        progress_data['current_streak'] = self.calculate_streak(user_id)
        if progress_data['current_streak'] > progress.get('longest_streak', 0):
            progress_data['longest_streak'] = progress_data['current_streak']
        
        # Check achievements
        achievements = progress.get('achievements', [])
        new_achievements = self.check_achievements(progress_data, user)
        progress_data['achievements'] = new_achievements
        
        return self.db.update_progress(user_id, progress_data)
    
    def calculate_streak(self, user_id: str) -> int:
        """Calculate current streak for user"""
        reflections = self.get_user_reflections(user_id)
        if not reflections:
            return 0
        
        # Sort by date
        sorted_reflections = sorted(reflections, key=lambda x: x.get('created_at', ''))
        
        streak = 0
        current_date = datetime.now().date()
        
        for reflection in reversed(sorted_reflections):
            ref_date = datetime.fromisoformat(reflection.get('created_at', '')).date()
            days_diff = (current_date - ref_date).days
            
            if days_diff <= 1:  # Today or yesterday
                streak += 1
                current_date = ref_date
            else:
                break
        
        return streak
    
    def check_achievements(self, progress_data: Dict[str, Any], user: Dict[str, Any]) -> List[str]:
        """Check and award achievements"""
        achievements = progress_data.get('achievements', [])
        
        # First week achievement
        if progress_data.get('current_streak', 0) >= 7 and 'first_week' not in achievements:
            achievements.append('first_week')
        
        # Monthly champion achievement
        if progress_data.get('current_streak', 0) >= 30 and 'monthly_champion' not in achievements:
            achievements.append('monthly_champion')
        
        # Journey completion achievement
        if progress_data.get('journey_completion', 0) >= 100.0 and 'journey_complete' not in achievements:
            achievements.append('journey_complete')
        
        # Consistent learner achievement
        if progress_data.get('total_days_completed', 0) >= 14 and 'consistent_learner' not in achievements:
            achievements.append('consistent_learner')
        
        return achievements
    
    def get_reflection_analytics(self, user_id: str) -> Dict[str, Any]:
        """Get analytics for user reflections"""
        reflections = self.get_user_reflections(user_id)
        
        if not reflections:
            return {
                'total_reflections': 0,
                'average_quality_score': 0,
                'total_words': 0,
                'mood_trend': {}
            }
        
        total_reflections = len(reflections)
        total_words = sum(ref.get('word_count', 0) for ref in reflections)
        quality_scores = [ref.get('anti_cheat_score', 0.5) for ref in reflections]
        average_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0.5
        
        # Mood analysis
        mood_counts = {'low': 0, 'okay': 0, 'good': 0}
        for ref in reflections:
            mood = ref.get('mood_after', 'okay')
            if mood in mood_counts:
                mood_counts[mood] += 1
        
        return {
            'total_reflections': total_reflections,
            'average_quality_score': round(average_quality, 2),
            'total_words': total_words,
            'average_words_per_reflection': round(total_words / total_reflections, 1) if total_reflections > 0 else 0,
            'mood_distribution': mood_counts,
            'quality_trend': self.get_quality_trend(reflections)
        }
    
    def get_quality_trend(self, reflections: List[Dict[str, Any]]) -> str:
        """Analyze quality trend over time"""
        if len(reflections) < 3:
            return 'insufficient_data'
        
        # Get last 3 reflections
        recent_reflections = reflections[-3:]
        recent_scores = [ref.get('anti_cheat_score', 0.5) for ref in recent_reflections]
        
        if all(score >= 0.8 for score in recent_scores):
            return 'improving'
        elif all(score >= 0.6 for score in recent_scores):
            return 'stable'
        elif recent_scores[-1] > recent_scores[0]:
            return 'improving'
        else:
            return 'declining'
    
    def generate_reflection_insights(self, user_id: str) -> Dict[str, Any]:
        """Generate insights from user reflections"""
        reflections = self.get_user_reflections(user_id)
        
        if len(reflections) < 5:
            return {
                'insights': ['Keep reflecting to build patterns'],
                'recommendations': ['Try to be more detailed in your reflections']
            }
        
        # Analyze common themes
        all_learning = ' '.join([ref.get('learning', '') for ref in reflections])
        all_feelings = ' '.join([ref.get('feeling', '') for ref in reflections])
        
        # Simple keyword analysis
        learning_words = all_learning.lower().split()
        feeling_words = all_feelings.lower().split()
        
        common_learning_words = self.get_most_common_words(learning_words, 5)
        common_feeling_words = self.get_most_common_words(feeling_words, 5)
        
        return {
            'insights': [
                f"You've completed {len(reflections)} reflections",
                f"Your average reflection quality is {self.get_average_quality(reflections):.2f}",
                f"Current streak: {self.calculate_streak(user_id)} days"
            ],
            'common_themes': {
                'learning_topics': common_learning_words,
                'feeling_patterns': common_feeling_words
            },
            'recommendations': self.get_recommendations(reflections)
        }
    
    def get_most_common_words(self, words: List[str], limit: int) -> List[str]:
        """Get most common words from a list"""
        word_count = {}
        for word in words:
            if len(word) > 3:  # Ignore short words
                word_count[word] = word_count.get(word, 0) + 1
        
        # Sort by frequency and return top words
        sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
        return [word for word, count in sorted_words[:limit]]
    
    def get_average_quality(self, reflections: List[Dict[str, Any]]) -> float:
        """Calculate average quality score"""
        if not reflections:
            return 0.0
        
        scores = [ref.get('anti_cheat_score', 0.5) for ref in reflections]
        return sum(scores) / len(scores)
    
    def get_recommendations(self, reflections: List[Dict[str, Any]]) -> List[str]:
        """Generate personalized recommendations based on reflections"""
        recommendations = []
        
        avg_quality = self.get_average_quality(reflections)
        avg_words = sum(ref.get('word_count', 0) for ref in reflections) / len(reflections) if reflections else 0
        
        if avg_quality < 0.6:
            recommendations.append("Try to be more specific and detailed in your reflections")
        
        if avg_words < 30:
            recommendations.append("Consider writing more to express your thoughts fully")
        
        if len(reflections) >= 10:
            recommendations.append("Great consistency! Keep up the reflection habit")
        
        return recommendations
