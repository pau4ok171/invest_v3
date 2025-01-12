<script lang="ts">
import {defineComponent} from 'vue'
import CompanyDetailAboutCompanyTable from "@/components/company_detail/content_list/summary/CompanyDetailAboutCompanyTable.vue";
import CompanyDetailSection from "@/components/company_detail/content_list/CompanyDetailSection.vue";
import DetailSectionTitle from "@/components/UI/text/DetailSectionTitle.vue";
import {mapGetters} from "vuex";
import BaseButton from "@/apps/visagiste/components/BaseButton/BaseButton.vue";

export default defineComponent({
  name: "CompanyDetailAboutCompany",
  components: {
    BaseButton,
    DetailSectionTitle,
    CompanyDetailSection,
    CompanyDetailAboutCompanyTable,
  },
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

  <base-button
    v-if="descriptionIsAvailable"
    :text="isCutting ? 'Show More' : 'Show Less'"
    theme="dark-blue"
    rounded="large"
    lower
    size="small"
    @click="isCutting=!isCutting"
  />

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