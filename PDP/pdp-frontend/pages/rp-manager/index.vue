<style>
table {
    width: 100%;
    border-collapse: collapse; /* 讓邊框合併，防止雙重邊框 */
  }

  th, td {
    padding: 10px; /* 調整儲存格內部的間距 */
    text-align: left; /* 文字靠左對齊 */
    border: 1px solid #ccc; /* 加入邊框以便查看對齊 */
  }

  thead th {
    background-color: #f7f7f7; /* 設定標題列背景色 */
    font-weight: bold; /* 加粗標題文字 */
  }
</style>



<template> 
    <CBox p="4">
      <!-- 標題區塊 -->
      <CHeading as="h2" size="xl" mb="4">RP Manager</CHeading>
      <CText mb="4">This is the RP Manager page.</CText>
      
      <!-- 主區塊 -->
      <CBox border="1px" borderColor="gray.200" borderRadius="md" p="4" bg="gray.50">
        <!-- 操作按鈕組與搜尋框 -->
        <CBox mb="4" display="flex" alignItems="center" gap="4">
          <CButton left-icon="add" colorScheme="blue" variant="solid" @click="addRP" style="background-color: #001D51; color: white;">
            新增單一RP
          </CButton>
  
          <CBox display="flex" alignItems="center" gap="2" ml="auto">
            <CInput placeholder="輸入欲查詢之RP編號" />
            <CButton colorScheme="gray" size="md">搜尋</CButton>
          </CBox>
        </CBox>

        <!-- 表格結構 -->
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Alias Name</th>
            <th>IP</th>
            <th>Port</th>
            <th>OS Type</th>
            <th>Description</th>
            <th>Setting</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="rp in rpList" :key="rp.id">
            <td>{{ rp.id }}</td>
            <td>{{ rp.alias_name }}</td>
            <td>{{ rp.ip_address }}</td>
            <td>{{ rp.port }}</td>
            <td>{{ rp.os_type }}</td>
            <td>{{ rp.description }}</td>
            <td>
              <CButton variant-color="blue" size="sm" mr="2" @click="openEditModal(rp)">
                編輯
              </CButton>
              <CButton variant-color="red" size="sm" @click="deleterp(rp.id)">
                刪除
              </CButton>
            </td>
          </tr>
        </tbody>
      </table>
    </CBox>

    <!-- 編輯彈出視窗 -->
    <CModal v-if="isModalOpen" @close="closeEditModal">
      <CModalOverlay />
      <CModalContent>
        <CModalHeader>編輯 RP</CModalHeader>
        <CModalCloseButton />
        <CModalBody>
          <CInput v-model="editingRP.alias_name" placeholder="Alias Name" mb="4" />
          <CInput v-model="editingRP.ip_address" placeholder="IP" mb="4" />
          <CInput v-model="editingRP.port" placeholder="Port" mb="4" />
          <CInput v-model="editingRP.os_type" placeholder="OS Type" mb="4" />
          <CInput v-model="editingRP.description" placeholder="Description" mb="4" />
        </CModalBody>

        <CModalFooter>
          <CButton colorScheme="blue" mr="3" @click="saveRP(editingRP)">更新</CButton>
          <CButton variant="ghost" @click="closeEditModal">取消</CButton>
        </CModalFooter>
      </CModalContent>
    </CModal>



  </CBox>
</template>

 
<script setup>
import { ref, onMounted } from 'vue';
import { CBox, CButton, CInput, CModal, CModalOverlay, CModalContent, CModalHeader, CModalBody, CModalFooter, CModalCloseButton, CText } from '@chakra-ui/vue';
  
// 反應式變數
const rpList = ref([]);
const isModalOpen = ref(false); // 控制模態框是否打開
const editingRP = ref({}); // 用來保存正在編輯的 RP
  
  // 取得資料列表
  const fetchRPList = async () => {
    try {
      const response = await fetch("https://de.yuntech.poc.com:3443/rp/", {
        method: "GET",
        redirect: "follow"
      });
  
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
     
      rpList.value = await response.json();
  } catch (error) {
    console.error('Fetch error:', error);
  }
};
  
  // 新增 RP 函數
  const addRP = async () => {
    try {
      const response = await fetch('/rp/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          alias_name: 'test_computer',
          ip_address: '192.168.50.2',
          port: '22',
          os_type: 'linux',
          description: '測試用 前端傳輸 3 ',
        }),
      });
  
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
  
      const result = await response.text();
      alert(result);
    } catch (error) {
      alert('Fetch error:' + error);
    }
  };

// 打開編輯模態框
const openEditModal = (rp) => {
  editingRP.value = { ...rp }; // 複製 RP 資料到 editingRP
  isModalOpen.value = true;
};

// 關閉編輯模態框
const closeEditModal = () => {
  isModalOpen.value = false;
  editingRP.value = {};
};

  
// 儲存 RP 的變更
const saveRP = async (rp) => {
  try {
    const response = await fetch(`https://de.yuntech.poc.com:3443/rp/${rp.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        alias_name: rp.alias_name,
        ip_address: rp.ip_address,
        port: rp.port,
        os_type: rp.os_type,
        description: rp.description,
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.text();
    alert(result);

    // 更新完後關閉模態框
    closeEditModal();

    // 更新表格資料
    const index = rpList.value.findIndex(item => item.id === rp.id);
    if (index !== -1) {
      rpList.value[index] = { ...rp }; // 更新表格中的 RP 資料
    }
  } catch (error) {
    console.error('Save error:', error);
    alert('更新失敗，請確認 API 路徑及權限設定');
  }
};



// 刪除指定rp
const deleterp = async (rpId) => {
  try {
    const requestOptions = {
      method: "DELETE",
      redirect: "follow"
    };

    const response = await fetch(`https://de.yuntech.poc.com:3443/rp/${rpId}`, requestOptions);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    // 刪除成功後，更新用戶列表
    rpList.value = rpList.value.filter(rp => rp.id !== rpId);
    console.log(`rp ${rpId} deleted successfully`);
  } catch (error) {
    console.error('Delete error:', error);
  }
};
  
  // 頁面初始化時調用資料
  onMounted(() => {
    fetchRPList();
  });
  </script>
  