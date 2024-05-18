<template>
  <div>
    <AppLayout>
      <RouterView/>
    </AppLayout>
  </div>
</template>

<script lang="ts">
import { RouterView } from 'vue-router';
import AppLayout from '@/layouts/AppLayout.vue';
import axios from "axios";
import {mapMutations, mapState} from "vuex";
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
    ...mapState({
      token: 'authModule/token',
    })
  },
})
</script>

<style>
  @import 'assets/css/main.css';
</style>
