<script lang="ts">
// Composables
import { useComponentProps } from '@/apps/visagiste/composables/component'
import { createForm, useFormProps } from '@/apps/visagiste/composables/form'

// Utilities
import { ref } from 'vue'
import { defineComponent, propsFactory } from '@/apps/visagiste/utils'

// Types
import type { SubmitEventPromise } from '@/apps/visagiste/composables/form'

export const useBaseFormProps = propsFactory(
  {
    ...useComponentProps(),
    ...useFormProps(),
  },
  'BaseForm'
)

export default defineComponent({
  name: 'BaseForm',
  props: useBaseFormProps(),
  emits: {
    'update:modelValue': (val: boolean | null) => true,
    submit: (e: SubmitEventPromise) => true,
  },
  setup(props, { emit }) {
    const form = createForm(props)
    const formRef = ref<HTMLFormElement>()

    function onReset(e: Event) {
      e.preventDefault()
      form.reset()
    }

    function onSubmit(_e: Event) {
      const e = _e as SubmitEventPromise

      const ready = form.validate()
      e.then = ready.then.bind(ready)
      e.catch = ready.catch.bind(ready)
      e.finally = ready.finally.bind(ready)

      emit('submit', e)

      if (!e.defaultPrevented) {
        ready.then(({ valid }) => {
          if (valid) {
            formRef.value?.submit()
          }
        })
      }

      e.preventDefault()
    }

    return {
      form,
      formRef,
      onReset,
      onSubmit,
    }
  },
})
</script>

<template>
  <form
    ref="formRef"
    :class="['base-form', $props.class]"
    :style="$props.style"
    novalidate
    @reset="onReset"
    @submit="onSubmit"
  >
    <slot v-bind="form" />
  </form>
</template>
