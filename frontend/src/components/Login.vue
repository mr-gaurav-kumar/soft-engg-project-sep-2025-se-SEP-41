<!-- <template>
  <v-container>
    <v-card class="pa-5 mx-auto" max-width="400">
      <v-card-title>Login</v-card-title>
      <v-card-text>
        <v-text-field label="Email" v-model="form.email" />
        <v-text-field label="Password" v-model="form.password" type="password" />
      </v-card-text>
      <v-card-actions>
        <v-btn color="primary" @click="login">Send OTP</v-btn>
      </v-card-actions>
      <v-alert v-if="otp" type="success" class="mt-2">
        OTP Sent: {{ otp }} (debug)
        <v-btn small color="primary" class="ml-2" @click="$router.push('/verify')">Verify OTP</v-btn>
      </v-alert>
    </v-card>
  </v-container>
</template>

<script setup>
import api from "../services/api";
import { ref } from "vue";

const form = ref({ email: "", password: "" });
const otp = ref("");

const login = async () => {
  const res = await api.post("/login", form.value);
  otp.value = res.data.otp;
};
</script> -->


<template>
  <v-container>
    <v-card class="pa-5 mx-auto" max-width="400">
      <v-card-title>Login</v-card-title>

      <v-card-text>
        <!-- Role Selection -->
        <v-select
          v-model="form.role"
          :items="roleOptions"
          label="Login as"
          item-title="text"
          item-value="value"
          @update:model-value="onRoleChange"
        ></v-select>

        <!-- Customer Login Fields -->
        <template v-if="form.role === 'customer' || !form.role">
          <v-text-field label="Account Number" v-model="form.account_number" />
          <v-text-field label="Login Password" type="password" v-model="form.password" />
        </template>

        <!-- Employee/Manager Login Fields -->
        <template v-else>
          <v-text-field label="Email" v-model="form.email" type="email" />
          <v-text-field label="Password" type="password" v-model="form.password" />
        </template>
      </v-card-text>

      <v-card-actions>
        <v-btn block color="primary" @click="login" :disabled="!isFormValid">
          {{ form.role === 'customer' || !form.role ? 'Send OTP' : 'Login' }}
        </v-btn>
      </v-card-actions>

      <v-alert v-if="errorMessage" type="error" class="mt-2">{{ errorMessage }}</v-alert>
      <v-alert v-if="debugOtp" type="success" class="mt-2">
        OTP (debug): {{ debugOtp }}
        <v-btn small class="ml-2" @click="$router.push('/verify')">Verify</v-btn>
      </v-alert>
      
      <v-card-text class="text-center pt-2">
        <span class="text-body-2">Don't have an account?</span>
        <v-btn variant="text" color="primary" @click="$router.push('/register')" class="ml-1">
          Register
        </v-btn>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import api from "../services/api";
import { ref, computed } from "vue";
import { useRouter } from "vue-router";

const router = useRouter(); 

const form = ref({ 
  role: 'customer', // Default to customer
  account_number: "", 
  email: "",
  password: "" 
});
const debugOtp = ref("");
const errorMessage = ref("");

const roleOptions = [
  { text: 'Customer', value: 'customer' },
  { text: 'Employee', value: 'employee' },
  { text: 'Manager', value: 'manager' }
];

const isFormValid = computed(() => {
  if (!form.value.role) return false;
  if (form.value.role === 'customer') {
    return form.value.account_number && form.value.password;
  } else {
    return form.value.email && form.value.password;
  }
});

const onRoleChange = () => {
  // Clear form when role changes
  form.value.account_number = "";
  form.value.email = "";
  form.value.password = "";
  errorMessage.value = "";
  debugOtp.value = "";
};

const login = async () => {
  errorMessage.value = "";
  debugOtp.value = "";

  try {
    if (form.value.role === 'customer') {
      // Customer login (existing flow)
      const res = await api.post("/login", {
        account_number: form.value.account_number,
        password: form.value.password
      });
      
      localStorage.setItem("temp_account_number", form.value.account_number);
      router.push("/verify");
    } else if (form.value.role === 'employee') {
      // Employee login
      const res = await api.post("/api/employee/login", {
        email: form.value.email,
        password: form.value.password
      });
      
      if (res.status === 201 || res.data?.message === "Login successful") {
        localStorage.setItem("employee_id", res.data.employee_id);
        localStorage.setItem("employee_name", res.data.name || "Employee");
        localStorage.setItem("employee_email", res.data.email);
        localStorage.setItem("user_role", "employee");
        router.push("/employee-dashboard");
      }
    } else if (form.value.role === 'manager') {
      // Manager login
      const res = await api.post("/api/manager/login", {
        email: form.value.email,
        password: form.value.password
      });
      
      if (res.status === 201 || res.data?.message === "Login successful") {
        localStorage.setItem("manager_id", res.data.manager_id);
        localStorage.setItem("manager_name", res.data.name || "Manager");
        localStorage.setItem("manager_email", res.data.email);
        localStorage.setItem("user_role", "manager");
        router.push("/manager-dashboard");
      }
    }
  } catch (err) {
    errorMessage.value = err.response?.data?.message || "Login failed. Please check your credentials.";
    console.error("Login error:", err);
  }
};
</script>
