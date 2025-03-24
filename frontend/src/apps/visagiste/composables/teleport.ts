// Utilities
import {computed, warn} from "vue";
import {IN_BROWSER} from "@/apps/visagiste/utils";

export function useTeleport (target: () => (boolean | string | ParentNode)) {
  const teleportTarget = computed(() => {
    const _target = target()

    if (_target === true || !IN_BROWSER) return undefined

    const targetElement = _target === false
      ? document.body
      : typeof _target === 'string'
        ? document.querySelector(_target)
        : _target

    if (targetElement === null) {
      warn(`Unable to locate target ${_target}`)
      return undefined
    }

    let container = [...targetElement.children].find(el => el.matches('.base-overlay-container'))

    if (!container) {
      container = document.createElement('div')
      container.className = 'base-overlay-container'
      targetElement.appendChild(container)
    }

    return container
  })

  return { teleportTarget }
}