<script lang="ts">
import {defineComponent} from 'vue'
import CompanyDetailSection from "@/components/company_detail/CompanyDetailSection.vue";
import CompanyDetailContentGroup from "@/components/company_detail/CompanyDetailContentGroup.vue";
import BookIcon from "@/components/icons/BookIcon.vue";
import RoundedDarkBlueButton from "@/components/UI/buttons/RoundedDarkBlueButton.vue";
import PenIcon from "@/components/icons/PenIcon.vue";
import DetailSectionTitle from "@/components/UI/text/DetailSectionTitle.vue";
import DetailSectionText from "@/components/UI/text/DetailSectionText.vue";
import CompanyDetailNotesModalMenu from "@/components/company_detail/summary/notes/CompanyDetailNotesModalMenu.vue";
import {mapGetters, mapMutations, mapState} from "vuex";
import RoundedGreyButton from "@/components/UI/buttons/RoundedGreyButton.vue";
import DotsIcon from "@/components/icons/DotsIcon.vue";
import CompanyDetailNotesToolDropDownMenu
  from "@/components/company_detail/summary/notes/CompanyDetailNotesToolDropDownMenu.vue";
import CompanyDetailNotesNoteItem from "@/components/company_detail/summary/notes/CompanyDetailNotesNoteItem.vue";

export default defineComponent({
  name: "CompanyDetailNotes",
  components: {
    CompanyDetailNotesNoteItem,
    CompanyDetailNotesToolDropDownMenu,
    DotsIcon,
    RoundedGreyButton,
    CompanyDetailNotesModalMenu,
    DetailSectionText,
    DetailSectionTitle,
    PenIcon,
    RoundedDarkBlueButton,
    BookIcon,
    CompanyDetailContentGroup,
    CompanyDetailSection
  },
  computed: {
    ...mapGetters({
      notesModalMenuIsOpen: "companyDetail/getNotesModalMenuIsActive",
      notes: 'companyDetail/getNotes',
      note: "companyDetail/getNote",
    }),
    getNoteListClass() {
      return `detail-notes__note-list-${this.notes.slice(0, 3).length}-el`
    }
  },
  methods: {
    ...mapMutations({
      setNotesModalMenuIsOpen: "companyDetail/setNotesModalMenuIsOpen",
      setNote: "companyDetail/setNote",
    }),
  }
})
</script>

<template>
<CompanyDetailSection>
  <CompanyDetailContentGroup>

    <header class="detail-notes">
      <DetailSectionTitle>My Notes</DetailSectionTitle>
      <mark class="detail-notes__mark">{{ notes.length }}</mark>
    </header>

    <template v-if="notes.length">
      <div :class="['detail-notes__note-list', getNoteListClass]">
        <CompanyDetailNotesNoteItem
          v-for="note in notes.slice(0, 3)"
          :note
          :key="note.id"
        />
      </div>
      <RoundedDarkBlueButton :isFullWidth="true">See more</RoundedDarkBlueButton>
    </template>

    <div v-else class="detail-notes__empty">
      <BookIcon class="detail-notes__empty-image"/>
      <DetailSectionText>Capture your thoughts, links and company narrative</DetailSectionText>
      <RoundedDarkBlueButton @click="setNotesModalMenuIsOpen(true)">
        <PenIcon/>
        <span>Add note</span>
      </RoundedDarkBlueButton>
    </div>

  </CompanyDetailContentGroup>
</CompanyDetailSection>

<CompanyDetailNotesModalMenu v-if="notesModalMenuIsOpen"/>
</template>

<style scoped>
.detail-notes {
  display: grid;
  gap: 8px;
  grid-template-columns: auto auto 1fr;
  justify-content: start;
  align-items: center;
  margin-bottom: 8px;
}
.detail-notes__mark {
  font-size: 1.4rem;
  border-radius: 8px;
  background-color: #262e3a;
  margin: 0 4px 8px;
  padding: 2px 8px;
  color: inherit;
  white-space: nowrap;
}
.detail-notes__empty {
  display: grid;
  gap: 8px;
  grid-template-columns: repeat(1, 1fr);
  grid-template-rows: auto auto auto;
  justify-items: center;
  align-content: center;
  max-height: 164px;
  margin-bottom: 8px;
}
.detail-notes__empty-image {
  width: 64px;
  height: 66px;
  fill: none;
  transform: translateY(4px);
}
.detail-notes__note-list {
  display: grid;
  gap: 8px;
  grid-template-rows: auto;
  max-height: 164px;
  margin-bottom: 8px;
}
.detail-notes__note-list-1-el {
  grid-template-columns: repeat(1, 1fr);
}
.detail-notes__note-list-2-el {
  grid-template-columns: repeat(2, 1fr);
}
.detail-notes__note-list-3-el {
  grid-template-columns: repeat(3, 1fr);
}
</style>