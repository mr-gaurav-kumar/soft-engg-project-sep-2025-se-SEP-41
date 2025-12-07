<template>
  <div class="d-flex min-vh-100 font-sans" :class="isDarkMode ? 'bg-dark' : 'bg-light'" :style="isDarkMode ? 'background-color: #0f172a;' : ''">
    <!-- Sidebar -->
    <div class="sidebar d-flex flex-column shadow-sm" style="width: 280px; z-index: 1000; background-color: #1e293b;">
      <!-- Logo/Header -->
      <div class="p-4 mb-2">
        <div class="d-flex align-items-center gap-3 mb-4">
          <div class="logo-box bg-primary bg-gradient text-white rounded-3 d-flex align-items-center justify-content-center shadow-sm">
            <span class="fw-bold fs-4">S</span>
          </div>
          <div>
            <h5 class="fw-bold text-white mb-0">Sep Bank</h5>
            <small class="text-white-50">Premium Banking</small>
          </div>
        </div>
        
        <div 
          class="user-profile p-3 rounded-3 d-flex align-items-center gap-3 cursor-pointer hover-bg-light-transition" 
          style="background-color: rgba(255,255,255,0.05);"
          @click="$router.push('/profile')"
        >
          <div class="avatar bg-primary text-white rounded-circle d-flex align-items-center justify-content-center fw-bold">
            {{ getInitials(customerName) }}
          </div>
          <div class="overflow-hidden">
            <h6 class="text-white mb-0 text-truncate">{{ customerName }}</h6>
          </div>
        </div>
      </div>

      <!-- Navigation -->
      <div class="flex-grow-1 px-3">
        <p class="text-uppercase text-white-50 fw-bold ms-2 mb-2" style="font-size: 0.75rem; letter-spacing: 1px;">Menu</p>
        <div class="d-grid gap-1">
          <button
            v-for="item in navItems"
            :key="item.id"
            @click="navigate(item.path)"
            :class="[
              'btn text-start d-flex align-items-center gap-3 px-3 py-2 rounded-3 transition-all',
              currentView === item.id
                ? 'bg-primary text-white shadow-sm'
                : 'btn-ghost-dark text-white-50 hover-text-white'
            ]"
          >
            <component :is="item.icon" :size="20" />
            <span class="fw-medium">{{ item.label }}</span>
          </button>
        </div>
      </div>

      <!-- Dark Mode Toggle -->
      <div class="px-3 py-2 border-top border-secondary border-opacity-25">
        <button 
          class="btn btn-ghost-dark text-white-50 w-100 d-flex align-items-center justify-content-between px-3 py-2 rounded-3 transition-all hover-text-white"
          @click="toggleDarkMode"
        >
          <div class="d-flex align-items-center gap-3">
            <component :is="isDarkMode ? Sun : Moon" :size="20" />
            <span class="fw-medium">{{ isDarkMode ? 'Light Mode' : 'Dark Mode' }}</span>
          </div>
        </button>
      </div>

      <!-- Logout -->
      <!-- <div class="p-3 border-top border-secondary border-opacity-25">
        <button class="btn btn-ghost-dark text-danger-emphasis w-100 d-flex align-items-center justify-content-center gap-2 py-2 hover-bg-danger-subtle" @click="handleLogout">
          <LogOut :size="18" />
          <span class="fw-medium">Sign Out</span>
        </button>
      </div> -->
      <div class="p-3 border-top border-secondary border-opacity-25">
        <button 
          class="logout-btn w-100 d-flex align-items-center justify-content-center gap-2 py-2"
          @click="handleLogout"
        >
          <LogOut :size="18" />
          <span class="fw-semibold">Sign Out</span>
        </button>
      </div>
    </div>

    <!-- Main Content -->
    <div class="flex-grow-1 overflow-auto">
      <!-- Top Header -->
      <header 
        class="border-bottom px-4 py-3 d-flex justify-content-between align-items-center sticky-top shadow-sm"
        :class="isDarkMode ? 'bg-dark' : 'bg-white border-light'"
        :style="isDarkMode ? 'background-color: #1e293b; border-color: rgba(255,255,255,0.1) !important;' : ''"
      >
        <div>
          <h4 :class="isDarkMode ? 'fw-bold text-white mb-0' : 'fw-bold text-dark mb-0'">{{ currentViewTitle }}</h4>
          <p :class="isDarkMode ? 'text-white-50 mb-0 small' : 'text-muted mb-0 small'">{{ currentViewSubtitle }}</p>
        </div>
        <div class="d-flex align-items-center gap-3">
          <button class="btn btn-light rounded-circle p-2 position-relative" @click="toggleNotifications">
            <Bell :size="20" class="text-secondary" />
            <span v-if="unreadCount > 0" class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">
              {{ unreadCount }}
            </span>
          </button>
        </div>
      </header>

      <!-- Notification Dropdown -->
      <div v-if="showNotifications" class="notification-dropdown position-absolute end-0 me-4 mt-2 bg-white rounded-3 shadow-lg" style="width: 320px; max-height: 400px; overflow-y: auto; z-index: 1001;">
        <div class="p-3 border-bottom">
          <h6 class="fw-bold mb-0">Notifications</h6>
        </div>
        <div v-if="notifications.length === 0" class="p-4 text-center text-muted">
          No new notifications
        </div>
        <div v-else>
          <div
            v-for="notif in notifications"
            :key="notif.id"
            class="p-3 border-bottom hover-bg-light cursor-pointer"
            @click="markAsRead(notif.id)"
          >
            <div class="d-flex justify-content-between align-items-start">
              <div class="flex-grow-1">
                <p class="mb-1 fw-semibold" :class="{ 'text-primary': !notif.is_read }">{{ notif.title }}</p>
                <p class="mb-0 small text-muted">{{ notif.message }}</p>
              </div>
              <button class="btn btn-sm btn-link text-danger p-0" @click.stop="deleteNotification(notif.id)">
                <X :size="16" />
              </button>
            </div>
          </div>
        </div>
      </div>

      <div class="p-4 p-lg-5">
        <!-- Dashboard View -->
        <div v-if="currentView === 'dashboard'" class="row g-4">
          <!-- Left Column -->
          <div class="col-lg-8">
            <!-- Balance Card -->
            <div class="card border-0 shadow-lg bg-primary bg-gradient text-white mb-4 overflow-hidden position-relative credit-card">
              <div class="card-body p-4 p-lg-5 position-relative z-1">
                <div class="d-flex justify-content-between align-items-start mb-5">
                  <div>
                    <p class="mb-1 opacity-75 fw-medium">Total Balance</p>
                    <h1 class="display-5 fw-bold mb-0">₹{{ balance.toLocaleString() }}</h1>
                  </div>
                  <div class="glass-icon p-2 rounded-3">
                    <CreditCard :size="32" class="text-white" />
                  </div>
                </div>
                <div class="d-flex justify-content-between align-items-end">
                  <div>
                    <p class="mb-1 opacity-75 small">Account Number</p>
                    <p class="mb-0 font-monospace fs-5">**** **** **** {{ customerId.toString().padStart(4, '0') }}</p>
                  </div>
                  <div class="text-end">
                    <p class="mb-0 opacity-75 small">Valid Thru</p>
                    <p class="mb-0 fw-medium">12/28</p>
                  </div>
                </div>
              </div>
              <!-- Decorative Circles -->
              <div class="position-absolute top-0 end-0 translate-middle-y me-n5 mt-n5 rounded-circle bg-white opacity-10" style="width: 300px; height: 300px;"></div>
              <div class="position-absolute bottom-0 start-0 translate-middle-x ms-n5 mb-n5 rounded-circle bg-black opacity-10" style="width: 200px; height: 200px;"></div>
            </div>

            <!-- Quick Actions -->
            <h5 class="fw-bold text-dark mb-3">Quick Actions</h5>
            <div class="row g-3 mb-4">
              <div class="col-6 col-md-3">
                <button @click="navigate('/transfer')" class="btn btn-white w-100 h-100 p-3 rounded-4 shadow-sm border-0 d-flex flex-column align-items-center justify-content-center gap-2 hover-lift transition-all">
                  <div class="icon-box bg-primary-subtle text-primary rounded-circle p-3 mb-1">
                    <Send :size="24" />
                  </div>
                  <span class="fw-medium text-dark small">Transfer</span>
                </button>
              </div>
              <div class="col-6 col-md-3">
                <button @click="navigate('/beneficiary')" class="btn btn-white w-100 h-100 p-3 rounded-4 shadow-sm border-0 d-flex flex-column align-items-center justify-content-center gap-2 hover-lift transition-all">
                  <div class="icon-box bg-success-subtle text-success rounded-circle p-3 mb-1">
                    <Users :size="24" />
                  </div>
                  <span class="fw-medium text-dark small">Beneficiaries</span>
                </button>
              </div>
              <div class="col-6 col-md-3">
                <button @click="navigate('/history')" class="btn btn-white w-100 h-100 p-3 rounded-4 shadow-sm border-0 d-flex flex-column align-items-center justify-content-center gap-2 hover-lift transition-all">
                  <div class="icon-box bg-warning-subtle text-warning rounded-circle p-3 mb-1">
                    <FileText :size="24" />
                  </div>
                  <span class="fw-medium text-dark small">History</span>
                </button>
              </div>
              <div class="col-6 col-md-3">
                <button @click="navigate('/payments')" class="btn btn-white w-100 h-100 p-3 rounded-4 shadow-sm border-0 d-flex flex-column align-items-center justify-content-center gap-2 hover-lift transition-all">
                  <div class="icon-box bg-info-subtle text-info rounded-circle p-3 mb-1">
                    <MessageSquare :size="24" />
                  </div>
                  <span class="fw-medium text-dark small">Payments</span>
                </button>
              </div>
            </div>

            <!-- Recent Transactions -->
            <div class="card border-0 shadow-sm rounded-4 overflow-hidden">
              <div class="card-header bg-white border-bottom border-light p-4 d-flex justify-content-between align-items-center">
                <h5 class="fw-bold text-dark mb-0">Recent Transactions</h5>
                <button class="btn btn-link text-primary text-decoration-none fw-medium p-0" @click="navigate('/history')">View All</button>
              </div>
              <div class="card-body p-0">
                <div v-if="transactions.length === 0" class="p-4 text-center text-muted">
                  No transactions yet
                </div>
                <div v-else class="list-group list-group-flush">
                  <div
                    v-for="transaction in transactions.slice(0, 5)"
                    :key="transaction.id"
                    class="list-group-item border-light p-3 d-flex align-items-center justify-content-between hover-bg-light transition-all"
                  >
                    <div class="d-flex align-items-center gap-3">
                      <div :class="['rounded-circle p-2 d-flex align-items-center justify-content-center', transaction.type === 'credit' ? 'bg-success-subtle text-success' : 'bg-light text-secondary']" style="width: 40px; height: 40px;">
                        <ArrowDownLeft v-if="transaction.type === 'credit'" :size="20" />
                        <ArrowUpRight v-else :size="20" />
                      </div>
                      <!-- <div>
                        <p class="mb-0 fw-semibold text-dark">{{ transaction.description }}</p>
                        <small class="text-muted">{{ formatDate(transaction.timestamp) }}</small>
                      </div>  -->
                      <div>
                        <p class="mb-0 fw-semibold text-dark">{{ transaction.description }}</p>
                        <small class="text-muted me-2">{{ formatDateCard(transaction.timestamp) }}</small>
                        <small class="text-muted">{{ formatTimeCard(transaction.timestamp) }}</small>
                      </div> 

                    </div>
                    <span :class="['fw-bold', transaction.type === 'debit' ? 'text-dark' : 'text-success']">
                      {{ transaction.type === 'debit' ? '-' : '+' }}₹{{ transaction.amount }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Right Column -->
          <div class="col-lg-4">
            <!-- Spending Summary -->
            <div class="card border-0 shadow-sm rounded-4 h-100" :class="isDarkMode ? 'bg-dark' : ''" :style="isDarkMode ? 'background-color: #1e293b; border: 1px solid rgba(255,255,255,0.1) !important;' : ''">
              <div class="card-header border-bottom p-4" :class="isDarkMode ? 'bg-dark' : 'bg-white border-light'" :style="isDarkMode ? 'background-color: #1e293b; border-color: rgba(255,255,255,0.1) !important;' : ''">
                <h5 :class="isDarkMode ? 'fw-bold text-white mb-0' : 'fw-bold text-dark mb-0'">Spending Summary</h5>
              </div>
              <div class="card-body p-4 d-flex flex-column align-items-center justify-content-center" :style="isDarkMode ? 'background-color: #1e293b;' : ''">
                <div class="position-relative mb-4">
                  <!-- CSS Conic Gradient Pie Chart -->
                  <div class="pie-chart rounded-circle" :style="pieChartStyle"></div>
                  <div class="position-absolute top-50 start-50 translate-middle rounded-circle d-flex flex-column align-items-center justify-content-center shadow-sm" :class="isDarkMode ? 'bg-dark' : 'bg-white'" :style="isDarkMode ? 'background-color: #1e293b; width: 140px; height: 140px;' : 'width: 140px; height: 140px;'">
                    <span :class="isDarkMode ? 'text-white-50 small' : 'text-muted small'">Total</span>
                    <span :class="isDarkMode ? 'fw-bold fs-4 text-white' : 'fw-bold fs-4'">₹{{ totalSpending.toLocaleString() }}</span>
                  </div>
                </div>

                <div class="w-100">
                  <div
                    v-for="(category, index) in spendingCategories"
                    :key="index"
                    class="d-flex justify-content-between align-items-center mb-3 p-2 rounded-3 hover-bg-light transition-all"
                  >
                    <div class="d-flex align-items-center gap-2">
                      <div class="rounded-circle" :style="{ backgroundColor: category.color, width: '10px', height: '10px' }"></div>
                      <span class="text-dark fw-medium">{{ category.name }}</span>
                    </div>
                    <span class="fw-bold text-dark">{{ category.percentage }}%</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Transfer View -->
        <div v-if="currentView === 'transfer'" class="row g-4">
          <div class="col-lg-6 mx-auto">
            <div class="card border-0 shadow-sm rounded-4">
              <div class="card-body p-4">
                <h5 class="fw-bold mb-4">Transfer Funds</h5>
                <div class="mb-3">
                  <label class="form-label fw-medium">Select Beneficiary</label>
                    <!-- <select v-model="transfer.beneficiary_account" class="form-select">
                      <option value="">Choose a beneficiary</option>
                      <option v-for="acc in activeBeneficiaryAccounts" :key="acc" :value="acc">{{ acc }}</option>
                    </select> -->
                    <select v-model="transfer.beneficiary_account" class="form-select">
                      <option value="">Choose a beneficiary</option>
                      <option v-for="acc in activeBeneficiaryAccounts" :key="acc.account_number" :value="acc.account_number">
                        {{ acc.name }} - {{ acc.account_number }}
                      </option>
                    </select>
                </div>
                <div class="mb-3">
                  <label class="form-label fw-medium">Amount</label>
                  <input v-model="transfer.amount" type="number" class="form-control" placeholder="Enter amount">
                </div>
                <div class="mb-3">
                  <label class="form-label fw-medium">Remarks (optional)</label>
                  <input v-model="transfer.remarks" type="text" class="form-control" placeholder="Add a note">
                </div>
                <button @click="transferFunds" class="btn btn-primary w-100 py-2">
                  <Send :size="18" class="me-2" />
                  Transfer Now
                </button>
              </div>
            </div>
          </div>
        </div>



        <!-- History View -->
        <div v-if="currentView === 'history'" class="row g-4">
          <div class="col-12">
            <div class="card border-0 shadow-sm rounded-4">
              <div class="card-header bg-white border-bottom border-light p-4 d-flex justify-content-between align-items-center">
                <h5 class="fw-bold mb-0">Transaction History</h5>
                <div class="d-flex gap-2">
                  <button @click="downloadCSV" class="btn btn-outline-primary btn-sm">
                    <Download :size="16" class="me-1" />
                    CSV
                  </button>
                </div>
              </div>
              <div class="card-body p-4">
                <div v-if="transactions.length === 0" class="text-center text-muted py-5">
                  <FileText :size="48" class="mb-3 opacity-25" />
                  <p>No transactions yet</p>
                </div>
                <div v-else class="row g-3">
                  <div v-for="transaction in transactions" :key="transaction.id" class="col-12">
                    <div 
                      :class="[
                        'transaction-card p-4 rounded-4 shadow-sm border-0 d-flex align-items-center justify-content-between',
                        transaction.type === 'credit' ? 'bg-success-light' : 'bg-danger-light'
                      ]"
                    >
                      <div class="d-flex align-items-center gap-3 flex-grow-1">
                        <!-- Icon -->
                        <div 
                          :class="[
                            'transaction-icon rounded-circle d-flex align-items-center justify-content-center',
                            transaction.type === 'credit' ? 'bg-success text-white' : 'bg-danger text-white'
                          ]"
                          style="width: 50px; height: 50px;"
                        >
                          <ArrowDownLeft v-if="transaction.type === 'credit'" :size="24" />
                          <ArrowUpRight v-else :size="24" />
                        </div>

                        <!-- Transaction Details -->
                        <div class="flex-grow-1">
                          <!-- Description with recipient details -->
                          <h6 class="mb-1 fw-bold text-dark">
                            {{ getTransactionTitle(transaction) }}
                          </h6>
                          
                          <!-- Remarks (if present) -->
                          <p v-if="hasRemarks(transaction)" class="mb-1 text-muted small">
                            {{ getRemarks(transaction) }}
                          </p>
                          
                          <!-- Date and Time on same line -->
                          <div class="d-flex align-items-center gap-3 text-muted small">
                            <span>{{ formatDateCard(transaction.timestamp) }}</span>
                            <span>•</span>
                            <span>{{ formatTimeCard(transaction.timestamp) }}</span>
                          </div>
                        </div>

                        <!-- Amount -->
                        <div class="text-end">
                          <h5 
                            :class="[
                              'mb-0 fw-bold',
                              transaction.type === 'credit' ? 'text-success' : 'text-danger'
                            ]"
                          >
                            {{ transaction.type === 'debit' ? '-' : '+' }}₹{{ transaction.amount.toLocaleString() }}
                          </h5>
                        </div>
                      </div>
                    </div>
                  </div>
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
import axios from "axios";
import notificationService from "@/services/notificationService";
import {
  LayoutDashboard,
  Send,
  Users,
  FileText,
  MessageSquare,
  LogOut,
  Bell,
  CreditCard,
  ArrowDownLeft,
  ArrowUpRight,
  Download,
  X,
  Wallet,
  Moon,
  Sun
} from "lucide-vue-next";
import { useDarkMode } from "@/composables/useDarkMode";

