<script setup lang="ts">
// Components
import GoogleAuthButton from '@/components/base/auth/social/GoogleAuthButton.vue'
import YandexAuthButton from '@/components/base/auth/social/YandexAuthButton.vue'
import GithubAuthButton from "@/components/base/auth/social/GithubAuthButton.vue";
</script>

<template>
  <v-card-item>
    <div class="d-flex flex-column ga-4 px-16">
      <google-auth-button />

      <yandex-auth-button />

      <github-auth-button />
    </div>
  </v-card-item>
</template>
