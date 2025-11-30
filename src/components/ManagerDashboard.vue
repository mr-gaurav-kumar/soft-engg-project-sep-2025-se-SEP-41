<template>
  <div class="manager-dashboard-container">
    <header class="dashboard-header">
      <h1><span class="emoji">📊</span> Management & Oversight Hub</h1>
      <p class="text-muted">High-level performance metrics and task assignments.</p>
    </header>

    ---

    <section class="stats-grid">
      <div class="stat-card team-members">
        <div class="icon-box"><i class="bi bi-people-fill"></i></div>
        <div class="stat-content">
          <span class="stat-label">Team Members</span>
          <span class="stat-value">12</span>
        </div>
      </div>
      <div class="stat-card completed-tasks">
        <div class="icon-box"><i class="bi bi-check-circle-fill"></i></div>
        <div class="stat-content">
          <span class="stat-label">Tasks Completed</span>
          <span class="stat-value">176</span>
        </div>
      </div>
      <div class="stat-card pending-tasks">
        <div class="icon-box"><i class="bi bi-clock-fill"></i></div>
        <div class="stat-content">
          <span class="stat-label">Pending Tasks</span>
          <span class="stat-value">34</span>
        </div>
      </div>
      <div class="stat-card efficiency">
        <div class="icon-box"><i class="bi bi-lightning-fill"></i></div>
        <div class="stat-content">
          <span class="stat-label">Avg Efficiency</span>
          <span class="stat-value">87%</span>
        </div>
      </div>
    </section>

    ---

    <section class="charts-section">
      <div class="chart-panel small-chart">
        <h4 class="chart-title">Task Performance (Weekly)</h4>
        <canvas id="barChart"></canvas>
      </div>

      <div class="chart-panel small-chart">
        <h4 class="chart-title">Verification Statistics</h4>
        <canvas id="pieChart"></canvas>
      </div>
    </section>

    <div class="chart-panel full-chart">
      <h4 class="chart-title">Task Completion Rate – Monthly Trend</h4>
      <canvas id="lineChart"></canvas>
    </div>

    ---

    <div class="row-panels">
        <div class="panel active-tasks-panel">
          <h3><span class="emoji">📝</span> Active Tasks ({{ tasks.length }})</h3>
          <div class="task-list">
            <div v-for="(task, index) in tasks" :key="index" :class="['task-item', task.priority]">
              <div class="task-header">
                <strong class="task-title">{{ task.title }}</strong>
                <span :class="['priority-tag', task.priority]">{{ task.priority.toUpperCase() }}</span>
              </div>
              <p class="task-meta">Customer: **{{ task.customer }}**</p>
              <p class="task-meta">Assigned To: **{{ task.assignedTo }}**</p>
              <p class="task-due"><i class="bi bi-calendar-check me-1"></i> Due: {{ task.due }}</p>
            </div>
          </div>
        </div>

        <div class="panel create-task-panel">
          <h3><span class="emoji">➕</span> Create & Assign Task</h3>
          <form @submit.prevent="createTask">
            <div class="form-group">
              <label for="title">Task Title</label>
              <input id="title" v-model="newTask.title" placeholder="e.g., Process payment dispute" required />
            </div>

            <div class="form-group">
              <label for="customer">Customer Name</label>
              <input id="customer" v-model="newTask.customer" placeholder="Enter customer name" required />
            </div>

            <div class="form-group">
              <label for="assignedTo">Assign To Employee</label>
              <select id="assignedTo" v-model="newTask.assignedTo" required>
                <option disabled value="">Select Employee</option>
                <option>Jane (8 pending tasks)</option>
                <option>Robert (5 pending tasks)</option>
                <option>Alex (2 pending tasks)</option>
              </select>
            </div>

            <div class="d-flex-split">
                <div class="form-group half-width">
                  <label for="priority">Priority</label>
                  <select id="priority" v-model="newTask.priority" required>
                    <option value="high">High</option>
                    <option value="medium">Medium</option>
                    <option value="low">Low</option>
                  </select>
                </div>
                <div class="form-group half-width">
                  <label for="due">Due Date</label>
                  <input id="due" type="date" v-model="newTask.due" required />
                </div>
            </div>

            <div class="form-group">
              <label for="description">Task Description</label>
              <textarea id="description" v-model="newTask.description" placeholder="Brief description of the required action..."></textarea>
            </div>

            <div class="actions">
              <button type="button" class="btn-secondary" @click="resetForm">Cancel</button>
              <button type="submit" class="btn-primary"><i class="bi bi-send-fill me-1"></i> Create & Assign Task</button>
            </div>
          </form>
        </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Chart from 'chart.js/auto'

