<script lang="ts">
// Styles
import './BaseSelect.scss'

// Components
import { BaseDialogTransition } from '@/apps/visagiste/components/transitions'
import { BaseAvatar } from '@/apps/visagiste/components/BaseAvatar'
import { BaseCheckboxButton } from '@/apps/visagiste/components/BaseCheckbox'
import { BaseChip } from '@/apps/visagiste/components/BaseChip'
import { BaseDefaultsProvider } from '@/apps/visagiste/components/BaseDefaultsProvider'
import { BaseIcon } from '@/apps/visagiste/components/BaseIcon'
import { BaseList, BaseListItem } from '@/apps/visagiste/components/BaseList'
import { BaseMenu } from '@/apps/visagiste/components/BaseMenu'
import {
  BaseTextField,
  useBaseTextFieldProps,
} from '@/apps/visagiste/components/BaseTextField'
import { BaseVirtualScroll } from '@/apps/visagiste/components/BaseVirtualScroll'

// Composables
import { useScrolling } from './useScrolling'
import { useForm } from '@/apps/visagiste/composables/form'
import { IconValue } from '@/apps/visagiste/composables/icons'
import {
  useItems,
  useItemsProps,
} from '@/apps/visagiste/composables/list-items'
import { useLocale } from '@/apps/visagiste/composables/locale'
import { useProxiedModel } from '@/apps/visagiste/composables/proxiedModel'
import { useTransitionProps } from '@/apps/visagiste/composables/transition'
import { useSlotIsEmpty } from '@/apps/visagiste/composables/slotIsEmpty'

// Utilities
import { computed, mergeProps, nextTick, ref, shallowRef, watch } from 'vue'
import {
  checkPrintable,
  deepEqual,
  defineComponent,
  IN_BROWSER,
  matchesSelector,
  omit,
  propsFactory,
  wrapInArray,
} from '@/apps/visagiste/utils'

// Types
import type { Component, PropType } from 'vue'
import type { ListItem } from '@/apps/visagiste/composables/list-items'

type Primitive = string | number | boolean | symbol

type Val<T, ReturnObject extends boolean> = [T] extends [Primitive]
  ? T
  : ReturnObject extends true
    ? T
    : any

type Value<
  T,
  ReturnObject extends boolean,
  Multiple extends boolean,
> = Multiple extends true
  ? readonly Val<T, ReturnObject>[]
  : Val<T, ReturnObject> | null

export const useSelectProps = propsFactory(
  {
    chips: Boolean,
    closableChips: Boolean,
    closeText: {
      type: String,
      default: '$visagiste.close',
    },
    openText: {
      type: String,
      default: '$visagiste.open',
    },
    eager: Boolean,
    hideNoData: Boolean,
    hideSelected: Boolean,
    listProps: {
      type: Object as PropType<InstanceType<typeof BaseList>['$props']>,
    },
    menu: Boolean,
    menuIcon: {
      type: IconValue,
      default: '$dropdown',
    },
    menuProps: {
      type: Object as PropType<InstanceType<typeof BaseMenu>['$props']>,
    },
    multiple: Boolean,
    noDataText: {
      type: String,
      default: '$visagiste.noDataText',
    },
    openOnClear: Boolean,
    itemColor: String,

    ...useItemsProps({ itemChildren: false }),
  },
  'Select'
)

export const useBaseSelectProps = propsFactory(
  {
    ...useSelectProps(),
    ...omit(
      useBaseTextFieldProps({
        modelValue: null,
        role: 'combobox',
      }),
      ['validationValue', 'dirty', 'appendInnerIcon']
    ),
    ...useTransitionProps({
      transition: { component: BaseDialogTransition as Component },
    }),
  },
  'BaseSelect'
)

