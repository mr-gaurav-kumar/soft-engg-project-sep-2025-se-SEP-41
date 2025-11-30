<template>
  <div class="flex min-h-screen bg-gray-50">
    <!-- Sidebar Navigation -->
    <div class="w-64 bg-white border-r-2 border-gray-400 flex flex-col">
      <!-- Header -->
      <div class="p-6 border-b-2 border-gray-400">
        <div class="w-12 h-12 bg-gray-300 mb-2 flex items-center justify-center">
          <span class="text-gray-600">LOGO</span>
        </div>
        <h2 class="text-gray-800">Customer Portal</h2>
        <p class="text-gray-600">John Doe</p>
      </div>

      <!-- Navigation Buttons -->
      <nav class="flex-1 p-4 space-y-2">
        <button
          v-for="item in navItems"
          :key="item.id"
          @click="navigate(item.id)"
          :class="[
            'w-full flex items-center gap-3 px-4 py-3 border-2',
            currentPage === item.id
              ? 'bg-gray-800 text-white border-gray-800'
              : 'bg-white text-gray-800 border-gray-400 hover:bg-gray-100'
          ]"
        >
          <component :is="item.icon" class="w-5 h-5" />
          <span>{{ item.label }}</span>
        </button>
      </nav>

      <!-- Logout Button -->
      <div class="p-4 border-t-2 border-gray-400">
        <button
          class="w-full flex items-center gap-2 border-2 border-gray-400 bg-white hover:bg-gray-100 px-4 py-2"
          @click="$emit('go-back')"
        >
          <LogOut class="w-5 h-5" />
          Logout
        </button>
      </div>
    </div>

    <!-- Main Chat Area -->
    <div class="flex-1">
      <!-- Page Header -->
      <div class="border-b-2 border-gray-400 bg-white p-6">
        <h1 class="text-gray-800">
          AI Banking Assistant & Personal Spending Coach
        </h1>
        <p class="text-gray-600">
          Get instant help and personalized spending insights powered by local AI
        </p>
      </div>

      <!-- Chat Window -->
      <div class="p-6">
        <div
          class="max-w-4xl mx-auto bg-white border-2 border-gray-400 flex flex-col"
          style="height: calc(100vh - 250px);"
        >
          <!-- Chat Header -->
          <div class="p-4 border-b-2 border-gray-400 bg-gray-100 flex items-center gap-3">
            <div class="w-10 h-10 rounded-full bg-gray-300 flex items-center justify-center">
              <Bot class="w-6 h-6 text-gray-700" />
            </div>
            <div>
              <h3 class="text-gray-800">Banking Assistant</h3>
              <p class="text-gray-600">Online - Avg. response time: 2 sec</p>
            </div>
          </div>

          <!-- Messages -->
          <div class="flex-1 overflow-y-auto p-6 space-y-4">
            <div
              v-for="msg in messages"
              :key="msg.id"
              class="flex gap-3"
              :class="msg.type === 'user' ? 'flex-row-reverse' : 'flex-row'"
            >
              <div
                class="w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0"
                :class="msg.type === 'user' ? 'bg-gray-600' : 'bg-gray-300'"
              >
                <component
                  :is="msg.type === 'user' ? User : Bot"
                  class="w-5 h-5"
                  :class="msg.type === 'user' ? 'text-white' : 'text-gray-700'"
                />
              </div>

              <div class="max-w-lg flex flex-col" :class="msg.type === 'user' ? 'items-end' : 'items-start'">
                <div
                  class="p-4 border-2"
                  :class="msg.type === 'user'
                    ? 'bg-gray-800 text-white border-gray-800'
                    : 'bg-gray-100 text-gray-800 border-gray-300'"
                >
                  <p>{{ msg.text }}</p>

                  <!-- Spending Data -->
                  <div v-if="msg.spendingData" class="mt-4 space-y-3">
                    <div class="p-3 bg-white border-2 border-gray-400">
                      <div class="flex items-center justify-between mb-2">
                        <span class="text-gray-800">Total Spent on {{ msg.spendingData.category }}</span>
                        <span class="text-gray-800">₹{{ msg.spendingData.amount }}</span>
                      </div>
                      <p class="text-gray-600">Last Month Analysis</p>
                    </div>

                    <div class="space-y-2">
                      <p class="text-gray-800">Transaction Proof:</p>
                      <div
                        v-for="(txn, idx) in msg.spendingData.transactions"
                        :key="idx"
                        class="flex items-center justify-between p-2 bg-white border border-gray-300"
                      >
                        <div class="flex items-center gap-2">
                          <Coffee class="w-4 h-4 text-gray-600" />
                          <div>
                            <p class="text-gray-800">{{ txn.merchant }}</p>
                            <p class="text-gray-600">{{ txn.date }}</p>
                          </div>
                        </div>
                        <span class="text-gray-800">₹{{ txn.amount }}</span>
                      </div>
                    </div>

                    <div class="p-3 bg-yellow-50 border-2 border-yellow-300">
                      <div class="flex items-start gap-2">
                        <TrendingDown class="w-5 h-5 text-yellow-700 mt-0.5" />
                        <div>
                          <p class="text-gray-800">Spending Coach Recommendation:</p>
                          <p class="text-gray-600 mt-1">
                            You spent ₹4,500 on food last month. Try limiting it to ₹3,000 this month to save ₹1,500.
                            Consider home-cooked meals 2–3 times per week!
                          </p>
                        </div>
                      </div>
                    </div>

                    <div class="p-2 bg-white border border-gray-300">
                      <p class="text-gray-600">
                        💡 Data Source: Local SQLite database (transactions.db) - No internet required
                      </p>
                    </div>
                  </div>
                </div>
                <span class="text-gray-500 mt-1">{{ msg.time }}</span>
              </div>
            </div>
          </div>

          <!-- Quick Actions -->
          <div class="p-4 border-t-2 border-gray-400 bg-gray-50">
            <p class="text-gray-600 mb-2">Quick Actions:</p>
            <div class="flex flex-wrap gap-2">
              <button
                v-for="(action, index) in quickActions"
                :key="index"
                class="border border-gray-400 px-3 py-1 rounded hover:bg-gray-100"
                @click="handleQuickAction(action)"
              >
                {{ action }}
              </button>
            </div>
          </div>

          <!-- Input -->
          <div class="p-4 border-t-2 border-gray-400">
            <div class="flex gap-2">
              <input
                v-model="inputMessage"
                @keyup.enter="handleSendMessage"
                placeholder="Type your message..."
                class="flex-1 border border-gray-400 rounded px-3 py-2 outline-none focus:ring-2 focus:ring-gray-300"
              />
              <button
                @click="handleSendMessage"
                class="border border-gray-800 bg-gray-800 text-white px-4 py-2 flex items-center gap-2 hover:bg-gray-700"
              >
                <Send class="w-4 h-4" />
                Send
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { Bot, User, Coffee, TrendingDown, LogOut, Send, Home, Users, History, MessageSquare, Send as SendIcon } from 'lucide-vue-next'

