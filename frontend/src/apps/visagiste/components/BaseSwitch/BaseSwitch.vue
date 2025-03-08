<script lang="ts">
// Styles
import './BaseSwitch.scss'

// Components
import {
  BaseInput,
  useBaseInputProps,
} from '@/apps/visagiste/components/BaseInput'
import {
  BaseSelectionControl,
  useBaseSelectionControlProps,
} from '@/apps/visagiste/components/BaseSelectionControl'
import BaseDefaultsProvider from '@/apps/visagiste/components/BaseDefaultsProvider/BaseDefaultsProvider.vue'
import BaseIcon from '@/apps/visagiste/components/BaseIcon/BaseIcon.vue'
import BaseProgressCircular from '@/apps/visagiste/components/BaseProgressCircular/BaseProgressCircular.vue'
import { BaseScaleTransition } from '@/apps/visagiste/components/transitions'

// Composables
import LoaderSlot, {
  useLoader,
} from '@/apps/visagiste/composablesV2/loader.vue'

// Utilities
import {
  defineComponent,
  filterInputAttrs,
  getUid,
  IN_BROWSER,
  propsFactory,
} from '@/apps/visagiste/utils'

// Types
import type { ComputedRef, Ref } from 'vue'
import type { IconValue } from '@/apps/visagiste/composables/icons'
import type { BaseInputSlots } from '@/apps/visagiste/components/BaseInput/BaseInput.vue'
import type { BaseSelectionControlSlots } from '@/apps/visagiste/components/BaseSelectionControl/BaseSelectionControl.vue'
import type { LoaderSlotProps } from '@/apps/visagiste/composablesV2/loader.vue'
import { useProxiedModel } from '@/apps/visagiste/composables/proxiedModel'
import { useFocus } from '@/apps/visagiste/composables/focus'
import { computed, ref } from 'vue'

export type BaseSwitchSlot = {
  model: Ref<boolean>
  isValid: ComputedRef<boolean | null>
}

export type BaseSwitchSlots = BaseInputSlots &
  BaseSelectionControlSlots & {
    loader: LoaderSlotProps
    thumb: { icon: IconValue | undefined } & BaseSwitchSlot
    'track-false': BaseSwitchSlot
    'track-true': BaseSwitchSlot
  }

export const useBaseSwitchProps = propsFactory(
  {
    indeterminate: Boolean,
    inset: Boolean,
    flat: Boolean,
    loading: {
      type: [Boolean, String],
      default: false,
    },

    ...useBaseInputProps(),
    ...useBaseSelectionControlProps(),
  },
  'BaseSwitch'
)

export default defineComponent({
  name: 'BaseSwitch',
  inheritAttrs: false,
  props: useBaseSwitchProps(),
  emits: {
    'update:focused': (focused: boolean) => true,
    'update:modelValue': (value: any) => true,
    'update:indeterminate': (value: boolean) => true,
  },
  components: {
    BaseProgressCircular,
    BaseScaleTransition,
    LoaderSlot,
    BaseIcon,
    BaseDefaultsProvider,
    BaseSelectionControl,
    BaseInput,
  },
  setup(props, { attrs }) {
    const indeterminate = useProxiedModel(props, 'indeterminate')
    const model = useProxiedModel(props, 'modelValue')
    const { loaderClasses } = useLoader(props)
    const { isFocused, focus, blur } = useFocus(props)
    const control = ref<InstanceType<typeof BaseSelectionControl>>()
    const isForcedColorsModeActive =
      IN_BROWSER && window.matchMedia('(forced-colors: active)').matches

    const loaderColor = computed(() => {
      return typeof props.loading === 'string' && props.loading !== ''
        ? props.loading
        : props.color
    })

    const uid = getUid()
    const id = computed(() => props.id || `switch-${uid}`)

    function onChange() {
      if (indeterminate.value) {
        indeterminate.value = false
      }
    }
    function onTrackClick(e: Event) {
      e.stopPropagation()
      e.preventDefault()
      control.value?.input?.click()
    }

    const { rootAttrs, controlAttrs } = computed(() => {
      const [root, control] = filterInputAttrs(attrs)
      return { rootAttrs: root, controlAttrs: control }
    }).value
    const inputProps = computed(() => BaseInput.filterProps(props))
    const controlProps = computed(() => BaseSelectionControl.filterProps(props))

    return {
      id,
      control,
      indeterminate,
      model,
      rootAttrs,
      controlAttrs,
      inputProps,
      controlProps,
      loaderClasses,
      loaderColor,
      isForcedColorsModeActive,
      isFocused,
      focus,
      blur,
      onChange,
      onTrackClick,
    }
  },
})
</script>

