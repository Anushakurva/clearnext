# ClearNext Backend - Student Guidance System

## 🏗️ Architecture

```text
backend/
├── app.py                 # Flask app entry point
├── start.py               # Startup script with options
├── config.py              # Configuration
├── requirements.txt         # Dependencies
├── models/                 # Data models
│   ├── __init__.py
│   ├── user.py
│   └── task.py
├── controllers/            # Route handlers
│   ├── __init__.py
│   ├── user_controller.py
│   ├── task_controller.py
│   └── reflection_controller.py
├── services/              # Business logic
│   ├── __init__.py
│   ├── user_service.py
│   ├── task_service.py
│   └── reflection_service.py
├── utils/                 # Utilities
│   ├── __init__.py
│   ├── validators.py
│   ├── database.py
│   └── mock_db.py
└── prompts/               # AI prompts (can be mocked)
    ├── __init__.py
    └── task_prompts.py
```

## 🚀 Features

- **User Management** - Guest and registered users
- **Journey Duration** - 7/14/21 day programs
- **Daily Tasks** - Personalized task delivery
- **Reflection Storage** - Student reflections with validation
- **AI Guidance** - Optional AI-based guidance (mockable)
- **MongoDB Integration** - With fallback to in-memory storage
- **Layered Architecture** - Clean separation of concerns

## 🛠️ Setup

### **Quick Start**
```bash
# Install dependencies
pip install -r requirements.txt

# Start with mock database (no MongoDB needed)
python start.py

# Start with MongoDB
python start.py --mongo
```

### **Development Mode**
```bash
# Debug mode with mock database
python start.py --debug

# Debug mode with MongoDB
python start.py --mongo --debug
```

### **Manual Start**
```bash
# With mock database
python app.py --mock

# With MongoDB
python app.py
```

## 📊 API Endpoints

### Users
- `POST /api/users/guest` - Create guest user
- `POST /api/users/register` - Register new user
- `POST /api/users/login` - User login
- `GET /api/users/:id` - Get user profile

### Tasks
- `GET /api/tasks/today/:user_id` - Get today's task
- `POST /api/tasks/:id/complete` - Complete task
- `GET /api/tasks/user/:user_id` - Get all user tasks

### Reflections
- `POST /api/reflections` - Submit reflection
- `GET /api/reflections/user/:user_id` - Get user reflections
- `POST /api/reflections/validate` - Validate reflection
- `GET /api/reflections/:id` - Get specific reflection

### System
- `GET /api/health` - Health check

## 🔧 Configuration

### **Environment Variables**
```bash
# Database
MONGO_URI=mongodb://localhost:27017/clearnext
USE_MOCK_DB=true

# Flask
SECRET_KEY=your-secret-key
FLASK_DEBUG=1

# CORS
CORS_ORIGINS=http://localhost:8000
```

### **Features**
- **Task Window** - 12:00 AM to 11:59 PM
- **Journey Duration** - 7, 14, or 21 days
- **Reflection Validation** - Minimum 50 characters
- **Progress Tracking** - Streaks and achievements
- **Mock AI** - Built-in AI responses for testing

## 🧪 Testing

### **Mock Mode**
- No MongoDB required
- In-memory database
- Mock AI responses
- Perfect for development

### **Production Mode**
- MongoDB connection
- Persistent storage
- Real AI integration ready
- Environment-based config
