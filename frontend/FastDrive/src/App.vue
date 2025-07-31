<template>
  <div>
    <div v-if="!loggedIn">
      <h2>System log in</h2>
      <input v-model="username" placeholder="User name" />
      <input v-model="password" type="password" placeholder="Password" />
      <button @click="login">Sign in</button>
      <p v-if="loginError" style="color:red">Failed to sign in</p>
    </div>
    <div v-else>
      <h2>File Upload</h2>
      <input type="file" ref="fileInput" />
      <button @click="upload">Upload</button>
      <h2>File Download</h2>
      <input v-model="downloadFilename" placeholder="Files" />
      <button @click="download">Download</button>
      <button @click="logout">Exit</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const backendUrl = 'http://localhost:3001'
const username = ref('')
const password = ref('')
const loggedIn = ref(false)
const loginError = ref(false)
const downloadFilename = ref('')

const login = async () => {
  try {
    await axios.post(`${backendUrl}/login`, 
      new URLSearchParams({ username: username.value, password: password.value })
    )
    loggedIn.value = true
    loginError.value = false
  } catch (e) {
    loginError.value = true
  }
}

const upload = async () => {
  const files = document.querySelector('input[type="file"]').files
  if (!files.length) return
  const form = new FormData()
  form.append('file', files[0])
  form.append('username', username.value)
  form.append('password', password.value)
  await axios.post(`${backendUrl}/upload/`, form)
  alert('Uploading success!')
}

const download = async () => {
  try {
    const params = new URLSearchParams({ username: username.value, password: password.value })
    const url = `${backendUrl}/download/${downloadFilename.value}?${params}`
    window.open(url, '_blank')
  } catch (e) {
    alert('Failed to download!')
  }
}

const logout = () => {
  loggedIn.value = false
  username.value = ''
  password.value = ''
}
</script>
