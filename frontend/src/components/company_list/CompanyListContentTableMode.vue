<script setup lang="ts">
// Composables
import { useCompanyListStore } from '@/store/companyList/companyList'
import { useAuthStore } from '@/store/auth'
import { useI18n } from 'vue-i18n'

// Utilities
import { computed, inject } from 'vue'

// Types
import type { PropType } from 'vue'
import type { CompanyItem } from '@/store/companyList/types'
import type { ActiveAnimations } from '@/composables/priceUpdater'

const props = defineProps({
  items: {
    type: Object as PropType<CompanyItem[]>,
  },
})

const store = useCompanyListStore()
const authStore = useAuthStore()
const { t } = useI18n()

const activeAnimations = inject<ActiveAnimations>('activeAnimations') || {}

const headers = computed(() => [
  { key: 'companyLogo', title: '', sortable: false },
  { key: 'companyName', title: t('companyList.dataTable.headers.company') },
  { key: 'lastPrice', title: t('companyList.dataTable.headers.lastPrice') },
  { key: 'return7D', title: t('companyList.dataTable.headers.return7d') },
  { key: 'return1Y', title: t('companyList.dataTable.headers.return1y') },
  { key: 'marketCap', title: t('companyList.dataTable.headers.marketCap') },
  {
    key: 'consensus',
    title: t('companyList.dataTable.headers.analystsTarget'),
  },
  { key: 'fairValue', title: t('companyList.dataTable.headers.valuation') },
  { key: 'growth', title: t('companyList.dataTable.headers.growth') },
  {
    key: 'dividendYield',
    title: t('companyList.dataTable.headers.dividendYield'),
  },
  { key: 'sector', title: t('companyList.dataTable.headers.industry') },
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
    hide-default-footer
  >
    <template #item.companyLogo="{ item }">
      <router-link :to="item.to" class="px-xl-4">
        <v-avatar :image="item.companyLogo" variant="tonal" />
      </router-link>
    </template>
    <template #item.companyName="{ item }: { item: CompanyItem }">
      <router-link :to="item.to" class="px-xl-4">
        <span class="text-info font-weight-medium">{{ item.ticker }}</span>
        <span>{{ item.companyName }}</span>
      </router-link>
    </template>
    <template #item.lastPrice="{ item }: { item: CompanyItem }">
      <router-link :to="item.to" class="px-xl-4">
        <span
          :class="[
            'price',
            {
              'price-positive': activeAnimations[item.uid] === 'up',
              'price-negative': activeAnimations[item.uid] === 'down',
            },
          ]"
        >
          {{ item.lastPrice }}
        </span>
      </router-link>
    </template>
    <template #item.return7D="{ item }: { item: CompanyItem }">
      <router-link
        :to="item.to"
        :class="[
          !item.return7D.startsWith('-') ? 'text-success' : 'text-error',
          'px-xl-4',
        ]"
        >{{ item.return7D }}</router-link
      >
    </template>
    <template #item.return1Y="{ item }: { item: CompanyItem }">
      <router-link
        :to="item.to"
        :class="[
          !item.return1Y.startsWith('-') ? 'text-success' : 'text-error',
          'px-xl-4',
        ]"
        >{{ item.return1Y }}</router-link
      >
    </template>
    <template #item.marketCap="{ item }: { item: CompanyItem }">
      <router-link :to="item.to" class="px-xl-4">{{
        item.marketCap
      }}</router-link>
    </template>
    <template #item.consensus="{ item }: { item: CompanyItem }">
      <router-link :to="item.to" class="px-xl-4">{{
        item.consensus
      }}</router-link>
    </template>
    <template #item.fairValue="{ item }: { item: CompanyItem }">
      <router-link :to="item.to" class="px-xl-4">{{
        item.fairValue
      }}</router-link>
    </template>
    <template #item.growth="{ item }: { item: CompanyItem }">
      <router-link :to="item.to" class="px-xl-4">{{ item.growth }}</router-link>
    </template>
    <template #item.dividendYield="{ item }: { item: CompanyItem }">
      <router-link :to="item.to" class="px-xl-4">{{
        item.dividendYield
      }}</router-link>
    </template>

    <template #item.watchlisted="{ item }: { item: CompanyItem }">
      <v-btn
        :icon="item.watchlisted ? '$ratingFull' : '$ratingEmpty'"
        variant="text"
        size="small"
        rounded="lg"
        density="comfortable"
        :color="item.watchlisted ? 'info' : undefined"
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
@use 'vuetify/settings' as vuetify;

.company-list-companies-table.v-table {
  > .v-table__wrapper {
    > table {
      > thead {
        > tr {
          > th {
            padding-inline: 4px;

            @media #{map-get(vuetify.$display-breakpoints, 'lg-and-down')} {
              &:nth-child(2) {
                position: sticky;
                left: -4px;
                top: 0;
                z-index: 1;
                background-color: rgb(var(--v-theme-background));
              }
            }
          }
        }
      }
      > tbody {
        > tr {
          > td {
            padding-inline: 4px;

            @media #{map-get(vuetify.$display-breakpoints, 'lg-and-down')} {
              &:nth-child(2) {
                position: sticky;
                left: -4px;
                top: 0;
                z-index: 1;
                background-color: rgb(var(--v-theme-background));
              }
            }

            > a {
              display: flex;
              flex-direction: column;
              width: 100%;
              height: 100%;
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
  .price {
    padding: 4px;
    border-radius: 4px;
    color: inherit;
    background-color: transparent;
    transition:
      color 0.6s ease-in,
      background-color 0.6s ease-in;
  }
  .price-positive {
    color: rgb(var(--v-theme-success));
    background-color: rgba(0, 255, 0, 0.12);
  }
  .price-negative {
    color: rgb(var(--v-theme-error));
    background-color: rgba(255, 0, 0, 0.12);
  }
}
</style>
