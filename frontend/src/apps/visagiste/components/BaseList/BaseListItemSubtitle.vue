<script lang="ts">
// Composables
import {useTagProps} from "@/apps/visagiste/composables/tag";
import {useComponentProps} from "@/apps/visagiste/composables/component";

// Utilities
import {h} from "vue";
import {defineComponent, propsFactory} from '@/apps/visagiste/utils'

export const useBaseListItemSubtitle = propsFactory({
  opacity: [Number, String],

  ...useComponentProps(),
  ...useTagProps(),
}, 'BaseListItemSubtitle')

export default defineComponent({
  name: "BaseListItemSubtitle",
  props: useBaseListItemSubtitle(),
  setup (props, { slots }) {
    return () => h(props.tag, {
      class: ['base-list-item-subtitle', props.class],
      style: [
        {'--base-list-item-subtitle-opacity': props.opacity},
        props.style
      ],
    }, slots.default?.())
  }
})
</script>

<template>

</template>
