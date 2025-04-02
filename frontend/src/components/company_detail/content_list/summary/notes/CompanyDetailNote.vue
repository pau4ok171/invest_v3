<script setup lang="ts">
// Composables
import { useCompanyDetailStore } from '@/store/companyDetail'

// Types
import type { PropType } from 'vue'
import type { Note } from '@/types/notes'

const props = defineProps({
  note: {
    type: Object as PropType<Note>,
    required: true,
  },
})

const companyDetailStore = useCompanyDetailStore()

function editNote(note: Note) {
  companyDetailStore.note = note
  companyDetailStore.notesEditorIsActive = true
}
</script>

<template>
  <v-card color="surface-bright" @click="() => editNote(note)">
    <v-card-text class="company-detail-notes__note-text">{{
      note.text
    }}</v-card-text>
    <v-card-item>
      <template #prepend>
        <div class="opacity-50" style="font-size: 0.75rem">
          <span class="mr-1">{{
            note.created === note.updated ? 'Created' : 'Updated'
          }}</span>
          <time v-if="note.updated" :datetime="note.updated">{{
            new Date(note.updated).toLocaleDateString('ru-RU')
          }}</time>
        </div>
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
