<template>
  <CBox p="4">
    <CHeading as="h2" size="xl" mb="4">User Manager</CHeading>

    <c-tabs variant="line">
      <c-tab-list>
        <c-tab>User Data</c-tab>
        <c-tab>Permission Setting</c-tab>
      </c-tab-list>

      <c-tab-panels>
        <!-- User Data Tab -->
        <c-tab-panel>
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>User Name</th>
                <th>E-mail</th>
                <th>Created at</th>
                <th>Certificate</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in UserList" :key="user.id.toString()">
                <td>{{ user.id }}</td>
                <td>{{ user.username }}</td>
                <td>{{ user.email }}</td>
                <td>{{ user.created_at }}</td>
                <td>
                  <img
                    src="/icon/certificate.png"
                    alt="Cert"
                    style="width: 50px; height: 50px; cursor: pointer;"
                    @click="openDialog"
                  />
                </td>
                <c-alert-dialog
                  :is-open="isOpen"
                  :least-destructive-ref="$refs.cancelRef"
                  :on-close="closeDialog"
                >
                  <c-alert-dialog-overlay />
                  <c-alert-dialog-content>
                    <c-alert-dialog-header font-size="lg" font-weight="bold">
                      Certificate
                    </c-alert-dialog-header>
                    <c-alert-dialog-body>
                      <p>AAGUID: {{ user.aaguid }}</p>
                      <p>CredentialId: {{ user.credential_id }}</p>
                      <p>PublicKey: {{ user.public_key }}</p>
                    </c-alert-dialog-body>
                    <c-alert-dialog-footer>
                      <c-button ref="cancelRef" @click="closeDialog">
                        Close
                      </c-button>
                    </c-alert-dialog-footer>
                  </c-alert-dialog-content>
                </c-alert-dialog>
                <td>
                  <c-button
                    variant-color="red"
                    @click="deleteUser(user.id)"
                    size="lg"
                  >
                    刪除
                  </c-button>
                </td>
              </tr>
            </tbody>
          </table>
        </c-tab-panel>

        <!-- Service Setting Tab -->
        <c-tab-panel>
          <c-flex h="100vh">
            <c-box
              bg="gray.400"
              w="20%"
              p="4"
              borderRadius="md"
              boxShadow="md"
            >
              <c-box
                v-for="user in UserList"
                :key="user.id.toString()"
                mb="4"
                p="3"
                bg="gray.100"
                borderRadius="md"
                cursor="pointer"
                @click="fetchMatainedRP(user.id, user.username)"                
              >
                <c-flex align="center" justify="space-between">
                  <c-text fontWeight="bold" color="gray.700">
                    {{ user.username }}
                  </c-text>
                  <c-avatar
                    :src="user.avatar || 'https://bit.ly/broken-link'"
                    size="sm"
                  />
                </c-flex>
              </c-box>
            </c-box>
            
            <c-box w="80%" p="4">
              <c-flex justify="space-between" align="center" mb="4">
                <CHeading as="h2" size="xl">{{headerusername }}</CHeading>
                <c-button variant-color="blue" @click="saveChanges">Save</c-button>
              </c-flex>

               
               
              <table>
                <thead>
                  <tr>
                    <th>Status</th>
                    <th>ID</th>
                    <th>RP</th>
                    <th>IP</th>
                    <th>PORT</th>
                    <th>OS</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="rp in RPList" :key="rp.id.toString()">
                    <td>
                      <c-switch size="lg" v-model="rp.statusSwitch" />
                    </td>
                    <td>{{ rp.id }}</td>
                    <td>{{ rp.alias_name }}</td>
                    <td>{{ rp.ip_address }}</td>
                    <td>{{ rp.port }}</td>
                    <td>{{ rp.os_type }}</td>
                  </tr>
                </tbody>
              </table>
            </c-box>
          </c-flex>
        </c-tab-panel>
      </c-tab-panels>
    </c-tabs>
  </CBox>
</template>

<script setup>
import { ref, onMounted } from 'vue';

// 反應式變數
const headerusername = ref("");
const UserList = ref([]);
const RPList = ref([]);
const originalRPList = ref([]); // 保存原始狀態
const isOpen = ref(false);
let selectedUserId = null; // 保存選中的使用者 ID

// 取得資料列表
const fetchUserList = async () => {
  try {
    const response = await fetch("https://de.yuntech.poc.com:3443/users", {
      method: "GET",
      redirect: "follow",
    });
    if (!response.ok)
      throw new Error(`HTTP error! status: ${response.status}`);
    UserList.value = await response.json();
  } catch (error) {
    console.error("Fetch error:", error);
  }
};

// Delete User 
const deleteUser = async (id) => {
  const url = "https://de.yuntech.poc.com:3443/maintained-computers/allow/" + id ; 
  const response = await fetch(url, {
      method: "GET",
      redirect: "follow",
  });
  if(response.ok){
    alert("該使用者被允許存取特定RP，請先移除權限後再刪除使用者");
    return ;
  }
  const data = await response.json();

}

// Maintained by ID
const fetchMatainedRP = async (id, username) => {
  selectedUserId = id; // 保存選中的 user_id
  headerusername.value = username ; 
  try {
    RPList.value = [];
    originalRPList.value = [];
    const url = "https://de.yuntech.poc.com:3443/maintained-computers/" + id;
    const response = await fetch(url, {
      method: "GET",
      redirect: "follow",
    });
    if (!response.ok)
      throw new Error(`HTTP error! status: ${response.status}`);
    const data = await response.json();
    
    // 保存原始資料
    RPList.value = data.map((rp) => ({
      ...rp,
      statusSwitch: rp.status === "true",
    }));
    
    // 複製一份原始資料
    originalRPList.value = JSON.parse(JSON.stringify(RPList.value));
  } catch (error) {
    console.error("Fetch error:", error);
  }
};

// 保存改變
const saveChanges = async () => {
  try {
    const toInsert = [];
    const toDelete = [];

    RPList.value.forEach((rp) => {
      const original = originalRPList.value.find(o => o.id === rp.id);
      if (original && original.statusSwitch !== rp.statusSwitch) {
        if (rp.statusSwitch) {
          console.log(rp.id + "要新增");
          toInsert.push({ user_id: selectedUserId, computer_id: rp.id });
        } else {
          console.log(rp.id + "要刪除");
          // If changed from true to false, delete
          toDelete.push(rp.id);
        }
      }
    });    
    
    
    // DELETE 請求
    for (const computer_id of toDelete) {
      const url = `https://de.yuntech.poc.com:3443/maintained-computers/${selectedUserId}/${computer_id}`;
      await fetch(url, {
        method: "DELETE",
        redirect: "follow",
      });
    }

    // POST 請求
    if (toInsert.length > 0) {
      const url = "https://de.yuntech.poc.com:3443/maintained-computers";
      await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(toInsert),
        redirect: "follow",
      });
    }

    alert("Changes saved successfully.");
    location.reload();
  } catch (error) {
    console.error("Save error:", error);
  }
};

const closeDialog = () => {
  isOpen.value = false;
};

const openDialog = () => {
  isOpen.value = true;
};

// 初始化函數
onMounted(() => {
  fetchUserList();
});
</script>
