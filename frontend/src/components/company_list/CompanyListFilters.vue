<script lang="ts">
import {defineComponent} from 'vue'
import BaseButton from "@/components/UI/base/components/BaseButton/BaseButton.vue";
import {mapActions, mapGetters} from "vuex";
import BaseMenu from "@/components/UI/base/components/BaseMenu/BaseMenu.vue";
import BaseList from "@/components/UI/base/components/BaseList/BaseList.vue";
import BaseDialog from "@/components/UI/base/components/BaseDialog/BaseDialog.vue";

export default defineComponent({
  name: "CompanyListFilters",
  components: {
    BaseList,
    BaseMenu,
    BaseButton
  },
  computed: {
    ...mapGetters({
      active_filters: "companyList/getActiveFilters",
      filters: "companyList/getFilters",
    }),
  },
  methods: {
    ...mapActions({
      changeFilter: "companyList/changeFilter"
    }),
    setActiveFilter(activeItem: any, filterName: string) {
      const activeFilter = {slug: activeItem.id, title: activeItem.title}
      this.changeFilter({filter_name: filterName, object:  activeFilter})
    }
  },
})
</script>

<template>
<section class="company-list__filters">

  <div class="company-list__basic-filters">

    <base-menu>
      <template #activator>
        <base-button
          :text="active_filters.country.title"
          append-icon="ArrowDownIcon"
          variant="outlined"
        />
      </template>
      <template #list>
        <base-list
          :active-item="{id: active_filters.country.slug, title: active_filters.country.title}"
          :items="filters.country.map((i: any) => ({id: i.slug, title: i.title}))"
          :has-search=true
          @setActiveItem="(activeItem: any) => setActiveFilter(activeItem, 'country')"
        />
      </template>
    </base-menu>

    <base-menu>
      <template #activator>
        <base-button
          :text="active_filters.sector.title"
          append-icon="ArrowDownIcon"
          variant="outlined"
        />
      </template>
      <template #list>
        <base-list
          :active-item="{id: active_filters.sector.slug, title: active_filters.sector.title}"
          :items="filters.sector.map((i: any) => ({id: i.slug, title: i.title}))"
          :has-search=true
          @setActiveItem="(activeItem: any) => setActiveFilter(activeItem, 'sector')"
        />
      </template>
    </base-menu>

  </div>

  <base-button
    text="advanced filters"
    append-icon="FilterIcon"
    variant="text"
    rounded="large"
  />

</section>
</template>

<style scoped>
.company-list__filters {
  display: grid;
  grid-template-columns: auto auto;
  grid-template-rows: 40px;
  justify-content: space-between;
  align-items: center;
  color: #92969c;
  margin-top: 16px;
}
.company-list__basic-filters {
  display: grid;
  column-gap: 8px;
  grid-template-columns: auto auto;
}
</style>