"""Web dashboard for cross-project overview."""

import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime, timedelta

from roadmapper.projects import get_all_projects, get_project_health
from roadmapper.history import read_history, get_session_stats


def get_dashboard_data() -> Dict:
    """
    Get all data needed for dashboard display.
    
    Returns:
        Dictionary with projects, metrics, and patterns
    """
    projects = get_all_projects()
    
    # Calculate cross-project metrics
    total_projects = len(projects)
    total_sessions = 0
    sessions_last_7_days = 0
    sessions_last_30_days = 0
    
    health_counts = {
        "healthy": 0,
        "inactive": 0,
        "stale": 0,
        "unknown": 0,
    }
    
    projects_data = []
    
    for project_info in projects:
        project_path = Path(project_info["path"])
        
        # Get project stats
        try:
            stats = get_session_stats(project_path)
            project_sessions = stats.get("total_sessions", 0)
            total_sessions += project_sessions
            
            # Count recent sessions
            history = read_history(project_path)
            now = datetime.now()
            for record in history:
                try:
                    record_date_str = record["date"].replace("Z", "+00:00")
                    record_date = datetime.fromisoformat(record_date_str)
                    if record_date.tzinfo is None:
                        record_date = record_date.replace(tzinfo=now.tzinfo if now.tzinfo else None)
                    days_ago = (now - record_date).days
                    if days_ago <= 7:
                        sessions_last_7_days += 1
                    if days_ago <= 30:
                        sessions_last_30_days += 1
                except Exception:
                    pass
        except Exception:
            project_sessions = 0
        
        # Count health status
        health = project_info.get("health", "unknown")
        health_counts[health] = health_counts.get(health, 0) + 1
        
        # Get last session info
        last_session = project_info.get("last_session")
        last_session_date = None
        if last_session and last_session.get("date"):
            try:
                last_session_date = last_session["date"][:10]  # YYYY-MM-DD
            except Exception:
                pass
        
        projects_data.append({
            "name": project_info.get("name", project_path.name),
            "path": str(project_path),
            "health": health,
            "total_sessions": project_sessions,
            "last_session": last_session_date,
        })
    
    # Simple pattern detection - find common terms/issues
    patterns = detect_patterns(projects)
    
    return {
        "projects": projects_data,
        "metrics": {
            "total_projects": total_projects,
            "total_sessions": total_sessions,
            "sessions_last_7_days": sessions_last_7_days,
            "sessions_last_30_days": sessions_last_30_days,
            "health_counts": health_counts,
        },
        "patterns": patterns,
    }


def detect_patterns(projects: List[Dict]) -> List[Dict]:
    """
    Detect common patterns/issues across projects.
    
    This is a simple implementation - can be enhanced later.
    
    Args:
        projects: List of project info dictionaries
    
    Returns:
        List of detected patterns
    """
    patterns = []
    
    # Find projects with similar health issues
    stale_projects = [p for p in projects if p.get("health") == "stale"]
    if len(stale_projects) >= 2:
        patterns.append({
            "type": "stale_projects",
            "title": f"{len(stale_projects)} projects haven't been worked on recently",
            "description": "Consider reviewing or archiving these projects",
            "projects": [p.get("name") for p in stale_projects[:5]],
        })
    
    # Find projects with no sessions
    no_session_projects = []
    for project_info in projects:
        project_path = Path(project_info["path"])
        try:
            stats = get_session_stats(project_path)
            if stats.get("total_sessions", 0) == 0:
                no_session_projects.append(project_info.get("name"))
        except Exception:
            pass
    
    if no_session_projects:
        patterns.append({
            "type": "no_sessions",
            "title": f"{len(no_session_projects)} projects have no session history",
            "description": "These projects may need initialization or are new",
            "projects": no_session_projects[:5],
        })
    
    return patterns


