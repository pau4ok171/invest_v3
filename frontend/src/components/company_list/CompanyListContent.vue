<script setup lang="ts">
// Composables
import { useCompanyListStore } from '@/store/companyList/companyList'

// Utilities
import { computed, ref } from 'vue'
import { useAuthStore } from '@/store/auth'

const companyListStore = useCompanyListStore()
const authStore = useAuthStore()

interface CompanyItem {
  companyLogo: string
  companyName: string
  lastPrice: string
  return7D: string
  return1Y: string
  marketCap: string
  consensus: string
  fairValue: string
  growth: string
  dividendYield: string
  sector: string
  watchlisted: boolean
  ticker: string
  to: string
  uid: string
}

const headers = ref([
  { key: 'companyLogo', title: '', sortable: false },
  { key: 'companyName', title: 'Компания' },
  { key: 'lastPrice', title: 'Цена' },
  { key: 'return7D', title: '7Д Изм' },
  { key: 'return1Y', title: '1Г Изм' },
  { key: 'marketCap', title: 'Кап' },
  { key: 'consensus', title: 'Консенсус' },
  { key: 'fairValue', title: 'Стоимость' },
  { key: 'growth', title: 'Рост' },
  { key: 'dividendYield', title: 'Див' },
  { key: 'sector', title: 'Сектор' },
  { key: 'watchlisted', title: '', sortable: false },
])

const items = computed<CompanyItem[]>(
  () =>
    companyListStore.companies.map((c) => ({
      companyLogo: c.logo_url,
      companyName: c.title,
      lastPrice: `${c.formatting.primaryCurrencySymbol}${c.price_data.last_price?.toFixed(2)}`,
      return7D: `${c.return_1y.toFixed(2)}%`,
      return1Y: `${c.return_7d.toFixed(2)}%`,
      marketCap: humanize(
        c.price_data.capitalisation,
        c.formatting.primaryCurrencySymbol
      ),
      consensus: 'TBA',
      fairValue: 'TBA',
      growth: 'TBA',
      dividendYield: 'TBA',
      sector: c.sector.title,
      ticker: c.ticker,
      to: c.absolute_url,
      uid: c.uid,
      watchlisted: c.is_watchlisted,
    })) as CompanyItem[]
)

function humanize(val: number = 0, currencyUnit: string = '') {
  if (val === 0) return 'n/a'
  for (const unit of ['', 't', 'M', 'B', 'T']) {
    if (Math.abs(val) < 1000) return currencyUnit + val.toFixed(2) + unit
    val /= 1000
  }
  return currencyUnit + val.toFixed(2) + 'Q'
}
</script>

<template>
  <v-infinite-scroll
    @load="companyListStore.fetchCompanies"
    empty-text=""
    class="overflow-y-hidden"
  >
    <v-data-table-virtual
      class="company-list-companies-table bg-background"
      :style="{ fontSize: '.75rem' }"
      :headers="headers"
      :items="items"
      hover
      :hide-no-data="companyListStore.fetching"
      hideDefaultFooter
    >
      <template #item.companyLogo="{ item }">
        <router-link :to="item.to">
          <v-avatar :image="item.companyLogo" variant="tonal" />
        </router-link>
      </template>
      <template #item.companyName="{ item }: { item: CompanyItem }">
        <router-link :to="item.to">
          <span class="text-info font-weight-medium">{{ item.ticker }}</span>
          <span>{{ item.companyName }}</span>
        </router-link>
      </template>
      <template #item.lastPrice="{ item }: { item: CompanyItem }">
        <router-link :to="item.to">{{ item.lastPrice }}</router-link>
      </template>
      <template #item.return7D="{ item }: { item: CompanyItem }">
        <router-link
          :to="item.to"
          :class="
            !item.return7D.startsWith('-') ? 'text-success' : 'text-error'
          "
          >{{ item.return7D }}</router-link
        >
      </template>
      <template #item.return1Y="{ item }: { item: CompanyItem }">
        <router-link
          :to="item.to"
          :class="
            !item.return1Y.startsWith('-') ? 'text-success' : 'text-error'
          "
          >{{ item.return1Y }}</router-link
        >
      </template>
      <template #item.marketCap="{ item }: { item: CompanyItem }">
        <router-link :to="item.to">{{ item.marketCap }}</router-link>
      </template>
      <template #item.consensus="{ item }: { item: CompanyItem }">
        <router-link :to="item.to">{{ item.consensus }}</router-link>
      </template>
      <template #item.fairValue="{ item }: { item: CompanyItem }">
        <router-link :to="item.to">{{ item.fairValue }}</router-link>
      </template>
      <template #item.growth="{ item }: { item: CompanyItem }">
        <router-link :to="item.to">{{ item.growth }}</router-link>
      </template>
      <template #item.dividendYield="{ item }: { item: CompanyItem }">
        <router-link :to="item.to">{{ item.dividendYield }}</router-link>
      </template>

      <template #item.watchlisted="{ item }: { item: CompanyItem }">
        <v-btn
          :icon="item.watchlisted ? '$ratingFull' : '$ratingEmpty'"
          variant="text"
          density="compact"
          :disabled="!authStore.isAuthenticated"
          @click="companyListStore.toggleWatchlisted(item)"
        />
      </template>

      <template #item.sector="{ item }: { item: CompanyItem }">
        <v-chip :text="item.sector" label color="blue" />
      </template>

      <template #body.append v-if="companyListStore.fetching">
        <tr v-for="i in 20" :key="i">
          <td><v-skeleton-loader loading type="avatar" /></td>
          <td><v-skeleton-loader loading type="text" /></td>
          <td><v-skeleton-loader loading type="text" /></td>
          <td><v-skeleton-loader loading type="text" /></td>
          <td><v-skeleton-loader loading type="text" /></td>
          <td><v-skeleton-loader loading type="text" /></td>
          <td><v-skeleton-loader loading type="text" /></td>
          <td><v-skeleton-loader loading type="text" /></td>
          <td><v-skeleton-loader loading type="text" /></td>
          <td><v-skeleton-loader loading type="text" /></td>
          <td><v-skeleton-loader loading type="chip" /></td>
          <td><v-skeleton-loader loading type="button" /></td>
        </tr>
      </template>
    </v-data-table-virtual>
  </v-infinite-scroll>
</template>

<style lang="scss">
.company-list-companies-table.v-table {
  > .v-table__wrapper {
    > table {
      > tbody {
        > tr {
          > td {
            padding: 0;

            > a {
              display: flex;
              flex-direction: column;
              width: 100%;
              height: 100%;
              padding: 0 16px;
              align-items: start;
              justify-content: center;
              text-decoration: none;
              color: inherit;
            }
          }
        }
      }
    }
  }
}
.v-skeleton-loader__avatar {
  width: 40px;
  min-width: 40px;
  height: 40px;
  min-height: 40px;
}
.v-skeleton-loader__chip {
  margin-left: 4px;
  border-radius: 4px;
}
.v-skeleton-loader__button {
  border-radius: 4px;
  height: 24px;
  margin: 4px;
  max-width: 24px;
}
</style>
