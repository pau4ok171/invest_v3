<script lang="ts">
import {defineComponent} from 'vue'
import BaseLateralMenu from "@/components/UI/lateral_menu/BaseLateralMenu.vue";
import CompanyDetailNotesNoteItem
  from "@/components/company_detail/content_list/summary/notes/CompanyDetailNotesNoteItem.vue";
import {mapGetters} from "vuex";

export default defineComponent({
  name: "CompanyDetailNotesLateralMenu",
  components: {CompanyDetailNotesNoteItem, BaseLateralMenu},
  computed: {
    ...mapGetters({
      notes: 'companyDetail/getNotes',
    }),
  },
})
</script>

<template>
<BaseLateralMenu>
  <template #title>
    Notes
  </template>
  <template #content>
    <div class="base-lateral-menu-content">
      <CompanyDetailNotesNoteItem
        v-for="note in notes.slice(0, 3)"
        :note
        :key="note.id"
      />
    </div>

  </template>
</BaseLateralMenu>
</template>

<style scoped>
.base-lateral-menu-content {
  display: grid;
  gap: 8px;
}
</style>