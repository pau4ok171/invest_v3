import type {ComponentInternalInstance, ComputedGetter, InjectionKey, PropType, ToRefs, VNode, VNodeChild} from "vue";
import {capitalize, computed, Fragment, reactive, toRefs, watchEffect} from "vue";
import {IN_BROWSER} from "@/apps/visagiste/utils/globals";

export function getNestedValue (obj: any, path: (string | number)[], fallback?: any): any {
  const last = path.length - 1
  if (last < 0) return obj === undefined ? fallback : obj

  for (let i = 0; i < last; i++) {
    if (obj == null) {
      return fallback
    }
    obj = obj[path[i]]
  }

  if (obj == null) return fallback

  return obj[path[last]] === undefined ? fallback : obj[path[last]]
}

export function deepEqual (a: any, b: any): boolean {
  if (a === b) return true

  if (
    a instanceof Date &&
    b instanceof Date &&
    a.getTime() !== b.getTime()
  ) {
    // If the values are Date, compare them as timestamps
    return false
  }

  if (a !== Object(a) || b!== Object(b)) {
    // If the values aren't objects, they were already checked for equality
    return false
  }

  const props = Object.keys(a)

  if (props.length !== Object.keys(b).length) {
    // Different number of props, don't bother to check
    return false
  }

  return props.every(p => deepEqual(a[p], b[p]))
}

export function getObjectValueByPath (obj: any, path?: string | null, fallback?: any): any {
  // credit: http://stackoverflow.com/questions/6491463/accessing-nested-javascript-objects-with-string-key#comment55278413_6491621
  if (obj == null || !path || typeof path !== 'string') return fallback
  if (obj[path] !== undefined) return obj[path]
  path = path.replace(/\[(\w+)\]/g, '.$1') // convert indexes to properties
  path = path.replace(/^\./, '') // strip a leading dot
  return getNestedValue(obj, path.split('.'), fallback)
}

export type SelectItemKey<T = Record<string, any>> =
  | boolean | null | undefined // Ignored
  | string // Lookup by key, can use dot notation for nested objects
  | readonly (string | number)[] // Nested lookup by key, each array item is a key in the next level
  | ((item: T, fallback?: any) => any)

export function pick<
  T extends object,
  U extends Extract<keyof T, string>
> (obj: T, paths: U[]): MaybePick<T, U> {
  const found: any = {}

  const keys = new Set(Object.keys(obj))
  for (const path of paths) {
    if (keys.has(path)) {
      found[path] = obj[path]
    }
  }

  return found
}

export function getPropertyFromItem (
  item: any,
  property: SelectItemKey,
  fallback?: any
): any {
  if (property === true) return item === undefined ? fallback : item

  if (property == null || typeof property === 'boolean') return fallback

  if (item !== Object(item)) {
    if (typeof property !== 'function') return fallback

    const value = property(item, fallback)

    return typeof value === 'undefined' ? fallback : value
  }

  if (typeof property === 'string') return getObjectValueByPath(item, property, fallback)

  if (Array.isArray(property)) return getNestedValue(item, property, fallback)

  if (typeof property !== 'function') return fallback

  const value = property(item, fallback)

  return typeof value === 'undefined' ? fallback : value
}

export type EventProp<T extends any[] = any[], F = (...args: T) => void> = F
export const EventProp = <T extends any[] = any[]>() => [Function, Array] as PropType<EventProp<T>>

export function callEvent<T extends any[]> (handler: EventProp<T> | EventProp<T>[] | undefined, ...args: T) {
  if (Array.isArray(handler)) {
    for (const h of handler) {
      h(...args)
    }
  } else if (typeof handler === 'function') {
    handler(...args)
  }
}

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

export function findChildrenWithProvide (
  key: InjectionKey<any> | symbol,
  vnode?: VNodeChild,
): ComponentInternalInstance[] {
  if (!vnode || typeof vnode !== 'object') return []

  if (Array.isArray(vnode)) {
    return vnode.map(child => findChildrenWithProvide(key, child)).flat(1)
  } else if (vnode.suspense) {
    return findChildrenWithProvide(key, vnode.ssContent!)
  } else if (Array.isArray(vnode.children)) {
    vnode.children.map(child => findChildrenWithProvide(key, child)).flat(1)
  } else if (vnode.component) {
    if (Object.getOwnPropertySymbols(vnode.component.provides).includes(key as symbol)) {
      return [vnode.component]
    } else if (vnode.component.subTree) {
      return findChildrenWithProvide(key, vnode.component.subTree).flat(1)
    }
  }

  return []
}

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

