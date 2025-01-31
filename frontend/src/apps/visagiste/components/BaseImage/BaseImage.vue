<script lang="ts">
// Styles
import './BaseImage.scss';

// Components
import BaseResponsive, { useBaseResponsiveProps } from '../BaseResponsive/BaseResponsive.vue'

// Composables
import {useRounded, useRoundedProps} from "@/apps/visagiste/composables/rounded";
import {useTransitionProps} from "@/apps/visagiste/composables/transition";
import {useBackgroundColor} from "@/apps/visagiste/composables/color";
import {useComponentProps} from "@/apps/visagiste/composables/component";
import MaybeTransition from "@/apps/visagiste/composables_v2/transition.vue";

// Directives
import intersect from "@/apps/visagiste/directives/intersect";

// Utilities
import {
  computed,
  h,
  nextTick,
  onBeforeMount,
  onBeforeUnmount,
  ref,
  shallowRef,
  toRef,
  vShow,
  watch,
  withDirectives
} from "vue";
import {
  convertToUnit,
  defineComponent,
  getCurrentInstance,
  propsFactory,
  SUPPORTS_INTERSECTION
} from "@/apps/visagiste/utils";

// Types
import type {PropType} from "vue";

// Not intended for public use, this is passed in by visagiste-loader
export interface srcObject {
  src?: string
  srcset?: string
  lazySrc?: string
  aspect: number
}

export type BaseImageSlots = {
  default: never
  placeholder: never
  error: never
  sources: never
}

export const useBaseImageProps = propsFactory({
  absolute: Boolean,
  alt: String,
  cover: Boolean,
  color: String,
  draggable: {
    type: [Boolean, String] as PropType<boolean | 'true' | 'false'>,
    default: undefined
  },
  eager: Boolean,
  gradient: String,
  lazySrc: String,
  options: {
    type: Object as PropType<IntersectionObserverInit>,
    // For more information on types, navigate to:
    // https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API
    default: () => ({
      root: undefined,
      rootMargin: undefined,
      threshold: undefined,
    }),
  },
  sizes: String,
  src: {
    type: [String, Object] as PropType<string | srcObject>,
    default: '',
  },
  crossorigin: String as PropType<'' | 'anonymous' | 'use-credentials'>,
  referrerpolicy: String as PropType<
    | 'no-referrer'
    | 'no-referrer-when-downgrade'
    | 'origin'
    | 'origin-when-cross-origin'
    | 'same-origin'
    | 'strict-origin'
    | 'strict-origin-when-cross-origin'
    | 'unsafe-url'
  >,
  srcset: String,
  position: String,

  ...useBaseResponsiveProps(),
  ...useComponentProps(),
  ...useRoundedProps(),
  ...useTransitionProps(),
}, 'BaseImage')

