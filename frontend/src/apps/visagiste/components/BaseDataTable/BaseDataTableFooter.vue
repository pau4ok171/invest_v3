<script lang="ts">
// Styles
import './BaseDataTableFooter.scss'

// Components
import { BaseSelect } from '@/apps/visagiste/components/BaseSelect'
import { BasePagination } from '@/apps/visagiste/components/BasePagination'

// Composables
import { usePagination } from '@/apps/visagiste/components/BaseDataTable/composables/paginate'
import { IconValue } from '@/apps/visagiste/composables/icons'
import { useLocale } from '@/apps/visagiste/composables'

// Utilities
import { computed } from 'vue'
import { defineComponent, propsFactory } from '@/apps/visagiste/utils'

// Types
import type { PropType } from 'vue'

export const useBaseDataTableFooterProps = propsFactory(
  {
    prevIcon: {
      type: IconValue,
      default: '$prev',
    },
    nextIcon: {
      type: IconValue,
      default: '$next',
    },
    firstIcon: {
      type: IconValue,
      default: '$first',
    },
    lastIcon: {
      type: IconValue,
      default: '$last',
    },
    itemsPerPageText: {
      type: String,
      default: '$visagiste.dataFooter.itemsPerPageText',
    },
    pageText: {
      type: String,
      default: '$visagiste.dataFooter.pageText',
    },
    firstPageLabel: {
      type: String,
      default: '$visagiste.dataFooter.firstPage',
    },
    prevPageLabel: {
      type: String,
      default: '$visagiste.dataFooter.prevPage',
    },
    nextPageLabel: {
      type: String,
      default: '$visagiste.dataFooter.nextPage',
    },
    lastPageLabel: {
      type: String,
      default: '$visagiste.dataFooter.lastPage',
    },
    itemsPerPageOptions: {
      type: Array as PropType<
        readonly (number | { title: string; value: number })[]
      >,
      default: () => [
        { value: 10, title: '10' },
        { value: 25, title: '25' },
        { value: 50, title: '50' },
        { value: 100, title: '100' },
        { value: -1, title: '$visagiste.dataFooter.itemsPerPageAll' },
      ],
    },
    showCurrentPage: Boolean,
  },
  'BaseDataTableFooter'
)

export default defineComponent({
  name: 'BaseDataTableFooter',
  components: { BasePagination, BaseSelect },
  props: useBaseDataTableFooterProps(),
  setup(props) {
    const { t } = useLocale()
    const {
      page,
      pageCount,
      startIndex,
      stopIndex,
      itemsLength,
      itemsPerPage,
      setItemsPerPage,
    } = usePagination()

    const itemsPerPageOptions = computed(() =>
      props.itemsPerPageOptions.map((option) => {
        if (typeof option === 'number') {
          return {
            value: option,
            title:
              option === -1
                ? t('$visagiste.dataFooter.itemsPerPageAll')
                : String(option),
          }
        }

        return {
          ...option,
          title: !isNaN(Number(option.title)) ? option.title : t(option.title),
        }
      })
    )

    const paginationProps = computed(() => BasePagination.filterProps(props))

    return {
      t,
      page,
      pageCount,
      itemsLength,
      itemsPerPage,
      itemsPerPageOptions,
      setItemsPerPage,
      startIndex,
      stopIndex,
      paginationProps,
    }
  },
})
</script>

<template>
  <div class="base-data-table-footer">
    <slot name="prepend" />

    <div class="base-data-table-footer__items-per-page">
      <span>{{ t($props.itemsPerPageText as string) }}</span>

      <BaseSelect
        :items="itemsPerPageOptions"
        :modelValue="itemsPerPage"
        @update:modelValue="(v) => setItemsPerPage(Number(v))"
        density="compact"
        variant="outlined"
        hide-details
      />
    </div>

    <div class="base-data-table-footer__info">
      <div>
        {{
          t(
            $props.pageText as string,
            !itemsLength ? 0 : startIndex + 1,
            stopIndex,
            itemsLength
          )
        }}
      </div>
    </div>

    <div class="base-data-table-footer__pagination">
      <BasePagination
        v-model="page"
        density="comfortable"
        :first-aria-label="$props.firstPageLabel"
        :last-aria-label="$props.lastPageLabel"
        :length="pageCount"
        :next-aria-label="$props.nextPageLabel"
        :previous-aria-label="$props.prevPageLabel"
        rounded
        show-first-last-page
        :total-visible="$props.showCurrentPage ? 1 : 0"
        variant="plain"
        v-bind="paginationProps"
      />
    </div>
  </div>
</template>