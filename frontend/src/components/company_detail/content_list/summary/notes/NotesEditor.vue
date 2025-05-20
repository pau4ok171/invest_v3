<script setup lang="ts">
// Composables
import { useCompanyDetailStore } from '@/store/companyDetail'
import { EditorContent, useEditor } from '@tiptap/vue-3'
import { useI18n } from 'vue-i18n'

// Utilities
import { computed, onBeforeUnmount, shallowRef, watch } from 'vue'
import axios from 'axios'
import { toast } from 'vue3-toastify'
import { StarterKit } from '@tiptap/starter-kit'
import { Placeholder } from '@tiptap/extension-placeholder'
import { CharacterCount } from '@tiptap/extension-character-count'

const CONTENT_MAX_LENGTH = 10000

const companyDetailStore = useCompanyDetailStore()
const note = computed(() => companyDetailStore.note)

const dialog = computed(() => companyDetailStore.notesEditorIsActive)
const expanded = shallowRef(false)
const timeoutId = shallowRef(-1)
const saving = shallowRef(false)
const { t } = useI18n()
const savingStatus = computed(() =>
  t(`companyDetail.overview.notes.${saving.value ? 'saving' : 'saved'}`)
)

companyDetailStore.noteSavedContent = note.value.body || ''

const editor = useEditor({
  content: note.value.body,
  editorProps: {
    attributes: {
      class: 'notes-editor__editor',
    },
  },
  onUpdate: () => {
    if (timeoutId.value) window.clearTimeout(timeoutId.value)
    timeoutId.value = setTimeout(saveNote, 2000)
    if (!!editor.value && note.value.body !== editor.value.getHTML()) {
      note.value.body = editor.value.getHTML()
      note.value.text = editor.value.getText()
    }
  },
  extensions: [
    StarterKit,
    Placeholder.configure({
      emptyEditorClass: 'editor--empty-state',
      placeholder: t('companyDetail.overview.notes.placeholder'),
    }),
    CharacterCount.configure({
      limit: CONTENT_MAX_LENGTH,
    }),
  ],
})

const contentLength = computed<number>(() => note.value.text?.length || 0)
const usedVolume = computed(() =>
  Math.min((contentLength.value / CONTENT_MAX_LENGTH) * 100, 100)
)
const limiterColor = computed(() => {
  if (usedVolume.value <= 50) return 'info'
  if (usedVolume.value < 100) return 'warning'
  return 'error'
})

async function saveNote() {
  if (
    note.value.body != null &&
    note.value.body !== companyDetailStore.noteSavedContent
  ) {
    await postNote()
  }
}

async function postNote() {
  const formData = new FormData()
  Object.entries({
    note_id: note.value.id,
    company_id: note.value.company || companyDetailStore.company.id,
    content: note.value.body,
    text: note.value.text,
    updated: new Date().toISOString(),
  }).forEach(([key, val]: [string, any]) => formData.append(key, val))

  saving.value = true

  if (note.value.id) {
    await axios
      .put(`/notes/api/v1/notes/${note.value.id}/`, formData)
      .then((response) => {
        companyDetailStore.noteSavedContent = response.data.body
        companyDetailStore.note = response.data
        companyDetailStore.updateNotes(response.data)
        toast.success('Note successfully saved')
      })
      .catch((error) => console.log(error))
  } else {
    await axios
      .post('/notes/api/v1/notes/', formData)
      .then((response) => {
        companyDetailStore.noteSavedContent = response.data.body
        companyDetailStore.note = response.data
        companyDetailStore.addNote(response.data)
        toast.success('Note successfully saved')
      })
      .catch((error) => console.log(error))
  }

  saving.value = false
}

watch(
  () => note.value,
  (value) => {
    if (!editor.value || editor.value.getHTML() === value.body) return

    editor.value?.commands.setContent(value.body, false)
  },
  { deep: true }
)

onBeforeUnmount(() => {
  window.clearTimeout(timeoutId.value)
  saveNote()
  editor.value?.destroy()
  companyDetailStore.note = {
    id: null,
    body: null,
    text: null,
    created: null,
    updated: null,
    company: companyDetailStore.company.id || -1,
  }
  companyDetailStore.noteSavedContent = ''

  companyDetailStore.notesEditorIsActive = false
})
</script>

