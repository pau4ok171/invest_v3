<script setup lang="ts">
// Components
import CompanyDetailSidebarHeader from '@/components/company_detail/sidebar/CompanyDetailSidebarHeader.vue'
import CompanyDetailSidebarMain from '@/components/company_detail/sidebar/CompanyDetailSidebarMain.vue'
import CompanyDetailSidebarFooter from '@/components/company_detail/sidebar/CompanyDetailSidebarFooter.vue'

// Utilities
import { onMounted, onUnmounted, ref } from 'vue'
import { debounce } from '@/apps/visagiste/utils'

const headerRef = ref<InstanceType<typeof CompanyDetailSidebarHeader>>()
const bodyRef = ref<InstanceType<typeof CompanyDetailSidebarMain>>()

function changeOpacity() {
  const opacity = String(calculateOpacity())

  if (!headerRef.value || !bodyRef.value) return

  headerRef.value.$el.style.setProperty('opacity', opacity)
  bodyRef.value.$el.style.setProperty('opacity', opacity)

  headerRef.value.$el.style.setProperty(
    'clip-path',
    `inset(${(1 - Number(opacity)) * 100}% 0px 0px)`
  )
}

function calculateOpacity() {
  const scrollVisible = 25
  const scrollHidden = 200
  const scrollY = window.scrollY
  let opacity = 0

  if (scrollY < scrollHidden && scrollY > scrollVisible) {
    opacity = (scrollY - scrollVisible) / (scrollHidden - scrollVisible)
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
}

onMounted(() => {
  window.addEventListener('scroll', debounce(changeOpacity, 1))
})

onUnmounted(() => {
  window.removeEventListener('scroll', debounce(changeOpacity, 1))
})
</script>

<template>
  <div class="detail-sidebar">
    <section class="detail-sidebar__inner">
      <CompanyDetailSidebarHeader ref="headerRef" />

      <CompanyDetailSidebarMain ref="bodyRef" />

      <CompanyDetailSidebarFooter />
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
}
</style>
