#!/usr/bin/env python3
"""
Startup script for the AI PDF Assistant chatbot
This script helps you start the chatbot and checks your setup
"""

import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'flask', 'flask_cors', 'PyPDF2', 'mistralai', 
        'python-dotenv', 'langchain', 'langchain-mistralai', 'tiktoken'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} - Missing")
    
    if missing_packages:
        print(f"\n📦 Installing missing packages: {', '.join(missing_packages)}")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_packages)
            print("✅ All packages installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install packages. Please run manually:")
            print(f"   pip install {' '.join(missing_packages)}")
            return False
    
    return True

def check_env_file():
    """Check if .env file exists and has Mistral AI API key"""
    env_file = Path('.env')
    
    if not env_file.exists():
        print("❌ .env file not found")
        print("📝 Creating .env file...")
        
        api_key = input("Enter your Mistral AI API key (or press Enter to skip for now): ").strip()
        
        if api_key:
            with open(env_file, 'w') as f:
                f.write(f"MISTRAL_API_KEY={api_key}\n")
            print("✅ .env file created with Mistral AI API key")
            return True
        else:
            # Create empty .env file
            with open(env_file, 'w') as f:
                f.write("# Mistral AI API Configuration\n")
                f.write("# Get your free API key from: https://console.mistral.ai/\n")
                f.write("MISTRAL_API_KEY=your_mistral_api_key_here\n")
            print("⚠️  .env file created without API key")
            print("   You'll need to add your Mistral AI API key to use AI features")
            print("   Get your free API key from: https://console.mistral.ai/")
            return False
    else:
        # Check if API key is set
        with open(env_file, 'r') as f:
            content = f.read()
            if 'MISTRAL_API_KEY=your_mistral_api_key_here' in content or 'MISTRAL_API_KEY=' in content:
                print("⚠️  .env file exists but Mistral AI API key not configured")
                print("   Please add your Mistral AI API key to the .env file")
                print("   Get your free API key from: https://console.mistral.ai/")
                return False
            else:
                print("✅ .env file configured with Mistral AI API key")
                return True

def start_backend():
    """Start the Flask backend"""
    print("\n🚀 Starting the chatbot backend...")
    
    try:
        # Change to backend directory
        backend_dir = Path('backend')
        if not backend_dir.exists():
            print("❌ Backend directory not found")
            return False
        
        os.chdir(backend_dir)
        
        # Check if app.py exists
        if not Path('app.py').exists():
            print("❌ app.py not found in backend directory")
            return False
        
        print("✅ Backend files found")
        print("🌐 Starting Flask server on http://127.0.0.1:5000")
        print("📱 You can now open the frontend in your browser")
        print("\n" + "="*50)
        print("Press Ctrl+C to stop the server")
        print("="*50)
        
        # Start the Flask app
        subprocess.run([sys.executable, 'app.py'])
        
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        return False
    
    return True

def open_frontend():
    """Open the frontend in the browser"""
    frontend_file = Path('frontend/index.html')
    if frontend_file.exists():
        print(f"\n🌐 Opening frontend: {frontend_file.absolute()}")
        try:
            webbrowser.open(f'file://{frontend_file.absolute()}')
        except Exception as e:
            print(f"⚠️  Could not open browser automatically: {e}")
            print(f"   Please manually open: {frontend_file.absolute()}")
    else:
        print("❌ Frontend file not found")

def main():
    """Main startup function"""
    print("🤖 AI PDF Assistant - Startup Script (Mistral AI)")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check dependencies
    print("\n📦 Checking dependencies...")
    if not check_dependencies():
        print("\n❌ Please install missing dependencies and try again")
        sys.exit(1)
    
    # Check environment configuration
    print("\n🔧 Checking environment configuration...")
    check_env_file()
    
    # Show startup options
    print("\n🎯 Startup Options:")
    print("1. Start backend server (recommended)")
    print("2. Open frontend only")
    print("3. Run tests")
    print("4. Exit")
    
    while True:
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            start_backend()
            break
        elif choice == '2':
            open_frontend()
            break
        elif choice == '3':
            print("\n🧪 Running tests...")
            os.chdir('..')  # Go back to chatbot directory
            subprocess.run([sys.executable, 'test_chatbot.py'])
            break
        elif choice == '4':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    main() 