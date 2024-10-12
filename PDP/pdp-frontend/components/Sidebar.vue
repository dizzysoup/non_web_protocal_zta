<template>
    <CBox
      as="aside"
      w="250px"
      bg="gray.800"
      color="white"
      h="100vh"
      p="4"
      pos="fixed"
    >
      <CHeading size="md" mb="6"> YUNTECH DE </CHeading>
      <CStack spacing="4">
        <NuxtLink to="/user-manager" style="text-decoration: none;">
          <CButton variant="ghost" justifyContent="flex-start" w="100%">
            User Manager 
          </CButton>
        </NuxtLink>
        <NuxtLink to="/rp-manager" style="text-decoration: none;">
          <CButton variant="ghost" justifyContent="flex-start" w="100%">
            RP Manager
          </CButton>
        </NuxtLink>
        
        <NuxtLink to="/log" style="text-decoration: none;">
          <CButton variant="ghost" justifyContent="flex-start" w="100%">
            Log
          </CButton>
        </NuxtLink>
        <NuxtLink to="/ad-server" style="text-decoration: none;">
          <CButton variant="ghost" justifyContent="flex-start" w="100%">
            AD Server
          </CButton>
        </NuxtLink>
      </CStack>
    </CBox>
  </template>
  
  <script setup>
  </script>
  