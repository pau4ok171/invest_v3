<script setup lang="ts">
// Components
import { BaseButton } from '@/apps/visagiste/components/BaseButton'
import { BaseDialog } from '@/apps/visagiste/components/BaseDialog'
import BaseCard from '@/apps/visagiste/components/BaseCard/BaseCard.vue'
import BaseCardText from '@/apps/visagiste/components/BaseCard/BaseCardText.vue'
import BaseList from '@/apps/visagiste/components/BaseList/BaseList.vue'
import BaseListSubheader from "@/apps/visagiste/components/BaseList/BaseListSubheader.vue";
import BaseListItem from "@/apps/visagiste/components/BaseList/BaseListItem.vue";
import BaseIcon from "@/apps/visagiste/components/BaseIcon/BaseIcon.vue";
import BaseListItemTitle from "@/apps/visagiste/components/BaseList/BaseListItemTitle.vue";

// Composables
import { useCompanyDetailStore } from '@/store/companyDetail'

// Utilities
import { computed, shallowRef } from 'vue'
import BaseChip from "@/apps/visagiste/components/BaseChip/BaseChip.vue";
import BaseListItemSubtitle from "@/apps/visagiste/components/BaseList/BaseListItemSubtitle.vue";
import type {Statement} from "@/types/statements";
import BaseCardTitle from "@/apps/visagiste/components/BaseCard/BaseCardTitle.vue";
import type {DetailCompany} from "@/types/invest";

const companyDetailStore = useCompanyDetailStore()
const company = computed<DetailCompany>(() => companyDetailStore.company)

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

const items = computed<Statement[]>(() => [
  ...rewards.value,
  ...risks.value,
])
</script>

<template>
  <base-list bg-color="surface-light" class="mb-4">
    <base-list-subheader title="Rewards" class="text-uppercase" />
    <base-list-item v-for="item in rewards" :key="item.id">
      <template #prepend>
        <base-icon icon="$iSolidStar" color="success" />
      </template>
      <base-list-item-title>{{ item.description }}</base-list-item-title>
    </base-list-item>
    <base-list-subheader title="Risks" class="text-uppercase" />
    <base-list-item v-for="item in risks" :key="item.id">
      <template #prepend>
        <base-icon icon="$iAlert" :color="item.severity === 'MAJOR' ? 'error' : 'warning'" />
      </template>
      <base-list-item-title>{{ item.description }}</base-list-item-title>
    </base-list-item>
  </base-list>

  <base-dialog v-model="dialog" max-width="800">
    <template #activator="{ props: activatorProps }">
      <base-button
        v-bind="activatorProps"
        text="see all risks checks"
        color="info"
      />
    </template>
    <template #default>
      <base-card title="Risk Checks">
        <template #append>
          <base-button icon="$close" density="comfortable"  variant="text" @click="dialog = false" />
        </template>
        <base-card-text>
          We perform automated risk checks on every company. We flag any
          failed checks as potential investment risks. A company which passes
          all our checks, however, is not 'risk free'.
        </base-card-text>
        <base-card-text>
          <base-card-title>{{ company.title }} ({{ company.slug?.toUpperCase() }}) Risk Checks</base-card-title>
          <base-list lines="two">
            <base-list-item
              v-for="item in items"
              :key="item.id"
            >
              <template #prepend>
                <base-chip class="mr-3" :text="item.status" :color="item.status === 'PASS' ? 'success' : 'warning'" />
              </template>
              <base-list-item-title>{{ item.question }}</base-list-item-title>
              <base-list-item-subtitle>{{ item.description }}</base-list-item-subtitle>
              <template #append>
                <base-chip :text="item.type" label color="info"/>
              </template>
            </base-list-item>
          </base-list>
        </base-card-text>
      </base-card>
    </template>
  </base-dialog>
</template>
