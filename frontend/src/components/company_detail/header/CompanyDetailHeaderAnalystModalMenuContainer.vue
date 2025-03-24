<script setup lang="ts">
// Components
import { BaseDialog } from '@/apps/visagiste/components/BaseDialog'
import { BaseButton } from '@/apps/visagiste/components/BaseButton'
import BaseCard from '@/apps/visagiste/components/BaseCard/BaseCard.vue'
import BaseCardText from '@/apps/visagiste/components/BaseCard/BaseCardText.vue'
import BaseDivider from '@/apps/visagiste/components/BaseDivider/BaseDivider.vue'
import BaseCardTitle from '@/apps/visagiste/components/BaseCard/BaseCardTitle.vue'

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
    <base-dialog v-model="dialog" title="Analyst Sources" max-width="700">
      <template #activator="{ props: activatorProps }">
        <base-button
          v-bind="activatorProps"
          class="text-capitalize text-decoration-underline"
          variant="text"
          :text="`${totalIdeas} Analysts`"
          size="small"
          density="comfortable"
        />
      </template>
      <template #default>
        <base-card title="Analysts">
          <template #append>
            <base-button
              icon="$close"
              density="compact"
              variant="text"
              @click="dialog = false"
            />
          </template>
          <base-card-title>
            {{ companyDetailStore.company.title }} is covered by
            {{ totalIdeas }} analysts.
          </base-card-title>
          <base-divider />
          <base-card-text>
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
          </base-card-text>
        </base-card>
      </template>
    </base-dialog>
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
