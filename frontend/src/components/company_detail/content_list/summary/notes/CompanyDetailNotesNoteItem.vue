<script lang="ts">
import {defineComponent} from 'vue';
import type {PropType} from 'vue';
import DotsIcon from "@/components/icons/DotsIcon.vue";
import CompanyDetailNotesToolDropDownMenu
  from "@/components/company_detail/content_list/summary/notes/CompanyDetailNotesToolDropDownMenu.vue";
import {mapActions, mapMutations} from "vuex";
import RoundedButton from "@/components/UI/buttons/RoundedButton.vue";
import type {Note} from "@/types/notes";

export default defineComponent({
  name: "CompanyDetailNotesNoteItem",
  components: {RoundedButton, CompanyDetailNotesToolDropDownMenu, DotsIcon},
  props: {
    note: {
      type: Object as PropType<Note>,
      required: true,
    }
  },
  data() {
    return {
      dropDownMenuIsActive: false
    }
  },
  methods: {
    closeDropDownMenu() {
      this.dropDownMenuIsActive = false
    },
    ...mapActions({
      deleteNote: "companyDetail/deleteNote",
    }),
    ...mapMutations({
      setNote: "companyDetail/setNote",
      setNotesModalMenuIsOpen: "companyDetail/setNotesModalMenuIsOpen",
    }),
    editNote() {
      this.setNote(this.note)
      this.setNotesModalMenuIsOpen(true)
    },
  },
})
</script>

<template>
<section class="detail-notes__note-item">
  <div class="detail-notes__note-main" >
    <button @click="editNote" class="detail-notes__note-button">
      {{ note.text }}
    </button>
  </div>

  <footer class="detail-notes__note-footer">
    <p class="detail-notes_note-created">
      <template v-if="note.created === note.updated">Created</template>
      <template v-else>Updated</template>
      <time :datetime="note.updated">{{ new Date(note.updated).toLocaleDateString('ru-RU') }}</time>
    </p>
    <div class="detail-notes__note-actions">
    <RoundedButton @click="dropDownMenuIsActive=!dropDownMenuIsActive"><DotsIcon/></RoundedButton>
    <CompanyDetailNotesToolDropDownMenu
      v-if="dropDownMenuIsActive"
      @closeDropDownMenu="closeDropDownMenu"
      @editNote="editNote"
      @deleteNote="deleteNote(note)"
    />
    </div>

  </footer>
</section>
</template>

<style scoped>
.detail-notes__note-item {
  display: grid;
  grid-template-rows: 72px 35px;
  padding: 8px;
  border-radius: 8px;
  transition: background .3s cubic-bezier(.23, 1, .32, 1) 0s;
  background-color: rgb(38, 46, 58);
  min-height: 124px;
}
.detail-notes__note-main {
  line-height: 1.5;
  padding: 8px;
  cursor: pointer;
  word-break: break-word;
  font-size: 1.4rem;
  width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 3;
}
.detail-notes__note-button {
  display: flex;
  width: 100%;
  height: 100%;
  color: #fff;
  text-align: left;
  transition: all .3s ease 0s;
  overflow: visible;
  cursor: pointer;
  line-height: 1;
}
.detail-notes__note-footer {
  display: grid;
  grid-template-columns: auto auto;
  -webkit-box-pack: justify;
  justify-content: space-between;
  -webkit-box-align: center;
  align-items: center;
  margin: 0 8px;
}
.detail-notes_note-created {
  display: flex;
  gap: 4px;
  line-height: 1.5;
  color: rgba(255, 255, 255, .5);
  font-size: 1.2rem;
}
.detail-notes__note-actions {
  position: relative;
}
</style>