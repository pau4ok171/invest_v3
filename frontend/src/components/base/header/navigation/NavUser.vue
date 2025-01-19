<script lang="ts">
import NavUserDropDown from "@/components/base/header/navigation/NavUserDropDown.vue";
import AuthModalMenu from "@/components/base/auth/AuthModalMenu.vue";
import {mapGetters} from "vuex";
import {defineComponent} from "vue";
import BaseButton from "@/apps/visagiste/components/BaseButton/BaseButton.vue";
import BaseMenu from "@/apps/visagiste/components/BaseMenu/BaseMenu.vue";
import BaseDialog from "@/apps/visagiste/components/BaseDialog/BaseDialog.vue";

export default defineComponent({
  name: 'NavUser',
  components: {
    BaseDialog,
    BaseMenu,
    BaseButton,
    AuthModalMenu,
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
<div class="nav-user__wrapper">
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
    <base-dialog
      max-width="700"
      footer-type="withoutFooter"
    >
      <template #activator>
        <base-button
          text="login"
          rounded="large"
          theme="blue"
        />
      </template>
      <template #dialog>
        <AuthModalMenu/>
      </template>
    </base-dialog>
  </template>
</div>
</template>

<style>
.nav-user__wrapper {
  display: flex;
  justify-content: center;
  min-width: 90px;
}

</style>
