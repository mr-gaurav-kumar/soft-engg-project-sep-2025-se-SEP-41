<!-- <template>
  <v-container>
    <v-card class="pa-5 mx-auto" max-width="400">
      <v-card-title>Register</v-card-title>
      <v-card-text>
        <v-text-field label="Full Name" v-model="form.full_name" />
        <v-text-field label="Email" v-model="form.email" />
        <v-text-field label="Phone" v-model="form.phone" />
        <v-text-field label="Password" v-model="form.password" type="password" />
      </v-card-text>
      <v-card-actions>
        <v-btn color="primary" @click="register">Register</v-btn>
      </v-card-actions>
      <v-alert v-if="msg" type="info" class="mt-2">{{ msg }}</v-alert>
    </v-card>
  </v-container>
</template>

<script setup>
import api from "../services/api";
import { ref } from "vue";

const form = ref({ full_name: "", email: "", phone: "", password: "" });
const msg = ref("");

const register = async () => {
  const res = await api.post("/register", form.value);
  msg.value = res.data.message;
};
</script> -->


<template>
  <v-container>
    <v-card class="pa-5 mx-auto" :max-width="form.role === 'customer' ? '500' : '450'">
      <v-card-title class="text-h5 mb-4">
        {{ form.role === 'customer' ? 'Register Customer' : form.role === 'employee' ? 'Register Employee' : 'Register Manager' }}
      </v-card-title>

      <v-card-text>
        <!-- Role Selection -->
        <v-select
          v-model="form.role"
          :items="roleOptions"
          label="Register as"
          item-title="text"
          item-value="value"
          @update:model-value="onRoleChange"
          class="mb-4"
        ></v-select>

        <!-- Customer Registration Fields -->
        <template v-if="form.role === 'customer' || !form.role">
          <v-text-field 
            label="Full Name" 
            v-model="form.full_name" 
            :rules="[rules.required]"
            class="mb-2"
          />
          <v-text-field 
            label="Email" 
            v-model="form.email" 
            type="email"
            :rules="[rules.required, rules.email]"
            class="mb-2"
          />
          <v-text-field 
            label="Phone" 
            v-model="form.phone" 
            :rules="[rules.required]"
            class="mb-2"
          />
          <v-text-field 
            label="Login Password" 
            type="password" 
            v-model="form.login_password"
            :rules="[rules.required, rules.minLength]"
            class="mb-2"
          />
          <v-text-field 
            label="Transaction Password" 
            type="password" 
            v-model="form.transaction_password"
            :rules="[rules.required, rules.minLength]"
            class="mb-2"
          />
        </template>

        <!-- Employee Registration Fields -->
        <template v-else-if="form.role === 'employee'">
          <v-text-field 
            label="Full Name" 
            v-model="form.name" 
            :rules="[rules.required]"
            class="mb-2"
          />
          <v-text-field 
            label="Email" 
            v-model="form.email" 
            type="email"
            :rules="[rules.required, rules.email]"
            class="mb-2"
          />
          <v-text-field 
            label="Contact Number" 
            v-model="form.contact_number" 
            :rules="[rules.required]"
            class="mb-2"
          />
          <v-text-field 
            label="Password" 
            type="password" 
            v-model="form.password"
            :rules="[rules.required, rules.minLength]"
            class="mb-2"
          />
          <v-text-field 
            label="Manager ID" 
            v-model="form.manager_id" 
            type="number"
            :rules="[rules.required]"
            hint="Enter the ID of the manager who will supervise you"
            persistent-hint
            class="mb-2"
          />
        </template>

        <!-- Manager Registration Fields -->
        <template v-else-if="form.role === 'manager'">
          <v-text-field 
            label="Full Name" 
            v-model="form.name" 
            :rules="[rules.required]"
            class="mb-2"
          />
          <v-text-field 
            label="Email" 
            v-model="form.email" 
            type="email"
            :rules="[rules.required, rules.email]"
            class="mb-2"
          />
          <v-text-field 
            label="Contact Number" 
            v-model="form.contact_number" 
            :rules="[rules.required]"
            class="mb-2"
          />
          <v-text-field 
            label="Password" 
            type="password" 
            v-model="form.password"
            :rules="[rules.required, rules.minLength]"
            class="mb-2"
          />
        </template>
      </v-card-text>

      <v-card-actions>
        <v-btn 
          color="primary" 
          block 
          @click="register" 
          :disabled="!isFormValid"
          :loading="loading"
        >
          {{ getRegisterButtonText() }}
        </v-btn>
      </v-card-actions>

      <v-alert v-if="msg" :type="msgType" class="mt-2">{{ msg }}</v-alert>
      
      <v-card-text class="text-center pt-2">
        <span class="text-body-2">Already have an account?</span>
        <v-btn variant="text" color="primary" @click="$router.push('/login')" class="ml-1">
          Login
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
const msg = ref("");
const msgType = ref("info");
const loading = ref(false);

