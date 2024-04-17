<template>
  <div class="detail-header__info-item">
    <div class="detail-header__info-item-title">
      <slot name="title"/>
    </div>
    <div class="detail-header__info-item-value">
      <slot name="value"/>
    </div>
  </div>
</template>

<script lang="ts">
 export default {
   name: 'CompanyDetailHeaderInfoItem',
 }
</script>

<style>
  .detail-header__info-item {
    display: flex;
    flex-flow: wrap;
    justify-content: flex-start;
    margin-top: 0;
    width: auto;
    float: none;
    margin-right: 24px;
    height: 40px;
  }
  .detail-header__info-item--nowrap {
    flex-flow: nowrap;
    align-items: flex-end;
    justify-content: flex-end;
  }
  .detail-header__info-item-value--on-row {
    display: flex;
    gap: 2px;
  }
  .detail-header__info-item-title {
    position: relative;
    width: 100%;
    min-height: 0;
    max-width: fit-content;
    flex: 0 0 100%;
    font-size: 1.2rem;
    font-weight: normal;
    color: #fff;
    text-transform: uppercase;
    white-space: nowrap;
    line-height: 1.5;
    color: rgba(255, 255, 255, .7);
    padding-right: 8px;
  }
  .detail-header__info-item-value {
    position: relative;
    width: 100%;
    min-height: 0;
    max-width: 100%;
    font-size: 1.4rem;
    line-height: 1.5;
    font-weight: 500;
    white-space: nowrap;
  }

  .detail-header__info-item-value--small {
    font-size: 1.2rem;
  }

  .detail-header__error-color {
    color: var(--color-error);
  }
  .detail-header__success-color {
    color: var(--color-success);
  }
</style>