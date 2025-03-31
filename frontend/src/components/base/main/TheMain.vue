<script setup lang="ts"></script>

<template>
  <v-main class="main">
    <div class="main__inner">
      <slot />
    </div>
  </v-main>
</template>

<style lang="scss">
.main {
  display: flex;
  position: relative;
  flex-wrap: wrap;
  max-width: 100%;
  flex: 1 0 auto;
  justify-content: center;
  transition: 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}
.main__inner {
  position: relative;
  max-width: 1200px;
  display: flex;
  flex-direction: column;
  width: 100%;
}
</style>
