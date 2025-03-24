// Utilities
import {propsFactory} from "@/apps/visagiste/utils";

// Types
export interface TagProps {
  tag: string
}

// Composables
export const useTagProps = propsFactory({
  tag: {
    type: String,
    default: 'div'
  },
}, 'tag')