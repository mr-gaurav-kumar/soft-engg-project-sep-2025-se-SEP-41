<template>
  <v-container>
    <v-card class="pa-5 mx-auto" max-width="600">
      <v-card-title>Upload KYC Documents</v-card-title>

      <v-card-text>
        <v-file-input label="Aadhaar (PDF/Image)" v-model="aadhaar" />
        <v-file-input label="PAN (PDF/Image)" v-model="pan" />
        <v-file-input label="Photo" v-model="photo" />
        <v-file-input label="Signature" v-model="signature" />
      </v-card-text>

      <v-card-actions>
        <v-btn block color="primary" @click="uploadKYC">Submit KYC</v-btn>
      </v-card-actions>

      <v-alert v-if="msg" type="info" class="mt-2">{{ msg }}</v-alert>
    </v-card>
  </v-container>
</template>

<script setup>
import api from "../services/api";
import { ref } from "vue";
import { useRoute, useRouter } from "vue-router";

const route = useRoute();
const router = useRouter();
const msg = ref("");

const aadhaar = ref(null);
const pan = ref(null);
const photo = ref(null);
const signature = ref(null);

const uploadKYC = async () => {
  const formData = new FormData();
  formData.append("aadhaar", aadhaar.value);
  formData.append("pan", pan.value);
  formData.append("photo", photo.value);
  formData.append("signature", signature.value);

  try {
    await api.post(`/kyc/upload/${route.params.customer_id}`, formData, {
      headers: { "Content-Type": "multipart/form-data" }
    });

    msg.value = "KYC Uploaded. Sending OTP...";

    await api.post(`/kyc/send_otp/${route.params.customer_id}`);

    router.push(`/kyc-otp/${route.params.customer_id}`);

  } catch (err) {
    msg.value = err.response?.data?.message || "Upload failed";
  }
};
</script>
