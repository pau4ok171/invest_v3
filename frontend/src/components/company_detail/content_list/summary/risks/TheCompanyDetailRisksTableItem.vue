<script lang="ts">
import {defineComponent} from 'vue';
import type {PropType} from "vue";
import type {Statement} from "@/types/statements";
import BaseButton from "@/apps/visagiste/components/BaseButton/BaseButton.vue";

export default defineComponent({
  name: "TheCompanyDetailRisksTableItem",
  components: {
    BaseButton,
  },
  props: {
    statement: {
      type: Object as PropType<Statement>,
      required: true,
    },
  },
  methods: {
    get_mark_class() {
      if (this.statement.status === 'PASS') {
        return 'detail-risks-table__status--success'
      } else if (this.statement.status === 'FAIL') {
          if (this.statement.severity === 'MAJOR') {
            return 'detail-risks-table__status--high-error'
          } else {
            return 'detail-risks-table__status--error'
          }
      } else {
        return 'detail-risks-table__status--no-data'
      }
    }
  },
})
</script>

<template>
<tr>
  <td>
    <div class="detail-risks-table__status">
    <mark :class="get_mark_class()">{{ statement.status }}</mark>
    </div>
  </td>
  <td>
    <div class="detail-risks-table__content">
      <div class="detail-risks-table__description">
        <p class="detail-risks-table__question">{{ statement.question }}</p>
        <span>{{ statement.description }}</span>
      </div>

      <base-button
        :text="statement.area"
        append-icon="ArrowDownIcon"
        variant="text"
        rounded="large"
        size="small"
        theme="dark"
      />
    </div>
  </td>
</tr>
</template>

<style scoped>
.detail-risks-table__content {
  display: flex;
  flex-flow: wrap;
  -webkit-box-pack: end;
  justify-content: flex-end;
  gap: 8px;
}
.detail-risks-table__description {
  width: 75%;
}
.detail-risks-table__question {
  font-size: 1.4rem;
  line-height: 1.5;
  font-weight: 500;
  margin-bottom: 3px;
}
.detail-risks-table__status mark {
  border-radius: 4px;
  padding: 3px 7px;
  color: #fff;
  line-height: 1.5;
  text-align: right;
  white-space: nowrap;
  font-size: 1.4rem;
}
.detail-risks-table__status--success {
  background-color: rgb(45, 201, 126);
}
.detail-risks-table__status--high-error {
  background-color: rgb(230, 65, 65);
}
.detail-risks-table__status--error {
  background-color: rgb(255, 146, 18);
}
.detail-risks-table__status--no-data {
  background-color: rgb(201, 203, 207);
}
</style>