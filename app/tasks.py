# app/tasks.py
from crewai import Task
import logging

logger = logging.getLogger(__name__)

def create_task_breakdown_task(agent, project_data: dict):
    """Create the task breakdown task"""
    return Task(
        description=f"""
        Break down the following project into detailed tasks:
        
        Project Type: {project_data.get('project_type', 'Website')}
        Project Objectives: {project_data.get('project_objectives', 'Create a website')}
        Industry: {project_data.get('industry', 'Technology')}
        Team Members: {project_data.get('team_members', '')}
        Project Requirements: {project_data.get('project_requirements', '')}
        
        Create a comprehensive task breakdown that includes:
        1. Clear task names and descriptions
        2. Task dependencies and order
        3. Estimated complexity levels (Low, Medium, High)
        4. Required skills for each task
        5. Deliverables for each task
        
        Format the output as a structured list of tasks with clear descriptions.
        """,
        expected_output="""
        A detailed task breakdown with the following structure:
        - Task ID (e.g., T001, T002)
        - Task Name
        - Task Description
        - Dependencies (list of Task IDs)
        - Complexity (Low/Medium/High)
        - Required Skills
        - Deliverables
        """,
        agent=agent
    )

def create_estimation_task(agent, project_data: dict):
    """Create the estimation task"""
    return Task(
        description=f"""
        Based on the following project details, provide accurate time and resource estimates:
        
        Project Type: {project_data.get('project_type', 'Website')}
        Project Objectives: {project_data.get('project_objectives', 'Create a website')}
        Industry: {project_data.get('industry', 'Technology')}
        Team Members: {project_data.get('team_members', '')}
        Project Requirements: {project_data.get('project_requirements', '')}
        
        For each task, estimate:
        1. Time required in hours
        2. Resources needed (team members, tools, skills)
        3. Dependencies between tasks
        4. Potential risks and buffers
        
        Provide realistic estimates based on industry standards and team capabilities.
        """,
        expected_output="""
        A comprehensive estimation report with:
        - Task ID
        - Estimated Time (in hours)
        - Required Resources (list)
        - Dependencies (list of Task IDs)
        - Risk Factors
        - Buffer Time (in hours)
        """,
        agent=agent
    )

def create_resource_allocation_task(agent, project_data: dict):
    """Create the resource allocation task"""
    return Task(
        description=f"""
        Create an optimal resource allocation plan based on the following project:
        
        Project Type: {project_data.get('project_type', 'Website')}
        Project Objectives: {project_data.get('project_objectives', 'Create a website')}
        Industry: {project_data.get('industry', 'Technology')}
        Team Members: {project_data.get('team_members', '')}
        Project Requirements: {project_data.get('project_requirements', '')}
        
        The plan should include:
        1. Task assignments to specific team members
        2. Start and end dates for each task
        3. Milestones with deadlines
        4. Resource utilization across the timeline
        5. Buffer for unexpected delays
        
        Ensure optimal resource utilization and realistic scheduling.
        """,
        expected_output="""
        A comprehensive resource allocation plan with:
        - Task ID
        - Assigned Team Member
        - Start Date
        - End Date
        - Allocated Hours
        - Priority Level
        - Milestone Name
        - Resource Utilization Percentage
        """,
        agent=agent
    )

def create_data_collection_task(agent):
    """Create the data collection task"""
    return Task(
        description="""
        Collect project data from Trello board and organize it for analysis.
        
        Use the BoardDataFetcherTool to fetch all cards, their details, comments,
        and activity logs. Then use CardDataFetcherTool to get detailed information
        about specific cards if needed.
        
        Organize the collected data into a structured format including:
        1. List of all cards with their statuses
        2. Card details (name, description, due date, labels)
        3. Comments and activity logs
        4. Card assignments and progress
        5. Overall board statistics (total cards, completed, in progress, blocked)
        
        Calculate the following metrics:
        - Total number of cards
        - Cards by list/status
        - Cards with due dates
        - Cards with comments
        - Completion rate
        """,
        expected_output="""
        A comprehensive dataset containing all Trello board information in a
        structured format ready for analysis.
        """,
        agent=agent
    )

def create_data_analysis_task(agent):
    """Create the data analysis task"""
    return Task(
        description="""
        Analyze the collected project data to generate insights about project progress.
        
        Based on the Trello board data, provide analysis on:
        1. Overall project progress (percentage complete)
        2. Task completion rates by list/status
        3. Bottlenecks and blockers
        4. Team performance metrics
        5. Upcoming deadlines and milestones
        6. Risk assessment and issues
        7. Recommendations for improvement
        
        Calculate key metrics:
        - Completion rate = (Completed tasks / Total tasks) * 100
        - On-track tasks percentage
        - At-risk tasks percentage
        - Average time to complete a task
        - Team workload distribution
        """,
        expected_output="""
        A detailed analysis report with key metrics, insights, and recommendations
        for improving project progress.
        """,
        agent=agent
    )

def create_report_generation_task(agent):
    """Create the report generation task"""
    return Task(
        description="""
        Generate a comprehensive project progress report based on the analysis.
        
        The report should include:
        1. Executive Summary
           - Project overview
           - Key achievements
           - Critical issues
        
        2. Project Overview and Status
           - Overall progress
           - Milestone status
           - Timeline variance
        
        3. Task Completion Analysis
           - Completed tasks
           - In-progress tasks
           - Blocked tasks
           - Task completion rate by team member
        
        4. Team Performance Metrics
           - Individual contributions
           - Workload balance
           - Efficiency metrics
        
        5. Risk Assessment
           - Identified risks
           - Impact analysis
           - Mitigation strategies
        
        6. Recommendations
           - Process improvements
           - Resource reallocation
           - Priority adjustments
        
        7. Next Steps
           - Immediate actions
           - Upcoming milestones
           - Long-term goals
        
        Format the report professionally with clear sections and data visualization
        recommendations.
        """,
        expected_output="""
        A well-structured project progress report in markdown format with all
        sections, metrics, and actionable recommendations.
        """,
        agent=agent
    )