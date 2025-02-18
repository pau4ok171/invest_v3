<script lang="ts">
// Styles
import './BaseOverlay.scss'

// Composables
import {useLocationStrategies, useLocationStrategyProps} from "./locationStrategies";
import {useScrollStrategies, useScrollStrategyProps} from "./scrollStrategies";
import {useActivator, useActivatorProps} from "./useActivator";
import {useComponentProps} from "@/apps/visagiste/composables/component";
import {useDimension, useDimensionProps} from "@/apps/visagiste/composables/dimensions";
import {provideTheme, useThemeProps} from "@/apps/visagiste/composables/theme";
import {useLazy, useLazyProps} from "@/apps/visagiste/composables/lazy";
import {useProxiedModel} from "@/apps/visagiste/composables/proxiedModel";
import {useRtl} from "@/apps/visagiste/composables";
import {useBackgroundColor} from "@/apps/visagiste/composables/color";
import {useStack} from "@/apps/visagiste/composables/stack";
import {useTeleport} from "@/apps/visagiste/composables/teleport";
import {useHydration} from "@/apps/visagiste/composables/hydration";
import {useScopeId} from "@/apps/visagiste/composables/scopeId";
import {useBackButton, useRouter} from "@/apps/visagiste/composables/router";
import {useToggleScope} from "@/apps/visagiste/composables/toggleScope";
import MaybeTransition, { useTransitionProps } from "@/apps/visagiste/composablesV2/transition.vue";

// Directives
import { ClickOutside } from "@/apps/visagiste/directives";

// Utilities
import {computed, h, mergeProps, onBeforeUnmount, ref, toRef, Transition, watch} from "vue";
import {
  animate,
  convertToUnit,
  defineComponent,
  getCurrentInstance,
  getScrollParent,
  IN_BROWSER,
  propsFactory,
  standardEasing,
} from "@/apps/visagiste/utils";

// Types
import type { Ref, PropType } from 'vue';
import type {BackgroundColorData} from "@/apps/visagiste/composables/color";
import type { TemplateRef } from "@/apps/visagiste/utils";

interface ScrimProps {
  [key: string]: unknown
  modelValue: boolean
  color: BackgroundColorData
}
function Scrim (props: ScrimProps) {
  const { modelValue, color, ...rest } = props
  return h(Transition, {
    name: 'fade-transition',
    appear: true,
  }, {
    default: () => props.modelValue
      ? h('div', {
        class: ['base-overlay__scrim', props.color.backgroundColorClasses.value],
        style: props.color.backgroundColorStyles.value,
        ...rest,
      })
      : null
  })
}

export type OverlaySlots = {
  default: { isActive: Ref<boolean> }
  activator: { isActive: boolean, props: Record<string, any>, targetRef: TemplateRef }
}

export const useBaseOverlayProps = propsFactory({
  absolute: Boolean,
  attach: [Boolean, String, Object] as PropType<boolean | string | Element>,
  closeOnBack: {
    type: Boolean,
    default: true,
  },
  contained: Boolean,
  contentClass: null,
  contentProps: null,
  disabled: Boolean,
  opacity: [Number, String],
  noClickAnimation: Boolean,
  modelValue: Boolean,
  persistent: Boolean,
  scrim: {
    type: [Boolean, String],
    default: true,
  },
  zIndex: {
    type: [Number, String],
    default: 2000,
  },

  ...useActivatorProps(),
  ...useComponentProps(),
  ...useDimensionProps(),
  ...useLazyProps(),
  ...useLocationStrategyProps(),
  ...useScrollStrategyProps(),
  ...useThemeProps(),
  ...useTransitionProps(),
}, 'BaseOverlay')

