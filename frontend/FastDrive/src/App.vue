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
      
      <h2>Available Files</h2>
      <button @click="loadFileList">Refresh File List</button>
      <div v-if="fileList.length > 0" style="margin-top: 10px;">
        <div v-for="file in fileList" :key="file.filename" 
             style="border: 1px solid #ccc; margin: 5px; padding: 10px; border-radius: 5px;">
          <strong>{{ file.filename }}</strong>
          <div style="font-size: 12px; color: #666;">
            Size: {{ formatFileSize(file.size) }} | 
            Uploaded: {{ formatDate(file.upload_time) }}
          </div>
          <button @click="downloadFile(file.filename)" 
                  style="margin-top: 5px; background-color: #007bff; color: white; border: none; padding: 5px 10px; border-radius: 3px; cursor: pointer;">
            Download
          </button>
        </div>
      </div>
      <div v-else-if="fileListLoaded" style="color: #666; margin-top: 10px;">
        No files available
      </div>
      
      <h2>Manual Download</h2>
      <input v-model="downloadFilename" placeholder="Enter filename" />
      <button @click="download">Download</button>
      
      <button @click="logout" style="margin-top: 20px;">Exit</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const backendUrl = '/api'
const username = ref('')
const password = ref('')
const loggedIn = ref(false)
const loginError = ref(false)
const downloadFilename = ref('')
const fileList = ref([])
const fileListLoaded = ref(false)

const login = async () => {
  try {
    await axios.post(`${backendUrl}/login`, 
      new URLSearchParams({ username: username.value, password: password.value })
    )
    loggedIn.value = true
    loginError.value = false
    loadFileList() // Load file list on successful login
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
  loadFileList() // Refresh file list after upload
  loadFileList() // Refresh file list after upload
}

const loadFileList = async () => {
  try {
    const params = new URLSearchParams({ username: username.value, password: password.value })
    const response = await axios.get(`${backendUrl}/files?${params}`)
    fileList.value = response.data.files
    fileListLoaded.value = true
  } catch (e) {
    console.error('Failed to load file list:', e)
    fileListLoaded.value = true
  }
}

const downloadFile = async (filename) => {
  try {
    const params = new URLSearchParams({ username: username.value, password: password.value })
    const url = `${backendUrl}/download/${filename}?${params}`
    window.open(url, '_blank')
  } catch (e) {
    alert('Failed to download!')
  }
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

const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleString()
}

const logout = () => {
  loggedIn.value = false
  username.value = ''
  password.value = ''
}
</script>
