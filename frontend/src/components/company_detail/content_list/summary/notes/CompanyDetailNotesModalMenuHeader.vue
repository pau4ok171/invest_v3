<script lang="ts">
import {defineComponent} from 'vue'
import ExpandIcon from "@/components/icons/ExpandIcon.vue";
import RoundedButton from "@/components/UI/buttons/RoundedButton.vue";
import NotificationIcon from "@/components/icons/NotificationIcon.vue";
import ModalMenuCloseIcon from "@/components/icons/ModalMenuCloseIcon.vue";
import ReduceIcon from "@/components/icons/ReduceIcon.vue";
import {mapGetters, mapMutations} from "vuex";

export default defineComponent({
  name: "CompanyDetailNotesModalMenuHeader",
  components: {
    ReduceIcon,
    ModalMenuCloseIcon,
    NotificationIcon,
    RoundedButton,
    ExpandIcon,
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
    <RoundedButton @click="setNotesModalIsLateral(false)" v-if="notesModalIsLateral"><ExpandIcon/></RoundedButton>
    <RoundedButton @click="setNotesModalIsLateral(true)" v-else><ReduceIcon/></RoundedButton>
    <p class="detail_notes_modal_menu_header__title">MISC:SBER</p>
  </div>
  <div class="detail_notes_modal_menu_header__content-group">
    <RoundedButton><NotificationIcon style="width: 20px; height: 20px;"/></RoundedButton>
    <RoundedButton @click="setNotesModalIsActive(false)"><ModalMenuCloseIcon/></RoundedButton>
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