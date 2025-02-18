// Icons
import { aliases, mdi } from '@/apps/visagiste/iconsets/mdi'

// Utilities
import {computed, h, inject, unref} from "vue";
import {defineComponent, consoleWarn, mergeDeep, propsFactory} from "@/apps/visagiste/utils";

// Types
import type {ComponentPublicInstance, FunctionalComponent, InjectionKey, PropType, Ref} from "vue";

export type JSXComponent<Props = any> =
    | { new (): ComponentPublicInstance<Props> }
    | FunctionalComponent<Props>

export type IconValue =
  | string
  | (string | [path: string, opacity: number])[]
  | JSXComponent
export const IconValue = [String, Function, Object, Array] as PropType<IconValue>

export interface IconAliases {
  [name: string]: IconValue
  complete: IconValue
  cancel: IconValue
  close: IconValue
  delete: IconValue
  clear: IconValue
  success: IconValue
  info: IconValue
  warning: IconValue
  error: IconValue
  prev: IconValue
  next: IconValue
  checkboxOn: IconValue
  checkboxOff: IconValue
  checkboxIndeterminate: IconValue
  delimiter: IconValue
  sortAsc: IconValue
  sortDesc: IconValue
  expand: IconValue
  menu: IconValue
  subgroup: IconValue
  dropdown: IconValue
  radioOn: IconValue
  radioOff: IconValue
  edit: IconValue
  ratingEmpty: IconValue
  ratingFull: IconValue
  ratingHalf: IconValue
  loading: IconValue
  first: IconValue
  last: IconValue
  unfold: IconValue
  file: IconValue
  plus: IconValue
  minus: IconValue
  calendar: IconValue
}

export interface IconProps {
  tag: string,
  icon?: IconValue,
  disabled?: Boolean,
}

type IconComponent = JSXComponent<IconProps>

export interface IconSet {
  component: IconComponent
}

export type InternalIconOptions = {
  defaultSet: string
  aliases: Partial<IconAliases>
  sets: Record<string, IconSet>
}

export type IconOptions = Partial<InternalIconOptions>

type IconInstance = {
  component: IconComponent
  icon?: IconValue
}

export const IconSymbol: InjectionKey<InternalIconOptions> = Symbol.for('visagiste:icons')

export const useIconProps = propsFactory({
   icon: {
      type: IconValue,
    },
    tag: {
      type: String,
      required: true
    },
}, 'icon')

export const BaseComponentIcon = defineComponent({
  name: 'BaseComponentIcon',
  props: useIconProps(),
  setup(props, { slots }) {
    return () => {
      const Icon = props.icon as JSXComponent
      return h(
        props.tag,
        null,
        props.icon ? h(Icon) : slots.default?.()
      )
    }
  }
})
export type BaseComponentIcon = InstanceType<typeof BaseComponentIcon>

export const BaseSvgIcon = defineComponent({
  name: 'BaseSvgIcon',
  inheritAttrs: false,
  props: useIconProps(),
  setup(props, { attrs }) {
    return () => {
      const icon = Array.isArray(props.icon)
        ? props.icon.map(path => {
            if (Array.isArray(path)) {
              return h('path', {d: path[0], fillOpacity: path[1]});
            } else {
              return h('path', {d: path});
            }
          })
         : h('path', { d: props.icon });

      console.log(icon)

      return h(props.tag, { ...attrs, style: null} ,
        h('svg', {
          class: "base-icon__svg",
          xmlns: "http://www.w3.org/2000/svg",
          viewBox: "0 0 24 24",
          role: "img",
          'aria-hidden': "true",
        }, icon)
      )
    }
  }
})
export type BaseSvgIcon = InstanceType<typeof BaseSvgIcon>

export const BaseLigatureIcon = defineComponent({
  name: 'BaseLigatureIcon',
  props: useIconProps(),
  setup(props) {
    return () => h(props.tag, null, props.icon)
  },
})
export type BaseLigatureIcon = InstanceType<typeof BaseLigatureIcon>

export const BaseClassIcon = defineComponent({
  name: 'BaseClassIcon',
  props: useIconProps(),
  setup(props, context) {
    return () => {
      return h(props.tag, { class: props.icon })
    }
  },
})
export type BaseClassIcon = InstanceType<typeof BaseClassIcon>

function generateDefaults (): Record<string, IconSet> {
  return {
    svg: {
      component: BaseSvgIcon,
    },
    class: {
      component: BaseClassIcon,
    },
  }
}

// Composables
export function createIcons (options?: IconOptions) {
  const sets = generateDefaults()
  const defaultSet = options?.defaultSet ?? 'mdi'

  if (defaultSet === 'mdi' && !sets.mdi) {
    sets.mdi = mdi
  }

  return mergeDeep({
    defaultSet,
    sets,
    aliases: {
      ...aliases,
     // Here can be set default svg path
    }
  }, options) as InternalIconOptions
}

export const useIcon = (props: Ref<IconValue | undefined>) => {
  const icons = inject(IconSymbol)

  if (!icons) throw new Error('Missing Visagiste Icons provide!')

  const iconData = computed<IconInstance>(() => {
    const iconAlias = unref(props)

    if (!iconAlias) return { component: BaseComponentIcon }

    let icon: IconValue | undefined = iconAlias

    if (typeof icon === 'string') {
      icon = icon.trim()

      if (icon.startsWith('$')) {
        icon = icons.aliases?.[icon.slice(1)]
      }
    }

    if (!icon) consoleWarn(`Could not find aliased icon ${iconAlias}`)

    if (Array.isArray(icon)) {
      return {
        component: BaseSvgIcon,
        icon,
      }
    } else if (typeof icon !== 'string') {
      return {
        component: BaseComponentIcon,
        icon,
      }
    }

    const iconSetName = Object.keys(icons.sets).find(
      setName => typeof icon === 'string' && icon.startsWith(`${setName}:`)
    )

    const iconName = iconSetName ? icon.slice(iconSetName.length + 1) : icon
    const iconSet = icons.sets[iconSetName ?? icons.defaultSet]

    return {
      component: iconSet.component,
      icon: iconName,
    }
  })

  return { iconData }
}