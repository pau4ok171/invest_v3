<script lang="ts">
import axios from "axios";
import DropDownMenu from "@/components/UI/DropDownMenu.vue";
import {mapMutations} from "vuex";
import {defineComponent} from "vue";

export default defineComponent({
  name: 'NavUserDropDown',
  components: {DropDownMenu},
  methods: {
    ...mapMutations({
      removeToken: 'authModule/removeToken',
    }),
    logout() {
      axios.defaults.headers.common['Authorization'] = ''

      localStorage.removeItem('token')
      localStorage.removeItem('username')
      localStorage.removeItem('userid')

      this.removeToken()
    },
  },
})
</script>

<template>
<DropDownMenu>
<div class="account-access__dropdown">
  <nav class="account-access__navigation">
    <div class="account-access-navigation__inner">
      <ul class="account-access__list">
        <li><a href="#">Profile</a></li>
        <li><a href="#">Plans & Pricing</a></li>
        <li><a href="#">Notifications</a></li>
        <li><a href="#">Help Center</a></li>
        <li><button @click="logout">Logout</button></li>
      </ul>
    </div>
  </nav>
</div>
</DropDownMenu>
</template>

<style scoped>
.account-access__dropdown {
  transition: visibility 0s .6s, opacity .6s ease;
}
.account-access__navigation {
  width: 200px;
  position: absolute;
  bottom: 0;
  right: 0;
}
.account-access-navigation__inner {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  background-color: #262e3a;
  border-radius: 4px;
}
.account-access__list {
  list-style: none;
}
.account-access__list li {
  font-size: 1.4rem;
  line-height: 1.5;
}
.account-access__list li:last-child {
  border-top: 1px solid #3c434e;
}
.account-access__list li > * {
  display: block;
  text-align: left;
  color: #fff;
  width: 100%;
  padding: 12px 16px;
  transition: all .3s ease 0s;
}
.account-access__list li:first-child > * {
  border-top-right-radius: 4px;
  border-top-left-radius: 4px;
}
.account-access__list li:last-child > * {
  border-bottom-right-radius: 4px;
  border-bottom-left-radius: 4px;
}
.account-access__list li > *:hover {
  background-color: rgb(35, 148, 223);
}
</style>