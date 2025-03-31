<template>
<div class="navigation__logo">
  <RouterLink
    :key="`home`"
    :to="{ name: `home` }"
  >
    Finargo
  </RouterLink>
</div>
</template>

<style lang="scss">
.navigation__logo {
  font-size: 30px;
  font-weight: 900;
  user-select: none;
  color: rgb(var(--v-theme-on-background));
  text-decoration: none;

  > a {
    text-decoration: none;
    color: inherit;
  }
}
</style>