<template>
  <div class="d-flex min-vh-100 banking-theme">
    <div class="sidebar d-flex flex-column">
      <div class="sidebar-header">
        <div class="logo-box">
          <span class="logo-text">SECURE</span>
        </div>
        <h5 class="text-white mb-0">Customer Portal</h5>
        <small class="text-info">John Doe</small>
      </div>

      <div class="flex-grow-1 p-3 nav-section">
        <div class="d-grid gap-2">
          <button
            v-for="item in navItems"
            :key="item.id"
            @click="navigate(item.path)"
            :class="[
              'nav-button',
              $route.path === item.path ? 'nav-active' : 'nav-inactive'
            ]"
          >
            <span class="d-flex align-items-center gap-2">
                <i :class="getIconClass(item.id)"></i>
                {{ item.label }}
            </span>
          </button>
        </div>
      </div>

      <div class="sidebar-footer">
        <BaseButton variant="outline-light" class="w-100" @click="handleLogout">
          <i class="bi bi-box-arrow-right me-2"></i> Logout
        </BaseButton>
      </div>
    </div>

    <div class="flex-grow-1 main-content-area">
      <div class="main-header">
        <h2 class="text-primary mb-1">Dashboard</h2>
        <p class="text-muted mb-0">Welcome back, **John Doe**</p>
      </div>

      <div class="p-4 dashboard-body">
        <div class="balance-card mb-4">
          <p class="text-muted mb-1">Available Balance</p>
          <h3 class="text-primary fw-bold">$12,458.75</h3>
          <p class="text-muted">Account Number: **** **** 1234</p>
        </div>

        <div class="row text-center mb-4 quick-actions-row">
          <div class="col-md-3 mb-3">
            <button class="action-btn" @click="$emit('go-to-transfer')">
              <i class="bi bi-arrow-left-right"></i>
              <span>Transfer Money</span>
            </button>
          </div>
          <div class="col-md-3 mb-3">
            <button class="action-btn" @click="$emit('go-to-beneficiary')">
              <i class="bi bi-person-plus"></i>
              <span>Add Beneficiary</span>
            </button>
          </div>
          <div class="col-md-3 mb-3">
            <button class="action-btn" @click="$emit('go-to-transactions')">
              <i class="bi bi-receipt"></i>
              <span>View Transactions</span>
            </button>
          </div>
          <div class="col-md-3 mb-3">
            <button class="action-btn" @click="$emit('go-to-aiassistant')">
              <i class="bi bi-robot"></i>
              <span>AI Assistant</span>
            </button>
          </div>
        </div>

        <div class="row">
          <div class="col-md-6 mb-4">
            <div class="card-section h-100">
              <div class="d-flex justify-content-between align-items-center mb-3">
                <h4 class="text-primary mb-0">Recent Transactions</h4>
                <BaseButton variant="outline" size="sm" @click="navigate('/history')">
                  View All <i class="bi bi-chevron-right ms-1"></i>
                </BaseButton>
              </div>

              <div class="transaction-list">
                <div
                  v-for="transaction in transactions"
                  :key="transaction.id"
                  class="transaction-item"
                >
                  <div>
                    <p class="mb-0 fw-semibold text-dark">{{ transaction.description }}</p>
                    <small class="text-muted">{{ transaction.date }}</small>
                  </div>
                  <span
                    :class="transaction.type === 'debit' ? 'text-danger fw-bold' : 'text-success fw-bold'"
                  >
                    {{ transaction.amount }}
                  </span>
                </div>
              </div>
            </div>
          </div>

          <div class="col-md-6 mb-4">
            <div class="card-section h-100">
              <h4 class="text-primary mb-3">Spending Summary</h4>

              <div class="d-flex flex-column align-items-center mb-4">
                <div class="chart-placeholder">
                  <span class="text-muted">PIE CHART</span>
                </div>
                <p class="text-muted mt-2">Monthly Spending Breakdown</p>
              </div>

              <div>
                <div class="spending-category" style="--cat-color: #4a90e2;">
                  <div class="d-flex align-items-center gap-2">
                    <div class="category-dot" style="background-color: #4a90e2;"></div>
                    <span>Shopping</span>
                  </div>
                  <span class="fw-semibold">45%</span>
                </div>

                <div class="spending-category" style="--cat-color: #50e3c2;">
                  <div class="d-flex align-items-center gap-2">
                    <div class="category-dot" style="background-color: #50e3c2;"></div>
                    <span>Bills & Utilities</span>
                  </div>
                  <span class="fw-semibold">30%</span>
                </div>

                <div class="spending-category" style="--cat-color: #f39c12;">
                  <div class="d-flex align-items-center gap-2">
                    <div class="category-dot" style="background-color: #f39c12;"></div>
                    <span>Food & Dining</span>
                  </div>
                  <span class="fw-semibold">25%</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'CustomerDashboard',
  setup() {
    const router = useRouter()

    const navItems = [
      { id: 'dashboard', label: 'Dashboard', path: '/customer-dashboard' },
      { id: 'beneficiary', label: 'Beneficiaries', path: '/beneficiary' },
      { id: 'transfer', label: 'Transfer Money', path: '/transfer' },
      { id: 'history', label: 'Transactions', path: '/history' },
      { id: 'chatbot', label: 'AI Assistant', path: '/chatbot' },
    ]

    const transactions = ref([
      { id: 1, type: 'debit', description: 'Transfer to Alice Johnson', amount: '-$250.00', date: '2025-10-14' },
      { id: 2, type: 'credit', description: 'Salary Deposit', amount: '+$3,500.00', date: '2025-10-13' },
      { id: 3, type: 'debit', description: 'ATM Withdrawal', amount: '-$100.00', date: '2025-10-12' },
      { id: 4, type: 'debit', description: 'Online Shopping', amount: '-$85.50', date: '2025-10-11' },
      { id: 5, type: 'credit', description: 'Refund - Store X', amount: '+$45.00', date: '2025-10-10' },
    ])

    const navigate = (path) => {
      // Logic to check if the path is the current route is handled in the template
      // and only calls this function for navigation.
      // Assuming $route is available for comparison in the template.
      if (path && router) {
          router.push(path)
      }
    }

    const handleLogout = () => {
      router.push('/')
    }

    // Helper to map nav item IDs to Bootstrap Icons classes
    const getIconClass = (id) => {
        const icons = {
            dashboard: 'bi bi-grid-fill',
            beneficiary: 'bi bi-people-fill',
            transfer: 'bi bi-arrow-left-right',
            history: 'bi bi-clock-history',
            chatbot: 'bi bi-robot',
        }
        return icons[id] || 'bi bi-circle'; // Default icon
    }

    return { navItems, transactions, navigate, handleLogout, getIconClass }
  },
  components: {
    // Keeping BaseButton component definition local for completeness
    BaseButton: {
      props: {
        variant: { type: String, default: 'default' },
        size: { type: String, default: 'md' },
      },
      emits: ['click'],
      template: `
        <button
          :class="buttonClasses"
          @click="$emit('click', $event)"
        >
          <slot></slot>
        </button>
      `,
      computed: {
        buttonClasses() {
          const base = 'btn d-inline-flex align-items-center justify-content-center fw-semibold transition-all'
          const variants = {
            default: 'btn-primary text-white',
            outline: 'btn-outline-primary', // Changed to primary for theme
            'outline-light': 'btn-outline-light text-white', // New variant for dark sidebar
          }
          const sizes = {
            sm: 'btn-sm',
            md: '',
            lg: 'btn-lg',
          }
          return [base, variants[this.variant] || variants.default, sizes[this.size]].join(' ')
        }
      }
    }
  },
  emits: [
    'go-to-transfer', 
    'go-to-beneficiary', 
    'go-to-transactions', 
    'go-to-aiassistant'
  ]
}
</script>

