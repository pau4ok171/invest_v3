<template>
  <div>
    <AppLayout>
      <RouterView />
    </AppLayout>
  </div>
</template>

<script lang="ts">
import { RouterView } from 'vue-router';
import AppLayout from '@/layouts/AppLayout.vue';
import axios from "axios";
import store from "@/store";

export default {
  components: {
    AppLayout,
    RouterView,
  },
  beforeCreate() {
    store.commit('initializeStore')

    const token = store.state.token

    axios.defaults.headers.common["Authorization"] = token ? `Token ${token}` : ''
  },
  computed: {
    store() {
      return store
    }
  },

}

</script>

<style>
  @import 'assets/css/main.css';
</style>
