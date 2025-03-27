<script setup lang="ts">
import {computed, onMounted, ref, watch} from 'vue'
import AdminModels from '@/components/admin/models/AdminModels.vue'
import AdminDashboard from '@/components/admin/dashboard/AdminDashboard.vue'
import AdminSettings from '@/components/admin/settings/AdminSettings.vue'
import AdminStaff from '@/components/admin/staff/AdminStaff.vue'
import AdminModel from '@/components/admin/models/AdminModel.vue'
import { previousComponentList } from '@/components/admin/models/components'
import { useAdminStore } from '@/store/admin'
import { AdminComponentName } from '@/types/admin.types'

const adminStore = useAdminStore()

const navigationHeaders = ref([
  AdminComponentName.DASHBOARD,
  AdminComponentName.MODELS,
  AdminComponentName.STAFF,
  AdminComponentName.SETTINGS,
])

const components = {
  AdminDashboard,
  AdminSettings,
  AdminStaff,
  AdminModels,
  AdminModel,
}

async function openModel(company_uid: string) {
  await adminStore.init()
  adminStore.companyUID = company_uid
  adminStore.activeComponent = AdminComponentName.MODEL
}

async function changeComponent(componentIs: AdminComponentName) {
  adminStore.activeComponent = componentIs
}

onMounted(() => {
  document.title = 'ADMIN PANEL'
})

const WatchActiveComponent = computed(() => adminStore.activeComponent)
watch(WatchActiveComponent, () => {
  adminStore.previousComponent = previousComponentList[adminStore.activeComponent]
  window.scrollTo(0, 0)
})
</script>

<template>
  <div class="admin-view">
    <div class="admin-sidebar">
      <div class="admin-sidebar__navigation">
        <ul class="admin-sidebar__menu">
          <li
            v-for="header in navigationHeaders"
            :key="header"
            :class="[
              'admin-sidebar__menu-item',
              {
                'admin-sidebar__menu-item--active':
                  adminStore.activeComponent === header,
              },
            ]"
            @click="adminStore.activeComponent = header"
          >
            {{ header.slice(5) }}
          </li>
        </ul>
      </div>
    </div>
    <div class="admin-content">
      <div class="admin-content__back">
        <v-btn
          prepend-icon="$prev"
          text=""
          color="info"
          size="small"
          :disabled="!adminStore.previousComponent"
          v-tippy="{
            content: 'Click to turn back',
            theme: 'tooltip-theme-paper',
            appendTo: 'parent',
            arrow: false,
          }"
          @click="changeComponent(adminStore.previousComponent)"
        />
      </div>

      <component @openModel="openModel" :is="components[adminStore.activeComponent]" />
    </div>
  </div>
</template>

<style scoped>
.admin-view {
  display: flex;
  width: 100%;
}
.admin-sidebar {
  flex: 0 0 25%;
  width: 25%;
}
.admin-content {
  flex: 0 0 75%;
  width: 75%;
}
.admin-sidebar__navigation {
  width: 100%;
  margin-top: 20px;
}
.admin-sidebar__menu-item {
  cursor: pointer;
  width: 267px;
  position: relative;
  border-radius: 4px;
  color: rgba(255, 255, 255, 0.5);
  padding: 4px 0 4px 12px;
  margin-left: 14px;
  line-height: 1.5;
  font-size: 1.6rem;
}
.admin-sidebar__menu-item:hover {
  background-color: #1b222d;
}
.admin-sidebar__menu-item--active {
  color: #fff;
  background-color: #1b222d;
}
.admin-sidebar__menu-item--active::before {
  content: '';
  display: block;
  position: absolute;
  width: 4px;
  height: 100%;
  top: 0;
  background-color: var(--blue);
  border-radius: 4px;
  margin-left: -12px;
}
.admin-content__back {
  margin-top: 20px;
}
.admin-content__back-icon {
  margin-right: 32px;
  width: 16px;
  height: 16px;
}
</style>