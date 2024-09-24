<template>
  <div class="container">    
    <CThemeProvider>      
      <CColorModeProvider>
       
        <CBox font-family="body" as="main">
          <Sidebar />          
          <CReset />
          <CBox ml="260px" p="4">
            <Nuxt />
          </CBox>
        </CBox>
      </CColorModeProvider>
    </CThemeProvider>
  </div>
</template>
<script>
import {
  CThemeProvider,
  CColorModeProvider,
  CReset,
  CBox
} from '@chakra-ui/vue'

export default {
  name: 'DefaultLayout',
  components: {
    CThemeProvider,
    CColorModeProvider,
    CReset,
    CBox
  }
}
</script>
