# app/agents.py
import os
import logging
from crewai import Agent
from app.model_manager import model_manager
from app.tools import board_data_fetcher_tool, card_data_fetcher_tool, board_list_fetcher_tool

logger = logging.getLogger(__name__)

def create_project_planning_agent():
    """Create the project planning agent"""
    config = model_manager.get_model_config('project_planning_agent')
    llm = model_manager.get_llm(config['model'], config.get('temperature', 0.3))
    
    return Agent(
        role="Senior Project Planning Manager",
        goal="Create comprehensive project breakdowns and define clear task structures",
        backstory=(
            "You are an expert project planning manager with over 15 years of experience in "
            "software development and project management. You excel at breaking down complex "
            "projects into manageable tasks, identifying dependencies, and creating clear "
            "roadmaps."
        ),
        allow_delegation=False,
        verbose=True,
        llm=llm
    )

def create_estimation_agent():
    """Create the estimation agent"""
    config = model_manager.get_model_config('estimation_agent')
    llm = model_manager.get_llm(config['model'], config.get('temperature', 0.2))
    
    return Agent(
        role="Expert Estimation Specialist",
        goal="Provide accurate time and resource estimations for project tasks",
        backstory=(
            "You are a seasoned estimation specialist with deep expertise in project "
            "estimation techniques. You've worked on hundreds of projects and have a "
            "knack for predicting time requirements and resource needs with remarkable "
            "accuracy."
        ),
        allow_delegation=False,
        verbose=True,
        llm=llm
    )

def create_resource_allocation_agent():
    """Create the resource allocation agent"""
    config = model_manager.get_model_config('resource_allocation_agent')
    llm = model_manager.get_llm(config['model'], config.get('temperature', 0.4))
    
    return Agent(
        role="Resource Optimization Expert",
        goal="Optimally allocate resources and create realistic project schedules",
        backstory=(
            "You are a resource optimization expert who specializes in matching the right "
            "people to the right tasks. You understand team dynamics, skill sets, and "
            "project constraints."
        ),
        allow_delegation=False,
        verbose=True,
        llm=llm
    )

def create_data_collection_agent():
    """Create the data collection agent with Trello tools"""
    config = model_manager.get_model_config('data_collection_agent')
    llm = model_manager.get_llm(config['model'], config.get('temperature', 0.3))
    
    return Agent(
        role="Data Collection Specialist",
        goal="Collect and organize project data from external sources like Trello",
        backstory=(
            "You are a data collection specialist with expertise in gathering project "
            "information from various sources. You use tools like Trello API to fetch "
            "card data, comments, and activity logs. You organize this data into "
            "structured formats for analysis."
        ),
        allow_delegation=False,
        verbose=True,
        llm=llm,
        tools=[board_data_fetcher_tool, card_data_fetcher_tool, board_list_fetcher_tool]
    )

def create_analysis_agent():
    """Create the analysis agent"""
    config = model_manager.get_model_config('analysis_agent')
    llm = model_manager.get_llm(config['model'], config.get('temperature', 0.2))
    
    return Agent(
        role="Project Analysis Expert",
        goal="Analyze project data and generate comprehensive progress reports",
        backstory=(
            "You are a project analysis expert with deep experience in evaluating "
            "project progress, identifying bottlenecks, and providing actionable "
            "insights. You combine data from multiple sources to create detailed "
            "progress reports that help teams stay on track."
        ),
        allow_delegation=False,
        verbose=True,
        llm=llm
    )