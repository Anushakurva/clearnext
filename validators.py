from datetime import datetime
from typing import Dict, Any, List

def validate_user_data(data: Dict[str, Any]) -> tuple[bool, str]:
    """Validate user registration data"""
    required_fields = ['name', 'status', 'confusion_area', 'struggle_type']
    
    for field in required_fields:
        if not data.get(field) or len(str(data.get(field)).strip()) == 0:
            return False, f"{field} is required"
    
    if len(data.get('name', '')) < 2:
        return False, "Name must be at least 2 characters"
    
    if data.get('status') not in ['Student', 'Professional', 'Other']:
        return False, "Invalid status"
    
    return True, ""

def validate_reflection_data(data: Dict[str, Any]) -> tuple[bool, str, Dict[str, Any]]:
    """Validate reflection submission data"""
    required_fields = ['user_id', 'task_id', 'learning', 'feeling', 'improvement']
    
    for field in required_fields:
        if not data.get(field) or len(str(data.get(field)).strip()) == 0:
            return False, f"{field} is required", {}
    
    # Check minimum length
    total_text = f"{data.get('learning', '')} {data.get('feeling', '')} {data.get('improvement', '')}"
    if len(total_text.strip()) < 50:
        return False, "Total reflection must be at least 50 characters", {
            'current_length': len(total_text.strip()),
            'required_length': 50
        }
    
    # Check individual sections
    min_section_length = 10
    for section in ['learning', 'feeling', 'improvement']:
        if len(str(data.get(section, '')).strip()) < min_section_length:
            return False, f"Each section must be at least {min_section_length} characters", {
                'section': section,
                'current_length': len(str(data.get(section, '')).strip()),
                'required_length': min_section_length
            }
    
    return True, "", {}

def validate_journey_duration(days: int) -> tuple[bool, str]:
    """Validate journey duration"""
    if days not in [7, 14, 21]:
        return False, "Journey duration must be 7, 14, or 21 days"
    return True, ""

def validate_task_window() -> tuple[bool, str]:
    """Check if current time is within task window"""
    from config import Config
    current_hour = datetime.now().hour
    
    if current_hour < Config.TASK_WINDOW_START_HOUR or current_hour > Config.TASK_WINDOW_END_HOUR:
        return False, f"Tasks are only available from {Config.TASK_WINDOW_START_HOUR}:00 to {Config.TASK_WINDOW_END_HOUR}:59"
    
    return True, ""

def generate_user_id(user_type: str = "GUEST") -> str:
    """Generate unique user ID"""
    import uuid
    timestamp = int(datetime.now().timestamp())
    unique_id = str(uuid.uuid4())[:8]
    return f"{user_type}_{timestamp}_{unique_id}"

def generate_task_id(user_id: str, day_number: int) -> str:
    """Generate task ID"""
    return f"task_{user_id.split('_')[1]}_{day_number}"

def generate_reflection_id(user_id: str, day_number: int) -> str:
    """Generate reflection ID"""
    return f"ref_{user_id.split('_')[1]}_{day_number}"

def calculate_reflection_score(text: str) -> float:
    """Calculate reflection quality score (0.0 - 1.0)"""
    score = 0.5  # Base score
    
    # Length bonus
    if len(text) >= 100:
        score += 0.2
    elif len(text) >= 200:
        score += 0.3
    
    # Word variety bonus
    words = text.lower().split()
    unique_words = set(words)
    if len(words) > 0:
        variety_ratio = len(unique_words) / len(words)
        if variety_ratio > 0.7:
            score += 0.2
    
    return min(1.0, max(0.0, score))

def format_response(success: bool, message: str, data: Any = None) -> Dict[str, Any]:
    """Format standard API response"""
    response = {
        'success': success,
        'message': message,
        'timestamp': datetime.utcnow().isoformat()
    }
    
    if data is not None:
        response['data'] = data
    
    return response