export default defineComponent({
  name: 'BaseSelect',
  methods: { mergeProps },
  components: {
    BaseChip,
    BaseDefaultsProvider,
    BaseIcon,
    BaseAvatar,
    BaseCheckboxButton,
    BaseVirtualScroll,
    BaseListItem,
    BaseList,
    BaseMenu,
    BaseTextField,
  },
  props: useBaseSelectProps(),
  emits: {
    'update:focused': (focused: boolean) => true,
    'update:modelValue': (value: any) => true,
    'update:menu': (ue: boolean) => true,
  },
  setup(props) {
    const { t } = useLocale()
    const baseTextFieldRef = ref()
    const baseMenuRef = ref<InstanceType<typeof BaseMenu>>()
    const baseVirtualScrollRef = ref<InstanceType<typeof BaseVirtualScroll>>()
    const _menu = useProxiedModel(props, 'menu')
    const menu = computed({
      get: () => _menu.value,
      set: (v) => {
        if (_menu.value && !v && baseMenuRef.value?.openChildren.size) return
        _menu.value = v
      },
    })
    const { items, transformIn, transformOut } = useItems(props)
    const model = useProxiedModel(
      props,
      'modelValue',
      [],
      (v) => transformIn(v === null ? [null] : wrapInArray(v)),
      (v) => {
        const transformed = transformOut(v)
        return props.multiple ? transformed : (transformed[0] ?? null)
      }
    )
    const counterValue = computed(() => {
      return typeof props.counterValue === 'function'
        ? props.counterValue(model.value)
        : typeof props.counterValue === 'number'
          ? props.counterValue
          : model.value.length
    })
    const form = useForm(props)
    const selectedValues = computed(() =>
      model.value.map((selection) => selection.value)
    )
    const isFocused = shallowRef(false)
    const label = computed(() =>
      menu.value ? props.closeText : props.openText
    )

    let keyboardLookupPrefix = ''
    let keyboardLookupLastTime: number

    const displayItems = computed(() => {
      if (props.hideSelected) {
        return items.value.filter(
          (item) =>
            !model.value.some((s) =>
              (props.valueComparator || deepEqual)(s, item)
            )
        )
      }
      return items.value
    })

    const menuDisabled = computed(
      () =>
        (props.hideNoData && !displayItems.value.length) ||
        form.isReadonly.value ||
        form.isDisabled.value
    )

    const computedMenuProps = computed(() => {
      return {
        ...props.menuProps,
        activatorProps: {
          ...(props.menuProps?.activatorProps || {}),
          'aria-haspopup': 'listbox', // Set aria-haspopup to 'listbox'
        },
      }
    })

    const listRef = ref<InstanceType<typeof BaseList>>()
    const listEvents = useScrolling(listRef, baseTextFieldRef)
    function onClear(e: MouseEvent) {
      if (props.openOnClear) {
        menu.value = true
      }
    }
    function onMousedownControl() {
      if (menuDisabled.value) return

      menu.value = !menu.value
    }
    function onListKeydown(e: KeyboardEvent) {
      if (checkPrintable(e)) {
        onKeydown(e)
      }
    }
    function onKeydown(e: KeyboardEvent) {
      if (!e.key || form.isReadonly.value) return

      if (
        ['Enter', ' ', 'ArrowDown', 'ArrowUp', 'Home', 'End'].includes(e.key)
      ) {
        e.preventDefault()
      }

      if (['Enter', 'ArrowDown', ' '].includes(e.key)) {
        menu.value = true
      }

      if (['Escape', 'Tab'].includes(e.key)) {
        menu.value = false
      }

      if (e.key === 'Home') {
        listRef.value?.focus('first')
      } else if (e.key === 'End') {
        listRef.value?.focus('last')
      }

      // html select hotkeys
      const KEYBOARD_LOOKUP_THRESHOLD = 1000 // milliseconds

      if (!checkPrintable(e)) return

      const now = performance.now()
      if (now - keyboardLookupLastTime > KEYBOARD_LOOKUP_THRESHOLD) {
        keyboardLookupPrefix = ''
      }
      keyboardLookupPrefix += e.key.toLowerCase()
      keyboardLookupLastTime = now

      const item = items.value.find((item) =>
        item.title.toLowerCase().startsWith(keyboardLookupPrefix)
      )
      if (item !== undefined) {
        model.value = [item]
        const index = displayItems.value.indexOf(item)
        IN_BROWSER &&
          window.requestAnimationFrame(() => {
            index >= 0 && baseVirtualScrollRef.value?.scrollToIndex(index)
          })
      }
    }

    /** @param set - null means toggle */
    function select(item: ListItem, set: boolean | null = true) {
      if (item.props.disabled) return

      if (props.multiple) {
        const index = model.value.findIndex((selection) =>
          (props.valueComparator || deepEqual)(selection.value, item.value)
        )
        const add = set == null ? !~index : set

        if (~index) {
          const value = add ? [...model.value, item] : [...model.value]
          value.splice(index, 1)
          model.value = value
        } else if (add) {
          model.value = [...model.value, item]
        }
      } else {
        const add = set !== false
        model.value = add ? [item] : []

        nextTick(() => {
          menu.value = false
        })
      }
    }

    function onBlur(e: FocusEvent) {
      if (!listRef.value?.$el.contains(e.relatedTarget as HTMLElement)) {
        menu.value = false
      }
    }

    function onAfterEnter() {
      if (props.eager) {
        baseVirtualScrollRef.value?.calculateVisibleItems()
      }
    }

    function onAfterLeave() {
      if (isFocused.value) {
        baseTextFieldRef.value?.focus()
      }
    }

    function onFocusin(e: FocusEvent) {
      isFocused.value = true
    }

    function onModelUpdate(v: any) {
      if (v == null) model.value = []
      else if (
        matchesSelector(baseTextFieldRef.value, ':autofill') ||
        matchesSelector(baseTextFieldRef.value, ':-webkit-autofill')
      ) {
        const item = items.value.find((item) => item.title === v)
        if (item) {
          select(item)
        }
      } else if (baseTextFieldRef.value) {
        baseTextFieldRef.value.value = ''
      }
    }

    watch(menu, () => {
      if (!props.hideSelected && menu.value && model.value.length) {
        const index = displayItems.value.findIndex((item) =>
          model.value.some((s) =>
            (props.valueComparator || deepEqual)(s.value, item.value)
          )
        )
        IN_BROWSER &&
          window.requestAnimationFrame(() => {
            index >= 0 && baseVirtualScrollRef.value?.scrollToIndex(index)
          })
      }
    })

    watch(
      () => props.items,
      (newVal, oldVal) => {
        if (menu.value) return

        if (isFocused.value && !oldVal.length && newVal.length) {
          menu.value = true
        }
      }
    )

    const chipIsEmpty = useSlotIsEmpty('chip')
    const prependItemIsEmpty = useSlotIsEmpty('prepend-item')
    const appendItemIsEmpty = useSlotIsEmpty('append-item')
    const noDataIsEmpty = useSlotIsEmpty('no-data')
    const selectionIsEmpty = useSlotIsEmpty('selection')

    const hasChips = computed(() => !!props.chips || !chipIsEmpty.value)
    const hasList = computed(
      () =>
        !props.hideNoData ||
        displayItems.value.length ||
        !prependItemIsEmpty.value ||
        !appendItemIsEmpty.value ||
        !noDataIsEmpty.value
    )
    const isDirty = computed(() => model.value.length > 0)
    const textFieldProps = computed(() => BaseTextField.filterProps(props))
    const placeholder = computed(() =>
      isDirty.value ||
      (!isFocused.value && !props.label && !props.persistentPlaceholder)
        ? undefined
        : props.placeholder
    )

    function onChipClose(e: Event, item: ListItem) {
      e.stopPropagation()
      e.preventDefault()

      select(item, false)
    }

    function onChipKeydown(e: KeyboardEvent, item: ListItem) {
      if (e.key !== 'Enter' && e.key !== ' ') return

      e.preventDefault()
      e.stopPropagation()

      onChipClose(e, item)
    }

    function onChipMousedown(e: MouseEvent) {
      e.preventDefault()
      e.stopPropagation()
    }

    return {
      baseVirtualScrollRef,
      baseTextFieldRef,
      baseMenuRef,
      listRef,
      textFieldProps,
      listEvents,
      displayItems,
      model,
      onModelUpdate,
      onClear,
      onMousedownControl,
      onBlur,
      onKeydown,
      onListKeydown,
      onAfterEnter,
      onAfterLeave,
      onFocusin,
      onChipClose,
      onChipKeydown,
      onChipMousedown,
      isFocused,
      isDirty,
      hasList,
      hasChips,
      counterValue,
      selectionIsEmpty,
      selectedValues,
      placeholder,
      t,
      select,
      label,
      menu,
      menuDisabled,
      computedMenuProps,
    }
  },
})
</script>

