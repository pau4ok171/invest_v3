<script lang="ts">
import {defineComponent} from 'vue'
import MegaphoneIcon from "@/components/icons/MegaphoneIcon.vue";

export default defineComponent({
  name: "CompanyDetailNewsItem",
  components: {MegaphoneIcon}
})
</script>

<template>
<button class="detail-recent-news__item">
  <article class="detail-recent-news__article">
    <div class="detail-recent-news__icon">
      <MegaphoneIcon/>
    </div>
    <div class="detail-recent-news__message">
      <h4 class="detail-recent-news__title">Sberbank of Russia to Report Q2, 2023 Results on Aug 03, 2023</h4>
      <span class="detail-recent-news__text">Jul 28</span>
    </div>
  </article>
</button>
</template>

<style>
.detail-recent-news__item {
  position: relative;
  border-radius: 8px;
  transition: all .3s ease 0s;
  padding: 0 12px;
  color: rgb(38, 46, 58);
  vertical-align: middle;
  height: auto;
  line-height: normal;
  background-color: inherit;
  text-align: left;
}
.detail-recent-news__item:hover {
  background-color: #262e3a;
}
.detail-recent-news__article {
  display: grid;
  gap: 12px;
  grid-template-columns: min-content auto;
  align-items: start;
  cursor: pointer;
  background: transparent;
  padding: 8px;
}
.detail-recent-news__icon {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 40px;
  width: 40px;
  position: relative;
}
.detail-recent-news__icon::before {
  content: "";
  width: 40px;
  height: 40px;
  border-radius: 50%;
  position: absolute;
  left: 0;
  top: 0;
  background-color: #8c929b;
  opacity: .1;
  z-index: 0;
}
.detail-recent-news__icon > svg {
  opacity: .5;
}
.detail-recent-news__message {
  display: grid;
  row-gap: 4px;
  font-size: 1.2rem;
  font-weight: normal;
  color: #fff;
  overflow: hidden;
  text-overflow: ellipsis;
  line-height: 1.5;
}
.detail-recent-news__title {
  font-size: 1.4rem;
  font-weight: normal;
}
.detail-recent-news__text {
  color: rgba(255, 255, 255, .5);
}
</style>