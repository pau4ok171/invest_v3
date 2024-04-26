<script lang="ts">
import {defineComponent} from 'vue'
import RoundedButton from "@/components/UI/buttons/RoundedButton.vue";
import HeaderIcon from "@/components/icons/HeaderIcon.vue";
import BoldIcon from "@/components/icons/BoldIcon.vue";
import ListIcon from "@/components/icons/ListIcon.vue";
import RoundedDarkBlueButton from "@/components/UI/buttons/RoundedDarkBlueButton.vue";
import {mapMutations} from "vuex";

export default defineComponent({
  name: "CompanyDetailNotesModalMenuFooter",
  components: {RoundedDarkBlueButton, ListIcon, BoldIcon, HeaderIcon, RoundedButton},
  methods: {
    ...mapMutations({
      setNotesModalIsActive: 'companyDetail/setNotesModalMenuIsOpen'
    })
  },
  props: {
    editor: Object,
    saveStatus: String,
  },
})
</script>

<template>
<footer class="detail_notes_model_menu_footer">

  <div v-if="editor" class="detail_notes_model_menu_footer__content_group">

    <RoundedButton
      @click="editor.chain().focus().toggleHeading({ level: 1 }).run()" :class="{ 'is-active': editor.isActive('heading', { level: 1 }) }"
    >
      <HeaderIcon/>
    </RoundedButton>

    <RoundedButton
      @click="editor.chain().focus().toggleBold().run()" :disabled="!editor.can().chain().focus().toggleBold().run()" :class="{ 'is-active': editor.isActive('bold') }"
    >
      <BoldIcon/>
    </RoundedButton>

    <RoundedButton
      @click="editor.chain().focus().toggleBulletList().run()" :class="{ 'is-active': editor.isActive('bulletList') }"
    >
      <ListIcon/>
    </RoundedButton>

  </div>

  <div class="detail_notes_model_menu_footer__content_group detail_notes_model_menu_footer__r-content_group">

    <div class="detail_notes_model_menu_footer__saving_state">{{ saveStatus }}</div>
    <div class="detail_notes_model_menu_footer__volume_state">
      <svg height="24" viewBox="0 0 20 20" width="24">
        <circle class="detail_notes_model_menu_footer__volume_state_total"></circle>
        <circle class="detail_notes_model_menu_footer__volume_state_used"></circle>
      </svg>
    </div>
    <RoundedDarkBlueButton @click="setNotesModalIsActive(false)"><span>Close</span></RoundedDarkBlueButton>

  </div>

</footer>
</template>

<style scoped>
.detail_notes_model_menu_footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 0 24px;
    padding: 8px 0;
    border-top: 1px solid #494e57;
}
.detail_notes_model_menu_footer__content_group {
    display: flex;
    gap: 4px;
    align-items: center;
    justify-content: center;
}
.detail_notes_model_menu_footer__r-content_group {
  gap: 16px;
}
.detail_notes_model_menu_footer__saving_state {
    font-size: 1.2rem;
    line-height: 1.5;
    color: #8c929b;
}
.detail_notes_model_menu_footer__volume_state {
    transform: rotate(-90deg);
}
.detail_notes_model_menu_footer__volume_state_total {
    stroke: rgba(255, 255, 255, .1);
    stroke-width: 2px;
    stroke-linecap: round;
    r: 9;
    fill: none;
    cx: 50%;
    cy: 50%;
}
.detail_notes_model_menu_footer__volume_state_used {
    stroke: rgb(35, 148, 223);
    stroke-dashoffset: 56.248;
    stroke-dasharray: 56.2705;
    transition: stroke-dashoffset 0.2s ease 0s, stroke 0.4s ease 0s;
    stroke-width: 2px;
    stroke-linecap: round;
    r: 9;
    fill: none;
    cx: 50%;
    cy: 50%;
}
</style>