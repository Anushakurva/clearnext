#!/usr/bin/env python3
"""
ClearNext Backend Startup Script
Quick start for development and testing
"""

import os
import sys
import subprocess

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = ['flask', 'pymongo']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("Install with: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies satisfied")
    return True

def setup_environment():
    """Setup environment variables"""
    if not os.environ.get('MONGO_URI'):
        os.environ['MONGO_URI'] = 'mongodb://localhost:27017/clearnext'
        print("📝 Set default MongoDB URI")
    
    if not os.environ.get('USE_MOCK_DB'):
        os.environ['USE_MOCK_DB'] = 'true'
        print("📝 Using mock database (add --mongo to use MongoDB)")

def main():
    """Main startup function"""
    print("🚀 ClearNext Backend Startup")
    print("=" * 40)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Setup environment
    setup_environment()
    
    # Command line arguments
    use_mongo = '--mongo' in sys.argv
    debug_mode = '--debug' in sys.argv
    
    if use_mongo:
        os.environ['USE_MOCK_DB'] = 'false'
        print("🗄️ Using MongoDB database")
    else:
        print("📝 Using mock database")
    
    if debug_mode:
        os.environ['FLASK_DEBUG'] = '1'
        print("🐛 Debug mode enabled")
    
    print("=" * 40)
    print("🌟 Starting ClearNext Backend...")
    print(f"📍 Database: {'MongoDB' if use_mongo else 'Mock'}")
    print(f"🔧 Debug: {'On' if debug_mode else 'Off'}")
    print(f"🌐 Server: http://localhost:5000")
    print("=" * 40)
    
    # Start Flask app
    try:
        if use_mongo:
            subprocess.run([sys.executable, 'app.py'], check=True)
        else:
            subprocess.run([sys.executable, 'app.py', '--mock'], check=True)
    except KeyboardInterrupt:
        print("\n👋 ClearNext Backend stopped gracefully")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