<template>
  <BaseInput
    :class="[
      'base-switch',
      {
        'base-switch--flat': $props.flat,
        'base-switch--inset': $props.inset,
        'base-switch--indeterminate': indeterminate,
      },
      loaderClasses,
      $props.class,
    ]"
    v-bind="{ ...rootAttrs, ...inputProps }"
    v-model="model"
    :id="id"
    :focused="isFocused"
    :style="$props.style"
  >
    <template #prepend><slot name="prepend" /></template>
    <template #append><slot name="append" /></template>
    <template #details><slot name="details" /></template>
    <template #message><slot name="message" /></template>

    <template #default="{ id, messagesId, isDisabled, isReadonly, isValid }">
      <BaseSelectionControl
        ref="control"
        v-bind="{ ...controlProps, ...controlAttrs }"
        v-model="model"
        :id="id.value"
        :aria-describedby="messagesId.value"
        type="checkbox"
        :onUpdate:modelValue="onChange"
        :aria-checked="indeterminate ? 'mixed' : undefined"
        :disabled="isDisabled.value"
        :readonly="isReadonly.value"
        :onFocus="focus"
        :onBlur="blur"
      >
        <template #label><slot name="label" /></template>

        <template #default="{ backgroundColorClasses, backgroundColorStyles }">
          <div
            :class="[
              'base-switch__track',
              !isForcedColorsModeActive ? backgroundColorClasses : undefined,
            ]"
            :style="backgroundColorStyles"
            @click="onTrackClick"
          >
            <div
              v-if="$slots['track-true']"
              key="prepend"
              class="base-switch__track-true"
            >
              <slot name="track-true" :model="model" :isValid="isValid" />
            </div>

            <div
              v-if="$slots['track-false']"
              key="append"
              class="base-switch__track-false"
            >
              <slot name="track-false" :model="model" :isValid="isValid" />
            </div>
          </div>
        </template>

        <template
          #input="{
            inputNode,
            icon,
            backgroundColorClasses,
            backgroundColorStyles,
          }"
        >
          <component :is="inputNode" />

          <div
            :class="[
              'base-switch__thumb',
              { 'base-switch__thumb--filled': icon || $props.loading },
              $props.inset || isForcedColorsModeActive
                ? undefined
                : backgroundColorClasses,
            ]"
            :style="$props.inset ? undefined : backgroundColorStyles"
          >
            <BaseDefaultsProvider
              v-if="$slots.thumb"
              :defaults="{
                BaseIcon: {
                  icon,
                  size: 'x-small',
                },
              }"
            >
              <slot name="thumb" v-bind="{ model, isValid, icon }" />
            </BaseDefaultsProvider>

            <BaseScaleTransition v-else>
              <template v-if="!$props.loading">
                <BaseIcon
                  v-if="icon"
                  :icon="icon"
                  :key="String(icon)"
                  size="x-small"
                />
              </template>

              <LoaderSlot
                v-else
                name="base-switch"
                active
                :color="isValid.value === false ? undefined : loaderColor"
              >
                <template #default="{ isActive, color }">
                  <slot name="loader" :isActive="isActive" :color="color">
                    <BaseProgressCircular
                      :active="isActive"
                      :color="color"
                      indeterminate
                      size="16"
                      width="2"
                    />
                  </slot>
                </template>
              </LoaderSlot>
            </BaseScaleTransition>
          </div>
        </template>
      </BaseSelectionControl>
    </template>
  </BaseInput>
</template>
