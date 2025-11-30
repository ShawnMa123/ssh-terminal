<template>
  <div class="terminal-container">
    <div class="terminal-header">
      <span class="server-name">📡 {{ serverName }}</span>
      <span class="session-id">{{ sessionId.substring(0, 8) }}</span>
      <button @click="$emit('close')" class="close-btn">✕</button>
    </div>
    <div ref="terminalRef" class="terminal"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { Terminal } from '@xterm/xterm'
import { FitAddon } from '@xterm/addon-fit'
import '@xterm/xterm/css/xterm.css'

const props = defineProps({
  sessionId: {
    type: String,
    required: true,
  },
  serverName: {
    type: String,
    required: true,
  },
})

defineEmits(['close'])

const terminalRef = ref(null)
let terminal = null
let fitAddon = null
let ws = null

onMounted(() => {
  initTerminal()
  connectWebSocket()
})

onUnmounted(() => {
  cleanup()
})

function initTerminal() {
  // Create terminal instance
  terminal = new Terminal({
    cursorBlink: true,
    fontSize: 14,
    fontFamily: 'Menlo, Monaco, "Courier New", monospace',
    theme: {
      background: '#1e1e1e',
      foreground: '#cccccc',
      cursor: '#ffffff',
      black: '#000000',
      red: '#cd3131',
      green: '#0dbc79',
      yellow: '#e5e510',
      blue: '#2472c8',
      magenta: '#bc3fbc',
      cyan: '#11a8cd',
      white: '#e5e5e5',
      brightBlack: '#666666',
      brightRed: '#f14c4c',
      brightGreen: '#23d18b',
      brightYellow: '#f5f543',
      brightBlue: '#3b8eea',
      brightMagenta: '#d670d6',
      brightCyan: '#29b8db',
      brightWhite: '#e5e5e5',
    },
    allowProposedApi: true,
  })

  // Add fit addon
  fitAddon = new FitAddon()
  terminal.loadAddon(fitAddon)

  // Mount terminal
  terminal.open(terminalRef.value)
  fitAddon.fit()

  // Handle user input
  terminal.onData((data) => {
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({ type: 'input', data }))
    }
  })

  // Handle resize
  let resizeTimeout
  window.addEventListener('resize', () => {
    clearTimeout(resizeTimeout)
    resizeTimeout = setTimeout(() => {
      fitAddon.fit()
      sendResize()
    }, 100)
  })
}

function connectWebSocket() {
  // Determine WebSocket URL
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
  const wsUrl = `${protocol}//${window.location.host}/ws/ssh/${props.sessionId}`

  ws = new WebSocket(wsUrl)

  ws.onopen = () => {
    console.log('WebSocket connected')
    sendResize()
  }

  ws.onmessage = (event) => {
    try {
      const message = JSON.parse(event.data)

      switch (message.type) {
        case 'output':
          terminal.write(message.data)
          break

        case 'connected':
          console.log('SSH connected')
          break

        case 'disconnected':
          terminal.write('\r\n\r\n[Connection closed]\r\n')
          break

        case 'error':
          terminal.write(`\r\n\r\n[Error: ${message.message}]\r\n`)
          break
      }
    } catch (error) {
      console.error('WebSocket message error:', error)
    }
  }

  ws.onerror = (error) => {
    console.error('WebSocket error:', error)
    terminal.write('\r\n\r\n[WebSocket error]\r\n')
  }

  ws.onclose = () => {
    console.log('WebSocket closed')
    terminal.write('\r\n\r\n[Connection closed]\r\n')
  }
}

function sendResize() {
  if (ws && ws.readyState === WebSocket.OPEN && terminal) {
    ws.send(
      JSON.stringify({
        type: 'resize',
        cols: terminal.cols,
        rows: terminal.rows,
      })
    )
  }
}

function cleanup() {
  if (ws) {
    ws.close()
    ws = null
  }

  if (terminal) {
    terminal.dispose()
    terminal = null
  }
}
</script>

<style scoped>
.terminal-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
}

.terminal-header {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  background: #2d2d30;
  border-bottom: 1px solid #3e3e42;
  gap: 12px;
}

.server-name {
  flex: 1;
  font-size: 14px;
  font-weight: 500;
  color: #fff;
}

.session-id {
  font-size: 12px;
  color: #888;
  font-family: monospace;
}

.close-btn {
  background: transparent;
  border: none;
  color: #888;
  font-size: 20px;
  cursor: pointer;
  padding: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.2s;
}

.close-btn:hover {
  color: #fff;
}

.terminal {
  flex: 1;
  padding: 8px;
  overflow: hidden;
}
</style>
