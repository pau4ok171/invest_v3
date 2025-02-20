<script lang="ts">
// Composables
import { useComponentProps } from "@/apps/visagiste/composables/component";
import { useTagProps } from "@/apps/visagiste/composables/tag";

// Utilities
import { defineComponent, propsFactory } from "@/apps/visagiste/utils";
import { h } from "vue";

export const useBaseCardTextProps = propsFactory(
  {
    opacity: [Number, String],

    ...useComponentProps(),
    ...useTagProps(),
  },
  "BaseCardText",
);

export default defineComponent({
  name: "BaseCardText",
  props: useBaseCardTextProps(),
  setup(props, { slots }) {
    return () =>
      h(
        props.tag,
        {
          class: ["base-card-text", props.class],
          style: [{ "--base-card-title-opacity": props.opacity }, props.style],
        },
        () => slots.default?.(),
      );
  },
});
</script>
