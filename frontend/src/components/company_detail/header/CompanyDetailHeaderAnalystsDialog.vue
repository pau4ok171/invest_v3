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
  <v-dialog
    activator="parent"
    v-model="dialog"
    title="Analyst Sources"
    max-width="700"
  >
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
      <v-card-item>
        <v-table>
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
              <td>
                <v-rating
                  length="5"
                  :model-value="idea.analyst.score"
                  readonly
                  density="compact"
                  active-color="info"
                  color="warning"
                />
              </td>
            </tr>
          </tbody>
        </v-table>
      </v-card-item>
    </v-card>
  </v-dialog>
</template>
