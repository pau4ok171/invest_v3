<script lang="ts">
import {defineComponent} from 'vue'
import CheckedIcon from "@/components/icons/CheckedIcon.vue";

export default defineComponent({
  name: "CompanyDetailDropDownMenu",
  components: {CheckedIcon},
  props: {
    objects: {
      type: Array,
      required: true,
    },
  },
})
</script>

<template>
  <div class="detail-dropdown-menu">
    <ul>
      <li
        v-for="object in objects"
        :key="object.slug"
      >
        <a :class="['detail-dropdown-menu__link', {'detail-dropdown-menu__link--selected': object.isChosen}]">
          <CheckedIcon class="detail-dropdown-menu__icon" v-if="object.isChosen"/>
          {{ object.title }}
        </a>
      </li>
    </ul>
  </div>
</template>

<style>
   .detail-dropdown-menu {
      display: block;
      position: absolute;
      width: 100%;
      z-index: 9999;
      left: 0;
      bottom: 0;
  }
  .detail-dropdown-menu ul {
    font-size: 1.6rem;
    position: absolute;
    top: 8px;
    right: 8px;
    width: 100%;
    min-width: 200px;
    padding: 4px 0;
    border-radius: 4px;
    background: white;
    max-height: 200px;
    overflow: hidden auto;
    box-shadow: rgba(0, 0, 0, .25) 0 2px 8px;
  }
  .detail-dropdown-menu__link {
    transition: all 0.3s ease 0s;
    position: relative;
    white-space: nowrap;
    line-height: 1.5;
    cursor: pointer;
    padding: 8px 12px 8px 36px;
    display: block;
    text-decoration: none;
    user-select: none;
    border-top: none;
    font-size: 1.4rem;
    background: #fff;
    color: #262e3a;
  }
  .detail-dropdown-menu__link--selected {
    font-weight: 500;
  }
  .detail-dropdown-menu__link:hover {
    background: rgb(35, 148, 223);
    color: #fff;
  }
  .detail-dropdown-menu__link:hover svg {
    fill: #fff;
  }
  .detail-dropdown-menu__icon {
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