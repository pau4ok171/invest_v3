// Styles
import 'vuetify/styles'

// Components
import { VFileUpload } from 'vuetify/labs/VFileUpload'

// Composables
import { createVuetify } from 'vuetify'

// Utilities
import { themes } from '@/vuetify/themes'
import { aliases, mdi } from 'vuetify/iconsets/mdi-svg'
import { aliases as iAliases } from '@/vuetify/iconsets/iIcons/i-svg'

export const vuetify = createVuetify({
  components: {
    VFileUpload,
  },
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
      activeClass: 'text-info',
    },
    VSelect: {
      activeClass: 'text-info',
    },
    VSkeletonLoader: {
      color: 'background',
    },
  },
})
