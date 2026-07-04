# run.py
import os
import sys

# Add the current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.getenv('FLASK_ENV', 'development') == 'development'
    
    print("=" * 60)
    print("📋 AI Project Planner & Progress Reporter")
    print("=" * 60)
    print(f"🚀 Server running at: http://localhost:{port}")
    print(f"📱 Open in your browser")
    print("=" * 60)
    print("🤖 Agents:")
    print("  1. Project Planning Agent - Breaks down tasks")
    print("  2. Estimation Agent - Estimates time & resources")
    print("  3. Resource Allocation Agent - Allocates resources")
    print("  4. Data Collection Agent - Fetches Trello data")
    print("  5. Analysis Agent - Analyzes progress & generates reports")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=port, debug=debug)