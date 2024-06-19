<script lang="ts">
import {defineComponent} from 'vue'
import BaseLateralMenu from "@/components/UI/lateral_menu/BaseLateralMenu.vue";
import {mapGetters} from "vuex";
import CompanyDetailNewsItem from "@/components/company_detail/content_list/summary/news/CompanyDetailNewsItem.vue";

export default defineComponent({
  name: "CompanyDetailNewsLateralMenu",
  components: {CompanyDetailNewsItem, BaseLateralMenu},
  computed: {
    ...mapGetters({
      company: 'companyDetail/getCompany',
    }),
  },
})
</script>

<template>
<BaseLateralMenu>
  <template #title>
    Notes
  </template>
  <template #content>
    <div class="detail-news-lateral-menu-content">
      <CompanyDetailNewsItem
        v-for="news in company.company_news"
        :key="news.id"
        :news_item="news"
      />
    </div>
  </template>
</BaseLateralMenu>
</template>

<style scoped>
.detail-news-lateral-menu-content {
    color: rgb(201, 203, 207);
    margin-left: -8px;
    margin-right: -8px;
    overflow: auto;
    height: calc(100% - 42px);
}
</style>