const form = ref({
  role: 'customer', // Default to customer
  // Customer fields
  full_name: "",
  email: "",
  phone: "",
  login_password: "",
  transaction_password: "",
  // Employee/Manager fields
  name: "",
  contact_number: "",
  password: "",
  manager_id: ""
});

const roleOptions = [
  { text: 'Customer', value: 'customer' },
  { text: 'Employee', value: 'employee' },
  { text: 'Manager', value: 'manager' }
];

const rules = {
  required: (value) => !!value || 'This field is required',
  email: (value) => {
    const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    return pattern.test(value) || 'Invalid email address'
  },
  minLength: (value) => (value && value.length >= 6) || 'Password must be at least 6 characters'
};

const isFormValid = computed(() => {
  if (!form.value.role) return false;
  
  if (form.value.role === 'customer') {
    return form.value.full_name && 
           form.value.email && 
           form.value.phone && 
           form.value.login_password && 
           form.value.transaction_password;
  } else if (form.value.role === 'employee') {
    return form.value.name && 
           form.value.email && 
           form.value.contact_number && 
           form.value.password && 
           form.value.manager_id;
  } else if (form.value.role === 'manager') {
    return form.value.name && 
           form.value.email && 
           form.value.contact_number && 
           form.value.password;
  }
  return false;
});

const onRoleChange = () => {
  // Clear all form fields when role changes
  form.value.full_name = "";
  form.value.email = "";
  form.value.phone = "";
  form.value.login_password = "";
  form.value.transaction_password = "";
  form.value.name = "";
  form.value.contact_number = "";
  form.value.password = "";
  form.value.manager_id = "";
  msg.value = "";
  msgType.value = "info";
};

const getRegisterButtonText = () => {
  if (form.value.role === 'customer') {
    return 'Continue to KYC';
  } else if (form.value.role === 'employee') {
    return 'Register Employee';
  } else {
    return 'Register Manager';
  }
};

const register = async () => {
  loading.value = true;
  msg.value = "";
  msgType.value = "info";

  try {
    if (form.value.role === 'customer') {
      // Customer registration
      const res = await api.post("/register", {
        full_name: form.value.full_name,
        email: form.value.email,
        phone: form.value.phone,
        login_password: form.value.login_password,
        transaction_password: form.value.transaction_password
      });
      
      msg.value = res.data.message;
      msgType.value = "success";
      
      // Go to KYC upload
      setTimeout(() => {
        router.push(`/kyc-upload/${res.data.customer_id}`);
      }, 1500);
      
    } else if (form.value.role === 'employee') {
      // Employee registration
      const res = await api.post("/api/employee/register", {
        name: form.value.name,
        email: form.value.email,
        password: form.value.password,
        contact_number: form.value.contact_number,
        manager_id: parseInt(form.value.manager_id)
      });
      
      msg.value = res.data.message;
      msgType.value = res.status === 201 ? "success" : "error";
      
      if (res.status === 201) {
        setTimeout(() => {
          router.push("/login");
        }, 2000);
      }
      
    } else if (form.value.role === 'manager') {
      // Manager registration
      const res = await api.post("/api/manager/register", {
        name: form.value.name,
        email: form.value.email,
        password: form.value.password,
        contact_number: form.value.contact_number
      });
      
      msg.value = res.data.message;
      msgType.value = res.status === 201 ? "success" : "error";
      
      if (res.status === 201) {
        setTimeout(() => {
          router.push("/login");
        }, 2000);
      }
    }
  } catch (e) {
    msg.value = e.response?.data?.message || "Registration failed. Please try again.";
    msgType.value = "error";
    console.error("Registration error:", e);
  } finally {
    loading.value = false;
  }
};
</script>
