<template>
  <div class="dashboard-container">
    
    <div class="motivational-alert-bar">
      <div class="scroll-text">
        <p>
          🎉 **Congratulations, Alex!** You're the Top Performer of the Week! | 🏆 **Team Goal:** Resolve 100 cases by Friday. Current: 65/100 | 🔔 **System Update:** Maintenance scheduled tonight at 2:00 AM.
        </p>
      </div>
    </div>
    
    <header class="dashboard-header">
      <h1><span class="emoji">🚀</span> Employee Productivity Hub</h1>
    </header>

    <section class="stats-grid">
      <div class="stat-card pending">
        <span class="stat-value">{{ pendingTasksCount }}</span>
        <span class="stat-label">Pending Tasks</span>
      </div>
      <div class="stat-card completed">
        <span class="stat-value">2</span> <span class="stat-label">Completed Today</span>
      </div>
      <div class="stat-card verifications">
        <span class="stat-value">{{ kycVerifications.length }}</span>
        <span class="stat-label">KYC Verifications</span>
      </div>
      <div class="stat-card priority">
        <span class="stat-value">{{ highPriorityCount }}</span>
        <span class="stat-label">High Priority</span>
      </div>
    </section>

    <div class="tabs-navigation">
      <button :class="{ active: tab === 'tasks' }" @click="tab = 'tasks'">
        <span class="emoji">📝</span> My Tasks
      </button>
      <button :class="{ active: tab === 'kyc' }" @click="tab = 'kyc'">
        <span class="emoji">🆔</span> KYC Verification
      </button>
      <button :class="{ active: tab === 'disputes' }" @click="tab = 'disputes'">
        <span class="emoji">⚖️</span> Dispute Resolution
      </button>
    </div>

    <main class="content-section">
      <div v-if="tab === 'tasks'" class="task-list">
        <h2>Outstanding Actions</h2>
        <div
          class="task-item"
          :class="task.priority"
          v-for="task in tasks"
          :key="task.id"
        >
          <div class="task-details">
            <p class="task-title">
              **{{ task.title }}**
            </p>
            <p class="task-customer">
              Customer: **{{ task.customer }}**
            </p>
          </div>
          <div class="task-meta">
            <p class="task-due">
              <span class="emoji">🗓️</span> Due: **{{ task.due }}**
            </p>
            <span :class="['priority-tag', task.priority]">{{
              task.priority.toUpperCase()
            }}</span>
            <button class="complete-btn action-btn">
              <span class="emoji">✅</span> Complete
            </button>
          </div>
        </div>
      </div>

      <div v-else-if="tab === 'kyc'" class="task-list">
        <h2>KYC Review Queue ({{ kycVerifications.length }} items)</h2>
        <div
          class="task-item"
          :class="kyc.priority"
          v-for="kyc in kycVerifications"
          :key="kyc.id"
        >
          <div class="task-details">
            <p class="task-title">
              **Verification for {{ kyc.customer }}**
            </p>
            <p class="task-customer">
              Document Type: **{{ kyc.type }}** | Status: **{{ kyc.status }}**
            </p>
          </div>
          <div class="task-meta kyc-meta">
            <p class="task-due">
              <span class="emoji">⏱️</span> Submitted: **{{ kyc.submitted }}**
            </p>
            <span :class="['priority-tag', kyc.priority]">{{
              kyc.priority.toUpperCase()
            }}</span>
            <button class="complete-btn review-btn">
              <span class="emoji">🔍</span> Review Documents
            </button>
          </div>
        </div>
      </div>

      <div v-else-if="tab === 'disputes'" class="task-list">
        <h2>Active Dispute Cases ({{ disputes.length }} cases)</h2>
        <div
          class="task-item"
          :class="dispute.priority"
          v-for="dispute in disputes"
          :key="dispute.id"
        >
          <div class="task-details">
            <p class="task-title">
              Case: **{{ dispute.case }}**
            </p>
            <p class="task-customer">
              Customer: **{{ dispute.customer }}** | Amount: **${{ dispute.amount.toFixed(2) }}**
            </p>
          </div>
          <div class="task-meta dispute-meta">
            <p class="task-due">
              <span class="emoji">📅</span> Filed: **{{ dispute.filed }}**
            </p>
            <span class="status-tag dispute-status">{{ dispute.status }}</span>
            <span :class="['priority-tag', dispute.priority]">{{
              dispute.priority.toUpperCase()
            }}</span>
            <button class="complete-btn action-btn">
              <span class="emoji">➡️</span> View Case
            </button>
          </div>
        </div>
      </div>

      <div v-else class="empty-state">
        <p>No data available for the selected section. Choose a tab above.</p>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";

const tab = ref("tasks");

// --- Dummy Data ---
const tasks = [
  { id: 1, title: "Process loan application", customer: "John Doe", due: "2025-10-16", priority: "high" },
  { id: 2, title: "Update customer KYC", customer: "Alice Smith", due: "2025-10-17", priority: "medium" },
  { id: 3, title: "Resolve complaint ticket", customer: "Bob Johnson", due: "2025-10-15", priority: "high" },
  { id: 4, title: "Review escalated refund", customer: "Eve Miller", due: "2025-10-18", priority: "low" },
];

const kycVerifications = [
  { id: 101, customer: "Michael Brown", submitted: "2025-11-04", status: "Review Required", type: "ID Proof", priority: "medium" },
  { id: 102, customer: "Sarah Connor", submitted: "2025-11-03", status: "Address Mismatch", type: "Address Proof", priority: "high" },
  { id: 103, customer: "David Lee", submitted: "2025-11-05", status: "Pending Upload", type: "Passport", priority: "low" },
];

