<script lang="ts">
// Styles
import './BaseFileUpload.scss'

// Components
import BaseFileUploadItem from './BaseFileUploadItem.vue'
import { useBaseDividerProps } from '@/apps/visagiste/components/BaseDivider'
import {
  BaseCard,
  useBaseCardProps,
} from '@/apps/visagiste/components/BaseCard'
import { BaseDefaultsProvider } from '@/apps/visagiste/components/BaseDefaultsProvider'
import { BaseIcon } from '@/apps/visagiste/components/BaseIcon'
import { BaseDivider } from '@/apps/visagiste/components/BaseDivider'
import { BaseButton } from '@/apps/visagiste/components/BaseButton'
import { BaseOverlay } from '@/apps/visagiste/components/BaseOverlay'

// Composables
import { IconValue } from '@/apps/visagiste/composables/icons'
import { useDelayProps } from '@/apps/visagiste/composables/delay'
import {
  useDensity,
  useDensityProps,
} from '@/apps/visagiste/composables/density'
import { useLocale } from '@/apps/visagiste/composables'
import { useProxiedModel } from '@/apps/visagiste/composables/proxiedModel'
import { useSlotIsEmpty } from '@/apps/visagiste/composables/slotIsEmpty'

// Utilities
import { computed, h, onMounted, onUnmounted, ref, shallowRef } from 'vue'
import {
  defineComponent,
  filterInputAttrs,
  omit,
  pick,
  propsFactory,
  wrapInArray,
} from '@/apps/visagiste/utils'

// Types
import type { PropType, VNode } from 'vue'

export type BaseFileUploadSlots = {
  browse: {
    props: { onClick: (e: MouseEvent) => void }
  }
  default: never
  icon: never
  input: {
    inputNode: VNode
  }
  item: {
    file: File
    props: { 'onClick:remover': () => void }
  }
  title: never
  divider: never
}

export const useBaseFileUploadProps = propsFactory(
  {
    browseText: {
      type: String,
      default: '$visagiste.fileUpload.browse',
    },
    dividerText: {
      type: String,
      default: '$visagiste.fileUpload.divider',
    },
    icon: {
      type: IconValue,
      default: '$upload',
    },
    modelValue: {
      type: [Array, Object] as PropType<File[] | File>,
      default: null,
      validator: (val: any) => {
        return wrapInArray(val).every((v) => v != null && typeof v === 'object')
      },
    },
    clearable: Boolean,
    disabled: Boolean,
    hideBrowse: Boolean,
    multiple: Boolean,
    scrim: {
      type: [Boolean, String],
      default: true,
    },
    showSize: Boolean,
    name: String,

    ...useDelayProps(),
    ...useDensityProps(),
    ...pick(
      useBaseDividerProps({
        length: 150,
      }),
      ['length', 'thickness', 'opacity']
    ),
    ...omit(
      useBaseCardProps({
        title: '$visagiste.fileUpload.title',
      }),
      ['disabled']
    ),
  },
  'BaseFileUpload'
)

export default defineComponent({
  name: 'BaseFileUpload',
  components: {
    BaseFileUploadItem,
    BaseOverlay,
    BaseButton,
    BaseDivider,
    BaseIcon,
    BaseDefaultsProvider,
    BaseCard,
  },
  inheritAttrs: false,
  props: useBaseFileUploadProps(),
  emits: {
    'update:modelValue': (files: File[]) => true,
  },
  setup(props, { attrs }) {
    const { t } = useLocale()
    const { densityClasses } = useDensity(props)
    const model = useProxiedModel(
      props,
      'modelValue',
      props.modelValue,
      (val) => wrapInArray(val),
      (val) =>
        props.multiple || Array.isArray(props.modelValue) ? val : val[0]
    )

    const dragOver = shallowRef(false)
    const baseCardRef = ref<InstanceType<typeof BaseCard> | null>(null)
    const inputRef = ref<HTMLInputElement | null>(null)

    onMounted(() => {
      baseCardRef.value?.$el.addEventListener('dragover', onDragOver)
      baseCardRef.value?.$el.addEventListener('drop', onDrop)
    })

    onUnmounted(() => {
      baseCardRef.value?.$el.removeEventListener('dragover', onDragOver)
      baseCardRef.value?.$el.removeEventListener('drop', onDrop)
    })

    function onDragOver(e: DragEvent) {
      e.preventDefault()
      e.stopImmediatePropagation()
      dragOver.value = true
    }

    function onDragLeave(e: DragEvent) {
      e.preventDefault()
      dragOver.value = false
    }

    function onDrop(e: DragEvent) {
      e.preventDefault()
      e.stopImmediatePropagation()
      dragOver.value = false

      const files = Array.from(e.dataTransfer?.files ?? [])

      if (!files.length) return

      if (!props.multiple) {
        model.value = [files[0]]

        return
      }

      const array = model.value.slice()

      for (const file of files) {
        if (!array.some((f) => f.name === file.name)) {
          array.push(file)
        }
      }

      model.value = array
    }

    function onClick() {
      inputRef.value?.click()
    }

    function onClickRemove(index: number) {
      const newValue = model.value.filter((_, i) => i !== index)
      model.value = newValue

      if (newValue.length > 0 || !inputRef.value) return

      inputRef.value.value = ''
    }

    const titleIsEmpty = useSlotIsEmpty('title')
    const iconIsEmpty = useSlotIsEmpty('icon')
    const browseIsEmpty = useSlotIsEmpty('browse')
    const hasTitle = computed(() => !titleIsEmpty.value || !!props.title)
    const hasIcon = computed(() => !iconIsEmpty.value || !!props.icon)
    const hasBrowse = computed(
      () =>
        !props.hideBrowse &&
        (!browseIsEmpty.value || props.density === 'default')
    )
    const cardProps = computed(() => BaseCard.filterProps(props))
    const dividerProps = computed(() => BaseDivider.filterProps(props))
    const { rootAttrs, inputAttrs } = computed(() => {
      const [root, input] = filterInputAttrs(attrs)
      return { rootAttrs: root, inputAttrs: input }
    }).value

    const inputNode = () =>
      h('input', {
        ref: inputRef,
        type: 'file',
        disabled: props.disabled,
        multiple: props.multiple,
        name: props.name,
        onChange: (e) => {
          if (!e.target) return

          const target = e.target as HTMLInputElement
          model.value = [...(target.files ?? [])]
        },
        ...inputAttrs,
      })

    return {
      baseCardRef,
      inputRef,
      inputNode,
      cardProps,
      dividerProps,
      rootAttrs,
      inputAttrs,
      t,
      model,
      dragOver,
      densityClasses,
      onDragOver,
      onDragLeave,
      onDrop,
      onClick,
      onClickRemove,
      hasTitle,
      hasIcon,
      hasBrowse,
    }
  },
})
</script>

