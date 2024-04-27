<script lang="ts">
import {defineComponent} from 'vue'
import CompanyDetailNotesModalMenuHeader
  from "@/components/company_detail/summary/notes/CompanyDetailNotesModalMenuHeader.vue";
import CompanyDetailNotesModalMenuMain
  from "@/components/company_detail/summary/notes/CompanyDetailNotesModalMenuMain.vue";
import CompanyDetailNotesModalMenuFooter
  from "@/components/company_detail/summary/notes/CompanyDetailNotesModalMenuFooter.vue";
import CompanyDetailModalMenu from "@/components/UI/CompanyDetailModalMenu.vue";
import {Editor} from "@tiptap/vue-3";
import {StarterKit} from "@tiptap/starter-kit";
import {Placeholder} from "@tiptap/extension-placeholder";
import axios from "axios";
import {mapActions, mapGetters, mapMutations} from "vuex";

export default defineComponent({
  name: "CompanyDetailNotesModalMenu",
  components: {
    CompanyDetailModalMenu,
    CompanyDetailNotesModalMenuFooter,
    CompanyDetailNotesModalMenuMain,
    CompanyDetailNotesModalMenuHeader
  },
  data() {
    return {
      editor: null,
      checkInterval: null,
      saveStatus: 'Saved',
      contentLengthMax: 10000,
      isSaving: false,
    }
  },
  mounted() {
    this.setNoteSavedContent(this.note.body)
    this.checkInterval = setInterval(() => this.checkIfChanged(), 5000)

    this.editor = new Editor({
      content: this.note.body,
      onUpdate: () => {
        if (this.note.body !== this.editor.getHTML()) {
          this.note.body = this.editor.getHTML()
        }
      },
      extensions: [
          StarterKit,
          Placeholder.configure({
            emptyEditorClass: 'is-editor-empty',
            placeholder: 'Write your thoughts, links, and company narrative',
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
    window.clearInterval(this.checkInterval)
    this.checkIfChanged()
    this.editor.destroy()
    const new_note = {
      id: null,
      body: null,
      created: null,
      updated: null,
      company: this.company.id,
    }
    this.setNote(new_note)
    this.setNoteSavedContent('')
    console.log(`${this.$options.name} was UNMOUNTED`)
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
      this.note.body.length
    },
    ...mapGetters({
      company: "companyDetail/getCompany",
      note: 'companyDetail/getNote',
      savedContent: "companyDetail/getNoteSavedContent",
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
        company_id: this.note.company,
        content: this.note.body,
        updated: new Date(),
      }).forEach(([key, val]) => formData.append(key, val))

      this.saveStatus = 'Saving...'

      if (this.note.id) {
        await axios
          .put(`/notes/api/v1/notes/${this.note.id}/`, formData)
          .then(response => {
            this.setNoteSavedContent(response.data.body)
            this.setNote(response.data)
            this.updateNotesWithNewNote(response.data)
          })
          .catch(error => console.log(error))
      } else {
        await axios
          .post('/notes/api/v1/notes/', formData)
          .then(response => {
            this.setNote(response.data)
            this.setNoteSavedContent(response.data.body)
            this.addNewNote(this.note)
          })
          .catch(error => console.log(error))
      }

      this.saveStatus = 'Saved'
    }
  },
})
</script>

<template>
<CompanyDetailModalMenu>

  <CompanyDetailNotesModalMenuHeader/>

  <CompanyDetailNotesModalMenuMain :editor/>

  <CompanyDetailNotesModalMenuFooter :saveStatus :editor/>

</CompanyDetailModalMenu>
</template>
