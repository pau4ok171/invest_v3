<script setup lang="ts">
// Composables
import { useCompanyDetailStore } from '@/store/companyDetail'

// Utilities
import { computed } from 'vue'

const props = defineProps({
  name: {
    type: String,
    required: true,
  },
})

const store = useCompanyDetailStore()
const statement = computed(() => store.statements[props.name])
const title = computed(() => statement.value?.title || '')
const description = computed(() => statement.value?.description || '')
</script>

<template>
  <section class="detail-statement">
    <blockquote class="detail-statement-item">
      <p class="detail-statement-item__text">
        <span :class="statement?.status === 'PASS' ? 'text-success' : 'text-error'">{{ title }}: </span>
        <span>{{ description }}</span>
      </p>
    </blockquote>
  </section>
</template>

<style scoped>
.detail-statement {
  margin-top: 24px;
}
.detail-statement-item {
  position: relative;
  margin-top: 8px;
  text-align: left;
}
.detail-statement-item__text {
  font-size: 1rem;
  line-height: 1.5;
}
</style>
