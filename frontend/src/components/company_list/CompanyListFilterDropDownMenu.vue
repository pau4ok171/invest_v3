<template>
  <div class="dropdown-menu">
    <div class="dropdown-menu__inner">

      <template v-if="has_search">
        <div @click.stop class="dropdown-menu__search">
          <BaseInput
            type="search"
            class="dropdown-menu__input"
            autocomplete="false"
            placeholder="Type to filter..."
            :value="searchQuery"
            @input="searchQuery=$event.target.value"
          />
        </div>
      </template>

      <ul class="dropdown-menu__list">
          <li
            class="dropdown-menu__item"
            v-for="f in filteredFilter"
            :key="f.slug"
          >
            <button
              class="dropdown-menu__button"
              @click="changeFilter({filter_name: filter_name, object: f})"
              :disabled="f.slug === this.active_filter.slug"
              :value="f.slug"
            >
              <CheckedIcon :disabled="f.slug !== this.active_filter.slug"/>
              <span>{{ f.title }}</span>
            </button>
          </li>
      </ul>

    </div>
  </div>
</template>

<script lang="ts">
import CheckedIcon from "@/components/icons/CheckedIcon.vue";
import BaseInput from "@/components/UI/base/BaseInput.vue";
import {mapActions} from "vuex";

export default {
  name: 'CompanyListFilterDropDownMenu',
  components: {BaseInput, CheckedIcon},
  data() {return {
      searchQuery: '',
    }},
  props: {
    has_search: Boolean,
    filter_name: String,
    filter: {
      type: Array,
      required: true,
    },
    active_filter: {
      type: Object,
      required: true,
    }
  },
  computed: {
    filteredFilter() {
      return [...this.filter].filter(s => s.title.toLowerCase().includes(this.searchQuery.toLowerCase()) || s.required)
    }
  },
  methods: {
    ...mapActions({
      changeFilter: "companyList/changeFilter"
    }),
  },
}
</script>

<style scoped>
.dropdown-menu {
  position: absolute;
  top: 40px;
  width: 280px;
  z-index: 5;
  max-height: 300px;
  overflow-y: auto;
  border-radius: 8px;
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
  gap: 8px;
  width: 100%;
  text-align: left;
  padding: .8rem 1.6rem;
  color: inherit;
}
.dropdown-menu__button:not([disabled]):hover {
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