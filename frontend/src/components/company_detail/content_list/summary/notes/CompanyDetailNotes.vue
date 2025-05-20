<script setup lang="ts">
// Components
import BookIcon from '@/components/icons/BookIcon.vue'
import CompanyDetailNote from '@/components/company_detail/content_list/summary/notes/CompanyDetailNote.vue'
import NotesEditor from '@/components/company_detail/content_list/summary/notes/NotesEditor.vue'

// Composables
import { useCompanyDetailStore } from '@/store/companyDetail'
import { usePageStore } from '@/store/page'
import { useAuthStore } from '@/store/auth'
import { useI18n } from 'vue-i18n'

// Utilities
import { computed } from 'vue'

// Types
import type { Note } from '@/types/notes'

const authStore = useAuthStore()
const pageStore = usePageStore()
const companyDetailStore = useCompanyDetailStore()
const notes = computed<Note[]>(() => companyDetailStore.notes)
const { t } = useI18n()

function onOpenLateral() {
  companyDetailStore.lateralMenuComponentName = 'notes'
  pageStore.extended = true
}
</script>

<template>
  <v-card color="surface-light" class="mb-4 pa-4">
    <v-card-title class="pt-4">
      <v-badge color="surface-bright" :content="notes.length" floating>
        {{ t('companyDetail.overview.notes.header') }}
      </v-badge>
    </v-card-title>

    <v-empty-state
      v-if="!notes.length"
      :title="t('companyDetail.overview.notes.placeholder')"
    >
      <template #media><book-icon /></template>

      <template #actions>
        <v-btn
          prepend-icon="$iEdit"
          color="info"
          rounded="large"
          :disabled="!authStore.isAuthenticated"
          @click="() => (companyDetailStore.notesEditorIsActive = true)"
        >
          <notes-editor />
          {{ t('buttons.addNote') }}
        </v-btn>
      </template>
    </v-empty-state>

    <v-card-item v-else>
      <v-row class="mb-2">
        <v-col v-for="note in notes.slice(0, 3)" :key="`note-${note.id}`">
          <company-detail-note :note />
        </v-col>
      </v-row>
      <v-btn
        color="info"
        :text="t('buttons.seeMore')"
        block
        variant="tonal"
        @click="onOpenLateral"
        :disabled="pageStore.extended"
      />
    </v-card-item>
  </v-card>
</template>
