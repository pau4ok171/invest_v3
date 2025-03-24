<script lang="ts">
// Styles
import './BaseInfiniteScroll.scss'

// Components
import { BaseButton } from '@/apps/visagiste/components/BaseButton'
import { BaseProgressCircular } from '@/apps/visagiste/components/BaseProgressCircular'

// Composables
import { useLocale } from '@/apps/visagiste/composables'
import { useTagProps } from '@/apps/visagiste/composables/tag'
import {
  useDimension,
  useDimensionProps,
} from '@/apps/visagiste/composables/dimensions'
import { useIntersectionObserver } from '@/apps/visagiste/composables/intersectionObserver'

// Utilities
import {computed, h, nextTick, onMounted, ref, shallowRef, watch} from 'vue'
import {
  convertToUnit,
  defineComponent,
  propsFactory,
} from '@/apps/visagiste/utils'

// Types
import type { PropType } from 'vue'

export type InfiniteScrollSide = 'start' | 'end' | 'both'
export type InfiniteScrollStatus = 'ok' | 'empty' | 'loading' | 'error'

type InfiniteScrollSlot = {
  side: InfiniteScrollSide
  props: Record<string, any>
}

type BaseInfiniteScrollSlots = {
  default: never
  loading: InfiniteScrollSlot
  error: InfiniteScrollSlot
  empty: InfiniteScrollSlot
  'load-more': InfiniteScrollSlot
}

export const useBaseInfiniteScrollProps = propsFactory(
  {
    color: String,
    direction: {
      type: String as PropType<'vertical' | 'horizontal'>,
      default: 'vertical',
      validator: (value: any) => ['vertical', 'horizontal'].includes(value),
    },
    side: {
      type: String as PropType<InfiniteScrollSide>,
      default: 'end',
      validator: (value: any) => ['start', 'end', 'both'].includes(value),
    },
    mode: {
      type: String as PropType<'intersect' | 'manual'>,
      default: 'intersect',
      validator: (value: any) => ['intersect', 'manual'].includes(value),
    },
    margin: [Number, String],
    loadMoreText: {
      type: String,
      default: '$visagiste.infiniteScroll.loadMore',
    },
    emptyText: {
      type: String,
      default: '$visagiste.infiniteScroll.empty',
    },

    ...useDimensionProps(),
    ...useTagProps(),
  },
  'BaseInfiniteScroll'
)

export const BaseInfiniteScrollIntersect = defineComponent({
  name: 'BaseInfiniteScrollIntersect',
  props: {
    side: {
      type: String as PropType<InfiniteScrollSide>,
      required: true,
    },
    rootMargin: String,
  },
  emits: {
    intersect: (side: InfiniteScrollSide, isIntersecting: boolean) => true,
  },
  setup(props, { emit }) {
    const { intersectionRef, isIntersecting } = useIntersectionObserver()

    watch(isIntersecting, async (val) => {
      emit('intersect', props.side, val)
    })

    return () =>
      h(
        'div',
        {
          class: 'base-infinite-scroll-intersect',
          style: { '--base-infinite-margin-size': props.rootMargin },
          ref: intersectionRef,
        }
      )
  },
})

