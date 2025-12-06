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
    <v-card class="pa-5 mx-auto" max-width="500">
      <v-card-title>Register Customer</v-card-title>
      <v-card-text>
        <v-text-field label="Full Name" v-model="form.full_name" />
        <v-text-field label="Email" v-model="form.email" />
        <v-text-field label="Phone" v-model="form.phone" />
        <v-text-field label="Login Password" type="password" v-model="form.login_password" />
        <v-text-field label="Transaction Password" type="password" v-model="form.transaction_password" />
      </v-card-text>

      <v-card-actions>
        <v-btn color="primary" block @click="registerCustomer">
          Continue to KYC
        </v-btn>
      </v-card-actions>

      <v-alert v-if="msg" type="info" class="mt-2">{{ msg }}</v-alert>
    </v-card>
  </v-container>
</template>

<script setup>
import api from "../services/api";
import { ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const msg = ref("");
const form = ref({
  full_name: "",
  email: "",
  phone: "",
  login_password: "",
  transaction_password: ""
});

const registerCustomer = async () => {
  try {
    const res = await api.post("/register", form.value);
    msg.value = res.data.message;

    // Go to KYC upload        
    router.push(`/kyc-upload/${res.data.customer_id}`);
  } catch (e) {
    msg.value = e.response?.data?.message || "Error!";
  }
};
</script>
