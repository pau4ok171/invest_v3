<script lang="ts">
import {defineComponent} from 'vue'
import AdminModelHeader from "@/components/admin/models/AdminModelHeader.vue";
import AdminModelForm from "@/components/admin/models/AdminModelForm.vue";

export default defineComponent({
  name: "AdminModel",
  components: {
    AdminModelForm,
    AdminModelHeader
  },
  data() {
    return {
      editModeActivated: false,
    }
  },
})
</script>

<template>
<div class="admin-model">
  <AdminModelHeader v-model:edit-mode-activated="editModeActivated"/>
  <AdminModelForm v-model:edit-mode-activated="editModeActivated"/>
</div>
</template>

<style scoped>
.admin-model {
  margin-top: 16px;
}
</style>