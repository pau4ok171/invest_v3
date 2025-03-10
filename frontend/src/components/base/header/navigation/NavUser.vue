<script lang="ts">
// Components
import AuthModalMenu from '@/components/base/auth/AuthModalMenu.vue'

// Base Components
import { BaseButton } from '@/apps/visagiste/components/BaseButton'
import { BaseMenu } from '@/apps/visagiste/components/BaseMenu'
import { BaseDialog } from '@/apps/visagiste/components/BaseDialog'
import { BaseCard } from '@/apps/visagiste/components/BaseCard/'
import { BaseList } from '@/apps/visagiste/components/BaseList'
import { BaseListItem } from '@/apps/visagiste/components/BaseList'
import { BaseDivider } from '@/apps/visagiste/components/BaseDivider'

// Utilities
import { defineComponent } from 'vue'
import axios from 'axios'
import { mapGetters, mapMutations, mapState } from 'vuex'

export default defineComponent({
  name: 'NavUser',
  components: {
    BaseDivider,
    BaseListItem,
    BaseList,
    BaseCard,
    BaseDialog,
    BaseMenu,
    BaseButton,
    AuthModalMenu,
  },
  data() {
    return {
      items: [
        { title: 'Profile', to: '/profile', id: 'profile' },
        { title: 'Plan & Pricing', to: '/pricing', id: 'pricing' },
        { title: 'Notifications', to: '/notifications', id: 'notifications' },
        { title: 'HelpCenter', to: '/helpcenter', id: 'help' },
      ],
      dialog: false,
    }
  },
  computed: {
    ...mapState({
      userInfo: (state: any) => state.authModule.userInfo,
    }),
    ...mapGetters({
      isAuthenticated: 'authModule/getIsAuthenticated',
    }),
  },
  methods: {
    ...mapMutations({
      removeToken: 'authModule/removeToken',
    }),
    logout() {
      axios.defaults.headers.common['Authorization'] = ''

      localStorage.removeItem('token')
      localStorage.removeItem('username')
      localStorage.removeItem('userid')

      this.removeToken()
      document.location.reload()
    },
  },
})
</script>

<template>
  <div class="nav-user__wrapper">
    <template v-if="isAuthenticated">
      <base-menu>
        <template #activator="{ props }">
          <base-button
            v-bind="props"
            icon="$iUser"
            variant="text"
            size="large"
            rounded="lg"
          />
        </template>
        <template #default>
          <base-card>
            <base-list>
              <base-list-item
                v-if="userInfo.is_staff"
                :to="{ name: 'admin' }"
                title="Admin Panel"
              />
              <base-list-item
                v-for="item in items"
                :key="item.id"
                :title="item.title"
                :to="item.to"
              />
              <base-divider />
              <base-list-item @click="logout" title="Logout" />
            </base-list>
          </base-card>
        </template>
      </base-menu>
    </template>

    <template v-else>
      <base-dialog v-model="dialog" max-width="700">
        <template #activator="{ props: activatorProps }">
          <base-button text="login" color="blue" v-bind="activatorProps" />
        </template>
        <template #default>
          <base-card title="Finargo">
            <template #append>
              <base-button
                icon="$close"
                density="compact"
                variant="text"
                @click="dialog = false"
              />
            </template>
            <AuthModalMenu />
          </base-card>
        </template>
      </base-dialog>
    </template>
  </div>
</template>

<style>
.nav-user__wrapper {
  display: flex;
  justify-content: center;
  min-width: 90px;
}
</style>
