<script setup lang="ts">
// Components
import AdminModelIndicator from '@/components/admin/models/AdminModelIndicator.vue'

// Composables
import { useRouter } from 'vue-router'
import { usePageStore } from '@/store/page'

// Utilities
import { computed, ref, shallowRef, onMounted } from 'vue'
import axios from 'axios'

// Types
import type { IAdminCompany } from '@/types/admin.types'

type CompaniesResponse = IAdminCompany[]

const router = useRouter()
const store = usePageStore()
const companies = ref<IAdminCompany[]>([])
const fetching = shallowRef(false)

const headers = [
  { title: 'Id', key: 'id' },
  { title: 'Title', key: 'title' },
  { title: 'Ticker', key: 'ticker' },
  { title: 'Logo', key: 'logo' },
  { title: 'Market', key: 'market' },
  { title: 'Sector', key: 'sector' },
  { title: 'Visible', key: 'visible' },
]

const items = computed(() =>
  [...companies.value].map((c) => ({
    id: c.id,
    title: c.title,
    ticker: c.ticker,
    logo: c.logo,
    market: c.market_name,
    sector: c.sector_name,
    visible: c.is_visible,
    to: `companies/${c.uid}`,
  }))
)

async function fetchCompanies() {
  try {
    fetching.value = true

    const response = await axios.get<CompaniesResponse>(
      'api/v1/admin/companies/'
    )

    companies.value = response.data
  } catch (error) {
    console.log(error)
    if (axios.isAxiosError(error)) {
      throw new Error(`[ADMIN MODELS ERROR] ${error}`)
    }
  } finally {
    fetching.value = false
  }
}

function getCellProps() {
  return {
    style: 'padding: 0',
  }
}

onMounted(async () => {
  document.title = 'ADMIN MODELS'
  store.loading = false
  await fetchCompanies()
})
</script>

<template>
  <div class="w-100 my-5">
    <v-data-table-virtual
      :headers
      :items
      :loading="fetching"
      hover
      :cell-props="getCellProps"
      class="bg-background"
    >
      <template #top>
        <v-toolbar flat color="background">
          <v-toolbar-title>
            <v-icon
              color="medium-emphasis"
              icon="$iDatabase"
              size="small"
              start
            ></v-icon>

            Companies
          </v-toolbar-title>

          <v-btn
            class="me-2"
            color="info"
            prepend-icon="$plus"
            rounded="lg"
            text="Add company"
            border
            @click="router.push({ name: 'adminCompanyModelNew' })"
          ></v-btn>
        </v-toolbar>
      </template>

      <template #item.id="{ item }">
        <router-link class="admin-models-table__link" :to="item.to">{{
          item.id
        }}</router-link>
      </template>
      <template #item.title="{ item }">
        <router-link class="admin-models-table__link" :to="item.to">{{
          item.title
        }}</router-link>
      </template>
      <template #item.ticker="{ item }">
        <router-link class="admin-models-table__link" :to="item.to">{{
          item.ticker
        }}</router-link>
      </template>

      <template #item.logo="{ item }">
        <router-link class="admin-models-table__link" :to="item.to">
          <v-avatar :image="item.logo" />
        </router-link>
      </template>

      <template #item.market="{ item }">
        <router-link class="admin-models-table__link" :to="item.to">{{
          item.market
        }}</router-link>
      </template>

      <template #item.sector="{ item }">
        <router-link class="admin-models-table__link" :to="item.to">
          <v-chip :text="item.sector" label color="info" />
        </router-link>
      </template>

      <template #item.visible="{ item }">
        <router-link
          class="admin-models-table__link justify-center"
          :to="item.to"
        >
          <admin-model-indicator :is-active="item.visible" />
        </router-link>
      </template>
    </v-data-table-virtual>
  </div>
</template>

<style>
.admin-models-table__link {
  display: flex;
  align-items: center;
  text-align: inherit;
  text-decoration: none;
  color: inherit;
  padding: 0 16px;
  width: 100%;
  height: 100%;
}
</style>
