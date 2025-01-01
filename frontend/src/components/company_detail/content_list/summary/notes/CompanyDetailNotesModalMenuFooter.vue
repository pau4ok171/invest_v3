<script lang="ts">
import {defineComponent} from 'vue'
import {mapMutations} from "vuex";
import BaseButton from "@/components/UI/base/components/BaseButton/BaseButton.vue";

export default defineComponent({
  name: "CompanyDetailNotesModalMenuFooter",
  components: {
    BaseButton,
  },
  methods: {
    ...mapMutations({
      setNotesModalIsActive: 'companyDetail/setNotesModalMenuIsOpen'
    })
  },
  props: {
    editor: Object,
    saveStatus: String,
    usedVolume: Number,
    limitIsExceeded: Boolean,
  },
})
</script>

<template>
<footer class="detail_notes_model_menu_footer">

  <div v-if="editor" class="detail_notes_model_menu_footer__content_group">

    <base-button
      icon="HeaderIcon"
      variant="text"
      rounded="x-small"
      density="comfortable"
      @click="editor.chain().focus().toggleHeading({ level: 1 }).run()"
      :active="editor.isActive('heading', { level: 1 })"
    />

    <base-button
      icon="BoldIcon"
      variant="text"
      rounded="x-small"
      density="comfortable"
      @click="editor.chain().focus().toggleBold().run()"
      :active="editor.isActive('bold')"
      :disabled="!editor.can().chain().focus().toggleBold().run()"
    />

    <base-button
      icon="ListIcon"
      variant="text"
      rounded="x-small"
      density="comfortable"
      @click="editor.chain().focus().toggleBulletList().run()"
      :active="editor.isActive('bulletList')"
    />

  </div>

  <div class="detail_notes_model_menu_footer__content_group detail_notes_model_menu_footer__r-content_group">

    <div class="detail_notes_model_menu_footer__saving_state">{{ saveStatus }}</div>
    <div class="detail_notes_model_menu_footer__volume_state">
      <svg height="24" viewBox="0 0 20 20" width="24">
        <circle r="9" cx="50%" cy="50%" class="detail_notes_model_menu_footer__volume_state_total"></circle>
        <circle :stroke-dasharray="usedVolume"  r="9" cx="50%" cy="50%" class="detail_notes_model_menu_footer__volume_state_used" :class="{'detail_notes_model_menu_footer__volume_state_used--exceeded': limitIsExceeded}"></circle>
      </svg>
    </div>
    <base-button
      text="Close"
      theme="dark-blue"
      rounded="large"
      @click="setNotesModalIsActive(false)"
    />

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
    fill: none;
}
.detail_notes_model_menu_footer__volume_state_used {
    stroke: rgb(35, 148, 223);
    stroke-dashoffset: 56.248;
    transition: stroke-dashoffset 0.2s ease 0s, stroke 0.4s ease 0s;
    stroke-width: 2px;
    stroke-linecap: round;
    fill: none;
}
.detail_notes_model_menu_footer__volume_state_used--exceeded {
  stroke: #e64141;
}
</style>