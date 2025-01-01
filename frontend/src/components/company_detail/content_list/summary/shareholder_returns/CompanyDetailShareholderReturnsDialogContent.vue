<script lang="ts">
import {defineComponent} from 'vue'
import {mapGetters} from "vuex";

interface Period {
  name: string,
  key: string,
}

export default defineComponent({
  name: "CompanyDetailShareholderReturnsModalMenu",
  data() {
    return {
      periods: [
        {name: '7 Day', key: 'return_7d'},
        {name: '30 Day', key: 'return_30d'},
        {name: '90 Day', key: 'return_90d'},
        {name: '1 Year', key: 'return_1y'},
        {name: '3 Year', key: 'return_3y'},
        {name: '5 Year', key: 'return_5y'},
      ] as Array<Period>
    }
  },
  computed: {
    ...mapGetters({
      company: "companyDetail/getCompany",
    }),
  },
  methods: {
    get_formatted_return(obj: Record<string, number>, p: Period) {
      const value = obj[p.key]
      return `${(value * 100).toFixed(1)}%`
    }
  },
})
</script>

<template>

<div class="detail-analysts-modal-menu__content">
  <table class="detail-analysts-modal-menu__table">
    <thead>
      <tr>
        <th></th>
        <th>{{ company.ticker }}</th>
        <th>Industry</th>
        <th>Market</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="p in periods" :key="p.key">
        <td class="detail-shareholder-returns-modal-menu__period_title">{{ p.name }}</td>
        <td>{{ get_formatted_return(company, p) }}</td>
        <td>{{ get_formatted_return(company.sector_market, p) }}</td>
        <td>{{ get_formatted_return(company.market, p) }}</td>
      </tr>
    </tbody>
  </table>
</div>

</template>

<style scoped>
.detail-analysts-modal-menu__content {
  padding: 32px 24px;
  width: 700px;
}
.detail-analysts-modal-menu__table {
  width: 100%;
  border-spacing: 0;
  border: 1px solid rgba(38, 46, 58, .2);
  font-size: 1.4rem;
  line-height: 1.5;
}
.detail-analysts-modal-menu__table tr {
  height: 40px;
}
.detail-analysts-modal-menu__table thead th {
  padding: 8px;
  vertical-align: top;
  background: rgba(38, 46, 58, .1);
  font-weight: 500;
  text-align: left;
}
.detail-analysts-modal-menu__table td {
  width: calc((100% - 35%)/4);
  padding: 8px;
  text-align: left;
  border-top: 1px solid rgba(38, 46, 58, .2);
  vertical-align: top;
}
.detail-analysts-modal-menu__table td:first-child {
  width: 35%;
}
.detail-shareholder-returns-modal-menu__period_title {
  font-size: 1.2rem;
}
</style>