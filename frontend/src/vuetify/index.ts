// Vuetify
import 'vuetify/styles'
import { createVuetify } from "vuetify";
import { themes } from "@/vuetify/themes";
import { aliases, mdi } from "vuetify/iconsets/mdi-svg";
import { aliases as iAliases } from '@/vuetify/iconsets/iIcons/i-svg'

export const vuetify= createVuetify({
  theme: {
    defaultTheme: 'finargo-dark',
    themes: {
      'finargo-dark': themes.finargoDarkTheme,
      'finargo-light': themes.finargoLightTheme,
    },
  },
  icons: {
    aliases: {
      ...aliases,
      ...iAliases,
    },
    sets: {
      mdi,
    },
  },
  defaults: {
    VList: {
      activeClass: 'text-info'
    },
    VSelect: {
      activeClass: 'text-info',
    },
    VSkeletonLoader: {
      color: 'background',
    },
  },
})
