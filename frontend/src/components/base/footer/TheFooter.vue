<script setup lang="ts">
// Components
import Logo from '@/components/icons/Logo.vue'
import SmallLogo from '@/components/icons/SmallLogo.vue'

// Composables
import { usePageStore } from '@/store/page'
import { useI18n } from 'vue-i18n'

// Utilities
import { onMounted, onUnmounted, ref } from 'vue'

// Types
import type { VNodeRef } from 'vue'

const pages = [
  { name: 'About Us', to: 'aboutUs', key: 'aboutUs' },
  { name: 'Plan & Pricing', to: 'planPricing', key: 'planAndPricing' },
  { name: 'Articles', to: 'articles', key: 'articles' },
  { name: 'Help Center', to: 'helpCenter', key: 'helpCenter' },
  { name: 'Screener', to: 'screener', key: 'screener' },
  { name: 'Markets', to: 'markets', key: 'markets' },
]

const socials = [
  { icon: '$iXSocial', link: 'https://x.com/', key: 'x' },
  { icon: '$iTgSocial', link: 'https://telegram.org/', key: 'telegram' },
  { icon: '$iVkSocial', link: 'https://vk.ru/', key: 'vk' },
]

const store = usePageStore()
const footerRef = ref<VNodeRef | null>(null)
const { t } = useI18n()

onMounted(() => {
  if (!footerRef.value) return

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        store.footerOnViewport = entry.isIntersecting
      })
    },
    {
      root: null,
      rootMargin: '0px',
      threshold: 0.1,
    }
  )

  observer.observe(footerRef.value.$el)

  onUnmounted(() => {
    observer.disconnect()
  })
})
</script>

<template>
  <v-footer
    ref="footerRef"
    color="background"
    class="d-flex align-center justify-center"
  >
    <v-card color="background" width="1200" class="mt-8" flat>
      <v-card-item>
        <router-link :to="{ name: 'home' }"
          ><logo class="mb-8" style="height: 40px"
        /></router-link>
        <div class="mb-4">
          <v-btn
            v-for="page in pages"
            :key="page.key"
            :to="page.to"
            :text="t(`header.${page.key}`)"
            color="info"
            variant="plain"
          />
        </div>
        <p class="on-surface text-medium-emphasis text-caption mb-4">
          {{ t('footer.disclaimer') }}
        </p>
        <v-divider class="my-4" />
        <div class="d-flex justify-space-between">
          <div class="d-flex align-center">
            <router-link
              class="mr-4"
              style="height: 40px"
              :to="{ name: 'home' }"
              ><small-logo class="h-100"
            /></router-link>
            <span class="on-surface text-medium-emphasis text-caption"
              >© 2025 Finargo. {{ t('footer.rights') }}</span
            >
          </div>
          <div>
            <v-btn
              v-for="social in socials"
              :key="`social-${social.key}`"
              :icon="social.icon"
              :href="social.link"
              target="_blank"
              variant="plain"
            />
          </div>
        </div>
      </v-card-item>
    </v-card>
  </v-footer>
</template>
