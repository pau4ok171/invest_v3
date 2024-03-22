<template>
  <BasicHeader :class="{'screen__blured' : store.state.authModalMenuIsActive}"/>
  <AuthModalMenu v-if="store.state.authModalMenuIsActive"/>
  <Loader v-if="store.state.isLoading"/>
</template>

<script lang="ts">
import BasicHeader from '@/components/base/header/BasicHeader.vue'
import AuthModalMenu from "@/components/base/auth/AuthModalMenu.vue";
import store from "@/store";
import Loader from "@/components/UI/Loader.vue";

export default {
  name: 'AppLayoutDefault',
  components: {
    Loader,
    BasicHeader,
    AuthModalMenu
  },
  computed: {
    store () {
      return store
    },
  },
}
</script>

<style scoped>

</style>