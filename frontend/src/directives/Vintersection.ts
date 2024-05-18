import type {DirectiveBinding} from "vue";

export default {
    mounted(el: Element, binding: DirectiveBinding) {
    const options = {
      rootMargin: "0px",
      threshold: 1.0,
    };
    const callback = (entries: Array<IntersectionObserverEntry>) => {
      if (entries[0].isIntersecting) {
        binding.value()
      }
    }
    const observer = new IntersectionObserver(callback, options);
    observer.observe(el)
  },
}