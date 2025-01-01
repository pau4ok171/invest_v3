<script lang="ts">
import BaseModalMenuContainer from "@/components/UI/modal_menu/BaseModalMenuContainer.vue";
import NavUserDropDown from "@/components/base/header/navigation/NavUserDropDown.vue";
import AuthModalMenu from "@/components/base/auth/AuthModalMenu.vue";
import {mapGetters} from "vuex";
import {defineComponent} from "vue";
import BaseButton from "@/components/UI/base/components/BaseButton/BaseButton.vue";
import BaseMenu from "@/components/UI/base/components/BaseMenu/BaseMenu.vue";

export default defineComponent({
  name: 'NavUser',
  components: {
    BaseMenu,
    BaseButton,
    AuthModalMenu,
    BaseModalMenuContainer,
    NavUserDropDown,
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
      <base-menu>
        <template #activator>
          <base-button
            icon="UserIcon"
            variant="text"
            rounded="x-small"
          />
        </template>
        <template #list>
          <NavUserDropDown/>
        </template>
      </base-menu>
    </template>
    <template v-else>
      <BaseModalMenuContainer>
        <template #button>
          <base-button
            text="login"
            rounded="large"
            theme="blue"
          />
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
  color: #92969c;
  justify-content: center;
  align-items: center;
  position: relative;
  height: 64px;
  padding-left: 8px;
  user-select: none;
  cursor: pointer;
}
</style>