<template>
  <BaseTextField
    ref="baseTextFieldRef"
    v-bind="textFieldProps"
    :modelValue="model.map((v) => v.props.value).join(', ')"
    @update:modelValue="onModelUpdate"
    v-model:focused="isFocused"
    :validationValue="model.externalValue"
    :counterValue="counterValue"
    :dirty="isDirty"
    :class="[
      'base-select',
      {
        'base-select--active-menu': menu,
        'base-select--chips': !!$props.chips,
        [`base-select--${$props.multiple ? 'multiple' : 'single'}`]: true,
        'base-select--selected': model.length,
        'base-select--selection-slot': !selectionIsEmpty,
      },
      $props.class,
    ]"
    :style="$props.style"
    inputmode="none"
    :placeholder="placeholder"
    @click:clear="onClear"
    @mousedown:control="onMousedownControl"
    @blur="onBlur"
    @keydown="onKeydown"
    :aria-label="t(label)"
    :title="t(label)"
  >
    <template #prepend-inner="slotProps"
      ><slot name="prepend-inner" v-bind="slotProps"
    /></template>
    <template #prepend="slotProps"
      ><slot name="prepend" v-bind="slotProps"
    /></template>
    <template #append="slotProps"
      ><slot name="append" v-bind="slotProps"
    /></template>
    <template #loader="slotProps"
      ><slot name="loader" v-bind="slotProps"
    /></template>
    <template #clear="slotProps"
      ><slot name="clear" v-bind="slotProps"
    /></template>
    <template #message="slotProps"
      ><slot name="message" v-bind="slotProps"
    /></template>
    <template #details="slotProps"
      ><slot name="details" v-bind="slotProps"
    /></template>
    <template #label="slotProps"
      ><slot name="label" v-bind="slotProps"
    /></template>
    <template #counter="slotProps"
      ><slot name="counter" v-bind="slotProps"
    /></template>

    <template #default>
      <BaseMenu
        ref="baseMenuRef"
        v-model="menu"
        v-bind="computedMenuProps"
        activator="parent"
        contentClass="base-select__content"
        :disabled="menuDisabled"
        :eager="$props.eager"
        :max-Height="310"
        :openOnClick="false"
        :closeOnContentClick="false"
        :transition="$props.transition"
        @afterEnter="onAfterEnter"
        @afterLeave="onAfterLeave"
      >
        <template v-if="hasList">
          <BaseList
            ref="listRef"
            v-bind="{ ...listEvents, ...$props.listProps }"
            :selected="selectedValues"
            :selectStrategy="
              $props.multiple ? 'independent' : 'single-independent'
            "
            @mousedown="(e: MouseEvent) => e.preventDefault()"
            @keydown="onListKeydown"
            @focusin="onFocusin"
            tabindex="-1"
            aria-live="polite"
            :color="$props.itemColor ?? $props.color"
          >
            <slot name="prepend-item" />

            <template v-if="!displayItems.length && !$props.hideNoData">
              <slot name="prepend-item">
                <BaseListItem key="no-data" :title="t($props.noDataText)" />
              </slot>
            </template>

            <BaseVirtualScroll
              ref="baseVirtualScrollRef"
              renderless
              :items="displayItems"
            >
              <template #default="{ item, index, itemRef }">
                <slot
                  name="item"
                  v-bind="{
                    item,
                    index,
                    props: mergeProps(item.props, {
                      ref: itemRef,
                      key: item.value,
                      onClick: () => select(item, null),
                    }),
                  }"
                >
                  <BaseListItem
                    role="option"
                    v-bind="
                      mergeProps(item.props, {
                        ref: itemRef,
                        key: item.value,
                        onClick: () => select(item, null),
                      })
                    "
                  >
                    <template #prepend="{ isSelected }">
                      <template v-if="$props.multiple && !$props.hideSelected">
                        <BaseCheckboxButton
                          :key="item.value"
                          :modelValue="isSelected"
                          :ripple="false"
                          tabindex="-1"
                        />
                      </template>

                      <template v-if="item.props.prependAvatar">
                        <BaseAvatar :image="item.props.prependAvatar" />
                      </template>

                      <template v-if="item.props.prependIcon">
                        <BaseIcon :icon="item.props.prependIcon" />
                      </template>
                    </template>
                  </BaseListItem>
                </slot>
              </template>
            </BaseVirtualScroll>

            <slot name="append-item" />
          </BaseList>
        </template>
      </BaseMenu>

      <div
        v-for="(item, index) in model"
        :key="item.value"
        class="base-select__selection"
      >
        <template v-if="hasChips">
          <template v-if="$slots.chip">
            <BaseDefaultsProvider
              key="chip-defaults"
              :defaults="{
                BaseChip: {
                  closable: $props.closableChips,
                  size: 'small',
                  text: item.title,
                },
              }"
            >
              <slot
                name="chip"
                v-bind="{ item, index }"
                @click:close="(e: Event) => onChipClose(e, item)"
                @keydown="(e: KeyboardEvent) => onChipKeydown(e, item)"
                @mousedown="onChipMousedown"
                :modelValue="true"
                @update:modelValue="undefined"
              />
            </BaseDefaultsProvider>
          </template>
          <template v-else>
            <BaseChip
              key="chip"
              :closable="$props.closableChips"
              size="small"
              :text="item.title"
              :disabled="item.props.disabled"
              @click:close="(e: Event) => onChipClose(e, item)"
              @keydown="(e: KeyboardEvent) => onChipKeydown(e, item)"
              @mousedown="onChipMousedown"
              :modelValue="true"
              @update:modelValue="undefined"
            />
          </template>
        </template>
        <template v-else>
          <slot name="selection" v-bind="{ item, index }">
            <span class="base-select__selection-text">
              {{ item.title }}
              <span
                v-if="$props.multiple && index < model.length - 1"
                class="base-select__selection-comma"
              >
                ,
              </span>
            </span>
          </slot>
        </template>
      </div>
    </template>

    <template #append-inner="slotProps">
      <slot name="append-inner" v-bind="slotProps" />
      <template v-if="$props.menuIcon">
        <BaseIcon class="base-select__menu-icon" :icon="$props.menuIcon" />
      </template>
    </template>
  </BaseTextField>
</template>
