<script lang="ts">
// Styles

// Components
import { BaseFadeTransition } from '@/apps/visagiste/components/transitions'

// Composables
import {
  useDisplay,
  useDisplayProps,
} from '@/apps/visagiste/composables/display'
import { useGroup, useGroupProps } from '@/apps/visagiste/composables/group'
import { useComponentProps } from '@/apps/visagiste/composables/component'
import { useGoTo } from '@/apps/visagiste/composables/goto'
import { IconValue } from '@/apps/visagiste/composables/icons'
import { useTagProps } from '@/apps/visagiste/composables/tag'
import { useRtl } from '@/apps/visagiste/composables'
import { useResizeObserver } from '@/apps/visagiste/composables/resizeObserver'

// Utilities
import { computed, shallowRef, watch } from 'vue'
import {
  defineComponent,
  focusableChildren,
  IN_BROWSER,
  propsFactory,
} from '@/apps/visagiste/utils'
import {
  calculateUpdatedTarget,
  calculateCenteredTarget,
  getOffsetSize,
  getScrollPosition,
  getScrollSize,
  getClientSize,
} from './helpers'

// Types
import type { InjectionKey, PropType } from 'vue'
import type { GroupProvide } from '@/apps/visagiste/composables/group'
import type { GoToOptions } from '@/apps/visagiste/composables/goto'
import { BaseIcon } from '@/apps/visagiste/components/BaseIcon'

export const BaseSlideGroupSymbol: InjectionKey<GroupProvide> = Symbol.for(
  'visagiste:base-slide-group'
)

interface SlideGroupSlot {
  next: GroupProvide['next']
  prev: GroupProvide['prev']
  select: GroupProvide['select']
  isSelect: GroupProvide['isSelected']
}

type BaseSlideGroupSlots = {
  default: SlideGroupSlot
  prev: SlideGroupSlot
  next: SlideGroupSlot
}

export const useBaseSlideGroupProps = propsFactory(
  {
    centerActive: Boolean,
    direction: {
      type: String as PropType<'horizontal' | 'vertical'>,
      default: 'horizontal',
    },
    symbol: {
      type: null,
      default: BaseSlideGroupSymbol,
    },
    nextIcon: {
      type: IconValue,
      default: '$next',
    },
    prevIcon: {
      type: IconValue,
      default: '$prev',
    },
    showArrows: {
      type: [Boolean, String],
      validator: (v: any) =>
        typeof v === 'boolean' || ['always', 'desktop', 'mobile'].includes(v),
    },

    ...useComponentProps(),
    ...useDisplayProps({ mobile: null }),
    ...useTagProps(),
    ...useGroupProps({
      selectedClass: 'base-slide-group-item--active',
    }),
  },
  'BaseSlideGroup'
)

