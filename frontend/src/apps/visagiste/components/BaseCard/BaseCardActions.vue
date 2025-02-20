<script lang="ts">
// Composables
import { useComponentProps } from "@/apps/visagiste/composables/component";
import { provideDefaults } from "@/apps/visagiste/composables/defaults";

// Utilities
import { h } from "vue";
import { defineComponent } from "@/apps/visagiste/utils";

export default defineComponent({
  name: "BaseCardActions",
  props: useComponentProps(),
  setup(props, { slots }) {
    provideDefaults({
      BaseButton: {
        slim: true,
        variant: "text",
      },
    });

    return () =>
      h(
        "div",
        {
          class: ["base-card-actions", props.class],
          style: props.style,
        },
        () => slots.default?.(),
      );
  },
});
</script>
