<template>
  <button
      @click="$emit('buttonClick')"
      class="company-list__button"
  >
    <slot/>
  </button>
</template>

<script>
export default {
  name: 'CompanyListButton',
}
</script>

<style>
  .company-list__button {
    display: flex;
    align-items: center;
    height: 40px;
    padding: 0 12px;
    border-radius: 8px;
    font-size: 1.4rem;
    color: rgba(255, 255, 255, .7);
    background-color: transparent;
    transition: background-color .2s ease 0s;
    user-select: none;
  }
  .company-list__button--rounded {
    height: 32px;
    font-size: 1.2rem;
  }
  .company-list__button--circled {
    border-radius: 100%;
  }
  .company-list__button:not([disabled]):hover {
    background-color: rgba(255, 255, 255, .05);
  }
  .company-list__button[disabled] {
    opacity: .5;
    cursor: auto;
  }
  .company-list__button span {
    color: #fff;
    pointer-events: none;
    margin: 0 4px;
  }
  .company-list__button svg {
    width: 24px;
    height: 24px;
    fill: rgba(255, 255, 255, .5);
    pointer-events: none;
    margin: 0 -4px;
  }
</style>