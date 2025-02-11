<script lang="ts">
// Styles
import './BaseMenu.scss';

// Components
import { useBaseOverlayProps } from '../BaseOverlay/BaseOverlay.vue'
import BaseDialogTransition from '../transitions/dialog-transition'
import BaseOverlay from "@/apps/visagiste/components/BaseOverlay/BaseOverlay.vue";
import BaseDefaultsProvider from "@/apps/visagiste/components/BaseDefaultsProvider/BaseDefaultsProvider.vue";

// Composables
import {useProxiedModel} from "@/apps/visagiste/composables/proxiedModel";
import {useScopeId} from "@/apps/visagiste/composables/scopeId";
import {useRtl} from "@/apps/visagiste/composables";

// Utilities
import {
  computed,
  h,
  inject,
  mergeProps,
  nextTick,
  onBeforeUnmount,
  onDeactivated,
  provide,
  ref,
  shallowRef,
  watch
} from "vue";
import {BaseMenuSymbol} from "@/apps/visagiste/components/BaseMenu/shared";
import {
  defineComponent,
  focusableChildren,
  focusChild,
  getNextElement,
  getUid,
  IN_BROWSER,
  isClickInsideElement,
  omit,
  propsFactory
} from '@/apps/visagiste/utils';

// Types
import type {Component} from "vue";


export const useBaseMenuProps = propsFactory({
  // TODO
  // disableKeys: Boolean,
  id: String,
  submenu: Boolean,

  ...omit(useBaseOverlayProps({
    closeDelay: 250,
    closeOnContentClick: true,
    locationStrategy: 'connected' as const,
    location: undefined,
    openDelay: 300,
    scrim: false,
    scrollStrategy: 'reposition' as const,
    transition: { component: BaseDialogTransition as Component },
  }), ['absolute']),
}, 'BaseMenu')

export default defineComponent({
  name: "BaseMenu",
  props: useBaseMenuProps(),
  emits: {
    'update:modelValue': (value: boolean) => true,
  },
  setup (props, { slots }) {
    const isActive = useProxiedModel(props, 'modelValue')
    const { scopeId } = useScopeId()
    const { isRtl } = useRtl()

    const uid = getUid()
    const id = computed(() => props.id || `base-menu-${uid}`)

    const overlay = ref<BaseOverlay>()

    const parent = inject(BaseMenuSymbol, null)
    const openChildren = shallowRef(new Set<number>())
    provide(BaseMenuSymbol, {
      register() {
        openChildren.value.add(uid)
      },
      unregister() {
        openChildren.value.delete(uid)
      },
      closeParents(e?: MouseEvent) {
        setTimeout(() => {
          if (!openChildren.value.size &&
          !props.persistent &&
          (e == null || (overlay.value?.contentEl && !isClickInsideElement(e, overlay.value.contentEl)))
          ) {
            isActive.value = false
            parent?.closeParents()
          }
        }, 40)
      },
    })

    onBeforeUnmount(() => {
      parent?.unregister()
      document.removeEventListener('focusin', onFocusIn)
    })
    onDeactivated(() => isActive.value = false)

    async function onFocusIn (e: FocusEvent) {
      const before = e.relatedTarget as HTMLElement | null
      const after = e.target as HTMLElement | null

      await nextTick()

      if (
        isActive.value &&
        before !== after &&
        overlay.value?.contentEl &&
        // We're the topmost menu
        overlay.value?.globalTop &&
        // It isn't the document or the menu body
        ![document, overlay.value.contentEl].includes(after!) &&
        // It isn't inside the menu body
        !overlay.value.contentEl.contains(after)
      ) {
        const focusable = focusableChildren(overlay.value.contentEl)
        focusable[0]?.focus()
      }
    }

    watch(isActive, val => {
      if (val) {
        parent?.register()
        if (IN_BROWSER) {
          document.addEventListener('focusin', onFocusIn, { once: true })
        }
      } else {
        parent?.unregister()
        if (IN_BROWSER) {
          document.removeEventListener('focusin', onFocusIn)
        }
      }
    }, { immediate: true })

    function onClickOutside (e: MouseEvent) {
      parent?.closeParents(e)
    }

    function onKeydown (e: KeyboardEvent) {
      if (props.disabled) return

      if (e.key === 'Tab' || (e.key === 'Enter' && !props.closeOnContentClick)) {
        if (
          e.key === 'Enter' &&
          ((e.target instanceof HTMLTextAreaElement) ||
          (e.target instanceof HTMLInputElement && !!e.target.closest('form')))
        ) return
        if (e.key === 'Enter') e.preventDefault()

        const nextElement = getNextElement(
          focusableChildren(overlay.value?.contentEl as Element, false),
          e.shiftKey ? 'prev' : 'next',
          (el: HTMLElement) => el.tabIndex >= 0
        )
        if (!nextElement) {
          isActive.value = false
          overlay.value?.activatorEl?.focus()
        }
      } else if (props.submenu && e.key === (isRtl.value ? 'ArrowRight' : 'ArrowLeft')) {
        isActive.value = false
        overlay.value?.activatorEl?.focus()
      }
    }

    function onActivatorKeydown (e: KeyboardEvent) {
      if (props.disabled) return

      const el = overlay.value?.contentEl
      if (el && isActive.value) {
        if (e.key === 'ArrowDown') {
          e.preventDefault()
          e.stopImmediatePropagation()
          focusChild(el, 'next')
        } else if (e.key === 'ArrowUp') {
          e.preventDefault()
          e.stopImmediatePropagation()
          focusChild(el, 'prev')
        } else if (props.submenu) {
          if (e.key === (isRtl ? 'ArrowRight' : 'ArrowLeft')) {
            isActive.value = false
          } else if (e.key === (isRtl ? 'ArrowLeft' : 'ArrowRight')) {
            e.preventDefault()
            focusChild(el, 'first')
          }
        }
      } else if (
        props.submenu
          ? e.key === (isRtl ? 'ArrowLeft' : 'ArrowRight')
          : ['ArrowDown', 'ArrowUp'].includes(e.key)
      ) {
        isActive.value = true
        e.preventDefault()
        setTimeout(() => setTimeout(() => onActivatorKeydown(e)))
      }
    }

    const activatorProps = computed(() =>
      mergeProps({
        'aria-haspopup': 'menu',
        'aria-expanded': String(isActive.value),
        'aria-controls': id.value,
      }, props.activatorProps)
    )

    return () => {
      const overlayProps = BaseOverlay.filterProps(props)

      return h(
        BaseOverlay,
        {
          ref: overlay,
          id: id.value,
          class: ['base-menu', props.class],
          style: props.style,
          ...overlayProps,
          modelValue: isActive.value,
          'onUpdate:modelValue': (value: boolean) => isActive.value = value,
          absolute: true,
          activatorProps: activatorProps.value,
          location: props.location ?? (props.submenu ? 'end' : 'bottom'),
          'onClick:outside': onClickOutside,
          onKeydown: onKeydown,
          ...scopeId,
        },
        {
          activator: slots.activator,
          default: (...args: any[]) => h(
            BaseDefaultsProvider,
            {
              root: 'BaseMenu'
            },
            {
              default: () => slots.default?.(...args)
            }
          )
        }
      )
    }
  },
})
</script>

