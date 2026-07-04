# app/models.py
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class TaskEstimate(BaseModel):
    """Model for task estimation"""
    task_name: str = Field(..., description="Name of the task")
    task_description: Optional[str] = Field(None, description="Detailed description of the task")
    estimated_time_hours: float = Field(..., description="Estimated time to complete the task in hours")
    required_resources: List[str] = Field(..., description="List of resources required to complete the task")
    dependencies: List[str] = Field(default_factory=list, description="List of task IDs this task depends on")
    complexity: str = Field("Medium", description="Complexity level: Low, Medium, High")
    deliverables: List[str] = Field(default_factory=list, description="List of deliverables for this task")
    assigned_to: Optional[str] = Field(None, description="Team member assigned to this task")

class Milestone(BaseModel):
    """Model for project milestone"""
    milestone_name: str = Field(..., description="Name of the milestone")
    description: Optional[str] = Field(None, description="Description of the milestone")
    tasks: List[str] = Field(..., description="List of task IDs associated with this milestone")
    target_date: Optional[str] = Field(None, description="Target completion date")
    status: str = Field("Pending", description="Status: Pending, In Progress, Completed")

class ResourceAllocation(BaseModel):
    """Model for resource allocation"""
    task_id: str = Field(..., description="Task ID")
    team_member: str = Field(..., description="Team member assigned")
    hours: float = Field(..., description="Allocated hours")
    start_date: Optional[str] = Field(None, description="Task start date")
    end_date: Optional[str] = Field(None, description="Task end date")
    priority: str = Field("Medium", description="Priority: Low, Medium, High")

class ProjectPlan(BaseModel):
    """Complete project plan model"""
    project_name: str = Field(..., description="Name of the project")
    project_objectives: str = Field(..., description="Project objectives")
    tasks: List[TaskEstimate] = Field(..., description="List of tasks with their estimates")
    milestones: List[Milestone] = Field(..., description="List of project milestones")
    resource_allocation: List[ResourceAllocation] = Field(
        default_factory=list, 
        description="Resource allocation plan"
    )
    total_estimated_hours: float = Field(0.0, description="Total estimated hours for the project")
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    status: str = Field("Draft", description="Plan status: Draft, Review, Approved")