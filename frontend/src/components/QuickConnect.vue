<template>
  <div class="quick-connect">
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label>主机地址</label>
        <input
          v-model="form.host"
          type="text"
          placeholder="192.168.1.100"
          required
        />
      </div>

      <div class="form-row">
        <div class="form-group">
          <label>端口</label>
          <input
            v-model.number="form.port"
            type="number"
            placeholder="22"
            min="1"
            max="65535"
          />
        </div>

        <div class="form-group">
          <label>用户名</label>
          <input
            v-model="form.username"
            type="text"
            placeholder="root"
            required
          />
        </div>
      </div>

      <div class="form-group">
        <label>密码</label>
        <input
          v-model="form.password"
          type="password"
          placeholder="输入密码"
          required
        />
      </div>

      <button type="submit" class="connect-btn">连接</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['connect'])

const form = ref({
  host: '',
  port: 22,
  username: '',
  password: '',
})

function handleSubmit() {
  if (!form.value.host || !form.value.username || !form.value.password) {
    alert('请填写所有必填字段')
    return
  }

  const params = {
    host: form.value.host,
    port: form.value.port || 22,
    username: form.value.username,
    password: form.value.password,
  }

  emit('connect', params)
}
</script>

<style scoped>
.quick-connect {
  width: 100%;
}

.form-group {
  margin-bottom: 12px;
}

.form-group label {
  display: block;
  font-size: 12px;
  color: #ccc;
  margin-bottom: 4px;
}

.form-group input {
  width: 100%;
  padding: 8px 12px;
  background: #3c3c3c;
  border: 1px solid #3e3e42;
  border-radius: 4px;
  color: #fff;
  font-size: 13px;
  outline: none;
  transition: border-color 0.2s;
}

.form-group input:focus {
  border-color: #007acc;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}

.connect-btn {
  width: 100%;
  padding: 10px;
  background: #0e639c;
  border: none;
  border-radius: 4px;
  color: #fff;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
}

.connect-btn:hover {
  background: #1177bb;
}

.connect-btn:active {
  background: #0d5689;
}
</style>