<template>
  <v-dialog
    transition="slide-y-transition"
    v-model="dialog"
    @update:modelValue="
      (v: boolean) => (companyDetailStore.notesEditorIsActive = v)
    "
    :class="['notes-editor', { 'notes-editor--expanded': expanded }]"
    :scrim="!!expanded"
    scroll-strategy="reposition"
    :width="expanded ? 866 : 433"
    :height="expanded ? 662 : 420"
    persistent
  >
    <v-card color="surface-light" rounded="lg" class="pa-1">
      <v-toolbar flat>
        <template #prepend>
          <v-btn
            :icon="expanded ? '$iReduce' : '$iExpand'"
            rounded="lg"
            variant="text"
            density="comfortable"
            @click="() => (expanded = !expanded)"
          />
          <v-card-text>MISC:SBER</v-card-text>
        </template>
        <template #append>
          <v-btn
            icon="$iBell"
            rounded="lg"
            variant="text"
            density="comfortable"
          />
          <v-btn
            icon="$close"
            rounded="lg"
            variant="text"
            density="comfortable"
            @click="companyDetailStore.notesEditorIsActive = false"
          />
        </template>
      </v-toolbar>
      <v-card-text class="py-0">
        <div class="notes-editor__content">
          <EditorContent :editor />
        </div>
      </v-card-text>
      <v-divider />
      <v-card-item>
        <template #prepend>
          <v-btn-toggle multiple>
            <v-btn
              icon="$iHeader"
              variant="text"
              @click="editor?.chain().focus().toggleHeading({ level: 1 }).run()"
              :active="editor?.isActive('heading', { level: 1 })"
            />
            <v-btn
              icon="$iBold"
              variant="text"
              @click="editor?.chain().focus().toggleBold().run()"
              :disabled="!editor?.can().chain().focus().toggleBold().run()"
              :active="editor?.isActive('bold')"
            />
            <v-btn
              icon="$menu"
              variant="text"
              @click="editor?.chain().focus().toggleBulletList().run()"
              :active="editor?.isActive('bulletList')"
            />
          </v-btn-toggle>
        </template>
        <template #append>
          <div class="notes-editor__footer-append">
            {{ savingStatus }}
            <v-progress-circular
              :color="limiterColor"
              :model-value="usedVolume"
            />
            <v-btn
              :text="t('buttons.close')"
              color="info"
              @click="() => (companyDetailStore.notesEditorIsActive = false)"
            />
          </div>
        </template>
      </v-card-item>
    </v-card>
  </v-dialog>
</template>

<style lang="scss">
.notes-editor.v-overlay {
  justify-content: flex-end;
  align-items: flex-end;

  &.notes-editor--expanded {
    justify-content: center;
  }
}
.notes-editor__content {
  border-bottom: none;
  overflow-y: auto;
  height: 100%;
  cursor: text;

  > div {
    height: 100%;
  }

  &::-webkit-scrollbar {
    -webkit-box-shadow: 5px 5px 5px -5px rgba(34, 60, 80, 0.2);
    background-color: #f9f9fd;
    border-radius: 10px;
  }
  &::-webkit-scrollbar-thumb {
    border-radius: 10px;
    background: linear-gradient(180deg, #00c6fb, #005bea);
  }
}
.notes-editor__editor {
  appearance: none;
  outline: none;
  width: 100%;
  height: 100%;

  p {
    font-weight: 400;
    font-size: 1.125rem;
    line-height: 1.5;
  }
  h1 {
    font-weight: 500;
    font-size: 1.5rem;
    line-height: 1.25;
  }
  ul {
    margin-top: 12px;
    margin-bottom: 0;
  }
  ul li {
    list-style-type: disc;
    padding-left: 4px;
    margin-left: 24px;
    margin-top: 8px;
    margin-bottom: 0;
  }
  p.editor--empty-state:first-child::before {
    color: #adb5bd;
    content: attr(data-placeholder);
    float: left;
    height: 0;
    pointer-events: none;
  }
}
.notes-editor__footer-append {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}
</style>