// Dummy Data
const tasks = ref([
  { title: 'Process loan application', customer: 'John Doe', assignedTo: 'Jane', due: '2025-10-16', priority: 'high' },
  { title: 'Update customer KYC', customer: 'Alice Smith', assignedTo: 'Robert', due: '2025-10-17', priority: 'medium' },
  { title: 'Resolve complaint ticket', customer: 'Bob Johnson', assignedTo: 'Alex', due: '2025-10-15', priority: 'high' }
])

const newTask = ref({
  title: '',
  customer: '',
  assignedTo: '',
  priority: 'medium', // Use lowercase for consistency with task list styling
  due: '',
  description: ''
})

const resetForm = () => {
  newTask.value = { title: '', customer: '', assignedTo: '', priority: 'medium', due: '', description: '' }
}

const createTask = () => {
  tasks.value.push({ ...newTask.value })
  alert('Task created & assigned successfully!')
  resetForm()
}

// Chart setup
onMounted(() => {
  const primaryColor = '#4a90e2';
  const secondaryColor = '#50e3c2';
  const highColor = '#e74c3c';

  // Bar Chart (Task Performance)
  new Chart(document.getElementById('barChart'), {
    type: 'bar',
    data: {
      labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
      datasets: [{
        label: 'Tasks Completed',
        data: [12, 19, 8, 17, 14],
        backgroundColor: primaryColor,
        borderRadius: 4,
      }]
    },
    options: { responsive: true, scales: { y: { beginAtZero: true } } }
  })

  // Pie Chart (Verification Statistics)
  new Chart(document.getElementById('pieChart'), {
    type: 'doughnut',
    data: {
      labels: ['Approved', 'Pending', 'Rejected'],
      datasets: [{
        data: [63, 29, 8],
        backgroundColor: [secondaryColor, primaryColor, highColor],
      }]
    },
    options: { responsive: true, maintainAspectRatio: false }
  })

  // Line Chart (Task Completion Rate – Monthly Trend)
  new Chart(document.getElementById('lineChart'), {
    type: 'line',
    data: {
      labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
      datasets: [{
        label: 'Completion Rate (%)',
        data: [40, 50, 55, 65, 70, 80],
        borderColor: primaryColor,
        backgroundColor: 'rgba(74, 144, 226, 0.1)',
        tension: 0.3,
        fill: true,
      }]
    },
    options: { responsive: true, scales: { y: { beginAtZero: true, max: 100 } } }
  })
})
</script>

<style scoped>
/* --- Design Variables --- */
:root {
  --primary-color: #4a90e2; /* Modern Blue */
  --secondary-color: #50e3c2; /* Teal Accent */
  --bg-color: #f4f7f6; /* Light, calming background */
  --card-bg: #ffffff;
  --text-dark: #333;
  --shadow-light: 0 4px 12px rgba(0, 0, 0, 0.08);
  --high-priority: #e74c3c; /* Red */
  --medium-priority: #f39c12; /* Orange */
  --low-priority: #2ecc71; /* Green */
}

.manager-dashboard-container {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  padding: 30px;
  background-color: var(--bg-color);
  min-height: 100vh;
  color: var(--text-dark);
}

/* --- Header --- */
.dashboard-header {
  margin-bottom: 30px;
}
.dashboard-header h1 {
  font-size: 2rem;
  font-weight: 700;
  color: var(--primary-color);
  border-bottom: 2px solid #ddd;
  padding-bottom: 10px;
}
.emoji { margin-right: 8px; }

