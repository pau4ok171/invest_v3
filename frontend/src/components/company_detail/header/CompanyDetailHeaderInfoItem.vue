<script setup lang="ts">
const props = defineProps({
  nowrap: Boolean,
  onRow: Boolean,
  small: Boolean,
})
</script>

<template>
  <div
    :class="[
      'detail-header__info-item',
      {
        'detail-header__info-item--nowrap': props.nowrap,
      },
    ]"
  >
    <div v-if="$slots.title" class="detail-header__info-item-title">
      <slot name="title" />
    </div>
    <div
      v-if="$slots.value"
      :class="[
        'detail-header__info-item-value',
        {
          'detail-header__info-item-value--on-row': props.onRow,
          'detail-header__info-item-value--small': props.small,
        },
      ]"
    >
      <slot name="value" />
    </div>

    <slot />
  </div>
</template>

<style lang="scss" scoped>
.detail-header__info-item {
  display: flex;
  flex-flow: wrap;
  justify-content: center;
  margin-top: 0;
  width: auto;
  float: none;
  height: 40px;
}
.detail-header__info-item--nowrap {
  flex-flow: nowrap;
  align-items: center;
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
  font-size: 0.75rem;
  font-weight: normal;
  color: #fff;
  text-transform: uppercase;
  white-space: nowrap;
  line-height: 1.5;
  color: rgba(255, 255, 255, 0.7);
  padding-right: 8px;
}
.detail-header__info-item-value {
  position: relative;
  width: 100%;
  min-height: 0;
  max-width: 100%;
  font-size: 0.875rem;
  line-height: 1.5;
  font-weight: 500;
  white-space: nowrap;
}
.detail-header__info-item-value--small {
  font-size: 0.75rem;
}
</style>
