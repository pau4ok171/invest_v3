<script setup lang="ts">
// Components
import CompanyListHeader from '@/components/company_list/CompanyListHeader.vue'
import CompanyListContent from '@/components/company_list/CompanyListContent.vue'

// Composables
import { useCompanyListStore } from '@/store/companyList/companyList'
import { usePageStore } from '@/store/page'
import { useWebsocket } from '@/composables/websocket'
import { usePriceUpdater } from '@/composables/priceUpdater'
import { useTitle } from '@/composables/documentTitle'

// Utilities
import { onMounted, provide } from 'vue'

const store = useCompanyListStore()
const pageStore = usePageStore()
const { setTitle } = useTitle()
setTitle('pageTitles.companyList')

const { priceChanges, activeAnimations, updatePrice } = usePriceUpdater()

provide('priceChanges', priceChanges)
provide('activeAnimations', activeAnimations)

// Websocket
const { connect } = useWebsocket({
  url: 'ws/api/v1/prices',
  maxReconnectAttempts: 5,
  reconnectInterval: 3000,

  onMessage: (data) => {
    const company = store.companies.find((c) => c.uid === data.uid)
    if (!company) return

    const oldPrice = company.price_data.last_price
    company.price_data.last_price = data.price

    updatePrice(data.uid, data.price, oldPrice)
  },
  onOpen: () => {
    console.log('Websocket connected')
  },

  onError: (error) => {
    console.log('Websocket error', error)
  },
})

onMounted(async () => {
  pageStore.loading = false
  await store.initFilters()

  // Connect to Websocket
  connect()
})
</script>

<template>
  <div class="d-flex w-100 h-100 flex-column">
    <CompanyListHeader />

    <CompanyListContent />
  </div>
</template>
