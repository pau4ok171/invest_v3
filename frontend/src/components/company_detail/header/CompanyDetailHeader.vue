<script setup lang="ts">
// Components
import CompanyDetailHeaderInfoPanel from '@/components/company_detail/header/CompanyDetailHeaderInfoPanel.vue'
import CompanyDetailPortfolioDialog from '@/components/company_detail/content_list/summary/portfolio/CompanyDetailPortfolioDialog.vue'

// Composables
import { useCompanyDetailStore } from '@/store/companyDetail'
import { useAuthStore } from '@/store/auth'
import { useI18n } from 'vue-i18n'

// Utilities
import { computed } from 'vue'
import { RouteNamesEnum } from '@/router/routes.types'

// Types
import type { DetailCompany } from '@/types/invest'

const companyDetailStore = useCompanyDetailStore()
const authStore = useAuthStore()
const company = computed<DetailCompany>(() => companyDetailStore.company)
const loading = computed(() => companyDetailStore.fetchingCompany)
const { t } = useI18n()

const breadcrumbs = computed(() => [
  {
    title: 'Markets',
    disabled: false,
    to: { name: RouteNamesEnum.company_list },
  },
  {
    title: companyDetailStore.company.title || 'Company',
    disabled: true,
  },
])

function createNote() {
  companyDetailStore.note = {
    id: null,
    body: null,
    text: null,
    created: null,
    updated: null,
    company: company.value.id || -1,
  }
  companyDetailStore.noteSavedContent = ''

  companyDetailStore.notesEditorIsActive = true
}
</script>

<template>
  <v-defaults-provider
    :defaults="{
      VSkeletonLoader: {
        color: 'surface',
      },
    }"
  >
    <v-card
      class="px-4 mb-4"
      style="z-index: 1"
      :loading="companyDetailStore.fetchingCompany && 'info'"
    >
      <template #image>
        <v-img
          v-if="!companyDetailStore.fetchingCompany"
          class="opacity-70"
          :src="companyDetailStore.company.sector.main_header"
          cover
        >
          <div
            v-if="company.sector.main_header"
            class="company-header__image-mask"
          ></div>
        </v-img>
      </template>
      <v-breadcrumbs :items="breadcrumbs" />
      <v-card-item>
        <template #prepend>
          <v-skeleton-loader v-if="loading" type="avatar" height="60" />
          <v-avatar v-else :image="company.logo_url" size="60" />
        </template>
        <template #title>
          <v-skeleton-loader
            v-if="loading"
            type="text"
            width="250"
            height="28"
          />
          <template v-else>{{ company.title }}</template>
        </template>
        <template #subtitle>
          <v-skeleton-loader
            v-if="loading"
            type="text"
            width="250"
            height="28"
          />
          <template v-else>
            {{
              `${company.market.title}:${company.slug?.toUpperCase()} ${t('companyDetail.header.stockReport')}`
            }}
          </template>
        </template>
      </v-card-item>
      <v-card-actions class="justify-lg-end">
        <v-skeleton-loader
          v-if="loading"
          class="company-detail-header__skeleton-loader"
          width="250"
          type="button@3"
          height="28"
        />
        <template v-else>
          <v-btn
            v-if="!company.is_watchlisted"
            prepend-icon="$ratingEmpty"
            :text="t('buttons.addToWatchlist')"
            color="info"
            variant="flat"
            :loading="companyDetailStore.watchlistLoading"
            :disabled="!authStore.isAuthenticated"
            @click="companyDetailStore.toggleWatchlisted"
            size="small"
          />

          <template v-else>
            <v-btn
              icon="$ratingFull"
              color="info"
              variant="flat"
              :loading="companyDetailStore.watchlistLoading"
              :disabled="!authStore.isAuthenticated"
              @click="companyDetailStore.toggleWatchlisted"
              size="small"
              rounded="lg"
              density="comfortable"
            />

            <v-btn
              prepend-icon="$iEdit"
              :text="t('buttons.addNote')"
              @click="createNote"
              variant="flat"
              color="info"
              size="small"
            />
          </template>

          <v-btn
            color="grey"
            :disabled="!authStore.isAuthenticated"
            variant="flat"
            size="small"
          >
            <company-detail-portfolio-dialog />

            {{ t('buttons.addToPortfolio') }}
          </v-btn>
        </template>
      </v-card-actions>
      <v-card-text>
        <company-detail-header-info-panel />
      </v-card-text>
    </v-card>
  </v-defaults-provider>
</template>

<style lang="scss">
.company-header__image-mask {
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1;
  background: rgba(var(--v-theme-mask), var(--v-medium-emphasis-opacity));
}
.company-detail-header__skeleton-loader {
  > .v-skeleton-loader__button {
    height: 28px;
    margin-top: 0;
    margin-bottom: 0;
  }
}
</style>
