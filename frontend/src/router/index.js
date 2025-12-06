import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../components/Login.vue'
import Register from '../components/Register.vue'
import VerifyOtp from '../components/VerifyOTP.vue'
import ForgotPassword from '../components/ForgotPassword.vue'
import ResetPassword from '../components/ResetPassword.vue'
import Dashboard from '../components/Dashboard.vue'
import KYCUpload from "../components/KYCUpload.vue";
import Beneficiary from '../components/Beneficiary.vue'
import KYCOTP from '@/components/KYCOTP.vue'
import AIAssistent from '@/components/AIAssistent.vue'
import ManagerPanel from '@/components/ManagerPanel.vue'
import Payments from '@/components/Payments.vue'

const routes = [
  { path: '/', name: 'home', component: Home },
  { path: "/login", name: 'login', component: Login },
  { path: "/register", name: 'register', component: Register },
  { path: "/verify", name: 'VerifyOtp', component: VerifyOtp },
  { path: "/forgot", name: 'ForgotPassword', component: ForgotPassword },
  { path: "/reset", name: 'ResetPassword', component: ResetPassword },
  { path: "/dashboard", name: 'Dashboard', component: Dashboard },
  { path: "/transfer", name: 'Transfer', component: Dashboard },
  { path: "/beneficiary", name: 'Beneficiary', component: Beneficiary },
  { path: "/history", name: 'History', component: Dashboard },
  { path: "/kyc-upload/:customer_id", component: KYCUpload },
  { path: "/kyc-otp/:customer_id", component: KYCOTP },
  { path: "/chatbot", component: AIAssistent},
  { path: "/manager", component: ManagerPanel},
  { path: "/payments", component: Payments}
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
