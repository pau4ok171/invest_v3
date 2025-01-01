<script lang="ts">
import type {PropType} from 'vue';
import {defineComponent} from 'vue';
import BaseButton from "@/components/UI/base/components/BaseButton/BaseButton.vue";
import type {Theme} from "@/components/UI/base/components/BaseTheme/baseTheme";
import type {FooterType, HeaderType} from "@/components/UI/base/components/BaseDialog/baseDialog";
import BaseOverlay from "@/components/UI/base/components/BaseOverlay/BaseOverlay.vue";

export default defineComponent({
  name: "BaseDialog",
  components: {
    BaseOverlay,
    BaseButton,
  },
  data() {
    return {
      isActive: false,
    }
  },
  props: {
    title: {
      type: String,
      default: '',
    },
    maxWidth: {
      type: String,
      default: '',
    },
    theme: {
      type: String as PropType<Theme>,
      default: 'light',
    },
    elevated: {
      type: Boolean,
      default: true
    },
    scrollable: {
      type: Boolean,
      default: false,
    },
    persistent: {
      type: Boolean,
      default: false,
    },
    headerType: {
      type: String as PropType<HeaderType>,
      default: 'default',
    },
    footerType: {
      type: String as PropType<FooterType>,
      default: 'withClose'
    },
  },
  computed: {
    dialogClassObject() {
      const classObj = []
      classObj.push(`base-dialog`)
      classObj.push(`base-theme--${this.theme}`)

      if (this.elevated) {
        classObj.push(`base-dialog--elevated`)
      }
      return classObj
    },
    dialogStyleObject() {
      const styleObj: Record<string, string> = {}
      if (this.maxWidth) {
        styleObj['--base-dialog-max-width'] = this.maxWidth.endsWith('px') ? this.maxWidth : `${this.maxWidth}px`
      }
      return styleObj
    },
  },
  methods: {
    processButtonClick(buttonName: string, close: boolean = true) {
      this.$emit(`click:${buttonName}`)
      if (close) {
        this.isActive = false
      }
    },
  },
})
</script>

<template>
<div>
  <div @click="isActive=!isActive">
    <slot name="activator"/>
  </div>

  <base-overlay
    v-model:is-active="isActive"
    :scrollable="scrollable"
    :persistent="persistent"
    :theme="theme"
  >
    <template #content>
      <div :style="dialogStyleObject" :class="dialogClassObject">
        <header v-if="headerType !== 'withoutHeader'" class="base-dialog__header">
          <h1 class="base-dialog__title">{{ title }}</h1>
          <base-button
            v-if="headerType !== 'withoutCloseButton'"
            icon="ModalMenuCloseIcon"
            variant="text"
            color="#92969c"
            rounded="x-small"
            density="comfortable"
            theme="grey"
            @click="isActive=false"
          />
        </header>
        <main class="base-dialog__main">
          <slot name="dialog"/>
        </main>
        <footer v-if="footerType !== 'withoutFooter'" class="base-dialog__footer">
          <base-button v-if="footerType === 'withOk'" @click.stop="processButtonClick('ok')" text="Ok" variant="text"/>
          <base-button v-if="footerType === 'withClose'" @click.stop="processButtonClick('close')" text="Close" variant="text"/>
          <template v-if="footerType === 'withYesNo'">
            <base-button @click.stop="processButtonClick('yes')" theme="success" text="Yes" variant="flat"/>
            <base-button @click.stop="processButtonClick('no')" theme="error" text="No" variant="flat"/>
          </template>
          <template v-if="footerType === 'withYesNoCancel'">
            <base-button @click.stop="processButtonClick('yes')" text="Yes" variant="text"/>
            <base-button @click.stop="processButtonClick('no')" text="No" variant="text"/>
            <base-button @click.stop="processButtonClick('cancel')" text="Cancel" variant="text"/>
          </template>
        </footer>
      </div>
    </template>
  </base-overlay>
</div>
</template>

<style lang="scss" scoped>
@use 'styles';
</style>