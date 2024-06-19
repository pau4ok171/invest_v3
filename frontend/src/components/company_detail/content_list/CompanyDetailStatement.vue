<script lang="ts">
import {defineComponent} from 'vue';
import type {Statement} from "@/types/statements";
import {mapGetters} from "vuex";

export default defineComponent({
  name: "CompanyDetailStatement",
  props: {
    name: {
      type: String,
      required: true,
    },
  },
  computed: {
    ...mapGetters({
      statements: 'companyDetail/getStatements',
    }),
    get_title() {
      const statement: Statement = this.statements[this.name]
      if (statement) return statement.title
      return ''
    },
    get_description() {
      const statement: Statement = this.statements[this.name]
      if (statement) return statement.description
      return ''
    },
  },
})
</script>

<template>
<section class="detail-statement">

  <blockquote class="detail-statement-item">
    <p class="detail-statement-item__text">
      <span class="text--error">{{  get_title }}: </span>
      <span>{{ get_description }}</span>
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