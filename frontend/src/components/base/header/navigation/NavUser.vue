<template>
  <div class="navigation__account-access">
    <div class="account-access__inner">
      <template v-if="store.state.isAuthenticated">
        <button class="account-access__button" @click="toggleDropDownMenu">
          <span><UserIcon/></span>
          <span><ArrowDownIcon/></span>
        </button>
      </template>
      <template v-else>
        <button class="account-access__button--login" @click="openAuthModalMenu">Вход</button>
      </template>
    </div>

    <NavUserDropDown
        v-if="dropDownMenuIsActive"
        @closeDropDownMenu="closeDropDownMenu"
    />
  </div>
</template>

<script lang="ts">
import store from "@/store";
import UserIcon from "@/components/icons/UserIcon.vue";
import ArrowDownIcon from "@/components/icons/ArrowDownIcon.vue";
import NavUserDropDown from "@/components/base/header/navigation/NavUserDropDown.vue";

export default {
  name: 'NavUser',
  components: {NavUserDropDown, ArrowDownIcon, UserIcon},
  methods: {
    openAuthModalMenu() {
      store.commit('setAuthModalMenuIsActive', true)
    },
    toggleDropDownMenu() {
      this.dropDownMenuIsActive = !this.dropDownMenuIsActive
    },
    closeDropDownMenu() {
      this.dropDownMenuIsActive = false
    },
  },
  data() {
    return {
      dropDownMenuIsActive: false
    }
  },
  computed: {
    store () {
      return store
    },
  },
}
</script>

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
    display: flex;
    flex-direction: row;
    align-items: center;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 1;
  }
  .account-access__button span {
    pointer-events: none;
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

  .account-access__button svg {
    fill: #fff;
    width: 16px;
    height: 16px;
  }
</style>