export default defineComponent({
  name: 'BaseImage',
  methods: {
    convertToUnit,
  },
  components: {
    MaybeTransition,
    BaseResponsive
  },
  directives: { intersect },
  props: useBaseImageProps(),
  emits: {
    loadstart: (value: string | undefined) => true,
    load: (value: string | undefined) => true,
    error: (value: string | undefined) => true
  },
  setup (props, { emit, slots }) {
    const { backgroundColorClasses, backgroundColorStyles } = useBackgroundColor(toRef(props, 'color'))
    const { roundedClasses } = useRounded(props)
    const vm = getCurrentInstance('BaseImage')

    const currentSrc = shallowRef('') // Set from srcset
    const image = ref<HTMLImageElement>()
    const state = shallowRef<'idle' | 'loading' | 'loaded' | 'error'>(props.eager ? 'loading' : 'idle')
    const naturalWidth = shallowRef<number>()
    const naturalHeight = shallowRef<number>()

    const normalisedSrc = computed<srcObject>(() => {
      return props.src && typeof props.src === 'object'
        ? {
            src: props.src.src,
            srcset: props.srcset || props.src.srcset,
            lazySrc: props.lazySrc || props.src.lazySrc,
            aspect: Number(props.aspectRatio || props.src.aspect || 0),
          } : {
            src: props.src,
            srcset: props.srcset,
            lazySrc: props.lazySrc,
            aspect: Number(props.aspectRatio || 0),
          }
    })
    const aspectRatio = computed(() => {
      return normalisedSrc.value.aspect || naturalWidth.value! / naturalHeight.value! || 0
    })

    watch(() => props.src, () => {
      init(state.value !== 'idle')
    })
    watch(aspectRatio, (val, oldValue) => {
      if (!val && oldValue && image.value) {
        pollForSize(image.value)
      }
    })

    // TODO: getSrc when window width changes

    onBeforeMount(() => init())

    function init (isIntersecting?: boolean) {
      if (props.eager && isIntersecting) return
      if (
        SUPPORTS_INTERSECTION &&
        !isIntersecting &&
        !props.eager
      ) return

      state.value = 'loading'

      if (normalisedSrc.value.lazySrc) {
        const lazyImage = new Image()
        lazyImage.src = normalisedSrc.value.lazySrc
        pollForSize(lazyImage, null)
      }

      if (!normalisedSrc.value.src) return

      nextTick(() => {
        emit('loadstart', image.value?.currentSrc || normalisedSrc.value.src)

        setTimeout(() => {
          if (vm.isUnmounted) return

          if (image.value?.complete) {
            if (!image.value?.naturalWidth) {
              onError()
            }

            if (state.value === 'error') return

            if (!aspectRatio.value) pollForSize(image.value, null)
            if (state.value === 'loading') onLoad()
          } else {
            if (!aspectRatio.value) pollForSize(image.value!)
            getSrc()
          }
        })
      })
    }

    function onLoad () {
      if (vm.isUnmounted) return

      getSrc()
      pollForSize(image.value!)
      state.value = 'loaded'
      emit('load', image.value?.currentSrc || normalisedSrc.value.src)
    }

    function onError () {
      if (vm.isUnmounted) return

      state.value = 'error'
      emit('error', image.value?.currentSrc || normalisedSrc.value.src)
    }

    function getSrc () {
      const img = image.value
      if (img) currentSrc.value = img.currentSrc || img.src
    }

    let timer = -1

    onBeforeUnmount(() => {
      clearTimeout(timer)
    })

    function pollForSize (img: HTMLImageElement, timeout: number | null = 100) {
      const poll = () => {
        clearTimeout(timer)
        if (vm.isUnmounted) return

        const { naturalHeight: imgHeight, naturalWidth: imgWidth } = img

        if (imgHeight || imgWidth) {
          naturalWidth.value = imgWidth
          naturalHeight.value = imgHeight
        } else if (!img.complete && state.value === 'loading' && timeout != null) {
          timer = window.setTimeout(poll, timeout)
        } else if (img.currentSrc.endsWith('.svg') || img.currentSrc.startsWith('data:image/svg+xml')) {
          naturalWidth.value = 1
          naturalHeight.value = 1
        }
      }

      poll()
    }

    const containClasses = computed(() => ({
      'base-image__image--cover': props.cover,
      'base-image__image--contain': !props.cover,
    }))

    const imageIs = () => {
      console.log(normalisedSrc.value)
      console.log(state.value)
      if (!normalisedSrc.value.src || state.value === 'idle') return null

      const img = h('img', {
        class: ['base-image__image', containClasses.value],
        style: {objectPosition: props.position},
        crossorigin: props.crossorigin,
        src: normalisedSrc.value.src,
        srcset: normalisedSrc.value.srcset,
        alt: props.alt,
        referrerpolicy: props.referrerpolicy,
        draggable: props.draggable,
        sizes: props.sizes,
        ref: image,
        onLoad: onLoad,
        onError: onError,
      })

      const sources = slots.sources?.()

      return h(MaybeTransition, {
        transition: props.transition,
        appear: true,
      },
      withDirectives(
        sources
          ? h('picture', { class: 'base-image__picture' }, [sources, img])
          : img,
        [[vShow, state.value === 'loaded']]
      ))
    }

    const preloadImageIs = () => h(MaybeTransition, {
      transition: props.transition,
    }, {
      default: () => [
        normalisedSrc.value.lazySrc && state.value !== 'loaded'
          ? h('img', {
            class: ['base-image__image', 'base-image__image--preload', containClasses.value],
            style: {objectPosition: props.position},
            crossorigin: props.crossorigin,
            src: normalisedSrc.value.lazySrc,
            alt: props.alt,
            referrerpolicy: props.referrerpolicy,
            draggable: props.draggable,
          })
          : null
      ]
    })

    const placeholderIs = () => {
      if (!slots.placeholder) return null

      return h(MaybeTransition, {
        transition: props.transition,
        appear: true,
      }, [
        state.value === 'loading' || (state.value === 'error' && !slots.error)
          ? h('div', { class: 'base-image__placeholder' }, [slots.placeholder()])
          : null
      ])
    }

    const errorIs = () => {
      if (!slots.error) return null

      return h(MaybeTransition, {
        transition: props.transition,
        appear: true,
      }, [
        state.value === 'error'
          ? h('div', { class: 'base-image__error' }, [slots.error()])
          : null
      ])
    }

    const gradientIs = () => {
      if (!props.gradient) return null

      return h('div', {
        class: 'base-image__gradient',
        style: { backgroundImage: `linear-gradient(${props.gradient})` },
      })
    }

    const isBooted = shallowRef(false)
    {
      const stop = watch(aspectRatio, val => {
        if (val) {
          // Doesn't work with nextTick, idk why
          requestAnimationFrame(() => {
            requestAnimationFrame(() => {
              isBooted.value = true
            })
          })
          stop()
        }
      })
    }

    const responsiveProps = computed(() => BaseResponsive.filterProps(props))

    return {
      backgroundColorClasses,
      backgroundColorStyles,
      roundedClasses,
      aspectRatio,
      init,
      naturalWidth,
      isBooted,
      responsiveProps,
      imageIs,
      preloadImageIs,
      placeholderIs,
      errorIs,
      gradientIs,
    }
  }
})
</script>

<template>
<BaseResponsive
  :class="[
    'base-image',
    {
      'base-image--absolute': $props.absolute,
      'base-image--booting': !isBooted,
    },
    backgroundColorClasses,
    roundedClasses,
    $props.class,
  ]"
  :style="[
    { width: convertToUnit($props.width === 'auto' ? naturalWidth : $props.width) },
    backgroundColorStyles,
    $props.style,
  ]"
  v-bind="{...responsiveProps}"
  :aspectRatio="aspectRatio"
  :aria-label="$props.alt"
  :role="$props.alt ? 'img' : undefined"
  v-intersect="[{
    handler: init,
    options: $props.options,
  }, null, ['once']]"
>

  <component :is="imageIs"/>
  <component :is="preloadImageIs"/>
  <component :is="gradientIs"/>
  <component :is="placeholderIs"/>
  <component :is="errorIs"/>

  <slot/>

</BaseResponsive>
</template>