export default defineComponent({
  name: "BaseOverlay",
  components: {
    MaybeTransition,
  },
  methods: {
    convertToUnit,
    mergeProps
  },
  directives: {
    ClickOutside,
  },
  inheritAttrs: false,
  props: {
    _disableGlobalStack: Boolean,

    ...useBaseOverlayProps(),
  },
  emits: {
    'click:outside': (e: MouseEvent) => true,
    'update:modelValue': (value: boolean) => true,
    afterEnter: () => true,
    afterLeave: () => true,
  },
  setup (props, { emit }) {
    const vm = getCurrentInstance('BaseOverlay')
    const root = ref<HTMLElement>()
    const scrimEl = ref<HTMLElement>()
    const contentEl = ref<HTMLElement>()
    const model = useProxiedModel(props, 'modelValue')
    const isActive = computed({
      get: () => model.value,
      set: v => {
        if (!(v && props.disabled)) model.value = v
      },
    })

    const { themeClasses } = provideTheme(props)
    const { rtlClasses, isRtl } = useRtl()
    const { hasContent, onAfterLeave: _onAfterLeave } = useLazy(props, isActive)
    const scrimColor = useBackgroundColor(computed(() => {
      return typeof props.scrim === 'string' ? props.scrim : null
    }))
    const { globalTop, localTop, stackStyles } = useStack(isActive, toRef(props, 'zIndex'), props._disableGlobalStack)
    const {
      activatorEl,
      activatorRef,
      target,
      targetEl,
      targetRef,
      activatorEvents,
      contentEvents,
      scrimEvents,
    } = useActivator(props, { isActive, isTop: localTop, contentEl })
    const { teleportTarget } = useTeleport(() => {
      const target = props.attach || props.contained
      if (target) return target
      const rootNode = activatorEl?.value?.getRootNode() || vm.proxy?.$el?.getRootNode()
      if (rootNode instanceof ShadowRoot) return rootNode
      return false
    })
    const { dimensionStyles } = useDimension(props)
    const isMounted = useHydration()
    const { scopeId } = useScopeId()

    watch(() => props.disabled, v => {
      if (v) isActive.value = false
    })

    const { contentStyles, updateLocation } = useLocationStrategies(props, {
      isRtl,
      contentEl,
      target,
      isActive,
    })
    useScrollStrategies(props, {
      root,
      contentEl,
      targetEl,
      isActive,
      updateLocation,
    })

    function onClickOutside (e: MouseEvent) {
      emit('click:outside', e)

      if (!props.persistent) isActive.value = false
      else animateClick()
    }

    function closeConditional (e: Event) {
      return isActive.value && globalTop.value && (
        // If using scrim, only close if clicking on it rather than anything opened on top
        !props.scrim || e.target === scrimEl.value || (e instanceof MouseEvent && e.shadowTarget === scrimEl.value)
      )
    }

    IN_BROWSER && watch(isActive, val => {
      if (val) {
        window.addEventListener('keydown', onKeydown)
      } else {
        window.removeEventListener('keydown', onKeydown)
      }
    }, { immediate: true })

    onBeforeUnmount(() => {
      if (!IN_BROWSER) return

      window.removeEventListener('keydown', onKeydown)
    })

    function onKeydown (e: KeyboardEvent) {
      if (e.key === 'Escape' && globalTop.value) {
        if (!props.persistent) {
          isActive.value = false
          if (contentEl.value?.contains(document.activeElement)) {
            activatorEl.value?.focus()
          }
        } else animateClick()
      }
    }

    const router = useRouter()
    useToggleScope(() => props.closeOnBack, () => {
      useBackButton(router, next => {
        if (globalTop.value && isActive.value) {
          next(false)
          if (!props.persistent) isActive.value = false
          else animateClick()
        } else {
          next()
        }
      })
    })

    const top = ref<number>()
    watch(() => isActive.value && (props.absolute || props.contained) && teleportTarget.value == null, val => {
      if (val) {
        const scrollParent = getScrollParent(root.value)
        if (scrollParent && scrollParent !== document.scrollingElement) {
          top.value = scrollParent.scrollTop
        }
      }
    })

    // Add a quick "bounce" animation to the content
    function animateClick () {
      if (props.noClickAnimation) return

      contentEl.value && animate(contentEl.value, [
        { transformOrigin: 'center' },
        { transform: 'scale(1.03)' },
        { transformOrigin: 'center' },
      ], {
        duration: 150,
        easing: standardEasing,
      })
    }

    function onAfterEnter () {
      emit('afterEnter')
    }

    function onAfterLeave () {
      _onAfterLeave()
      emit('afterLeave')
    }

    return {
      isActive,
      isMounted,
      hasContent,
      activatorEl,
      activatorRef,
      activatorEvents,
      closeConditional,
      contentEl,
      contentEvents,
      contentStyles,
      dimensionStyles,
      target,
      targetRef,
      teleportTarget,
      top,
      root,
      themeClasses,
      rtlClasses,
      stackStyles,
      scopeId,
      Scrim,
      scrimColor,
      scrimEl,
      scrimEvents,
      onAfterEnter,
      onAfterLeave,
      onClickOutside,
    }
  }
})
</script>

<template>
<slot
  name="activator"
  v-bind="{
    isActive,
    targetRef,
    props: mergeProps({
    ref: activatorRef
    }, activatorEvents, $props.activatorProps,
    )
  }"
/>

<template v-if="isMounted && hasContent">
  <Teleport
    :disabled="!teleportTarget"
    :to="teleportTarget"
  >
    <div
      :class="[
        'base-overlay',
        {
          'base-overlay--absolute': $props.absolute || $props.contained,
          'base-overlay--active': isActive,
          'base-overlay--contained': $props.contained,
        },
        themeClasses,
        rtlClasses,
        $props.class,
      ]"
      :style="[
        stackStyles,
        {
          '--base-overlay-opacity': $props.opacity,
          top: convertToUnit(top),
        },
        $props.style,
      ]"
      ref="root"
      v-bind="{...scopeId, ...$attrs}"
    >
      <component
        :is="Scrim"
        :color="scrimColor"
        :modelValue="isActive && !!$props.scrim"
        ref="scrimEl"
        v-bind="{...scrimEvents}"
      />
      <MaybeTransition
        appear
        persisted
        :transition="$props.transition"
        :target="target"
        :onAfterEnter="onAfterEnter"
        :onAfterLeave="onAfterLeave"
      >
        <div
          ref="contentEl"
          v-show="isActive"
          v-click-outside="{ handler: onClickOutside, closeConditional, include: () => [activatorEl] }"
          :class="[
            'base-overlay__content',
            $props.contentClass,
          ]"
          :style="[
            dimensionStyles,
            contentStyles,
          ]"
          v-bind="{ ...contentEvents, ...$props.contentProps }"
        >
          <slot v-bind="{ isActive }"/>
        </div>
      </MaybeTransition>
    </div>
  </Teleport>
</template>
</template>
