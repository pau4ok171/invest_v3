<template>
  <table class="company-list__table">
    <thead>
      <tr>
        <th></th>
        <th>Компания</th>
        <th>Последняя цена</th>
        <th>7Д Изменение</th>
        <th>1Г Изменение</th>
        <th>Капитализация</th>
        <th>Консенсус</th>
        <th>Стоимость</th>
        <th>Рост</th>
        <th>Дивиденд</th>
        <th>Сектор</th>
        <th></th>
      </tr>
    </thead>
    <tbody>
      <CompanyListItem
        v-for="company in companies"
        :key="company.uid"
        @toggleToWatchlist="toggleToWatchlist"
        :object="company"
      />
    </tbody>
  </table>
  <div class="observer" ref="observer"></div>
</template>

<script lang="ts">
import CompanyListItem from "@/components/company_list/CompanyListItem.vue";
import axios from "axios";

export default {
  name: 'CompanyListContent',
  components: {
    CompanyListItem,
  },
  props: {
    companies: {
      type: Array,
      required: true,
    },
    next_url: String,
  },
  emits: ['fetchMoreCompanies', 'toggleToWatchlist'],
  methods: {
    async toggleToWatchlist(object) {
      const formData = {
        uid: object.uid
      }
      if (object.is_watchlisted) {
        await axios
          .delete('/invest/api/v1/toggle_to_watchlist/', {
            data: formData
          })
          .then(response => this.$emit('toggleToWatchlist', {uid: object.uid, is_watchlisted: false}))
          .catch(error => console.log(error))
      } else {
        await axios
          .patch('/invest/api/v1/toggle_to_watchlist/', formData)
          .then(response => {this.$emit('toggleToWatchlist', {uid: object.uid, is_watchlisted: true})})
          .catch(error => console.log(error))
      }

    }
  },
  mounted() {
    const options = {
      rootMargin: "0px",
      threshold: 1.0,
    };
    const callback = (entries, observer) => {
      if (entries[0].isIntersecting && this.next_url !== null && this.companies.length) {
        this.$emit('fetchMoreCompanies')
      }
    }
    const observer = new IntersectionObserver(callback, options);
    observer.observe(this.$refs.observer)
  },
}
</script>

<style scoped>
  .company-list__table {
    min-width: 920px;
    width: 100%;
    table-layout: auto;
    border-spacing: 0;
    color: #fff;
  }
  .company-list__table thead {
    white-space: nowrap;
    text-align: left;
  }
  .company-list__table th {
    font-size: 1.2rem;
    line-height: 1.5;
    font-weight: 500;
    color: #fff;
    opacity: .5;
    border-bottom: 1px solid rgba(255, 255, 255, .1);
    position: sticky;
    background-color: var(--bg-color);
    padding: 10px 8px;
  }
  .company-list__table th:first-child {
    height: 55px;
    width: 56px;
  }
  .company-list__table th:nth-child(2) {
    width: 116px;
  }
  .company-list__table tr {
    height: auto;
  }
  .observer {
    width: 100%;
    height: 16px;
    background-color: inherit;
  }
</style>