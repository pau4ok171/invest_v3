<script lang="ts">
import {defineComponent} from 'vue'
import {mapGetters} from "vuex";

export default defineComponent({
  name: "CompanyDetailShareholderReturnsTable",
  computed: {
    ...mapGetters({
      company: 'companyDetail/getCompany'
    }),
  },
  methods: {
    get_formatted_percent(value: number) {
      return `${(value * 100).toFixed(1)}%`
    },
    get_color_class(value: number) {
      if (value > 0) {
        return 'text--success'
      }
      if (value < 0) {
        return 'text--error'
      }
    }
  },
})
</script>

<template>
<table class="detail-shareholder-return__table" v-if="company.country && company.sector">
  <thead>
    <tr>
      <th></th>
      <th>{{ company.ticker.toUpperCase() }}</th>
      <th>{{ company.country.slug.toUpperCase() }} {{ company.sector.title }}</th>
      <th>{{ company.country.slug.toUpperCase() }} Market</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>7D</td>
      <td :class="get_color_class(company.return_7d)">{{ get_formatted_percent(company.return_7d) }}</td>
      <td :class="get_color_class(company.sector_market.return_7d)">{{ get_formatted_percent(company.sector_market.return_7d) }}</td>
      <td :class="get_color_class(company.market.return_7d)">{{ get_formatted_percent(company.market.return_7d) }}</td>
    </tr>
    <tr>
      <td>1Y</td>
      <td :class="get_color_class(company.return_1y)">{{ get_formatted_percent(company.return_1y) }}</td>
      <td :class="get_color_class(company.sector_market.return_1y)">{{ get_formatted_percent(company.sector_market.return_1y) }}</td>
      <td :class="get_color_class(company.market.return_1y)">{{ get_formatted_percent(company.market.return_1y) }}</td>
    </tr>
  </tbody>
</table>
</template>

<style scoped>
.detail-shareholder-return__table {
  width: 100%;
  color: rgba(255, 255, 255, .5);
  border-spacing: 0;
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, .1);
  margin-bottom: 16px;
}
.detail-shareholder-return__table tr {
  font-size: 1.2rem;
  line-height: 1.5;
  font-weight: 500;
}
.detail-shareholder-return__table tbody tr {
  font-size: 1.8rem;
}
.detail-shareholder-return__table th,
.detail-shareholder-return__table td {
  width: 25%;
  vertical-align: top;
  padding: 4px;
  border-bottom: 1px solid rgba(255, 255, 255, .1);
}
.detail-shareholder-return__table th:first-child,
.detail-shareholder-return__table td:first-child {
  width: 10%;
  padding-left: 8px;
}
.detail-shareholder-return__table tbody tr:last-child td {
  border-bottom: none;
}
.detail-shareholder-return__table th {
  font-weight: normal;
  text-align: left;
  line-height: 1.5;
}
</style>