<template>
  <div class="server-list">
    <div
      v-for="server in servers"
      :key="server.id"
      :class="['server-item', { active: activeSessionId === server.id }]"
      @click="$emit('connect', server)"
    >
      <div class="server-icon">🖥️</div>
      <div class="server-info">
        <div class="server-name">{{ server.name }}</div>
        <div class="server-address">{{ server.host }}:{{ server.port }}</div>
      </div>
    </div>

    <div v-if="servers.length === 0" class="empty-state">
      <p>暂无已保存的服务器</p>
      <p class="hint">使用快速连接或添加新服务器</p>
    </div>
  </div>
</template>

<script setup>
defineProps({
  servers: {
    type: Array,
    required: true,
  },
  activeSessionId: {
    type: String,
    default: null,
  },
})

defineEmits(['connect', 'disconnect'])
</script>

<style scoped>
.server-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.server-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: #2d2d30;
  border: 1px solid #3e3e42;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.server-item:hover {
  background: #37373d;
  border-color: #007acc;
}

.server-item.active {
  background: #094771;
  border-color: #007acc;
}

.server-icon {
  font-size: 24px;
}

.server-info {
  flex: 1;
  min-width: 0;
}

.server-name {
  font-size: 14px;
  font-weight: 500;
  color: #fff;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.server-address {
  font-size: 12px;
  color: #888;
  font-family: monospace;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.empty-state {
  text-align: center;
  padding: 20px;
  color: #666;
}

.empty-state p {
  margin: 4px 0;
  font-size: 13px;
}

.empty-state .hint {
  font-size: 12px;
  color: #555;
}
</style>
