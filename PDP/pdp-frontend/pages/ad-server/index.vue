<template>
    <CBox p="4">
      <CHeading mb="4">AD-Server</CHeading>
      <CText mb="4">This is the AD-Server page.</CText>
  
      <CFormControl mb="4">
        <CFormLabel>IP Address : 192.168.50.243</CFormLabel>        
      </CFormControl>
  
      <CFormControl mb="4">
        <CFormLabel>Username</CFormLabel>
        <CInput v-model="username" placeholder="Enter Username" />
      </CFormControl>

      <CButton colorScheme="teal" @click="handleSubmit">LDAP Test Connect</CButton>
    </CBox>
  </template>
  
  <script setup>
  import { ref  } from 'vue';
  import axios from 'axios';
  const username = ref('');
  
  // 定義狀態
  const handleSubmit = () => {
    
    axios.post('http://192.168.50.76:3000/fido2/check/ADuser', { username: username.value })
      .then(response => {
        console.log('Response:', response.data);
        alert('Success');
      })
      .catch(error => {
        console.error('There was an error!', error);
        alert('Failed');
      });
  }


  </script>
  