export default {
  name: 'AIAssistant',
  props: ['currentPage'],
  components: { Bot, User, Coffee, TrendingDown, LogOut, Send, Home, Users, History, MessageSquare, SendIcon },
  emits: ['go-to-dashboard', 'go-to-beneficiary', 'go-to-transfer', 'go-to-transactions', 'go-to-aiassistant', 'go-back'],
  setup(_, { emit }) {
    const messages = ref([
      {
        id: 1,
        type: 'bot',
        text: "Hello! I'm your AI banking assistant. How can I help you today?",
        time: '10:00 AM'
      },
      {
        id: 2,
        type: 'bot',
        text: 'I can help you with account information, transaction queries, financial advice, and more.',
        time: '10:00 AM'
      }
    ])

    const inputMessage = ref('')
    const quickActions = ['Check my balance', 'Analyze my spending', 'Food spending tips', 'Monthly budget advice']

    function handleSendMessage() {
      if (!inputMessage.value.trim()) return
      const userMsg = {
        id: messages.value.length + 1,
        type: 'user',
        text: inputMessage.value,
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      }

      let botResponse
      if (inputMessage.value.toLowerCase().includes('food') || inputMessage.value.toLowerCase().includes('spending')) {
        botResponse = {
          id: messages.value.length + 2,
          type: 'bot',
          text: "I analyzed your food spending from local transaction history. Here's what I found:",
          time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
          spendingData: {
            category: 'Food & Dining',
            amount: 4500,
            transactions: [
              { date: '2025-10-12', merchant: 'Zomato Order', amount: 850 },
              { date: '2025-10-09', merchant: 'Restaurant ABC', amount: 1200 },
              { date: '2025-10-05', merchant: 'Grocery Store', amount: 2450 }
            ]
          }
        }
      } else {
        botResponse = {
          id: messages.value.length + 2,
          type: 'bot',
          text: "I'm your Personal Spending Coach powered by local AI. Try asking about your food spending or monthly budget!",
          time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        }
      }

      messages.value.push(userMsg, botResponse)
      inputMessage.value = ''
    }

    function handleQuickAction(action) {
      inputMessage.value = action
    }

    const navItems = [
      { id: 'dashboard', label: 'Dashboard', icon: Home },
      { id: 'beneficiary', label: 'Beneficiaries', icon: Users },
      { id: 'transfer', label: 'Transfer Money', icon: SendIcon },
      { id: 'transactions', label: 'Transactions', icon: History },
      { id: 'aiassistant', label: 'AI Assistant', icon: MessageSquare }
    ]

    function navigate(page) {
      emit(`go-to-${page}`)
    }

    return { messages, inputMessage, handleSendMessage, handleQuickAction, quickActions, navItems, navigate }
  }
}
</script>

<style scoped>
.flex {
  display: flex;
}
</style>