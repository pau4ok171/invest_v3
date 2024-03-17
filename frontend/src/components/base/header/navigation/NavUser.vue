<script setup lang="ts">

</script>

<template>
  <div class="navigation__account-access">
    <div class="account-access__inner">
  <!--            {% if request.user.is_authenticated %}-->
  <!--            <button class="account-access__button"></button>-->
  <!--            <span class="account-access__user"><ion-icon name="person"></ion-icon></span>-->
  <!--            <span class="account-access__chevron"><ion-icon name="chevron-down"></ion-icon></span>-->
  <!--            {% else %}-->
      <button class="modal__initLoginButton account-access__button--login">Вход</button>
  <!--            {% endif %}-->
    </div>
  <!--          {% include 'invest/base/blocks/account-dropdown-menu.html' %}-->
  </div>
</template>

<style scoped>
  .navigation__account-access {
    position: relative;

  }

  .account-access__inner {
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
    height: 64px;
    padding-right: 24px;
    padding-left: 8px;
    user-select: none;
    cursor: pointer;
  }

  .account-access__button {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 1;
  }

  .account-access__button--login {
    font-size: 1.4rem;
    background-color: rgb(35, 148, 223);
    border-radius: 6px;
    height: 40px;
    font-weight: 500;
    line-height: 40px;
    color: #fff;
    padding: 0 16px;
  }
</style>