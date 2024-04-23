<script lang="ts">
import {defineComponent} from 'vue'
import BaseModalMenu from "@/components/UI/base/BaseModalMenu.vue";
import RoundedGreyButton from "@/components/UI/buttons/RoundedGreyButton.vue";
import ModalMenuCloseIcon from "@/components/icons/ModalMenuCloseIcon.vue";
import {mapGetters, mapMutations} from "vuex";

export default defineComponent({
  name: "CompanyDetailAnalystsModalMenu",
  components: {ModalMenuCloseIcon, RoundedGreyButton, BaseModalMenu},
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

  <header class="detail-portfolio-modal-menu__header">
    <h1 class="detail-portfolio-modal-menu__title">Analyst Sources</h1>
    <RoundedGreyButton @click="setAnalystsModalMenuIsOpen(false)"><ModalMenuCloseIcon/></RoundedGreyButton>
  </header>

  <main class="detail-portfolio-modal-menu__main">
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
  </main>

</BaseModalMenu>
</template>

<style scoped>
.detail-portfolio-modal-menu__header {
  padding: 16px 24px;
  display: flex;
  justify-content: space-between;
  border-bottom: 1px solid #e8e8e8;
}
.detail-portfolio-modal-menu__title {
  font-size: 2rem;
  line-height: 1.5;
  font-weight: 500;
  color: #262e3a;
}
.detail-portfolio-modal-menu__main {
  padding: 32px 24px;
  border-bottom: 1px solid #e8e8e8;
  max-height: 392px;
  overflow-y: auto;
}
.detail-portfolio-modal-menu__main::-webkit-scrollbar {
  width: 10px;
}
.detail-portfolio-modal-menu__main::-webkit-scrollbar-track {
	-webkit-box-shadow: 5px 5px 5px -5px rgba(34, 60, 80, .2);
	background-color: #f9f9fd;
	border-radius: 10px;
}
.detail-portfolio-modal-menu__main::-webkit-scrollbar-thumb {
	border-radius: 10px;
	background: linear-gradient(180deg, #00c6fb, #005bea);
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