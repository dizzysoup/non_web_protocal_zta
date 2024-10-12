<template>
    <CBox p="4" >
      <CHeading> PDP Log</CHeading>
      <CText>This is the Log page </CText>


      <iframe src="http://192.168.50.210:3000/d-solo/cdwrs0g5pkwsgd/pdp-log?orgId=1&refresh=5s&from=now-1h&to=now&panelId=1" width="100%" height="700px" frameborder="0"></iframe>



      <CHeading>PEP Log</CHeading>
      <iframe src="http://192.168.50.210:3000/d-solo/ce09nurwmyk1se/pep-log?orgId=1&refresh=10s&from=now-1h&to=now&panelId=1" width="100%" height="700px" frameborder="0"></iframe>


      <CHeading>FIDO2 Log</CHeading>
      <iframe src="http://192.168.50.210:3000/d-solo/cdz1884yx4ydcb/fido2-log?orgId=1&refresh=10s&from=now-1h&to=now&panelId=1" width="100%" height="700px" frameborder="0"></iframe>


    </CBox>
    
  </template>
  
  <script setup>
  </script>
  