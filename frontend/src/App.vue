<script lang="ts">
import { RouterView } from 'vue-router';
import AppLayout from '@/layouts/AppLayout.vue';
import axios from "axios";
import {mapActions, mapGetters, mapMutations, mapState} from "vuex";
import {defineComponent} from "vue";
import Loader from "@/components/UI/Loader.vue";

export default defineComponent({
  components: {
    Loader,
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
<div>
  <AppLayout>
    <RouterView/>
  </AppLayout>

<!--  <Loader v-if="isLoading"/>-->
</div>
</template>

<style>
  @import 'assets/css/main.css';
</style>
