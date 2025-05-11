<script setup lang="ts">
// Components
import CompanyDetailSidebar from '@/components/company_detail/sidebar/CompanyDetailSidebar.vue'
import CompanyDetailContentList from '@/components/company_detail/content_list/CompanyDetailContentList.vue'

// Composables
import { useDisplay, useLayout } from 'vuetify'
import { provideSectionContext } from '@/composables/sectionObserver'

// Utilities
import { SECTIONS } from '@/assets/static/companyDetail'

const layout = useLayout()
const { activeSection, changeSection } = provideSectionContext(layout)

const { lgAndUp } = useDisplay()
</script>

<template>
  <div class="detail__content">
    <v-app-bar v-if="!lgAndUp">
      <v-tabs
        :model-value="[activeSection]"
        @update:model-value="(section) => changeSection([section as string])"
        selected-class="text-info"
      >
        <v-tab
          v-for="section in SECTIONS"
          :key="`section-tab-${section.value}`"
          class="text-body-2 text-capitalize"
          :text="section.shortTitle"
          :value="section.value"
        />
      </v-tabs>
    </v-app-bar>

    <company-detail-sidebar v-else />

    <company-detail-content-list />
  </div>
</template>

<style scoped>
.detail__content {
  display: flex;
  flex-flow: wrap;
  justify-content: left;
}
</style>
