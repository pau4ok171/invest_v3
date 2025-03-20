<script lang="ts">
import { defineComponent } from 'vue'
import { BaseButton } from '@/apps/visagiste/components/BaseButton/'

export default defineComponent({
  name: 'BaseLateralMenu',
  components: {
    BaseButton,
  },
})
</script>

<template>
  <div class="base-lateral-menu">
    <div class="base-lateral-menu__inner">
      <header class="base-lateral-menu__header">
        <h3 class="base-lateral-menu__title">
          <slot name="title" />
        </h3>
        <base-button
          icon="$close"
          variant="text"
          color="#92969c"
          rounded="x-small"
          density="comfortable"
          @click="$emit('closeMenu')"
        />
      </header>
      <main class="base-lateral-menu__main">
        <slot name="content" />
      </main>
    </div>
  </div>
</template>

<style>
.base-lateral-menu {
  position: fixed;
  left: 1368px;
  top: 76px;
  right: 4px;
  width: 377px;
  height: calc(-88px + 100vh);
  overflow: hidden;
  color: rgb(201, 203, 207);
}
.base-lateral-menu__inner {
  position: relative;
  height: 100%;
  background-color: rgb(27, 34, 45);
  padding: 16px;
  border-radius: 8px;
}
.base-lateral-menu__header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}
.base-lateral-menu__title {
  font-size: 2rem;
  font-weight: normal;
  color: rgb(255, 255, 255);
  line-height: 1.5;
}
</style>