/* --- 1. Stats Grid --- */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background: var(--card-bg);
  padding: 20px;
  border-radius: 12px;
  box-shadow: var(--shadow-light);
  display: flex;
  align-items: center;
  gap: 15px;
  transition: transform 0.3s ease;
  border-left: 6px solid #ccc;
}
.stat-card:hover { transform: translateY(-3px); }

.icon-box {
  background-color: var(--primary-color);
  color: white;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
}

.stat-content {
    display: flex;
    flex-direction: column;
}
.stat-label {
    font-size: 0.9rem;
    color: #7f8c8d;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.stat-value {
    font-size: 1.8rem;
    font-weight: 700;
    color: var(--primary-color);
}

.team-members { border-left-color: var(--primary-color); }
.completed-tasks { border-left-color: var(--low-priority); }
.pending-tasks { border-left-color: var(--high-priority); }
.efficiency { border-left-color: var(--secondary-color); }

/* --- 2. Charts Section --- */
.charts-section {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}

.chart-panel {
  background: var(--card-bg);
  border-radius: 12px;
  padding: 20px;
  box-shadow: var(--shadow-light);
  border: 1px solid #eee;
}

.small-chart {
  flex: 1;
  max-height: 350px; /* Constrain height for smaller charts */
}

.full-chart {
    min-height: 350px;
}

.chart-title {
    font-size: 1.2rem;
    font-weight: 600;
    color: var(--text-dark);
    margin-bottom: 15px;
    border-bottom: 1px dashed #eee;
    padding-bottom: 10px;
}

/* --- 3. Task Panels (List & Create) --- */
.row-panels {
    display: grid;
    grid-template-columns: 1.2fr 1fr; /* Task list slightly wider than form */
    gap: 20px;
}

.panel {
    background: var(--card-bg);
    border-radius: 12px;
    padding: 25px;
    box-shadow: var(--shadow-light);
    border: 1px solid #eee;
}

.panel h3 {
    font-size: 1.5rem;
    color: var(--primary-color);
    margin-bottom: 20px;
    border-bottom: 1px solid #f0f0f0;
    padding-bottom: 10px;
}

/* Active Tasks List */
.task-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.task-item {
  background: #f7f9fa;
  padding: 15px;
  border-radius: 8px;
  border-left: 5px solid #ccc; /* Priority color via JS class */
}

.task-item.high { border-left-color: var(--high-priority); }
.task-item.medium { border-left-color: var(--medium-priority); }
.task-item.low { border-left-color: var(--low-priority); }

.task-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 5px;
}

.task-title {
    font-size: 1.05rem;
}

.task-meta, .task-due {
    font-size: 0.9rem;
    color: #666;
    margin-bottom: 2px;
}
.task-due {
    font-weight: 500;
}


/* Priority Tag Styling */
.priority-tag {
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.5px;
  color: white;
  line-height: 1;
}

.priority-tag.high { background-color: var(--high-priority); }
.priority-tag.medium { background-color: var(--medium-priority); }
.priority-tag.low { background-color: var(--low-priority); }

/* Task Creation Form */
.create-task-panel form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.form-group {
    display: flex;
    flex-direction: column;
}

label {
    font-weight: 600;
    margin-bottom: 5px;
    font-size: 0.95rem;
    color: var(--text-dark);
}

input, select, textarea {
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 6px;
    font-size: 1em;
    width: 100%;
    box-sizing: border-box;
}

textarea {
    resize: vertical;
    min-height: 80px;
}

.d-flex-split {
    display: flex;
    gap: 15px;
}

.half-width {
    flex: 1;
}

.actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

.btn-primary, .btn-secondary {
  border: none;
  padding: 10px 18px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: background-color 0.3s;
}

.btn-primary {
  background: var(--primary-color);
  color: white;
}
.btn-primary:hover {
  background: #397bc7;
}

.btn-secondary {
  background: #adb5bd;
  color: white;
}
.btn-secondary:hover {
  background: #868e96;
}
</style>