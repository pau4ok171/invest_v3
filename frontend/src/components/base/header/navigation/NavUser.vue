<template>
  <div class="navigation__account-access">
    <div class="account-access__inner">
      <template v-if="store.state.isAuthenticated">
        <DropDownMenuBox>
          <template v-slot:button>
            <span><UserIcon/></span>
            <span><ArrowDownIcon/></span>
          </template>
          <template v-slot:menu>
            <NavUserDropDown/>
          </template>
        </DropDownMenuBox>
      </template>
      <template v-else>
        <button class="account-access__button" @click="openAuthModalMenu">Вход</button>
      </template>
    </div>

  </div>
</template>

<script lang="ts">
import store from "@/store";
import UserIcon from "@/components/icons/UserIcon.vue";
import ArrowDownIcon from "@/components/icons/ArrowDownIcon.vue";
import NavUserDropDown from "@/components/base/header/navigation/NavUserDropDown.vue";
import DropDownMenuBox from "@/components/UI/DropDownMenuBox.vue";

export default {
  name: 'NavUser',
  components: {DropDownMenuBox, NavUserDropDown, ArrowDownIcon, UserIcon},
  methods: {
    openAuthModalMenu() {
      store.commit('setAuthModalMenuIsActive', true)
    },
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
    padding-left: 8px;
    user-select: none;
    cursor: pointer;
  }
  .account-access__button {
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