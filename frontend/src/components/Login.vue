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
        <v-text-field label="Account Number" v-model="form.account_number" />
        <v-text-field label="Login Password" type="password" v-model="form.password" />
      </v-card-text>

      <v-card-actions>
        <v-btn block color="primary" @click="login">Send OTP</v-btn>
      </v-card-actions>

      <v-alert v-if="debugOtp" type="success" class="mt-2">
        OTP (debug): {{ debugOtp }}
        <v-btn small class="ml-2" @click="$router.push('/login-otp')">Verify</v-btn>
      </v-alert>
    </v-card>
  </v-container>
</template>

<script setup>
import api from "../services/api";
import { ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter(); 

const form = ref({ account_number: "", password: "" });
const debugOtp = ref("");

const login = async () => {
  const res = await api.post("/login", form.value);
  // debugOtp.value = res.data.otp;

  localStorage.setItem("temp_account_number", form.value.account_number);

  router.push("/verify");
};
</script>
