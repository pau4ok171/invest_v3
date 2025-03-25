<script lang="ts">
// Styles
import './BaseToolbar.scss'

// Components
import BaseImage from '@/apps/visagiste/components/BaseImage/BaseImage.vue'
import BaseDefaultsProvider from '@/apps/visagiste/components/BaseDefaultsProvider/BaseDefaultsProvider.vue'
import { BaseExpandTransition } from '@/apps/visagiste/components/transitions'

// Composables
import { useBackgroundColor } from '@/apps/visagiste/composables/color'
import { provideDefaults } from '@/apps/visagiste/composables/defaults'
import { useBorder, useBorderProps } from '@/apps/visagiste/composables/border'
import { useSlotIsEmpty } from '@/apps/visagiste/composables/slotIsEmpty'
import {
  useElevation,
  useElevationProps,
} from '@/apps/visagiste/composables/elevation'
import {
  useRounded,
  useRoundedProps,
} from '@/apps/visagiste/composables/rounded'
import { provideTheme, useThemeProps } from '@/apps/visagiste/composables/theme'
import { useRtl } from '@/apps/visagiste/composables/locale'
import { useComponentProps } from '@/apps/visagiste/composables/component'
import { useTagProps } from '@/apps/visagiste/composables/tag'

// Utilities
import { computed, shallowRef, toRef } from 'vue'
import {
  convertToUnit,
  defineComponent,
  propsFactory,
} from '@/apps/visagiste/utils'

// Types
import type { PropType, SlotsType } from 'vue'

export type BaseToolbarSlots = {
  default: (props?: any) => void
  image: (props?: any) => void
  prepend: (props?: any) => void
  append: (props?: any) => void
  title: (props?: any) => void
  extension: (props?: any) => void
}

const allowedDensities = [
  null,
  'prominent',
  'default',
  'comfortable',
  'compact',
] as const
export type Density = null | 'prominent' | 'default' | 'comfortable' | 'compact'

export const useBaseToolbarProps = propsFactory(
  {
    absolute: Boolean,
    collapse: Boolean,
    color: String,
    density: {
      type: String as PropType<Density>,
      default: 'default',
      validator: (v: any) => allowedDensities.includes(v),
    },
    extended: Boolean,
    extensionHeight: {
      type: [Number, String],
      default: 48,
    },
    flat: Boolean,
    floating: Boolean,
    height: {
      type: [Number, String],
      default: 64,
    },
    image: String,
    title: String,

    ...useBorderProps(),
    ...useComponentProps(),
    ...useElevationProps(),
    ...useRoundedProps(),
    ...useTagProps({ tag: 'header' }),
    ...useThemeProps(),
  },
  'BaseToolbar'
)

export default defineComponent({
  name: 'BaseToolbar',
  computed: {
    BaseExpandTransition() {
      return BaseExpandTransition
    },
  },
  methods: {
    convertToUnit,
  },
  components: { BaseDefaultsProvider, BaseImage },
  props: useBaseToolbarProps(),
  slots: Object as SlotsType<BaseToolbarSlots>,
  setup(props, { slots }) {
    const { backgroundColorClasses, backgroundColorStyles } =
      useBackgroundColor(toRef(props, 'color'))
    const { borderClasses } = useBorder(props)
    const { elevationClasses } = useElevation(props)
    const { roundedClasses } = useRounded(props)
    const { themeClasses } = provideTheme(props)
    const { rtlClasses } = useRtl()

    const extensionIsEmpty = useSlotIsEmpty('extension')
    const isExtended = shallowRef((props.extended || !extensionIsEmpty.value))
    const contentHeight = computed(() =>
      parseInt(
        Number(props.height) +
          (props.density === 'prominent' ? Number(props.height) : 0) -
          (props.density === 'comfortable' ? 8 : 0) -
          (props.density === 'compact' ? 16 : 0),
        10
      )
    )
    const extensionHeight = computed(() =>
      isExtended.value
        ? parseInt(
            Number(props.extensionHeight) +
              (props.density === 'prominent'
                ? Number(props.extensionHeight)
                : 0) -
              (props.density === 'comfortable' ? 4 : 0) -
              (props.density === 'compact' ? 8 : 0),
            10
          )
        : 0
    )

    provideDefaults({
      BaseBtn: {
        variant: 'text',
      },
    })

    const titleIsEmpty = useSlotIsEmpty('title')
    const imageIsEmpty = useSlotIsEmpty('image')

    const hasTitle = computed(() => !!props.title || !titleIsEmpty.value)
    const hasImage = computed(() => !!props.image || !imageIsEmpty.value)
    const extension = computed(() => slots.extension?.())
    isExtended.value = computed(
      () => !!(props.extended || extension.value)
    ).value

    return {
      backgroundColorClasses,
      backgroundColorStyles,
      borderClasses,
      elevationClasses,
      roundedClasses,
      themeClasses,
      rtlClasses,
      contentHeight,
      extensionHeight,
      hasTitle,
      hasImage,
      extension,
      isExtended,
    }
  },
})
</script>

<template>
  <component
    :is="$props.tag as string"
    :class="[
      'base-toolbar',
      {
        'base-toolbar--absolute': $props.absolute,
        'base-toolbar--collapse': $props.collapse,
        'base-toolbar--flat': $props.flat,
        'base-toolbar--floating': $props.floating,
        [`base-toolbar--density-${$props.density}`]: true,
      },
      backgroundColorClasses,
      borderClasses,
      elevationClasses,
      roundedClasses,
      themeClasses,
      rtlClasses,
      $props.class,
    ]"
    :style="[backgroundColorStyles, $props.style]"
  >
    <template v-if="hasImage">
      <div key="image" class="base-toolbar__image">
        <BaseImage
          v-if="!$slots.image"
          key="image-image"
          cover
          :src="$props.image"
        />
        <BaseDefaultsProvider
          key="image-defaults"
          :disabled="!$props.image"
          :defaults="{
            BaseImage: {
              cover: true,
              src: $props.image,
            },
          }"
        >
          <slot name="image" />
        </BaseDefaultsProvider>
      </div>
    </template>

    <BaseDefaultsProvider
      :defaults="{
        BaseTabs: {
          height: convertToUnit(contentHeight),
        },
      }"
    >
      <div
        class="base-toolbar__content"
        :style="{ height: convertToUnit(contentHeight) }"
      >
        <template v-if="$slots.prepend">
          <div class="base-toolbar__prepend">
            <slot name="prepend" />
          </div>
        </template>

        <template v-if="hasTitle">
          <div class="base-toolbar-title">
            <div class="base-toolbar-title__placeholder">
              <slot name="title">{{ $props.title }}</slot>
            </div>
          </div>
        </template>

        <slot />

        <template v-if="$slots.append">
          <div class="base-toolbar__append">
            <slot name="append" />
          </div>
        </template>
      </div>
    </BaseDefaultsProvider>

    <BaseDefaultsProvider
      :defaults="{
        BaseTabs: {
          height: convertToUnit(extensionHeight),
        },
      }"
    >
      <component :is="BaseExpandTransition">
        <template v-if="isExtended">
          <div
            class="base-toolbar__extension"
            :style="{ height: convertToUnit(extensionHeight) }"
          >
            {{ extension }}
          </div>
        </template>
      </component>
    </BaseDefaultsProvider>
  </component>
</template>
