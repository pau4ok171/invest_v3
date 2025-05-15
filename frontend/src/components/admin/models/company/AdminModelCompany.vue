<script setup lang="ts">
// Components
import AdminModelCompanyForm from '@/components/admin/models/company/AdminModelCompanyForm.vue'
import AdminModelHeader from '@/components/admin/models/AdminModelHeader.vue'

// Composables
import { useAdminModelStore } from '@/store/admin/admin'
import { usePageStore } from '@/store/page'
import { useAsyncState } from '@vueuse/core'
import { useRouter } from 'vue-router'

// Utilities
import { onUnmounted, watch } from 'vue'

const props = defineProps({
  companyUID: {
    type: String,
    default: '',
  },
})

const store = useAdminModelStore()
const pageStore = usePageStore()
const router = useRouter()

async function initialize() {
  pageStore.loading = true
  try {
    await store.initStore(props.companyUID, router)
    await store.fetchCompany()
  } finally {
    pageStore.loading = false
  }
}

const { isLoading } = useAsyncState(initialize(), null, {
  immediate: true,
})

watch(isLoading, (newVal) => {
  pageStore.loading = newVal
})

onUnmounted(() => {
  store.resetStore()
})
</script>

<template>
  <Suspense>
    <template #default>
      <div v-if="!isLoading" class="admin-model-company">
        <admin-model-header class="mb-4" />

        <admin-model-company-form class="mb-4" />
      </div>
    </template>
  </Suspense>
</template>

<style scoped lang="scss">
.admin-model-company {
  min-height: 100vh;
  width: 100%;
  margin-top: 16px;
}
</style>
