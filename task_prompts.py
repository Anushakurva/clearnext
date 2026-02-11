from typing import Dict, Any, List

class TaskPrompts:
    """AI prompt templates for task generation (can be mocked)"""
    
    @staticmethod
    def get_ai_conversation_prompts() -> List[str]:
        """Get prompts for AI conversation"""
        return [
            "Hello! I'm ClearNext AI. To personalize your learning journey, I need to understand you better. What's your name?",
            "Thank you! What's your current status - are you a student, professional, or something else?",
            "I understand. What's your primary confusion or challenge right now with learning?",
            "That helps clarify things. What type of struggle are you experiencing - is it with motivation, time management, understanding concepts, or something else?",
            "Perfect! I now have a good understanding of your situation. Let me save this information and create a personalized learning plan for you."
        ]
    
    @staticmethod
    def get_task_generation_prompt(user_profile: Dict[str, Any], day_number: int) -> str:
        """Generate task prompt based on user profile"""
        status = user_profile.get('status', 'Student')
        confusion_area = user_profile.get('confusion_area', 'Career')
        struggle_type = user_profile.get('struggle_type', 'Motivation')
        
        prompt = f"""
        Generate a personalized learning task for Day {day_number} based on this user profile:
        
        User Profile:
        - Status: {status}
        - Confusion Area: {confusion_area}
        - Struggle Type: {struggle_type}
        - Current Day: {day_number}
        
        Task Requirements:
        1. Should be specific and actionable
        2. Should address their confusion area
        3. Should consider their struggle type
        4. Should be achievable in one day
        5. Should promote learning and growth
        
        Task Examples:
        - For Career + Motivation: "Research 3 career paths and list pros/cons"
        - For Time + Concepts: "Create a study schedule for concept mastery"
        - For Learning + Time: "Use Pomodoro technique for focused learning"
        
        Please generate one specific task that matches these criteria.
        """
        
        return prompt.strip()
    
    @staticmethod
    def get_reflection_guidance_prompt(reflection_data: Dict[str, Any]) -> str:
        """Generate AI guidance for reflection improvement"""
        learning = reflection_data.get('learning', '')
        feeling = reflection_data.get('feeling', '')
        improvement = reflection_data.get('improvement', '')
        
        prompt = f"""
        Analyze this student reflection and provide guidance for improvement:
        
        Learning: {learning}
        Feeling: {feeling}
        Improvement: {improvement}
        
        Provide guidance on:
        1. Reflection depth and quality
        2. Areas for improvement
        3. Positive reinforcement
        4. Next learning suggestions
        
        Keep it encouraging and constructive.
        """
        
        return prompt.strip()
    
    @staticmethod
    def get_motivational_message(user_data: Dict[str, Any]) -> str:
        """Generate motivational message based on user progress"""
        current_day = user_data.get('current_day', 1)
        total_days = user_data.get('journey_days', 7)
        streak = user_data.get('current_streak', 0)
        
        if streak >= 7:
            return f"Amazing {streak}-day streak! You're building incredible consistency!"
        elif current_day >= total_days:
            return "🎉 Congratulations! You've completed your learning journey!"
        elif streak >= 3:
            return f"Great {streak}-day streak! Keep the momentum going!"
        else:
            return f"Day {current_day} of {total_days} - Every step forward is progress!"
    
    @staticmethod
    def get_streak_encouragement(streak_length: int) -> str:
        """Get encouraging message based on streak length"""
        if streak_length >= 30:
            return "Incredible! A month-long streak shows true dedication!"
        elif streak_length >= 21:
            return "Three weeks of consistency! You're forming lifelong habits!"
        elif streak_length >= 14:
            return "Two weeks strong! You're building real momentum!"
        elif streak_length >= 7:
            return "One week complete! You've proven your commitment!"
        elif streak_length >= 3:
            return "Three days in a row! Great start to your streak!"
        else:
            return "Every day counts. Keep showing up!"

class MockAI:
    """Mock AI service for testing without real AI integration"""
    
    @staticmethod
    def generate_response(prompt: str) -> str:
        """Generate mock AI response"""
        if "name" in prompt.lower():
            return "That's a lovely name! I'm excited to help you on your learning journey."
        elif "status" in prompt.lower():
            return "Thank you for sharing that. It helps me understand your context better."
        elif "confusion" in prompt.lower() or "challenge" in prompt.lower():
            return "I appreciate your honesty. Identifying challenges is the first step to overcoming them."
        elif "struggle" in prompt.lower():
            return "That's a common challenge. Many successful people face similar obstacles."
        elif "task" in prompt.lower():
            return "Based on your profile, here's a personalized task for your growth."
        else:
            return "I understand. Let's move forward with this information."
    
    @staticmethod
    def analyze_reflection_quality(text: str) -> Dict[str, Any]:
        """Mock reflection quality analysis"""
        word_count = len(text.split())
        char_count = len(text)
        
        # Simple quality metrics
        quality_score = min(1.0, max(0.0, (word_count / 50) * 0.5 + (char_count / 200) * 0.5))
        
        return {
            'word_count': word_count,
            'character_count': char_count,
            'quality_score': round(quality_score, 2),
            'feedback': "Good reflection!" if quality_score > 0.7 else "Try to add more detail next time."
        }
