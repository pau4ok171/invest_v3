<script lang="ts">
import {defineComponent} from 'vue'
import CompanyDetailDropDownMenu from "@/components/company_detail/content_list/CompanyDetailDropDownMenu.vue";

export default defineComponent({
  name: "MultiplierVsPeersTabListDropDownMenu",
  components: {CompanyDetailDropDownMenu},
  data() {
    return {
      objects: [
        {title: 'Price to Earnings', slug: 'price-to-earnings', isChosen: true},
        {title: 'Price to Sales', slug: 'price-to-sales', isChosen: false},
        {title: 'Price to Book', slug: 'price-to-book', isChosen: false},
      ]
    }
  }
})
</script>

<template>
<CompanyDetailDropDownMenu :objects/>
</template>
