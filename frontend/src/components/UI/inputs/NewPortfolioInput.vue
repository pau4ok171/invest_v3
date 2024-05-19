<script lang="ts">
import {defineComponent} from 'vue'
import BaseInput from "@/components/UI/base/BaseInput.vue";

export default defineComponent({
  name: "NewPortfolioInput",
  components: {BaseInput},
  props: ['modelValue', 'inputMode'],
  emits: ['update:modelValue', 'update:inputMode', 'createNewPortfolio'],
  mounted() {
    document.addEventListener('click', this.changeInputMode)
    document.addEventListener('keydown', this.changeInputMode)
    this.$el.select()
  },
  unmounted() {
    document.removeEventListener('click', this.changeInputMode)
    document.removeEventListener('keydown', this.changeInputMode)
  },
  methods: {
    changeInputMode(event: Event) {
      if (event.type === 'keydown' && event.code === 'Escape') {
        this.$emit('update:inputMode', false)
      }
      if (event.type === 'keydown' && event.code === 'Enter') {
        this.$emit('createNewPortfolio')
      }
      if (event.type === 'click' && event.target !== this.$el) {
        this.$emit('update:inputMode', false)
      }
    },
  },
})
</script>

<template>
<BaseInput
  :value="modelValue"
  @input="$emit('update:modelValue', $event.target.value)"
  class="detail-portfolio-modal-menu__input"
  placeholder="Например: Мой новый портфель"
/>
</template>

<style scoped>
.detail-portfolio-modal-menu__input {
    width: 100%;
    height: 40px;
    border: 1px solid rgba(38, 46, 58, .2);
    padding: 0 14px;
    appearance: none;
    outline: none;
    font-size: 1.4rem;
    font-weight: 500;
    border-radius: 4px;
    background-color: rgba(35, 148, 223, .05);
    caret-color: var(--blue);
    color: #000;
    transition: border .2s ease 0s, background-color .2s ease 0s;
}
</style>