<style scoped>
/* Import Bootstrap Icons (assuming it's linked in your main HTML/project) */
/* @import url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css"); */

/* --- Theme Variables --- */
:root {
  --primary-color: #1f3a93; /* Deep, professional blue */
  --secondary-color: #50e3c2; /* Teal accent */
  --sidebar-bg: #2c3e50; /* Dark, solid sidebar */
  --body-bg: #f4f7f6; /* Light, clean background */
  --card-bg: #ffffff;
  --text-dark: #34495e;
  --text-light: #ecf0f1;
  --shadow-subtle: 0 4px 12px rgba(0, 0, 0, 0.08);
  --shadow-sidebar: 2px 0 5px rgba(0, 0, 0, 0.2);
}

/* --- Global Layout/Theme Overrides --- */
.banking-theme {
    background-color: var(--body-bg) !important;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
.transition-all {
    transition: all 0.2s ease-in-out;
}

/* --- 1. Sidebar Styling --- */
.sidebar {
    width: 280px !important; /* Slightly wider sidebar */
    background-color: var(--sidebar-bg) !important;
    color: var(--text-light);
    box-shadow: var(--shadow-sidebar);
}

/* Sidebar Header */
.sidebar-header {
    padding: 30px 20px;
    text-align: center;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.logo-box {
    background-color: var(--primary-color);
    border-radius: 8px;
    width: 60px;
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 10px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
}

.logo-text {
    color: var(--secondary-color);
    font-weight: bold;
    font-size: 0.8rem;
}

.sidebar-header h5 {
    font-weight: 600;
}

/* Navigation Buttons */
.nav-section {
    padding-top: 20px !important;
}

.nav-button {
    text-align: left;
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 15px;
    margin-bottom: 8px;
    border-radius: 6px;
    border: none;
    font-size: 1.05rem;
    font-weight: 500;
    cursor: pointer;
    background: transparent;
    color: var(--text-light);
    transition: all 0.2s ease-in-out;
}

.nav-button:hover {
    background-color: rgba(255, 255, 255, 0.1);
}

.nav-active {
    background-color: var(--primary-color) !important;
    color: var(--text-light) !important;
    font-weight: 600 !important;
    box-shadow: var(--shadow-subtle);
}

/* Sidebar Footer */
.sidebar-footer {
    padding: 20px 15px !important;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
}

/* --- 2. Main Content Styling --- */

/* Main Header */
.main-header {
    background-color: var(--card-bg) !important;
    padding: 20px 30px !important;
    border-bottom: 3px solid var(--primary-color);
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05);
}
.main-header h2 {
    color: var(--primary-color) !important;
    font-weight: 700;
    font-size: 1.8rem;
}

.dashboard-body {
    padding: 30px !important;
}

/* Balance Card */
.balance-card {
    background-color: var(--primary-color) !important;
    color: white !important;
    padding: 30px !important;
    border-radius: 12px;
    box-shadow: var(--shadow-subtle);
    border: none !important;
    background-image: linear-gradient(135deg, #1f3a93 0%, #3b5998 100%);
}
.balance-card p, .balance-card h3 {
    color: white !important;
}
.balance-card h3 {
    font-size: 2.5rem;
    margin-bottom: 5px !important;
}

/* Quick Actions */
.action-btn {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;
    padding: 20px 10px;
    border: 1px solid #ddd;
    border-radius: 8px;
    background-color: var(--card-bg);
    color: var(--text-dark);
    font-weight: 600;
    box-shadow: var(--shadow-subtle);
    transition: all 0.3s ease;
}

.action-btn i {
    font-size: 1.8rem;
    margin-bottom: 8px;
    color: var(--primary-color);
}

.action-btn:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
    border-color: var(--primary-color);
}

/* Card Sections (Transactions/Spending) */
.card-section {
    background-color: var(--card-bg) !important;
    border-radius: 12px;
    padding: 25px !important;
    box-shadow: var(--shadow-subtle);
    border: 1px solid #eee !important;
}

/* Transactions List */
.transaction-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 0;
    border-bottom: 1px solid #f0f0f0;
}
.transaction-item:last-child {
    border-bottom: none;
}
.transaction-list {
    margin-top: 15px;
}

/* Spending Summary */
.chart-placeholder {
    width: 150px;
    height: 150px;
    border-radius: 50%;
    border: 8px dashed #ccc;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #f9f9f9;
}

.spending-category {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 10px;
    margin-bottom: 8px;
    border-radius: 4px;
    background-color: #f7f9fa;
    border-left: 5px solid var(--cat-color, #ccc);
}

.category-dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    margin-right: 5px;
}

/* Helper Class for BaseButton (updated variant for dark background) */
.btn-outline-light {
    border-color: rgba(255, 255, 255, 0.5) !important;
}
.btn-outline-light:hover {
    background-color: var(--primary-color) !important;
    color: white !important;
}
</style>