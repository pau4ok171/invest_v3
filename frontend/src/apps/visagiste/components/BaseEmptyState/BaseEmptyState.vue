<script lang="ts">
// Styles
import './BaseEmptyState.scss'

// Components
import BaseImage from '@/apps/visagiste/components/BaseImage/BaseImage.vue'
import BaseIcon from '@/apps/visagiste/components/BaseIcon/BaseIcon.vue'
import BaseButton from '@/apps/visagiste/components/BaseButton/BaseButton.vue'

// Composables
import { IconValue } from '@/apps/visagiste/composables/icons'
import { useComponentProps } from '@/apps/visagiste/composables/component'
import {
  useDimension,
  useDimensionProps,
} from '@/apps/visagiste/composables/dimensions'
import { useSizeProps } from '@/apps/visagiste/composables/size'
import { provideTheme, useThemeProps } from '@/apps/visagiste/composables/theme'
import { useBackgroundColor } from '@/apps/visagiste/composables/color'
import { useDisplay } from '@/apps/visagiste/composables'
import { useSlotIsEmpty } from '@/apps/visagiste/composables/slotIsEmpty'

// Utilities
import { computed, toRef } from 'vue'
import {
  convertToUnit,
  defineComponent,
  propsFactory,
} from '@/apps/visagiste/utils'

// Types
import type { PropType } from 'vue'

export const useBaseEmptyStateProps = propsFactory(
  {
    actionText: String,
    bgColor: String,
    color: String,
    icon: IconValue,
    image: String,
    justify: {
      type: String as PropType<'start' | 'center' | 'end'>,
      default: 'center',
    },
    headline: String,
    title: String,
    text: String,
    textWidth: {
      type: [Number, String],
      default: 500,
    },
    href: String,
    to: String,

    ...useComponentProps(),
    ...useDimensionProps(),
    ...useSizeProps({ size: undefined }),
    ...useThemeProps(),
  },
  'BaseEmptyState'
)

export default defineComponent({
  name: 'BaseEmptyState',
  methods: { convertToUnit },
  components: { BaseButton, BaseIcon, BaseImage },
  props: useBaseEmptyStateProps(),
  emits: {
    'click:action': (e: Event) => true,
  },
  setup(props, { emit }) {
    const { themeClasses } = provideTheme(props)
    const { backgroundColorClasses, backgroundColorStyles } =
      useBackgroundColor(toRef(props, 'bgColor'))
    const { dimensionStyles } = useDimension(props)
    const { displayClasses } = useDisplay()

    function onClickAction(e: Event) {
      emit('click:action', e)
    }

    const actionsIsEmpty = useSlotIsEmpty('actions')
    const headlineIsEmpty = useSlotIsEmpty('headline')
    const titleIsEmpty = useSlotIsEmpty('title')
    const textIsEmpty = useSlotIsEmpty('text')
    const mediaIsEmpty = useSlotIsEmpty('media')

    const hasActions = computed(
      () => !actionsIsEmpty.value || !!props.actionText
    )
    const hasHeadline = computed(
      () => !headlineIsEmpty.value || !!props.headline
    )
    const hasTitle = computed(() => !titleIsEmpty.value || !!props.title)
    const hasText = computed(() => !textIsEmpty.value || !!props.text)
    const hasMedia = computed(
      () => !mediaIsEmpty.value || !!props.actionText || !!props.icon
    )
    const size = computed(() => props.size || (props.image ? 200 : 96))

    return {
      themeClasses,
      backgroundColorClasses,
      backgroundColorStyles,
      dimensionStyles,
      displayClasses,
      onClickAction,
      hasActions,
      hasHeadline,
      hasTitle,
      hasText,
      hasMedia,
      size,
    }
  },
})
</script>

<template>
  <div
    :class="[
      'base-empty-state',
      {
        [`base-empty-state--${$props.justify}`]: true,
      },
      themeClasses,
      backgroundColorClasses,
      displayClasses,
      $props.class,
    ]"
    :style="[backgroundColorStyles, dimensionStyles, $props.style]"
  >
    <template v-if="hasMedia">
      <div key="media" class="base-empty-state__media">
        <slot name="media">
          <BaseImage
            v-if="$props.image"
            key="image"
            :src="$props.image"
            :height="size"
          />
          <BaseIcon
            v-if="$props.icon"
            key="icon"
            :color="$props.color"
            :size="size"
            :icon="$props.icon"
          />
        </slot>
      </div>
    </template>

    <template v-if="hasHeadline">
      <div key="headline" class="base-empty-state__headline">
        <slot name="headline">{{ $props.headline }}</slot>
      </div>
    </template>

    <template v-if="hasTitle">
      <div key="title" class="base-empty-state__title">
        <slot name="title">{{ $props.title }}</slot>
      </div>
    </template>

    <template v-if="hasText">
      <div
        key="text"
        class="base-empty-state__text"
        :style="{ maxWidth: convertToUnit($props.textWidth) }"
      >
        <slot name="text">{{ $props.text }}</slot>
      </div>
    </template>

    <template v-if="$slots.default">
      <div key="content" class="base-empty-state__content">
        <slot />
      </div>
    </template>

    <template v-if="hasActions">
      <div key="actions" class="base-empty-state__actions">
        <slot name="actions" v-bind="{ props: { onClick: onClickAction } }">
          <BaseButton
            class="base-empty-state__action-btn"
            :color="$props.color ?? 'surface-variant'"
            :text="$props.actionText"
            @click="onClickAction"
          />
        </slot>
      </div>
    </template>
  </div>
</template>
