<template>
  <div class="d-flex min-vh-100 bg-light">
    <!-- Sidebar -->
    <div class="bg-white border-end border-2 border-secondary d-flex flex-column" style="width: 250px;">
      <div class="border-bottom border-2 border-secondary p-4 text-center">
        <div class="bg-secondary-subtle rounded d-flex align-items-center justify-content-center mx-auto mb-2" style="width: 60px; height: 60px;">
          <span class="text-secondary fw-bold">LOGO</span>
        </div>
        <h5 class="text-dark mb-0">Customer Portal</h5>
        <small class="text-secondary">John Doe</small>
      </div>

      <div class="flex-grow-1 p-3 d-grid gap-2">
        <button class="btn border-2 text-start border-secondary text-dark" @click="$emit('go-back')">Dashboard</button>
        <button class="btn border-2 text-start bg-dark text-white border-dark">Beneficiaries</button>
      </div>

      <div class="border-top border-2 border-secondary p-3">
        <button class="btn btn-outline-secondary w-100" @click="$emit('go-back')">Logout</button>
      </div>
    </div>

    <!-- Main Content -->
    <div class="flex-grow-1">
      <!-- Header -->
      <div class="border-bottom border-2 border-secondary bg-white p-4 d-flex justify-content-between align-items-center">
        <div>
          <h2 class="text-dark mb-1">Beneficiary Management</h2>
          <p class="text-secondary mb-0">Manage your saved beneficiaries</p>
        </div>
        <button class="btn btn-dark d-flex align-items-center gap-2" @click="showAddModal = true">
          ➕ Add Beneficiary
        </button>
      </div>

      <!-- Beneficiary Table -->
      <div class="p-4">
        <div class="bg-white border border-2 border-secondary">
          <div class="row fw-semibold bg-light border-bottom border-2 border-secondary py-3 px-2">
            <div class="col">Name</div>
            <div class="col">Account Number</div>
            <div class="col">Bank Name</div>
            <div class="col">Status</div>
            <div class="col text-end">Actions</div>
          </div>

          <div
            v-for="b in beneficiaries"
            :key="b.id"
            class="row align-items-center border-bottom py-3 px-2"
          >
            <div class="col">{{ b.name }}</div>
            <div class="col text-secondary">{{ b.account }}</div>
            <div class="col text-secondary">{{ b.bank }}</div>
            <div class="col">
              <span class="badge bg-secondary-subtle text-dark border border-secondary">Active</span>
            </div>
            <div class="col text-end">
              <button class="btn btn-outline-secondary btn-sm me-2" @click="editBeneficiary(b)">✏️</button>
              <button class="btn btn-outline-danger btn-sm" @click="deleteBeneficiary(b)">🗑️</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Modal -->
    <div v-if="showAddModal" class="modal-backdrop">
      <div class="modal-box">
        <h4>Add New Beneficiary</h4>
        <div class="mb-3">
          <label>Name</label>
          <input v-model="newBeneficiary.name" class="form-control border border-2 border-secondary" />
        </div>
        <div class="mb-3">
          <label>Account Number</label>
          <input v-model="newBeneficiary.account" class="form-control border border-2 border-secondary" />
        </div>
        <div class="mb-3">
          <label>Bank Name</label>
          <input v-model="newBeneficiary.bank" class="form-control border border-2 border-secondary" />
        </div>

        <div class="d-flex justify-content-end gap-2 mt-3">
          <button class="btn btn-outline-secondary" @click="showAddModal = false">Cancel</button>
          <button class="btn btn-dark" @click="addBeneficiary">Add</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const beneficiaries = ref([
  { id: 1, name: 'Alice Johnson', account: '****5678', bank: 'Bank of America' },
  { id: 2, name: 'Bob Smith', account: '****9012', bank: 'Chase Bank' },
  { id: 3, name: 'Carol Williams', account: '****3456', bank: 'Wells Fargo' },
])

const showAddModal = ref(false)
const newBeneficiary = ref({ name: '', account: '', bank: '' })

function addBeneficiary() {
  if (!newBeneficiary.value.name || !newBeneficiary.value.account || !newBeneficiary.value.bank) {
    alert('Please fill all fields')
    return
  }
  beneficiaries.value.push({
    id: Date.now(),
    ...newBeneficiary.value,
  })
  newBeneficiary.value = { name: '', account: '', bank: '' }
  showAddModal.value = false
}

function editBeneficiary(b) {
  alert(`Edit Beneficiary: ${b.name}`)
}

function deleteBeneficiary(b) {
  beneficiaries.value = beneficiaries.value.filter(item => item.id !== b.id)
}
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}
.modal-box {
  background: white;
  padding: 2rem;
  border: 2px solid #6c757d;
  border-radius: 8px;
  width: 400px;
}
</style>