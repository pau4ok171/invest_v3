<script lang="ts">
import {defineComponent} from 'vue';
import type {Statement} from "@/types/statements";
import {mapGetters} from "vuex";

export default defineComponent({
  name: "CompanyDetailStatement",
  data() {
    return {
      title: '',
      description: '',
    }
  },
  props: {
    name: {
      type: String,
      required: true,
    },
  },
  watch: {
    statements() {
      const statement: Statement = this.statements[this.name]
      this.title = statement.title
      this.description = statement.description
    },
  },
  computed: {
    ...mapGetters({
      statements: 'companyDetail/getStatements',
    }),
  },
})
</script>

<template>
<section class="detail-statement">

  <blockquote class="detail-statement-item">
    <p class="detail-statement-item__text">
      <span class="text--error">{{  title }}: </span>
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
  font-size: 1.6rem;
  line-height: 1.5;
}
</style>