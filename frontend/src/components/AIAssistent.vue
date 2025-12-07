<template>
  <div class="d-flex min-vh-100 bg-light font-sans">
    <!-- Sidebar -->
    <div class="sidebar d-flex flex-column shadow-sm" style="width: 280px; z-index: 1000; background-color: #1e293b;">
      <!-- Logo/Header -->
      <div class="p-4 mb-2">
        <div class="d-flex align-items-center gap-3 mb-4">
          <div class="logo-box bg-primary bg-gradient text-white rounded-3 d-flex align-items-center justify-content-center shadow-sm">
            <span class="fw-bold fs-4">S</span>
          </div>
          <div>
            <h5 class="fw-bold text-white mb-0">Sep Bank</h5>
            <small class="text-white-50">Premium Banking</small>
          </div>
        </div>
        
        <div class="user-profile p-3 rounded-3 d-flex align-items-center gap-3" style="background-color: rgba(255,255,255,0.05);">
          <div class="avatar bg-primary text-white rounded-circle d-flex align-items-center justify-content-center fw-bold">
            {{ customerInitials }}
          </div>
          <div class="overflow-hidden">
            <h6 class="text-white mb-0 text-truncate">{{ customerName }}</h6>
            
          </div>
        </div>
      </div>

      <!-- Navigation -->
      <div class="flex-grow-1 px-3">
        <p class="text-uppercase text-white-50 fw-bold ms-2 mb-2" style="font-size: 0.75rem; letter-spacing: 1px;">Menu</p>
        <div class="d-grid gap-1">
          <button
            v-for="item in navItems"
            :key="item.id"
            @click="navigate(item.path)"
            :class="[
              'btn text-start d-flex align-items-center gap-3 px-3 py-2 rounded-3 transition-all',
              $route.path === item.path || (item.id === 'chatbot')
                ? 'bg-primary text-white shadow-sm'
                : 'btn-ghost-dark text-white-50 hover-text-white'
            ]"
          >
            <component :is="item.icon" :size="20" />
            <span class="fw-medium">{{ item.label }}</span>
          </button>
        </div>
      </div>

      <!-- Logout -->
      <div class="p-3 border-top border-secondary border-opacity-25">
        <button class="btn btn-ghost-dark text-danger-emphasis w-100 d-flex align-items-center justify-content-center gap-2 py-2 hover-bg-danger-subtle" @click="handleLogout">
          <LogOut :size="18" />
          <span class="fw-medium">Sign Out</span>
        </button>
      </div>
    </div>

    <!-- Main Content -->
    <div class="flex-grow-1 d-flex flex-column h-100 overflow-hidden">
      <!-- Header -->
      <header class="bg-white border-bottom border-light px-4 py-3 d-flex justify-content-between align-items-center shadow-sm z-1">
        <div>
          <h4 class="fw-bold text-dark mb-0">AI Assistant</h4>
          <p class="text-muted mb-0 small">Your personal financial advisor.</p>
        </div>
        <div class="d-flex align-items-center gap-2">
          <div class="badge bg-success-subtle text-success border border-success-subtle d-flex align-items-center gap-1 px-3 py-2 rounded-pill">
            <div class="rounded-circle bg-success" style="width: 8px; height: 8px;"></div>
            <span>Online</span>
          </div>
        </div>
      </header>

      <!-- Chat Area -->
      <div class="flex-grow-1 bg-light p-4 overflow-auto d-flex flex-column">
        <div class="container-fluid p-0 h-100 d-flex flex-column" style="max-width: 900px;">
          
          <!-- Messages List -->
          <div class="flex-grow-1 d-flex flex-column gap-4 mb-4">
            <div
              v-for="msg in messages"
              :key="msg.id"
              class="d-flex gap-3"
              :class="msg.type === 'user' ? 'flex-row-reverse' : 'flex-row'"
            >
              <!-- Avatar -->
              <div
                class="rounded-circle d-flex align-items-center justify-content-center flex-shrink-0 shadow-sm"
                :class="msg.type === 'user' ? 'bg-primary text-white' : 'bg-white text-primary'"
                style="width: 40px; height: 40px;"
              >
                <component :is="msg.type === 'user' ? User : Bot" :size="20" />
              </div>

              <!-- Message Bubble -->
              <div class="d-flex flex-column" :class="msg.type === 'user' ? 'align-items-end' : 'align-items-start'" style="max-width: 75%;">
                <div
                  class="p-3 shadow-sm"
                  :class="[
                    msg.type === 'user' 
                      ? 'bg-primary text-white rounded-top-left-3 rounded-bottom-3' 
                      : 'bg-white text-dark rounded-top-right-3 rounded-bottom-3'
                  ]"
                  style="border-radius: 1rem;"
                >
                  <p class="mb-0" style="white-space: pre-wrap;">{{ msg.text }}</p>

                  <!-- Rich Content: Spending Data -->
                  <div v-if="msg.spendingData" class="mt-3">
                    <div class="card border-0 shadow-sm overflow-hidden mb-2">
                      <div class="card-body p-3 bg-light">
                        <div class="d-flex justify-content-between align-items-center mb-2">
                          <span class="text-secondary small fw-bold text-uppercase">{{ msg.spendingData.category }}</span>
                          <span class="text-dark fw-bold">₹{{ msg.spendingData.amount }}</span>
                        </div>
                        <div class="progress" style="height: 6px;">
                          <div class="progress-bar bg-warning" role="progressbar" style="width: 75%"></div>
                        </div>
                        <small class="text-muted mt-1 d-block">75% of monthly budget used</small>
                      </div>
                    </div>

                    <div class="bg-white rounded-3 border border-light overflow-hidden">
                      <div v-for="(txn, idx) in msg.spendingData.transactions" :key="idx" class="d-flex justify-content-between align-items-center p-2 border-bottom border-light last-border-0">
                        <div class="d-flex align-items-center gap-2">
                          <div class="bg-light rounded p-1">
                            <Coffee :size="14" class="text-secondary" />
                          </div>
                          <div>
                            <div class="fw-medium text-dark small">{{ txn.merchant }}</div>
                            <div class="text-muted x-small" style="font-size: 0.75rem;">{{ txn.date }}</div>
                          </div>
                        </div>
                        <span class="fw-bold text-dark small">₹{{ txn.amount }}</span>
                      </div>
                    </div>
                  </div>
                </div>
                <small class="text-muted mt-1 mx-1" style="font-size: 0.75rem;">{{ msg.time }}</small>
              </div>
            </div>
            
            <!-- Loading Indicator -->
            <div v-if="isLoading" class="d-flex gap-3">
              <div class="rounded-circle d-flex align-items-center justify-content-center flex-shrink-0 shadow-sm bg-white text-primary" style="width: 40px; height: 40px;">
                <Bot :size="20" />
              </div>
              <div class="d-flex align-items-start">
                <div class="p-3 shadow-sm bg-white text-dark rounded-top-right-3 rounded-bottom-3" style="border-radius: 1rem;">
                  <div class="d-flex gap-2 align-items-center">
                    <div class="spinner-border spinner-border-sm text-primary" role="status">
                      <span class="visually-hidden">Loading...</span>
                    </div>
                    <span class="text-muted small">Thinking...</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>

      <!-- Input Area -->
      <div class="bg-white border-top border-light p-4">
        <div class="container-fluid p-0" style="max-width: 900px;">
          <!-- Quick Actions -->
          <div class="d-flex gap-2 mb-3 overflow-auto pb-2 no-scrollbar">
            <button
              v-for="(action, index) in quickActions"
              :key="index"
              class="btn btn-outline-secondary btn-sm rounded-pill text-nowrap px-3 hover-bg-light"
              @click="handleQuickAction(action)"
            >
              {{ action }}
            </button>
          </div>

          <div class="input-group input-group-lg shadow-sm rounded-pill overflow-hidden border border-light">
            <input
              v-model="inputMessage"
              @keyup.enter="handleSendMessage"
              type="text"
              class="form-control border-0 bg-light ps-4"
              placeholder="Ask me anything about your finances..."
              :disabled="isLoading"
            />
            <button 
              class="btn btn-primary px-4 d-flex align-items-center gap-2" 
              @click="handleSendMessage"
              :disabled="isLoading || !inputMessage.trim()"
            >
              <span v-if="!isLoading">Send</span>
              <span v-else class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
              <Send v-if="!isLoading" :size="18" />
            </button>
          </div>
          <div class="text-center mt-2">
            <small class="text-muted x-small">AI can make mistakes. Please verify important information.</small>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { 
  LayoutDashboard, 
  Users, 
  Send, 
  FileText, 
  MessageSquare, 
  LogOut, 
  Bot, 
  User, 
  Coffee, 
  TrendingDown,
  Wallet
} from 'lucide-vue-next'

