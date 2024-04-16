<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "CompanyDetailShareholderReturnsTable"
})
</script>

<template>
  <table class="detail-shareholder-return__table">
    <thead>
      <tr>
        <th></th>
        <th>SBER</th>
        <th>RU Banks</th>
        <th>RU Market</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>7D</td>
        <td>0%</td>
        <td>0%</td>
        <td>0%</td>
      </tr>
      <tr>
        <td>1Y</td>
        <td class="text--error">-63.2%</td>
        <td class="text--error">-60.5%</td>
        <td class="text--error">-38.2%</td>
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