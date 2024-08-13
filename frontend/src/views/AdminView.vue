<script lang="ts">
import {defineComponent} from 'vue'
import AdminModels from "@/components/admin/models/AdminModels.vue";
import AdminDashboard from "@/components/admin/dashboard/AdminDashboard.vue";
import AdminSettings from "@/components/admin/settings/AdminSettings.vue";
import AdminStaff from "@/components/admin/staff/AdminStaff.vue";
import {mapActions, mapMutations} from "vuex";
import AdminModel from "@/components/admin/models/AdminModel.vue";

export default defineComponent({
  name: "AdminView",
  data() {
    return {
      activeComponent: 'AdminDashboard',
    }
  },
  components: {
    AdminDashboard,
    AdminModels,
    AdminStaff,
    AdminSettings,
    AdminModel,
  },
  mounted() {
    document.title = 'ADMIN PANEL'
  },
  methods: {
    ...mapMutations({
      setCompanyUID: 'adminModule/setCompanyUID',
    }),
    ...mapActions({
      initAdminStore: 'adminModule/initAdminStore',
    }),
    openModel(company_uid: string) {
      this.initAdminStore()
      this.setCompanyUID(company_uid)
      this.activeComponent = 'AdminModel'
    },
  },
})
</script>

<template>
<div class="admin-view">
  <div class="admin-sidebar">
    <div class="admin-sidebar__navigation">

      <ul class="admin-sidebar__menu">
        <li :class="['admin-sidebar__menu-item', {'admin-sidebar__menu-item--active': activeComponent === 'AdminDashboard'}]" @click="activeComponent = 'AdminDashboard'">Dashboard</li>
        <li :class="['admin-sidebar__menu-item', {'admin-sidebar__menu-item--active': activeComponent === 'AdminModels'}]" @click="activeComponent = 'AdminModels'">Models</li>
        <li :class="['admin-sidebar__menu-item', {'admin-sidebar__menu-item--active': activeComponent === 'AdminStaff'}]" @click="activeComponent = 'AdminStaff'">Staff</li>
        <li :class="['admin-sidebar__menu-item', {'admin-sidebar__menu-item--active': activeComponent === 'AdminSettings'}]" @click="activeComponent = 'AdminSettings'">Settings</li>
      </ul>

    </div>
  </div>
  <div class="admin-content">
    <component @openModel="openModel" :is="activeComponent"/>
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
  color: rgba(255, 255, 255, .5);
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
  content: "";
  display: block;
  position: absolute;
  width: 4px;
  height: 100%;
  top: 0;
  background-color: var(--blue);
  border-radius: 4px;
  margin-left: -12px;
}
</style>