<script lang="ts">
import {defineComponent} from 'vue'
import BaseModalMenu from "@/components/UI/base/BaseModalMenu.vue";
import {mapGetters, mapMutations} from "vuex";

export default defineComponent({
  name: "CompanyDetailAnalystsModalMenu",
  components: {
    BaseModalMenu
  },
  computed: {
    ...mapGetters({
      company: "companyDetail/getCompany",
    }),
    totalIdeas() {
      return this.company.analyst_ideas.length
    },
  },
   methods: {
    ...mapMutations({
      setAnalystsModalMenuIsOpen: 'companyDetail/setAnalystsModalMenuIsOpen',
    }),
  },
})
</script>

<template>
<BaseModalMenu>

  <template #title>
    Analyst Sources
  </template>

  <template #content>
  <div class="detail-analysts-modal-menu__content">
    <div class="detail-analysts-modal-menu__description">
      {{ company.title }} is covered by {{ totalIdeas }} analysts.
    </div>
    <table class="detail-analysts-modal-menu__table">
      <thead>
        <tr>
          <th>Institution</th>
          <th>Target</th>
          <th>Score</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="analyst in company.analyst_ideas" :key="analyst.id">
          <td>{{ analyst.analyst.name }}</td>
          <td>{{ analyst.price_target }}{{ analyst.currency.symbol }}</td>
          <td>{{ analyst.analyst.score }}/5</td>
        </tr>
      </tbody>
    </table>
  </div>
  </template>

</BaseModalMenu>
</template>

<style scoped>
.detail-analysts-modal-menu__content {
  padding: 32px 24px;
}
.detail-analysts-modal-menu__description {
  font-size: 1.6rem;
  line-height: 1.7;
  margin-bottom: 24px;
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
  padding: 8px;
  text-align: left;
  border-top: 1px solid rgba(38, 46, 58, .2);
  vertical-align: top;
}
.detail-analysts-modal-menu__table th:last-child,
.detail-analysts-modal-menu__table td:last-child {
  text-align: right;
}
</style>