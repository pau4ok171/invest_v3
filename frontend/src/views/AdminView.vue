<script setup lang="ts">
// Utilities
import { onMounted } from 'vue'

onMounted(() => {
  document.title = 'ADMIN PANEL'
})
</script>

<template>
  <div class="admin-view">
    <router-view />
  </div>
</template>

<style scoped>
.admin-view {
  display: flex;
  justify-content: center;
  align-items: start;
  width: 100%;
}
</style>
