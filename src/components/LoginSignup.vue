<template>
  <div class="secure-banking-portal">
    
    <header class="banking-header">
      <h1>💰 Welcome to **Secure Digital Banking**</h1>
      <p>Your trusted portal for seamless financial management.</p>
    </header>

    <div class="security-alert-bar">
      <div class="scroll-text">
        <p>
          🚨 **SECURITY ALERT:** Never share your password, OTP, or account details with anyone. Secure Banking will *never* ask for this information via phone or email. Always verify the URL: **https://secure.banking.portal.com**
        </p>
      </div>
    </div>
    
    ---

    <div class="form-section">
      <div class="toggle-buttons">
        <button 
          :class="{ active: isLoginMode }" 
          @click="isLoginMode = true; clearMessages();"
        >
          Customer Login
        </button>
        <button 
          :class="{ active: !isLoginMode }" 
          @click="isLoginMode = false; clearMessages();"
        >
          New Account Sign Up
        </button>
      </div>

      <div class="form-wrapper">
        <form v-if="isLoginMode" @submit.prevent="handleLogin" class="auth-form">
          <h3>Sign In to Your Account</h3>
          
          <select v-model="loginData.role" required>
            <option value="" disabled>Login as: Customer, Employee, or Manager</option>
            <option value="customer">Customer</option>
            <option value="employee">Employee</option>
            <option value="manager">Manager</option>
          </select>

          <input 
            v-model="loginData.email" 
            type="email" 
            placeholder="Email Address" 
            required 
          />
          <input 
            v-model="loginData.password" 
            type="password" 
            placeholder="Password" 
            required 
          />
          <button type="submit">Secure Login</button>
          <p v-if="loginMessage" class="feedback-message success">{{ loginMessage }}</p>
          <a href="#" class="forgot-link">Forgot Password?</a>
        </form>

        <form v-else @submit.prevent="handleSignup" class="auth-form">
          <h3>Open a New Account</h3>
          
          <input 
            v-model="signupData.email" 
            type="email" 
            placeholder="Email (for communication)" 
            required 
          />
          <input 
            v-model="signupData.mobileNo" 
            type="tel" 
            placeholder="Mobile Number (10 digits)" 
            pattern="[0-9]{10}"
            title="Mobile number must be 10 digits"
            required 
          />
          <input 
            v-model="signupData.accountNo" 
            type="text" 
            placeholder="Account Number (If existing/pre-approved)" 
            required 
          />
          <input 
            v-model="signupData.password" 
            type="password" 
            placeholder="Create Password" 
            required 
          />
          
          <button type="submit">Register and Proceed</button>
          <p v-if="signupMessage" class="feedback-message success">{{ signupMessage }}</p>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';

// --- State Management ---
const isLoginMode = ref(true); 

const loginData = reactive({
  role: '',
  email: '',
  password: ''
});

const signupData = reactive({
  email: '',
  mobileNo: '',
  accountNo: '',
  password: ''
});

const loginMessage = ref('');
const signupMessage = ref('');


// --- Methods ---

const clearMessages = () => {
    loginMessage.value = '';
    signupMessage.value = '';
}

const handleLogin = () => {
  clearMessages();
  if (!loginData.role) {
    loginMessage.value = '🛑 Error: Please select your user role before logging in.';
    return;
  }
  
  // In a real app: Perform API call to authenticate user
  console.log('Attempting Login with:', { role: loginData.role, email: loginData.email });

  // Simulate success
  setTimeout(() => {
    loginMessage.value = `✅ Login successful as **${loginData.role.toUpperCase()}**! Redirecting...`;
    
    // Clear data after success (or redirect)
    setTimeout(() => {
      loginMessage.value = '';
      loginData.email = '';
      loginData.password = '';
    }, 4000);
  }, 500);
};

const handleSignup = () => {
  clearMessages();
  
  // In a real app: Perform API call to register new user
  console.log('Attempting Sign Up with:', signupData);

  // Simulate success
  setTimeout(() => {
    signupMessage.value = `✅ Registration received! Welcome, your account setup is being processed.`;
    
    // Clear form data after submission
    setTimeout(() => {
        signupMessage.value = '';
        signupData.email = '';
        signupData.mobileNo = '';
        signupData.accountNo = '';
        signupData.password = '';
    }, 4000);
  }, 500);
};
</script>

<style scoped>
/* --- Component Structure & Theme --- */
.secure-banking-portal {
  max-width: 900px;
  margin: 40px auto;
  padding: 30px;
  background: #ffffff;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* --- Header Styling --- */
.banking-header {
  text-align: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 2px solid #0056b3;
}

.banking-header h1 {
  color: #0056b3;
  font-size: 2.2em;
  font-weight: 700;
}

.banking-header p {
  color: #555;
  font-size: 1.1em;
}

/* --- Security Alert (Moving Notification) --- */
.security-alert-bar {
  background-color: #ffe0b2;
  color: #e65100;
  padding: 8px 0;
  margin-bottom: 25px;
  overflow: hidden;
  white-space: nowrap;
  border-radius: 4px;
  border: 1px solid #ffcc80;
}

.scroll-text {
  display: inline-block;
  padding-left: 100%;
  animation: scroll-left 40s linear infinite;
}

.scroll-text p {
  margin: 0;
  font-weight: 600;
}

@keyframes scroll-left {
  0% {
    transform: translateX(0%);
  }
  100% {
    transform: translateX(-100%);
  }
}

/* --- Form Styling --- */
.form-section {
    padding-top: 20px;
}

.toggle-buttons {
  display: flex;
  margin-bottom: 30px;
  border-radius: 6px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.toggle-buttons button {
  flex-grow: 1;
  padding: 12px;
  border: none;
  background-color: #f1f1f1;
  color: #333;
  cursor: pointer;
  font-weight: 600;
  font-size: 1.05em;
  transition: background-color 0.3s, color 0.3s;
}

.toggle-buttons button.active {
  background-color: #0056b3; 
  color: white;
  box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.2);
}

.toggle-buttons button:not(.active):hover {
  background-color: #e0e0e0;
}

.auth-form {
  display: flex;
  flex-direction: column;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: #fafafa;
}

.auth-form h3 {
  text-align: center;
  margin-bottom: 25px;
  color: #333;
}

.auth-form input,
.auth-form select {
  padding: 12px;
  margin-bottom: 20px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 1em;
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
}

.auth-form button {
  padding: 14px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1.1em;
  font-weight: bold;
  transition: background-color 0.3s;
}

.auth-form button:hover {
  background-color: #0056b3;
}

.forgot-link {
    text-align: right;
    margin-top: 10px;
    color: #007bff;
    text-decoration: none;
    font-size: 0.9em;
}

/* --- Feedback Messages --- */
.feedback-message {
    padding: 12px;
    margin-top: 15px;
    border-radius: 4px;
    text-align: center;
    font-weight: bold;
}

.success {
    background-color: #d4edda;
    color: #155724;
    border: 1px solid #c3e6cb;
}
</style>