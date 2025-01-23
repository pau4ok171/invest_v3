// Composables
// TODO: CreateDate
import { createDefaults, DefaultsSymbol } from "./composables/defaults";
import { createDisplay, DisplaySymbol } from "./composables/display";
// TODO: CreateGoTo
// TODO: CreateIcons
import { createLocale, LocaleSymbol } from "./composables/locale";
import  { createTheme, ThemeSymbol } from "./composables/theme";

// Utilities
import {defineComponent, nextTick, reactive} from "vue";
import {getUid, IN_BROWSER, mergeDeep} from "@/apps/visagiste/utils";

// Types
import type { App, ComponentPublicInstance, InjectionKey } from "vue";
// TODO: Create DateOptions
import type { DefaultsOptions } from "./composables/defaults";
import type { DisplayOptions, SSROptions } from "./composables/display";
// TODO: Create GoToOptions
// TODO: Create IconOptions
import type { LocaleOptions, RtlOptions } from "@/apps/visagiste/composables/locale";
import type { ThemeOptions } from "@/apps/visagiste/composables/theme";
export * from "@/apps/visagiste/composables"

export interface VisagisteOptions {
  aliases?: Record<string, any>
  blueprint?: Blueprint
  components?: Record<string, any>
  // date?: DateOptions
  directives?: Record<string, any>
  defaults?: DefaultsOptions
  display?: DisplayOptions
  // goTo?: GoToOptions
  theme?: ThemeOptions
  // icons?: IconOptions
  locale?: LocaleOptions & RtlOptions
  ssr?: SSROptions
}

export interface Blueprint extends Omit<VisagisteOptions, 'blueprint'> {}

export function createVisagiste (visagiste: VisagisteOptions = {}) {
  const { blueprint, ...rest } = visagiste
  const options: VisagisteOptions = mergeDeep(blueprint, rest)
  const {
    aliases = {},
    components = {},
    directives = {},
  } = options

  const defaults = createDefaults(options.defaults)
  const display = createDisplay(options.display, options.ssr)
  const theme = createTheme(options.theme)
  // const icons = createIcons(options.icons)
  const locale = createLocale(options.locale)
  // const date = createDate(options.date)
  // const goTo = createGoTo(options.goTo)

  const install = (app: App) => {
    for (const key in directives) {
      app.directive(key, directives[key])
    }
    for (const key in components) {
      app.component(key, components[key])
    }

    for (const key in aliases) {
      app.component(key, defineComponent({
        ...aliases[key],
        name: key,
        aliasName: aliases[key].name,
      }))
    }

    theme.install(app)

    app.provide(DefaultsSymbol, defaults)
    app.provide(DisplaySymbol, display)
    app.provide(ThemeSymbol, theme)
    // app.provide(IconSymbol, icons)
    app.provide(LocaleSymbol, locale)
    // app.provide(DateOptionsSymbol, date.options)
    // app.provide(DateAdapterSymbol, date.instance)
    // app.provide(GoToSymbol, goTo)

    // In case of SSR
    if (IN_BROWSER && options.ssr) {
      if (app.$nuxt) {
        app.$nuxt.hook('app:suspense:resolve', () => {
          display.update()
        })
      } else {
        const { mount } = app
        app.mount = (...args) => {
          const vm = mount(...args)
          nextTick(() => display.update())
          app.mount = mount
          return vm
        }
      }
    }

    getUid.reset()

    app.mixin({
      computed: {
        $visagiste () {
          return reactive({
            defaults: inject.call(this, DefaultsSymbol),
            display: inject.call(this, DisplaySymbol),
            theme: inject.call(this, ThemeSymbol),
            // icons: inject.call(this, IconSymbol),
            locale: inject.call(this, LocaleSymbol),
            // date: inject.call(this, DateAdapterSymbol),
          })
        }
      }
    })
  }

  return {
    install,
    defaults,
    display,
    theme,
    // icons,
    locale,
    // date,
    // goTo,
  }
}

function inject (this: ComponentPublicInstance, key: InjectionKey<any> | string) {
  const vm = this.$

  const provides = vm.parent?.provides ?? vm.vnode.appContext?.provides

  if (provides && (key as any) in provides) {
    return provides[(key as string)]
  }
}