export default {
  name: "Dashboard",
  components: {
    LayoutDashboard,
    Send,
    Users,
    FileText,
    MessageSquare,
    LogOut,
    Bell,
    CreditCard,
    ArrowDownLeft,
    ArrowUpRight,
    Download,
    X,
    Wallet,
    Moon,
    Sun
  },
  setup() {
    const { isDarkMode, toggleDarkMode } = useDarkMode()
    return {
      isDarkMode,
      toggleDarkMode
    }
  },
  data() {
    return {
      customerId: Number(localStorage.getItem("customer_id")),
      customerName: localStorage.getItem("customer_name") || "Customer",
      balance: 0,
      transactions: [],
      transactions: [],
      beneficiaries: [],
      transfer: {
        beneficiary_account: '',
        amount: '',
        remarks: ''
      },
      notifications: [],
      unreadCount: 0,
      showNotifications: false,
      currentView: 'dashboard',
      navItems: [
        { id: 'dashboard', label: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
        { id: 'beneficiary', label: 'Beneficiaries', path: '/beneficiary', icon: Users },
        { id: 'transfer', label: 'Transfer Money', path: '/transfer', icon: Send },
        { id: 'history', label: 'Transactions', path: '/history', icon: FileText },
        { id: 'payments', label: 'Payments', path: '/payments', icon: Wallet },
        { id: 'chatbot', label: 'AI Assistant', path: '/chatbot', icon: MessageSquare }
      ]
      ,
      spendingCategories: []
    };
  },
  computed: {
    currentViewTitle() {
      const titles = {
        dashboard: 'Dashboard Overview',
        transfer: 'Transfer Funds',
        history: 'Transaction History'
      };
      return titles[this.currentView] || 'Dashboard';
    },
    currentViewSubtitle() {
      const subtitles = {
        dashboard: "Here's what's happening with your account today.",
        transfer: 'Send money to your beneficiaries quickly and securely.',
        history: 'View all your past transactions and download statements.'
      };
      return subtitles[this.currentView] || '';
    },
    // activeBeneficiaryAccounts() {
    //   return this.beneficiaries
    //     .filter(b => b.status === 'Active')
    //     .map(b => b.account_number);
    // },
    activeBeneficiaryAccounts() {
        return this.beneficiaries
          .filter(b => b.status === 'Active')
          .map(b => ({
            name: b.name,
            account_number: b.account_number
          }));
      },
    totalSpending() {
      // Use spending categories total if available, otherwise calculate from transactions
      if (this.spendingCategories.length > 0) {
        return Math.round(
          this.spendingCategories.reduce((sum, cat) => sum + (cat.spent_amount || 0), 0)
        );
      }
      const debits = this.transactions
        .filter(t => t.type === 'debit')
        .reduce((sum, t) => sum + parseFloat(t.amount || 0), 0);
      return Math.round(debits);
    },
    pieChartStyle() {
      // Handle empty categories
      if (!this.spendingCategories || this.spendingCategories.length === 0) {
        return {
          width: '200px',
          height: '200px',
          background: 'conic-gradient(#e9ecef 0% 100%)'
        };
      }
      
      const colors = this.spendingCategories.map(c => c.color);
      const percentages = this.spendingCategories.map(c => c.percentage);
      
      let gradientStops = [];
      let currentPercent = 0;
      
      for (let i = 0; i < colors.length; i++) {
        gradientStops.push(`${colors[i]} ${currentPercent}% ${currentPercent + percentages[i]}%`);
        currentPercent += percentages[i];
      }
      
      return {
        width: '200px',
        height: '200px',
        background: `conic-gradient(${gradientStops.join(', ')})`
      };
    }
  },
  methods: {
    getInitials(name) {
      return name
        .split(' ')
        .map(n => n[0])
        .join('')
        .toUpperCase()
        .slice(0, 2);
    },
    navigate(path) {
      this.$router.push(path);
    },
    updateViewFromRoute() {
      const path = this.$route.path;
      const viewMap = {
        '/dashboard': 'dashboard',
        '/transfer': 'transfer',
        '/history': 'history',
      };
      this.currentView = viewMap[path] || 'dashboard';
      
      if (this.currentView === 'history') {
        this.fetchAllTransactions();
      } else if (this.currentView === 'dashboard') {
        this.fetchMiniStatement();
        this.fetchSpendingCategories();
      }
    },
    handleLogout() {
      localStorage.clear();
      this.$router.push("/");
    },
    toggleNotifications() {
      this.showNotifications = !this.showNotifications;
    },
    // formatDate(timestamp) {
    //   if (!timestamp) return 'N/A';
    //   const date = new Date(timestamp);
    //   return date.toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' });
    // },
    formatDate(timestamp) {
  if (!timestamp) return 'N/A';

  // Create a Date object from UTC timestamp
  const date = new Date(timestamp);

  // Add 5 hours 30 minutes (IST offset)
  const IST_OFFSET = 5.5 * 60 * 60 * 1000; // in milliseconds
  const istDate = new Date(date.getTime() + IST_OFFSET);

  // Format the IST date
  return istDate.toLocaleDateString('en-IN', {
    day: 'numeric',
    month: 'short',
    year: 'numeric'
  });
}
,
    async fetchBalance() {
      try {
        const res = await axios.get(
          `http://127.0.0.1:5000/customer/balance/${this.customerId}`
        );
        this.balance = res.data.balance;
      } catch (err) {
        console.error("Error fetching balance:", err);
      }
    },
    async fetchMiniStatement() {
      try {
        const res = await axios.get(
          `http://127.0.0.1:5000/customer/mini-statement/${this.customerId}`
        );
        this.transactions = res.data;
      } catch (err) {
        console.error("Error fetching mini statement:", err);
      }
    },
    async fetchSpendingCategories() {
      try {
        const res = await axios.get(
          `http://127.0.0.1:5000/customer/spending-categories/${this.customerId}`
        );
        
        // Color palette for categories
        const colors = [
          '#0d6efd', // Blue
          '#198754', // Green
          '#ffc107', // Yellow
          '#dc3545', // Red
          '#6c757d', // Gray
          '#0dcaf0', // Cyan
          '#fd7e14', // Orange
          '#6f42c1', // Purple
          '#20c997', // Teal
          '#e9ecef'  // Light gray
        ];
        
        // Map categories with colors
        this.spendingCategories = res.data.categories.map((cat, index) => ({
          name: cat.name,
          percentage: cat.percentage,
          spent_amount: cat.spent_amount,
          color: colors[index % colors.length]
        }));
      } catch (err) {
        console.error("Error fetching spending categories:", err);
        // Fallback to empty array if error
        this.spendingCategories = [];
      }
    },
    async downloadCSV() {
      try {
        const res = await axios.get(
          `http://127.0.0.1:5000/customer/transactions/${this.customerId}?format=csv`,
          { responseType: "blob" }
        );
        const url = window.URL.createObjectURL(new Blob([res.data]));
        const link = document.createElement("a");
        link.href = url;
        link.setAttribute("download", "transactions.csv");
        document.body.appendChild(link);
        link.click();
        link.remove();
      } catch (err) {
        console.error("Error downloading CSV:", err);
      }
    },
    async downloadPDF() {
      try {
        const res = await axios.get(
          `http://127.0.0.1:5000/customer/transactions/${this.customerId}?format=pdf`,
          { responseType: "blob" }
        );
        const url = window.URL.createObjectURL(new Blob([res.data]));
        const link = document.createElement("a");
        link.href = url;
        link.setAttribute("download", "transactions.pdf");
        document.body.appendChild(link);
        link.click();
        link.remove();
      } catch (err) {
        console.error("Error downloading PDF:", err);
      }
    },
    async fetchNotifications() {
      try {
        const data = await notificationService.getAll(this.customerId);
        this.notifications = data;
        this.unreadCount = data.filter((n) => !n.is_read).length;
      } catch (err) {
        console.error("Error fetching notifications:", err);
      }
    },
    async markAsRead(id) {
      try {
        await notificationService.markAsRead(id);
        this.fetchNotifications();
      } catch (err) {
        console.error("Error marking as read:", err);
      }
    },
    async deleteNotification(id) {
      try {
        await notificationService.delete(id);
        this.fetchNotifications();
      } catch (err) {
        console.error("Error deleting notification:", err);
      }
    },
    async fetchBeneficiaries() {
      try {
        const res = await axios.get(
          `http://127.0.0.1:5000/customer/beneficiaries/${this.customerId}`
        );
        this.beneficiaries = res.data;
      } catch (err) {
        console.error("Error fetching beneficiaries:", err);
      }
    },
    async transferFunds() {
      if (!this.transfer.beneficiary_account || !this.transfer.amount) {
        alert('Please fill in all required fields');
        return;
      }

      // Extract account number from the selected beneficiary
      const accountNumber = typeof this.transfer.beneficiary_account === 'string' 
        ? this.transfer.beneficiary_account 
        : this.transfer.beneficiary_account.account_number;

      try {
        const res = await axios.post('http://127.0.0.1:5000/customer/initiate-transfer', {
          customer_id: this.customerId,
          amount: parseFloat(this.transfer.amount),
          beneficiary_account: accountNumber,
          remarks: this.transfer.remarks
        });

        console.log("Initiate-transfer RESPONSE:", res.data);

        this.$router.push({
          name: "TransactionConfirm",
          query: {
            session_id: res.data.session_id,
            customer_id: this.customerId,
            amount: this.transfer.amount,
            beneficiary_account: accountNumber,
            remarks: this.transfer.remarks
          }
        });
      } catch (err) {
        console.error('Error initiating transfer:', err);
        alert(err.response?.data?.message || 'Error initiating transfer');
      }
    },

    async fetchAllTransactions() {
      try {
        const res = await axios.get(
          `http://127.0.0.1:5000/customer/transactions/${this.customerId}`
        );
        this.transactions = res.data;
      } catch (err) {
        console.error("Error fetching transactions:", err);
      }
    },
    
    // Helper methods for transaction card display with IST timezone conversion
    // formatDateCard(timestamp) {
    //   if (!timestamp) return 'N/A';
    //   const date = new Date(timestamp);
    //   // Convert to IST (UTC+5:30)
    //   const istDate = new Date(date.toLocaleString('en-US', { timeZone: 'Asia/Kolkata' }));
    //   const day = istDate.getDate();
    //   const month = istDate.toLocaleDateString('en-GB', { month: 'short', timeZone: 'Asia/Kolkata' });
    //   const year = istDate.getFullYear().toString().slice(-2);
    //   return `${day} ${month} ${year}`;
    // },

    formatDateCard(timestamp) {
  if (!timestamp) return 'N/A';

  const istDate = new Date(timestamp);

  // Format date in DD MMM YY
  return istDate.toLocaleDateString('en-GB', { 
    day: '2-digit', 
    month: 'short', 
    year: '2-digit',
    timeZone: 'Asia/Kolkata'
  });
}
,

    // formatTimeCard(timestamp) {
    //   if (!timestamp) return 'N/A';
    //   const date = new Date(timestamp);
    //   // Convert to IST (UTC+5:30)
    //   return date.toLocaleTimeString('en-GB', { 
    //     hour: '2-digit', 
    //     minute: '2-digit', 
    //     second: '2-digit', 
    //     hour12: false,
    //     timeZone: 'Asia/Kolkata'
    //   });
    // },

    formatTimeCard(timestamp) {
  if (!timestamp) return 'N/A';

  const istDate = new Date(timestamp);

  // Format time in HH:MM:SS (24-hour)
  return istDate.toLocaleTimeString('en-GB', { 
    hour: '2-digit', 
    minute: '2-digit', 
    second: '2-digit', 
    hour12: false,
    timeZone: 'Asia/Kolkata'
  });
}
,

    getTransactionTitle(transaction) {
      // Extract the main part before " - " (which typically contains remarks)
      const description = transaction.description || '';
      const parts = description.split(' - ');
      return parts[0].trim();
    },

    hasRemarks(transaction) {
      const description = transaction.description || '';
      const parts = description.split(' - ');
      // Check if there's a second part and it's not empty
      return parts.length > 1 && parts[1] && parts[1].trim() !== '';
    },

    getRemarks(transaction) {
      const description = transaction.description || '';
      const parts = description.split(' - ');
      // Return everything after the first " - "
      if (parts.length > 1) {
        return parts.slice(1).join(' - ').trim();
      }
      return '';
    },
  },
  mounted() {
    this.updateViewFromRoute();
    this.fetchBalance();
    this.fetchMiniStatement();
    this.fetchSpendingCategories();
    this.fetchBeneficiaries();
    this.fetchNotifications();
    
    // Close notifications when clicking outside
    document.addEventListener('click', (e) => {
      if (this.showNotifications && !e.target.closest('.notification-dropdown') && !e.target.closest('.btn')) {
        this.showNotifications = false;
      }
    });
  },
  watch: {
    '$route': 'updateViewFromRoute'
  }
};
</script>

<style scoped>
/* Custom styles for premium look */
.font-sans {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

.logo-box {
  width: 48px;
  height: 48px;
}

.avatar {
  width: 40px;
  height: 40px;
  font-size: 14px;
}

.btn-ghost-dark {
  background: transparent;
  border: none;
  color: rgba(255, 255, 255, 0.5);
  transition: all 0.2s ease;
}

.btn-ghost-dark:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
}

.hover-text-white:hover {
  color: white !important;
}

.hover-bg-danger-subtle:hover {
  background-color: rgba(220, 53, 69, 0.1);
}

.transition-all {
  transition: all 0.2s ease;
}

.credit-card {
  min-height: 240px;
}

.glass-icon {
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
}

.btn-white {
  background: white;
}

.hover-lift {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.hover-lift:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1) !important;
}

