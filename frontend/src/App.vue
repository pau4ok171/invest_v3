<script lang="ts">
import { RouterView } from 'vue-router';
import AppLayout from '@/layouts/AppLayout.vue';
import axios from "axios";
import {mapGetters, mapMutations, mapState} from "vuex";
import {defineComponent} from "vue";

export default defineComponent({
  components: {
    AppLayout,
    RouterView,
  },
  mounted() {
    this.initializeAuth()

    axios.defaults.headers.common["Authorization"] = this.token ? `Token ${this.token}` : ''
  },
  methods: {
    ...mapMutations({
      initializeAuth: "authModule/initializeAuth"
    })
  },
  computed: {
    ...mapGetters({
      token: 'authModule/getToken',
    })
  },
})
</script>

<template>
  <div>
    <AppLayout>
      <RouterView/>
    </AppLayout>
  </div>
</template>

<style>
  @import 'assets/css/main.css';
</style>
