<script lang="ts">
import {defineComponent} from 'vue'
import type {PropType} from 'vue'
// @ts-ignore
import {AtomSpinner} from "epic-spinners";
import BaseIcon from "@/components/UI/base/BaseIcon/BaseIcon.vue";
import type {IBaseIcon, IconValue} from "@/components/UI/base/BaseIcon/baseIcon";
import type {Density, Elevation, Rounded, Size, Variant} from "@/components/UI/base/BaseButton/baseButton";
import type {Theme} from "@/components/UI/base/BaseTheme/baseTheme";

export default defineComponent({
  name: "BaseButton",
  components: {
    BaseIcon,
    AtomSpinner,
  },
  props: {
    variant: {
      type: String as PropType<Variant>,
      default: 'elevated',
    },
    text: {
      type: String,
      default: 'Button'
    },
    icon: {
      type: [String, Object] as PropType<IconValue | IBaseIcon>,
    },
    appendIcon: {
      type: [String, Object] as PropType<IconValue | IBaseIcon>,
    },
    prependIcon: {
      type: [String, Object] as PropType<IconValue | IBaseIcon>,
    },
    stacked: Boolean,
    density: {
      type: String as PropType<Density>,
      default: 'default',
    },
    disabled: {
      type: Boolean,
      default: false,
    },
    size: {
      type: String as PropType<Size>,
      default: 'default',
    },
    block: {
      type: Boolean,
      default: false,
    },
    rounded: {
      type: String as PropType<Rounded>,
      default: 'default',
    },
    elevation: {
      type: String as PropType<Elevation>,
      default: '2',
    },
    ripple: {
      type: Boolean,
      default: true,
    },
    loading: {
      type: Boolean,
      default: false,
    },
    theme: {
      type: String as PropType<Theme>,
      default: 'light',
    },
    color: {
      type: String,
    },
    lower: {
      type: Boolean,
      default: false,
    },
    active: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    classObject() {
      const classObj = []
      classObj.push(`base-theme--${this.theme}`)

      classObj.push('base-button')

      classObj.push(`base-button--variant-${this.variant}`)
      classObj.push(`base-button--density-${this.density}`)
      classObj.push(`base-button--size-${this.size}`)
      classObj.push(`base-button--rounded-${this.rounded}`)
      if (!!this.icon) {
        classObj.push('base-button--icon')
      }
      if (!this.icon && this.stacked) {
        classObj.push('base-button--stacked')
      }
      if (this.disabled) {
        classObj.push('base-button--disabled')
      }
      if (this.variant === 'elevated') {
        classObj.push(`base-button--elevation-${this.elevation}`)
      }
      if (this.block) {
        classObj.push('base-button--block')
      }
      if (this.loading) {
        classObj.push('base-button--loading')
      }
      if (this.color) {
        classObj.push('base-button--color')
      }
      if (this.lower) {
        classObj.push('base-button--lower')
      }
      if (this.active) {
        classObj.push('base-button--active')
      }
      return classObj
    }
  },
})
</script>

<template>
<button v-ripple="ripple" :class="classObject" :disabled="loading || disabled">
  <span class="base-button__overlay"></span>
  <span class="base-button__underlay"></span>
  <template v-if="icon">
    <span class="base-button__icon" v-if="icon"><BaseIcon :icon="icon"/></span>
  </template>

  <template v-else>
    <span class="base-button__prepend" v-if="prependIcon"><BaseIcon :icon="prependIcon"/></span>
    <span class="base-button__text">{{ text }}</span>
    <span class="base-button__append" v-if="appendIcon"><BaseIcon :icon="appendIcon"/></span>
  </template>
  <span v-if="loading" class="base-button__loader"><atom-spinner color="inherit" :animation-duration="1250"/></span>
</button>
</template>

