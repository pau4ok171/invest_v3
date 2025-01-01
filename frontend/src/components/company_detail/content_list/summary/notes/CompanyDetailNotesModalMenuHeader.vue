<script lang="ts">
import {defineComponent} from 'vue'
import {mapGetters, mapMutations} from "vuex";
import BaseButton from "@/components/UI/base/components/BaseButton/BaseButton.vue";

export default defineComponent({
  name: "CompanyDetailNotesModalMenuHeader",
  components: {
    BaseButton,
  },
  computed: {
    ...mapGetters({
      notesModalIsLateral: "companyDetail/getNotesModalMenuIsLateral",
    }),
  },
  methods: {
    ...mapMutations({
      setNotesModalIsActive: 'companyDetail/setNotesModalMenuIsOpen',
      setNotesModalIsLateral: 'companyDetail/setNotesModalMenuIsLateral',

    })
  },
})
</script>

<template>
<header class="detail_notes_modal_menu_header">

  <div class="detail_notes_modal_menu_header__content-group">
    <base-button
      :icon="notesModalIsLateral ? {value: 'ExpandIcon', size: 'large'} : {value: 'ReduceIcon', size: 'large'}"
      rounded="x-small"
      variant="text"
      density="comfortable"
      @click="setNotesModalIsLateral(!notesModalIsLateral)"
    />
    <p class="detail_notes_modal_menu_header__title">MISC:SBER</p>
  </div>
  <div class="detail_notes_modal_menu_header__content-group">
    <base-button
      icon="NotificationIcon"
      rounded="x-small"
      variant="text"
      density="comfortable"
    />
    <base-button
      :icon="{value: 'ModalMenuCloseIcon', size: 'large'}"
      rounded="x-small"
      variant="text"
      density="comfortable"
      @click="setNotesModalIsActive(false)"
    />
  </div>

</header>
</template>

<style scoped>
.detail_notes_modal_menu_header {
  display: flex;
  justify-content: space-between;
  padding: 16px 8px 8px;
  border-bottom: none;
}
.detail_notes_modal_menu_header__content-group {
  display: flex;
  align-items: center;
}
.detail_notes_modal_menu_header__title {
  margin-left: 10px;
  font-size: 1.4rem;
}
</style>