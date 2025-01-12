<script setup lang="ts">

import type {ComponentPublicInstance, FunctionalComponent, PropType} from "vue";

export type ComposableComponent<Props = any> =
    | { new (): ComponentPublicInstance<Props> }
    | FunctionalComponent<Props>

export type IconValue =
  | string
  | (string | [path: string, opacity: number])[]
  | ComposableComponent
export const IconValue = [String, Function, Object, Array] as PropType<IconValue>

export interface IconProps {
  tag: string,
  icon?: IconValue,
  disabled?: Boolean,
}

export interface IconAliases {
  [name: string]: IconValue
}

type IconComponent = ComposableComponent<IconProps>

export interface IconSet {
  component: IconComponent
}
</script>

<template>

</template>

<style scoped>

</style>