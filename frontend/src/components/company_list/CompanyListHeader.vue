<template>
  <header class="company-list__header">

    <section class="company-list__info">
      <div class="company-list__title">Largest {{ active_filters.country.title }} Stocks by {{ active_filters.sorter.title }}</div>
      <div class="company-list__updated"><span>Updated</span> {{ list_updated }}</div>
      <div class="company-list__description">
        Discover large cap {{ active_filters.country.title }} companies<template v-if="active_filters.country.markets"> that are on the {{ active_filters.country.markets[0].title }}</template>. These companies are organised by {{ active_filters.sorter.title }}.
      </div>
    </section>

    <section class="company-list__filters">

      <div class="company-list__basic-filters">
        <div class="company-list__basic-filter">
          <DropDownMenuBox>
            <template v-slot:button>
              <RoundedButton>
                <span>{{ active_filters.country.title }}</span>
                <ArrowDownIcon/>
              </RoundedButton>
            </template>
            <template v-slot:menu>
              <CompanyListFilterDropDownMenu
                  @changeFilter="changeFilter"
                  :objects="filters.country"
                  :active_object="active_filters.country"
                  :filter_name="`country`"
                  :hasSearch="true"
                  :inputValue="country_search_query"
                  @updateInput="updateCountrySearchQuery"
              />
            </template>
          </DropDownMenuBox>
        </div>

        <div class="company-list__basic-filter">
          <DropDownMenuBox>
            <template v-slot:button >
              <RoundedButton>
                <span>{{ active_filters.sector.title }}</span>
                <ArrowDownIcon/>
              </RoundedButton>

            </template>
            <template v-slot:menu>
              <CompanyListFilterDropDownMenu
                  @changeFilter="changeFilter"
                  :objects="filters.sector"
                  :active_object="active_filters.sector"
                  :filter_name="`sector`"
                  :hasSearch="true"
                  :inputValue="sector_search_query"
                  @updateInput="updateSectorSearchQuery"
              />
            </template>
          </DropDownMenuBox>
        </div>
      </div>

      <div>
        <BaseButton>
          <span>Advanced filters</span>
          <FilterIcon/>
        </BaseButton>
      </div>

    </section>

    <section class="company-list__options">
      <div class="company-list__sorter">
         <DropDownMenuBox>
            <template v-slot:button >
              <RoundedButton>
                 <span>{{ active_filters.sorter.title }}</span>
                <ArrowDownIcon/>
              </RoundedButton>
            </template>
            <template v-slot:menu>
              <CompanyListFilterDropDownMenu
                @changeFilter="changeFilter"
                :objects="filters.sorter"
                :active_object="active_filters.sorter"
                :filter_name="`sorter`"
              />
            </template>
          </DropDownMenuBox>
      </div>
      <div class="company-list__company-count"><p>{{ this.totalCompaniesLength }} companies</p></div>
      <div class="company-list__view-modes">
        <CircledButton disabled>
          <TableModeIcon/>
        </CircledButton>
        <CircledButton>
          <TileModeIcon/>
        </CircledButton>
      </div>
    </section>
  </header>
</template>

<script lang="ts">
import ArrowDownIcon from "@/components/icons/ArrowDownIcon.vue";
import FilterIcon from "@/components/icons/FilterIcon.vue";
import TableModeIcon from "@/components/icons/TableModeIcon.vue";
import TileModeIcon from "@/components/icons/TileModeIcon.vue";
import BaseButton from "@/components/UI/buttons/BaseButton.vue";
import CompanyListFilterDropDownMenu from "@/components/company_list/CompanyListFilterDropDownMenu.vue";
import DropDownMenuBox from "@/components/UI/DropDownMenuBox.vue";
import CircledButton from "@/components/UI/buttons/CircledButton.vue";
import RoundedButton from "@/components/UI/buttons/RoundedButton.vue";

export default {
  name: "CompanyListHeader",
  components: {
    RoundedButton,
    CircledButton,
    DropDownMenuBox,
    CompanyListFilterDropDownMenu, BaseButton, TileModeIcon, TableModeIcon, FilterIcon, ArrowDownIcon},
  props: {
    companies: {
      type: Array,
      required: true
    },
    filters: {
      type: Object,
      required: true,
      country: [],
      sector: [],
      sorter: [],
    },
    active_filters: {
      type: Object,
      required: true,
      country: {},
      sector: {},
      sorter: {},
    },
    list_updated: {
      type: String
    },
    totalCompaniesLength: Number,
    country_search_query: String,
    sector_search_query: String,
  },
  methods: {
    changeFilter(object: Object, filter_name: String) {
      if (filter_name === 'country') {
        this.active_filters.sector = this.filters.sector[0]
      }
      this.active_filters[`${filter_name}`] = object
      if (filter_name !== 'sorter') {
        this.$emit('fetchNewCompanies')
      }
    },
    updateCountrySearchQuery(value) {
      this.$emit('updateCountrySearchQuery', value)
    },
    updateSectorSearchQuery(value) {
      this.$emit('updateSectorSearchQuery', value)
      },
  },
}
</script>

<style scoped>
  .company-list__header {
    padding-bottom: 8px;
    border-bottom: 1px solid rgba(255, 255, 255, .1);
    display: grid;
  }
  .company-list__info {
    padding: 10px 0;
    display: grid;
    grid-row: 2 / auto;
  }
  .company-list__title {
    margin-bottom: 8px;
    font-size: 2.8rem;
    line-height: 1.25;
    font-weight: 500;
  }
  .company-list__updated {
    font-size: 1.2rem;
    line-height: 1.5;
  }
  .company-list__updated span {
    color: rgba(255, 255, 255, .7);
    text-transform: uppercase;
  }
  .company-list__description {
    margin-top: 16px;
    font-size: 1.4rem;
    line-height: 1.5;
    color: rgba(255, 255, 255, .5);
  }
  .company-list__filters {
    display: grid;
    grid-template-columns: auto auto;
    grid-template-rows: 40px;
    justify-content: space-between;
    align-items: center;
  }
  .company-list__basic-filters {
    display: grid;
    column-gap: 8px;
    grid-template-columns: auto auto;
  }
  .company-list__basic-filter {
    position: relative;
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, .2);
  }
  .company-list__options {
    display: grid;
    grid-template-columns: 250px auto 250px;
  }
  .company-list__sorter {
    position: relative;
  }
  .company-list__company-count {
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
    font-weight: normal;
    line-height: 1.5;
    color: rgba(255, 255, 255, .3);
  }
  .company-list__view-modes {
    display: grid;
    grid-template-columns: auto auto;
    justify-content: end;
  }
</style>