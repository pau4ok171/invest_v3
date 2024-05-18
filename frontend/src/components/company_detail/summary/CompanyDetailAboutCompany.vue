<script lang="ts">
import {defineComponent} from 'vue'
import CompanyDetailAboutCompanyTable from "@/components/company_detail/summary/CompanyDetailAboutCompanyTable.vue";
import CompanyDetailSection from "@/components/company_detail/CompanyDetailSection.vue";
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
  },
})
</script>

<template>
<CompanyDetailSection id="about-company-section">

  <DetailSectionTitle>About the Company</DetailSectionTitle>

  <CompanyDetailAboutCompanyTable/>

  <div class="detail-about-company__description">
    {{ company.description }}
  </div>

  <RoundedDarkBlueButton>Show more</RoundedDarkBlueButton>

</CompanyDetailSection>
</template>

<style scoped>
.detail-about-company__description {
  font-size: 1.6rem;
  line-height: 1.5;
  margin-bottom: 24px;
}
</style>