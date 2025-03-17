<script lang="ts">
// Styles
import "./BaseDialog.scss";

// Components
import { BaseDialogTransition } from "@/apps/visagiste/components/transitions";
import { BaseDefaultsProvider } from "@/apps/visagiste/components/BaseDefaultsProvider";
import { BaseOverlay } from "@/apps/visagiste/components/BaseOverlay";
import { useBaseOverlayProps } from "@/apps/visagiste/components/BaseOverlay";

// Composables
import { useProxiedModel } from "@/apps/visagiste/composables/proxiedModel";
import { useScopeId } from "@/apps/visagiste/composables/scopeId";

// Utilities
import {
  computed,
  mergeProps,
  nextTick,
  onBeforeUnmount,
  ref,
  watch,
} from "vue";
import {
  defineComponent,
  focusableChildren,
  IN_BROWSER,
  propsFactory,
} from "@/apps/visagiste/utils";

// Types
import type { Component } from "vue";

export const useBaseDialogProps = propsFactory(
  {
    fullscreen: Boolean,
    retainFocus: {
      type: Boolean,
      default: true,
    },
    scrollable: Boolean,

    ...useBaseOverlayProps({
      origin: "center center" as const,
      scrollStrategy: "block" as const,
      transition: { component: BaseDialogTransition as Component },
      zIndex: 2400,
    }),
  },
  "BaseDialog",
);

export default defineComponent({
  name: "BaseDialog",
  components: { BaseDefaultsProvider, BaseOverlay },
  props: useBaseDialogProps(),
  emits: {
    "update:modelValue": (value: boolean) => true,
    afterEnter: () => true,
    afterLeave: () => true,
  },
  setup(props, { emit }) {
    const isActive = useProxiedModel(props, "modelValue");
    const { scopeId } = useScopeId();

    const overlay = ref<InstanceType<typeof BaseOverlay>>();
    function onFocusin(e: FocusEvent) {
      const before = e.relatedTarget as HTMLElement | null;
      const after = e.target as HTMLElement | null;

      if (
        before !== after &&
        overlay.value?.contentEl &&
        // We're the topmost dialog
        overlay.value?.globalTop &&
        // It isn't the document or the dialog body
        ![document, overlay.value.contentEl].includes(after!) &&
        // It isn't inside the dialog body
        !overlay.value.contentEl.contains(after)
      ) {
        const focusable = focusableChildren(overlay.value.contentEl);

        if (!focusable.length) return;

        const firstElement = focusable[0];
        const lastElement = focusable[focusable.length - 1];

        if (before === firstElement) {
          lastElement.focus();
        } else {
          firstElement.focus();
        }
      }
    }

    onBeforeUnmount(() => {
      document.removeEventListener("focusin", onFocusin);
    });

    if (IN_BROWSER) {
      watch(
        () => isActive.value && props.retainFocus,
        (val) => {
          val
            ? document.addEventListener("focusin", onFocusin)
            : document.removeEventListener("focusin", onFocusin);
        },
        { immediate: true },
      );
    }

    function onAfterEnter() {
      emit("afterEnter");
      if (
        overlay.value?.contentEl &&
        !overlay.value.contentEl.contains(document.activeElement)
      ) {
        overlay.value.contentEl.focus({ preventScroll: true });
      }
    }

    function onAfterLeave() {
      emit("afterLeave");
    }

    watch(isActive, async (val) => {
      if (!val) {
        await nextTick();
        overlay.value!.activatorEl?.focus({ preventScroll: true });
      }
    });

    const overlayProps = computed(() => BaseOverlay.filterProps(props));
    const activatorProps = computed(() =>
      mergeProps(
        {
          "aria-haspopup": "dialog",
        },
        props.activatorProps,
      ),
    );
    const contentProps = computed(() =>
      mergeProps(
        {
          tabindex: -1,
        },
        props.contentProps,
      ),
    );

    return {
      overlay,
      overlayProps,
      activatorProps,
      contentProps,
      scopeId,
      isActive,
      onAfterEnter,
      onAfterLeave,
    };
  },
});
</script>

<template>
  <BaseOverlay
    ref="overlay"
    :class="[
      'base-dialog',
      {
        'base-dialog--fullscreen': $props.fullscreen,
        'base-dialog--scrollable': $props.scrollable,
      },
      $props.class,
    ]"
    :style="$props.style"
    v-bind="{ ...overlayProps, ...scopeId }"
    v-model="isActive"
    aria-modal="true"
    :activator-props="activatorProps"
    :content-props="contentProps"
    :height="!$props.fullscreen ? $props.height : undefined"
    :width="!$props.fullscreen ? $props.width : undefined"
    :max-height="!$props.fullscreen ? $props.maxHeight : undefined"
    :max-width="!$props.fullscreen ? $props.maxWidth : undefined"
    role="dialog"
    :onAfterEnter="onAfterEnter"
    :onAfterLeave="onAfterLeave"
  >
    <template #activator="{ ...args }">
      <slot name="activator" v-bind="{ ...args }"/>
    </template>
    <template #default="{ ...args }">
      <BaseDefaultsProvider root="BaseDialog">
        <slot name="default" v-bind="{ ...args }" />
      </BaseDefaultsProvider>
    </template>
  </BaseOverlay>
</template>