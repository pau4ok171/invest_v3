<script setup lang="ts">
// Composables
import { useCompanyDetailStore } from '@/store/companyDetail'
import { useI18n } from 'vue-i18n'

// Utilities
import { computed, shallowRef } from 'vue'

// Types
import type { Statement } from '@/types/statements'
import type { DetailCompany } from '@/types/invest'

const companyDetailStore = useCompanyDetailStore()
const company = computed<DetailCompany>(() => companyDetailStore.company)
const { t } = useI18n()

const dialog = shallowRef(false)

const risks = computed(() =>
  Object.values(companyDetailStore.statements)
    .filter(
      (item) =>
        item.type === 'RISKS' && item.status === 'FAIL' && item.outcome > 1000
    )
    .sort((s1) => (s1.severity === 'MAJOR' ? -1 : 1))
)

const rewards = computed(() =>
  Object.values(companyDetailStore.statements).filter(
    (item) =>
      item.type === 'REWARDS' && item.status === 'PASS' && item.outcome > 1000
  )
)

const items = computed<Statement[]>(() => [...rewards.value, ...risks.value])
</script>

<template>
  <v-list bg-color="surface-light" class="mb-4">
    <v-list-subheader title="Rewards" class="text-uppercase" />
    <v-list-item v-for="item in rewards" :key="item.id">
      <template #prepend>
        <v-icon icon="$iSolidStar" color="success" />
      </template>
      <v-list-item-title>{{ item.description }}</v-list-item-title>
    </v-list-item>
    <v-list-subheader title="Risks" class="text-uppercase" />
    <v-list-item v-for="item in risks" :key="item.id">
      <template #prepend>
        <v-icon
          icon="$iAlertCircle"
          :color="item.severity === 'MAJOR' ? 'error' : 'warning'"
        />
      </template>
      <v-list-item-title>{{ item.description }}</v-list-item-title>
    </v-list-item>
  </v-list>

  <v-dialog v-model="dialog" max-width="800">
    <template #activator="{ props: activatorProps }">
      <v-btn
        v-bind="activatorProps"
        :text="t('buttons.seeAllRisksChecks')"
        color="info"
        variant="tonal"
      />
    </template>
    <template #default>
      <v-card title="Risk Checks">
        <template #append>
          <v-btn
            icon="$close"
            density="comfortable"
            variant="text"
            @click="dialog = false"
          />
        </template>
        <v-card-text>
          We perform automated risk checks on every company. We flag any failed
          checks as potential investment risks. A company which passes all our
          checks, however, is not 'risk free'.
        </v-card-text>
        <v-card-text>
          <v-card-title
            >{{ company.title }} ({{ company.slug?.toUpperCase() }}) Risk
            Checks</v-card-title
          >
          <v-list lines="two">
            <v-list-item v-for="item in items" :key="item.id">
              <template #prepend>
                <v-chip
                  class="mr-3"
                  :text="item.status"
                  :color="item.status === 'PASS' ? 'success' : 'warning'"
                />
              </template>
              <v-list-item-title>{{ item.question }}</v-list-item-title>
              <v-list-item-subtitle>{{
                item.description
              }}</v-list-item-subtitle>
              <template #append>
                <v-chip :text="item.type" label color="info" />
              </template>
            </v-list-item>
          </v-list>
        </v-card-text>
      </v-card>
    </template>
  </v-dialog>
</template>
