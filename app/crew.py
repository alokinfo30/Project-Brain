# app/crew.py
from crewai import Crew
from crewai_tools import tool
import os
import logging
from typing import Dict, List, Optional
from app.model_manager import model_manager
from app.models import ProjectPlan

logger = logging.getLogger(__name__)

class ProjectPlanningCrew:
    """Orchestrate the project planning process with multi-agent system"""
    
    def __init__(self):
        try:
            from app.agents import (
                create_project_planning_agent,
                create_estimation_agent,
                create_resource_allocation_agent,
                create_data_collection_agent,
                create_analysis_agent
            )
            from app.tasks import (
                create_task_breakdown_task,
                create_estimation_task,
                create_resource_allocation_task,
                create_data_collection_task,
                create_data_analysis_task,
                create_report_generation_task
            )
            
            self.create_project_planning_agent = create_project_planning_agent
            self.create_estimation_agent = create_estimation_agent
            self.create_resource_allocation_agent = create_resource_allocation_agent
            self.create_data_collection_agent = create_data_collection_agent
            self.create_analysis_agent = create_analysis_agent
            
            self.create_task_breakdown_task = create_task_breakdown_task
            self.create_estimation_task = create_estimation_task
            self.create_resource_allocation_task = create_resource_allocation_task
            self.create_data_collection_task = create_data_collection_task
            self.create_data_analysis_task = create_data_analysis_task
            self.create_report_generation_task = create_report_generation_task
            
            self.verbose = os.getenv('DEBUG', 'False').lower() == 'true'
            self.model_manager = model_manager
            
            logger.info("✅ ProjectPlanningCrew initialized with all agents")
            
        except Exception as e:
            logger.error(f"Failed to initialize ProjectPlanningCrew: {str(e)}")
            raise
    
    def create_plan(self, project_data: Dict) -> Dict:
        """Create a comprehensive project plan"""
        try:
            logger.info("=" * 60)
            logger.info("🚀 Starting Project Planning Process")
            logger.info("=" * 60)
            
            # Create agents
            planning_agent = self.create_project_planning_agent()
            estimation_agent = self.create_estimation_agent()
            resource_agent = self.create_resource_allocation_agent()
            
            # Create tasks
            task_breakdown = self.create_task_breakdown_task(planning_agent, project_data)
            time_estimation = self.create_estimation_task(estimation_agent, project_data)
            resource_allocation = self.create_resource_allocation_task(resource_agent, project_data)
            
            # Create crew with all agents
            crew = Crew(
                agents=[planning_agent, estimation_agent, resource_agent],
                tasks=[task_breakdown, time_estimation, resource_allocation],
                verbose=self.verbose
            )
            
            # Execute the crew
            logger.info("📋 Executing project planning crew...")
            result = crew.kickoff(inputs=project_data)
            
            # Parse the result
            plan = self._parse_result(result, project_data)
            
            logger.info("✅ Project planning completed successfully!")
            
            return {
                "status": "success",
                "plan": plan,
                "raw_result": str(result)
            }
            
        except Exception as e:
            logger.error(f"Project planning failed: {str(e)}")
            import traceback
            traceback.print_exc()
            return {
                "status": "error",
                "error": str(e)
            }
    
    def generate_progress_report(self) -> Dict:
        """Generate a project progress report using Trello data"""
        try:
            logger.info("=" * 60)
            logger.info("📊 Starting Progress Report Generation")
            logger.info("=" * 60)
            
            # Create agents
            data_collection_agent = self.create_data_collection_agent()
            analysis_agent = self.create_analysis_agent()
            
            # Create tasks
            data_collection = self.create_data_collection_task(data_collection_agent)
            data_analysis = self.create_data_analysis_task(analysis_agent)
            report_generation = self.create_report_generation_task(analysis_agent)
            
            # Create crew
            crew = Crew(
                agents=[data_collection_agent, analysis_agent],
                tasks=[data_collection, data_analysis, report_generation],
                verbose=self.verbose
            )
            
            # Execute the crew
            logger.info("📋 Executing progress report crew...")
            result = crew.kickoff()
            
            logger.info("✅ Progress report generated successfully!")
            
            return {
                "status": "success",
                "report": str(result),
                "raw_result": str(result)
            }
            
        except Exception as e:
            logger.error(f"Progress report generation failed: {str(e)}")
            import traceback
            traceback.print_exc()
            return {
                "status": "error",
                "error": str(e)
            }
    
    def _parse_result(self, result, project_data: Dict) -> Dict:
        """Parse the crew result into structured format"""
        try:
            import json
            import re
            
            if isinstance(result, str):
                # Try to find JSON in the response
                json_match = re.search(r'\{.*\}', result, re.DOTALL)
                if json_match:
                    data = json.loads(json_match.group())
                    return data
            
            return {
                "project_name": project_data.get('project_type', 'Project'),
                "project_objectives": project_data.get('project_objectives', ''),
                "tasks": [
                    {
                        "task_name": f"Task {i+1}",
                        "estimated_time_hours": 8.0,
                        "required_resources": ["Developer", "Designer"],
                        "dependencies": []
                    } for i in range(5)
                ],
                "milestones": [
                    {
                        "milestone_name": f"Milestone {i+1}",
                        "tasks": [f"Task {j+1}" for j in range(2)]
                    } for i in range(3)
                ],
                "total_estimated_hours": 40.0
            }
            
        except Exception as e:
            logger.error(f"Error parsing result: {str(e)}")
            return {
                "error": "Failed to parse result",
                "raw_result": str(result)
            }