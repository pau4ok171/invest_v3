<script lang="ts">
import {defineComponent} from 'vue'
import RoundedDarkBlueButton from "@/components/UI/buttons/RoundedDarkBlueButton.vue";
import CompanyDetailNewsItem from "@/components/company_detail/summary/news/CompanyDetailNewsItem.vue";
import DetailSectionTitle from "@/components/UI/text/DetailSectionTitle.vue";
import {mapGetters} from "vuex";
import BaseModalMenuContainer from "@/components/UI/modal_menu/BaseModalMenuContainer.vue";
import DetailNewsItemModalMenu from "@/components/company_detail/summary/news/DetailNewsItemModalMenu.vue";

export default defineComponent({
  name: "CompanyDetailRecentNews",
  components: {
    DetailNewsItemModalMenu,
    BaseModalMenuContainer, DetailSectionTitle, CompanyDetailNewsItem, RoundedDarkBlueButton},
  computed: {
    ...mapGetters({
      company: 'companyDetail/getCompany',
    }),
  },
})
</script>

<template>
<div v-if="company.company_news.length">
  <DetailSectionTitle>Recent News & Updates</DetailSectionTitle>

  <div class="detail-recent-news detail__d-news">
    <BaseModalMenuContainer v-for="news_item in company.company_news" :key="news_item.id">
      <template #button>
        <CompanyDetailNewsItem :news_item/>
      </template>
      <template #menu="menuProps">
        <DetailNewsItemModalMenu @closeMenu="menuProps.close()" :news_item/>
      </template>
    </BaseModalMenuContainer>

  </div>

  <div class="detail-recent-news__button">
    <RoundedDarkBlueButton :isFullWidth="true">See more updates</RoundedDarkBlueButton>
  </div>
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