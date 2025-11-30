import { createRouter, createWebHistory } from 'vue-router'

// Authentication
import LoginSignup from '../components/LoginSignup.vue'

// Dashboards
import CustomerDashboard from '../components/CustomerDashboard.vue'
import EmployeeDashboard from '../components/EmployeeDashboard.vue'
import ManagerDashboard from '../components/ManagerDashboard.vue'

// Customer-related
import DashboardHome from '../components/DashboardHome.vue'
import MoneyTransfer from '../components/MoneyTransfer.vue'
import BeneficiaryManagement from '../components/BeneficiaryManagement.vue'
import TransactionHistory from '../components/TransactionHistory.vue'

// Employee-related
import KYCVerification from '../components/KYCVerification.vue'
import KYCVerificationRule from '../components/KYCVerificationRule.vue'
import DisputeResolution from '../components/DisputeResolution.vue'

// AI assistant (optional)
import AIAssistant from '../components/AIAssistant.vue'

const routes = [
  // ------------------------------
  // 🔐 Auth Route
  // ------------------------------
  {
    path: '/',
    name: 'LoginSignup',
    component: LoginSignup
  },

  // ------------------------------
  // 🧍 Customer Portal Routes
  // ------------------------------
  {
    path: '/customer-dashboard',
    component: CustomerDashboard,
    children: [
      { path: '', component: DashboardHome },
      { path: 'transfer', component: MoneyTransfer },
      { path: 'beneficiary', component: BeneficiaryManagement },
      { path: 'transactions', component: TransactionHistory }
    ]
  },

  // ------------------------------
  // 🧑‍💼 Employee Portal Routes
  // ------------------------------
  {
    path: '/employee-dashboard',
    component: EmployeeDashboard,
    children: [
      { path: 'kyc', component: KYCVerification },
      { path: 'kyc-rule', component: KYCVerificationRule },
      { path: 'disputes', component: DisputeResolution }
    ]
  },

  // ------------------------------
  // 👨‍💼 Manager Portal Route
  // ------------------------------
  {
    path: '/manager-dashboard',
    component: ManagerDashboard
  },

  // ------------------------------
  // 🤖 AI Assistant
  // ------------------------------
  {
    path: '/ai-assistant',
    component: AIAssistant
  },

  // ------------------------------
  // Default / Fallback
  // ------------------------------
  {
    path: '/:catchAll(.*)',
    redirect: '/'
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
