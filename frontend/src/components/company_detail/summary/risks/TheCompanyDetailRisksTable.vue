<script lang="ts">
import {defineComponent} from 'vue'
import RoundedBorderedButton from "@/components/UI/buttons/RoundedBorderedButton.vue";
import RoundedWhiteButton from "@/components/UI/buttons/RoundedWhiteButton.vue";
import RoundedGreyButton from "@/components/UI/buttons/RoundedGreyButton.vue";
import RoundedHighGreyButton from "@/components/UI/buttons/RoundedHighGreyButton.vue";
import ArrowDownIcon from "@/components/icons/ArrowDownIcon.vue";
import TheCompanyDetailRisksTableItem
  from "@/components/company_detail/summary/risks/TheCompanyDetailRisksTableItem.vue";
import {mapGetters} from "vuex";

export default defineComponent({
  name: "TheCompanyDetailRisksTable",
  components: {
    TheCompanyDetailRisksTableItem,
    ArrowDownIcon, RoundedHighGreyButton, RoundedGreyButton, RoundedWhiteButton, RoundedBorderedButton
  },
  computed: {
    ...mapGetters({
      company: "companyDetail/getCompany",
      statements: "companyDetail/getStatements",
    })
  },
})
</script>

<template>
<table class="detail-risks-table">
  <thead>
    <tr>
      <th colspan="2">
        <div>{{ company.title }} ({{ company.slug.toUpperCase() }}) Risk Checks</div>
      </th>
    </tr>
  </thead>
  <tbody>
    <TheCompanyDetailRisksTableItem v-for="statement in statements" :statement :key="statement.id"/>
  </tbody>
</table>
</template>

<style>
.detail-risks-table {
    width: 100%;
    border: 1px solid rgba(38, 46, 58, .2);
    color: rgb(38, 46, 58);
}
.detail-risks-table tr {
    height: 40px;
}
.detail-risks-table th {
    color: rgb(38, 46, 58);
    padding: 8px;
    vertical-align: top;
    background: rgba(38, 46, 58, .1);
    line-height: 1.5;
    font-size: 1.6rem;
    width: 12.5%;
    text-align: left;
}
.detail-risks-table tbody tr {
    font-size: 1.4rem;
    line-height: 1.5;
}
.detail-risks-table td {
    padding: 8px;
    border-top: 1px solid rgba(38, 46, 58, .2);
    vertical-align: top;
}
.detail-risks-table td:first-child {
    text-align: right;
    width: 12.5%;
    color: rgb(38, 46, 58);
}
.detail-risks-table td:last-child {
    text-align: left;
    width: 87.5%;
}
</style>