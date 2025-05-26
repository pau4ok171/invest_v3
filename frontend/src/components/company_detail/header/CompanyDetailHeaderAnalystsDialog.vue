<script setup lang="ts">
// Composables
import { useCompanyDetailStore } from '@/store/companyDetail'
import { useI18n } from 'vue-i18n'

// Utilities
import { computed, shallowRef } from 'vue'

const companyDetailStore = useCompanyDetailStore()
const { t } = useI18n()

const dialog = shallowRef(false)
const totalIdeas = computed(
  () => companyDetailStore.company.analyst_ideas.length
)
</script>

<template>
  <v-dialog activator="parent" v-model="dialog" max-width="700">
    <v-card :title="t('companyDetail.analysts.title')">
      <template #append>
        <v-btn
          icon="$close"
          density="compact"
          variant="text"
          @click="dialog = false"
        />
      </template>
      <v-card-title>
        {{
          t('companyDetail.analysts.subtitle', {
            title: companyDetailStore.company.title,
            n: totalIdeas,
          })
        }}
      </v-card-title>
      <v-divider />
      <v-card-item>
        <v-table>
          <thead>
            <tr>
              <th>{{ t('companyDetail.analysts.table.institution') }}</th>
              <th>{{ t('companyDetail.analysts.table.target') }}</th>
              <th>{{ t('companyDetail.analysts.table.score') }}</th>
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
