<script setup lang="ts">
// Utilities
import { onMounted } from 'vue'

const props = defineProps<{
  code: string
}>()

onMounted(() => {
  if (props.code) {
    if (localStorage.getItem('yandex_popup') === 'open') {
      localStorage.removeItem('yandex_popup')

      localStorage.setItem(
        'yandex_auth_response',
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
  <div>Processing Yandex authentification...</div>
</template>
