<script setup lang="ts">
// Composables
import { useCompanyDetailStore } from '@/store/companyDetail'
import { useI18n } from 'vue-i18n'

// Utilities
import { computed, ref, shallowRef } from 'vue'

// Types
import type { Portfolio } from '@/types/portfolios'

const store = useCompanyDetailStore()
const company = computed(() => store.company)
const portfolios = computed<Portfolio[]>(() => store.portfolios)
const { t } = useI18n()

const inputMode = shallowRef(false)
const portfolioName = ref(null)
const submitting = shallowRef(false)
const portfolioDialog = shallowRef(false)

async function onCreatePortfolio() {
  const value = portfolioName.value as string | null

  if (!value) return

  submitting.value = true

  const result = await store.createPortfolio(value.trim())

  if (result === 'success') {
    portfolioName.value = null
    inputMode.value = false
  }

  submitting.value = false
}
</script>

<template>
  <v-dialog activator="parent" max-width="700" v-model="portfolioDialog">
    <v-card :title="t('companyDetail.portfolio.title')">
      <template #append>
        <v-btn
          icon="$close"
          density="compact"
          variant="text"
          @click="portfolioDialog = false"
        />
      </template>
      <v-card-item>
        <v-list>
          <v-list-item
            v-for="p in portfolios"
            :key="`portfolio-${p.id}`"
            lines="two"
          >
            <v-list-item-title>{{ p.name }}</v-list-item-title>
            <v-list-item-subtitle>
              {{ t('companyDetail.portfolio.holdings', p.positions.length) }}
            </v-list-item-subtitle>
            <template #append>
              <template v-if="p.positions.includes(company.id as number)">
                <v-btn
                  prepend-icon="$iChecked"
                  :text="t('buttons.added')"
                  color="success"
                  rounded="large"
                  readonly
                  class="mr-2"
                />

                <v-btn
                  icon="$iDelete"
                  color="error"
                  rounded="lg"
                  density="comfortable"
                  @click="store.updatePortfolio('exclude', p)"
                />
              </template>

              <template v-else>
                <v-btn
                  prepend-icon="$plus"
                  :text="t('buttons.add')"
                  color="info"
                  rounded="large"
                  @click="store.updatePortfolio('include', p)"
                />
              </template>
            </template>
          </v-list-item>
        </v-list>
      </v-card-item>

      <v-card-item>
        <v-text-field
          v-if="inputMode"
          v-model="portfolioName"
          v-click-outside="{
            handler: () => (inputMode = false),
            closeConditional: () => !!inputMode,
          }"
          @keydown.enter.stop="onCreatePortfolio"
          @keydown.esc.stop.prevent="inputMode = false"
          :placeholder="t('companyDetail.portfolio.placeholder')"
          single-line
          variant="solo-filled"
          density="comfortable"
          flat
          hide-details
          autofocus
        />

        <v-btn
          v-else
          :text="t('buttons.newPortfolio')"
          color="primary"
          rounded="large"
          variant="tonal"
          @click.stop="inputMode = true"
        />
      </v-card-item>
    </v-card>
  </v-dialog>
</template>
