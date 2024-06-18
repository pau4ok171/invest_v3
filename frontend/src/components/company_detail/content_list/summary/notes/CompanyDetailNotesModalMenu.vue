<script lang="ts">
import {defineComponent} from 'vue'
import CompanyDetailNotesModalMenuHeader
  from "@/components/company_detail/content_list/summary/notes/CompanyDetailNotesModalMenuHeader.vue";
import CompanyDetailNotesModalMenuMain
  from "@/components/company_detail/content_list/summary/notes/CompanyDetailNotesModalMenuMain.vue";
import CompanyDetailNotesModalMenuFooter
  from "@/components/company_detail/content_list/summary/notes/CompanyDetailNotesModalMenuFooter.vue";
import {Editor} from "@tiptap/vue-3";
import {StarterKit} from "@tiptap/starter-kit";
import {Placeholder} from "@tiptap/extension-placeholder";
import {CharacterCount} from '@tiptap/extension-character-count';
import axios from "axios";
import {mapActions, mapGetters, mapMutations} from "vuex";
import {toast} from "vue3-toastify";

export default defineComponent({
  name: "CompanyDetailNotesModalMenu",
  components: {
    CompanyDetailNotesModalMenuFooter,
    CompanyDetailNotesModalMenuMain,
    CompanyDetailNotesModalMenuHeader
  },
  data() {
    return {
      editor: null as any,
      checkInterval: null as any,
      saveStatus: 'Saved',
      contentLengthMax: 10000,
      isSaving: false,
      limitIsExceeded: false,
    }
  },
  mounted() {
    this.setNoteSavedContent(this.note.body)

    this.editor = new Editor({
      content: this.note.body,
      onUpdate: () => {
        if (this.checkInterval) window.clearTimeout(this.checkInterval)
        this.checkInterval = setTimeout(() => this.checkIfChanged(), 2000)
        if (this.note.body !== this.editor.getHTML()) {
          this.note.body = this.editor.getHTML()
          this.note.text = this.editor.getText()
        }
      },
      extensions: [
          StarterKit,
          Placeholder.configure({
            emptyEditorClass: 'is-editor-empty',
            placeholder: 'Write your thoughts, links, and company narrative',
          }),
          CharacterCount.configure({
            limit: this.contentLengthMax,
          }),
      ],
    })
    this.editor.setOptions({
      editorProps: {
        attributes: {
          class: 'detail_notes_modal_menu_main__editor',
        },
      },
    })
  },
  beforeUnmount() {
    window.clearTimeout(this.checkInterval)
    this.checkIfChanged()
    this.editor.destroy()
    const new_note = {
      id: null,
      body: null,
      text: null,
      created: null,
      updated: null,
      company: this.company.id,
    }
    this.setNote(new_note)
    this.setNoteSavedContent('')
  },
  watch: {
    note(value) {
      const isSame = this.editor.getHTML() === value
      if (isSame) {
        return
      }
      this.editor.commands.setContent(value.body, false)
    },
  },
  computed: {
    contentLength() {
      return this.note?.text?.length
    },
    usedVolume() {
      const circleMin = 56.248
      const circleMax = 111.248
      const circleDashArray = circleMin + (this.contentLength / this.contentLengthMax * (circleMax - circleMin)) || circleMin
      this.limitIsExceeded = this.contentLength >= this.contentLengthMax
      return  circleDashArray < circleMax ?  circleDashArray : circleMax
    },
    ...mapGetters({
      company: "companyDetail/getCompany",
      note: 'companyDetail/getNote',
      savedContent: "companyDetail/getNoteSavedContent",
    }),
    ...mapGetters({
      notesModalIsLateral: "companyDetail/getNotesModalMenuIsLateral",
    }),
  },
  methods: {
    ...mapMutations({
      addNewNote: 'companyDetail/addNewNote',
      setNote: "companyDetail/setNote",
      setNoteSavedContent: "companyDetail/setNoteSavedContent",
    }),
    ...mapActions({
      updateNotesWithNewNote: "companyDetail/updateNotesWithNewNote"
    }),
    checkIfChanged() {
      if (this.note.body !== this.savedContent) {
        this.saveNote()
      }
    },
    async saveNote() {
      const formData = new FormData()
      Object.entries({
        note_id: this.note.id,
        company_id: this.note.company || this.company.id,
        content: this.note.body,
        text : this.note.text,
        updated: new Date().toISOString(),
      }).forEach(([key, val]) => formData.append(key, val))

      this.saveStatus = 'Saving...'

      if (this.note.id) {
        await axios
          .put(`/notes/api/v1/notes/${this.note.id}/`, formData)
          .then(response => {
            this.setNoteSavedContent(response.data.body)
            this.setNote(response.data)
            this.updateNotesWithNewNote(response.data)
            toast.success('Note successfully saved')
          })
          .catch(error => console.log(error))
      } else {
        await axios
          .post('/notes/api/v1/notes/', formData)
          .then(response => {
            this.setNote(response.data)
            this.setNoteSavedContent(response.data.body)
            this.addNewNote(this.note)
            toast.success('Note successfully saved')
          })
          .catch(error => console.log(error))
      }

      this.saveStatus = 'Saved'
    }
  },
})
</script>

<template>
<teleport to="body">

  <div class="detail_modal_menu__wrapper" v-if="!notesModalIsLateral"></div>

  <div class="detail_modal_menu" :class="{'detail_modal_menu--lateral': notesModalIsLateral}">
    <CompanyDetailNotesModalMenuHeader/>

    <CompanyDetailNotesModalMenuMain :editor/>

    <CompanyDetailNotesModalMenuFooter :limitIsExceeded :usedVolume :saveStatus :editor/>
</div>

</teleport>
</template>

<style>
.detail_modal_menu__wrapper {
  z-index: 9999;
  position: fixed;
  width: 100vw;
  height: 100vh;
  top: 0;
  left: 0;
  background-color: #000;
  opacity: 0.8;
  transition: opacity .4s cubic-bezier(.23, 1, .32, 1) 0s;
}
.detail_modal_menu {
  z-index: 9999;
  position: fixed;
  display: grid;
  grid-template-rows: auto 1fr auto;
  width: 100%;
  height: calc(100dvh - 40px);
  max-width: 886px;
  overflow-x: hidden;
  top: auto;
  right: max(0px, 50vw - 443px);
  bottom: 0;
  background-color: #1b222d;
  border: 1px solid rgb(38, 46, 58);
  touch-action: none;
  color: #8c929b;
  border-top-left-radius: 8px;
  border-top-right-radius: 8px;
  box-shadow: rgba(11, 14, 19, .25) -10px -10px 10px, rgba(11, 14, 19, .1) 10px 10px 10px;
  transform: translate3d(0px, 0%, 0px);
  transition: transform 0.4s cubic-bezier(0.23, 1, 0.32, 1) 0s, top 0.4s cubic-bezier(0.23, 1, 0.32, 1) 0s, right 0.4s cubic-bezier(0.23, 1, 0.32, 1) 0s, max-width 0.4s cubic-bezier(0.23, 1, 0.32, 1) 0s, height 0.4s cubic-bezier(0.23, 1, 0.32, 1) 0s;
}
.detail_modal_menu--lateral {
  left: auto;
  right: 40px;
  width: 433px;
  height: 420px;
  padding: 0;
  overflow: visible;
  transform: translate3d(0px, 0%, 0px);
}
.detail_modal_menu--lateral .detail_modal_menu__main {
    min-height: 200px;
    height: 270px;
}
</style>
