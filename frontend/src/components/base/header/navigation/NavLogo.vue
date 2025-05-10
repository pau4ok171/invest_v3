<script setup lang="ts">
// Components
import Logo from '@/components/icons/Logo.vue'
import SmallLogo from '@/components/icons/SmallLogo.vue'

// Composables
import { useDisplay } from 'vuetify'

const { mdAndDown } = useDisplay()
</script>

<template>
  <div class="navigation__logo h-100">
    <RouterLink
      :key="`home`"
      :to="{ name: `home` }"
      class="d-flex align-center h-100 w-100"
    >
      <small-logo style="height: 32px" v-if="mdAndDown" />
      <logo style="height: 32px" v-else />
    </RouterLink>
  </div>
</template>
