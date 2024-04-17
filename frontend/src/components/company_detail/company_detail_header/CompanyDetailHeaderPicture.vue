<script lang="ts">
import {defineComponent} from 'vue'
import {mapState} from "vuex";

export default defineComponent({
  name: "CompanyDetailHeaderPicture",
  computed: {
    ...mapState({
      company: state => state.companyDetail.company,
    }),
  },
})
</script>

<template>
  <picture class="detail-header__picture">
    <div class="detail-header__cover"></div>
    <img
      :src="this.company.sector.main_header"
      alt="Company background image"
    >
  </picture>
</template>

<style scoped>
  .detail-header__picture {
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 0;
  }
  .detail-header__cover {
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 1;
    background: rgba(21, 27, 36, .7);
  }
  .detail-header__picture img {
    border-radius: 0 0 8px 8px;
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
</style>