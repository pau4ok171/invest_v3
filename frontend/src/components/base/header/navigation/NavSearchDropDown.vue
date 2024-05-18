<script lang="ts">
import type {PropType} from "vue";
import type {SearchCompanyItems} from "@/types/invest";
import {defineComponent} from "vue";

export default defineComponent({
  name: 'NavSearchDropDown',
  props: {
    companies: {
      type: Object as PropType<SearchCompanyItems>,
      required: true,
    }
  },
  mounted() {
    document.addEventListener('click', this.clickHandler)
  },
  methods: {
    clickHandler() {
      this.$emit('closeDropDownMenu')
      document.removeEventListener('click', this.clickHandler)
    }
  },
})
</script>

<template>
<div class="nav_search__dropdown">
<div class="dropdown-menu nav-search__dropdown-inner">
<ul class="nav-search__dropdown-list">

  <li
      class="nav-search__dropdown-item"
      v-for="company in companies"
      :key="company.uid"
  >
    <RouterLink
        :to="company.absolute_url"
        class="nav-search__dropdown-link"
    >
      <img :src="company.logo_url" alt="company_icon" class="nav-search__dropdown-link-icon">
      <div class="nav-search__dropdown-info">
        <div class="nav-search__dropdown-desc">
          <div class="nav-search__dropdown-title">{{ company.title }}</div>
          <div class="nav-search__dropdown-market">
            <img class="nav-search__dropdown-market-img" src="../../../../assets/img/flags/ru.svg" alt="RU">
            <p class="nav-search__dropdown-market-title">{{ company.market.title }}</p>
          </div>
        </div>
        <div class="nav-search__dropdown-sector">Bank</div>
      </div>
    </RouterLink>
  </li>

</ul>
</div>
</div>
</template>

<style scoped>
.dropdown-menu::-webkit-scrollbar {
  width: 10px;
}
.dropdown-menu::-webkit-scrollbar-track {
  -webkit-box-shadow: 5px 5px 5px -5px rgba(34, 60, 80, .2);
  background-color: #f9f9fd;
  border-radius: 10px;
}
.dropdown-menu::-webkit-scrollbar-thumb {
  border-radius: 10px;
  background: linear-gradient(180deg, #00c6fb, #005bea);
}
.nav_search__dropdown {
  position: fixed;
  left: 0;
  top: 0;
  margin: 0;
  transform: translate(1020px, 55px);
  transition: opacity .3s linear 0s, transform .3s ease-out 0s;
  opacity: 1;
}
.nav-search__dropdown-inner {
  width: 400px;
  top: 4px;
  left: 0;
  position: absolute;
  background-color: rgb(27, 34, 45);
  border-radius: 4px;
  border: 1px solid rgba(255, 255, 255, .1);
  max-height: 325px;
  overflow: hidden auto;
}
.nav-search__dropdown-list {
  list-style: none;
  font-size: 1.6rem;
}
.nav-search__dropdown-link {
  transition: all .3s ease 0s;
  color: rgb(35, 148, 223);
  text-decoration: none;

  position: relative;
  display: flex;
  height: 64px;
  border-bottom: 1px solid rgba(255, 255, 255, .1);
  padding-bottom: 8px;
  background-color: transparent;
}
.nav-search__dropdown-link:hover {
  background-color: rgba(95, 104, 117, .1);
}
.nav-search__dropdown-link-icon {
  margin-left: 16px;
  background-color: #fff;
  border-radius: 100%;
  width: 48px;
  height: 48px;
  align-self: center;
}
.nav-search__dropdown-info {
  display: flex;
  -webkit-box-pack: justify;
  justify-content: space-between;
  flex-wrap: nowrap;
  width: 100%;
}
.nav-search__dropdown-desc {
  padding-left: 12px;
  padding-top: 8px;
  width: 205px;
}
.nav-search__dropdown-title {
  display: flex;
  flex-flow: wrap;
  justify-content: left;

  width: 100%;
  padding-right: 10px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  color: rgb(255, 255, 255);

  line-height: 1.5;
  font-weight: 500;
}
.nav-search__dropdown-market {
  display: grid;
  grid-template-columns: 24px auto;
  -webkit-box-align: center;
  align-items: center;
}
.nav-search__dropdown-market-img {
  width: 16px;
  height: 11px;
}
.nav-search__dropdown-market-title {
  text-transform: uppercase;
  font-size: 1.2rem;
  line-height: 1.5;
  color: rgba(255, 255, 255, .5);
}
.nav-search__dropdown-sector {
  align-self: center;
  width: 80px;
  max-width: 51px;
  font-size: 1.2rem;
  line-height: 1.5;
  margin-right: 16px;
  border-radius: 12px;
  padding: 3px 12px;
  background-color: rgb(38, 46, 58);
  color: rgba(242, 242, 243, .5);
  height: 26px;
}
</style>