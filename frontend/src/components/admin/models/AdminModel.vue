<script lang="ts">
import {defineComponent} from 'vue'
import type {AdminDetailCompany} from "@/types/admin";
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
      adminCompany: {
        id: null,
        ticker: null,
        slug: null,
        uid: null,
        title: null,
        shortTitle: null,
        isVisible: null,
        logo: null,
        isFund: null,
        marketName: null,
        sectorName: null,
        industryName: null,
        absoluteURL: null,
        country_flag: null,
        currencySymbol: null,
        created: null,
        updated: null,
      } as AdminDetailCompany
    }
  },
})
</script>

<template>
<div class="admin-model">
  <AdminModelHeader :adminCompany/>
  <AdminModelForm/>
</div>
</template>

<style scoped>
.admin-model {
  margin-top: 16px;
}
</style>