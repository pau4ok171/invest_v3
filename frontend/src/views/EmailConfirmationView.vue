<script setup lang="ts">
// Composables
import { usePageStore } from '@/store/page'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'

// Utilities
import { onMounted } from 'vue'
import { toast } from 'vue3-toastify'
import axios from 'axios'

// Types
import type { AxiosError } from 'axios'

const props = defineProps<{
  uid: string
  token: string
}>()

const { t } = useI18n()
const store = usePageStore()
const router = useRouter()

const activateEmail = async () => {
  try {
    store.loading = true

    await axios.post('/api/v1/users/activation/', {
      uid: props.uid,
      token: props.token,
    })

    toast.success(t('toasts.emailConfirmed'))



  } catch (error) {
    if (axios.isAxiosError(error)) {
      const e = error as AxiosError
      if (e.response?.status === 403) {
        await router.push({ name: 'home' })
        return
      }
    }

    console.error(error)
    toast.error(t('toasts.somethingWrong'))
  } finally {
    store.loading = false
  }
}

onMounted(async () => await activateEmail())
</script>

<template>
  <div style="height: 100vh" />
</template>
