<script lang="ts">
import {defineComponent} from 'vue';
import type {PropType} from 'vue';
import BaseInput from "@/components/UI/base/BaseInput.vue";
import BaseIcon from "@/components/UI/base/BaseIcon/BaseIcon.vue";

interface ListItem {
  id: number | string,
  title: string,
  highlightedTitle?: string,
}

export default defineComponent({
  name: "BaseList",
  components: {
    BaseIcon,
    BaseInput
  },
  data() {
    return {
      searchQuery: '',
    }
  },
  props: {
    activeItem: {
      type: Object as PropType<ListItem>,
      required: true,
    },
    items: {
      type: Object as PropType<ListItem[]>,
      required: true
    },
    hasSearch: {
      type: Boolean,
      default: false
    },
  },
  computed: {
    filteredItems() {
      const filtered = this.items.filter(i => i.title.toLowerCase().includes(this.searchQuery.toLowerCase().trim()))

      if (this.searchQuery) {
        const regex = new RegExp(this.searchQuery.trim(), 'gi')
        return filtered.map(f => {
          const highlightedTitle = f.title.replace(regex, match => `<span class="base-list__highlight">${match}</span>`)
          return {...f, highlightedTitle}
        })
      }
      return filtered
    },
  },
})
</script>

<template>
<div class="base-list">
  <div class="base-list__inner">

    <template v-if="hasSearch">
      <div @click.stop class="base-list__search">
        <BaseInput
          type="search"
          class="base-list__input"
          autocomplite="false"
          placeholder="Type to Filter..."
          :value="searchQuery"
          @input="searchQuery=$event.target.value"
        />
      </div>
    </template>

    <ul v-if="filteredItems.length" class="base-list__items">
      <li
        class="base-list__item"
        :key=item.id
        v-for="item in filteredItems"
      >
        <button
          class="base-list__button"
          @click="$emit('setActiveItem', item)"
          :disabled="item.id === activeItem.id"
          :value="item.id"
        >
          <base-icon
            icon="CheckedIcon"
            :disabled="item.id !== activeItem.id"
          />

          <span v-html="item.highlightedTitle || item.title"></span>

        </button>
      </li>
    </ul>
    <div v-else class="base-list__no-items">NOTHING HERE...</div>
  </div>
</div>
</template>

<style scoped>
.base-list {
  position: absolute;
  top: 40px;
  width: 280px;
  z-index: 5;
  border-radius: 8px;
}
.base-list__inner {
  background-color: #212529;
  width: 100%;
  height: 100%;
  border-radius: inherit;
}
.base-list__search {
  padding: .8rem;
  width: 100%;
  position: relative;
  background-color: inherit;
  border-radius: inherit;
}
.base-list__input {
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
.base-list__input:focus {
  color: #fff;
  border-color: #86b7fe;
  box-shadow: 0 0 0  .4rem rgba(13, 110, 253, .25);
}
.base-list__items {
  font-size: 1.4rem;
  font-weight: 400;
  border-radius: 8px;
  overflow-y: auto;
  max-height: 250px;
  margin-right: 8px;
}
.base-list__no-items {
  font-size: 1.2rem;
  font-weight: 400;
  text-align: center;
  padding: 8px 0 8px 0;
}
.base-list__item {
  list-style: none;
}
.base-list__button {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
  text-align: left;
  padding: .8rem 1.6rem;
  color: inherit;
}
.base-list__button:not([disabled]):hover {
  background-color: var(--blue);
}
.base-list__button:is([disabled]) {
  opacity: .2;
}
.base-list__button > i[disabled=true] {
  opacity: 0;
}
.base-list__items::-webkit-scrollbar {
  width: 10px;
}
.base-list__items::-webkit-scrollbar-track {
  -webkit-box-shadow: 5px 5px 5px -5px rgba(34, 60, 80, .2);
  background-color: #f9f9fd;
  border-radius: 10px;
}
.base-list__items::-webkit-scrollbar-thumb {
  border-radius: 10px;
  background: linear-gradient(180deg, #00c6fb, #005bea);
}
:global(.base-list__highlight) {
  background-color: yellow;
  color: black;
}
</style>