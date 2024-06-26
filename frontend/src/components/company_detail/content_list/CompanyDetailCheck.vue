<script lang="ts">
import {defineComponent} from 'vue'
import CheckIcon from "@/components/icons/CheckIcon.vue";
import CrossIcon from "@/components/icons/CrossIcon.vue";
import {mapGetters} from "vuex";
import type {Statement} from "@/types/statements";

export default defineComponent({
  name: "CompanyDetailCheck",
  components: {
    CrossIcon,
    CheckIcon
  },
  props: {
    name: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      check: {
        area: '',
        company: 0,
        description: '',
        id: 0,
        level: '',
        name: '',
        question: '',
        severity: '',
        status: '',
        title: '',
        type: '',
        outcome: 0,
      } as Statement
    }
  },
  computed: {
    ...mapGetters({
      statements: 'companyDetail/getStatements',
    }),
    get_check() {
      const check: Statement = this.statements[this.name]
      if (check) {
        return check
      }
    },
  },
})
</script>

<template>
<blockquote class="analysis-section__point">
  <CheckIcon v-if="check.status === 'PASS'" class="icon--success"/>
  <CrossIcon v-else class="icon--error"/>

  <p class="analysis-section__point-text">
    <span class="analysis-section__point-title">{{ get_check?.title }}: </span>
    <span>{{ get_check?.description }}</span>
  </p>
</blockquote>
</template>

<style scoped>
.analysis-section__point {
  position: relative;
  display: flex;
  gap: 4px;
  margin-top: 8px;
}
.analysis-section__point-text {
  font-size: 1.6rem;
  line-height: 1.5;
  margin-bottom: 8px;
}
.icon--success {
  fill: #2dc97e;
}
.icon--error {
  fill: #e64141;
}
</style>