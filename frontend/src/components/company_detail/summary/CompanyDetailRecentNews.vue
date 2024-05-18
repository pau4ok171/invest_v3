<script lang="ts">
import {defineComponent} from 'vue'
import RoundedDarkBlueButton from "@/components/UI/buttons/RoundedDarkBlueButton.vue";
import CompanyDetailNewsItem from "@/components/company_detail/summary/CompanyDetailNewsItem.vue";
import DetailSectionTitle from "@/components/UI/text/DetailSectionTitle.vue";

export default defineComponent({
  name: "CompanyDetailRecentNews",
  components: {DetailSectionTitle, CompanyDetailNewsItem, RoundedDarkBlueButton}
})
</script>

<template>
<DetailSectionTitle>Recent News & Updates</DetailSectionTitle>

<div class="detail-recent-news detail__d-news">

  <CompanyDetailNewsItem/>
  <CompanyDetailNewsItem/>
  <CompanyDetailNewsItem/>
  <CompanyDetailNewsItem/>
  <CompanyDetailNewsItem/>
  <CompanyDetailNewsItem/>

</div>

<div class="detail-recent-news__button">
  <RoundedDarkBlueButton :isFullWidth="true">See more updates</RoundedDarkBlueButton>
</div>
</template>

<style scoped>
.detail-recent-news {
  margin: 24px -8px 0 -8px;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  grid-template-rows: repeat(3, max-content);
  align-items: start;
}
.detail-recent-news__button {
  width: 100%;
  display: flex;
  flex: 0 0 100%;
  justify-content: center;
  padding-top: 16px;
}
</style>