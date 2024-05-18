<script lang="ts">
import {defineComponent} from 'vue'
import EditIcon from "@/components/icons/EditIcon.vue";
import DeleteIcon from "@/components/icons/DeleteIcon.vue";

export default defineComponent({
  name: "CompanyDetailNotesToolDropDownMenu",
  components: {DeleteIcon, EditIcon},
  methods: {
    closeDropDownMenu(event: Event) {
      const target = event.target as HTMLInputElement
      if (target.parentNode !== this.$el.parentNode) {
        this.$emit('closeDropDownMenu')
      }
    }
  },
  mounted() {
    document.addEventListener('click', this.closeDropDownMenu)
  },
  unmounted() {
    document.removeEventListener('click', this.closeDropDownMenu)
  },
})
</script>

<template>
<div class="detail-notes-tool-drop-down-menu">
  <button @click="$emit('editNote')" class="detail-notes-tool-drop-down-menu__button">
    <EditIcon/>
    Edit
  </button>
  <button @click="$emit('deleteNote')" class="detail-notes-tool-drop-down-menu__button">
    <DeleteIcon/>
    Delete
  </button>
</div>
</template>

<style scoped>
.detail-notes-tool-drop-down-menu {
  position: absolute;
  z-index: 1;
  top: 30px;
  right: 10px;
  background: white;
  border-radius: 4px;
  display: inline-block;
  width: auto;
  box-shadow: 0 0 10px 10px rgba(0, 0, 0, .2);
}
.detail-notes-tool-drop-down-menu__button {
  line-height: 1.5;
  color: rgb(0, 0, 0);
  display: flex;
  cursor: pointer;
  width: 100%;
  transition: background 0.2s cubic-bezier(.23, 1, .32, 1) 0s;
  padding: 8px 16px;
  font-size: 1.4rem;
}
.detail-notes-tool-drop-down-menu__button:first-child {
  border-top-left-radius: 3px;
  border-top-right-radius: 3px;
}
.detail-notes-tool-drop-down-menu__button:last-child {
  border-bottom-left-radius: 3px;
  border-bottom-right-radius: 3px;
}
.detail-notes-tool-drop-down-menu__button:hover {
  background-color: var(--blue-hover);
}
.detail-notes-tool-drop-down-menu__button svg {
  fill: #000;
  opacity: .5;
  width: 20px;
  height: 20px;
}
</style>