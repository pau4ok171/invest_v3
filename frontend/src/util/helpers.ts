import { unref } from "vue";
import type { Ref } from "vue";

export type MaybeRef<T> = T | Ref<T>

export function debounce(fn: Function, delay: MaybeRef<number>) {
  let timeoutId = 0 as any
  const wrap = (...args: any[]) => {
    clearTimeout(timeoutId)
    timeoutId = setTimeout(() => fn(...args), unref(delay))
  }
  wrap.clear = () => {
    clearTimeout(timeoutId)
  }
  wrap.immediate = fn
  return wrap
}