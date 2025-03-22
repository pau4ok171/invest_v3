<script setup lang="ts">
// Components
import BaseCard from '@/apps/visagiste/components/BaseCard/BaseCard.vue'
import BaseCardTitle from '@/apps/visagiste/components/BaseCard/BaseCardTitle.vue'
import BaseCardText from '@/apps/visagiste/components/BaseCard/BaseCardText.vue'
import BaseCardActions from '@/apps/visagiste/components/BaseCard/BaseCardActions.vue'
import BaseCardItem from '@/apps/visagiste/components/BaseCard/BaseCardItem.vue'
import BaseTable from '@/apps/visagiste/components/BaseTable/BaseTable.vue'
import BaseIcon from '@/apps/visagiste/components/BaseIcon/BaseIcon.vue'
import { BaseButton } from '@/apps/visagiste/components/BaseButton'

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
  <base-card color="surface-light" class="mb-4">
    <base-card-title>About the Company</base-card-title>

    <base-card-item>
      <base-table class="company-detail__about-company-table">
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
                <base-icon icon="$iExtraLink" />
              </a>
            </td>
            <td v-else>n/a</td>
          </tr>
        </tbody>
      </base-table>
    </base-card-item>

    <base-card-text>
      <div
        :class="[
          'company-detail-about-company__description',
          { 'company-detail-about-company__description--reduced': reduced },
        ]"
      >
        {{ description }}
      </div>
    </base-card-text>
    <base-card-actions>
      <base-button
        v-if="!!description"
        :text="reduced ? 'Show More' : 'Show Less'"
        color="info"
        rounded="large"
        size="small"
        @click="reduced = !reduced"
      />
    </base-card-actions>
  </base-card>
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
  background: linear-gradient(to bottom, rgba(0, 0, 0, 0), #1b222d 50%);
  width: 100%;
  height: 60px;
  opacity: 1;
  transition: 0.5s;
}
.company-detail__about-company-table {
  background: inherit;
}
</style>
