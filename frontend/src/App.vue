<script lang="ts">
import { RouterView } from 'vue-router';
import AppLayout from '@/layouts/AppLayout.vue';
import axios from "axios";
import {mapActions, mapGetters, mapMutations, mapState} from "vuex";
import {defineComponent} from "vue";
import BaseApp from "@/apps/visagiste/components/BaseApp/BaseApp.vue";

export default defineComponent({
  components: {
    BaseApp,
    AppLayout,
    RouterView,
  },
  async mounted() {
    this.initializeAuth()
    axios.defaults.headers.common["Authorization"] = this.token ? `Token ${this.token}` : ''
    await this.fetchUserInfo()
  },
  methods: {
    ...mapMutations({
      initializeAuth: "authModule/initializeAuth"
    }),
    ...mapActions({
      fetchUserInfo: 'authModule/fetchUserInfo',
    }),
  },
  computed: {
    ...mapGetters({
      token: 'authModule/getToken',
    }),
    ...mapState({
      isLoading: 'isLoading',
    }),
  },
})
</script>

<template>
<base-app>
  <AppLayout>
    <RouterView/>
  </AppLayout>
</base-app>
</template>