export default defineComponent({
  name: 'BaseInfiniteScroll',
  components: { BaseInfiniteScrollIntersect },
  props: useBaseInfiniteScrollProps(),
  emits: {
    load: (options: {
      side: InfiniteScrollSide
      done: (status: InfiniteScrollStatus) => void
    }) => true,
  },
  setup(props, { slots, emit }) {
    const rootEl = ref<HTMLDivElement>()
    const startStatus = shallowRef<InfiniteScrollStatus>('ok')
    const endStatus = shallowRef<InfiniteScrollStatus>('ok')
    const margin = computed(() => convertToUnit(props.margin))
    const isIntersecting = shallowRef(false)

    function setScrollAmount(amount: number) {
      if (!rootEl.value) return

      const property =
        props.direction === 'vertical' ? 'scrollTop' : 'scrollLeft'
      rootEl.value[property] = amount
    }

    function getScrollAmount() {
      if (!rootEl.value) return 0

      const property =
        props.direction === 'vertical' ? 'scrollTop' : 'scrollLeft'
      return rootEl.value[property]
    }

    function getScrollSize() {
      if (!rootEl.value) return 0
    }

    function getContainerSize() {
      if (!rootEl.value) return 0

      const property =
        props.direction === 'vertical' ? 'clientHeight' : 'clientWidth'
      return rootEl.value[property]
    }

    onMounted(() => {
      if (!rootEl.value) return

      if (props.side === 'start') {
        setScrollAmount(getScrollSize() as number)
      } else if (props.side === 'both') {
        setScrollAmount(getScrollSize() as number / 2 - getContainerSize() / 2)
      }
    })

    function setStatus(side: InfiniteScrollSide, status: InfiniteScrollStatus) {
      if (side === 'start') {
        startStatus.value = status
      } else if (side === 'end') {
        endStatus.value = status
      }
    }

    function getStatus(side: string) {
      return side === 'start' ? startStatus.value : endStatus.value
    }

    let previousScrollSize = 0
    function handleIntersect(
      side: InfiniteScrollSide,
      _isIntersecting: boolean
    ) {
      isIntersecting.value = _isIntersecting
      if (isIntersecting.value) {
        intersecting(side)
      }
    }

    function intersecting(side: InfiniteScrollSide) {
      if (props.mode !== 'manual' && !isIntersecting.value) return

      const status = getStatus(side)
      if (!rootEl.value || ['empty', 'loading'].includes(status)) return

      previousScrollSize = getScrollSize() as number
      setStatus(side, 'loading')

      function done(status: InfiniteScrollStatus) {
        setStatus(side, status)

        nextTick(() => {
          if (status === 'empty' || status === 'error') return

          if (status === 'ok' && side === 'start') {
            setScrollAmount(
              getScrollSize() as number - previousScrollSize + getScrollAmount()
            )
          }
          if (props.mode !== 'manual') {
            nextTick(() => {
              window.requestAnimationFrame(() => {
                window.requestAnimationFrame(() => {
                  window.requestAnimationFrame(() => {
                    intersecting(side)
                  })
                })
              })
            })
          }
        })
      }

      emit('load', { side, done })
    }

    const { t } = useLocale()

    function renderSide(
      side: InfiniteScrollSide,
      status: InfiniteScrollStatus
    ) {
      if (props.side !== side && props.side !== 'both') return

      const onClick = () => intersecting(side)
      const slotProps = { side, props: { onClick, color: props.color } }

      if (status === 'error') return slots.error?.(slotProps)

      if (status === 'empty')
        return slots.empty?.(slotProps) ?? h('div', t(props.emptyText))

      if (props.mode === 'manual') {
        if (status === 'loading') {
          return (
            slots.loading?.(slotProps) ??
            h(BaseProgressCircular, { indeterminate: true, color: props.color })
          )
        }

        return (
          slots['load-more']?.(slotProps) ??
          h(
            BaseButton,
            { variant: 'outlined', color: props.color, onClick: onClick },
            t(props.loadMoreText)
          )
        )
      }

      return (
        slots.loading?.(slotProps) ??
        h(BaseProgressCircular, { indeterminate: true, color: props.color })
      )
    }

    const { dimensionStyles } = useDimension(props)

    const hasStartIntersect = computed(
      () => props.side === 'start' || props.side === 'both'
    )
    const hasEndIntersect = computed(
      () => props.side === 'end' || props.side === 'both'
    )
    const intersectMode = computed(() => props.mode === 'intersect')

    return {
      rootEl,
      hasStartIntersect,
      hasEndIntersect,
      intersectMode,
      dimensionStyles,
      renderSide,
      startStatus,
      endStatus,
      handleIntersect,
      margin,
    }
  },
})
</script>

<template>
  <component
    :is="$props.tag as string"
    ref="rootEl"
    :class="[
      'base-infinite-scroll',
      `base-infinite-scroll--${$props.direction}`,
      {
        'base-infinite-scroll--start': hasStartIntersect,
        'base-infinite-scroll--end': hasEndIntersect,
      },
    ]"
    :style="dimensionStyles"
  >
    <div class="base-infinite-scroll__side">
      <component :is="renderSide('start', startStatus)" />
    </div>

    <template v-if="hasStartIntersect && intersectMode">
      <BaseInfiniteScrollIntersect
        key="start"
        side="start"
        :onIntersect="handleIntersect"
        :root-margin="margin"
      />
    </template>

    <slot name="default" />

    <template v-if="hasEndIntersect && intersectMode">
      <BaseInfiniteScrollIntersect
        key="end"
        side="end"
        :onIntersect="handleIntersect"
        :root-margin="margin"
      />
    </template>

    <div class="base-infinite-scroll__side">
      <component :is="renderSide('end', endStatus)" />
    </div>
  </component>
</template>
