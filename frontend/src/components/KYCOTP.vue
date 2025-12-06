<template>
  <v-container>
    <v-card class="pa-5 mx-auto" max-width="420">
      <v-card-title>KYC OTP Verification</v-card-title>
      <v-card-text>
        <v-text-field label="Enter OTP" v-model="otp" />
      </v-card-text>
      <v-card-actions>
        <v-btn block color="success" @click="verifyOTP">
          Verify OTP
        </v-btn>
      </v-card-actions>

      <v-alert v-if="msg" type="info" class="mt-2">{{ msg }}</v-alert>
    </v-card>
  </v-container>
</template>

<script setup>
import api from "../services/api";
import { ref } from "vue";
import { useRoute } from "vue-router";

const route = useRoute();
const otp = ref("");
const msg = ref("");

const verifyOTP = async () => {
  try {
    const res = await api.post(`/kyc/verify_otp/${route.params.customer_id}`, {
      otp: otp.value
    });

    msg.value =
      "KYC Verified. Your Account Number is: " + res.data.account_number +
      ". Wait for manager approval.";
  } catch (err) {
    msg.value = err.response?.data?.message || "OTP failed";
  }
};
</script>
