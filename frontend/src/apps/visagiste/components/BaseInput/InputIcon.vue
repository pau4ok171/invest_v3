<script lang="ts">
// Components
import { BaseIcon } from "@/apps/visagiste/components/BaseIcon";

// Composables
import { useLocale } from '@/apps/visagiste/composables/locale';

// Utilities
import { callEvent } from '@/apps/visagiste/utils'

// Types
import type { IconValue } from "@/apps/visagiste/composables/icons";
import type { EventProp } from "@/apps/visagiste/utils";
import {h} from "vue";

type names = 'clear' | 'prepend' | 'append' | 'appendInner' | 'prependInner'

type InputIconProps<T extends names> = {
  label: string | undefined
} & {
  [K in `${T}Icon`]: IconValue | undefined
} & {
  [K in `onClick:${T}`]: EventProp | undefined
}

type Listeners<T extends {}, U = keyof T> = U extends `onClick:${infer V extends names}` ? V : never

export function useInputIcon<T extends {}, K extends names = Listeners<T>> (props: T & InputIconProps<K>) {
  const { t } = useLocale()

  function InputIcon ({ name }: { name: Extract<names, K> }) {
    const localeKey = {
      prepend: 'prependAction',
      prependInner: 'prependAction',
      append: 'appendAction',
      appendInner: 'appendAction',
      clear: 'clear',
    }[name]
    const listener = props[`onClick:${name}`] as EventProp | undefined

    function onKeydown (e: KeyboardEvent) {
      if (e.key !== 'Enter' && e.key !== ' ') return

      e.preventDefault()
      e.stopPropagation()
      callEvent(listener, new PointerEvent('click', e))
    }

    const label = listener && localeKey
      ? t(`$visagiste.input.${localeKey}`, props.label ?? '')
      : undefined

    return () => h(BaseIcon, {
      icon: props[`${name}Icon`],
      'aria-label': label,
      onClick: listener,
      onKeydown: onKeydown
    })
  }

  return { InputIcon }
}
</script>

