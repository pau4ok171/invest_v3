<script setup lang="ts">
import TheHeader from '@/components/base/header/TheHeader.vue'
import TheMain from "@/components/base/main/TheMain.vue";
</script>

<template>
<TheHeader/>

<TheMain><slot/></TheMain>
</template>