<style lang="scss" scoped>
@use  '@/components/UI/base/BaseTheme/themes';
@use '@/components/UI/base/BaseButton/size';
@use '@/components/UI/base/BaseButton/density';
@use '@/components/UI/base/BaseButton/variant';
@use '@/components/UI/base/BaseButton/rounded';
@use '@/components/UI/base/BaseButton/elevation';
/* BASE BUTTON */
.base-button {
  /* Position */
  position: relative;
  display: inline-grid;
  align-items: center;
  justify-content: center;
  vertical-align: middle;
  flex-shrink: 0;
  grid-template-areas: "prepend text append";
  grid-template-columns: max-content auto max-content;
  margin: 0;
  /* Geometry */
  max-width: 100%;
  /* Styling */
  outline: none;
  font-weight: 500;
  text-indent: .0892857143em;
  text-transform: uppercase;
  text-decoration: none;
  letter-spacing: .0892857143em;
  transition: background-color .2s ease 0s;
  transition-property: box-shadow, transform, opacity, background;
  transition-duration: .28s;
  transition-timing-function: cubic-bezier(.4,0,.2,1);
  border-color: rgba(var(--base-border-color), var(--base-border-opacity));
  border-style: solid;
  border-width: 0;
  /* Options */
  user-select: none;
  cursor: pointer;
  overflow: visible;
  &.base-button--icon {
    border-radius: 50%;
    min-width: 0;
    padding: 0;
    height: calc(var(--base-button-height) + 12px);
    width: calc(var(--base-button-height) + 12px);
    & .base-icon--size {
      &-x-large{
      --base-icon-size-multiplier: 1.5;
      }
      &-large {
        --base-icon-size-multiplier: 1.2;
      }
      &-default {
        --base-icon-size-multiplier: 1;
      }
      &-small {
        --base-icon-size-multiplier: 0.8;
      }
      &-x-small {
        --base-icon-size-multiplier: 0.5;
      }
    }
  }
  &.base-button--icon.base-button--density-comfortable {
    height: calc(var(--base-button-height) + 0px);
    width: calc(var(--base-button-height) + 0px);
  }
  &.base-button--icon.base-button--density-compact {
    height: calc(var(--base-button-height) + -8px);
    width: calc(var(--base-button-height) + -8px);
  }
  &:hover > .base-button__overlay {
    opacity: 0.04;
  }
  &:focus-visible > .base-button__overlay {
    opacity: var(--base-focus-opacity);
  }
  &.base-button--disabled {
    pointer-events: none;
    opacity: .26;
    &.base-button--variant-elevated,
    &.base-button--variant-flat {
      box-shadow: none;
      opacity: 1;
      color: rgba(var(--base-theme-on-surface), .26);
      background: rgb(var(--base-theme-surface));
      & .base-button__overlay {
        opacity: 0.4615384615;
      }
    }
  }
  &.base-button--block {
    display: flex;
    flex: 1 0 auto;
    min-width: 100%;
  }
  &.base-button--color {
    color: v-bind(color);
  }
  &.base-button--lower {
    letter-spacing: normal;
    text-transform: none;
    font-weight: normal;
    text-indent: inherit;
  }
}
@supports selector(:focus-visible) {
  .base-button:focus-visible::after {
    opacity: .25;
  }
}
@supports selector(:focus-visible) {
  .base-button::after {
    position: absolute;
    content: "";
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-repeat: no-repeat;
    box-sizing: inherit;
  }
}
@supports selector(:focus-visible) {
  .base-button::after {
    pointer-events: none;
    border: 2px solid currentColor;
    border-radius: inherit;
    opacity: 0;
    transition: opacity .2s ease-in-out;
  }
}
.base-button--stacked {
  white-space: normal;
  grid-template-areas: "prepend" "text" "append";
  grid-template-columns: auto;
  grid-template-rows: max-content max-content max-content;
  justify-items: center;
  align-content: center;
  & .base-button__text {
    flex-direction: column;
    line-height: 1.25;
  }
  &.base-button--block {
    display: inline-grid;
  }
}
.base-button--stacked .base-button__append {
  margin-top: 4px;
}
.base-button--stacked .base-button__prepend,
.base-button--stacked .base-button__append {
  margin-inline: 0;
}
.base-button--stacked .base-icon {
  --base-button-size-multiplier: 1.1428571429;
}
.base-button__overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  background-color: currentColor;
  border-radius: inherit;
  opacity: 0;
  transition: opacity .2s ease-in-out;
}
.base-button__underlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}
.base-button__prepend, .base-button__text, .base-button__append {
  align-items: center;
  display: flex;
  transition: transform, opacity .2s cubic-bezier(.4, 0, .2, 1);
  pointer-events: none;
}
.base-button__icon {
  pointer-events: none;
}
.base-button__prepend {
  grid-area: prepend;
  margin-inline: calc(var(--base-button-height) / -9) calc(var(--base-button-height) / 4.5);
}
.base-button__text {
  grid-area: text;
  justify-content: center;
  white-space: nowrap;
}
.base-button__append {
  grid-area: append;
  margin-inline: calc(var(--base-button-height) / 4.5) calc(var(--base-button-height) / -9);
}
.base-button.base-button--loading {
  & {
    pointer-events: none;
  }
  & > .base-button__text,
  & > .base-button__icon,
  & > .base-button__prepend,
  & > .base-button__append {
    opacity: 0;
  }
}
.base-button__loader {
  display: flex;
  position: absolute;
  height: 100%;
  width: 100%;
  justify-content: center;
  align-items: center;
  left: 0;
  top: 0;
  & > .atom-spinner {
    width: 1.5em!important;
    height: 1.5em!important;
  }
}
</style>