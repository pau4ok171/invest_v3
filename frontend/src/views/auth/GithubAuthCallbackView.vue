<script setup lang="ts">
// Utilities
import { onMounted } from 'vue'

const props = defineProps<{
  code: string
}>()

onMounted(() => {
  if (props.code) {
    if (localStorage.getItem('github_popup') === 'open') {
      localStorage.removeItem('github_popup')

      localStorage.setItem(
        'github_auth_response',
        JSON.stringify({
          code: props.code,
          timestamp: Date.now(),
        })
      )
    }
  }
  window.close()
})
</script>

<template>
  <div>Processing GitHub authentication...</div>
</template>
