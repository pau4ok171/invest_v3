<script setup lang="ts">
// Composables
import { useCompanyDetailStore } from '@/store/companyDetail'

// Utilities
import { computed, shallowRef } from 'vue'

// Types
import type { DetailCompany } from '@/types/invest'

const store = useCompanyDetailStore()
const company = computed<DetailCompany>(() => store.company)

const description = computed(() => company.value.description)
const reduced = shallowRef(true)

function humanize(val: number | string) {
  if (typeof val === 'string') return val

  return new Intl.NumberFormat('en-EN').format(val)
}
</script>

<template>
  <v-card id="about-company-section" color="surface-light" class="mb-4">
    <v-card-title>About the Company</v-card-title>

    <v-card-item>
      <v-table class="company-detail__about-company-table">
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
            <td>{{ company.year_founded || 'n/a' }}</td>
            <td>
              {{
                humanize(
                  company.reports.length
                    ? company.reports[0].total_employees_figure
                    : 'n/a'
                )
              }}
            </td>
            <td>n/a</td>
            <td v-if="company.website">
              <a
                target="_blank"
                class="detail-about-company-table__extra-link"
                :href="company.website"
                rel="noopener noreferrer nofollow"
              >
                {{ company.website }}
                <v-icon icon="$iExtraLink" />
              </a>
            </td>
            <td v-else>n/a</td>
          </tr>
        </tbody>
      </v-table>
    </v-card-item>

    <v-card-text>
      <div
        :class="[
          'company-detail-about-company__description',
          { 'company-detail-about-company__description--reduced': reduced },
        ]"
      >
        {{ description }}
      </div>
    </v-card-text>
    <v-card-actions>
      <v-btn
        v-if="!!description"
        :text="reduced ? 'Show More' : 'Show Less'"
        color="info"
        rounded="large"
        size="small"
        @click="reduced = !reduced"
      />
    </v-card-actions>
  </v-card>
</template>

<style lang="scss" scoped>
.company-detail-about-company__description {
  position: relative;
  line-height: 1.5;
  transition: 0.5s ease-out;
}
.company-detail-about-company__description--reduced {
  line-height: 1.5;
  max-height: 120px;
  overflow: hidden;
}
.company-detail-about-company__description--reduced::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  background: linear-gradient(to bottom, rgb(0, 0, 0, 0), rgb(var(--v-theme-surface-light)) 50%);
  width: 100%;
  height: 60px;
  opacity: 1;
  transition: 0.5s;
}
.company-detail__about-company-table {
  background: inherit;
}
</style>
