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

<style>
.navigation__logo {
  font-size: 30px;
  font-weight: 900;
  user-select: none;
}
</style>