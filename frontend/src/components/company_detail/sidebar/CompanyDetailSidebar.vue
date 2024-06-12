<script lang="ts">
 import {mapGetters} from "vuex";
 import {defineComponent} from "vue";
 import CompanyDetailSidebarHeader from "@/components/company_detail/sidebar/CompanyDetailSidebarHeader.vue";
 import CompanyDetailSidebarMain from "@/components/company_detail/sidebar/CompanyDetailSidebarMain.vue";
 import CompanyDetailSidebarFooter from "@/components/company_detail/sidebar/CompanyDetailSidebarFooter.vue";

export default defineComponent({
  name: 'CompanyDetailSidebar',
  components: {
    CompanyDetailSidebarFooter,
    CompanyDetailSidebarMain,
    CompanyDetailSidebarHeader,
  },
  methods: {
    changeSidebarOpacity() {
      const opacity = String(this.calculateSidebarOpacity())
      const sidebar_header = this.$refs.sidebar_header as HTMLElement
      const sidebar_body = this.$refs.sidebar_main as HTMLElement

      sidebar_header.style.setProperty('opacity', opacity)
      sidebar_body.style.setProperty('opacity', opacity)

      if (Number(opacity) === 0) {
        sidebar_header.style.setProperty('visibility', 'hidden')
        sidebar_body.style.setProperty('visibility', 'hidden')
      } else {
        sidebar_header.style.setProperty('visibility', 'visible')
        sidebar_body.style.setProperty('visibility', 'visible')
      }
    },
    calculateSidebarOpacity(): Number {
      const scrollVisible = 25
      const scrollHidden = 200
      const scrollY = window.scrollY
      let opacity = 0

      if (scrollY < scrollHidden && scrollY > scrollVisible) {
        opacity = (scrollY - scrollVisible) /  (scrollHidden - scrollVisible)
        return opacity
      }
      if (scrollY <= scrollVisible) {
        opacity = 0
        return opacity
      }
      if (scrollY >= scrollHidden) {
        opacity = 1
        return opacity
      }
      return opacity
    },
  },
  mounted() {
    window.addEventListener('scroll', this.changeSidebarOpacity)
  },
  unmounted() {
    window.removeEventListener('scroll', this.changeSidebarOpacity)
  },
 })
</script>

<template>
<div class="detail-sidebar">
<section class="detail-sidebar__inner">

  <CompanyDetailSidebarHeader ref="sidebar_header"/>

  <CompanyDetailSidebarMain ref="sidebar_main"/>

  <CompanyDetailSidebarFooter/>

</section>
</div>
</template>

<style scoped>
.detail-sidebar {
  position: relative;
  width: 100%;
  min-height: 0;
  flex: 0 0 25%;
  max-width: 25%;
}
.detail-sidebar__inner {
  position: fixed;
  top: 80px;
  width: 298px;
  padding: 8px 24px 0 0;
}
</style>