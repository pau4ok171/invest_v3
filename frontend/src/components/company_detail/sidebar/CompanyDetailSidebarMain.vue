<script setup lang="ts">
// Composables
import { useCompanyDetailStore } from '@/store/companyDetail'
import { useAuthStore } from '@/store/auth'
import { useI18n } from 'vue-i18n'
import { useTranslations } from '@/composables/translations'

// Utilities
import { computed } from 'vue'
import { toast } from 'vue3-toastify'

// Types
import type { DetailCompany } from '@/types/invest'

const companyDetailStore = useCompanyDetailStore()
const authStore = useAuthStore()
const company = computed<DetailCompany>(() => companyDetailStore.company)
const { t } = useI18n()
const { getTranslation } = useTranslations()

function addToClipboard() {
  navigator.clipboard
    .writeText(location.href)
    .then(() => {
      toast.success(t('toasts.linkCopied'))
    })
    .catch((err) => {
      console.log(err)
    })
}

function createNote() {
  companyDetailStore.note = {
    id: null,
    text: null,
    body: null,
    created_at: null,
    updated_at: null,
    company: company.value.id || -1,
  }
  companyDetailStore.noteSavedContent = ''

  companyDetailStore.notesEditorIsActive = true
}

function humanizeFinancial(val: number = 0, currencySymbol: string = '') {
  if (val === 0) return 'n/a'
  for (const unit of ['', 't', 'M', 'B', 'T']) {
    if (Math.abs(val) < 1000) return currencySymbol + val.toFixed(2) + unit
    val /= 1000
  }
  return currencySymbol + val.toFixed(2) + 'Q'
}
</script>

<template>
  <div class="detail-sidebar__main">
    <p class="detail-sidebar__title">
      {{ getTranslation(company.translations, 'title') }}
      <v-btn
        icon="$iCopy"
        @click="addToClipboard"
        size="small"
        density="comfortable"
      />
    </p>
    <h3 v-if="company.market" class="detail-sidebar__text">
      {{ company.market.title }}:{{ company.slug?.toUpperCase() }}
      {{ t('companyDetail.header.stockReport') }}
    </h3>
    <p
      v-if="company.price_data"
      class="detail-sidebar__text detail-sidebar__text--small"
    >
      {{ t('companyDetail.header.shortMarketCap') }}:
      {{
        humanizeFinancial(
          company.price_data.capitalisation,
          company.formatting.primaryCurrencySymbol
        )
      }}
    </p>

    <section class="detail-sidebar__button-list">
      <template v-if="authStore.profile?.watchlist.includes(company.uid)">
        <v-btn
          icon="$ratingFull"
          color="blue"
          rounded="lg"
          size="small"
          density="comfortable"
          :loading="authStore.watchlistLoading"
          :disabled="!authStore.isAuthenticated"
          @click="authStore.updateWatchlist(company)"
        />

        <v-btn
          prepend-icon="$iPen"
          :text="t('buttons.addNote')"
          color="blue"
          size="small"
          @click="createNote"
        />
      </template>

      <template v-else>
        <v-btn
          prepend-icon="$ratingEmpty"
          :text="t('buttons.addToWatchlist')"
          color="blue"
          size="small"
          :loading="authStore.watchlistLoading"
          :disabled="!authStore.isAuthenticated"
          @click="authStore.updateWatchlist(company)"
        />
      </template>
    </section>
  </div>
</template>

<style lang="scss" scoped>
.detail-sidebar__main {
  opacity: 0;
}
.detail-sidebar__title {
  width: 100%;
  font-size: 1rem;
  line-height: 1.5;
  font-weight: 500;
  overflow: hidden;
  text-overflow: ellipsis;
}
.detail-sidebar__text {
  width: 100%;
  font-size: 0.875rem;
  line-height: 1.5;
  font-weight: 500;
  overflow: hidden;
  text-overflow: ellipsis;
  color: rgba(var(--v-theme-on-surface), var(--v-medium-emphasis-opacity));
}
.detail-sidebar__button-list {
  display: flex;
  gap: 4px;
  margin-top: 12px;
  min-height: 32px;
  position: relative;
  z-index: 1;
}
.detail-sidebar__text--small {
  font-size: 0.75rem;
}
</style>
