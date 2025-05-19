<script setup lang="ts">
// Components
import CompanyDetailSidebar from '@/components/company_detail/sidebar/CompanyDetailSidebar.vue'
import CompanyDetailContentList from '@/components/company_detail/content_list/CompanyDetailContentList.vue'

// Composables
import { useDisplay, useLayout } from 'vuetify'
import { provideSectionContext } from '@/composables/sectionObserver'
import { useI18n } from 'vue-i18n'

// Utilities
import { computed } from 'vue'
import { SECTIONS } from '@/assets/static/companyDetail'

const layout = useLayout()
const { activeSection, changeSection } = provideSectionContext(layout)

const { lgAndUp } = useDisplay()
const { t } = useI18n()

const sections = computed(() =>
  SECTIONS.map((s) => ({
    ...s,
    shortTitle: t(`companyDetail.sections.${s.value}Short`),
  }))
)
</script>

<template>
  <div class="detail__content">
    <v-app-bar v-if="!lgAndUp">
      <v-tabs
        :model-value="[activeSection]"
        @update:model-value="(section) => changeSection([section as string])"
        selected-class="text-info"
        center-active
        show-arrows
      >
        <v-tab
          v-for="section in sections"
          :key="`section-tab-${section.value}`"
          class="text-body-2 text-capitalize"
          :text="section.shortTitle"
          :value="section.value"
        />
      </v-tabs>
    </v-app-bar>

    <company-detail-sidebar v-else />

    <v-defaults-provider
      :defaults="{
        VCardSubtitle: {
          style: { whiteSpace: 'normal' },
        },
      }"
    >
      <company-detail-content-list />
    </v-defaults-provider>
  </div>
</template>

<style scoped>
.detail__content {
  display: flex;
  flex-flow: wrap;
  justify-content: left;
}
</style>
