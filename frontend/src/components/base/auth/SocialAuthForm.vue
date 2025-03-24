<script lang="ts">
  import GoogleIcon from "@/components/icons/GoogleIcon.vue";
  import {defineComponent} from "vue";

  export default defineComponent({
    name: 'SocialAuthForm',
    components: {
      GoogleIcon,
    }
  })
</script>

<template>
<div class="auth-form__socials">

  <div class="auth-form__socials-desc">Или с помощью:</div>

  <div class="auth-form__socials-items">
    <div class="auth-form__socials-item">
      <button class="auth-form__socials-button">
        <GoogleIcon/>
      </button>
    </div>

    <div class="auth-form__socials-item">
      <button class="auth-form__socials-button">
        <GoogleIcon/>
      </button>
    </div>

    <div class="auth-form__socials-item">
      <button class="auth-form__socials-button">
        <GoogleIcon/>
      </button>
    </div>
  </div>

</div>
</template>

<style scoped>
.auth-form__socials {
  padding-top: 24px;
}
.auth-form__socials-desc {
  margin-bottom: 16px;
  line-height: 1.5;
  text-align: center;
  font-weight: normal;
  color: #000;
}
.auth-form__socials-items {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 24px;
}
.auth-form__socials-item {
  position: relative;
}
.auth-form__socials-button {
  position: relative;
  border: 0;
  border-radius: 6px;
  vertical-align: top;
  padding: 0 12px;
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0 8px;
  width: 42px;
  height: 42px;
  background-color: #fff;
  box-shadow: rgba(0, 0, 0, .1) 0 2px 3px;
  transition: background-color .2s ease 0s, box-shadow .2s ease 0s, color .4s ease 0s, padding .4s ease 0s;
}
.auth-form__socials-button:hover {
  box-shadow: rgba(0, 0, 0, .2) 0 2px 3px;
}
.auth-form__socials-button img {
  left: 10px;
  top: 10px;
  width: 22px;
  height: 22px;
  display: inline;
  vertical-align: middle;
  margin: 0 -4px;
}
</style>
