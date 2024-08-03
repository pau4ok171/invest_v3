<script lang="ts">
import {defineComponent} from 'vue'
import type {PropType} from "vue";
import type {AdminCompany} from "@/types/admin";
import AdminModelIndicator from "@/components/admin/models/AdminModelIndicator.vue";

export default defineComponent({
  name: "AdminModelsCompanyItem",
  components: {AdminModelIndicator},
  props: {
    company: {
      type: Object as PropType<AdminCompany>,
      required: true
    }
  }
})
</script>

<template>
<tr>
  <td>{{ company.id }}</td>
  <td>{{ company.title }}</td>
  <td>{{ company.slug.toUpperCase() }}</td>
  <td>
    <img
        :src="company.logo"
        class="admin-models-company-item__logo"
        alt="company"
    >
  </td>
  <td>{{ company.market_name }}</td>
  <td>{{ company.sector_name }}</td>
  <td><AdminModelIndicator :is-active="company.is_visible"/></td>
</tr>
</template>

<style scoped>
.admin-models-company-item__logo {
  background-color: #fff;
  border-radius: 8px;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-left: 4px;
}
</style>