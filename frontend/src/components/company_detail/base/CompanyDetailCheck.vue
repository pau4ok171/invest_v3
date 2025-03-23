<script setup lang="ts">
// Components
import BaseIcon from '@/apps/visagiste/components/BaseIcon/BaseIcon.vue'

// Composables
import { useCompanyDetailStore } from '@/store/companyDetail'

// Utilities
import { computed } from 'vue'

// Types
import type { Statement } from '@/types/statements'

const props = defineProps({
  name: {
    type: String,
    required: true,
  },
})

const store = useCompanyDetailStore()
const statements = computed(() => store.statements)

const check = computed<Statement | undefined>(
  () => statements.value[props.name]
)
</script>

<template>
  <blockquote class="company-detail-check">
    <base-icon
      class="fill-rule-evenodd"
      :icon="check?.status === 'PASS' ? '$iCheck' : '$iCross'"
      :color="check?.status === 'PASS' ? 'success' : 'error'"
    />

    <p class="company-detail-check__text">
      <span :class="check?.status === 'PASS' ? 'text-success' : 'text-error'">
        {{ check?.title }}:
      </span>
      <span>{{ check?.description }}</span>
    </p>
  </blockquote>
</template>

<style scoped>
.company-detail-check {
  position: relative;
  display: flex;
  gap: 4px;
  margin-top: 8px;
}
.company-detail-check__text {
  line-height: 1.5;
  margin-bottom: 8px;
}
.fill-rule-evenodd {
  > svg > path {
    fill-rule: evenodd;
  }
}
</style>
