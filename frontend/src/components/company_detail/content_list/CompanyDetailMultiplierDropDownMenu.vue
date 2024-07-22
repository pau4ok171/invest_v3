<script lang="ts">
import {defineComponent} from 'vue'
import type {PropType} from 'vue'
import CheckedIcon from "@/components/icons/CheckedIcon.vue";
import type {Tab} from "@/components/company_detail/content_list/valuation/MultiplierVsPeers.vue";

export default defineComponent({
  name: "CompanyDetailMultiplierDropDownMenu",
  components: {CheckedIcon},
  props: {
    tabs: {
      type: Object as PropType<{[p: string]: Tab}>,
      required: true,
    },
  },
})
</script>

<template>
<div class="detail-multiplier-dropdown-menu">
<ul>
  <li v-for="tab in tabs" :key="tab.id">
    <button @click="$emit('changeMode', tab)" class="detail-multiplier-dropdown-menu__button" :disabled="tab.active">
      <CheckedIcon class="detail-multiplier-dropdown-menu__icon" v-if="tab.active"/>
      {{ tab.name }}
    </button>
  </li>
</ul>
</div>
</template>

<style>
.detail-multiplier-dropdown-menu {
  display: block;
  position: absolute;
  width: 100%;
  z-index: 9999;
  left: 0;
  bottom: 0;
}
.detail-multiplier-dropdown-menu ul {
  font-size: 1.6rem;
  position: absolute;
  top: 8px;
  right: 0;
  border-radius: 4px;
  background: white;
  overflow: hidden auto;
  box-shadow: rgba(0, 0, 0, .25) 0 2px 8px;
}
.detail-multiplier-dropdown-menu__button {
  width: 100%;
  display: flex;
  transition: all 0.3s ease 0s;
  position: relative;
  white-space: nowrap;
  line-height: 1.5;
  cursor: pointer;
  padding: 8px 12px 8px 36px;
  text-decoration: none;
  user-select: none;
  border-top: none;
  font-size: 1.4rem;
  background: #fff;
  color: #262e3a;
}
.detail-multiplier-dropdown-menu__button:disabled {
  font-weight: 500;
}
.detail-multiplier-dropdown-menu__button:hover {
  background: rgb(35, 148, 223);
  color: #fff;
}
.detail-multiplier-dropdown-menu__button:hover svg {
  fill: #fff;
}
.detail-multiplier-dropdown-menu__icon {
  cursor: pointer;
  user-select: none;
  pointer-events: none;
  fill: var(--blue);
  box-sizing: border-box;
  position: absolute;
  left: 8px;
  top: 6px;
}
</style>