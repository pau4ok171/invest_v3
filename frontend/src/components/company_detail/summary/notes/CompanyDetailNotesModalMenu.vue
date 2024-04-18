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
    }
  },
  mounted() {
    this.editor = new Editor({
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
    this.editor.destroy()
  },

})
</script>

<template>
<CompanyDetailModalMenu>

  <CompanyDetailNotesModalMenuHeader/>

  <CompanyDetailNotesModalMenuMain :editor/>

  <CompanyDetailNotesModalMenuFooter :editor/>

</CompanyDetailModalMenu>
</template>