export function isEmpty (val: any): boolean {
  return val === null || val === undefined || (typeof val === 'string' && val.trim() === '')
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

export function hasEvent (props: Record<string, any>, name: string) {
  name = 'on' + capitalize(name)
  return !!(props[name] || props[`${name}Once`] || props[`${name}Capture`] || props[`${name}OnceCapture`] || props[`${name}CaptureOnce`])
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

export function convertToUnit (str: number, unit?: string): string
export function convertToUnit (str: string | number | null | undefined, unit?: string): undefined
export function convertToUnit (str: string | number | null | undefined, unit = 'px'): string | undefined {
  if (str === null || str === '') {
    return undefined
  } else if (isNaN(+str!)) {
    return String(str)
  } else if (!isFinite(+str!)) {
    return undefined
  } else {
    return `${Number(str)}${unit}`
  }
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

/**
 * Filter attributes that should be applied to
 * the root element of an input component. Remaining
 * attributes should be passed to the <input> element inside.
 * */
export function filterInputAttrs (attrs: Record<string, unknown>) {
  const [events, props] = pickWithRest(attrs, [onRE])
  const inputEvents = omit(events, bubblingEvents)
  const [rootAttrs, inputAttrs] = pickWithRest(props, ['class', 'style', 'id', '/^data-/'])
  Object.assign(rootAttrs, events)
  Object.assign(inputAttrs, inputEvents)
  return [rootAttrs, inputAttrs]
}

export function flattenFragments (nodes: VNode[]): VNode[] {
  return nodes.map(node => {
    if (node.type === Fragment) {
      return flattenFragments(node.children as VNode[])
    } else {
      return node
    }
  }).flat()
}


type IfAny<T, Y, N> = 0 extends (1 & T) ? Y : N
export function wrapInArray<T> (
  v: T | null | undefined
): T extends readonly any[]
  ? IfAny<T, T[], T>
  : NonNullable<T>[] {
  return v == null ? [] : Array.isArray(v) ? v as any : [v]
}

type MaybePick<
  T extends object,
  U extends Extract<keyof T, string>
> = Record<string, unknown> extends T ? Partial<Pick<T, U>> : Pick<T, U>

// Array of keys
export function pickWithRest<
  T extends object,
  U extends Extract<keyof T, string>,
  E extends Extract<keyof T, string>
> (obj: T, paths: U[], exclude?: E[]): [yes: MaybePick<T, Exclude<U, E>>, no: Omit<T, Exclude<U, E>>]
// Array of keys or RegExp to test keys against
export function pickWithRest<
  T extends object,
  U extends Extract<keyof T, string>,
  E extends Extract<keyof T, string>
> (obj: T, paths: (U | RegExp)[], exclude?: E[]): [yes: Partial<T>, no: Partial<T>]
export function pickWithRest<
  T extends object,
  U extends Extract<keyof T, string>,
  E extends Extract<keyof T, string>
> (obj: T, paths: (U | RegExp)[], exclude?: E[]): [yes: Partial<T>, no: Partial<T>] {
  const found = Object.create(null)
  const rest = Object.create(null)

  for (const key in obj) {
    if (
      paths.some(path => path instanceof RegExp
        ? path.test(key)
        : path === key
      ) && !exclude?.some(path => path === key)
    ) {
      found[key] = obj[key]
    } else {
      rest[key] = obj[key]
    }
  }

  return [found, rest]
}

export function omit<
  T extends object,
  U extends Extract<keyof T, string>
> (obj: T, exclude: U[]): Omit<T, U> {
  const clone = { ...obj }

  exclude.forEach(prop => delete clone[prop])

  return clone
}

export function only<
  T extends object,
  U extends Extract<keyof T, string>
> (obj: T, include: U[]): Pick<T, U> {
  const clone = {} as T

  include.forEach(prop => clone[prop] = obj[prop])

  return clone
}

const onRE = /^on[^a-z]/
export const isOn = (key: string) => onRE.test(key)

const bubblingEvents = [
  'onAfterscriptexecute',
  'onAnimationcancel',
  'onAnimationend',
  'onAnimationiteration',
  'onAnimationstart',
  'onAuxclick',
  'onBeforeinput',
  'onBeforescriptexecute',
  'onChange',
  'onClick',
  'onCompositionend',
  'onCompositionstart',
  'onCompositionupdate',
  'onContextmenu',
  'onCopy',
  'onCut',
  'onDblclick',
  'onFocusin',
  'onFocusout',
  'onFullscreenchange',
  'onFullscreenerror',
  'onGesturechange',
  'onGestureend',
  'onGesturestart',
  'onGotpointercapture',
  'onInput',
  'onKeydown',
  'onKeypress',
  'onKeyup',
  'onLostpointercapture',
  'onMousedown',
  'onMousemove',
  'onMouseout',
  'onMouseover',
  'onMouseup',
  'onMousewheel',
  'onPaste',
  'onPointercancel',
  'onPointerdown',
  'onPointerenter',
  'onPointerleave',
  'onPointermove',
  'onPointerout',
  'onPointerover',
  'onPointerup',
  'onReset',
  'onSelect',
  'onSubmit',
  'onTouchcancel',
  'onTouchend',
  'onTouchmove',
  'onTouchstart',
  'onTransitioncancel',
  'onTransitionend',
  'onTransitionrun',
  'onTransitionstart',
  'onWheel',
]

/** Array.includes but value can be any type */
export function includes (arr: readonly any[], val: any) {
  return arr.includes(val)
}

/** Returns null if the selector is not supported, or we can't check */
export function matchesSelector (el: Element | undefined, selector: string): boolean | null {
  const supportsSelector = IN_BROWSER
    && typeof CSS !== 'undefined'
    && typeof CSS.supports !== 'undefined' &&
    CSS.supports(`selector(${selector})`)

  if (!supportsSelector) return null

  try {
    return !!el && el.matches(selector)
  } catch (err) {
    return null
  }
}