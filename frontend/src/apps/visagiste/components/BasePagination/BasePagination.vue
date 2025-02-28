<script lang="ts">
// Styles
import './BasePagination.scss'

// Components
import BaseButton from '@/apps/visagiste/components/BaseButton/BaseButton.vue'

// Composables
import { useRefs } from '@/apps/visagiste/composables/refs'
import { IconValue } from '@/apps/visagiste/composables/icons'
import { useBorderProps } from '@/apps/visagiste/composables/border'
import { useComponentProps } from '@/apps/visagiste/composables/component'
import { useDensityProps } from '@/apps/visagiste/composables/density'
import { useElevationProps } from '@/apps/visagiste/composables/elevation'
import { useRoundedProps } from '@/apps/visagiste/composables/rounded'
import { useSizeProps } from '@/apps/visagiste/composables/size'
import { useTagProps } from '@/apps/visagiste/composables/tag'
import { provideTheme, useThemeProps } from '@/apps/visagiste/composables/theme'
import { useVariantProps } from '@/apps/visagiste/composables/variant'
import { useProxiedModel } from '@/apps/visagiste/composables/proxiedModel'
import { provideDefaults } from '@/apps/visagiste/composables/defaults'
import { useResizeObserver } from '@/apps/visagiste/composables/resizeObserver'

// Utilities
import {
  createRange,
  defineComponent,
  keyValues,
  propsFactory,
} from '@/apps/visagiste/utils'
import { useDisplay, useLocale, useRtl } from '@/apps/visagiste/composables'
import { computed, nextTick, shallowRef, toRef } from 'vue'

// Types
import type { ComponentPublicInstance } from 'vue'

type ItemSlot = {
  isActive: boolean
  key: string | number
  page: string
  props: Record<string, any>
}

type ControlSlot = {
  icon: IconValue
  onClick: (e: Event) => void
  disabled: boolean
  'aria-label': string
  'aria-disabled': boolean
}

export type BasePaginationSlots = {
  item: ItemSlot
  first: ControlSlot
  prev: ControlSlot
  next: ControlSlot
  last: ControlSlot
}

export const useBasePaginationProps = propsFactory(
  {
    activeColor: String,
    start: {
      type: [Number, String],
      default: 1,
    },
    modelValue: {
      type: Number,
      default: (props: any) => props.start as number,
    },
    disabled: Boolean,
    length: {
      type: [Number, String],
      default: 1,
      validation: (val: number) => val % 1 === 0,
    },
    totalVisible: [Number, String],
    firstIcon: {
      type: IconValue,
      default: '$first',
    },
    prevIcon: {
      type: IconValue,
      default: '$prev',
    },
    nextIcon: {
      type: IconValue,
      default: '$next',
    },
    lastIcon: {
      type: IconValue,
      default: '$last',
    },
    ariaLabel: {
      type: String,
      default: '$visagiste.pagination.ariaLabel.root',
    },
    pageAriaLabel: {
      type: String,
      default: '$visagiste.pagination.ariaLabel.page',
    },
    currentPageAriaLabel: {
      type: String,
      default: '$visagiste.pagination.ariaLabel.currentPage',
    },
    firstAriaLabel: {
      type: String,
      default: '$visagiste.pagination.ariaLabel.first',
    },
    previousAriaLabel: {
      type: String,
      default: '$visagiste.pagination.ariaLabel.previous',
    },
    nextAriaLabel: {
      type: String,
      default: '$visagiste.pagination.ariaLabel.next',
    },
    lastAriaLabel: {
      type: String,
      default: '$visagiste.pagination.ariaLabel.last',
    },
    ellipsis: {
      type: String,
      default: '...',
    },
    showFirstLastPage: Boolean,

    ...useBorderProps(),
    ...useComponentProps(),
    ...useDensityProps(),
    ...useElevationProps(),
    ...useRoundedProps(),
    ...useSizeProps(),
    ...useTagProps({ tag: 'nav' }),
    ...useThemeProps(),
    ...useVariantProps({ variant: 'text' } as const),
  },
  'BasePagination'
)

