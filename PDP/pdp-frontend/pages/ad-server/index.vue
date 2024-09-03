<template>
    <CBox p="4">
      <CHeading mb="4">AD-Server</CHeading>
      <CText mb="4">This is the AD-Server page.</CText>
  
      <!-- IP 輸入框 -->
      <CFormControl mb="4">
        <CFormLabel>IP Address</CFormLabel>
        <CInput v-model="ip" placeholder="Enter IP Address" />
      </CFormControl>
  
      <!-- Username 輸入框 -->
      <CFormControl mb="4">
        <CFormLabel>Username</CFormLabel>
        <CInput v-model="username" placeholder="Enter Username" />
      </CFormControl>
  
      <!-- 提交按鈕 -->
      <CButton colorScheme="teal" @click="handleSubmit">Test Connect</CButton>
    </CBox>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  
  // 定義狀態
  const ip = ref('')
  const username = ref('')
  
  // 點擊處理函數
  const handleSubmit = () => {
    alert('Success')
  }
  </script>
  