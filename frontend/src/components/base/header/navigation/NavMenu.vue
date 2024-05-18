<script lang="ts">
import {RoutesHeaderEnum} from "@/router/routes.types";
import {defineComponent} from "vue";

export default defineComponent({
  computed: {
    RoutesHeaderEnum() {
      return RoutesHeaderEnum
    }
  }
})
</script>

<template>
<div class="navigation__nav-menu" >
  <RouterLink
      v-for="routeName in RoutesHeaderEnum"
      :key="routeName"
      class="nav-menu__item"
      :to="{ name: routeName }"
  >
    {{ routeName }}
  </RouterLink>
</div>
</template>

<style scoped>
.navigation__nav-menu {
  display: flex;
  justify-content: center;
  align-items: center;
}
.nav-menu__item {
  font-size: 1.4rem;
  padding: 0 8px;
  display: inline-block;
  text-transform: capitalize;
  height: 64px;
  line-height: 64px;
}
</style>