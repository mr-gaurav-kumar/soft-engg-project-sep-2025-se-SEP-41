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
        <button class="btn border-2 text-start bg-dark text-white border-dark">Transactions</button>
      </div>

      <div class="border-top border-2 border-secondary p-3">
        <button class="btn btn-outline-secondary w-100" @click="$emit('go-back')">Logout</button>
      </div>
    </div>

    <!-- Main Content -->
    <div class="flex-grow-1">
      <!-- Header -->
      <div class="border-bottom border-2 border-secondary bg-white p-4">
        <h2 class="text-dark mb-1">Transaction History & Insights</h2>
        <p class="text-secondary mb-0">View and analyze your transactions</p>
      </div>

      <div class="p-4 space-y-6">
        <!-- Filters -->
        <div class="bg-white border border-2 border-secondary p-4 mb-4">
          <h5 class="text-dark mb-3">Filters</h5>
          <div class="row g-3">
            <div class="col-md-3">
              <label class="form-label">Date Range</label>
              <select v-model="filters.dateRange" class="form-select border border-2 border-secondary">
                <option value="all">All Time</option>
                <option value="7days">Last 7 Days</option>
                <option value="30days">Last 30 Days</option>
                <option value="custom">Custom Range</option>
              </select>
            </div>
            <div class="col-md-3">
              <label class="form-label">Transaction Type</label>
              <select v-model="filters.type" class="form-select border border-2 border-secondary">
                <option value="all">All Types</option>
                <option value="debit">Debit</option>
                <option value="credit">Credit</option>
              </select>
            </div>
            <div class="col-md-3">
              <label class="form-label">Category</label>
              <select v-model="filters.category" class="form-select border border-2 border-secondary">
                <option value="all">All Categories</option>
                <option value="shopping">Shopping</option>
                <option value="bills">Bills</option>
                <option value="food">Food</option>
                <option value="transfer">Transfer</option>
              </select>
            </div>
            <div class="col-md-3">
              <label class="form-label">Search</label>
              <input v-model="filters.search" type="text" placeholder="Search transactions..." class="form-control border border-2 border-secondary" />
            </div>
          </div>
        </div>

        <!-- Spending Trends + Category Breakdown -->
        <div class="row g-4 mb-4">
          <div class="col-md-8">
            <div class="bg-white border border-2 border-secondary p-4">
              <div class="d-flex justify-content-between align-items-center mb-3">
                <h5 class="text-dark">Spending Trends</h5>
                <button class="btn btn-outline-secondary btn-sm">⬇️ Export</button>
              </div>

              <!-- Chart Placeholder -->
              <div class="h-64 border border-2 border-secondary bg-light d-flex align-items-end justify-around p-3">
                <div v-for="(height, idx) in [120, 160, 100, 180, 140, 80, 60]" :key="idx" class="d-flex flex-column align-items-center">
                  <div class="bg-secondary" :style="{ width: '40px', height: height + 'px' }"></div>
                  <small class="text-secondary">{{ days[idx] }}</small>
                </div>
              </div>
            </div>
          </div>

          <div class="col-md-4">
            <div class="bg-white border border-2 border-secondary p-4">
              <h5 class="text-dark mb-3">Category Breakdown</h5>
              <div class="d-flex justify-content-center align-items-center mb-4">
                <div class="rounded-circle border border-3 border-secondary d-flex justify-content-center align-items-center" style="width: 120px; height: 120px;">
                  <span class="text-secondary">PIE CHART</span>
                </div>
              </div>
              <div class="d-flex flex-column gap-2">
                <div v-for="(item, i) in breakdown" :key="i" class="d-flex justify-content-between border border-1 border-secondary p-2">
                  <div class="d-flex align-items-center gap-2">
                    <div class="rounded-circle" :style="{ width: '10px', height: '10px', background: item.color }"></div>
                    <span>{{ item.label }}</span>
                  </div>
                  <span>{{ item.amount }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Transactions Table -->
        <div class="bg-white border border-2 border-secondary">
          <div class="d-flex justify-content-between align-items-center border-bottom border-2 border-secondary p-4">
            <h5 class="text-dark mb-0">All Transactions</h5>
            <button class="btn btn-outline-secondary btn-sm">⬇️ Download Statement</button>
          </div>

          <div class="row bg-light fw-semibold border-bottom border-2 border-secondary py-2 px-3">
            <div class="col">Date</div>
            <div class="col">Description</div>
            <div class="col">Category</div>
            <div class="col">Type</div>
            <div class="col text-end">Amount</div>
          </div>

          <div
            v-for="t in filteredTransactions"
            :key="t.id"
            class="row align-items-center border-bottom border-secondary-subtle py-2 px-3 hover-bg-light"
          >
            <div class="col text-secondary">{{ t.date }}</div>
            <div class="col d-flex align-items-center gap-2">
              <div class="rounded-circle d-flex justify-content-center align-items-center" :class="t.type === 'debit' ? 'bg-light' : 'bg-secondary-subtle'" style="width: 28px; height: 28px;">
                <span>{{ t.type === 'debit' ? '⬆️' : '⬇️' }}</span>
              </div>
              <span class="text-dark">{{ t.description }}</span>
            </div>
            <div class="col">
              <span class="badge bg-light border border-1 border-secondary text-dark">{{ t.category }}</span>
            </div>
            <div class="col text-capitalize text-secondary">{{ t.type }}</div>
            <div class="col text-end" :class="t.type === 'debit' ? 'text-danger' : 'text-success'">
              {{ t.amount }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

const filters = ref({
  dateRange: 'all',
  type: 'all',
  category: 'all',
  search: ''
})

const transactions = ref([
  { id: 1, type: 'debit', description: 'Transfer to Alice Johnson', amount: '-$250.00', date: '2025-10-14', category: 'Transfer' },
  { id: 2, type: 'credit', description: 'Salary Deposit', amount: '+$3,500.00', date: '2025-10-13', category: 'Income' },
  { id: 3, type: 'debit', description: 'ATM Withdrawal', amount: '-$100.00', date: '2025-10-12', category: 'Cash' },
  { id: 4, type: 'debit', description: 'Online Shopping', amount: '-$85.50', date: '2025-10-11', category: 'Shopping' },
  { id: 5, type: 'credit', description: 'Refund - Store X', amount: '+$45.00', date: '2025-10-10', category: 'Refund' },
  { id: 6, type: 'debit', description: 'Utility Bill Payment', amount: '-$120.00', date: '2025-10-09', category: 'Bills' },
  { id: 7, type: 'debit', description: 'Restaurant', amount: '-$65.00', date: '2025-10-08', category: 'Food' },
  { id: 8, type: 'debit', description: 'Gas Station', amount: '-$50.00', date: '2025-10-07', category: 'Transport' },
])

const breakdown = ref([
  { label: 'Shopping', amount: '$335', color: '#6c757d' },
  { label: 'Bills', amount: '$220', color: '#adb5bd' },
  { label: 'Food', amount: '$165', color: '#dee2e6' },
])

const filteredTransactions = computed(() => {
  return transactions.value.filter(t => {
    const matchType = filters.value.type === 'all' || t.type === filters.value.type
    const matchCat = filters.value.category === 'all' || t.category.toLowerCase() === filters.value.category
    const matchSearch = !filters.value.search || t.description.toLowerCase().includes(filters.value.search.toLowerCase())
    return matchType && matchCat && matchSearch
  })
})
</script>

<style scoped>
.hover-bg-light:hover {
  background-color: #f8f9fa;
}
</style>