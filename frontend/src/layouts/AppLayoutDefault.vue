<script setup lang="ts">
  import { useLifecycleLogger } from '@/common/hooks/lifecycleLogger';

  useLifecycleLogger({ name: 'AppLayoutDefault' });
</script>

<template>
  <div>AppLayoutDefault</div>
  <slot/>
</template>

<style scoped>

</style>