export default defineComponent({
  name: 'BaseSlideGroup',
  computed: {
    sl() {
      return sl
    },
  },
  components: {
    BaseIcon,
    BaseFadeTransition,
  },
  props: useBaseSlideGroupProps(),
  emits: {
    'update:modelValue': (value: any) => true,
  },
  setup(props) {
    const { isRtl } = useRtl()
    const { displayClasses, mobile } = useDisplay(props)
    const group = useGroup(props, props.symbol)
    const isOverflowing = shallowRef(false)
    const scrollOffset = shallowRef(0)
    const containerSize = shallowRef(0)
    const contentSize = shallowRef(0)
    const isHorizontal = computed(() => props.direction === 'horizontal')

    const { resizeRef: containerRef, contentRect: containerRect } =
      useResizeObserver()
    const { resizeRef: contentRef, contentRect } = useResizeObserver()

    const goTo = useGoTo()
    const goToOptions = computed<Partial<GoToOptions>>(() => {
      return {
        container: containerRef.el,
        duration: 200,
        easing: 'easeOutQuart',
      }
    })

    const firstSelectedIndex = computed(() => {
      if (!group.selected.value.length) return -1

      return group.items.value.findIndex(
        (item) => item.id === group.selected.value[0]
      )
    })

    const lastSelectedIndex = computed(() => {
      if (!group.selected.value.length) return -1

      return group.items.value.findIndex(
        (item) =>
          item.id === group.selected.value[group.selected.value.length - 1]
      )
    })

    if (IN_BROWSER) {
      let frame = -1
      watch(
        () => [
          group.selected.value,
          containerRect.value,
          contentRect.value,
          isHorizontal.value,
        ],
        () => {
          cancelAnimationFrame(frame)
          frame = requestAnimationFrame(() => {
            if (contentRect.value && contentRect.value) {
              const sizeProperty = isHorizontal.value ? 'width' : 'height'

              containerSize.value = containerRect.value[sizeProperty]
              contentSize.value = contentRect.value[sizeProperty]

              isOverflowing.value =
                containerSize.value + 1 < containerSize.value
            }

            if (firstSelectedIndex.value >= 0 && contentRef.el) {
              // TODO: Is this too naive? Should we store element references in group composable?
              const selectedElement = contentRef.el.children[
                lastSelectedIndex.value
              ] as HTMLElement

              scrollToChildren(selectedElement, props.centerActive)
            }
          })
        }
      )
    }

    const isFocused = shallowRef(false)

    function scrollToChildren(children: HTMLElement, center?: boolean) {
      let target = 0

      if (center) {
        target = calculateCenteredTarget({
          containerElement: containerRef.el!,
          isHorizontal: isHorizontal.value,
          selectedElement: children,
        })
      } else {
        target = calculateUpdatedTarget({
          containerElement: containerRef.el!,
          isHorizontal: isHorizontal.value,
          isRtl: isRtl.value,
          selectedElement: children,
        })
      }

      scrollToPosition(target)
    }

    function scrollToPosition(newPosition: number) {
      if (!IN_BROWSER || !containerRef.el) return

      const offsetSize = getOffsetSize(isHorizontal.value, containerRef.el)
      const scrollPosition = getScrollPosition(
        isHorizontal.value,
        isRtl.value,
        containerRef.el
      )
      const scrollSize = getScrollSize(isHorizontal.value, containerRef.el)

      if (
        scrollSize <= offsetSize ||
        // Prevent scrolling by only a couple of pixels, which doesn't look smooth
        Math.abs(newPosition - scrollPosition) < 16
      )
        return

      if (isHorizontal.value && isRtl.value && containerRef.el) {
        const { scrollWidth, offsetWidth: containerWidth } = containerRef.el!

        newPosition = scrollWidth - containerWidth - newPosition
      }

      if (isHorizontal.value) {
        goTo.horizontal(newPosition, goToOptions.value)
      } else {
        goTo(newPosition, goToOptions.value)
      }
    }

    function onScroll(e: Event) {
      const { scrollTop, scrollLeft } = e.target as HTMLElement

      scrollOffset.value = isHorizontal.value ? scrollLeft : scrollTop
    }

    function onFocusin(e: FocusEvent) {
      isFocused.value = true

      if (!isOverflowing.value || !containerRef.el) return

      // Focused element is likely to be the root of an item, so a
      // breadth-first search will probably find it in the first iteration
      for (const el of e.composedPath()) {
        for (const item of contentRef.el.children) {
          if (item === el) {
            scrollToChildren(item as HTMLElement)
            return
          }
        }
      }
    }

    function onFocusout(e: FocusEvent) {
      isFocused.value = false
    }

    // Affix clicks produce onFocus that we have to ignore to avoid extra scrollToChildren
    let ignoreFocusEvent = false
    function onFocus(e: FocusEvent) {
      if (
        !ignoreFocusEvent &&
        !isFocused &&
        !(e.relatedTarget && contentRef.el?.contains(e.relatedTarget as Node))
      )
        focus()

      ignoreFocusEvent = false
    }

    function onFocusAffixes() {
      ignoreFocusEvent = true
    }

    function onKeydown(e: KeyboardEvent) {
      if (!contentRef.el) return

      function toFocus(location: Parameters<typeof focus>[0]) {
        e.preventDefault()
        focus(location)
      }

      if (isHorizontal.value) {
        if (e.key === 'ArrowRight') {
          toFocus(isRtl.value ? 'prev' : 'next')
        } else if (e.key === 'ArrowLeft') {
          toFocus(isRtl.value ? 'next' : 'prev')
        }
      } else {
        if (e.key === 'ArrowDown') {
          toFocus('next')
        } else if (e.key === 'ArrowUp') {
          toFocus('prev')
        }
      }

      if (e.key === 'Home') {
        toFocus('first')
      } else if (e.key === 'End') {
        toFocus('last')
      }
    }

    function getSiblingElement(
      el: HTMLElement | null,
      location: 'next' | 'prev'
    ) {
      if (!el) return undefined
      let sibling: HTMLElement | null = el
      do {
        sibling = sibling?.[
          location === 'next' ? 'nextElementSibling' : 'previousElementSibling'
        ] as HTMLElement | null
      } while (sibling?.hasAttribute('disabled'))
      return sibling
    }

    function focus(location?: 'next' | 'prev' | 'first' | 'last') {
      if (!contentRef.el) return

      let el: HTMLElement | null | undefined

      if (!location) {
        const focusable = focusableChildren(containerRef.el)
        el = focusable[0]
      } else if (location === 'next') {
        el = getSiblingElement(contentRef.el.querySelector(':focus'), location)

        if (!el) return focus('first')
      } else if (location === 'prev') {
        el = getSiblingElement(contentRef.el.querySelector(':focus'), location)

        if (!el) return focus('last')
      } else if (location === 'first') {
        el = contentRef.el.firstElementChild as HTMLElement

        if (el?.hasAttribute('disabled')) el = getSiblingElement(el, 'next')
      } else if (location === 'last') {
        el = contentRef.el.lastElementChild as HTMLElement

        if (el?.hasAttribute('disabled')) el = getSiblingElement(el, 'prev')
      }

      if (el) {
        el.focus({ preventScroll: true })
      }
    }

    function scrollTo(location: 'prev' | 'next') {
      const direction = isHorizontal.value && isRtl.value ? -1 : 1

      const offsetStep =
        (location === 'prev' ? -direction : direction) * containerSize.value

      let newPosition = scrollOffset.value + offsetStep

      // TODO: improve it
      if (isHorizontal.value && isRtl.value && containerRef.el) {
        const { scrollWidth, offsetWidth: containerWidth } = containerRef.el!

        newPosition += scrollWidth - containerWidth
      }

      scrollToPosition(newPosition)
    }

    const slotProps = computed(() => ({
      next: group.next,
      prev: group.prev,
      select: group.select,
      isSelected: group.isSelected,
    }))

    const hasAffixes = computed(() => {
      switch (props.showArrows) {
        // Always show arrows on desktop & mobile
        case 'always':
          return true

        // Allways show arrows on desktop
        case 'desktop':
          return !mobile.value

        // Show arrows on mobile when overflowing.
        // This matches the default 2.2 behavior
        case true:
          return isOverflowing.value || Math.abs(scrollOffset.value) > 0

        // Always show on mobile
        case 'mobile':
          return (
            mobile.value ||
            isOverflowing.value ||
            Math.abs(scrollOffset.value) > 0
          )

        // https://material.io/components/tabs#scrollable-tabs
        // Always show arrows when
        // overflowed on desktop
        default:
          return (
            !mobile.value &&
            (isOverflowing.value || Math.abs(scrollOffset.value) > 0)
          )
      }
    })

    const hasPrev = computed(() => {
      // 1 pixel in reserve, may be lost after rounding
      return Math.abs(scrollOffset.value) > 1
    })

    const hasNext = computed(() => {
      if (!containerRef.value) return false

      const scrollSize = getScrollSize(isHorizontal.value, containerRef.el)
      const clientSize = getClientSize(isHorizontal.value, containerRef.el)

      const scrollSizeMax = scrollSize - clientSize

      // 1 pixel in reserve, may be lost after rounding
      return scrollSizeMax - Math.abs(scrollOffset.value) > 1
    })

    return {
      containerRef,
      contentRef,
      slotProps,
      group,
      isHorizontal,
      isFocused,
      isRtl,
      hasAffixes,
      hasPrev,
      hasNext,
      isOverflowing,
      displayClasses,
      onFocus,
      onFocusAffixes,
      onScroll,
      onFocusin,
      onFocusout,
      onKeydown,
      scrollTo,
    }
  },
})
</script>

