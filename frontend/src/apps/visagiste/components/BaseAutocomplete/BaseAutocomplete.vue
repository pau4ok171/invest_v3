<script lang="ts">
// Styles
import './BaseAutocomplete.scss'

// Components
import { useSelectProps } from '../BaseSelect/BaseSelect.vue'
import { BaseTextField, useBaseTextFieldProps } from '../BaseTextField'
import { BaseList, BaseListItem } from '@/apps/visagiste/components/BaseList'
import { useScrolling } from '@/apps/visagiste/components/BaseSelect/useScrolling'
import { BaseMenu } from '@/apps/visagiste/components/BaseMenu'
import { BaseVirtualScroll } from '@/apps/visagiste/components/BaseVirtualScroll'
import { BaseCheckboxButton } from '@/apps/visagiste/components/BaseCheckbox'
import { BaseAvatar } from '@/apps/visagiste/components/BaseAvatar'
import { BaseIcon } from '@/apps/visagiste/components/BaseIcon'
import { BaseChip } from '@/apps/visagiste/components/BaseChip'
import { BaseDefaultsProvider } from '@/apps/visagiste/components/BaseDefaultsProvider'

// Composables
import { useLocale } from '@/apps/visagiste/composables'
import { useFilter, useFilterProps } from '@/apps/visagiste/composables/filter'
import type { FilterMatch } from '@/apps/visagiste/composables/filter'
import { useTransitionProps } from '@/apps/visagiste/composables/transition'
import { useProxiedModel } from '@/apps/visagiste/composables/proxiedModel'
import { useItems } from '@/apps/visagiste/composables/list-items'
import { useTextColor } from '@/apps/visagiste/composables/color'
import { useForm } from '@/apps/visagiste/composables/form'
import { useSlotIsEmpty } from '@/apps/visagiste/composables/slotIsEmpty'

// Utilities
import {
  computed,
  Fragment,
  h,
  mergeProps,
  nextTick,
  ref,
  shallowRef,
  watch,
} from 'vue'
import {
  checkPrintable,
  deepEqual,
  defineComponent,
  IN_BROWSER,
  matchesSelector,
  noop,
  omit,
  propsFactory,
  wrapInArray,
} from '@/apps/visagiste/utils'

// Types
import type { PropType } from 'vue'
import type { ListItem } from '@/apps/visagiste/composables/list-items'

function highlightResult(
  text: string,
  matches: FilterMatch | undefined,
  length: number
) {
  if (matches == null) return text

  if (Array.isArray(matches))
    throw new Error('Multiple matches is not implemented')

  return typeof matches === 'number' && ~matches
    ? () =>
        h(Fragment, [
          h(
            'span',
            { class: 'base-autocomplete__unmask' },
            text.slice(0, matches)
          ),
          h(
            'span',
            { class: 'base-autocomplete__mask' },
            text.slice(matches, matches + length)
          ),
          h(
            'span',
            { class: 'base-autocomplete__unmask' },
            text.slice(matches + length)
          ),
        ])
    : text
}

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

export const useBaseAutocompleteProps = propsFactory(
  {
    autoSelectFirst: {
      type: [Boolean, String] as PropType<boolean | 'exact'>,
    },
    clearOnSelect: Boolean,
    search: String,

    ...useFilterProps({ filterKeys: ['title'] }),
    ...useSelectProps(),
    ...omit(
      useBaseTextFieldProps({
        modelValue: null,
        role: 'combobox',
      }),
      ['validationValue', 'dirty', 'appendInnerIcon']
    ),
    ...useTransitionProps({ transition: false }),
  },
  'BaseAutocomplete'
)

