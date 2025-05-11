// Utilities
import { provide, inject, ref, onMounted, onUnmounted } from 'vue'

// Types
import type { Ref } from 'vue'
import type { CSSProperties } from 'vue'

type Position = 'top' | 'left' | 'right' | 'bottom'

interface SectionContext {
  activeSection: Ref<string>
  registerSection: (id: string, el: Element | null) => void
  scrollToSection: (id: string) => void
  changeSection: (id: string[]) => void
}

interface Layer {
  top: number
  bottom: number
  left: number
  right: number
}

interface LayoutItem extends Layer {
  id: string
  size: number
  position: Position
}

const SectionSymbol = Symbol('SectionContext')

export function provideSectionContext(layout: {
  getLayoutItem: (id: string) => LayoutItem | undefined
  mainRect: Ref<Layer>
  mainStyles: Ref<CSSProperties>
}) {
  const activeSection = ref('overview')
  const sections = new Map<string, Element>()
  let observer: IntersectionObserver | null = null

  const initObserver = () => {
    observer = new IntersectionObserver(
      (entries) => {
        let mostVisibleEntry: IntersectionObserverEntry | null = null

        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            if (
              !mostVisibleEntry ||
              entry.intersectionRatio > mostVisibleEntry.intersectionRatio
            ) {
              mostVisibleEntry = entry
            }
          }
        })

        if (mostVisibleEntry) {
          const newActiveSection = (mostVisibleEntry as any).target.id
          if (activeSection.value !== newActiveSection) {
            activeSection.value = newActiveSection
          }
        }
      },
      {
        root: null,
        rootMargin: '-50% 0px',
        threshold: [0, 0.1, 0.5, 1],
      }
    )

    sections.forEach((section) => observer?.observe(section))
  }

  const registerSection = (id: string, el: Element | null) => {
    if (!el) {
      sections.delete(id)
      if (observer) {
        const existingEl = sections.get(id)
        if (existingEl) observer.unobserve(existingEl)
      }
      return
    }

    sections.set(id, el)
    if (observer) {
      observer.observe(el)
    }
  }

  const changeSection = (section: string[]) => {
    if (section.length) {
      scrollToSection(section[0])
    }
  }

  const scrollToSection = (id: string) => {
    const section = sections.get(id)
    if (section) {
      observer?.disconnect()

      const rect = section.getBoundingClientRect()
      const windowScroll = document.documentElement.scrollTop
      const scrollTop = rect.top + windowScroll - layout.mainRect.value.top

      window.scrollTo({
        top: scrollTop,
        behavior: 'smooth',
      })

      setTimeout(() => {
        if (observer) {
          sections.forEach((el) => observer?.observe(el))
        }
      }, 1000)
    }
  }

  onMounted(initObserver)
  onUnmounted(() => {
    observer?.disconnect()
    observer = null
  })

  const context: SectionContext = {
    activeSection,
    registerSection,
    changeSection,
    scrollToSection,
  }

  provide(SectionSymbol, context)
  return context
}

export function useSectionContext() {
  const context = inject<SectionContext>(SectionSymbol)
  if (!context) {
    throw new Error('useSectionContext must be used within a provider')
  }
  return context
}