.hover-bg-light {
  transition: background-color 0.2s ease;
}

.hover-bg-light:hover {
  background-color: #f8f9fa;
}

.cursor-pointer {
  cursor: pointer;
}

.notification-dropdown {
  animation: slideDown 0.2s ease;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.modal-backdrop {
  background-color: rgba(0, 0, 0, 0.5);
}

.gap-1 {
  gap: 0.25rem;
}

.gap-2 {
  gap: 0.5rem;
}

.gap-3 {
  gap: 1rem;
}

.py-2\.5 {
  padding-top: 0.625rem;
  padding-bottom: 0.625rem;
}

.z-1 {
  z-index: 1;
}

/* Bootstrap 5 subtle backgrounds */
.bg-primary-subtle {
  background-color: rgba(13, 110, 253, 0.1);
}

.bg-success-subtle {
  background-color: rgba(25, 135, 84, 0.1);
}

.bg-warning-subtle {
  background-color: rgba(255, 193, 7, 0.1);
}

.bg-info-subtle {
  background-color: rgba(13, 202, 240, 0.1);
}

.text-primary {
  color: #0d6efd !important;
}

.text-success {
  color: #198754 !important;
}

.text-warning {
  color: #ffc107 !important;
}

.text-info {
  color: #0dcaf0 !important;
}

.logout-btn {
  background: #fff;
  border: 1px solid rgba(220, 53, 69, 0.35);
  color: #dc3545;
  border-radius: 12px;
  transition: all 0.25s ease-in-out;
  box-shadow: 0 2px 6px rgba(255, 0, 0, 0.06);
}

.logout-btn:hover {
  background: rgba(220, 53, 69, 0.08);
  border-color: rgba(220, 53, 69, 0.7);
  box-shadow: 0 4px 10px rgba(220, 53, 69, 0.15);
  transform: translateY(-2px);
}

.logout-btn:active {
  transform: scale(0.98);
  background: rgba(220, 53, 69, 0.16);
}

/* Transaction Card Styles */
.transaction-card {
  transition: all 0.3s ease;
  cursor: default;
}

.transaction-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12) !important;
}

.bg-success-light {
  background: linear-gradient(135deg, rgba(25, 135, 84, 0.08) 0%, rgba(25, 135, 84, 0.04) 100%);
  border-left: 4px solid #198754 !important;
}

.bg-danger-light {
  background: linear-gradient(135deg, rgba(220, 53, 69, 0.08) 0%, rgba(220, 53, 69, 0.04) 100%);
  border-left: 4px solid #dc3545 !important;
}

.transaction-icon {
  flex-shrink: 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.sidebar {
  flex-shrink: 0;
}

.cursor-pointer {
  cursor: pointer;
}

.hover-bg-light-transition {
  transition: background-color 0.2s ease;
}

.hover-bg-light-transition:hover {
  background-color: rgba(255,255,255,0.1) !important;
}

.modal-backdrop {
  animation: fadeIn 0.2s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
</style>

