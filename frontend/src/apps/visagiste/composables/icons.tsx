// Icons
import { aliases, mdi } from '@/apps/visagiste/iconsets/mdi'

// Utilities
import {computed, defineComponent, inject, unref} from "vue";
import {consoleWarn, mergeDeep} from "@/apps/visagiste/utils";

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

export const iconProps = {
   icon: {
      type: IconValue,
    },
    tag: {
      type: String,
      required: true
    },
}

export const BaseComponentIcon = defineComponent({
  name: 'BaseComponentIcon',
  props: iconProps,
  setup(props, { slots }) {
    return () => {
      const Icon = props.icon as JSXComponent
      return (
        <props.tag>
          { props.icon ? <Icon/> : slots.default?.() }
        </props.tag>
      )
    }
  }
})
export type BaseComponentIcon = InstanceType<typeof BaseComponentIcon>

export const BaseSvgIcon = defineComponent({
  name: 'BaseSvgIcon',
  inheritAttrs: false,
  props: iconProps,
  setup(props, { attrs }) {
    return () => {
      return (
        <props.tag { ...attrs } style={ null }>
          <svg
            class="base-icon__svg"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            role="img"
            aria-hidden="true"
          >
            { Array.isArray(props.icon)
              ? props.icon.map(path => (
                Array.isArray(path)
                  ? <path d={ path[0] as string } fill-opacity={ path[1] }></path>
                  : <path d={ path as string }></path>
              ))
              : <path d={ props.icon as string }></path>
            }
          </svg>
        </props.tag>
      )
    }
  }
})
export type BaseSvgIcon = InstanceType<typeof BaseSvgIcon>

export const BaseLigatureIcon = defineComponent({
  name: 'BaseLigatureIcon',
  props: iconProps,
  setup(props) {
    return () => {
      return <props.tag>{ props.icon }</props.tag>
    }
  },
})
export type BaseLigatureIcon = InstanceType<typeof BaseLigatureIcon>

export const BaseClassIcon = defineComponent({
  name: 'BaseClassIcon',
  props: iconProps,
  setup(props) {
    return () => {
      return <props.tag class={ props.icon }></props.tag>
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