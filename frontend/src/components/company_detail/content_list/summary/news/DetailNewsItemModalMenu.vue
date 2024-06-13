<script lang="ts">
import {defineComponent} from 'vue';
import type {PropType} from 'vue';
import BaseModalMenu from "@/components/UI/base/BaseModalMenu.vue";
import type {News} from "@/types/invest";
import {DateTime} from "luxon";

export default defineComponent({
  name: "DetailNewsItemModalMenu",
  components: {BaseModalMenu},
  props: {
    news_item: {
      type: Object as PropType<News>,
      required: true,
    },
  },
  computed: {
    formatted_date() {
      return DateTime.fromISO(this.news_item.date).toFormat('ccc, dd LLL yyyy')
    }
  },
})
</script>

<template>
<BaseModalMenu>
  <template #title>
    {{ formatted_date }}
  </template>
  <template #content>
    <section class="detail-news-item-modal-menu__content">
      <h3 class="detail-news-item-modal-menu__title">
        {{ news_item.title }}
      </h3>
      <p class="detail-news-item-modal-menu__body">
        {{ news_item.content }}
      </p>
    </section>
  </template>
</BaseModalMenu>
</template>

<style scoped>
.detail-news-item-modal-menu__content {
  background: white;
  color: black;
  overflow: hidden auto;
  font-size: 1.6rem;
  line-height: 1.5;
  padding: 32px 24px;
  margin-bottom: 56px;
}
.detail-news-item-modal-menu__title {
  color: black;
  font-weight: 700;
  line-height: 1.5;
  margin: 8px 0 16px;
  font-size: 2.4rem;
  padding-bottom: 16px;
  border-bottom: 1px solid rgb(232, 232, 232);
}
.detail-news-item-modal-menu__body {
  color: black;
  line-height: 1.7;
  margin-bottom: 16px;
  font-size: 1.6rem;
}
</style>