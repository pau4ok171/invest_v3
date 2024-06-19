<script lang="ts">
import {defineComponent} from 'vue'
import CompanyDetailAboutCompanyTable from "@/components/company_detail/content_list/summary/CompanyDetailAboutCompanyTable.vue";
import CompanyDetailSection from "@/components/company_detail/content_list/CompanyDetailSection.vue";
import RoundedDarkBlueButton from "@/components/UI/buttons/RoundedDarkBlueButton.vue";
import DetailSectionTitle from "@/components/UI/text/DetailSectionTitle.vue";
import {mapGetters} from "vuex";

export default defineComponent({
  name: "CompanyDetailAboutCompany",
  components: {DetailSectionTitle, RoundedDarkBlueButton, CompanyDetailSection, CompanyDetailAboutCompanyTable},
  computed: {
    ...mapGetters({
      company: 'companyDetail/getCompany',
    }),
    get_description() {
      this.descriptionIsAvailable = !!this.company.description;
      return this.company.description
    },
  },
  data() {
    return {
      isCutting: true,
      descriptionIsAvailable: true
    }
  },
})
</script>

<template>
<CompanyDetailSection id="about-company-section">

  <DetailSectionTitle>About the Company</DetailSectionTitle>

  <CompanyDetailAboutCompanyTable/>
    <div class="detail-about-company__description" :class="{'detail-about-company__description--cut': isCutting}">
      {{ get_description }}
    </div>

  <div v-if="descriptionIsAvailable">
    <RoundedDarkBlueButton @click="isCutting=!isCutting" v-if="isCutting">Show more</RoundedDarkBlueButton>
    <RoundedDarkBlueButton @click="isCutting=!isCutting" v-else>Show less</RoundedDarkBlueButton>
  </div>

</CompanyDetailSection>
</template>

<style scoped>
.detail-about-company__description {
  position: relative;
  font-size: 1.6rem;
  line-height: 1.5;
  margin-bottom: 24px;
  transition: .5s ease-out;
}
.detail-about-company__description--cut {
  font-size: 1.6rem;
  line-height: 1.5;
  margin-bottom: 24px;
  max-height: 120px;
  overflow: hidden;
}
.detail-about-company__description--cut::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  background: linear-gradient(to bottom, rgba(0, 0, 0, 0), #1b222d 50%);
  width: 100%;
  height: 60px;
  opacity: 1;
  transition: 0.5s;
}
</style>