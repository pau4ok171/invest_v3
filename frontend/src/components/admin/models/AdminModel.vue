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
})
</script>

<template>
<div class="admin-model">
  <AdminModelHeader/>
  <AdminModelForm/>
</div>
</template>

<style scoped>
.admin-model {
  margin-top: 16px;
}
</style>