export default defineComponent({
  name: 'BasePagination',
  components: { BaseButton },
  props: useBasePaginationProps(),
  emits: {
    'update:modelValue': (value: number) => true,
    first: (value: number) => true,
    prev: (value: number) => true,
    next: (value: number) => true,
    last: (value: number) => true,
  },
  setup(props, { emit }) {
    const page = useProxiedModel(props, 'modelValue')
    const { t, n } = useLocale()
    const { isRtl } = useRtl()
    const { themeClasses } = provideTheme(props)
    const { width } = useDisplay()
    const maxButtons = shallowRef(-1)

    provideDefaults(undefined, { scoped: true })

    const { resizeRef } = useResizeObserver(
      (entries: ResizeObserverEntry[]) => {
        if (!entries.length) return

        const { target, contentRect } = entries[0]

        const firstItem = target.querySelector(
          '.base-pagination__list > *'
        ) as HTMLElement

        if (!firstItem) return

        const totalWidth = contentRect.width
        const itemWidth =
          firstItem.offsetWidth +
          parseFloat(getComputedStyle(firstItem).marginRight) * 2

        maxButtons.value = getMax(totalWidth, itemWidth)
      }
    )

    const length = computed(() => parseInt(props.length, 10))
    const start = computed(() => parseInt(props.start, 10))

    const totalVisible = computed(() => {
      if (props.totalVisible != null) return parseInt(props.totalVisible, 10)
      else if (maxButtons.value >= 0) return maxButtons.value
      return getMax(width.value, 58)
    })

    function getMax(totalWidth: number, itemWidth: number) {
      const minButtons = props.showFirstLastPage ? 5 : 3
      return Math.max(
        0,
        Math.floor(
          // Round to two decimal places to avoid floating point errors
          +((totalWidth - itemWidth * minButtons) / itemWidth).toFixed(2)
        )
      )
    }

    const range = computed(() => {
      if (
        length.value <= 0 ||
        isNaN(length.value) ||
        length.value > Number.MAX_SAFE_INTEGER
      )
        return []

      if (totalVisible.value <= 0) return []
      else if (totalVisible.value === 1) return [page.value]

      if (length.value <= totalVisible.value) {
        return createRange(length.value, start.value)
      }

      const even = totalVisible.value % 2 === 0
      const middle = even
        ? totalVisible.value / 2
        : Math.floor(totalVisible.value / 2)
      const left = even ? middle : middle + 1
      const right = length.value - middle

      if (left - page.value >= 0) {
        return [
          ...createRange(Math.max(1, totalVisible.value - 1), start.value),
          props.ellipsis,
          length.value,
        ]
      } else if (page.value - right >= (even ? 1 : 0)) {
        const rangeLength = totalVisible.value - 1
        const rangeStart = length.value - rangeLength + start.value
        return [
          start.value,
          props.ellipsis,
          ...createRange(rangeLength, rangeStart),
        ]
      } else {
        const rangeLength = Math.max(1, totalVisible.value - 2)
        const rangeStart =
          rangeLength === 1
            ? page.value
            : page.value - Math.ceil(rangeLength / 2) + start.value
        return [
          start.value,
          props.ellipsis,
          ...createRange(rangeLength, rangeStart),
          props.ellipsis,
          length.value,
        ]
      }
    })

    // TODO: 'first' | 'prev' | 'next' | 'last' does not work here?
    function setValue(e: Event, value: number, event?: any) {
      e.preventDefault()
      page.value = value
      event && emit(event, value)
    }

    const { refs, updateRef } = useRefs<ComponentPublicInstance>()

    provideDefaults({
      BasePaginationBtn: {
        color: toRef(props, 'color'),
        border: toRef(props, 'border'),
        density: toRef(props, 'density'),
        size: toRef(props, 'size'),
        variant: toRef(props, 'variant'),
        rounded: toRef(props, 'rounded'),
        elevation: toRef(props, 'elevation'),
      },
    })

    const items = computed(() => {
      return range.value.map((item, index) => {
        const ref = (e: any) => updateRef(e, index)

        if (typeof item === 'string') {
          return {
            isActive: false,
            key: `ellipsis-${index}`,
            page: item,
            props: {
              ref,
              ellipsis: true,
              icon: true,
              disabled: true,
            },
          }
        } else {
          const isActive = item === page.value
          return {
            isActive,
            key: item,
            page: n(item),
            props: {
              ref,
              ellipsis: false,
              icon: true,
              disabled: !!props.disabled || +props.length < 2,
              color: isActive ? props.activeColor : props.color,
              'aria-current': isActive,
              'aria-label': t(
                isActive ? props.currentPageAriaLabel : props.pageAriaLabel,
                item
              ),
              onClick: (e: Event) => setValue(e, item),
            },
          }
        }
      })
    })

    const controls = computed(() => {
      const prevDisabled = !!props.disabled || page.value <= start.value
      const nextDisabled =
        !!props.disabled || page.value >= start.value + length.value - 1

      return {
        first: props.showFirstLastPage
          ? {
              icon: isRtl.value ? props.lastIcon : props.firstIcon,
              onClick: (e: Event) => setValue(e, start.value, 'first'),
              disabled: prevDisabled,
              'aria-label': t(props.firstAriaLabel),
              'aria-disabled': prevDisabled,
            }
          : undefined,
        prev: {
          icon: isRtl.value ? props.nextIcon : props.prevIcon,
          onClick: (e: Event) => setValue(e, page.value - 1, 'prev'),
          disabled: prevDisabled,
          'aria-label': t(props.previousAriaLabel),
          'aria-disabled': prevDisabled,
        },
        next: {
          icon: isRtl.value ? props.prevIcon : props.nextIcon,
          onClick: (e: Event) => setValue(e, page.value + 1, 'next'),
          disabled: nextDisabled,
          'aria-label': t(props.nextAriaLabel),
          'aria-disabled': nextDisabled,
        },
        last: props.showFirstLastPage
          ? {
              icon: isRtl.value ? props.firstIcon : props.lastIcon,
              onClick: (e: Event) =>
                setValue(e, start.value + length.value - 1, 'last'),
              disabled: nextDisabled,
              'aria-label': t(props.lastAriaLabel),
              'aria-disabled': nextDisabled,
            }
          : undefined,
      }
    })

    function updateFocus() {
      const currentIndex = page.value - start.value
      refs.value[currentIndex]?.$el.focus()
    }

    function onKeydown(e: KeyboardEvent) {
      if (
        e.key === keyValues.left &&
        !props.disabled &&
        page.value > +props.start
      ) {
        page.value = page.value - 1
        nextTick(updateFocus)
      } else if (
        e.key === keyValues.right &&
        !props.disabled &&
        page.value < start.value + length.value - 1
      ) {
        page.value = page.value + 1
        nextTick(updateFocus)
      }
    }

    return {
      resizeRef,
      themeClasses,
      onKeydown,
      controls,
      items,
      t,
    }
  },
})
</script>

