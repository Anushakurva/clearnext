import os
from datetime import datetime, timedelta

class Config:
    """Configuration settings for ClearNext backend"""
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'clearnext-secret-key-change-in-production')
    
    # Database Configuration
    MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/clearnext')
    USE_MOCK_DB = os.environ.get('USE_MOCK_DB', 'False').lower() == 'true'
    
    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET', 'clearnext-jwt-secret')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    
    # Journey Configuration
    DEFAULT_JOURNEY_DAYS = 7
    ALLOWED_JOURNEY_DAYS = [7, 14, 21]
    
    # Task Configuration
    TASK_WINDOW_START_HOUR = 0  # 12:00 AM
    TASK_WINDOW_END_HOUR = 23   # 11:59 PM
    
    # Reflection Configuration
    MIN_REFLECTION_LENGTH = 50
    MIN_SECTION_LENGTH = 10
    
    # CORS Configuration
    CORS_ORIGINS = ["http://localhost:8000", "http://127.0.0.1:8000"]
