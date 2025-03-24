<script setup lang="ts">
// Components
import { BaseButton } from '@/apps/visagiste/components/BaseButton'
import BaseBadge from '@/apps/visagiste/components/BaseBadge/BaseBadge.vue'
import BookIcon from '@/components/icons/BookIcon.vue'
import BaseCard from '@/apps/visagiste/components/BaseCard/BaseCard.vue'
import BaseCardTitle from '@/apps/visagiste/components/BaseCard/BaseCardTitle.vue'
import BaseContainer from '@/apps/visagiste/components/BaseGrid/BaseContainer.vue'
import BaseCol from '@/apps/visagiste/components/BaseGrid/BaseCol.vue'
import BaseEmptyState from '@/apps/visagiste/components/BaseEmptyState/BaseEmptyState.vue'
import CompanyDetailNotesDialog from '@/components/company_detail/content_list/summary/notes/NotesEditor.vue'
import BaseRow from '@/apps/visagiste/components/BaseGrid/BaseRow.vue'
import BaseCardText from "@/apps/visagiste/components/BaseCard/BaseCardText.vue";
import BaseCardItem from "@/apps/visagiste/components/BaseCard/BaseCardItem.vue";

// Composables
import { useCompanyDetailStore } from '@/store/companyDetail'
import { useAuthStore } from '@/store/auth'

// Utilities
import { computed } from 'vue'

// Types
import type { Note } from '@/types/notes'


const authStore = useAuthStore()
const companyDetailStore = useCompanyDetailStore()
const notes = computed<Note[]>(() => companyDetailStore.notes)
const note = computed<Note>(() => companyDetailStore.note)

function editNote(note: Note) {
  companyDetailStore.note = note
  companyDetailStore.notesEditorIsActive = true
}
</script>

<template>
  <base-card color="surface-light" class="mb-4 pa-4">
    <base-card-title class="pt-4">
      <base-badge color="surface-bright" :content="notes.length" floating
        >My Notes</base-badge
      >
    </base-card-title>

    <base-empty-state
      v-if="!notes.length"
      title="Capture your thoughts, links and company narrative"
    >
      <template #media><book-icon /></template>

      <template #actions>
        <base-button
          prepend-icon="$iEdit"
          color="info"
          rounded="large"
          :disabled="!authStore.isAuthenticated"
          @click="() => companyDetailStore.notesEditorIsActive = true"
        >
          <CompanyDetailNotesDialog />
          Add Note
        </base-button>
      </template>
    </base-empty-state>

    <base-container v-else>
      <base-row class="mb-2">
        <base-col v-for="note in notes.slice(0, 3)" :key="`note-${note.id}`">
          <base-card
            color="surface-bright"
            @click="() => editNote(note)"
          >
            <base-card-text class="company-detail-notes__note-text">{{ note.text }}</base-card-text>
            <base-card-item>
              <template #prepend>
                <span class="mr-1">{{
                  note.created === note.updated ? 'Created' : 'Updated'
                }}</span>
                <time v-if="note.updated" :datetime="note.updated">{{
                  new Date(note.updated).toLocaleDateString('ru-RU')
                }}</time>
              </template>
              <template #append>
                <base-button
                  icon="$iDelete"
                  variant="text"
                  color="error"
                  density="comfortable"
                  size="small"
                  rounded="lg"
                  @click.stop="companyDetailStore.deleteNote(note)"
                />
              </template>
            </base-card-item>
          </base-card>
        </base-col>
      </base-row>
      <!-- TODO: Create Dialog for notes on CompanyDetailNotes -->
      <base-button color="blue" text="See More" block />
    </base-container>
  </base-card>
</template>

<style scoped>
.company-detail-notes__note-text {
  height: 75px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 3;
}
</style>
