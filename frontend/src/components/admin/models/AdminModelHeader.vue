<script lang="ts">
import {defineComponent} from 'vue'
import EditIcon from "@/components/icons/EditIcon.vue";
import RoundedDarkBlueButton from "@/components/UI/buttons/RoundedDarkBlueButton.vue";
import DeleteIcon from "@/components/icons/DeleteIcon.vue";
import AdminModelIndicator from "@/components/admin/models/AdminModelIndicator.vue";

export default defineComponent({
  name: "AdminModelHeader",
  components: {AdminModelIndicator, DeleteIcon, RoundedDarkBlueButton, EditIcon},
  props: {
    adminCompany: {
      type: Object as PropType<AdminDetailCompany>,
      required: true,
    },
  },
})
</script>

<template>
<div class="admin-model__admin-model-header">
  <div>
    <div class="admin-model-header__breadcrumbs">
      {{ adminCompany.sectorName?adminCompany.sectorName:'Sector'  }}
      /
      {{ adminCompany.industryName?adminCompany.industryName:'Industry' }}
    </div>
    <div class="admin-model-header__block-company-name">
      <div class="admin-header__logo-wrapper">
        <img class="admin-header__logo" :src="adminCompany.logo" alt="LOGO" v-if="adminCompany.logo">
        <span class="admin-header__logo-text" v-else>Logo</span>
      </div>
      <div>
        <div class="admin-model-header__company-name">{{ adminCompany.title?adminCompany.title:'Company Name' }}</div>
        <div class="admin-model-header__ticker">{{ adminCompany.ticker?adminCompany.ticker:'Ticker' }}</div>
      </div>
    </div>

    <div class="admin-model-header__item">{{ adminCompany.uid?adminCompany.uid:'0000-0000-0000-0000' }}</div>
    <div class="admin-model-header__item">Country</div>
    <div class="admin-model-header__item">Currency Symbol</div>
  </div>
  <div class="admin-model-header__last-column">
    <div class="admin-model-header__indicator">
      <AdminModelIndicator/>
    </div>

    <div class="admin-model-header__last-column-info">
      <div class="admin-model-header__item">Created: 00.00.0000 00:00:00</div>
      <div class="admin-model-header__item">Updated: 00.00.0000 00:00:00</div>
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