import axios from 'axios'

export default {
  name: 'AIAssistant',
  components: {
    LayoutDashboard,
    Users,
    Send,
    FileText,
    MessageSquare,
    LogOut,
    Bot,
    User,
    Coffee,
    TrendingDown,
    Wallet
  },
  setup() {
    const router = useRouter()
    const customerName = localStorage.getItem("customer_name") || "Customer"
    
    const customerInitials = computed(() => {
      return customerName
        .split(' ')
        .map(n => n[0])
        .join('')
        .toUpperCase()
        .slice(0, 2)
    })

    const navItems = [
      { id: 'dashboard', label: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
      { id: 'beneficiary', label: 'Beneficiaries', path: '/beneficiary', icon: Users },
      { id: 'transfer', label: 'Transfer Money', path: '/transfer', icon: Send },
      { id: 'history', label: 'Transactions', path: '/history', icon: FileText },
      { id: 'payments', label: 'Payments', path: '/payments', icon: Wallet },
      { id: 'chatbot', label: 'AI Assistant', path: '/chatbot', icon: MessageSquare },
    ]

    const messages = ref([
      {
        id: 1,
        type: 'bot',
        text: "Hello! I'm your personal spending coach and banking assistant. How can I help you today?",
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      },
      {
        id: 2,
        type: 'bot',
        text: 'I can analyze your spending patterns, provide financial advice, answer account questions, and help you make better financial decisions. Try asking me about your spending habits!',
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      }
    ])

    const inputMessage = ref('')
    const customerId = Number(localStorage.getItem('customer_id'))
    const quickActions = ['Analyze my spending', 'Food spending tips', 'Travel spending advice', 'Shopping habits']
    const isLoading = ref(false)

    // Check if message is asking for spending analysis
    function isSpendingQuery(message) {
      const spendingKeywords = ['spending', 'expense', 'expenditure', 'budget', 'spend', 'food', 'travel', 'shopping', 'habits', 'analyze', 'analysis']
      const lowerMsg = message.toLowerCase()
      return spendingKeywords.some(keyword => lowerMsg.includes(keyword))
    }

    async function handleSendMessage() {
      if (!inputMessage.value.trim() || isLoading.value) return
      
      const userMsg = {
        id: messages.value.length + 1,
        type: 'user',
        text: inputMessage.value,
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      }

      messages.value.push(userMsg)
      inputMessage.value = ''
      isLoading.value = true

      let botResponse
      const nextId = messages.value.length + 1
      
      try {
        // Check if it's a spending-related query
        if (isSpendingQuery(userMsg.text) && customerId && !isNaN(customerId)) {
          // Use spending coach endpoint
          console.log('Using spending coach endpoint for customer:', customerId)
          const res = await axios.get(`http://127.0.0.1:5000/api/customer/coach/${customerId}`, {
            timeout: 300000 // 5 minutes timeout for AI processing
          })
          console.log('Spending coach response:', res.data)
          botResponse = {
            id: nextId,
            type: 'bot',
            text: res.data.advice || "I've analyzed your spending patterns. Here are some insights...",
            time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
          }
        } else {
          // Use general chat endpoint
          console.log('Using general chat endpoint, customerId:', customerId)
          const res = await axios.post('http://127.0.0.1:5000/api/chat', {
            message: userMsg.text,
            user_id: customerId && !isNaN(customerId) ? customerId : null
          }, {
            timeout: 300000 // 5 minutes timeout for AI processing
          })
          console.log('General chat response:', res.data)
          botResponse = {
            id: nextId,
            type: 'bot',
            text: res.data.response || "I'm here to help with your banking needs.",
            time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
          }
        }
      } catch (error) {
        console.error('AI Assistant Error:', error)
        console.error('Error details:', error.response?.data, error.message)
        botResponse = {
          id: nextId,
          type: 'bot',
          text: error.response?.data?.error || error.message || "Sorry, I'm having trouble connecting to the server. Please try again.",
          time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        }
      }

      messages.value.push(botResponse)
      isLoading.value = false
      
      // Auto-scroll to bottom
      setTimeout(() => {
        const chatArea = document.querySelector('.overflow-auto')
        if (chatArea) {
          chatArea.scrollTop = chatArea.scrollHeight
        }
      }, 100)
    }

    async function handleQuickAction(action) {
      inputMessage.value = action
      await handleSendMessage()
    }

    const handleLogout = () => {
      localStorage.clear()
      router.push('/')
    }

    return { 
      navItems, 
      messages, 
      inputMessage, 
      quickActions, 
      handleSendMessage, 
      handleQuickAction,
      handleLogout,
      customerName,
      customerInitials,
      isLoading
    }
  },
  methods: {
    navigate(path) {
      this.$router.push(path)
    }
  }
}
</script>

<style scoped>
.font-sans {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
}

.logo-box {
  width: 48px;
  height: 48px;
}

.avatar {
  width: 40px;
  height: 40px;
}

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
  transition: all 0.3s ease;
}

.rounded-top-left-3 { border-top-left-radius: 1rem !important; }
.rounded-top-right-3 { border-top-right-radius: 1rem !important; }
.rounded-bottom-3 { border-bottom-left-radius: 1rem !important; border-bottom-right-radius: 1rem !important; }

.last-border-0:last-child {
  border-bottom: none !important;
}

.no-scrollbar::-webkit-scrollbar {
  display: none;
}
.no-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.hover-bg-light:hover {
  background-color: #f8f9fa !important;
}
</style>
