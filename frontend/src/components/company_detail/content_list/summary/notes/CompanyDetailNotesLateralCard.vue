<script setup lang="ts">
// Components
import CompanyDetailNote from '@/components/company_detail/content_list/summary/notes/CompanyDetailNote.vue'

// Composables
import { usePageStore } from '@/store/page'
import { useCompanyDetailStore } from '@/store/companyDetail'
import { useI18n } from 'vue-i18n'

// Utilities
import { computed } from 'vue'

// Types
import type { Note } from '@/types/notes'

const pageStore = usePageStore()
const store = useCompanyDetailStore()
const notes = computed<Note[]>(() => store.notes)
const { t } = useI18n()
</script>

<template>
  <v-card height="100%">
    <v-toolbar
      :title="t('companyDetail.overview.notes.header')"
      color="surface"
    >
      <template #append>
        <v-btn
          class="mr-1"
          prepend-icon="$plus"
          :text="t('buttons.add')"
          size="small"
          variant="tonal"
          color="info"
        />
        <v-btn
          icon="$close"
          size="small"
          density="comfortable"
          rounded="lg"
          @click="pageStore.extended = false"
        />
      </template>
    </v-toolbar>
    <div style="overflow-y: auto; height: calc(100% - 88px)">
      <v-card-item v-for="note in notes" :key="`lateral-note-${note.id}`">
        <company-detail-note :note />
      </v-card-item>
    </div>
  </v-card>
</template>
