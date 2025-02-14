<script lang="ts">
// Components
import BaseLabel from "@/apps/visagiste/components/BaseLabel/BaseLabel.vue";

// Composables
import { useComponentProps } from "@/apps/visagiste/composables/component";

// Utilities
import { h } from "vue";
import { defineComponent, propsFactory } from "@/apps/visagiste/utils";

export const useBaseFieldLabelProps = propsFactory(
  {
    floating: Boolean,

    ...useComponentProps(),
  },
  "BaseFieldLabel",
);

export default defineComponent({
  name: "BaseFieldLabel",
  props: useBaseFieldLabelProps(),
  setup(props, { slots }) {
    return () =>
      h(
        BaseLabel,
        {
          class: [
            "base-field-label",
            {
              "base-field-label--floating": props.floating,
            },
            props.class,
          ],
          style: props.style,
          "aria-hidden": props.floating || undefined,
        },
        slots.default,
      );
  },
});
</script>
