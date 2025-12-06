<template>
  <v-container class="fill-height d-flex flex-column justify-center align-center">
    <v-card class="pa-8 text-center" elevation="6" max-width="600">
      <v-card-title class="text-h4 font-weight-bold mb-4">
        Welcome to Privault Banking App
      </v-card-title>
      <v-card-text class="text-body-1 mb-6">
        Manage your banking operations, track expenses, and stay secure — all in one place.
      </v-card-text>

      <v-btn color="primary" class="mr-4" @click="$router.push('/login')">
        Login
      </v-btn>

      <v-btn color="secondary" outlined @click="$router.push('/register')">
        Register
      </v-btn>
    </v-card>
  </v-container>
</template>

<script>
export default {
  name: "HomePage",
};
</script>

<style scoped>
.v-card {
  border-radius: 20px;
}
</style>
