<script lang="ts">
import {defineComponent} from 'vue'
import ExtraLinkIcon from "@/components/icons/ExtraLinkIcon.vue";
import {mapGetters} from "vuex";

export default defineComponent({
  name: "CompanyDetailAboutCompanyTable",
  components: {ExtraLinkIcon},
  computed: {
    ...mapGetters({
      company: 'companyDetail/getCompany',
    }),
    year_founded() {
      return this.company.year_founded ? this.company.year_founded : 'n/a'
    },
    total_employees_figure() {
      return this.company.reports.length ? this.humanize_number(this.company.reports[0].total_employees_figure) : 'n/a'
    }
  },
  methods: {
    humanize_number(val: number) {
      return new Intl.NumberFormat('en-EN').format(val)
    },
  },
})
</script>

<template>
<table class="detail-about-company-table">
  <thead>
    <tr>
      <th>Founded</th>
      <th>Employees</th>
      <th>CEO</th>
      <th>Website</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>{{ year_founded }}</td>
      <td>{{ total_employees_figure }}</td>
      <td>n/a</td>
      <td v-if="company.website">
        <a target="_blank"
           class="detail-about-company-table__extra-link"
           href="{{ company.website }}"
           rel="noopener noreferrer nofollow"
        >
          {{ company.website }}
          <ExtraLinkIcon/>
        </a>
      </td>
      <td v-else>
        n/a
      </td>
    </tr>
  </tbody>
</table>
</template>

<style scoped>
.detail-about-company-table {
  margin-left: -1px;
  margin-bottom: 16px;
}
.detail-about-company-table th {
  font-size: 1.4rem;
  color: rgba(255, 255, 255, .7);
}
.detail-about-company-table td {
  font-size: 1.6rem;
  font-weight: 500;
  line-height: 1.5;
}
.detail-about-company-table__extra-link {
  text-decoration: underline;
  color: var(--blue);
  transition: all .3s ease 0s;
}
.detail-about-company-table__extra-link svg {
  fill: var(--blue);
  display: inline-block;
  vertical-align: bottom;
  width: 20px;
  height: 20px;
  margin-bottom: 4px;
}
</style>