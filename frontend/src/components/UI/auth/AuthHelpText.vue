<script lang="ts">
import type {PropType} from "vue";
import {defineComponent} from "vue";

interface FieldCheck {
  isInit: boolean,
  isError: boolean,
  message: string,
}

export default defineComponent({
  name: 'AuthHelpText',
  props: {
    check: {
      type: Object as PropType<FieldCheck>,
      required: true,
    },
  }
})
</script>

<template>
<p
  class="form__help-text"
  :class="{'form__help-text--success': !check.isError && check.isInit, 'form__help-text--error': check.isError && check.isInit}"
>
  {{ check.message }}
</p>
</template>

<style scoped>
.form__help-text {
  font-size: 1.2rem;
  padding-top: 1.6rem;
  color: rgb(140, 146, 155);
  font-weight: normal;
  line-height: 1.5;
  text-align: left;
}
.form__help-text--error {
  font-size: 1.2rem;
  color: var(--color-error);
}
.form__help-text--success {
  font-size: 1.2rem;
  color: var(--color-success);
}
</style>