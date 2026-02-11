from datetime import datetime
from typing import Optional, Dict, Any
from config import Config

class MockDatabase:
    """In-memory database for testing/development without MongoDB"""
    
    def __init__(self):
        self.users = {}
        self.tasks = {}
        self.reflections = {}
        self.progress = {}
        self.counters = {
            'users': 0,
            'tasks': 0,
            'reflections': 0,
            'progress': 0
        }
    
    def get_next_id(self, prefix: str) -> str:
        """Generate next ID with prefix"""
        self.counters[prefix] = self.counters.get(prefix, 0) + 1
        return f"{prefix}_{self.counters[prefix]}"
    
    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new user"""
        user_id = self.get_next_id('user')
        user_data['user_id'] = user_id
        user_data['created_at'] = datetime.utcnow()
        user_data['updated_at'] = datetime.utcnow()
        self.users[user_id] = user_data
        return user_data
    
    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        return self.users.get(user_id)
    
    def update_user(self, user_id: str, updates: Dict[str, Any]) -> bool:
        """Update user data"""
        if user_id in self.users:
            self.users[user_id].update(updates)
            self.users[user_id]['updated_at'] = datetime.utcnow()
            return True
        return False
    
    def create_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new task"""
        task_id = self.get_next_id('task')
        task_data['task_id'] = task_id
        task_data['created_at'] = datetime.utcnow()
        self.tasks[task_id] = task_data
        return task_data
    
    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get task by ID"""
        return self.tasks.get(task_id)
    
    def get_user_tasks(self, user_id: str) -> list:
        """Get all tasks for a user"""
        return [task for task in self.tasks.values() if task.get('user_id') == user_id]
    
    def create_reflection(self, reflection_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new reflection"""
        reflection_id = self.get_next_id('reflection')
        reflection_data['reflection_id'] = reflection_id
        reflection_data['created_at'] = datetime.utcnow()
        self.reflections[reflection_id] = reflection_data
        return reflection_data
    
    def get_user_reflections(self, user_id: str) -> list:
        """Get all reflections for a user"""
        return [ref for ref in self.reflections.values() if ref.get('user_id') == user_id]
    
    def create_progress(self, progress_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create progress record"""
        progress_id = self.get_next_id('progress')
        progress_data['progress_id'] = progress_id
        progress_data['created_at'] = datetime.utcnow()
        progress_data['updated_at'] = datetime.utcnow()
        self.progress[progress_id] = progress_data
        return progress_data
    
    def get_progress(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get progress for user"""
        for progress in self.progress.values():
            if progress.get('user_id') == user_id:
                return progress
        return None
    
    def update_progress(self, user_id: str, updates: Dict[str, Any]) -> bool:
        """Update progress data"""
        for progress_id, progress in self.progress.items():
            if progress.get('user_id') == user_id:
                progress.update(updates)
                progress['updated_at'] = datetime.utcnow()
                return True
        return False

# Global mock database instance
mock_db = MockDatabase()
