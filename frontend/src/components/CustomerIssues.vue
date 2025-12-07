<template>
  <div class="dashboard-container p-4">
    <!-- Issue Resolution Section -->
    <section class="issues-section">
      <h2>Customer Issue Resolution</h2>

      <!-- Loading -->
      <div v-if="loadingIssues" class="loading">
        <div class="spinner"></div>
        <p>Loading issues...</p>
      </div>

      <!-- If No Issues -->
      <div v-else-if="issues.length === 0" class="empty-state">
        <p>No customer issues pending!</p>
      </div>

      <!-- Issues List -->
      <div v-else class="issue-list">
        <div
          class="issue-item"
          :class="getIssueStatusClass(issue.status)"
          v-for="issue in issues"
          :key="issue.id"
        >
          <div class="issue-info">
            <div class="issue-header">
              <p class="issue-title">{{ issue.title }}</p>
              <span :class="['issue-status-badge', isIssueResolved(issue.status) ? 'resolved' : 'pending']">
                {{ isIssueResolved(issue.status) ? 'Resolved' : 'Pending' }}
              </span>
            </div>
            <p class="issue-desc">{{ issue.description }}</p>
            <p class="issue-cust">Customer ID: <strong>{{ issue.customer_id }}</strong></p>
            <p class="issue-date">{{ formatDate(issue.created_date) }}</p>
          </div>

          <!-- Buttons - Only show if status is pending -->
          <div v-if="!isIssueResolved(issue.status)" class="issue-actions">
            <button class="action-btn ai-btn" @click="analyzeIssue(issue.id)">
              AI Draft Reply
            </button>

            <button class="action-btn resolve-btn" @click="markIssueResolved(issue.id)">
              Mark Resolved
            </button>
          </div>

          <!-- AI Output - Only show if status is pending -->
          <div v-if="!isIssueResolved(issue.status) && selectedIssueId === issue.id" class="ai-output-box">
            <h4>AI Suggested Reply</h4>
            <p>{{ aiDraft }}</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

const issues = ref([]);
const loadingIssues = ref(true);
const selectedIssueId = ref(null);
const aiDraft = ref("");

const formatDate = (dateString) => {
  if (!dateString) return 'N/A';
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
};

// Fetch Issues
const fetchIssues = async () => {
  try {
    loadingIssues.value = true;
    const res = await fetch("http://127.0.0.1:5000/api/issue/get");
    if (!res.ok) throw new Error("Failed to load issues");
    issues.value = await res.json();
  } catch (err) {
    console.error("Issue fetch error", err);
  } finally {
    loadingIssues.value = false;
  }
};

// AI Draft Call
const analyzeIssue = async (issueId) => {
  selectedIssueId.value = issueId;
  aiDraft.value = "Loading AI response...";

  try {
    const res = await fetch(
      `http://127.0.0.1:5000/api/employee/draft-dispute/${issueId}`
    );
    const data = await res.json();
    aiDraft.value = data.suggested_response;
  } catch (err) {
    aiDraft.value = "Error generating AI draft.";
  }
};

// Mark Resolved
const markIssueResolved = async (issueId) => {
  try {
    const res = await fetch(
      `http://127.0.0.1:5000/api/issue/update/${issueId}`,
      { method: "PUT" }
    );

    if (!res.ok) throw new Error("Unable to resolve issue");

    // Update the issue status locally immediately
    const issue = issues.value.find(i => i.id === issueId);
    if (issue) {
      issue.status = "complete";
    }
    
    // Clear AI draft if it was shown for this issue
    if (selectedIssueId.value === issueId) {
      selectedIssueId.value = null;
      aiDraft.value = "";
    }
    
    // Refresh to get latest data
    fetchIssues();
  } catch (err) {
    alert("Error resolving issue");
  }
};

// Normalize issue status for comparison
const isIssueResolved = (status) => {
  if (!status) return false;
  return status.toLowerCase() === 'complete' || status.toLowerCase() === 'resolved';
};

// Get CSS class for issue status
const getIssueStatusClass = (status) => {
  return isIssueResolved(status) ? 'issue-resolved' : 'issue-pending';
};

onMounted(() => {
  fetchIssues();
});
</script>

<style scoped>
.dashboard-container {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  min-height: 100vh;
  color: #333;
}

.issues-section {
  margin-top: 40px;
  padding: 20px;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.issues-section h2 {
  font-size: 1.8rem;
  color: #4a90e2;
  margin-bottom: 20px;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #4a90e2;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty-state {
  padding: 60px;
  text-align: center;
  font-size: 1.3rem;
  color: #666;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.issue-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.issue-item {
  padding: 18px;
  background: #fafafa;
  border-left: 5px solid #e67e22;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.issue-item.issue-pending {
  background: #fff4e6;
  border-left-color: #ff9800;
}

.issue-item.issue-resolved {
  background: #e8f5e9;
  border-left-color: #4caf50;
}

.issue-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.issue-title {
  font-size: 1.2rem;
  font-weight: 700;
  margin: 0;
  flex: 1;
}

.issue-status-badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

.issue-status-badge.resolved {
  background-color: #4caf50;
  color: white;
}

.issue-status-badge.pending {
  background-color: #ff9800;
  color: white;
}

.issue-desc {
  margin: 5px 0;
  color: #444;
}

.issue-actions {
  margin-top: 10px;
  display: flex;
  gap: 15px;
}

.action-btn {
  padding: 8px 14px;
  border-radius: 6px;
  font-weight: 600;
  border: none;
  cursor: pointer;
}

.ai-btn {
  background: #3498db;
  color: white;
}

.resolve-btn {
  background: #27ae60;
  color: white;
}

.ai-output-box {
  margin-top: 15px;
  padding: 12px;
  background: #eef6ff;
  border-left: 4px solid #2980b9;
  border-radius: 6px;
}
</style>

