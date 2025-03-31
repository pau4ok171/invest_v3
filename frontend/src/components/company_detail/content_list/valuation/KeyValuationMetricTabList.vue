<script setup lang="ts">
// Composables
import { useCompanyDetailStore } from '@/store/companyDetail'

// Utilities
import { computed, ref, watch } from 'vue'

// Types
import type { PropType } from 'vue'
import type { FairValueTab } from '@/components/company_detail/content_list/valuation/CompanyDetailValuation.vue'

const props = defineProps({
  tabs: {
    type: Object as PropType<FairValueTab[]>,
    required: true,
  },
  selected: {
    type: Object as PropType<FairValueTab>,
    required: true,
  },
})

const store = useCompanyDetailStore()
const company = computed(() => store.company)
const emit = defineEmits()

const modelValue = ref(0)

watch(modelValue, (value) => {
  emit('update:selected', props.tabs[value])
})
</script>

<template>
  <div>
    <v-btn-toggle
      class="mb-4"
      v-model="modelValue"
      variant="outlined"
      density="comfortable"
      mandatory
      selected-class="text-info"
    >
      <v-btn
        v-for="tab in tabs"
        :key="`key-valuation-tab-${tab.id}`"
        :text="tab.name"
      />
    </v-btn-toggle>

      <div class="detail-key-valuation-metric__text">
        <p class="detail-key-valuation-metric__text-desc">
          <mark class="detail-key-valuation-metric__text-mark"
            >Key metric:
          </mark>
          <span>{{ selected.metric }}</span>
        </p>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.detail-key-valuation-metric__tab-list {
  display: grid;
  align-content: start;
}
.detail-key-valuation-metric__tab-button-list {
  display: grid;
  grid-template-columns: repeat(4, auto);
}
.detail-key-valuation-metric__tab-button {
  display: block;
  width: 100%;
  height: auto;
  border-top: 1px solid transparent;
  border-left: 1px solid transparent;
  border-right: 1px solid transparent;
  padding: 4px;
  font-size: 0.875rem;
  line-height: 1.5;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.3);
  border-radius: 4px;
}
.detail-key-valuation-metric__tab-button:disabled {
  color: rgb(255, 255, 255);
  background-color: rgba(0, 0, 0, 0.3);
  cursor: auto;
}
.detail-key-valuation-metric__tab-button:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.1);
}
.detail-key-valuation-metric__tab-desc {
  display: grid;
  grid-template-columns: 30px auto;
  grid-template-rows: auto;
  background-color: rgb(38, 46, 58);
  gap: 10px;
  padding: 10px;
  border-radius: 4px;
  height: min-content;
  margin-top: 16px;
}
.detail-key-valuation-metric__tab-icon {
  display: grid;
  justify-content: center;
}
.detail-key-valuation-metric__text {
  display: grid;
}
.detail-key-valuation-metric__text-desc {
  line-height: 1.5;
  font-size: 0.875rem;
}
.detail-key-valuation-metric__text-mark {
  background-color: transparent;
  color: var(--base-theme-info);
}
</style>
