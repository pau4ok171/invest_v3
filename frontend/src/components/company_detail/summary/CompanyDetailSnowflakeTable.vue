<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "CompanyDetailSnowflakeTable"
})
</script>

<template>
  <div>
    <table class="snowflake-table">
      <caption class="table__caption">SBER fundamental analysis</caption>
      <thead>
        <tr>
          <th colspan="2">Showflake Score</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Value</td>
          <td>3/6</td>
        </tr>
        <tr>
          <td>Future</td>
          <td>4/6</td>
        </tr>
        <tr>
          <td>Past</td>
          <td>5/6</td>
        </tr>
        <tr>
          <td>Health</td>
          <td>1/6</td>
        </tr>
        <tr>
          <td>Dividend</td>
          <td>1/6</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
  .snowflake-table {
    font-size: 1.2rem;
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, .5);
  }
  .snowflake-table caption {
    caption-side: bottom;
    text-align: left;
    font-size: 1.2rem;
    font-weight: normal;
    color: rgba(255, 255, 255, .5);
    line-height: 1.5;
    padding: 8px 8px 0 0;
  }
  .snowflake-table tr {
    height: 32px;
  }
  .snowflake-table th {
	text-align: left;
	line-height: 1.5;
  font-weight: 500;
  border-bottom: 1px solid rgba(255, 255, 255, .5);
  vertical-align: top;
  padding: 8px;
  }
  .snowflake-table td {
    border-bottom: 1px solid rgba(255, 255, 255, .5);
    vertical-align: top;
    padding: 8px;
  }
  .snowflake-table td:last-child {
    text-align: right;
  }

</style>