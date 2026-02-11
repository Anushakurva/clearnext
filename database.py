from datetime import datetime
from typing import Dict, Any, Optional
from config import Config
from utils.mock_db import mock_db

class DatabaseManager:
    """Database manager that handles both MongoDB and mock database"""
    
    def __init__(self):
        self.use_mock = Config.USE_MOCK_DB
        self.mongo_client = None
        self.db = None
        
        if not self.use_mock:
            try:
                from pymongo import MongoClient
                self.mongo_client = MongoClient(Config.MONGO_URI)
                self.db = self.mongo_client.clearnext
                print("✅ Connected to MongoDB")
            except Exception as e:
                print(f"❌ MongoDB connection failed: {e}")
                print("🔄 Falling back to mock database")
                self.use_mock = True
        else:
            print("📝 Using mock database")
    
    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create user in database"""
        if self.use_mock:
            return mock_db.create_user(user_data)
        else:
            user_data['created_at'] = datetime.utcnow()
            user_data['updated_at'] = datetime.utcnow()
            result = self.db.users.insert_one(user_data)
            user_data['_id'] = str(result.inserted_id)
            return user_data
    
    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        if self.use_mock:
            return mock_db.get_user(user_id)
        else:
            return self.db.users.find_one({'user_id': user_id})
    
    def update_user(self, user_id: str, updates: Dict[str, Any]) -> bool:
        """Update user data"""
        if self.use_mock:
            return mock_db.update_user(user_id, updates)
        else:
            updates['updated_at'] = datetime.utcnow()
            result = self.db.users.update_one(
                {'user_id': user_id}, 
                {'$set': updates}
            )
            return result.modified_count > 0
    
    def create_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create task in database"""
        if self.use_mock:
            return mock_db.create_task(task_data)
        else:
            task_data['created_at'] = datetime.utcnow()
            result = self.db.tasks.insert_one(task_data)
            task_data['_id'] = str(result.inserted_id)
            return task_data
    
    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get task by ID"""
        if self.use_mock:
            return mock_db.get_task(task_id)
        else:
            return self.db.tasks.find_one({'task_id': task_id})
    
    def get_user_tasks(self, user_id: str) -> list:
        """Get all tasks for user"""
        if self.use_mock:
            return mock_db.get_user_tasks(user_id)
        else:
            return list(self.db.tasks.find({'user_id': user_id}))
    
    def create_reflection(self, reflection_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create reflection in database"""
        if self.use_mock:
            return mock_db.create_reflection(reflection_data)
        else:
            reflection_data['created_at'] = datetime.utcnow()
            result = self.db.reflections.insert_one(reflection_data)
            reflection_data['_id'] = str(result.inserted_id)
            return reflection_data
    
    def get_user_reflections(self, user_id: str) -> list:
        """Get all reflections for user"""
        if self.use_mock:
            return mock_db.get_user_reflections(user_id)
        else:
            return list(self.db.reflections.find({'user_id': user_id}))
    
    def create_progress(self, progress_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create progress record"""
        if self.use_mock:
            return mock_db.create_progress(progress_data)
        else:
            progress_data['created_at'] = datetime.utcnow()
            progress_data['updated_at'] = datetime.utcnow()
            result = self.db.progress.insert_one(progress_data)
            progress_data['_id'] = str(result.inserted_id)
            return progress_data
    
    def get_progress(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get progress for user"""
        if self.use_mock:
            return mock_db.get_progress(user_id)
        else:
            return self.db.progress.find_one({'user_id': user_id})
    
    def update_progress(self, user_id: str, updates: Dict[str, Any]) -> bool:
        """Update progress data"""
        if self.use_mock:
            return mock_db.update_progress(user_id, updates)
        else:
            updates['updated_at'] = datetime.utcnow()
            result = self.db.progress.update_one(
                {'user_id': user_id}, 
                {'$set': updates}
            )
            return result.modified_count > 0

# Global database instance
db = DatabaseManager()
