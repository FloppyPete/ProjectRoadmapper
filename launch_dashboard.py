#!/usr/bin/env python3
"""
Simple launcher for ProjectRoadmapper Dashboard.

Double-click this file to start the dashboard server and open it in your browser.
"""

import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def main():
    """Launch the dashboard with automatic browser opening."""
    print("🚀 Starting ProjectRoadmapper Dashboard...")
    print("=" * 50)
    
    # Check if Flask is installed
    try:
        import flask
    except ImportError:
        print("\n❌ Flask is required for the dashboard.")
        print("\nTo install Flask, run:")
        print("   pip install flask")
        print("\nOr install roadmapper with dashboard support:")
        print("   pip install 'roadmapper[dashboard]'")
        print("\nPress Enter to exit...")
        input()
        sys.exit(1)
    
    # Import after checking
    from roadmapper.dashboard import get_dashboard_data, get_dashboard_template
    from flask import Flask, render_template_string
    
    # Create Flask app
    app = Flask(__name__)
    
    @app.route("/")
    def index():
        data = get_dashboard_data()
        template = get_dashboard_template()
        return render_template_string(template, **data)
    
    # Open browser after a short delay
    url = "http://127.0.0.1:5000"
    print(f"\n📊 Dashboard will be available at: {url}")
    print("🌐 Opening browser automatically...")
    print("\n💡 The dashboard server will keep running.")
    print("   Close this window to stop the server.\n")
    
    # Open browser after a brief delay
    def open_browser():
        time.sleep(1.5)  # Give server time to start
        webbrowser.open(url)
    
    import threading
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    # Run Flask app
    try:
        app.run(host="127.0.0.1", port=5000, debug=False)
    except KeyboardInterrupt:
        print("\n\n👋 Dashboard server stopped")
    except Exception as e:
        print(f"\n❌ Error starting dashboard: {e}")
        print("\nPress Enter to exit...")
        input()
        sys.exit(1)


if __name__ == "__main__":
    main()

