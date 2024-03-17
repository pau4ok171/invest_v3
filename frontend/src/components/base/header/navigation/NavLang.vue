<script setup lang="ts">

</script>

<template>
  <div class="navigation__nav-lang">
    <button class="nav-lang__nav-button">
      <span class="nav-button__flag"><img src="../../../../assets/img/flags/ru.svg" alt="RU"></span>
      <span class="nav-button__langcode">RU</span>
    </button>
  </div>
</template>

<style scoped>
  .navigation__nav-lang {
    position: relative;
    display: flex;
    align-items: center;
    padding: 0 16px;
  }

  .nav-lang__nav-button {
    display: flex;
    padding: 0 16px;
    line-height: 1.5;
  }

  .nav-button__flag {
    display: inline-block;
    font-size: 1.4rem;
  }

  .nav-button__flag img {
    height: 12px;
  }

  .nav-button__langcode {
    padding-left: 8px;
    color: #fff;
    font-size: 1.4rem;
  }
</style>