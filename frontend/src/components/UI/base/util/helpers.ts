import type {PropType} from "vue";


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
