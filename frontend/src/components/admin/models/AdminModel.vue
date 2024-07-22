<script lang="ts">
import {defineComponent} from 'vue'
import RoundedDarkBlueButton from "@/components/UI/buttons/RoundedDarkBlueButton.vue";
import EditIcon from "@/components/icons/EditIcon.vue";
import DeleteIcon from "@/components/icons/DeleteIcon.vue";
import type {AdminDetailCompany} from "@/types/admin";
import AdminModelHeader from "@/components/admin/models/AdminModelHeader.vue";

export default defineComponent({
  name: "AdminModel",
  components: {AdminModelHeader, DeleteIcon, EditIcon, RoundedDarkBlueButton},
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
</div>
</template>

<style scoped>

</style>