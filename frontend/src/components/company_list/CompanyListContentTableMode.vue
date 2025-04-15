<script setup lang="ts">
// Composables
import { useCompanyListStore } from '@/store/companyList/companyList'
import { useAuthStore } from '@/store/auth'

// Utilities
import { ref } from 'vue'

// Types
import type { PropType } from 'vue'
import type { CompanyItem } from '@/store/companyList/types'

const props = defineProps({
  items: {
    type: Object as PropType<CompanyItem[]>,
  },
})

const store = useCompanyListStore()
const authStore = useAuthStore()

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
</script>

<template>
  <v-data-table-virtual
    class="company-list-companies-table bg-background"
    :style="{ fontSize: '.75rem' }"
    :headers="headers"
    :items="props.items"
    hover
    :hide-no-data="store.fetching"
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
        :class="!item.return7D.startsWith('-') ? 'text-success' : 'text-error'"
        >{{ item.return7D }}</router-link
      >
    </template>
    <template #item.return1Y="{ item }: { item: CompanyItem }">
      <router-link
        :to="item.to"
        :class="!item.return1Y.startsWith('-') ? 'text-success' : 'text-error'"
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
        @click="store.toggleWatchlisted(item)"
      />
    </template>

    <template #item.sector="{ item }: { item: CompanyItem }">
      <v-chip :text="item.sector" label color="blue" />
    </template>

    <template #body.append v-if="store.fetching">
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
}
</style>
