<script lang="ts">
import {defineComponent} from 'vue'
import type {PropType} from 'vue'
import CheckedIcon from "@/components/icons/CheckedIcon.vue";
import type {IFormattedSelector} from "@/types/admin.types";


export default defineComponent({
  name: "AdminSelectorDropDownMenu",
  components: {
    CheckedIcon
  },
  data() {
    return {
      searchQuery: '',
    }
  },
  props: {
    hasSearch: {
      type: Boolean,
      default: false,
    },
    modelValue: {
      type: Object as PropType<IFormattedSelector>,
      required: true,
    },
    options: {
      type: Array<IFormattedSelector>,
      required: true,
    },
  },
  computed: {
    filteredOptions() {
      return [...this.options].filter(s => s.name.toLowerCase().includes(this.searchQuery.toLowerCase()))
    }
  },
})
</script>

<template>
<div class="dropdown-menu">
  <div class="dropdown-menu__inner">

    <template v-if="hasSearch">
      <div @click.stop class="dropdown-menu__search">
        <input
          type="search"
          class="dropdown-menu__input"
          autocomplete="false"
          placeholder="Type to filter..."
          v-model="searchQuery"
        />
      </div>
    </template>

    <ul class="dropdown-menu__list">
      <li
        class="dropdown-menu__item"
        v-for="option in filteredOptions"
        :key="option.slug"
      >
        <button
          class="dropdown-menu__button"
          @click="$emit('update:modelValue', option)"
          :disabled="option.slug === modelValue.slug"
          :value="option.slug"
        >
          <CheckedIcon :disabled="option.slug !== modelValue.slug"/>
          <span>{{ option.name }}</span>
        </button>
      </li>
    </ul>

  </div>
</div>
</template>

<style lang="scss" scoped>
.dropdown-menu {
  position: absolute;
  top: 40px;
  width: 280px;
  z-index: 5;
  max-height: 300px;
  overflow-y: auto;
  border-radius: 8px;
  box-shadow: 0 10px 15px 10px rgba(26, 97, 212, .2);
}
.dropdown-menu__inner {
  background-color: #212529;
  width: 100%;
  height: 100%;
}
.dropdown-menu__search {
  padding: .8rem;
  width: 100%;
  position: sticky;
  background-color: inherit;
  z-index: 10;
  top: 0;
}
.dropdown-menu__input {
  width: 100%;
  height: 40px;
  font-size: 1.6rem;
  padding: .6rem 1.2rem;
  background-color: #212529;
  border: 1px solid #495057;
  border-radius: 8px;
  outline: none;
  font-weight: 400;
  line-height: 1.5;
  appearance: none;
  color: #fff;
  transition: border-color .15s ease-in-out, box-shadow .15s ease-in-out;
}
.dropdown-menu__input:focus {
  color: #fff;
  border-color: #86b7fe;
  box-shadow: 0 0 0  .4rem rgba(13, 110, 253, .25);
}
.dropdown-menu__list {
  font-size: 1.4rem;
  font-weight: 400;
  border-radius: 8px;
  overflow: hidden;
}
.dropdown-menu__item {
  list-style: none;
}
.dropdown-menu__button {
  display: flex;
  align-items: center;
  outline: none;
  gap: 8px;
  width: 100%;
  text-align: left;
  padding: .8rem 1.6rem;
  color: inherit;
}
.dropdown-menu__button:not([disabled]):hover {
  background-color: var(--blue);
}
.dropdown-menu__button:not([disabled]):focus {
  background-color: var(--blue);
}
.dropdown-menu__button:is([disabled]) {
  opacity: .2;
}
.dropdown-menu__button svg {
  fill: var(--color-success);
  width: 24px;
  height: 24px;
}
.dropdown-menu__button svg[disabled=true] {
  opacity: 0;
  }
</style>