// Types
import type {InjectionKey} from "vue";

interface MenuProvide {
  register (): void
  unregister (): void
  closeParents (e?: MouseEvent): void
}

export const BaseMenuSymbol: InjectionKey<MenuProvide> = Symbol.for('visagiste:base-menu')