<template>
  <component
    :is="$props.tag as string"
    :class="['base-pagination', themeClasses, $props.class]"
    :style="$props.style"
    role="navigation"
    :aria-label="t($props.ariaLabel as string)"
    @keydown="onKeydown"
    data-test="base-pagination-root"
  >
    <ul class="base-pagination__list">
      <li
        v-if="$props.showFirstLastPage"
        key="first"
        class="base-pagination__first"
        data-test="base-pagination__first"
      >
        <slot name="first" v-bind="controls.first">
          <BaseButton _as="BasePaginationButton" v-bind="controls.first" />
        </slot>
      </li>

      <li
        key="prev"
        class="base-pagination__prev"
        data-test="base-pagination-prev"
      >
        <slot name="prev" v-bind="controls.prev">
          <BaseButton _as="BasePaginationButton" v-bind="controls.prev" />
        </slot>
      </li>

      <li
        v-for="(item, index) in items"
        :key="item.key"
        :class="[
          'base-pagination__item',
          {
            'base-pagination__item--is-active': item.isActive,
          },
        ]"
        data-test="base-pagination-item"
      >
        <slot name="item" v-bind="item">
          <BaseButton _as="BasePaginationButton" v-bind="item.props">{{
            item.page
          }}</BaseButton>
        </slot>
      </li>

      <li
        key="next"
        class="base-pagination__next"
        data-test="base-pagination-next"
      >
        <slot name="next" v-bind="controls.next">
          <BaseButton _as="BasePaginationButton" v-bind="controls.next" />
        </slot>
      </li>

      <li
        v-if="$props.showFirstLastPage"
        key="last"
        class="base-pagination__last"
        data-test="base-pagination__last"
      >
        <slot name="last" v-bind="controls.last">
          <BaseButton _as="BasePaginationButton" v-bind="controls.last" />
        </slot>
      </li>
    </ul>
  </component>
</template>
