<script setup lang="ts">
// Components
import AdminModelCompanyForm from '@/components/admin/models/company/AdminModelCompanyForm.vue'
import AdminModelHeader from '@/components/admin/models/AdminModelHeader.vue'
import PageLoading from '@/components/UI/PageLoading.vue'

// Composables
import { useAdminModelStore } from '@/store/admin/admin'
import { useAsyncState } from '@vueuse/core'
import { useRouter } from 'vue-router'

// Utilities
import { onUnmounted } from 'vue'

const props = defineProps({
  companyUID: {
    type: String,
    default: '',
  },
})

const store = useAdminModelStore()
const router = useRouter()

async function initialize() {
  await store.initStore(props.companyUID, router)
  await store.fetchCompany()
}

const { isLoading, error } = useAsyncState(initialize(), null, {
  immediate: true,
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
    <template #fallback>
      <page-loading :model-value="true" />
    </template>
  </Suspense>
</template>

<style scoped lang="scss">
.admin-model-company {
  width: 100%;
  margin-top: 16px;
}
</style>
