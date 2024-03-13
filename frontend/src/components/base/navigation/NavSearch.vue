<script setup lang="ts">

</script>

<template>
  <div class="navigation__nav-search">
  <div class="nav-search__inner">
    <input autocomplete="off" type="search" name="search-field" placeholder="Поиск по компаниям" class="nav-search__input" value>
    <span class="nav-search__prefix"><svg width="24" height="24" class="nav-search__prefix-icon"><use href="#search-icon"></use></svg></span>
    <span class="nav-search__postfix"><svg width="24" height="24" class="nav-search__postfix-icon none"><use href="#search-cross-icon"></use></svg></span>
  </div>
</div>
</template>

<style scoped>
  .navigation__nav-search {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-left: 24px;
    width: 271px;
  }
  .nav-search__inner {
    width: 100%;
    z-index: 1;
    background: transparent;
    position: relative;
  }
  .nav-search__input {
    padding: 14px 48px;
    appearance: none;
    border: 1px solid rgba(255, 255, 255, .2);
    font-size: 1.4rem;
    width: 100%;
    border-radius: 4px;
    background-color: rgba(255, 255, 255, .05);
    font-weight: normal;
    height: 40px;
    line-height: normal;
    caret-color: var(--blue);
    color: #fff;
    transition: border .2s ease 0s, background-color .2s ease 0s;
  }
  .nav-search__input:focus {
    outline: none;
    background: rgba(35, 148, 223, .05)
  }
  .nav-search__prefix {
      position: absolute;
    left: 12px;
    font-size: 20px;
    color: var(--blue);
    height: 40px;
    line-height: 41px;
  }
  .nav-search__prefix-icon {
      height: 100%;
      fill: #2394df;
  }
  .nav-search__postfix {
      position: absolute;
    right: 12px;
    font-size: 20px;
    color: var(--blue);
    height: 40px;
    line-height: 41px;
  }
  .nav-search__postfix-icon {
      fill: #fff;
      height: 100%;
      opacity: .5;
      cursor: pointer;
  }
  .nav-search__postfix-icon use {
    pointer-events: none;
  }
</style>