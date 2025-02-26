<script lang="ts">
// Components
import { default as BaseCardSubtitle } from './BaseCardSubtitle.vue'
import { default as BaseCardTitle } from './BaseCardTitle.vue'
import { BaseAvatar } from '@/apps/visagiste/components/BaseAvatar'
import { BaseDefaultsProvider } from '@/apps/visagiste/components/BaseDefaultsProvider'
import { BaseIcon } from '@/apps/visagiste/components/BaseIcon'

// Composables
import { useComponentProps } from '@/apps/visagiste/composables/component'
import { useDensityProps } from '@/apps/visagiste/composables/density'
import { IconValue } from '@/apps/visagiste/composables/icons'

// Utilities
import type { SlotsType } from 'vue'
import { defineComponent, propsFactory } from '@/apps/visagiste/utils'
import { computed } from 'vue'

export type BaseCardItemSlots = {
  default: never
  prepend: never
  append: never
  title: never
  subtitle: never
}

export const useCardItemProps = propsFactory(
  {
    appendAvatar: String,
    appendIcon: IconValue,
    prependAvatar: String,
    prependIcon: IconValue,
    subtitle: [String, Number],
    title: [String, Number],

    ...useComponentProps(),
    ...useDensityProps(),
  },
  'BaseCardItem'
)

export default defineComponent({
  name: 'BaseCardItem',
  components: {
    BaseCardSubtitle,
    BaseCardTitle,
    BaseDefaultsProvider,
    BaseIcon,
    BaseAvatar,
  },
  props: useCardItemProps(),
  slots: Object as SlotsType<BaseCardItemSlots>,
  setup(props, { slots }) {
    const hasPrependMedia = computed(
      () => !!(props.prependAvatar || props.prependIcon)
    )
    const hasPrepend = computed(() => hasPrependMedia.value || slots.prepend)
    const hasAppendMedia = computed(
      () => !!(props.appendAvatar || props.appendIcon)
    )
    const hasAppend = computed(() => hasAppendMedia.value || slots.append)
    const hasTitle = computed(() => props.title != null || slots.title)
    const hasSubtitle = computed(() => props.subtitle != null || slots.subtitle)

    return {
      hasPrependMedia,
      hasPrepend,
      hasAppendMedia,
      hasAppend,
      hasTitle,
      hasSubtitle,
    }
  },
})
</script>

<template>
  <div :class="['base-card-item', $props.class]" :style="$props.style">
    <template v-if="hasPrepend">
      <div key="prepend" class="base-card-item__prepend">
        <template v-if="!$slots.prepend">
          <base-avatar
            v-if="$props.prependAvatar"
            key="prepend-avatar"
            :density="$props.density"
            :image="$props.prependAvatar"
          />
          <base-icon
            v-if="$props.prependIcon"
            key="prepend-icon"
            :density="$props.density"
            :icon="$props.prependIcon"
          />
        </template>
        <template v-else>
          <BaseDefaultsProvider
            key="prepend-defaults"
            :disabled="!hasPrependMedia"
            :defaults="{
              BaseAvatar: {
                density: $props.density,
                image: $props.prependAvatar,
              },
              BaseIcon: {
                density: $props.density,
                icon: $props.prependIcon,
              },
            }"
          >
            <slot name="prepend" />
          </BaseDefaultsProvider>
        </template>
      </div>
    </template>

    <div class="base-card-item__content">
      <BaseCardTitle v-if="hasTitle" key="title">
        <slot name="title">{{ $props.title }}</slot>
      </BaseCardTitle>

      <BaseCardSubtitle v-if="hasSubtitle" key="subtitle">
        <slot name="subtitle">{{ $props.subtitle }}</slot>
      </BaseCardSubtitle>
    </div>

    <slot name="default" />

    <template v-if="hasAppend">
      <div key="append" class="base-card-item__append">
        <template v-if="!$slots.append">
          <base-avatar
            v-if="$props.appendAvatar"
            key="append-avatar"
            :density="$props.density"
            :image="$props.appendAvatar"
          />
          <base-icon
            v-if="$props.appendIcon"
            key="append-icon"
            :density="$props.density"
            :icon="$props.appendIcon"
          />
        </template>
        <template v-else>
          <BaseDefaultsProvider
            key="prepend-defaults"
            :disabled="!hasAppendMedia"
            :defaults="{
              BaseAvatar: {
                density: $props.density,
                image: $props.appendAvatar,
              },
              BaseIcon: {
                density: $props.density,
                icon: $props.appendIcon,
              },
            }"
          >
            <slot name="append" />
          </BaseDefaultsProvider>
        </template>
      </div>
    </template>
  </div>
</template>
