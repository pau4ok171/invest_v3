<script lang="ts">
import {defineComponent} from 'vue'
import CompanyDetailStatementItem from "@/components/company_detail/CompanyDetailStatementItem.vue";

export default defineComponent({
  name: "CompanyDetailStatement",
  components: {CompanyDetailStatementItem},
  props: {
    statement_list: {
      type: Object,
      required: true,
    }
  }
})
</script>

<template>
  <section class="detail-statement">

    <CompanyDetailStatementItem v-for="statement in statement_list" :key="statement.id" :statement/>

  </section>
</template>

<style scoped>
  .detail-statement {
    margin-top: 24px;
  }
</style>