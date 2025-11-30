<template>
  <div class="d-flex min-vh-100 bg-light">
    <!-- Sidebar and Layout (simplified, same as CustomerDashboard) -->
    <div class="bg-white border-end border-2 border-secondary d-flex flex-column" style="width: 250px;">
      <div class="border-bottom border-2 border-secondary p-4 text-center">
        <div class="bg-secondary-subtle rounded d-flex align-items-center justify-content-center mx-auto mb-2" style="width: 60px; height: 60px;">
          <span class="text-secondary fw-bold">LOGO</span>
        </div>
        <h5 class="text-dark mb-0">Customer Portal</h5>
        <small class="text-secondary">John Doe</small>
      </div>

      <div class="flex-grow-1 p-3 d-grid gap-2">
        <router-link to="/" class="btn border-2 text-start text-dark border-secondary">Dashboard</router-link>
        <router-link to="/transfer" class="btn border-2 text-start bg-dark text-white border-dark">Transfer Money</router-link>
      </div>

      <div class="border-top border-2 border-secondary p-3">
        <button class="btn btn-outline-secondary w-100">Logout</button>
      </div>
    </div>

    <!-- Main Content -->
    <div class="flex-grow-1">
      <div class="border-bottom border-2 border-secondary bg-white p-4">
        <h2 class="text-dark mb-1">Money Transfer</h2>
        <p class="text-secondary mb-0">Send money to your beneficiaries</p>
      </div>

      <div class="p-4 d-flex justify-content-center">
        <div class="w-100" style="max-width: 700px;">
          <!-- Progress Steps -->
          <div class="bg-white border border-2 border-secondary p-4 mb-4 text-center">
            <div class="d-flex justify-content-between">
              <div class="flex-fill">
                <div :class="['rounded-circle border border-2 d-flex align-items-center justify-content-center mx-auto mb-2', currentStep === 'details' ? 'bg-dark text-white border-dark' : 'bg-white text-dark border-secondary']" style="width: 40px; height: 40px;">1</div>
                <small>Enter Details</small>
              </div>
              <div class="flex-fill">
                <div :class="['rounded-circle border border-2 d-flex align-items-center justify-content-center mx-auto mb-2', currentStep === 'otp' ? 'bg-dark text-white border-dark' : 'bg-white text-dark border-secondary']" style="width: 40px; height: 40px;">2</div>
                <small>Verify OTP</small>
              </div>
              <div class="flex-fill">
                <div :class="['rounded-circle border border-2 d-flex align-items-center justify-content-center mx-auto mb-2', currentStep === 'confirmation' ? 'bg-dark text-white border-dark' : 'bg-white text-dark border-secondary']" style="width: 40px; height: 40px;">3</div>
                <small>Confirm</small>
              </div>
            </div>
          </div>

          <!-- Steps -->
          <div class="bg-white border border-2 border-secondary p-4">
            <!-- Step 1 -->
            <div v-if="currentStep === 'details'" class="space-y-3">
              <h4>Transfer Details</h4>

              <div class="mb-3 text-start">
                <label class="form-label fw-semibold">Select Beneficiary</label>
                <select v-model="selectedBeneficiary" class="form-select border border-2 border-secondary">
                  <option value="">Choose Beneficiary</option>
                  <option v-for="b in beneficiaries" :key="b.id" :value="b.id">
                    {{ b.name }} - {{ b.account }}
                  </option>
                </select>
              </div>

              <div class="mb-3 text-start">
                <label class="form-label fw-semibold">Amount</label>
                <input v-model="amount" type="number" class="form-control border border-2 border-secondary" placeholder="Enter amount" />
                <small class="text-secondary">Available Balance: $12,458.75</small>
              </div>

              <div class="mb-3 text-start">
                <label class="form-label fw-semibold">Note (optional)</label>
                <input v-model="note" type="text" class="form-control border border-2 border-secondary" placeholder="Add a note" />
              </div>

              <button class="btn btn-dark w-100 py-2" @click="goToOTP">Proceed to Verify</button>
            </div>

            <!-- Step 2 -->
            <div v-else-if="currentStep === 'otp'" class="text-center">
              <h4>Verify OTP</h4>
              <p class="text-secondary">Enter the 6-digit code sent to your registered mobile number</p>

              <div class="d-flex justify-content-center mb-3">
                <input
                  v-model="otp"
                  type="text"
                  maxlength="6"
                  class="form-control text-center border border-2 border-secondary"
                  style="width: 200px; font-size: 24px; letter-spacing: 8px;"
                />
              </div>

              <button class="btn btn-link text-secondary">Resend OTP</button>

              <div class="d-flex gap-3 mt-3">
                <button class="btn btn-outline-secondary flex-fill" @click="currentStep = 'details'">Back</button>
                <button class="btn btn-dark flex-fill" @click="goToConfirmation">Verify & Continue</button>
              </div>
            </div>

            <!-- Step 3 -->
            <div v-else-if="currentStep === 'confirmation'" class="text-start">
              <h4>Confirm Transfer</h4>

              <div class="p-3 mb-3 bg-light border border-secondary rounded">
                <div class="d-flex justify-content-between"><span>From Account:</span><strong>**** **** 1234</strong></div>
                <div class="d-flex justify-content-between"><span>To:</span><strong>{{ selectedBeneficiaryName }}</strong></div>
                <div class="d-flex justify-content-between"><span>Amount:</span><strong>${{ amount || '0.00' }}</strong></div>
              </div>

              <div class="alert alert-warning border border-2 border-secondary">
                ⚠️ Please verify all details before confirming. This transaction cannot be reversed.
              </div>

              <div class="d-flex gap-3">
                <button class="btn btn-outline-secondary flex-fill" @click="currentStep = 'otp'">Back</button>
                <button class="btn btn-dark flex-fill" @click="confirmTransfer">Confirm Transfer</button>
              </div>
            </div>

            <!-- Step 4 -->
            <div v-else class="text-center py-5">
              <div class="bg-success-subtle border border-success d-inline-flex align-items-center justify-content-center rounded-circle mb-3" style="width: 80px; height: 80px;">
                ✅
              </div>
              <h4>Transfer Successful!</h4>
              <p class="text-secondary">Your transaction has been completed</p>

              <div class="p-3 bg-light border border-secondary rounded text-start mb-3">
                <div class="d-flex justify-content-between"><span>Transaction ID:</span><strong>TXN123456789</strong></div>
                <div class="d-flex justify-content-between"><span>Amount:</span><strong>${{ amount }}</strong></div>
                <div class="d-flex justify-content-between"><span>Date:</span><strong>Nov 5, 2025</strong></div>
              </div>

              <div class="d-flex gap-3">
                <router-link to="/" class="flex-fill text-decoration-none">
                  <button class="btn btn-outline-secondary w-100">Back to Dashboard</button>
                </router-link>
                <button class="btn btn-dark flex-fill" @click="resetForm">New Transfer</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const currentStep = ref('details')
const selectedBeneficiary = ref('')
const amount = ref('')
const note = ref('')
const otp = ref('')

const beneficiaries = [
  { id: '1', name: 'Alice Johnson', account: '****5678' },
  { id: '2', name: 'Bob Smith', account: '****9012' },
  { id: '3', name: 'Carol Williams', account: '****3456' },
]

const selectedBeneficiaryName = computed(() => {
  const ben = beneficiaries.find(b => b.id === selectedBeneficiary.value)
  return ben ? ben.name : 'N/A'
})

function goToOTP() {
  if (selectedBeneficiary.value && amount.value) {
    currentStep.value = 'otp'
  } else {
    alert('Please select a beneficiary and enter an amount')
  }
}

function goToConfirmation() {
  if (otp.value.length === 6) {
    currentStep.value = 'confirmation'
  } else {
    alert('Enter a valid 6-digit OTP')
  }
}

function confirmTransfer() {
  currentStep.value = 'success'
}

function resetForm() {
  selectedBeneficiary.value = ''
  amount.value = ''
  otp.value = ''
  note.value = ''
  currentStep.value = 'details'
}
</script>

<style scoped>
.space-y-3 > * + * {
  margin-top: 1rem;
}
</style>