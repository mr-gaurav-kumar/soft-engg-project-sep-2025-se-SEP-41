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
              $route.path === item.path
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
          <h4 :class="isDarkMode ? 'fw-bold text-white mb-0' : 'fw-bold text-dark mb-0'">Payments & Recharges</h4>
          <p :class="isDarkMode ? 'text-white-50 mb-0 small' : 'text-muted mb-0 small'">Manage your utility bills, recharges, and Fastag top-ups.</p>
        </div>
        <div class="d-flex align-items-center gap-3">
          <button class="btn btn-light rounded-circle p-2 position-relative">
            <Bell :size="20" class="text-secondary" />
            <!-- <span class="position-absolute top-0 start-100 translate-middle p-1 bg-danger border border-light rounded-circle" v-if="unreadCount > 0">
              <span class="visually-hidden">New alerts</span>
            </span> -->
          </button>
        </div>
      </header>

      <div class="p-4 p-lg-5">
        
        <!-- Payment Sections using Tabs or Accordion-like simplified stacked cards -->
        <div class="row g-4">
            
          <!-- Pay a Bill -->
          <div class="col-lg-4">
             <div class="card border-0 shadow-sm rounded-4 h-100">
                <div class="card-header bg-white border-bottom border-light p-4">
                  <div class="d-flex align-items-center gap-3">
                     <div class="rounded-circle bg-primary-subtle text-primary p-3 d-flex align-items-center justify-content-center" style="width: 50px; height: 50px;">
                        <FileText :size="24" />
                     </div>
                     <h5 class="fw-bold text-dark mb-0">Pay Bill</h5>
                  </div>
                </div>
                <div class="card-body p-4">
                   <form @submit.prevent="payBill">
                      <div class="mb-3">
                         <label class="form-label small text-muted fw-bold">Bill Type</label>
                         <select v-model="bill.bill_type" class="form-select bg-light border-0 py-2" required>
                            <option value="" disabled selected>Select Bill Type</option>
                            <option v-for="type in billOptions.bill_types" :key="type" :value="type">{{ type }}</option>
                         </select>
                      </div>
                      <div class="mb-3">
                         <label class="form-label small text-muted fw-bold">Biller</label>
                         <select v-model="bill.biller" class="form-select bg-light border-0 py-2" required>
                             <option value="" disabled selected>Select Biller</option>
                             <option v-for="biller in getBillerList(bill.bill_type)" :key="biller" :value="biller">{{ biller }}</option>
                         </select>
                      </div>
                      <div class="mb-3">
                         <label class="form-label small text-muted fw-bold">Consumer No</label>
                         <input v-model="bill.bill_account" type="text" class="form-control bg-light border-0 py-2" placeholder="Account / Consumer No" required>
                      </div>
                      <div class="mb-4">
                         <label class="form-label small text-muted fw-bold">Amount</label>
                         <input v-model="bill.amount" type="number" class="form-control bg-light border-0 py-2" placeholder="Enter amount" required>
                      </div>
                      <button type="submit" class="btn btn-primary w-100 py-2 fw-medium shadow-sm hover-lift">
                         Pay Bill
                      </button>
                   </form>
                </div>
             </div>
          </div>

          <!-- Recharge -->
          <div class="col-lg-4">
             <div class="card border-0 shadow-sm rounded-4 h-100">
                <div class="card-header bg-white border-bottom border-light p-4">
                  <div class="d-flex align-items-center gap-3">
                     <div class="rounded-circle bg-success-subtle text-success p-3 d-flex align-items-center justify-content-center" style="width: 50px; height: 50px;">
                        <Smartphone :size="24" />
                     </div>
                     <h5 class="fw-bold text-dark mb-0">Recharge</h5>
                  </div>
                </div>
                <div class="card-body p-4">
                   <form @submit.prevent="recharge">
                      <div class="mb-3">
                         <label class="form-label small text-muted fw-bold">Type</label>
                         <select v-model="rechargeData.recharge_type" class="form-select bg-light border-0 py-2" required>
                            <option value="" disabled selected>Select Type</option>
                            <option value="Mobile">Mobile</option>
                            <option value="DTH">DTH</option>
                         </select>
                      </div>
                      <div class="mb-3">
                         <label class="form-label small text-muted fw-bold">Operator</label>
                         <select v-model="rechargeData.operator" class="form-select bg-light border-0 py-2" required>
                            <option value="" disabled selected>Select Operator</option>
                            <option v-for="op in (rechargeData.recharge_type === 'Mobile' ? billOptions.mobile_operators : billOptions.dth_providers)" :key="op" :value="op">{{ op }}</option>
                         </select>
                      </div>
                      <div class="mb-3">
                         <label class="form-label small text-muted fw-bold">Number</label>
                         <input v-model="rechargeData.number" type="text" class="form-control bg-light border-0 py-2" placeholder="Mobile / DTH Number" required>
                      </div>
                      <div class="mb-4">
                         <label class="form-label small text-muted fw-bold">Amount</label>
                         <input v-model="rechargeData.amount" type="number" class="form-control bg-light border-0 py-2" placeholder="Enter amount" required>
                      </div>
                      <button type="submit" class="btn btn-primary w-100 py-2 fw-medium shadow-sm hover-lift">
                         Recharge
                      </button>
                   </form>
                </div>
             </div>
          </div>

          <!-- Fastag -->
          <div class="col-lg-4">
             <div class="card border-0 shadow-sm rounded-4 h-100">
                <div class="card-header bg-white border-bottom border-light p-4">
                  <div class="d-flex align-items-center gap-3">
                     <div class="rounded-circle bg-warning-subtle text-warning d-flex align-items-center justify-content-center" style="width: 50px; height: 50px; overflow: hidden;">
                        <img src="/Fastag-logo.png" alt="FASTag" style="width: 42px; height: 42px; object-fit: contain;" />
                     </div>
                     <h5 class="fw-bold text-dark mb-0">FASTag</h5>
                  </div>
                </div>
                <div class="card-body p-4">
                   <form @submit.prevent="fastagTopup">
                      <div class="mb-3">
                         <label class="form-label small text-muted fw-bold">Vehicle Number</label>
                         <input v-model="fastag.vehicle_number" type="text" class="form-control bg-light border-0 py-2" placeholder="e.g. KA01AB1234" required>
                      </div>
                      <div class="mb-3">
                         <label class="form-label small text-muted fw-bold">Tag ID</label>
                         <input v-model="fastag.tag_id" type="text" class="form-control bg-light border-0 py-2" placeholder="Optional Tag ID">
                      </div>
                      <div class="mb-4">
                         <label class="form-label small text-muted fw-bold">Amount</label>
                         <input v-model="fastag.amount" type="number" class="form-control bg-light border-0 py-2" placeholder="Enter amount" required>
                      </div>
                      <div class="mb-3" style="visibility: hidden;"> <!-- Spacer to align buttons -->
                        <label class="form-label small">&nbsp;</label>
                        <input type="text" class="form-control border-0 py-2">
                      </div>
                      <button type="submit" class="btn btn-primary w-100 py-2 fw-medium shadow-sm hover-lift">
                         Top-up FASTag
                      </button>
                   </form>
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
import { 
  LayoutDashboard, 
  Users, 
  Send, 
  FileText, 
  MessageSquare, 
  LogOut, 
  Bell,
  Smartphone,
  Zap,
  Wallet,
  Moon,
  Sun
} from 'lucide-vue-next';
import { useDarkMode } from "@/composables/useDarkMode";

