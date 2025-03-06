<script lang="ts">
// Styles
import './BaseSkeletonLoader.scss'

// Composables
import {
  useDimension,
  useDimensionProps,
} from '@/apps/visagiste/composables/dimensions'
import {
  useElevation,
  useElevationProps,
} from '@/apps/visagiste/composables/elevation'
import { provideTheme, useThemeProps } from '@/apps/visagiste/composables/theme'
import { useBackgroundColor } from '@/apps/visagiste/composables/color'
import { useLocale } from '@/apps/visagiste/composables'
import { useSlotIsEmpty } from '@/apps/visagiste/composables/slotIsEmpty'

// Utilities
import { computed, h, toRef } from 'vue'
import {
  defineComponent,
  propsFactory,
  wrapInArray,
} from '@/apps/visagiste/utils'

// Types
import type { PropType, VNode } from 'vue'

type BaseSkeletonBone<T> = T | BaseSkeletonBone<T>[]

export type BaseSkeletonBones = BaseSkeletonBone<VNode>
export type BaseSkeletonLoaderType = keyof typeof rootTypes

export const rootTypes = {
  actions: 'button@2',
  article: 'heading, paragraph',
  avatar: 'avatar',
  button: 'button',
  card: 'image, heading',
  'card-avatar': 'image, list-item-avatar',
  chip: 'chip',
  'date-picker':
    'list-item, heading, divider, date-picker-options, date-picker-days, actions',
  'date-picker-options': 'text, avatar@2',
  'date-picker-days': 'avatar@28',
  divider: 'divider',
  heading: 'heading',
  image: 'image',
  'list-item': 'text',
  'list-item-avatar': 'avatar, text',
  'list-item-two-line': 'sentences',
  'list-item-avatar-two-line': 'avatar, sentences',
  'list-item-three-line': 'paragraph',
  'list-item-avatar-three-line': 'avatar, paragraph',
  ossein: 'ossein',
  paragraph: 'text@3',
  sentences: 'text@2',
  subtitle: 'text',
  table: 'table-heading, table-thead, table-tbody, table-tfoot',
  'table-heading': 'chip, text',
  'table-thead': 'heading@6',
  'table-tbody': 'table-row-divider@6',
  'table-row-divider': 'table-row, divider',
  'table-row': 'text@6',
  'table-tfoot': 'text@2, avatar@2',
  text: 'text',
} as const

function genBone(type: string, children: BaseSkeletonBones = []) {
  return h(
    'div',
    { class: ['base-skeleton-loader__bone', `base-skeleton-loader__${type}`] },
    children
  )
}

function genBones(bone: string) {
  // e.g. 'text@3'
  const [type, length] = bone.split('@') as [BaseSkeletonLoaderType, number]

  // Generate a length array based upon
  // value after @ in the bone string
  return Array.from({ length }).map(() => genStructure(type))
}

function genStructure(type?: string): BaseSkeletonBones {
  let children: BaseSkeletonBones = []

  if (!type) return children

  // TODO: figure out a better way to type this
  const bone = (rootTypes as Record<string, string>)[type]

  // End of recursion, do nothing
  /* eslint-disable-next-line no-empty, brace-style */
  if (type === bone) {
  }
  // Array of values - e.g. 'heading, paragraph, text@2'
  else if (type.includes(',')) return mapBones(type)
  // Array of values - e.g. 'paragraph@4'
  else if (type.includes('@')) return genBones(type)
  // Array of values - e.g. 'card@2'
  else if (bone.includes(',')) children = mapBones(bone)
  // Array of values - e.g. 'list-item@2'
  else if (bone.includes('@')) children = genBones(bone)
  // Single value - e.g. 'card-heading'
  else if (bone) children.push(genStructure(bone))

  return [genBone(type, children)]
}

function mapBones(bones: string) {
  // Remove spaces and return array of structures
  return bones.replace(/\s/g, '').split(',').map(genStructure)
}

export const useBaseSkeletonLoaderProps = propsFactory(
  {
    boilerplate: Boolean,
    color: String,
    loading: Boolean,
    loadingText: {
      type: String,
      default: '$visagiste.loading',
    },
    type: {
      type: [String, Array] as PropType<
        | BaseSkeletonLoaderType
        | (string & {})
        | ReadonlyArray<BaseSkeletonLoaderType | (string & {})>
      >,
      default: 'ossein',
    },

    ...useDimensionProps(),
    ...useElevationProps(),
    ...useThemeProps(),
  },
  'BaseSkeletonLoader'
)

export default defineComponent({
  name: 'BaseSkeletonLoader',
  props: useBaseSkeletonLoaderProps(),
  setup(props, { slots }) {
    const { backgroundColorClasses, backgroundColorStyles } =
      useBackgroundColor(toRef(props, 'color'))
    const { dimensionStyles } = useDimension(props)
    const { elevationClasses } = useElevation(props)
    const { themeClasses } = provideTheme(props)
    const { t } = useLocale()

    const items = computed(() =>
      genStructure(wrapInArray(props.type).join(','))
    )

    const defaultIsEmpty = useSlotIsEmpty('default')
    const isLoading = computed(() => defaultIsEmpty.value || props.loading)
    const loadingProps = computed(() =>
      props.boilerplate || !isLoading.value
        ? {}
        : {
            ariaLive: 'polite',
            ariaLabel: t(props.loadingText),
            role: 'alert',
          }
    )

    return () =>
      h(
        'div',
        {
          class: [
            'base-skeleton-loader',
            {
              'base-skeleton-loader--boilerplate': props.boilerplate,
            },
            themeClasses.value,
            backgroundColorClasses.value,
            elevationClasses.value,
          ],
          style: [
            backgroundColorStyles.value,
            isLoading.value ? dimensionStyles.value : {},
          ],
          ...loadingProps.value,
        },
        isLoading.value ? items.value : slots.default?.()
      )
  },
})
</script>
