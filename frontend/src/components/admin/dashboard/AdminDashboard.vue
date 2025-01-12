<script lang="ts">
import {defineComponent} from 'vue'
import BaseOtpInput from "@/apps/visagiste/components/BaseOtpInput/BaseOtpInput.vue";

export default defineComponent({
  name: "AdminDashboard",
  data() {
    return {
      modelValue: '',
    }
  },
  components: {BaseOtpInput},
})
</script>

<template>
<div class="page-not-found">
  ADMIN DASHBOARD
</div>

<base-otp-input
  length="4"
  theme="dark"
  color="#000"
  variant="filled"
/>
</template>

<style scoped>
.page-not-found {
  display: flex;
  font-size: 5rem;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  margin: 100px 0;
}
</style>