<template>
  <BaseCard
    ref="baseCardRef"
    v-bind="{ ...cardProps, ...rootAttrs }"
    :class="[
      'base-file-upload',
      {
        'base-file-upload--clickable': !hasBrowse,
        'base-file-upload--disabled': $props.disabled,
        'base-file-upload--dragging': dragOver,
      },
      densityClasses,
    ]"
    :onDragleave="onDragLeave"
    :onDragover="onDragOver"
    :onDrop="onDrop"
    :onClick="!hasBrowse ? onClick : undefined"
    :title="undefined"
  >
    <div v-if="hasIcon" key="icon" class="base-file-upload-icon">
      <BaseDefaultsProvider
        v-if="$slots.icon"
        key="icon-defaults"
        :defaults="{
          BaseIcon: {
            icon: $props.icon,
          },
        }"
      >
        <slot name="icon" />
      </BaseDefaultsProvider>

      <BaseIcon v-else key="icon-icon" :icon="$props.icon" />
    </div>

    <div v-if="hasTitle" key="title" class="base-file-upload-title">
      <slot name="title">
        {{ t($props.title as string) }}
      </slot>
    </div>

    <template v-if="$props.density === 'default'">
      <div key="upload-divider" class="base-file-upload-divider">
        <slot name="divider">
          <BaseDivider v-bind="dividerProps">
            {{ t($props.dividerText as string) }}
          </BaseDivider>
        </slot>
      </div>

      <template v-if="hasBrowse">
        <BaseDefaultsProvider
          v-if="$slots.browse"
          :defaults="{
            BaseButton: {
              readonly: $props.disabled,
              size: 'large',
              text: t($props.browseText as string),
              variant: 'tonal',
            },
          }"
        >
          <slot name="browse" v-bind="{ props: { onClick } }" />
        </BaseDefaultsProvider>

        <BaseButton
          v-else
          :readonly="$props.disabled"
          size="large"
          :text="t($props.browseText as string)"
          variant="tonal"
          :onClick="onClick"
        />
      </template>

      <div v-if="$props.subtitle" class="base-file-upload-subtitle">
        {{ $props.subtitle as string }}
      </div>
    </template>

    <BaseOverlay :model-value="dragOver" contained :scrim="$props.scrim" />

    <slot name="input" v-bind="{ inputNode }">
      <component :is="inputNode" />
    </slot>
  </BaseCard>

  <template v-if="model.length > 0">
    <div class="base-file-upload-items">
      <BaseDefaultsProvider
        v-for="(file, i) in model"
        :key="i"
        :defaults="{
          BaseFileUploadItem: {
            file,
            clearable: $props.clearable,
            disabled: $props.disabled,
            showSize: $props.showSize,
          },
        }"
      >
        <slot
          name="item"
          v-bind="{ file, props: { 'onClick:remove': () => onClickRemove(i) } }"
        >
          <BaseFileUploadItem
            :file="file"
            :clearable="$props.clearable"
            :disabled="$props.disabled"
            :showSize="$props.showSize"
            :key="i"
            :onClick:remove="() => onClickRemove(i)"
          >
            <template #prepend><slot name="prepend"/></template>
            <template #append><slot name="append"/></template>
            <template #clear><slot name="clear"/></template>
          </BaseFileUploadItem>
        </slot>
      </BaseDefaultsProvider>
    </div>
  </template>
</template>