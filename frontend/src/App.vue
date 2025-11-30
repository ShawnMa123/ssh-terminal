<template>
  <div class="app">
    <aside class="sidebar">
      <div class="sidebar-header">
        <h1>🖥️ SSH Client</h1>
      </div>

      <div class="sidebar-section">
        <h3>服务器列表</h3>
        <ServerList
          :servers="servers"
          :activeSessionId="activeSessionId"
          @connect="handleConnect"
          @disconnect="handleDisconnect"
        />
      </div>

      <div class="sidebar-section">
        <h3>快速连接</h3>
        <QuickConnect @connect="handleQuickConnect" />
      </div>
    </aside>

    <main class="main-content">
      <Terminal
        v-if="activeSessionId"
        :sessionId="activeSessionId"
        :serverName="activeServerName"
        @close="handleDisconnect"
      />
      <div v-else class="welcome">
        <div class="welcome-content">
          <h2>欢迎使用 Web SSH 客户端</h2>
          <p>请从左侧选择服务器或使用快速连接</p>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Terminal from './components/Terminal.vue'
import ServerList from './components/ServerList.vue'
import QuickConnect from './components/QuickConnect.vue'
import axios from 'axios'

const servers = ref([])
const activeSessionId = ref(null)
const activeServerName = ref('')

// Load servers on mount
onMounted(async () => {
  try {
    const response = await axios.get('/api/servers')
    servers.value = response.data
  } catch (error) {
    console.error('Failed to load servers:', error)
  }
})

// Handle server connection
async function handleConnect(server) {
  try {
    // Create session
    const response = await axios.post('/api/sessions', {
      server_id: server.id,
      credential_id: server.default_credential_id,
    })

    activeSessionId.value = response.data.session_id
    activeServerName.value = server.name
  } catch (error) {
    console.error('Failed to connect:', error)
    alert(`连接失败: ${error.response?.data?.detail || error.message}`)
  }
}

// Handle quick connect
async function handleQuickConnect(params) {
  try {
    const response = await axios.post('/api/sessions/', params)

    activeSessionId.value = response.data.session_id
    activeServerName.value = params.host
  } catch (error) {
    console.error('Failed to connect:', error)

    // Handle different error formats
    let errorMessage = '未知错误'
    if (error.response?.data) {
      const data = error.response.data
      if (data.detail) {
        // FastAPI error detail
        if (typeof data.detail === 'string') {
          errorMessage = data.detail
        } else if (Array.isArray(data.detail)) {
          // Validation errors
          errorMessage = data.detail.map(e => `${e.loc.join('.')}: ${e.msg}`).join(', ')
        } else {
          errorMessage = JSON.stringify(data.detail)
        }
      } else {
        errorMessage = JSON.stringify(data)
      }
    } else if (error.message) {
      errorMessage = error.message
    }

    alert(`连接失败: ${errorMessage}`)
  }
}

// Handle disconnect
async function handleDisconnect() {
  if (!activeSessionId.value) return

  try {
    await axios.delete(`/api/sessions/${activeSessionId.value}`)
  } catch (error) {
    console.error('Failed to disconnect:', error)
  }

  activeSessionId.value = null
  activeServerName.value = ''
}
</script>

<style scoped>
.app {
  display: flex;
  height: 100vh;
  width: 100vw;
}

.sidebar {
  width: 320px;
  background: #252526;
  border-right: 1px solid #3e3e42;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
}

.sidebar-header {
  padding: 20px;
  background: #2d2d30;
  border-bottom: 1px solid #3e3e42;
}

.sidebar-header h1 {
  font-size: 18px;
  font-weight: 600;
  color: #fff;
}

.sidebar-section {
  padding: 20px;
  border-bottom: 1px solid #3e3e42;
}

.sidebar-section h3 {
  font-size: 14px;
  font-weight: 500;
  color: #ccc;
  margin-bottom: 12px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.main-content {
  flex: 1;
  background: #1e1e1e;
  position: relative;
}

.welcome {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
}

.welcome-content {
  text-align: center;
}

.welcome-content h2 {
  font-size: 28px;
  font-weight: 300;
  color: #fff;
  margin-bottom: 12px;
}

.welcome-content p {
  font-size: 16px;
  color: #888;
}
</style>
