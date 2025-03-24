<script setup lang="ts">
// Components
import CompanyDetailHeaderInfoPanel from '@/components/company_detail/header/CompanyDetailHeaderInfoPanel.vue'
import BaseCard from '@/apps/visagiste/components/BaseCard/BaseCard.vue'
import BaseBreadcrumbs from '@/apps/visagiste/components/BaseBreadcrumbs/BaseBreadcrumbs.vue'
import BaseCardItem from '@/apps/visagiste/components/BaseCard/BaseCardItem.vue'
import BaseCardActions from '@/apps/visagiste/components/BaseCard/BaseCardActions.vue'
import BaseButton from '@/apps/visagiste/components/BaseButton/BaseButton.vue'
import BaseDialog from '@/apps/visagiste/components/BaseDialog/BaseDialog.vue'
import BaseCardText from '@/apps/visagiste/components/BaseCard/BaseCardText.vue'
import CompanyDetailPortfolioModalMenu from '@/components/company_detail/content_list/summary/portfolio/CompanyDetailPortfolioModalMenu.vue'
import BaseImage from '@/apps/visagiste/components/BaseImage/BaseImage.vue'
import BaseAvatar from '@/apps/visagiste/components/BaseAvatar/BaseAvatar.vue'
import BaseSkeletonLoader from '@/apps/visagiste/components/BaseSkeletonLoader/BaseSkeletonLoader.vue'

// Composables
import { useCompanyDetailStore } from '@/store/companyDetail'
import { useAuthStore } from '@/store/auth'

// Utilities
import { computed, shallowRef } from 'vue'
import { RouteNamesEnum } from '@/router/routes.types'

// Types
import type { DetailCompany } from '@/types/invest'

const companyDetailStore = useCompanyDetailStore()
const authStore = useAuthStore()
const company = computed<DetailCompany>(() => companyDetailStore.company)
const loading = computed(() => companyDetailStore.fetchingCompany)

const portfolioDialog = shallowRef(false)
const breadcrumbs = computed(() => [
  {
    title: 'Markets',
    disabled: false,
    to: { name: RouteNamesEnum.company_list },
  },
  {
    title: companyDetailStore.company.title || 'Company',
    disabled: true,
    to: {
      name: RouteNamesEnum.company_detail,
      params: { companySlug: companyDetailStore.company.slug },
    },
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
  <base-card
    class="px-4 mb-4"
    style="z-index: 1"
    :loading="companyDetailStore.fetchingCompany && 'info'"
  >
    <template #image>
      <base-image
        class="opacity-70"
        :src="companyDetailStore.company.sector.main_header"
        cover
      >
        <div
          v-if="company.sector.main_header"
          class="company-header__image-mask"
        ></div>
      </base-image>
    </template>
    <base-breadcrumbs :items="breadcrumbs" />
    <base-card-item>
      <template #prepend>
        <base-skeleton-loader v-if="loading" type="avatar" />
        <base-avatar v-else :image="company.logo_url" size="60" />
      </template>
      <template #title>
        <base-skeleton-loader v-if="loading" type="text" width="250" />
        <template v-else>{{ company.title }}</template>
      </template>
      <template #subtitle>
        <base-skeleton-loader v-if="loading" type="text" width="250" />
        <template v-else>
          {{
            `${company.market.title}:${company.slug?.toUpperCase()} Stock Report`
          }}
        </template>
      </template>
    </base-card-item>
    <base-card-actions class="justify-end">
      <template v-if="loading">
        <base-skeleton-loader width="250" type="button@3" />
      </template>
      <template v-else>
        <base-button
          v-if="!company.is_watchlisted"
          prepend-icon="$ratingEmpty"
          text="add to watchlist"
          color="info"
          variant="flat"
          :loading="companyDetailStore.watchlistLoading"
          :disabled="!authStore.isAuthenticated"
          @click="companyDetailStore.toggleWatchlisted"
          size="small"
        />

        <template v-else>
          <base-button
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

          <base-button
            prepend-icon="$iEdit"
            text="add note"
            @click="createNote"
            variant="flat"
            color="info"
            size="small"
          />
        </template>

        <base-button
          color="grey"
          :disabled="!authStore.isAuthenticated"
          variant="flat"
          size="small"
        >
          <base-dialog
            activator="parent"
            :title="`Add ${company.ticker} to Portfolio`"
            max-width="700"
            v-model="portfolioDialog"
          >
            <base-card title="Portfolio">
              <template #append>
                <base-button
                  icon="$close"
                  density="compact"
                  variant="text"
                  @click="portfolioDialog = false"
                />
              </template>
              <base-card-text>
                <CompanyDetailPortfolioModalMenu />
              </base-card-text>
            </base-card>
          </base-dialog>

          Add to portfolio
        </base-button>
      </template>
    </base-card-actions>
    <base-card-text>
      <company-detail-header-info-panel />
    </base-card-text>
  </base-card>
</template>

<style scoped>
.company-header__image-mask {
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1;
  background: rgb(12 9 9 / 70%);
}
</style>
