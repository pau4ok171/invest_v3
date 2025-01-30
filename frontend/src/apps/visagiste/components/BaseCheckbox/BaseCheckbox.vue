<script lang="ts">
// Styles
import './BaseCheckbox.scss';

// Components
import BaseCheckboxButton, { useBaseCheckboxButtonProps } from './BaseCheckboxButton.vue';
import BaseInput, {useBaseInputProps} from "../BaseInput/BaseInput.vue";

// Composables
import {useFocus} from "@/apps/visagiste/composables/focus";
import {useProxiedModel} from "@/apps/visagiste/composables/proxiedModel";

// Utilities
import {computed} from "vue";
import {defineComponent, filterInputAttrs, getUid, omit, propsFactory} from "@/apps/visagiste/utils";

// Types
import type { SlotsType } from 'vue';
import type {BaseSelectionControlSlots} from "../BaseSelectionControl/BaseSelectionControl.vue";
import type { BaseInputSlots } from "../BaseInput/BaseInput.vue";

export type BaseCheckboxSlots = Omit<BaseInputSlots, 'default'> & BaseSelectionControlSlots

export const useBaseCheckboxProps = propsFactory({
  ...useBaseInputProps(),
  ...omit(useBaseCheckboxButtonProps(), ['inline']),
}, 'BaseCheckbox')

export default defineComponent({
  name: "BaseCheckbox",
  slots: Object as SlotsType<BaseCheckboxSlots>,
  components: {
    BaseCheckboxButton,
    BaseInput
  },
  inheritAttrs: false,
  props: useBaseCheckboxProps(),
  emits: {
    'update:modelValue': (value: any) => true,
    'update:focused': (value: any) => true,
  },
  setup (props, { attrs }) {
    const model = useProxiedModel(props, 'modelValue')
    const { isFocused, focus, blur } = useFocus(props)

    const uid = getUid()
    const id = computed(() => props.id || `checkbox-${uid}`)

    const [rootAttrs, controlAttrs] = filterInputAttrs(attrs)
    const inputProps = computed(() => BaseInput.filterProps(props))
    const checkboxProps = computed(() => BaseCheckboxButton.filterProps(props))

    return {
      model,
      isFocused,
      focus,
      blur,
      id,
      rootAttrs,
      controlAttrs,
      inputProps,
      checkboxProps,
    }
  }
})
</script>

<template>
<BaseInput
  :class="[
    'base-checkbox',
    $props.class
  ]"
  v-bind="{...rootAttrs, ...inputProps}"
  v-model="model"
  :id="id"
  :focused="isFocused"
  :stype="$props.style"
>
  <template #default="{ id, messagesId, isDisabled, isReadonly, isValid }">
    <BaseCheckboxButton
      v-model="model"
      v-bind="{...checkboxProps, ...controlAttrs}"
      :id="id.value"
      :aria-describedby="messagesId.value"
      :disabled="isDisabled.value"
      :readonly="isReadonly.value"
      :error="isValid.value === false"
      @focus="focus"
      @blur="blur"
    >
      <slot name="default"/>

      <template #input>
        <slot name="input"/>
      </template>

      <template #label>
        <slot name="label"/>
      </template>
    </BaseCheckboxButton>
  </template>

  <template #prepend>
    <slot name="prepend"/>
  </template>

  <template #append>
    <slot name="append"/>
  </template>

  <template #details>
    <slot name="details"/>
  </template>

  <template #message>
    <slot name="message"/>
  </template>
</BaseInput>
</template>
