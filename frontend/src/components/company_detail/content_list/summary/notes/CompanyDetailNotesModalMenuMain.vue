<script lang="ts">
import {defineComponent} from 'vue'
import {Editor, EditorContent} from "@tiptap/vue-3";

export default defineComponent({
  name: "CompanyDetailNotesModalMenuMain",
  components: {EditorContent},
  props: {
    editor: Editor,
  },
})
</script>

<template>
<main class="detail_notes_modal_menu_main">
  <EditorContent :editor="editor"/>
</main>
</template>

<style>
.detail_notes_modal_menu_main::-webkit-scrollbar {
    width: 10px;
}
.detail_notes_modal_menu_main::-webkit-scrollbar-track {
	-webkit-box-shadow: 5px 5px 5px -5px rgba(34, 60, 80, .2);
	background-color: #f9f9fd;
	border-radius: 10px;
}
.detail_notes_modal_menu_main::-webkit-scrollbar-thumb {
	border-radius: 10px;
	background: linear-gradient(180deg, #00c6fb, #005bea);
}
.detail_notes_modal_menu_main {
    border-bottom: none;
    overflow-y: auto;
    min-height: 200px;
    padding: 0 24px;
}
.detail_notes_modal_menu_main__editor {
    appearance: none;
    outline: none;
    width: 100%;
    height: 100%;
}
.detail_notes_modal_menu_main__editor p {
    color: #fff;
    font-weight: 400;
    font-size: 1.8rem;
    line-height: 1.5;
}
.detail_notes_modal_menu_main__editor h1 {
    color: #fff;
    font-weight: 500;
    font-size: 2.4rem;
    line-height: 1.25;
}
.detail_notes_modal_menu_main__editor ul {
  margin-top: 12px;
  margin-bottom: 0;
}
.detail_notes_modal_menu_main__editor ul li {
  list-style-type: disc;
  color: rgb(255, 255, 255);
  padding-left: 4px;
  margin-left: 24px;
  margin-top: 8px;
  margin-bottom: 0;
}
.detail_notes_modal_menu_main__editor p.is-editor-empty:first-child::before {
  color: #adb5bd;
  content: attr(data-placeholder);
  float: left;
  height: 0;
  pointer-events: none;
}
</style>