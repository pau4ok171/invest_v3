<script setup lang="ts">
// Components
import BookIcon from '@/components/icons/BookIcon.vue'
import CompanyDetailNotesDialog from '@/components/company_detail/content_list/summary/notes/NotesEditor.vue'

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
  <v-card color="surface-light" class="mb-4 pa-4">
    <v-card-title class="pt-4">
      <v-badge color="surface-bright" :content="notes.length" floating
        >My Notes</v-badge
      >
    </v-card-title>

    <v-empty-state
      v-if="!notes.length"
      title="Capture your thoughts, links and company narrative"
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
          <CompanyDetailNotesDialog />
          Add Note
        </v-btn>
      </template>
    </v-empty-state>

    <v-container v-else>
      <v-row class="mb-2">
        <v-col v-for="note in notes.slice(0, 3)" :key="`note-${note.id}`">
          <v-card color="surface-bright" @click="() => editNote(note)">
            <v-card-text class="company-detail-notes__note-text">{{
              note.text
            }}</v-card-text>
            <v-card-item>
              <template #prepend>
                <span class="mr-1">{{
                  note.created === note.updated ? 'Created' : 'Updated'
                }}</span>
                <time v-if="note.updated" :datetime="note.updated">{{
                  new Date(note.updated).toLocaleDateString('ru-RU')
                }}</time>
              </template>
              <template #append>
                <v-btn
                  icon="$iDelete"
                  variant="text"
                  color="error"
                  density="comfortable"
                  size="small"
                  rounded="lg"
                  @click.stop="companyDetailStore.deleteNote(note)"
                />
              </template>
            </v-card-item>
          </v-card>
        </v-col>
      </v-row>
      <!-- TODO: Create Dialog for notes on CompanyDetailNotes -->
      <v-btn color="blue" text="See More" block />
    </v-container>
  </v-card>
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
