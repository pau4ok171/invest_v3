<script setup lang="ts">
// Components
import CompanyDetailHeader from '@/components/company_detail/header/CompanyDetailHeader.vue'
import CompanyDetailContent from '@/components/company_detail/CompanyDetailContent.vue'
import CompanyDetailRightSidebar from '@/components/company_detail/rightSidebar/companyDetailRightSidebar.vue'
import NotesEditor from '@/components/company_detail/content_list/summary/notes/NotesEditor.vue'

// Composables
import { useCompanyDetailStore } from '@/store/companyDetail'
import { usePageStore } from '@/store/page'
import { useRoute } from 'vue-router'
import { useWebsocket } from '@/composables/websocket'
import { usePriceUpdater } from '@/composables/priceUpdater'

// Utilities
import { onMounted, onUnmounted, provide, watch } from 'vue'
import { RouteNamesEnum } from '@/router/routes.types'

const props = defineProps({
  companySlug: {
    type: String,
    required: true,
  },
})

const route = useRoute()
const pageStore = usePageStore()
const store = useCompanyDetailStore()

async function init() {
  pageStore.loading = true

  await store.fetchCompany(props.companySlug)
  await store.fetchPriceData(props.companySlug)

  pageStore.loading = false

  document.title = `${store.company.title} (${store.company.market.title}:${store.company.ticker}) - Обзор компании, Новости, Аналитика - Finargo`
}

const { priceChanges, activeAnimations, updatePrice } = usePriceUpdater()

provide('priceChanges', priceChanges)
provide('activeAnimations', activeAnimations)

// Websocket
const { connect, close } = useWebsocket({
  url: `ws://localhost:8000/ws/api/v1/prices/${props.companySlug}/`,
  maxReconnectAttempts: 5,
  reconnectInterval: 3000,

  onMessage: (data) => {
    const oldPrice = store.company.price_data.last_price
    store.company.price_data.last_price = data.price

    updatePrice(data.slug, data.price, oldPrice)
  },
  onOpen: () => {
    console.log('Websocket connected')
  },

  onError: (error) => {
    console.log('Websocket error', error)
  },
})

watch(route, (to) => {
  if (to.name === RouteNamesEnum.company_detail) {
    init()
  }
})

onMounted(async () => {
  await init()
  connect()
})

onUnmounted(() => {
  close()
})
</script>

<template>
  <section style="max-width: 1200px">
    <company-detail-header />
    <company-detail-content />
  </section>
  <company-detail-right-sidebar />
  <notes-editor />
</template>
