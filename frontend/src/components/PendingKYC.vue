<template>
  <div class="dashboard-container p-4">
    <!-- Pending KYC Section -->
    <section class="content-section">
      <h2>Pending KYC</h2>
      <div class="kyc-actions" style="display:flex;gap:12px;align-items:center;margin-bottom:12px;">
        <button class="retry-btn" @click="fetchPendingKyc" :disabled="loadingPending">
          {{ loadingPending ? 'Refreshing...' : 'Refresh Pending KYC' }}
        </button>
        <div v-if="pendingKyc.length === 0" style="color:#666">No pending KYC</div>
      </div>

      <div v-if="loadingPending" class="loading" style="padding:20px;">
        <div class="spinner"></div>
        <p>Loading pending KYC...</p>
      </div>

      <div v-else class="kyc-list">
        <div
          v-for="kyc in pendingKyc"
          :key="kyc.kyc_id"
          class="task-item"
          style="flex-direction:column;align-items:stretch;"
        >
          <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:12px;width:100%;">
            <div>
              <p style="font-weight:700;margin:0;">{{ kyc.customer_name }} <small style="color:#777">(#{{ kyc.customer_id }})</small></p>
              <p style="margin:4px 0;color:#555;font-size:0.95rem;">Submitted: <strong>{{ formatDate(kyc.submitted_at) }}</strong></p>
              <p style="margin:4px 0;color:#444;font-size:0.95rem;">
                Files:
                <span v-if="kyc.aadhaar_file">Aadhaar</span>
                <span v-if="kyc.pan_file">, PAN</span>
                <span v-if="kyc.photo_file">, Photo</span>
                <span v-if="kyc.signature_file">, Signature</span>
              </p>
            </div>

            <div style="display:flex;flex-direction:column;align-items:flex-end;gap:8px;">
              <div style="display:flex;gap:8px;">
                <button class="complete-btn" @click="analyzeKyc(kyc)" :disabled="kyc.analysisLoading">
                  <span v-if="kyc.analysisLoading">Analyzing...</span>
                  <span v-else>Analyze</span>
                </button>
                <button class="retry-btn" @click="viewFiles(kyc)">View</button>
              </div>
              <div v-if="kyc.ai_status" style="font-weight:700;margin-top:6px;">{{ kyc.ai_status }}</div>
            </div>
          </div>

          <!-- AI result -->
          <div v-if="kyc.aiResult" style="margin-top:12px;background:#f6fbff;padding:12px;border-radius:6px;border:1px dashed #d7edff;display:flex;gap:12px;">
            <div style="flex:1;">
              <strong>AI Remarks:</strong>
              <pre style="white-space:pre-wrap;margin:8px 0;font-size:0.95rem;color:#222;">{{ kyc.aiResult }}</pre>
            </div>

            <div style="width:240px;display:flex;flex-direction:column;gap:8px;">
              <textarea v-model="kyc.managerComment" placeholder="Optional comment..." style="width:100%;min-height:68px;padding:8px;border-radius:6px;border:1px solid #ddd;"></textarea>

              <div style="display:flex;gap:8px;justify-content:flex-end;">
                <button class="retry-btn" @click="rejectKyc(kyc)" :disabled="kyc.actionLoading">Reject</button>
                <button class="complete-btn" @click="approveKyc(kyc)" :disabled="kyc.actionLoading">Approve</button>
              </div>

              <div v-if="kyc.actionLoading" style="font-size:0.85rem;color:#666;">Processing...</div>
            </div>
          </div>

          <!-- waiting message -->
          <div v-else-if="kyc.analysisLoading" style="margin-top:12px;color:#777;">Waiting for AI response...</div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

const pendingKyc = ref([]);
const loadingPending = ref(false);
const BASE = 'http://127.0.0.1:5000';

const formatDate = (dateString) => {
  if (!dateString) return 'N/A';
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
};

const fetchPendingKyc = async () => {
  loadingPending.value = true;
  try {
    const res = await fetch(`${BASE}/manager/kyc/pending`);
    if (!res.ok) throw new Error('Failed to fetch pending KYC');
    const data = await res.json();
    pendingKyc.value = data.map(k => ({
      ...k,
      analysisLoading: false,
      actionLoading: false,
      aiResult: null,
      ai_status: null,
      managerComment: ''
    }));
  } catch (err) {
    console.error('fetchPendingKyc error', err);
    alert('Could not load pending KYC at this time.');
  } finally {
    loadingPending.value = false;
  }
};

const viewFiles = (kyc) => {
  const fileUrl = kyc.aadhaar_file || kyc.pan_file || kyc.photo_file || kyc.signature_file;
  if (!fileUrl) {
    alert('No file link available.');
    return;
  }
  const encodedPath = encodeURIComponent(fileUrl);
  const fullUrl = `${BASE}/profile/kyc_docs/${encodedPath}`;
  window.open(fullUrl, '_blank');
};

const analyzeKyc = async (kyc) => {
  if (!confirm(`Analyze KYC for ${kyc.customer_name} (#${kyc.customer_id})?`)) return;

  kyc.analysisLoading = true;
  kyc.aiResult = null;
  kyc.ai_status = null;

  try {
    const res = await fetch(`${BASE}/api/kyc/analyze/${kyc.kyc_id}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    });

    if (!res.ok) {
      const text = await res.text();
      throw new Error(`AI analyze failed: ${text}`);
    }

    const json = await res.json();
    kyc.aiResult = json.ai_remarks || 'No remarks returned';
    kyc.ai_status = json.ai_status || 'Unknown';
  } catch (err) {
    console.error('analyzeKyc error', err);
    alert('AI analysis failed. See console for details.');
  } finally {
    kyc.analysisLoading = false;
  }
};

const approveKyc = async (kyc) => {
  if (!confirm(`Approve KYC for ${kyc.customer_name} (#${kyc.customer_id})?`)) return;
  kyc.actionLoading = true;
  try {
    const payload = { comment: kyc.managerComment || '' };
    const res = await fetch(`${BASE}/manager/kyc/approve/${kyc.kyc_id}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (!res.ok) {
      const errText = await res.text();
      throw new Error(errText || 'Approve failed');
    }
    const json = await res.json();
    alert(`KYC approved: ${json.message || 'Success'}`);
    pendingKyc.value = pendingKyc.value.filter(p => p.kyc_id !== kyc.kyc_id);
  } catch (err) {
    console.error('approveKyc error', err);
    alert('Approve failed. Check console.');
  } finally {
    kyc.actionLoading = false;
  }
};

const rejectKyc = async (kyc) => {
  if (!confirm(`Reject KYC for ${kyc.customer_name} (#${kyc.customer_id})?`)) return;
  kyc.actionLoading = true;
  try {
    const payload = { comment: kyc.managerComment || '' };
    const res = await fetch(`${BASE}/manager/kyc/reject/${kyc.kyc_id}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (!res.ok) {
      const errText = await res.text();
      throw new Error(errText || 'Reject failed');
    }
    const json = await res.json();
    alert(`KYC rejected: ${json.message || 'Success'}`);
    pendingKyc.value = pendingKyc.value.filter(p => p.kyc_id !== kyc.kyc_id);
  } catch (err) {
    console.error('rejectKyc error', err);
    alert('Reject failed. Check console.');
  } finally {
    kyc.actionLoading = false;
  }
};

onMounted(() => {
  fetchPendingKyc();
});
</script>

<style scoped>
.dashboard-container {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  min-height: 100vh;
  color: #333;
}

.content-section h2 {
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

.retry-btn {
  background-color: #4a90e2;
  color: white;
  padding: 10px 25px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  font-size: 1rem;
  transition: background-color 0.3s ease;
}

.retry-btn:hover {
  background-color: #357abd;
}

.complete-btn {
  background-color: #4a90e2;
  color: white;
  padding: 8px 15px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: background-color 0.3s ease;
}

.complete-btn:hover {
  background-color: #357abd;
}

.kyc-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: 8px;
}

.task-item {
  background: #ffffff;
  padding: 18px 25px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}
</style>

