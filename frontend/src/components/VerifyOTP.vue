<!-- <template>
  <v-container>
    <v-card class="pa-5 mx-auto" max-width="400">
      <v-card-title>Verify OTP</v-card-title>
      <v-card-text>
        <v-text-field label="Email" v-model="email" />
        <v-text-field label="OTP" v-model="otp" />
      </v-card-text>
      <v-card-actions>
        <v-btn color="success" @click="verify">Verify</v-btn>
      </v-card-actions>
      <v-alert v-if="msg" type="info" class="mt-2">{{ msg }}</v-alert>
    </v-card>
  </v-container>
</template>

<script setup>
import api from "../services/api";
import { ref } from "vue";
import { useRouter } from "vue-router";

const email = ref("");
const otp = ref("");
const msg = ref("");
const router = useRouter();

const verify = async () => {
  const res = await api.post("/verify_otp", {
    email: email.value,
    otp: otp.value,
  });
  msg.value = res.data.message;

  if (res.data.message.includes("login successful")) {
    // Save the customer's name for dashboard display
    localStorage.setItem("customerName", email.value);
    // Redirect to dashboard
    router.push("/dashboard");
  }
};
</script> -->


<template>
  <v-container>
    <v-card class="pa-5 mx-auto" max-width="400">
      <v-card-title>Verify Login OTP</v-card-title>

      <v-card-text>
        <v-text-field label="OTP" v-model="otp" />
      </v-card-text>

      <v-card-actions>
        <v-btn block color="success" @click="verify">
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
import { useRouter } from "vue-router";

const otp = ref("");
const msg = ref("");
const router = useRouter();

// const verify = async () => {
//   const account_number = localStorage.getItem("temp_account_number");

//   const res = await api.post("/verify_otp", {
//     account_number,
//     otp: otp.value
//   });

//   msg.value = res.data.message;

//   if (res.data.message.includes("successful")) {
//     localStorage.setItem("logged_in_acc", account_number);
//     router.push("/dashboard");
//   }
// };

const verify = async () => {
  const account_number = localStorage.getItem("temp_account_number");

  const res = await api.post("/verify_otp", {
    account_number,
    otp: otp.value,
  });

  msg.value = res.data.message;

  if (res.data.message.includes("successful")) {
    // Save proper login details
    localStorage.setItem("customer_id", res.data.customer.id);
    localStorage.setItem("customer_name", res.data.customer.full_name);
    localStorage.setItem("account_number", res.data.customer.account_number);

    // Remove temp value
    localStorage.removeItem("temp_account_number");

    router.push("/dashboard");
  }
};

</script>