export default defineComponent({
  name: 'BaseAutocomplete',
  methods: { mergeProps, noop, highlightResult },
  components: {
    BaseDefaultsProvider,
    BaseChip,
    BaseIcon,
    BaseAvatar,
    BaseCheckboxButton,
    BaseVirtualScroll,
    BaseListItem,
    BaseList,
    BaseMenu,
    BaseTextField,
  },
  props: useBaseAutocompleteProps(),
  emits: {
    'update:focused': (focused: boolean) => true,
    'update:search': (value: any) => true,
    'update:modelValue': (value: any) => true,
    'update:menu': (value: boolean) => true,
  },
  setup(props) {
    const { t } = useLocale()
    const baseTextFieldRef = ref()
    const isFocused = shallowRef(false)
    const isPristine = shallowRef(true)
    const listHasFocus = shallowRef(false)
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
    const selectionIndex = shallowRef(-1)
    const color = computed(() => baseTextFieldRef.value?.color)
    const label = computed(() =>
      menu.value ? props.closeText : props.openText
    )
    const { items, transformIn, transformOut } = useItems(props)
    const { textColorClasses, textColorStyles } = useTextColor(color)
    const search = useProxiedModel(props, 'search', '')
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
    const { filteredItems, getMatches } = useFilter(props, items, () =>
      isPristine.value ? '' : search.value
    )

    const displayItems = computed(() => {
      if (props.hideSelected) {
        return filteredItems.value.filter(
          (filteredItem) =>
            !model.value.some((s) => s.value === filteredItem.value)
        )
      }
      return filteredItems.value
    })

    const chipsIsEmpty = useSlotIsEmpty('chips')
    const selectionIsEmpty = useSlotIsEmpty('selection')
    const hasChips = computed(() => !!props.chips || !chipsIsEmpty.value)
    const hasSelectionSlot = computed(
      () => hasChips.value || !selectionIsEmpty.value
    )

    const selectedValues = computed(() =>
      model.value.map((selection) => selection.props.value)
    )

    const highlightFirst = computed(() => {
      const selectFirst =
        props.autoSelectFirst === true ||
        (props.autoSelectFirst === 'exact' &&
          search.value === displayItems.value[0]?.title)
      return (
        selectFirst &&
        displayItems.value.length > 0 &&
        !isPristine.value &&
        !listHasFocus.value
      )
    })

    const menuDisabled = computed(
      () =>
        (props.hideNoData && !displayItems.value.length) ||
        form.isReadonly.value ||
        form.isDisabled.value
    )

    const listRef = ref<InstanceType<typeof BaseList>>()
    const listEvents = useScrolling(listRef, baseTextFieldRef)
    function onClear(e: MouseEvent) {
      if (props.openOnClear) {
        menu.value = true
      }

      search.value = ''
    }
    function onMousedownControl() {
      if (menuDisabled.value) return

      menu.value = true
    }
    function onMousedownMenuIcon(e: MouseEvent) {
      if (menuDisabled.value) return

      if (isFocused.value) {
        e.preventDefault()
        e.stopPropagation()
      }
      menu.value = !menu.value
    }
    function onListKeydown(e: KeyboardEvent) {
      if (e.key !== ' ' && checkPrintable(e)) {
        baseTextFieldRef.value?.focus()
      }
    }
    function onKeydown(e: KeyboardEvent) {
      if (form.isReadonly.value) return

      const selectionStart = baseTextFieldRef.value.inputRef.selectionStart
      const length = model.value.length

      if (['Enter', 'ArrowDown', 'ArrowUp'].includes(e.key)) {
        e.preventDefault()
      }

      if (['Enter', 'ArrowDown'].includes(e.key)) {
        menu.value = true
      }

      if (['Escape'].includes(e.key)) {
        menu.value = false
      }

      if (
        highlightFirst.value &&
        ['Enter', 'Tab'].includes(e.key) &&
        !model.value.some(({ value }) => value === displayItems.value[0].value)
      ) {
        select(displayItems.value[0])
      }

      if (e.key === 'ArrowDown' && highlightFirst.value) {
        listRef.value?.focus('next')
      }

      if (['Backspace', 'Delete'].includes(e.key)) {
        if (
          !props.multiple &&
          hasSelectionSlot.value &&
          model.value.length > 0 &&
          !search.value
        )
          return select(model.value[0], false)

        if (~selectionIndex.value) {
          e.preventDefault()
          const originalSelectionIndex = selectionIndex.value
          select(model.value[selectionIndex.value], false)

          selectionIndex.value =
            originalSelectionIndex >= length - 1
              ? length - 2
              : originalSelectionIndex
        } else if (e.key === 'Backspace' && !search.value) {
          selectionIndex.value = length - 1
        }

        return
      }

      if (!props.multiple) return

      if (e.key === 'ArrowLeft') {
        if (selectionIndex.value < 0 && selectionStart > 0) return

        const prev =
          selectionIndex.value > -1 ? selectionIndex.value - 1 : length - 1

        if (model.value[prev]) {
          selectionIndex.value = prev
        } else {
          selectionIndex.value = -1
          baseTextFieldRef.value.inputRef.setSelectionRange(
            search.value?.length,
            search.value?.length
          )
        }
      } else if (e.key === 'ArrowRight') {
        if (selectionIndex.value < 0) return

        const next = selectionIndex.value + 1

        if (model.value[next]) {
          selectionIndex.value = next
        } else {
          selectionIndex.value = -1
          baseTextFieldRef.value.inputRef.setSelectionRange(0, 0)
        }
      } else if (~selectionIndex.value && checkPrintable(e)) {
        selectionIndex.value = -1
      }
    }

    function onChange(e: Event) {
      if (
        matchesSelector(baseTextFieldRef.value, ':autofill') ||
        matchesSelector(baseTextFieldRef.value, ':-webkit-autofill')
      ) {
        const item = items.value.find(
          (item) => item.title === (e.target as HTMLInputElement).value
        )
        if (item) {
          select(item)
        }
      }
    }

    function onAfterEnter() {
      if (props.eager) {
        baseVirtualScrollRef.value?.calculateVisibleItems()
      }
    }
    function onAfterLeave() {
      if (isFocused.value) {
        isPristine.value = true
        baseTextFieldRef.value?.focus()
      }
    }

    function onFocusin(e: FocusEvent) {
      isFocused.value = true
      setTimeout(() => {
        listHasFocus.value = true
      })
    }
    function onFocusout(e: FocusEvent) {
      listHasFocus.value = false
    }
    function onUpdateModelValue(v: any) {
      if (v == null || (v === '' && !props.multiple && !hasSelectionSlot.value))
        model.value = []
    }

    const isSelecting = shallowRef(false)

    /** @param set - null means toggle */
    function select(item: ListItem | undefined, set: boolean | null = true) {
      if (!item || item.props.disabled) return

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

        if (props.clearOnSelect) {
          search.value = ''
        }
      } else {
        const add = set !== false
        model.value = add ? [item] : []
        search.value = add && !hasSelectionSlot.value ? item.title : ''

        // watch for search watcher to trigger
        nextTick(() => {
          menu.value = false
          isPristine.value = true
        })
      }
    }

    watch(isFocused, (val, oldVal) => {
      if (val === oldVal) return

      if (val) {
        isSelecting.value = true
        search.value =
          props.multiple || hasSelectionSlot.value
            ? ''
            : String(model.value.at(-1)?.props.title ?? '')
        isPristine.value = true

        nextTick(() => (isSelecting.value = false))
      } else {
        if (!props.multiple && search.value == null) model.value = []
        menu.value = false
        if (!model.value.some(({ title }) => title === search.value))
          search.value = ''
        selectionIndex.value = -1
      }
    })

    watch(search, (val) => {
      if (!isFocused.value || isSelecting.value) return

      if (val) menu.value = true

      isPristine.value = !val
    })

    watch(menu, () => {
      if (!props.hideSelected && menu.value && model.value.length) {
        const index = displayItems.value.findIndex((item) =>
          model.value.some((s) => item.value === s.value)
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

    const prependItemIsEmpty = useSlotIsEmpty('prepend-item')
    const appendItemIsEmpty = useSlotIsEmpty('append-item')
    const noDataIsEmpty = useSlotIsEmpty('no-data')
    const hasList = computed(
      () =>
        !!(!props.hideNoData || displayItems.value.length) ||
        !prependItemIsEmpty.value ||
        !appendItemIsEmpty.value ||
        !noDataIsEmpty.value
    )
    const isDirty = computed(() => model.value.length > 0)
    const textFieldProps = computed(() => BaseTextField.filterProps(props))

    return {
      baseTextFieldRef,
      baseMenuRef,
      listRef,
      baseVirtualScrollRef,
      textFieldProps,
      textColorClasses,
      textColorStyles,
      displayItems,
      search,
      model,
      menu,
      menuDisabled,
      form,
      highlightFirst,
      getMatches,
      t,
      select,
      label,
      listEvents,
      counterValue,
      selectionIndex,
      selectedValues,
      isFocused,
      isDirty,
      isPristine,
      hasList,
      hasChips,
      hasSelectionSlot,
      onClear,
      onChange,
      onKeydown,
      onListKeydown,
      onFocusin,
      onFocusout,
      onUpdateModelValue,
      onMousedownControl,
      onMousedownMenuIcon,
      onAfterEnter,
      onAfterLeave,
      onChipClose,
      onChipKeydown,
      onChipMousedown,
    }
  },
})
</script>

<template>
  <BaseTextField
    ref="baseTextFieldRef"
    v-bind="textFieldProps"
    v-model="search"
    :onUpdate:modelValue="onUpdateModelValue"
    v-model:focused="isFocused"
    :validationValue="model.externalValue"
    :counterValue="counterValue"
    :dirty="isDirty"
    :onChange="onChange"
    :class="[
      'base-autocomplete',
      `base-autocomplete--${$props.multiple ? 'multiple' : 'single'}`,
      {
        'base-autocomplete--active-menu': menu,
        'base-autocomplete--chips': !!$props.chips,
        'base-autocomplete--selection-slot': !!hasSelectionSlot,
        'base-autocomplete--selecting-index': selectionIndex > -1,
      },
      $props.class,
    ]"
    :style="$props.style"
    :readonly="form.isReadonly.value"
    :placeholder="isDirty ? undefined : $props.placeholder"
    :onClick:clear="onClear"
    :onMousedown:control="onMousedownControl"
    :onKeydown="onKeydown"
  >
    <template #label><slot name="label" /></template>

    <template #clear><slot name="clear" /></template>

    <template #prepend><slot name="prepend" /></template>

    <template #append><slot name="append" /></template>

    <template #prepend-inner><slot name="prepend-inner" /></template>

    <template #loader><slot name="loader" /></template>

    <template #message><slot name="message" /></template>

    <template #details><slot name="details" /></template>

    <template #counter><slot name="counter" /></template>

    <template #default>
      <BaseMenu
        ref="baseMenuRef"
        v-model="menu"
        activator="parent"
        contentClass="base-autocomplete__content"
        :disabled="menuDisabled"
        :eager="$props.eager"
        :max-height="310"
        :open-onClick="false"
        :closeOnContentClick="false"
        :transition="$props.transition"
        :onAfterEnter="onAfterEnter"
        :onAfterLeave="onAfterLeave"
        v-bind="$props.menuProps"
      >
        <template v-if="hasList">
          <BaseList
            ref="listRef"
            :selected="selectedValues"
            :select-strategy="
              $props.multiple ? 'independent' : 'single-independent'
            "
            :onMousedown="(e: MouseEvent) => e.preventDefault()"
            :onKeydown="onListKeydown"
            :onFocusin="onFocusin"
            :onFocusout="onFocusout"
            tabindex="-1"
            aria-live="polite"
            :color="$props.itemColor ?? $props.color"
            v-bind="{ ...listEvents, ...$props.listProps }"
          >
            <slot name="prepend-item" />

            <template v-if="!displayItems.length && !$props.hideNoData">
              <slot name="no-data">
                <BaseListItem
                  key="no-data"
                  :title="t($props.noDataText as string)"
                />
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
                      active: highlightFirst && index === 0 ? true : undefined,
                      onClick: () => select(item, null),
                    }),
                  }"
                >
                  <BaseListItem
                    v-bind="
                      mergeProps(item.props, {
                        ref: itemRef,
                        key: item.value,
                        active:
                          highlightFirst && index === 0 ? true : undefined,
                        onClick: () => select(item, null),
                      })
                    "
                    role="option"
                  >
                    <template #prepend="{ isSelected }">
                      <BaseCheckboxButton
                        v-if="$props.multiple && !$props.hideSelected"
                        :modelValue="isSelected"
                        :key="item.value"
                        :riple="false"
                        tabindex="-1"
                      />

                      <BaseAvatar
                        v-if="item.props.prependAvatar"
                        :image="item.props.prependAvatar"
                      />

                      <BaseIcon
                        v-if="item.props.prependIcon"
                        :icon="item.props.prependIcon"
                      />
                    </template>
                    <template #title>
                      <template v-if="isPristine">{{ item.title }}</template>
                      <template v-else
                        ><component
                          :is="
                            highlightResult(
                              item.title,
                              getMatches(item)?.title,
                              search?.length ?? 0
                            )
                          "
                      /></template>
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
        :class="[
          'base-autocomplete__selection',
          index === selectionIndex && [
            'base-autocomplete__selection--selected',
            textColorClasses,
          ],
        ]"
        :style="index === selectionIndex ? textColorStyles : {}"
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
                :onClick:close="(e: Event) => onChipClose(e, item)"
                :onKeydown="(e: KeyboardEvent) => onChipKeydown(e, item)"
                :onMousedown="onChipMousedown"
                :modelValue="true"
                :onUpdate:modelValue="undefined"
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
              :onClick:close="(e: Event) => onChipClose(e, item)"
              :onKeydown="(e: KeyboardEvent) => onChipKeydown(e, item)"
              :onMousedown="onChipMousedown"
              :modelValue="true"
              :onUpdate:modelValue="undefined"
            />
          </template>
        </template>
        <template v-else>
          <slot name="selection" v-bind="{ item, index }">
            <span class="base-autocomplete__selection-text">
              {{ item.title }}
              <span
                v-if="$props.multiple && index < model.length - 1"
                class="base-autocomplete__selection-comma"
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
        <BaseIcon
          class="base-autocomplete__menu-icon"
          :icon="$props.menuIcon"
          :onMousedown="onMousedownMenuIcon"
          :onClick="noop"
          :aria-label="t(label)"
          tabindex="-1"
        />
      </template>
    </template>
  </BaseTextField>
</template>
