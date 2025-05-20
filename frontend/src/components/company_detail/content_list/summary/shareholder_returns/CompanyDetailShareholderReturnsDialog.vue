<script setup lang="ts">
// Composables
import { useCompanyDetailStore } from '@/store/companyDetail'
import { useI18n } from 'vue-i18n'

// Utilities
import { computed, shallowRef } from 'vue'

// Types
import type { DetailCompany } from '@/types/invest'

export interface Period {
  name: string
  key: string
}

const store = useCompanyDetailStore()
const company = computed<DetailCompany>(() => store.company)
const { t } = useI18n()

const dialog = shallowRef(false)
const periods = computed(
  () =>
    [
      { name: t('date.days', 7), key: 'return_7d' },
      { name: t('date.days', 30), key: 'return_30d' },
      { name: t('date.days', 90), key: 'return_90d' },
      { name: t('date.years', 1), key: 'return_1y' },
      { name: t('date.years', 3), key: 'return_3y' },
      { name: t('date.years', 5), key: 'return_5y' },
    ] as Period[]
)

function humanize(item: Record<any, any>, p: Period) {
  const value = item[p.key]
  return `${(value * 100).toFixed(1)}%`
}
</script>

<template>
  <v-dialog activator="parent" v-model="dialog" max-width="750">
    <v-card>
      <template #append>
        <v-btn
          icon="$close"
          density="compact"
          variant="text"
          @click="dialog = false"
        />
      </template>

      <v-card-text>
        <table class="detail-analysts-modal-menu__table">
          <thead>
            <tr>
              <th></th>
              <th>{{ company.ticker }}</th>
              <th>{{ t('finance.industry') }}</th>
              <th>{{ t('finance.market') }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="p in periods" :key="p.key">
              <td class="detail-shareholder-returns-modal-menu__period_title">
                {{ p.name }}
              </td>
              <td>{{ humanize(company, p) }}</td>
              <td>{{ humanize(company.sector_market, p) }}</td>
              <td>{{ humanize(company.market, p) }}</td>
            </tr>
          </tbody>
        </table>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<style scoped>
.detail-analysts-modal-menu__table {
  width: 100%;
  border-spacing: 0;
  border: 1px solid rgba(38, 46, 58, 0.2);
  font-size: 0.875rem;
  line-height: 1.5;
}
.detail-analysts-modal-menu__table tr {
  height: 40px;
}
.detail-analysts-modal-menu__table thead th {
  padding: 8px;
  vertical-align: top;
  background: rgba(38, 46, 58, 0.1);
  font-weight: 500;
  text-align: left;
}
.detail-analysts-modal-menu__table td {
  width: calc((100% - 35%) / 4);
  padding: 8px;
  text-align: left;
  border-top: 1px solid rgba(38, 46, 58, 0.2);
  vertical-align: top;
}
.detail-analysts-modal-menu__table td:first-child {
  width: 35%;
}
.detail-shareholder-returns-modal-menu__period_title {
  font-size: 0.75rem;
}
</style>
