<script lang="ts">
import { defineComponent } from 'vue'
import { BaseButton } from '@/apps/visagiste/components/BaseButton'
import { mapActions, mapGetters } from 'vuex'
import { BaseDialog } from '@/apps/visagiste/components/BaseDialog'
import BaseCard from '@/apps/visagiste/components/BaseCard/BaseCard.vue'
import BaseCardText from '@/apps/visagiste/components/BaseCard/BaseCardText.vue'
import BaseToolbar from '@/apps/visagiste/components/BaseToolbar/BaseToolbar.vue'
import BaseTextField from '@/apps/visagiste/components/BaseTextField/BaseTextField.vue'
import BaseSelect from '@/apps/visagiste/components/BaseSelect/BaseSelect.vue'

export default defineComponent({
  name: 'CompanyListFilters',
  components: {
    BaseSelect,
    BaseToolbar,
    BaseCardText,
    BaseCard,
    BaseDialog,
    BaseButton,
  },
  data() {
    return {
      dialog: false,
      country: { slug: 'global', title: 'Global' },
      sector: { slug: 'any', title: 'Any' },
    }
  },
  computed: {
    ...mapGetters({
      active_filters: 'companyList/getActiveFilters',
      filters: 'companyList/getFilters',
    }),
  },
  methods: {
    ...mapActions({
      changeFilter: 'companyList/changeFilter',
    }),
  },
  watch: {
    country(newVal) {
      this.changeFilter({ filter_name: 'country', object: newVal })
      this.country = this.active_filters.country
      this.sector = this.active_filters.sector
    },
    sector(newVal) {
      this.changeFilter({ filter_name: 'sector', object: newVal })
      this.country = this.active_filters.country
      this.sector = this.active_filters.sector
    },
  },
})
</script>

<template>
  <section class="company-list__filters">
    <div class="company-list__basic-filters">
      <base-select
        v-model="country"
        :items="filters.country"
        variant="outlined"
        density="compact"
        single-line
        item-title="title"
        item-value="slug"
        return-object
        hide-details
      />

      <base-select
        v-model="sector"
        :items="filters.sector"
        variant="outlined"
        density="compact"
        single-line
        item-value="slug"
        return-object
        hide-details
      />
    </div>

    <base-dialog v-model="dialog" max-width="500">
      <template #activator="{ props: activatorProps }">
        <base-button
          v-bind="activatorProps"
          text="advanced filters"
          append-icon="$iFilter"
          variant="text"
        />
      </template>

      <template #default>
        <base-card>
          <base-toolbar title="Advanced filters">
            <base-button variant="text" icon="$close" @click="dialog = false" />
          </base-toolbar>
          <base-card-text>TO BE ADDED</base-card-text>
        </base-card>
      </template>
    </base-dialog>
  </section>
</template>

<style>
.company-list__filters {
  display: grid;
  grid-template-columns: auto auto;
  grid-template-rows: 40px;
  justify-content: space-between;
  align-items: center;
  margin-top: 16px;
}
.company-list__basic-filters {
  display: grid;
  column-gap: 8px;
  grid-template-columns: auto auto;
}
</style>
