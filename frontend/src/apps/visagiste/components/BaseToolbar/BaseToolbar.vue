<script lang="ts">
import './BaseToolbar.scss'

// Components
import BaseToolbarTitle from "./BaseToolbarTitle.vue";
import { BaseExpandTransition } from "@/apps/visagiste/components/transitions";

// Composables
import { borderProps, useBorder } from '@/apps/visagiste/composables/border'
import { useBackgroundColor } from "@/apps/visagiste/composables/color";
import { elevationProps, useElevation } from '@/apps/visagiste/composables/elevation'
import { roundedProps, useRounded } from '@/apps/visagiste/composables/rounded'
import { themeProps, provideTheme } from "@/apps/visagiste/composables/theme";

// Utilities
import {computed, shallowRef, toRef, defineComponent} from "vue";
import {convertToUnit} from "@/apps/visagiste/utils";

// Types
import type {PropType} from "vue";
const allowedDensities = [null, 'prominent', 'default', 'comfortable', 'compact'] as const

export type Density = null | 'prominent' |'default' | 'comfortable' | 'compact'

export default defineComponent({
  name: 'BaseToolbar',
  methods: {convertToUnit},
  components: {
    BaseExpandTransition,
    BaseToolbarTitle,
  },
  props: {
    absolute: Boolean,
    collapse: Boolean,
    color: String,
    density: {
      type: String as PropType<Density>,
      default: 'default',
      validator: (v: any) => allowedDensities.includes(v)
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
    ...borderProps,
    ...elevationProps,
    ...roundedProps,
    ...themeProps,
  },
  setup(props, { slots }) {
    const { backgroundColorClasses, backgroundColorStyles } = useBackgroundColor(toRef(props, 'color'))
    const { borderClasses } = useBorder(props)
    const { elevationClasses } = useElevation(props)
    const { roundedClasses } = useRounded(props)
    const { themeClasses } = provideTheme(props)

    const isExtended = shallowRef((props.extended || !!slots.extension))
    const contentHeight = computed(() => parseInt((
      Number(props.height) +
      (props.density === 'prominent' ? Number(props.height) : 0) -
      (props.density === 'comfortable' ? 8: 0) -
      (props.density === 'compact' ? 16: 0)
    ), 10))
    const extensionHeight = computed(() => isExtended.value
      ? parseInt((
        Number(props.extensionHeight) +
        (props.density === 'prominent' ? Number(props.extensionHeight) : 0) -
        (props.density === 'comfortable' ? 4 : 0) -
        (props.density === 'compact' ? 8 : 0)
        ), 10)
      : 0
    )
    const hasTitle = !!(props.title || slots.title)
    const hasImage = !!(props.image || slots.image)

    return {
      backgroundColorClasses,
      borderClasses,
      elevationClasses,
      roundedClasses,
      themeClasses,
      backgroundColorStyles,
      contentHeight,
      extensionHeight,
      hasTitle,
      hasImage,
      isExtended,
    }
  },
})
</script>

<template>
<header
  :class="[
    'base-toolbar',
    {
      'base-toolbar--absolute': absolute,
      'base-toolbar--collapse': collapse,
      'base-toolbar--flat': flat,
      'base-toolbar--floating': floating,
      [`base-toolbar--density-${density}`]: true,
    },
    backgroundColorClasses,
    borderClasses,
    elevationClasses,
    roundedClasses,
    themeClasses,
  ]"
  :style="[
    backgroundColorStyles,
  ]"
>
  <template v-if="hasImage">
    <div key="image" class="base-toolbar__image">
<!--      <base-image-->
<!--        key="image-image"-->
<!--        cover-->
<!--        :src="image"-->
<!--      />-->
    </div>
  </template>

  <div
    class="base-toolbar__content"
    :style="{height: convertToUnit(contentHeight)}"
  >
    <template v-if="$slots.prepend">
      <div class="base-toolbar__prepend">
        <slot name="prepend"/>
      </div>
    </template>

    <template v-if="hasTitle">
      <base-toolbar-title key="title" :text="title">
        <template #text>
          <slot name="title"/>
        </template>
      </base-toolbar-title>
    </template>

    <slot/>

    <template v-if="$slots.append">
      <div class="base-toolbar__append">
        <slot name="append"/>
      </div>
    </template>

  </div>

  <BaseExpandTransition>
    <template v-if="isExtended">
      <div class="base-toolbar__extension" :style="{height: convertToUnit(contentHeight)}">
        <slot name="extension"/>
      </div>
    </template>
  </BaseExpandTransition>
</header>
</template>
