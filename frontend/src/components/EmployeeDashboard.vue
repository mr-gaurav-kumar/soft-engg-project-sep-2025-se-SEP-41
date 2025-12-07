<template>
  <div class="d-flex min-vh-100">
    <!-- Sidebar Navigation -->
    <div class="sidebar d-flex flex-column" style="width: 280px; background-color: #1e293b; color: white;">
      <div class="p-4 mb-2">
        <div class="d-flex align-items-center gap-3 mb-4">
          <div class="logo-box bg-primary bg-gradient text-white rounded-3 d-flex align-items-center justify-content-center shadow-sm" style="width: 48px; height: 48px;">
            <span class="fw-bold fs-4">E</span>
          </div>
          <div>
            <h5 class="fw-bold text-white mb-0">Employee Portal</h5>
            <small class="text-white-50">{{ employeeName || 'Employee' }}</small>
          </div>
        </div>
      </div>

      <div class="flex-grow-1 px-3">
        <p class="text-uppercase text-white-50 fw-bold ms-2 mb-2" style="font-size: 0.75rem; letter-spacing: 1px;">Menu</p>
        <div class="d-grid gap-1">
          <button
            v-for="item in navItems"
            :key="item.id"
            @click="navigate(item.path)"
            :class="[
              'btn text-start d-flex align-items-center gap-3 px-3 py-2 rounded-3 transition-all',
              isActiveRoute(item.path)
                ? 'bg-primary text-white shadow-sm'
                : 'btn-ghost-dark text-white-50 hover-text-white'
            ]"
          >
            <component :is="item.icon" :size="20" />
            <span class="fw-medium">{{ item.label }}</span>
          </button>
        </div>
      </div>

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

    <!-- Main Content Area -->
    <div class="flex-grow-1 overflow-auto" style="background-color: #f4f7f6;">
      <!-- Router View for Nested Routes -->
      <router-view></router-view>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import { LogOut, LayoutDashboard, FileText, AlertCircle } from "lucide-vue-next";

const router = useRouter();
const route = useRoute();
const employeeName = ref(localStorage.getItem("employee_name") || "Employee");

const navItems = [
  { id: 'dashboard', label: 'Dashboard', path: '/employee-dashboard', icon: LayoutDashboard },
  { id: 'pending-kyc', label: 'Pending KYC', path: '/employee-dashboard/pending-kyc', icon: FileText },
  { id: 'customer-issues', label: 'Customer Issues', path: '/employee-dashboard/customer-issues', icon: AlertCircle }
];

const isActiveRoute = (path) => {
  if (path === '/employee-dashboard') {
    return route.path === '/employee-dashboard' || route.path === '/employee-dashboard/';
  }
  return route.path === path || route.path.startsWith(path + '/');
};

const navigate = (path) => {
  router.push(path);
};

const handleLogout = () => {
  localStorage.removeItem("employee_id");
  localStorage.removeItem("employee_name");
  localStorage.removeItem("employee_email");
  localStorage.removeItem("user_role");
  router.push("/");
};
</script>

<style scoped>
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

.transition-all {
  transition: all 0.2s ease-in-out;
}

.logo-box {
  width: 48px;
  height: 48px;
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
</style>
