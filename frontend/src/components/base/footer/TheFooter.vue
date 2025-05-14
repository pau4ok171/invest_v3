<script setup lang="ts">
// Components
import Logo from '@/components/icons/Logo.vue'
import SmallLogo from '@/components/icons/SmallLogo.vue'

const pages = [
  { name: 'About Us', to: 'aboutUs', key: 'aboutUs' },
  { name: 'Plan & Pricing', to: 'planPricing', key: 'planPricing' },
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
</script>

<template>
  <v-footer class="d-flex align-center justify-center">
    <v-card width="1200" class="mt-8" flat>
      <v-card-item>
        <router-link :to="{ name: 'home' }"
          ><logo class="mb-8" style="height: 40px"
        /></router-link>
        <div class="mb-4">
          <v-btn
            v-for="page in pages"
            :key="page.key"
            :to="page.to"
            :text="page.name"
            color="info"
            variant="plain"
          />
        </div>
        <p class="on-surface text-medium-emphasis text-caption mb-4">
          Any advice contained in this website is general advice only and has
          been prepared without considering your objectives, financial situation
          or needs. You should not rely on any advice and/or information
          contained in this website and before making any investment decision we
          recommend that you consider whether it is appropriate for your
          situation and seek appropriate financial, taxation and legal advice.
          Please read our Financial Services Guide before deciding whether to
          obtain financial services from us.
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
              >© 2025 Finargo. All rights reserved.</span
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

<style scoped lang="scss"></style>
