<script lang="ts">
import { defineComponent } from 'vue'
import AdminModelsCompanyItem from '@/components/admin/models/AdminModelsCompanyItem.vue'
import axios from 'axios'
import type { IAdminCompany } from '@/types/admin.types'

export default defineComponent({
  name: 'AdminModels',
  components: {
    AdminModelsCompanyItem,
  },
  data() {
    return {
      companies: {} as Array<IAdminCompany>,
      isFetched: false,
    }
  },
  mounted() {
    this.fetchCompanies()
    this.isFetched = true
  },
  methods: {
    fetchCompanies() {
      axios
        .get('api/v1/admin/companies/')
        .then((response) => (this.companies = response.data))
        .catch((error) => console.log(error))
    },
  },
})
</script>

<template>
  <div class="admin-models">
    <div class="admin-models__header">
      <h1>Select Company to change</h1>
      <v-btn
        text="add company"
        color="info"
        rounded="lg"
        size="small"
        @click="$emit('openModel', '')"
      />
    </div>
    <div v-if="isFetched" class="admin-models__content-list">
      <table>
        <thead>
          <tr>
            <th>Id</th>
            <th>Title</th>
            <th>Slug</th>
            <th>Logo</th>
            <th>Market</th>
            <th>Sector</th>
            <th>Visible</th>
          </tr>
        </thead>
        <tbody>
          <AdminModelsCompanyItem
            v-for="company in companies"
            :key="company.id"
            :company
            @click="$emit('openModel', company.uid)"
          />
        </tbody>
      </table>
    </div>
  </div>
</template>

<style>
.admin-models {
  padding: 20px 0;
}
.admin-models__header {
  display: flex;
  justify-content: space-between;
}
.admin-models__content-list {
  width: 100%;
  margin-top: 20px;
}
.admin-models__content-list table {
  width: 100%;
  table-layout: auto;
  border-spacing: 0;
  color: #fff;
}
.admin-models__content-list table thead {
  white-space: nowrap;
  text-align: left;
}
.admin-models__content-list table th {
  font-size: 0.75rem;
  line-height: 1.5;
  font-weight: 500;
  color: #fff;
  opacity: 0.5;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  position: sticky;
  cursor: pointer;
  background-color: var(--bg-color);
  padding: 10px 8px;
}
.admin-models__content-list table th > * {
  display: inline-block;
}
.admin-models__content-list table th:hover {
  background-color: var(--header-color);
}
.admin-models__content-list table th:first-child {
  height: 55px;
  width: 56px;
}
.admin-models__content-list table th:nth-child(2) {
  width: 116px;
}
.admin-models__content-list table th svg {
  width: 16px;
  height: 16px;
}
.admin-models__content-list table tr {
  height: auto;
}
.admin-models__content-list table tbody tr {
  font-size: 0.875rem;
  font-weight: normal;
  line-height: 1.5;
  transition: background-color 0.2s cubic-bezier(0.23, 1, 0.32, 1) 0s;
}
.admin-models__content-list table tbody tr:hover {
  background-color: rgba(255, 255, 255, 0.05);
}
.admin-models__content-list table td {
  background-color: transparent;
  font-size: 0.875rem;
  height: 64px;
  border-top: none;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  vertical-align: middle;
  padding: 10px 8px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  cursor: pointer;
}
</style>