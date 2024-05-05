<template>
  <table class="company-list-table">
    <thead>
      <tr>
        <th class="company-list-table__empty"></th>
        <th v-for="h in headers" :key="h.name" @click="setSort(h.name)">
          <div>{{ h.title }}</div>
          <div class="company-list-table__icon-box">
          <template v-if="sort.key === h.name">
            <SortUpIcon v-if="sort.reverse"/>
            <SortDownIcon v-else/>
          </template>
          </div>
        </th>
        <th class="company-list-table__empty"></th>
      </tr>
    </thead>
    <tbody>
      <CompanyListItem
        v-for="company in companiesSorted"
        :key="company.uid"
        :object="company"
      />
    </tbody>
  </table>
  <div class="observer" ref="observer"></div>
</template>

<script lang="ts">
import CompanyListItem from "@/components/company_list/CompanyListItem.vue";
import {mapActions, mapGetters} from "vuex";
import SortUpIcon from "@/components/icons/SortUpIcon.vue";
import SortDownIcon from "@/components/icons/SortDownIcon.vue";

export default {
  name: 'CompanyListContent',
  data() {
    return {
      headers: [
        {name: 'company_name', title: 'Компания'},
        {name: 'last_price', title: 'Цена'},
        {name: 'return_7d', title: '7Д Изм'},
        {name: 'return_1y', title: '1Г Изм'},
        {name: 'market_cap', title: 'Капитализация'},
        {name: 'consensus', title: 'Консенсус'},
        {name: 'fair_value', title: 'Стоимость'},
        {name: 'growth', title: 'Рост'},
        {name: 'dividend_yield', title: 'Дивиденд'},
        {name: 'sector', title: 'Сектор'},
      ],
      sort: {
        key: 'company_name',
        reverse: 0,
        options: {
          company_name: (a, b) => a.title.localeCompare(b.title),
          last_price: (a, b) => a.price_data.last_price - b.price_data.last_price,
          return_7d: (a, b) => a.price_data.return_7d - b.price_data.return_7d,
          return_1y: (a, b) => a.price_data.return_1y - b.price_data.return_1y,
          market_cap: (a, b) => a.price_data.capitalisation - b.price_data.capitalisation,
          consensus: (a, b) => a.title.localeCompare(b.title),
          fair_value: (a, b) => a.title.localeCompare(b.title),
          growth: (a, b) => a.title.localeCompare(b.title),
          dividend_yield: (a, b) => a.title.localeCompare(b.title),
          sector: (a, b) => a.sector.title.localeCompare(b.sector.title),
        }
      },
    }
  },
  components: {
    SortDownIcon,
    SortUpIcon,
    CompanyListItem,
  },
  computed: {
    ...mapGetters({
      companies: "companyList/getCompanies",
      next_url: "companyList/getNextURL",
    }),
    companiesSorted() {
      const { sort: {key, options, reverse} } = this
      const compare = options[key]
      return [...this.companies].sort((a, b) => compare(a, b) * (reverse ? -1 : 1))
    }
  },
  methods: {
    ...mapActions({
      fetchMoreCompanies: "companyList/fetchCompanies",
    }),
    setSort(key) {
      const { sort } = this;
      if (sort.options[key]) {
        sort.reverse = (sort.key === key) ^ sort.reverse;
        sort.key = key;
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
        this.fetchMoreCompanies()
      }
    }
    const observer = new IntersectionObserver(callback, options);
    observer.observe(this.$refs.observer)
  },
}
</script>

<style scoped>
.company-list-table {
  min-width: 920px;
  width: 100%;
  table-layout: auto;
  border-spacing: 0;
  color: #fff;
}
.company-list-table thead {
  white-space: nowrap;
  text-align: left;
}
.company-list-table th {
  font-size: 1.2rem;
  line-height: 1.5;
  font-weight: 500;
  color: #fff;
  opacity: .5;
  border-bottom: 1px solid rgba(255, 255, 255, .1);
  position: sticky;
  cursor: pointer;
  background-color: var(--bg-color);
  padding: 10px 8px;
}
.company-list-table th > * {
  display: inline-block;
}
.company-list-table th.company-list-table__empty {
  cursor: default;
}
.company-list-table th:hover {
  background-color: var(--header-color);
}
.company-list-table th.company-list-table__empty:hover {
  background-color: var(--bg-color);
}
.company-list-table th:first-child {
  height: 55px;
  width: 56px;
}
.company-list-table th:nth-child(2) {
  width: 116px;
}
.company-list-table__icon-box {
  width: 16px;
  height: 16px;
  margin-left: 2px;
}
.company-list-table th svg {
  width: 16px;
  height: 16px;
}
.company-list-table tr {
  height: auto;
}
.observer {
  width: 100%;
  height: 16px;
  background-color: inherit;
}
</style>