def get_dashboard_template() -> str:
    """Get HTML template for dashboard (Jinja2 format)."""
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ProjectRoadmapper Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: #f5f5f5;
            color: #333;
            line-height: 1.6;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        header {
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2c3e50;
            margin-bottom: 10px;
        }
        .subtitle {
            color: #7f8c8d;
            font-size: 14px;
        }
        .metrics {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        .metric-card {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .metric-value {
            font-size: 32px;
            font-weight: bold;
            color: #3498db;
            margin-bottom: 5px;
        }
        .metric-label {
            color: #7f8c8d;
            font-size: 14px;
        }
        .projects-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        .project-card {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border-left: 4px solid #3498db;
        }
        .project-card.healthy { border-left-color: #27ae60; }
        .project-card.inactive { border-left-color: #f39c12; }
        .project-card.stale { border-left-color: #95a5a6; }
        .project-card.unknown { border-left-color: #95a5a6; }
        .project-name {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 10px;
            color: #2c3e50;
        }
        .project-path {
            font-size: 12px;
            color: #7f8c8d;
            margin-bottom: 10px;
            word-break: break-all;
        }
        .project-stats {
            display: flex;
            gap: 15px;
            font-size: 14px;
        }
        .stat-item {
            color: #7f8c8d;
        }
        .stat-value {
            font-weight: bold;
            color: #2c3e50;
        }
        .patterns {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .pattern-item {
            padding: 15px;
            margin-bottom: 15px;
            border-left: 4px solid #e74c3c;
            background: #fef5e7;
            border-radius: 4px;
        }
        .pattern-title {
            font-weight: bold;
            margin-bottom: 5px;
            color: #2c3e50;
        }
        .pattern-description {
            color: #7f8c8d;
            font-size: 14px;
            margin-bottom: 10px;
        }
        .pattern-projects {
            font-size: 12px;
            color: #7f8c8d;
        }
        .health-badge {
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: bold;
            text-transform: uppercase;
        }
        .health-badge.healthy { background: #d5f4e6; color: #27ae60; }
        .health-badge.inactive { background: #fef5e7; color: #f39c12; }
        .health-badge.stale { background: #ecf0f1; color: #95a5a6; }
        .health-badge.unknown { background: #ecf0f1; color: #95a5a6; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🗺️ ProjectRoadmapper Dashboard</h1>
            <div class="subtitle">Cross-project overview and metrics</div>
        </header>
        
        <div class="metrics">
            <div class="metric-card">
                <div class="metric-value">{{ metrics.total_projects }}</div>
                <div class="metric-label">Total Projects</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{{ metrics.total_sessions }}</div>
                <div class="metric-label">Total Sessions</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{{ metrics.sessions_last_7_days }}</div>
                <div class="metric-label">Sessions (7 days)</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{{ metrics.sessions_last_30_days }}</div>
                <div class="metric-label">Sessions (30 days)</div>
            </div>
        </div>
        
        {% if patterns %}
        <div class="patterns">
            <h2 style="margin-bottom: 15px;">🔍 Detected Patterns</h2>
            {% for pattern in patterns %}
            <div class="pattern-item">
                <div class="pattern-title">{{ pattern.title }}</div>
                <div class="pattern-description">{{ pattern.description }}</div>
                {% if pattern.projects %}
                <div class="pattern-projects">
                    Projects: {{ pattern.projects|join(', ') }}
                </div>
                {% endif %}
            </div>
            {% endfor %}
        </div>
        {% endif %}
        
        <h2 style="margin: 20px 0;">📁 Projects</h2>
        <div class="projects-grid">
            {% for project in projects %}
            <div class="project-card {{ project.health }}">
                <div class="project-name">{{ project.name }}</div>
                <div class="project-path">{{ project.path }}</div>
                <div class="project-stats">
                    <div class="stat-item">
                        <span class="stat-value">{{ project.total_sessions }}</span> sessions
                    </div>
                    <div class="stat-item">
                        Health: <span class="health-badge {{ project.health }}">{{ project.health }}</span>
                    </div>
                </div>
                {% if project.last_session %}
                <div style="margin-top: 10px; font-size: 12px; color: #7f8c8d;">
                    Last session: {{ project.last_session }}
                </div>
                {% endif %}
            </div>
            {% endfor %}
        </div>
    </div>
</body>
</html>"""

