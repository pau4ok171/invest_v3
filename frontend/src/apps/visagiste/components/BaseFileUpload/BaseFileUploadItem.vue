<script lang="ts">
// Components
import {
  BaseListItem,
  useBaseListItemProps,
} from '@/apps/visagiste/components/BaseList'
import { BaseDefaultsProvider } from '@/apps/visagiste/components/BaseDefaultsProvider'
import { BaseAvatar } from '@/apps/visagiste/components/BaseAvatar'
import { BaseButton } from '@/apps/visagiste/components/BaseButton'

// Utilities
import { computed, ref, watchEffect } from 'vue'
import {
  defineComponent,
  humanReadableFileSize,
  propsFactory,
} from '@/apps/visagiste/utils'

// Types
import type { PropType } from 'vue'
import type { BaseListItemSlots } from '@/apps/visagiste/components/BaseList/BaseListItem.vue'
import {useSlotIsEmpty} from "@/apps/visagiste/composables/slotIsEmpty";

export type BaseFileUploadItemSlots = {
  clear: {
    props: { onClick: () => void }
  }
} & BaseListItemSlots

export const useBaseFileUploadItemProps = propsFactory(
  {
    clearable: Boolean,
    file: {
      type: Object as PropType<File>,
      default: null,
    },
    fileIcon: {
      type: String,
      default: '$upload',
    },
    showSize: Boolean,

    ...useBaseListItemProps({
      border: true,
      rounded: true,
      lines: 'two' as const,
    }),
  },
  'BaseFileUploadItem'
)

export default defineComponent({
  name: 'BaseFileUploadItem',
  methods: { humanReadableFileSize },
  components: { BaseButton, BaseAvatar, BaseDefaultsProvider, BaseListItem },
  props: useBaseFileUploadItemProps(),
  emits: {
    'click:remove': () => true,
    click: (e: MouseEvent | KeyboardEvent) => true,
  },
  setup(props, { emit }) {
    const preview = ref()
    const base = computed(() =>
      typeof props.showSize !== 'boolean' ? props.showSize : undefined
    )

    function onClickRemove() {
      emit('click:remove')
    }

    watchEffect(() => {
      preview.value = props.file?.type.startsWith('image')
        ? URL.createObjectURL(props.file)
        : undefined
    })

    const listItemProps = computed(() => BaseListItem.filterProps(props))

    const prependIsEmpty = useSlotIsEmpty('prepend')
    const clearIsEmpty = useSlotIsEmpty('clear')
    const hasPrepend = computed(() => !prependIsEmpty.value)
    const hasClear = computed(() => !clearIsEmpty.value)

    return {
      hasPrepend,
      hasClear,
      listItemProps,
      preview,
      base,
      onClickRemove,
    }
  },
})
</script>

<template>
  <BaseListItem
    v-bind="listItemProps"
    :title="$props.title ?? $props.file?.name"
    :subtitle="
      $props.showSize
        ? humanReadableFileSize($props.file?.size as number, base)
        : $props.file?.type
    "
    class="base-file-upload-item"
  >
    <template #prepend="slotProps">
      <BaseDefaultsProvider
        v-if="hasPrepend"
        :defaults="{
          BaseAvatar: {
            image: preview,
            icon: !preview ? $props.fileIcon : undefined,
            rounded: true,
          },
        }"
      >
        <slot name="prepend" v-bind="slotProps" />
      </BaseDefaultsProvider>

      <BaseAvatar v-else :icon="$props.fileIcon" :image="preview" rounded />
    </template>

    <template #append="slotProps">
      <template v-if="$props.clearable">
        <BaseDefaultsProvider
          v-if="hasClear"
          :defaults="{
            BaseButton: {
              icon: '$clear',
              density: 'comfortable',
              variant: 'text',
            },
          }"
        >
          <slot
            name="clear"
            v-bind="{ ...slotProps, props: { onClick: onClickRemove } }"
          />
        </BaseDefaultsProvider>

        <BaseButton
          v-else
          icon="$clear"
          density="comfortable"
          variant="text"
          :onClick="onClickRemove"
        />
      </template>
      <slot name="append" v-bind="slotProps" />
    </template>
  </BaseListItem>
</template>
