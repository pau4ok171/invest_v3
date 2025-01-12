<script lang="ts">
import {defineComponent} from 'vue'
import BaseButton from "@/apps/visagiste/components/BaseButton/BaseButton.vue";
import {animate} from "@/apps/visagiste/utils/animation";
import type {PropType} from "vue";
import type {Theme} from "@/apps/visagiste/components/BaseTheme/baseTheme";

export default defineComponent({
  name: "BaseOverlay",
  data() {
    return {
      contentEl: {} as HTMLElement,
      scrollablePosY: 0,
    }
  },
  props: {
    isActive: {
      type: Boolean,
      required: true,
    },
    scrollable: {
      type: Boolean,
      required: true,
    },
    persistent: {
      type: Boolean,
      required: true,
    },
    theme: {
      type: String as PropType<Theme>,
      default: 'light',
    },
  },
  components: {
    BaseButton
  },
  computed: {
    overlayClassObject() {
      const classObj = []
      classObj.push(`base-overlay`)
      classObj.push(`base-theme--${this.theme}`)
      classObj.push(`base-overlay--role-dialog`)
      if (!this.scrollable) {
        classObj.push(`base-overlay--scroll-blocked`)
      }
      return classObj
    },
  },
  methods: {
    onClickOutside(e: MouseEvent) {
      if (this.isActive) {
        if (!this.persistent) {
          this.$emit('update:is-active', false)
        } else {
          this.animateClick()
        }
      }
    },
    onKeyDown(e: KeyboardEvent) {
      if (e.key === 'Escape' && this.isActive) {
        if (!this.persistent) {
          this.$emit('update:is-active', false)
        } else {
          this.animateClick()
        }
      }
    },
    animateClick() {
      this.$refs.contentEl && animate(this.$refs.contentEl as Element, [
        { transformOrigin: 'center' },
        { transform: 'scale(1.03)' },
        { transformOrigin: 'center' },
      ], {
        duration: 150,
        easing: 'cubic-bezier(.4, 0, .2, 1)'
      })
     },
    onBeforeEnter(el: Element) {
      const contentEl = el.querySelector('.base-overlay__content') as HTMLElement
      contentEl.style.pointerEvents = 'none';
      contentEl.style.visibility = 'hidden';
    },
    async onEnter(el: Element, done: () => void) {
      const contentEl = el.querySelector('.base-overlay__content') as HTMLElement
      await new Promise(resolve => requestAnimationFrame(resolve))

      contentEl.style.visibility = ''

      const animation = animate(contentEl, [
        { transform: `translate(0, 0) scale(.8, .8)`, opacity: 0 },
        {},
      ], {
        duration: 225,
        easing: 'cubic-bezier(0.0, 0, 0.2, 1)'
      })

      this.getChildren(contentEl)?.forEach(el => {
        animate(el, [
          { opacity: 0 },
          { opacity: 0, offset: 0.33 },
          {},
        ], {
          duration: 225 * 2,
          easing: 'cubic-bezier(0.4, 0, 0.2, 1)',
        })
      })

      animation.finished.then(() => done())
    },
    onAfterEnter(el: Element) {
      const contentEl = el.querySelector('.base-overlay__content') as HTMLElement
      contentEl.style.removeProperty('pointer-events')
    },
    onBeforeLeave(el: Element) {
      const contentEl = el.querySelector('.base-overlay__content') as HTMLElement
      contentEl.style.pointerEvents = 'none'
    },
    async onLeave(el: Element, done: () => void) {
      const contentEl = el.querySelector('.base-overlay__content') as HTMLElement
      await new Promise(resolve => requestAnimationFrame(resolve))

      const animation = animate(contentEl, [
        {},
        { transform: `translate(0, 0) scale(.8, .8)`, opacity: 0 },
      ], {
        duration: 125,
        easing: 'cubic-bezier(0.4, 0, 0.2, 1)',
      })

      animation.finished.then(() => done())

      this.getChildren(contentEl)?.forEach(el => {
        animate(el, [
          {},
          { opacity: 0, offset: .2 },
          { opacity: 0 },
        ], {
          duration: 125 * 2,
          easing: 'cubic-bezier(0.4, 0, 0.2, 1)',
        })
      })
    },
    onAfterLeave(el: Element) {
      const contentEl = el.querySelector('.base-overlay__content') as HTMLElement
      contentEl.style.removeProperty('pointer-events')
    },
    getChildren (el: Element) {
      const els = el.querySelector(':scope > .base-dialog')?.children
      return els && [...els]
    },
  },
  mounted() {
    document.addEventListener('keydown', this.onKeyDown)
  },
  activated() {
    console.log('contentEl ', this.$refs.contentEl)
  },
  beforeUnmount() {
    document.removeEventListener('keydown', this.onKeyDown)
  },
  watch: {
    isActive() {
      if (this.isActive) {
        if (!this.scrollable) {
          this.scrollablePosY = window.scrollY
          document.body.style.top = `-${this.scrollablePosY}px`
          document.body.classList.add('base-overlay--scroll-blocked')
        }
      } else {
        document.body.classList.remove('base-overlay--scroll-blocked')
        if (!this.scrollable) {
          document.body.style.removeProperty('top')
          window.scrollTo(0, this.scrollablePosY)
          this.scrollablePosY = 0
        }
      }
    }
  },
})
</script>

<template>
  <teleport to="body" :disabled="!isActive">
    <transition
      name="dialog-transition"
      :css=false
      @before-enter="onBeforeEnter"
      @enter="onEnter"
      @after-enter="onAfterEnter"
      @before-leave="onBeforeLeave"
      @leave="onLeave"
      @after-leave="onAfterLeave"
    >
      <template v-if="isActive">
        <div ref="overlayContainer" class="base-overlay-container">
          <div :class="overlayClassObject" aria-modal="true" role="dialog">
            <div ref="scrimEl" @click="onClickOutside" class="base-overlay__scrim"></div>
            <div ref="contentEl" class="base-overlay__content" tabindex="-1" style="width: auto;">
              <slot name="content"/>
            </div>
          </div>
        </div>
      </template>
    </transition>
  </teleport>
</template>

<style lang="scss" scoped>
@use 'styles';
</style>