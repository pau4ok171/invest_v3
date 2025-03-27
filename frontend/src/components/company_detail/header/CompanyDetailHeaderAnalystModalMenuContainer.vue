<script setup lang="ts">
// Composables
import { useCompanyDetailStore } from '@/store/companyDetail'

// Utilities
import { computed, shallowRef } from 'vue'

const companyDetailStore = useCompanyDetailStore()

const dialog = shallowRef(false)
const totalIdeas = computed(
  () => companyDetailStore.company.analyst_ideas.length
)
</script>

<template>
  <div class="detail-analyst__modal-menu-container">
    <v-dialog v-model="dialog" title="Analyst Sources" max-width="700">
      <template #activator="{ props: activatorProps }">
        <v-btn
          v-bind="activatorProps"
          class="text-capitalize text-decoration-underline"
          variant="text"
          :text="`${totalIdeas} Analysts`"
          size="small"
          density="comfortable"
        />
      </template>
      <template #default>
        <v-card title="Analysts">
          <template #append>
            <v-btn
              icon="$close"
              density="compact"
              variant="text"
              @click="dialog = false"
            />
          </template>
          <v-card-title>
            {{ companyDetailStore.company.title }} is covered by
            {{ totalIdeas }} analysts.
          </v-card-title>
          <v-divider />
          <v-card-text>
            <table class="detail-analysts-modal-menu__table">
              <thead>
                <tr>
                  <th>Institution</th>
                  <th>Target</th>
                  <th>Score</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="idea in companyDetailStore.company.analyst_ideas"
                  :key="idea.id"
                >
                  <td>{{ idea.analyst.name }}</td>
                  <td>{{ idea.price_target }}{{ idea.currency.symbol }}</td>
                  <td>{{ idea.analyst.score }}/5</td>
                </tr>
              </tbody>
            </table>
          </v-card-text>
        </v-card>
      </template>
    </v-dialog>
  </div>
</template>

<style scoped>
.detail-analyst__modal-menu-container {
  margin-bottom: -1px;
  margin-left: -4px;
}
.detail-analysts-modal-menu__table {
  width: 100%;
  border-spacing: 0;
  border: 1px solid rgba(38, 46, 58, 0.2);
  font-size: 0.875rem;
  line-height: 1.5;
}
.detail-analysts-modal-menu__table tr {
  height: 40px;
}
.detail-analysts-modal-menu__table thead th {
  padding: 8px;
  vertical-align: top;
  background: rgba(38, 46, 58, 0.1);
  font-weight: 500;
  text-align: left;
}
.detail-analysts-modal-menu__table td {
  padding: 8px;
  text-align: left;
  border-top: 1px solid rgba(38, 46, 58, 0.2);
  vertical-align: top;
}
.detail-analysts-modal-menu__table th:last-child,
.detail-analysts-modal-menu__table td:last-child {
  text-align: right;
}
</style>