<template>
  <component
    :is="$props.tag"
    :class="[
      'base-slide-group',
      {
        'base-slide-group--vertical': !isHorizontal,
        'base-slide-group--has-affixes': hasAffixes,
        'base-slide-group--is-overflowing': isOverflowing,
      },
      displayClasses,
      $props.class,
    ]"
    :style="$props.style"
    :tabindex="isFocused || group.selected.length ? -1 : 0"
    @focus="onFocus"
  >
    <div
      v-if="hasAffixes"
      key="prev"
      :class="[
        'base-slide-group__prev',
        { 'base-slide-group--disabled': !hasPrev },
      ]"
      @mousedown="onFocusAffixes"
      @click="() => hasPrev && scrollTo('prev')"
    >
      <slot name="prev" v-bind:prev="slotProps">
        <BaseFadeTransition>
          <BaseIcon :icon="isRtl ? $props.nextIcon : $props.prevIcon" />
        </BaseFadeTransition>
      </slot>
    </div>

    <div
      key="container"
      :ref="containerRef"
      class="base-slide-group__container"
      @scroll="onScroll"
    >
      <div
        :ref="contentRef"
        class="base-slide-group__content"
        @focusin="onFocusin"
        @focusout="onFocusout"
        @keydown="onKeydown"
      >
        <slot v-bind="slotProps" />
      </div>
    </div>

    <div
      v-if="hasAffixes"
      key="next"
      :class="[
        'base-slide-group__next',
        { 'base-slide-group--disabled': !hasNext },
      ]"
      @mousedown="onFocusAffixes"
      @click="() => hasNext && scrollTo('next')"
    >
      <slot name="next" v-bind:prev="slotProps">
        <BaseFadeTransition>
          <BaseIcon :icon="isRtl ? $props.prevIcon : $props.nextIcon" />
        </BaseFadeTransition>
      </slot>
    </div>
  </component>
</template>
