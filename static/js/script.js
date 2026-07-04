document.addEventListener('DOMContentLoaded', function() {
    // Tab switching
    const tabs = document.querySelectorAll('.tab');
    const tabContents = {
        planning: document.getElementById('planningTab'),
        progress: document.getElementById('progressTab')
    };

    tabs.forEach(tab => {
        tab.addEventListener('click', function() {
            tabs.forEach(t => t.classList.remove('active'));
            this.classList.add('active');
            
            const tabName = this.dataset.tab;
            Object.keys(tabContents).forEach(key => {
                tabContents[key].classList.toggle('active', key === tabName);
            });
        });
    });

    // ============================================
    // PLANNING SECTION
    // ============================================

    const form = document.getElementById('projectForm');
    const generateBtn = document.getElementById('generateBtn');
    const processing = document.getElementById('processing');
    const results = document.getElementById('results');
    const planContent = document.getElementById('planContent');
    const progressLog = document.getElementById('progressLog');
    const exportBtn = document.getElementById('exportBtn');

    // Load models on startup
    async function loadModels() {
        try {
            const response = await fetch('/api/models');
            const data = await response.json();
            
            const modelList = document.getElementById('modelList');
            modelList.innerHTML = '';
            
            if (data.status === 'success') {
                const models = data.models;
                const allModels = [models.primary, ...models.fallbacks];
                
                allModels.forEach(model => {
                    if (model && model.trim()) {
                        const div = document.createElement('div');
                        div.className = 'model-item';
                        const isAvailable = models.available.includes(model);
                        if (!isAvailable) {
                            div.classList.add('unavailable');
                        }
                        div.textContent = `${model} ${isAvailable ? '✅' : '❌'}`;
                        modelList.appendChild(div);
                    }
                });
            }
        } catch (error) {
            console.error('Error loading models:', error);
            document.getElementById('modelList').innerHTML = '⚠️ Failed to load models';
        }
    }

    // Update agent status
    function updateAgentStatus(status, message) {
        const statusMap = {
            'idle': { agent1: '⏳ Planning Agent: Idle', agent2: '⏳ Estimation Agent: Idle', agent3: '⏳ Allocation Agent: Idle' },
            'planning': { agent1: '📋 Planning Agent: Breaking down tasks...', agent2: '⏳ Estimation Agent: Waiting', agent3: '⏳ Allocation Agent: Waiting' },
            'estimating': { agent1: '✅ Planning Agent: Complete', agent2: '📊 Estimation Agent: Estimating...', agent3: '⏳ Allocation Agent: Waiting' },
            'allocating': { agent1: '✅ Planning Agent: Complete', agent2: '✅ Estimation Agent: Complete', agent3: '📋 Allocation Agent: Allocating...' },
            'complete': { agent1: '✅ Planning Agent: Complete', agent2: '✅ Estimation Agent: Complete', agent3: '✅ Allocation Agent: Complete' },
            'error': { agent1: '❌ Planning Agent: Error', agent2: '❌ Estimation Agent: Error', agent3: '❌ Allocation Agent: Error' }
        };

        const statuses = statusMap[status] || statusMap.idle;
        document.getElementById('agent1').textContent = statuses.agent1;
        document.getElementById('agent2').textContent = statuses.agent2;
        document.getElementById('agent3').textContent = statuses.agent3;
        
        if (message) {
            const logEntry = document.createElement('div');
            logEntry.textContent = `🔄 ${new Date().toLocaleTimeString()}: ${message}`;
            progressLog.appendChild(logEntry);
            progressLog.scrollTop = progressLog.scrollHeight;
        }
    }

    // Handle form submission
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Get form data
        const data = {
            project_type: document.getElementById('projectType').value.trim(),
            project_objectives: document.getElementById('projectObjectives').value.trim(),
            industry: document.getElementById('industry').value.trim(),
            team_members: document.getElementById('teamMembers').value.trim(),
            project_requirements: document.getElementById('projectRequirements').value.trim()
        };

        // Validate
        if (!data.project_type || !data.project_objectives || !data.industry) {
            alert('Please fill in all required fields (marked with *)');
            return;
        }

        // Show processing
        processing.classList.remove('hidden');
        results.classList.add('hidden');
        progressLog.innerHTML = '';
        generateBtn.disabled = true;
        generateBtn.textContent = 'Generating...';
        
        updateAgentStatus('idle', 'Starting project planning process...');

        try {
            updateAgentStatus('planning', 'Planning agent is breaking down tasks...');
            
            const response = await fetch('/api/plan', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (response.ok && result.status === 'success') {
                updateAgentStatus('complete', '✅ Project plan generated successfully!');
                displayPlan(result.result);
            } else {
                updateAgentStatus('error', `❌ Error: ${result.error || 'Unknown error'}`);
                alert(`Error: ${result.error || 'Failed to generate plan'}`);
            }
        } catch (error) {
            console.error('Error:', error);
            updateAgentStatus('error', `❌ Network error: ${error.message}`);
            alert('Error generating plan. Please try again.');
        } finally {
            processing.classList.add('hidden');
            generateBtn.disabled = false;
            generateBtn.textContent = '🚀 Generate Project Plan';
        }
    });

    // Display plan
    function displayPlan(planData) {
        results.classList.remove('hidden');
        
        let html = '';
        
        // Plan summary
        html += `<h2>📋 ${planData.plan?.project_name || 'Project Plan'}</h2>`;
        html += `<p><strong>Status:</strong> ${planData.plan?.status || 'Draft'}</p>`;
        html += `<p><strong>Total Estimated Hours:</strong> ${planData.plan?.total_estimated_hours || 0}</p>`;
        html += `<hr>`;
        
        // Tasks
        const tasks = planData.plan?.tasks || [];
        if (tasks.length > 0) {
            html += `<h3>📝 Tasks</h3>`;
            tasks.forEach((task, i) => {
                html += `<div style="background: rgba(255,255,255,0.03); padding: 15px; border-radius: 8px; margin-bottom: 10px; border-left: 3px solid #667eea;">`;
                html += `<h4>Task ${i+1}: ${task.task_name || 'Untitled'}</h4>`;
                html += `<p><strong>Estimated Time:</strong> ${task.estimated_time_hours || 0} hours</p>`;
                html += `<p><strong>Complexity:</strong> ${task.complexity || 'Medium'}</p>`;
                if (task.required_resources && task.required_resources.length > 0) {
                    html += `<p><strong>Resources:</strong> ${task.required_resources.join(', ')}</p>`;
                }
                html += `</div>`;
            });
        }
        
        // Milestones
        const milestones = planData.plan?.milestones || [];
        if (milestones.length > 0) {
            html += `<h3>🎯 Milestones</h3>`;
            milestones.forEach((milestone, i) => {
                html += `<div style="background: rgba(255,255,255,0.03); padding: 15px; border-radius: 8px; margin-bottom: 10px; border-left: 3px solid #764ba2;">`;
                html += `<h4>${milestone.milestone_name || `Milestone ${i+1}`}</h4>`;
                if (milestone.tasks && milestone.tasks.length > 0) {
                    html += `<p><strong>Tasks:</strong> ${milestone.tasks.join(', ')}</p>`;
                }
                html += `</div>`;
            });
        }
        
        planContent.innerHTML = html;
        results.scrollIntoView({ behavior: 'smooth' });
    }

    // Export plan
    exportBtn.addEventListener('click', function() {
        const content = planContent.textContent;
        const blob = new Blob([content], { type: 'text/plain' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `project_plan_${new Date().toISOString().slice(0,10)}.txt`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    });

    // ============================================
    // PROGRESS REPORT SECTION
    // ============================================

    const reportBtn = document.getElementById('reportBtn');
    const reportProcessing = document.getElementById('reportProcessing');
    const reportResults = document.getElementById('reportResults');
    const reportContent = document.getElementById('reportContent');
    const reportProgressLog = document.getElementById('reportProgressLog');
    const exportReportBtn = document.getElementById('exportReportBtn');

    function updateReportAgentStatus(status, message) {
        const statusMap = {
            'idle': { agent1: '⏳ Data Collection: Idle', agent2: '⏳ Analysis Agent: Idle' },
            'collecting': { agent1: '📊 Data Collection: Fetching Trello data...', agent2: '⏳ Analysis Agent: Waiting' },
            'analyzing': { agent1: '✅ Data Collection: Complete', agent2: '📊 Analysis Agent: Analyzing data...' },
            'reporting': { agent1: '✅ Data Collection: Complete', agent2: '📋 Analysis Agent: Generating report...' },
            'complete': { agent1: '✅ Data Collection: Complete', agent2: '✅ Analysis Agent: Complete' },
            'error': { agent1: '❌ Data Collection: Error', agent2: '❌ Analysis Agent: Error' }
        };

        const statuses = statusMap[status] || statusMap.idle;
        document.getElementById('reportAgent1').textContent = statuses.agent1;
        document.getElementById('reportAgent2').textContent = statuses.agent2;
        
        if (message) {
            const logEntry = document.createElement('div');
            logEntry.textContent = `🔄 ${new Date().toLocaleTimeString()}: ${message}`;
            reportProgressLog.appendChild(logEntry);
            reportProgressLog.scrollTop = reportProgressLog.scrollHeight;
        }
    }

    // Generate progress report
    reportBtn.addEventListener('click', async function() {
        reportProcessing.classList.remove('hidden');
        reportResults.classList.add('hidden');
        reportProgressLog.innerHTML = '';
        reportBtn.disabled = true;
        reportBtn.textContent = 'Generating...';
        
        updateReportAgentStatus('idle', 'Starting progress report generation...');

        try {
            updateReportAgentStatus('collecting', 'Fetching data from Trello...');
            
            const response = await fetch('/api/progress-report', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            const result = await response.json();

            if (response.ok && result.status === 'success') {
                updateReportAgentStatus('complete', '✅ Progress report generated successfully!');
                displayReport(result.result);
            } else {
                updateReportAgentStatus('error', `❌ Error: ${result.error || 'Unknown error'}`);
                alert(`Error: ${result.error || 'Failed to generate report'}`);
            }
        } catch (error) {
            console.error('Error:', error);
            updateReportAgentStatus('error', `❌ Network error: ${error.message}`);
            alert('Error generating report. Please try again.');
        } finally {
            reportProcessing.classList.add('hidden');
            reportBtn.disabled = false;
            reportBtn.textContent = '📊 Generate Progress Report';
        }
    });

    // Display report
    function displayReport(reportData) {
        reportResults.classList.remove('hidden');
        
        let html = '';
        const report = reportData.report || reportData.raw_result || 'No report content available';
        
        // Convert markdown to HTML
        html = report
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/^# (.*$)/gm, '<h1>$1</h1>')
            .replace(/^## (.*$)/gm, '<h2>$1</h2>')
            .replace(/^### (.*$)/gm, '<h3>$1</h3>')
            .replace(/^#### (.*$)/gm, '<h4>$1</h4>')
            .replace(/^\* (.*$)/gm, '<li>$1</li>')
            .replace(/^- (.*$)/gm, '<li>$1</li>')
            .replace(/\n/g, '<br>');
        
        // Wrap lists
        html = html.replace(/(<li>.*<\/li>)/gs, '<ul>$1</ul>');
        
        reportContent.innerHTML = html;
        reportResults.scrollIntoView({ behavior: 'smooth' });
    }

    // Export report
    exportReportBtn.addEventListener('click', function() {
        const content = reportContent.textContent;
        const blob = new Blob([content], { type: 'text/plain' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `progress_report_${new Date().toISOString().slice(0,10)}.txt`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    });

    // Initialize
    loadModels();
    updateAgentStatus('idle', 'Ready to plan your project!');
    updateReportAgentStatus('idle', 'Ready to generate progress reports!');
    console.log('📋 Project Planning & Progress Reporting System loaded successfully!');
});