<script lang="ts">
import axios from "axios";
import NavSearchDropDown from "@/components/base/header/navigation/NavSearchDropDown.vue";
import SearchIcon from "@/components/icons/SearchIcon.vue";
import InputCrossIcon from "@/components/icons/InputCrossIcon.vue";
import BaseInput from "@/components/UI/base/BaseInput.vue";
import {defineComponent} from "vue";

export default defineComponent({
  name: "NavSearch",
  components: {
    BaseInput,
    InputCrossIcon,
    SearchIcon,
    NavSearchDropDown
  },
  data() {
    return {
      inputValue: '',
      searchResponse: []
    }
  },
  methods: {
    async updateInput(value: string) {
      this.inputValue = value

      if (this.inputValue.length) {
        await axios
          .get('/api/v1/invest/search_query/', {params: {query: this.inputValue}})
          .then(response => this.searchResponse = response.data)
          .catch(err => {console.log(err)})
        } else this.closeDropDown()
    },
    closeDropDown() {
      this.searchResponse = []
    },
    clearInput() {
      this.inputValue = ''
    }
  },
})
</script>

<template>
<div class="navigation__nav-search">

  <div class="nav-search__inner">
    <BaseInput
      type="search"
      name="search-field"
      ref="searchField"
      class="nav-search__input"
      placeholder="Поиск по компаниям"
      autocomplete="off"
      :inputValue
      @updateInput="updateInput"
    />
    <span class="nav-search__prefix">
      <SearchIcon width="24" height="24" class="nav-search__prefix-icon"/>
    </span>
    <span class="nav-search__postfix">
      <InputCrossIcon v-if="inputValue.length" @click="clearInput" width="24" height="24" class="nav-search__postfix-icon"/>
    </span>
  </div>

  <NavSearchDropDown
    v-if="searchResponse.length"
    :companies="searchResponse"
    @closeDropDownMenu="closeDropDown"
  />

</div>
</template>

<style scoped>
.navigation__nav-search {
  display: flex;
  justify-content: center;
  align-items: center;
  margin:0 24px;
  width: 271px;
}
.nav-search__inner {
  width: 100%;
  z-index: 1;
  background: transparent;
  position: relative;
}
.nav-search__input {
  padding: 14px 48px;
  appearance: none;
  border: 1px solid rgba(255, 255, 255, .2);
  font-size: 1.4rem;
  width: 100%;
  border-radius: 4px;
  background-color: rgba(255, 255, 255, .05);
  font-weight: normal;
  height: 40px;
  line-height: normal;
  caret-color: var(--blue);
  color: #fff;
  transition: border .2s ease 0s, background-color .2s ease 0s;
}
.nav-search__input:focus {
  outline: none;
  background: rgba(35, 148, 223, .05)
}
.nav-search__prefix {
    position: absolute;
  left: 12px;
  font-size: 20px;
  color: var(--blue);
  height: 40px;
  line-height: 41px;
}
.nav-search__prefix-icon {
    height: 100%;
    fill: #2394df;
}
.nav-search__postfix {
    position: absolute;
  right: 12px;
  font-size: 20px;
  color: var(--blue);
  height: 40px;
  line-height: 41px;
}
.nav-search__postfix-icon {
    fill: #fff;
    height: 100%;
    opacity: .5;
    cursor: pointer;
}
.nav-search__postfix-icon use {
  pointer-events: none;
}
</style>