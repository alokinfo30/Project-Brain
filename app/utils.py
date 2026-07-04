# app/utils.py
import json
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

def parse_ai_response(response: str) -> Dict[str, Any]:
    """Parse AI response to extract structured data"""
    import re
    
    try:
        # Try to parse as JSON directly
        if response.strip().startswith('{'):
            return json.loads(response)
        
        # Try to find JSON block in the response
        json_match = re.search(r'```json\s*(\{.*\})\s*```', response, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(1))
        
        # Try to find any JSON object
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(0))
        
        # Return empty dict if no JSON found
        return {}
        
    except json.JSONDecodeError as e:
        logger.error(f"JSON parse error: {str(e)}")
        return {}
    except Exception as e:
        logger.error(f"Error parsing AI response: {str(e)}")
        return {}

def format_project_plan(plan: Dict) -> str:
    """Format project plan for display"""
    if not plan:
        return "No plan available"
    
    output = []
    output.append("# Project Plan")
    output.append("")
    output.append(f"**Project:** {plan.get('project_name', 'Unnamed Project')}")
    output.append(f"**Status:** {plan.get('status', 'Draft')}")
    output.append(f"**Total Estimated Hours:** {plan.get('total_estimated_hours', 0)}")
    output.append("")
    
    # Tasks
    tasks = plan.get('tasks', [])
    if tasks:
        output.append("## Tasks")
        output.append("")
        for i, task in enumerate(tasks, 1):
            output.append(f"### Task {i}: {task.get('task_name', 'Untitled')}")
            output.append(f"- **Estimated Time:** {task.get('estimated_time_hours', 0)} hours")
            output.append(f"- **Complexity:** {task.get('complexity', 'Medium')}")
            output.append(f"- **Resources:** {', '.join(task.get('required_resources', []))}")
            output.append("")
    
    # Milestones
    milestones = plan.get('milestones', [])
    if milestones:
        output.append("## Milestones")
        output.append("")
        for milestone in milestones:
            output.append(f"### {milestone.get('milestone_name', 'Untitled')}")
            output.append(f"- **Tasks:** {', '.join(milestone.get('tasks', []))}")
            output.append("")
    
    return "\n".join(output)