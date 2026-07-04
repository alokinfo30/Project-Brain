# Project-Brain
Automated Project Planning, Estimation, and Allocation System


# AI Project Planning Agent

A multi-agent system for automated project planning, estimation, and resource allocation using CrewAI and OpenRouter.

## Features

- 🤖 **3 Specialized Agents**: Planning, Estimation, Resource Allocation
- 🧠 **Multi-Model Support**: Auto-fallback between OpenAI, Mistral, Llama, DeepSeek
- 📋 **Automated Task Breakdown**: Creates detailed task lists
- ⏱️ **Time & Resource Estimation**: Accurate project estimates
- 📊 **Resource Allocation**: Optimized team assignments
- 🔄 **Auto-Fallback**: If one model fails, others take over
- 🌐 **Web Interface**: User-friendly dashboard

## Architecture
User Input → Planning Agent → Estimation Agent → Resource Allocation Agent → Project Plan



ProjectPlanner/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── model_manager.py
│   ├── agents.py
│   ├── tasks.py
│   ├── crew.py
│   ├── models.py
|   ├── tools.py
│   └── utils.py
├── config/
│   ├── agents.yaml
│   └── tasks.yaml
├── templates/
│   └── index.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
├── data/
│   └── .gitkeep
├── .env
├── .gitignore
├── requirements.txt
├── run.py
└── README.md





### Agents

1. **Project Planning Agent**: Breaks down projects into tasks
2. **Estimation Agent**: Estimates time and resources
3. **Resource Allocation Agent**: Allocates team members


Configuration

Environment Variables
Variable	Description
OPENROUTER_API_KEY	Your OpenRouter API key
OPENROUTER_PRIMARY_MODEL	Primary model to use
OPENROUTER_FALLBACK_MODELS	Fallback models
PROJECT_PLANNING_MODEL	Model for planning agent
ESTIMATION_MODEL	Model for estimation agent
RESOURCE_ALLOCATION_MODEL	Model for resource allocation agent
Models Used
Model	Provider	Purpose
openai/gpt-4o-mini	OpenAI	Planning & Analysis
mistralai/mixtral-8x22b-instruct	Mistral	Estimation
meta-llama/llama-3.1-8b-instruct	Meta	Resource Allocation
deepseek/deepseek-chat	DeepSeek	Fallback
API Endpoints
Endpoint	Method	Description
/	GET	Web interface
/api/plan	POST	Generate project plan
/api/models	GET	List available models
/api/health	GET	Health check


Usage

Open http://localhost:5000

Fill in project details
Click "Generate Project Plan"
View the generated plan with tasks, milestones, and resource allocation


License
MIT

text

## Step 19: `data/.gitkeep`
This file ensures the data directory is tracked in git
text

## Step 20: Final Commands
## Installation
```powershell
# 1. Create virtual environment
python -m venv venv

# 2. Activate it
venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
python run.py

# 5. Open browser
# http://localhost:5000
Summary
This complete project implements:

✅ 3 Specialized Agents: Planning, Estimation, Resource Allocation
✅ Multi-Model Support: Auto-fallback between 4 models
✅ Web Interface: User-friendly dashboard
✅ Structured Output: Pydantic models for validation
✅ Error Handling: Graceful failure with fallbacks
✅ Complete Documentation: README with setup instructions
✅ Deployment Ready: Works with Render, Heroku

The system automatically:

Breaks down projects into tasks
Estimates time and resources
Allocates team members optimally
Creates milestones and timelines
All powered by CrewAI and OpenRouter with automatic model fallback! 🚀



Project Planning Features:

Task breakdown
Time estimation
Resource allocation
Multi-model support with auto-fallback

✅ Progress Report Features:

Trello board integration
Data collection from external sources
Project progress analysis

Comprehensive report generation

✅ Multi-Agent System:

Project Planning Agent - Breaks down tasks
Estimation Agent - Estimates time & resources
Resource Allocation Agent - Allocates team members
Data Collection Agent - Fetches Trello data with custom tools
Analysis Agent - Analyzes data and generates reports

✅ Technology Stack:

CrewAI for multi-agent orchestration
OpenRouter for multi-model support (OpenAI, Mistral, Llama, DeepSeek)
Trello API for external integration
Flask for web interface
Pydantic for structured output

✅ Features:

Auto-fallback between 4 models
Real-time agent status updates
Export functionality for plans and reports
Fully responsive design for mobile and laptop
Error handling with graceful fallbacks