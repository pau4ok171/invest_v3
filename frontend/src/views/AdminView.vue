<script lang="ts">
import {computed, defineComponent} from 'vue'
import AdminModels from "@/components/admin/models/AdminModels.vue";
import AdminDashboard from "@/components/admin/dashboard/AdminDashboard.vue";
import AdminSettings from "@/components/admin/settings/AdminSettings.vue";
import AdminStaff from "@/components/admin/staff/AdminStaff.vue";
import AdminModel from "@/components/admin/models/AdminModel.vue";
import RoundedDarkBlueButton from "@/components/UI/buttons/RoundedDarkBlueButton.vue";
import BackArrowIcon from "@/components/icons/BackArrowIcon.vue";
import {previousComponentList} from "@/components/admin/models/components";
import store from "@/store";
import {RouteNamesEnum} from "@/router/routes.types";
import {useAdminStore} from "@/store/admin";
import {AdminComponentName} from "@/types/admin.types";

const vuexStore = store

export default defineComponent({
  name: "AdminView",
  components: {
    BackArrowIcon,
    RoundedDarkBlueButton,
    AdminDashboard,
    AdminModels,
    AdminStaff,
    AdminSettings,
    AdminModel,
  },
  setup: () => {
    const store = useAdminStore()
    const WatchActiveComponent = computed(() => store.activeComponent)

    return {
      store,
      WatchActiveComponent
    }
  },
  mounted() {
    document.title = 'ADMIN PANEL'
  },
  beforeRouteEnter(to, from, next) {
    // TODO: Replace vuex by pinia
    const userInfo = vuexStore.state.authModule.userInfo
    if (!Object.hasOwn(userInfo, 'is_staff') || !userInfo.is_staff) {
      next(RouteNamesEnum.page_not_found)
    }
    next()
  },
  data() {
    return {
      navigationHeaders: [
        AdminComponentName.DASHBOARD,
        AdminComponentName.MODELS,
        AdminComponentName.STAFF,
        AdminComponentName.SETTINGS,
      ]
    }
  },
  methods: {
    async openModel(company_uid: string) {
      await this.store.initAdminStore()
      this.store.companyUID = company_uid
      this.store.activeComponent = AdminComponentName.MODEL
    },
    async changeComponent(componentIs: AdminComponentName) {
      this.store.activeComponent = componentIs
    },
  },
  watch: {
    WatchActiveComponent() {
      this.store.previousComponent = previousComponentList[this.store.activeComponent]
      window.scrollTo(0, 0)
    }
  },
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
          :class="['admin-sidebar__menu-item', {'admin-sidebar__menu-item--active': store.activeComponent === header}]"
          @click="store.activeComponent = header"
        >
          {{ header.slice(5) }}
        </li>
      </ul>

    </div>
  </div>
  <div class="admin-content">
    <div class="admin-content__back">
      <RoundedDarkBlueButton
          :disabled="!store.previousComponent"
          v-tippy="{content: 'Click to turn back', theme: 'tooltip-theme-paper', appendTo: 'parent', arrow: false}"
          @click="changeComponent(store.previousComponent)"
      >
        <BackArrowIcon class="admin-content__back-icon"/>
      </RoundedDarkBlueButton>
    </div>

    <component @openModel="openModel" :is="store.activeComponent"/>
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
.admin-content__back {
  margin-top: 20px;
}
.admin-content__back-icon {
  margin-right: 32px;
  width: 16px;
  height: 16px;
}
</style>