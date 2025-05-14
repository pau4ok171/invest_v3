<script setup lang="ts">
import TheHeader from '@/components/base/header/TheHeader.vue'
import TheMain from '@/components/base/main/TheMain.vue'
import TheFooter from '@/components/base/footer/TheFooter.vue'
</script>

<template>
  <the-header />

  <the-main><slot /></the-main>

  <the-footer />
</template>