export default {
  name: "Payments",
  components: {
    LayoutDashboard,
    Users,
    Send,
    FileText,
    MessageSquare,
    LogOut,
    Bell,
    Smartphone,
    Zap,
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
      customerId: localStorage.getItem("customer_id") || 1,
      customerName: localStorage.getItem("customer_name") || "Customer",
      billOptions: {
        bill_types: [],
        electricity_providers: [],
        gas_providers: [],
        internet_providers: [],
        mobile_operators: [],
        dth_providers: [],
        transport_providers: [],
        food_providers: [],
        others_providers: [],
      },
      bill: { bill_type: "", biller: "", bill_account: "", amount: "" },
      rechargeData: {
        recharge_type: "",
        operator: "",
        number: "",
        amount: "",
      },
      fastag: { vehicle_number: "", tag_id: "", amount: "" },
       navItems: [
        { id: 'dashboard', label: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
        { id: 'beneficiary', label: 'Beneficiaries', path: '/beneficiary', icon: Users },
        { id: 'transfer', label: 'Transfer Money', path: '/transfer', icon: Send },
        { id: 'history', label: 'Transactions', path: '/history', icon: FileText },
        { id: 'payments', label: 'Payments', path: '/payments', icon: Wallet },
        { id: 'chatbot', label: 'AI Assistant', path: '/chatbot', icon: MessageSquare }
      ]
    };
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
    handleLogout() {
      localStorage.clear();
      this.$router.push("/");
    },
    async fetchBillOptions() {
      try {
        const res = await axios.get("http://127.0.0.1:5000/customer/bill-options");
        this.billOptions = res.data;
      } catch (err) {
        console.error("Error loading bill options:", err);
      }
    },
    getBillerList(type) {
      switch (type) {
        case "Electricity":
          return this.billOptions.electricity_providers || [];
        case "Gas":
          return this.billOptions.gas_providers || [];
        case "Internet":
          return this.billOptions.internet_providers || [];
        case "Transport":
          return this.billOptions.transport_providers || [];
        case "Food":
          return this.billOptions.food_providers || [];
        case "Others":
          return this.billOptions.others_providers || [];
        default:
          return [];
      }
    },
    async payBill() {
      if (!this.bill.bill_type || !this.bill.biller || !this.bill.amount) {
        alert("Please fill all required fields");
        return;
      }

      try {
        // Step 1: Initiate Bill Payment
        const res = await axios.post("http://127.0.0.1:5000/customer/initiate-pay-bill", {
          customer_id: this.customerId,
          bill_type: this.bill.bill_type,
          biller: this.bill.biller,
          bill_account: this.bill.bill_account,
          amount: this.bill.amount
        });

        // Redirect to TransactionConfirmBill with required data
        this.$router.push({
          name: "TransactionConfirmBill",
          query: {
            session_id: res.data.session_id,
            type: "pay-bill",
            customer_id: this.customerId,
            bill_type: this.bill.bill_type,
            biller: this.bill.biller,
            bill_account: this.bill.bill_account,
            amount: this.bill.amount
          }
        });
      } catch (err) {
        alert(err.response?.data?.message || "Error initiating bill payment");
      }
    },
    async recharge() {
      if (!this.rechargeData.recharge_type || !this.rechargeData.operator || !this.rechargeData.number || !this.rechargeData.amount) {
        alert("Please fill all required fields");
        return;
      }

      try {
        // Step 1: Initiate Recharge
        const res = await axios.post("http://127.0.0.1:5000/customer/initiate-recharge", {
          customer_id: this.customerId,
          recharge_type: this.rechargeData.recharge_type,
          operator: this.rechargeData.operator,
          number: this.rechargeData.number,
          amount: this.rechargeData.amount
        });

        this.$router.push({
          name: "TransactionConfirmBill",
          query: {
            session_id: res.data.session_id,
            type: "recharge",
            customer_id: this.customerId,
            recharge_type: this.rechargeData.recharge_type,
            operator: this.rechargeData.operator,
            number: this.rechargeData.number,
            amount: this.rechargeData.amount
          }
        });
      } catch (err) {
        alert(err.response?.data?.message || "Error initiating recharge");
      }
    },
    async fastagTopup() {
      if (!this.fastag.vehicle_number || !this.fastag.amount) {
        alert("Please fill all required fields");
        return;
      }

      try {
        // Step 1: Initiate FASTag Top-up
        const res = await axios.post("http://127.0.0.1:5000/customer/initiate-fastag", {
          customer_id: this.customerId,
          vehicle_number: this.fastag.vehicle_number,
          tag_id: this.fastag.tag_id,
          amount: this.fastag.amount
        });

        this.$router.push({
          name: "TransactionConfirmBill",
          query: {
            session_id: res.data.session_id,
            type: "fastag",
            customer_id: this.customerId,
            vehicle_number: this.fastag.vehicle_number,
            tag_id: this.fastag.tag_id,
            amount: this.fastag.amount
          }
        });
      } catch (err) {
        alert(err.response?.data?.message || "Error initiating FASTag top-up");
      }
    },
  },
  mounted() {
    this.fetchBillOptions();
  },
};
</script>

<style scoped>
.font-sans {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
}

.logo-box {
  width: 48px;
  height: 48px;
}

.avatar {
  width: 40px;
  height: 40px;
}

.btn-ghost-dark {
  background: transparent;
  border: none;
}

.btn-ghost-dark:hover {
  background-color: rgba(255, 255, 255, 0.1);
  color: white !important;
}

.hover-text-white:hover {
  color: white !important;
}

.hover-bg-light:hover {
  background-color: #f8f9fa !important;
}

.hover-lift {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.hover-lift:hover {
  transform: translateY(-3px);
  box-shadow: 0 .5rem 1rem rgba(0,0,0,.15)!important;
}

.transition-all {
  transition: all 0.2s ease-in-out;
}

.bg-primary-subtle {
  background-color: rgba(13, 110, 253, 0.1);
}

.bg-success-subtle {
  background-color: rgba(25, 135, 84, 0.1);
}

.bg-warning-subtle {
    background-color: rgba(255, 193, 7, 0.1);
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
