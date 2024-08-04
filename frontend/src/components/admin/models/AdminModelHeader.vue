<script lang="ts">
import {defineComponent} from 'vue'
import EditIcon from "@/components/icons/EditIcon.vue";
import RoundedDarkBlueButton from "@/components/UI/buttons/RoundedDarkBlueButton.vue";
import DeleteIcon from "@/components/icons/DeleteIcon.vue";
import AdminModelIndicator from "@/components/admin/models/AdminModelIndicator.vue";
import {mapState} from "vuex";
import {DateTime} from "luxon";
import type {FormattedDetailCompany} from "@/types/admin";

export default defineComponent({
  name: "AdminModelHeader",
  components: {AdminModelIndicator, DeleteIcon, RoundedDarkBlueButton, EditIcon},
  methods: {
    getURLFromFile(image: File): string {
      try {
        return URL.createObjectURL(image)
      } catch {
        return ''
      }
    },
    getFormattedDate(isoDateTime: string) {
      return DateTime.fromISO(isoDateTime).toFormat('dd LLL yyyy')
    }
  },
  computed: {
    ...mapState({
      companyFormData: state => state.adminModule.companyFormData as FormattedDetailCompany,
    }),
  },
})
</script>

<template>
<div class="admin-model__admin-model-header">
  <div>
    <div class="admin-model-header__breadcrumbs">
      {{ companyFormData.sector.slug?companyFormData.sector.name:'Sector'  }}
      /
      {{ companyFormData.industry.slug?companyFormData.industry.name:'Industry' }}
    </div>
    <div class="admin-model-header__block-company-name">
      <div class="admin-header__logo-wrapper">
        <img class="admin-header__logo" :src="getURLFromFile(companyFormData.logo)" alt="LOGO" v-if="companyFormData.logo?.size">
        <span class="admin-header__logo-text" v-else>Logo</span>
      </div>
      <div>
        <div class="admin-model-header__company-name">{{ companyFormData.companyName?companyFormData.companyName:'Company Name' }}</div>
        <div class="admin-model-header__ticker">
          <span>{{ companyFormData.market.slug?companyFormData.market.slug.toUpperCase():'Market' }}</span>
          <span>:</span>
          <span>{{ companyFormData.ticker?companyFormData.ticker:'Ticker' }}</span>
        </div>
      </div>
    </div>

    <div class="admin-model-header__item">{{ companyFormData.uid?companyFormData.uid:'0000-0000-0000-0000' }}</div>
    <div class="admin-model-header__item">
      <img class="admin-model-header__country-flag-icon" :src="companyFormData.country.flagURL" alt="Country" v-if="companyFormData.country.flagURL">
      {{ companyFormData.country.slug?companyFormData.country.name:'Country' }}
    </div>
    <div class="admin-model-header__item">{{ companyFormData.country.currency?.name?`${companyFormData.country.currency.name} (${companyFormData.country.currency.symbol})`:'Currency Symbol' }}</div>
  </div>
  <div class="admin-model-header__last-column">
    <div class="admin-model-header__indicator">
      <AdminModelIndicator :is-active="companyFormData.isVisible"/>
    </div>

    <div class="admin-model-header__last-column-info">
      <div class="admin-model-header__item">Created: {{ companyFormData.created?getFormattedDate(companyFormData.created):'00.00.0000 00:00:00' }}</div>
      <div class="admin-model-header__item">Updated: {{ companyFormData.updated?getFormattedDate(companyFormData.updated):'00.00.0000 00:00:00' }}</div>
    </div>

    <div class="admin-model-header__action-list">
      <div class="admin-model-header__item">
        <RoundedDarkBlueButton>
          <EditIcon/>
          <span>Edit</span>
        </RoundedDarkBlueButton>
      </div>
      <div class="admin-model-header__item">
        <RoundedDarkBlueButton>
          <DeleteIcon/>
          <span>Delete</span>
        </RoundedDarkBlueButton>
      </div>
    </div>
  </div>
</div>
</template>

<style scoped>
.admin-model__admin-model-header {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 8px;
  background-color: #1b222d;
  width: 100%;
  min-height: 200px;
  border-radius: 8px;
  margin-bottom: 16px;
  padding: 16px 32px;
}
.admin-model-header__breadcrumbs {
  margin-bottom: 2.4rem;
  font-size: 1.4rem;
}
.admin-model-header__block-company-name {
  padding-bottom: 10px;
}
.admin-header__logo-wrapper {
  margin: 4px 12px 0 0;
  float: left;
  background-color: #92969c;
  border-radius: 8px;
  height: 56px;
  width: 56px;
}
.admin-header__logo-text {
  font-size: 1.4rem;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}
.admin-header__logo {
  width: 56px;
  height: 56px;
  min-width: 56px;
  min-height: 56px;
  border: 1px solid #fff;
  background-color: #fff;
  border-radius: 8px;
  object-fit: scale-down;
  vertical-align: text-bottom;
}
.admin-model-header__company-name {
  font-size: 2.8rem;
  line-height: 1.25;
  font-weight: 500;
  overflow: hidden;
}
.admin-model-header__ticker {
  font-size: 1.6rem;
  line-height: 1.5;
  color: rgba(255, 255, 255, .7);
}
.admin-model-header__item {
  font-size: 1.4rem;
  margin-bottom: 5px;
}
.admin-model-header__last-column {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
.admin-model-header__last-column-info {
  display: flex;
  flex-direction: column;
  align-items: end;
}
.admin-model-header__action-list {
  display: flex;
  justify-content: end;
  gap: 8px;
}
.admin-model-header__indicator {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: end;
}
</style>