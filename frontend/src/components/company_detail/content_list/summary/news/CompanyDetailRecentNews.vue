<script lang="ts">
import {defineComponent} from 'vue'
import CompanyDetailNewsItem from "@/components/company_detail/content_list/summary/news/CompanyDetailNewsItem.vue";
import DetailSectionTitle from "@/components/UI/text/DetailSectionTitle.vue";
import {mapGetters} from "vuex";
import DetailNewsItemModalMenu from "@/components/company_detail/content_list/summary/news/DetailNewsItemModalMenu.vue";
import BaseLateralMenuContainer from "@/components/UI/lateral_menu/BaseLateralMenuContainer.vue";
import CompanyDetailNewsLateralMenu
  from "@/components/company_detail/content_list/summary/news/CompanyDetailNewsLateralMenu.vue";
import BaseButton from "@/apps/visagiste/components/BaseButton/BaseButton.vue";
import BaseDialog from "@/apps/visagiste/components/BaseDialog/BaseDialog.vue";
import {DateTime} from "luxon";
import type {News} from "@/types/invest";

export default defineComponent({
  name: "CompanyDetailRecentNews",
  components: {
    BaseDialog,
    BaseButton,
    CompanyDetailNewsLateralMenu,
    BaseLateralMenuContainer,
    DetailNewsItemModalMenu,
    DetailSectionTitle,
    CompanyDetailNewsItem,
  },
  computed: {
    ...mapGetters({
      company: 'companyDetail/getCompany',
    }),
  },
  methods: {
    getNewsTitle(news_item: News) {
      return DateTime.fromISO(news_item.date).toFormat('ccc, dd LLL yyyy')
    }
  },
})
</script>

<template>
<template v-if="company.company_news">
<div v-if="company.company_news.length">
  <DetailSectionTitle>Recent News & Updates</DetailSectionTitle>

  <div class="detail-recent-news detail__d-news">
    <base-dialog
      v-for="news_item in company.company_news"
      :key="news_item.id"
      max-width="700"
      :title="getNewsTitle(news_item)"
    >
      <template #activator>
        <CompanyDetailNewsItem :news_item/>
      </template>
      <template #dialog>
        <DetailNewsItemModalMenu :news_item/>
      </template>
    </base-dialog>
  </div>
  <BaseLateralMenuContainer>
    <template #button>
      <div class="detail-recent-news__button">
        <base-button
          text="See More Updated"
          theme="dark-blue"
          rounded="large"
          block
        />
      </div>
    </template>
    <template #menu="menuProps">
      <CompanyDetailNewsLateralMenu @closeMenu="menuProps.close()"/>
    </template>
  </BaseLateralMenuContainer>
</div>
</template>
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