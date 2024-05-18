<script lang="ts">
import UserIcon from "@/components/icons/UserIcon.vue";
import ArrowDownIcon from "@/components/icons/ArrowDownIcon.vue";
import DropDownMenuBox from "@/components/UI/DropDownMenuBox.vue";
import RoundedButton from "@/components/UI/buttons/RoundedButton.vue";
import BaseModalMenuContainer from "@/components/UI/modal_menu/BaseModalMenuContainer.vue";
import NavUserDropDown from "@/components/base/header/navigation/NavUserDropDown.vue";
import AuthModalMenu from "@/components/base/auth/AuthModalMenu.vue";
import {mapGetters} from "vuex";
import {defineComponent} from "vue";

export default defineComponent({
  name: 'NavUser',
  components: {
    AuthModalMenu,
    BaseModalMenuContainer,
    RoundedButton,
    DropDownMenuBox,
    NavUserDropDown,
    ArrowDownIcon,
    UserIcon
  },
  computed: {
    ...mapGetters({
      isAuthenticated: 'authModule/getIsAuthenticated',
    })
  },
})
</script>

<template>
<div class="navigation__account-access">
  <div class="account-access__inner">
    <template v-if="isAuthenticated">
      <DropDownMenuBox>
        <template v-slot:button>
          <RoundedButton>
            <span><UserIcon/></span>
            <span><ArrowDownIcon/></span>
          </RoundedButton>
        </template>
        <template v-slot:menu>
          <NavUserDropDown/>
        </template>
      </DropDownMenuBox>
    </template>
    <template v-else>
      <BaseModalMenuContainer>
        <template #button>
          <button class="account-access__button">Вход</button>
        </template>
        <template #menu="menuProps">
          <AuthModalMenu @closeMenu="menuProps.close()"/>
        </template>
      </BaseModalMenuContainer>
    </template>
  </div>
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