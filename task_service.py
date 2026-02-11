from datetime import datetime, timedelta
from typing import Dict, Any, List
from models.task import Task
from utils.validators import generate_task_id

class TaskService:
    """Service for managing tasks and task generation"""
    
    def __init__(self, db):
        self.db = db
    
    def get_or_create_today_task(self, user_id: str, user: Dict[str, Any]) -> Task:
        """Get existing task for today or create new one"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Check if task already exists for today
        user_tasks = self.db.get_user_tasks(user_id)
        today_task = None
        
        for task in user_tasks:
            task_date = datetime.fromisoformat(task['created_at']).strftime('%Y-%m-%d')
            if task_date == today:
                today_task = Task(
                    task_id=task['task_id'],
                    user_id=task['user_id'],
                    day_number=task['day_number'],
                    task_content=task['task_content'],
                    task_type=task.get('task_type', 'learning'),
                    difficulty=task.get('difficulty', 'medium'),
                    mood_adapted=task.get('mood_adapted', 'okay')
                )
                break
        
        if today_task:
            return today_task
        
        # Create new task if none exists
        current_day = user.get('current_day', 1)
        if current_day > user.get('journey_days', 7):
            return None  # Journey complete
        
        task_content = self.generate_task_content(user, current_day)
        task_id = generate_task_id(user_id, current_day)
        
        new_task = Task(
            task_id=task_id,
            user_id=user_id,
            day_number=current_day,
            task_content=task_content,
            task_type='learning',
            difficulty=self.get_difficulty_for_user(user),
            mood_adapted='okay'
        )
        
        # Save to database
        self.db.create_task(new_task.to_dict())
        
        return new_task
    
    def generate_task_content(self, user: Dict[str, Any], day_number: int) -> str:
        """Generate personalized task content based on user profile"""
        status = user.get('status', 'Student')
        confusion_area = user.get('confusion_area', 'Career')
        struggle_type = user.get('struggle_type', 'Motivation')
        
        # Task templates based on user profile
        task_templates = {
            'Student': {
                'Career': {
                    'Motivation': [
                        f"Research 3 career paths in {confusion_area} and list pros/cons of each",
                        f"Create a mind map of your skills and how they relate to {confusion_area} careers",
                        f"Interview someone working in {confusion_area} (or watch interview) and summarize insights"
                    ],
                    'Time': [
                        f"Create a 30-day study schedule for {confusion_area} learning",
                        f"Use Pomodoro technique for 2 hours studying {confusion_area}",
                        f"Identify and eliminate 3 time-wasters from your daily routine"
                    ],
                    'Concepts': [
                        f"Explain a complex {confusion_area} concept in simple terms to someone else",
                        f"Find 3 online resources about {confusion_area} and evaluate their quality",
                        f"Create flashcards for 10 key concepts in {confusion_area}"
                    ]
                },
                'Learning': {
                    'Motivation': [
                        f"Set 3 learning goals for {confusion_area} this week",
                        f"Create a vision board for your {confusion_area} journey",
                        f"Write about why {confusion_area} matters to you personally"
                    ],
                    'Time': [
                        f"Time-block your study schedule for {confusion_area} learning",
                        f"Try the 2-minute rule for {confusion_area} tasks",
                        f"Create a priority list for {confusion_area} topics"
                    ],
                    'Concepts': [
                        f"Teach someone a {confusion_area} concept you just learned",
                        f"Create analogies for difficult {confusion_area} concepts",
                        f"Draw a concept map for {confusion_area} topic"
                    ]
                }
            },
            'Professional': {
                'Career': {
                    'Motivation': [
                        f"Update your resume/CV with {confusion_area} related skills",
                        f"Set 3 career goals for the next 6 months in {confusion_area}",
                        f"Network with 2 professionals in {confusion_area} field"
                    ],
                    'Time': [
                        f"Audit your workday and identify productivity gaps",
                        f"Implement one time management technique for a week",
                        f"Create a project timeline for your current {confusion_area} project"
                    ],
                    'Concepts': [
                        f"Apply a new {confusion_area} concept to your current work",
                        f"Teach a {confusion_area} skill to a colleague",
                        f"Write a case study of a {confusion_area} challenge you solved"
                    ]
                }
            }
        }
        
        # Get appropriate task template
        user_tasks = task_templates.get(status, {}).get(confusion_area, {}).get(struggle_type, [])
        
        if not user_tasks:
            # Fallback tasks
            user_tasks = [
                f"Spend 30 minutes learning about {confusion_area}",
                f"Write down 5 questions you have about {confusion_area}",
                f"Find one interesting fact about {confusion_area} and share it"
            ]
        
        # Select task based on day
        task_index = (day_number - 1) % len(user_tasks)
        task_content = user_tasks[task_index]
        
        # Add day-specific context
        if day_number == 1:
            task_content = f"Day 1: Welcome to your journey! {task_content}"
        elif day_number % 7 == 0:
            task_content = f"Day {day_number}: Weekly check-in! {task_content}"
        else:
            task_content = f"Day {day_number}: {task_content}"
        
        return task_content
    
    def get_difficulty_for_user(self, user: Dict[str, Any]) -> str:
        """Determine task difficulty based on user profile"""
        # Simple logic - can be enhanced with mood, progress, etc.
        struggle_type = user.get('struggle_type', 'Motivation')
        
        if struggle_type == 'Concepts':
            return 'medium'  # Concepts might need medium difficulty
        elif struggle_type == 'Time':
            return 'easy'    # Time struggles need easier tasks
        else:
            return 'medium'  # Default difficulty
    
    def is_task_window_active(self) -> bool:
        """Check if current time is within task window"""
        from config import Config
        current_hour = datetime.now().hour
        return Config.TASK_WINDOW_START_HOUR <= current_hour <= Config.TASK_WINDOW_END_HOUR
    
    def get_task_status_summary(self, user_id: str) -> Dict[str, Any]:
        """Get summary of task status for user"""
        user_tasks = self.db.get_user_tasks(user_id)
        
        completed_tasks = [task for task in user_tasks if task.get('completed')]
        total_tasks = len(user_tasks)
        completion_rate = (len(completed_tasks) / total_tasks * 100) if total_tasks > 0 else 0
        
        return {
            'total_tasks': total_tasks,
            'completed_tasks': len(completed_tasks),
            'completion_rate': round(completion_rate, 2),
            'current_streak': self.calculate_current_streak(user_tasks),
            'window_active': self.is_task_window_active()
        }
    
    def calculate_current_streak(self, tasks: List[Dict[str, Any]]) -> int:
        """Calculate current streak of completed tasks"""
        if not tasks:
            return 0
        
        # Sort tasks by creation date
        sorted_tasks = sorted(tasks, key=lambda x: x.get('created_at', ''))
        
        streak = 0
        current_date = datetime.now().date()
        
        for task in reversed(sorted_tasks):
            if task.get('completed'):
                task_date = datetime.fromisoformat(task.get('created_at', '')).date()
                if (current_date - task_date).days == 1:
                    streak += 1
                    current_date = task_date
                elif (current_date - task_date).days == 0:
                    streak += 1
                else:
                    break
            else:
                break
        
        return streak