const disputes = [
  { id: 201, case: "Unauthorized Transaction", customer: "Jennifer White", filed: "2025-11-02", amount: 450.00, status: "Investigating", priority: "high" },
  { id: 202, case: "Service Cancellation Fee", customer: "Thomas Green", filed: "2025-10-30", amount: 50.00, status: "Awaiting Customer Response", priority: "medium" },
];

// --- Computed Properties for Stats Grid ---
const pendingTasksCount = computed(() => tasks.length);
const highPriorityCount = computed(() => tasks.filter(t => t.priority === 'high').length + disputes.filter(d => d.priority === 'high').length);
</script>

<style scoped>
/* --- Design Variables and Global Styles --- */
:root {
  --primary-color: #4a90e2; /* Modern Blue */
  --secondary-color: #50e3c2; /* Teal/Mint Accent */
  --bg-color: #f4f7f6; /* Light, calming background */
  --card-bg: #ffffff;
  --text-color: #333;
  --shadow-light: 0 4px 12px rgba(0, 0, 0, 0.08);
  --high-priority: #e74c3c; /* Red */
  --medium-priority: #f39c12; /* Orange */
  --low-priority: #2ecc71; /* Green */
}

.dashboard-container {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  padding: 30px;
  background-color: var(--bg-color);
  min-height: 100vh;
  color: var(--text-color);
}

/* --- Motivational Alert (Moving Notification) --- */
.motivational-alert-bar {
  background-color: var(--secondary-color); /* Teal/Mint background */
  color: var(--text-color);
  padding: 8px 0;
  margin-bottom: 25px;
  overflow: hidden;
  white-space: nowrap;
  border-radius: 6px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.motivational-alert-bar .scroll-text {
  display: inline-block;
  padding-left: 100%;
  animation: scroll-left 50s linear infinite; /* Adjusted speed for longer text */
}

.motivational-alert-bar p {
  margin: 0;
  font-weight: 600;
  color: #1f3a93; /* Darker, professional text */
}

@keyframes scroll-left {
  0% {
    transform: translateX(0%);
  }
  100% {
    transform: translateX(-100%);
  }
}

/* --- Header Styling --- */
.dashboard-header h1 {
  font-size: 2.2rem;
  font-weight: 700;
  color: var(--primary-color);
  border-bottom: 3px solid var(--secondary-color);
  padding-bottom: 10px;
  margin-bottom: 30px;
}

.emoji {
  margin-right: 8px;
}

/* --- Stats Grid Styling (Same as previous, clean design) --- */
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
  flex-direction: column;
  align-items: center;
  transition: transform 0.3s ease;
  border-top: 5px solid;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.12);
}

.stat-value {
  font-size: 2.5rem;
  font-weight: 800;
  margin-bottom: 5px;
  color: var(--primary-color);
}

.stat-label {
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #7f8c8d;
}

.stat-card.pending { border-top-color: var(--high-priority); }
.stat-card.completed { border-top-color: var(--low-priority); }
.stat-card.verifications { border-top-color: var(--secondary-color); }
.stat-card.priority { border-top-color: var(--medium-priority); }


/* --- Tabs Styling (Same as previous, clean design) --- */
.tabs-navigation {
  display: flex;
  gap: 10px;
  margin-bottom: 25px;
  border-bottom: 2px solid #ddd;
}

.tabs-navigation button {
  padding: 12px 20px;
  border: none;
  background-color: transparent;
  color: #666;
  font-size: 1.05rem;
  cursor: pointer;
  transition: all 0.3s ease;
  border-bottom: 3px solid transparent;
  font-weight: 600;
}

.tabs-navigation button.active {
  color: var(--primary-color);
  border-bottom-color: var(--primary-color);
  background-color: #eaf1f8;
}

/* --- Task List Styling (Consistent Look for all tab content) --- */
.content-section h2 {
    font-size: 1.8rem;
    color: var(--primary-color);
    margin-bottom: 20px;
}

.task-list {
  display: grid;
  gap: 15px;
}

.task-item {
  background: var(--card-bg);
  padding: 18px 25px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: all 0.3s ease;
  border-left: 6px solid #ccc;
}

.task-item:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-light);
}

.task-item.high { border-left-color: var(--high-priority); }
.task-item.medium { border-left-color: var(--medium-priority); }
.task-item.low { border-left-color: var(--low-priority); }

.task-details {
  flex-grow: 1;
}

.task-title {
  font-size: 1.15rem;
  font-weight: 700;
  margin-bottom: 4px;
}

.task-customer {
  font-size: 0.9rem;
  color: #888;
}

.task-meta {
  display: flex;
  align-items: center;
  gap: 25px;
}

.task-due {
  font-size: 0.95rem;
  color: #555;
  font-weight: 500;
}

/* --- Priority Tag Styling --- */
.priority-tag {
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.5px;
  color: var(--card-bg);
}

.priority-tag.high { background-color: var(--high-priority); }
.priority-tag.medium { background-color: var(--medium-priority); }
.priority-tag.low { background-color: var(--low-priority); }

/* --- Button Styling (Adjusted for consistency) --- */
.complete-btn {
  /* Default action button style */
  background-color: var(--primary-color);
  color: var(--card-bg);
  padding: 8px 15px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: background-color 0.3s ease, transform 0.1s;
}

.complete-btn:hover {
  background-color: #397bc7; /* Slightly darker primary color */
}

.complete-btn:active {
  transform: scale(0.98);
}
</style>