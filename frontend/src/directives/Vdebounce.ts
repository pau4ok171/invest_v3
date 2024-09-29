import type {DirectiveBinding} from "vue";

function debounce(cb: Function, delay = 300) {
  let timeoutID: number | undefined = undefined;
  return function (this: GlobalEventHandlers) {
    clearTimeout(timeoutID)
    const args = arguments
    const that = this
    timeoutID = setTimeout(function () {
      cb.apply(that, args)
    }, delay)
  }
}

export default {
  mounted(el: HTMLInputElement, binding: DirectiveBinding) {
    if (binding.value !== binding.oldValue) {
      el.oninput = debounce(() => {
        el.dispatchEvent(new Event('change'))
      }, parseInt(binding.value) || 300)
    }
  }
}