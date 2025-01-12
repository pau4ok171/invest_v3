import type {ComputedGetter, PropType, ToRefs} from "vue";
import {computed, reactive, toRefs, watchEffect} from "vue";


export type EventProp<T extends any[] = any[], F = (...args: T) => void> = F
export const EventProp = <T extends any[] = any[]>() => [Function, Array] as PropType<EventProp<T>>

export function toKebabCase (str = '') {
  if (toKebabCase.cache.has(str)) return toKebabCase.cache.get(str)!
  const kebab = str
    .replace(/[^a-z]/gi, '-')
    .replace(/\B([A-Z])/g, '-$1')
    .toLowerCase()
  toKebabCase.cache.set(str, kebab)
  return kebab
  }
  toKebabCase.cache = new Map<string, string>()

export function focusableChildren(el: Element, filterByTabIndex = true) {
  const targets = ['button', '[href]', 'input:not([type="hidden"])', 'select', 'textarea', '[tabindex]']
    .map(s => `${s}${filterByTabIndex ? ':not([tabindex="-1"])' : ''}:not([disabled])`)
    .join(', ')
  return [...el.querySelectorAll(targets)] as HTMLElement[]
}
export function getNextElement(elements: HTMLElement[], location?: 'next' | 'prev', condition?: (el: HTMLElement) => boolean) {
  let _el
  let idx = elements.indexOf(document.activeElement as HTMLElement)
  const inc = location === 'next' ? 1 : -1
  do {
    idx += inc
    _el = elements[idx]
  } while ((!_el || _el.offsetParent == null || !(condition?.(_el) ?? true)) && idx < elements.length && idx >= 0)
  return _el
}

export function focusChild(el: Element, location?: 'next' | 'prev' | 'first' | 'last' | number) {
  const focusable = focusableChildren(el)

  if (!location) {
    if (el === document.activeElement || !el.contains(document.activeElement)) {
      focusable[0]?.focus()
    }
  } else if (location === 'first') {
    focusable[0]?.focus()
  } else if (location === 'last') {
    focusable.at(-1)?.focus()
  } else if (typeof location === 'number') {
    focusable[location]?.focus()
  } else {
    const _el = getNextElement(focusable, location)
    if (_el) _el.focus()
    else focusChild(el, location === 'next' ? 'first': 'last')
  }
}

// Only allow a single return type
type NotAUnion<T> = [T] extends [infer U] ? _NotAUnion<U, U> : never
type _NotAUnion<T, U> = U extends any ? [T] extends [U] ? unknown : never : never

/**
 * Convert a computed ref to a record of refs.
 * The getter function must always return an object with the same keys.
*/
export function destructComputed<T extends object> (getter: ComputedGetter<T & NotAUnion<T>>): ToRefs<T>
export function destructComputed<T extends object> (getter: ComputedGetter<T>) {
  const refs = reactive({}) as T
  const base = computed(getter)
  watchEffect(() => {
    for (const key in base.value) {
      refs[key] = base.value[key]
    }
  }, { flush: 'sync' })
  return toRefs(refs)
}

export function chunk (str: string, size = 1) {
  const chunked: string[] = []
  let index = 0
  while (index < str.length) {
    chunked.push(str.substring(index, index+size))
    index += size
  }
  return chunked
}

export function has<T extends string> (obj: object, key: T[]): obj is Record<T, unknown> {
  return key.every(k => obj.hasOwnProperty(k))
}

export function padEnd (str: string, length: number, char = '0') {
  return str + char.repeat(Math.max(0, length - str.length))
}

export function padStart (str: string, length: number, char = '0') {
  return char.repeat(Math.max(0, length - str.length)) + str
}

export function mergeDeep (
    source: Record<string, any> = {},
    target: Record<string, any> = {},
    arrayFn?: (a: unknown[], b: unknown[]) => unknown[],
) {
  const out: Record<string, any> = {}

  for (const key in source) {
    out[key] = source[key]
  }

  for (const key in target) {
    const sourceProperty = source[key]
    const targetProperty = target[key]

    // Only continue deep merging if
    // both properties are plain objects
    if (isPlainObject(sourceProperty) && isPlainObject(targetProperty)) {
      out[key] = mergeDeep(sourceProperty, targetProperty, arrayFn)

      continue
    }

    if (arrayFn && Array.isArray(sourceProperty) && Array.isArray(targetProperty)) {
      out[key] = arrayFn(sourceProperty, targetProperty)

      continue
    }

    out[key] = targetProperty
  }

  return out
}

export function isPlainObject (obj: any): obj is Record<string, any> {
  let proto
  return obj !== null && typeof obj === 'object' && (
      (proto = Object.getPrototypeOf(obj)) === Object.prototype || proto === null
  )
}

export function clamp (value: number, min = 0, max = 1) {
  return Math.max(min, Math.min(max, value))
}

export function createRange (length: number, start = 0): number[] {
  return Array.from({ length }, (v, k) => start + k)
}
