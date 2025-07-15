// Utilities
import { defineStore } from 'pinia'
import axios from 'axios'
import { toast } from 'vue3-toastify'
import { i18n } from '@/i18n/i18n'

// Types
import type { Portfolio } from '@/types/portfolios'
import type { Country, Currency, DetailCompany } from '@/types/invest'
import type {
  CompanyItem,
  CountryState,
  CurrencyState,
} from '@/store/companyList/types'

// Profile that we receive from server
export interface UserProfileResponse {
  id: string
  name: string
  first_name: string
  last_name: string
  username: string
  email: string
  is_staff: boolean
  registration_date: number
  display_name: string
  avatar: string | null
  locale: string
  country_iso: string
  currency_iso: string
  auth_provider: string
  bio: string
  external_link: string
  stock_view: string
  watchlist: string[]
  portfolios: Portfolio[]
  theme: string
  banner_color: string
}

export interface UserProfile {
  id: string
  name: string
  email: string
  username: string
  firstName: string
  familyName: string
  avatar: string | null
  languageCode: string
  registrationDate: number
  countryCode: string
  currencyCode: string
  loginMethod: string
  displayName: string
  portfolios: Portfolio[]
  watchlist: string[]
  stockView: string
  isStaff: boolean
  theme: string
  bannerColor: string
  aboutMe: string
  externalLink: string
}

export interface LoginResponse {
  access: string
  refresh: string
  user: UserProfileResponse
}

export type AuthMode =
  | 'login'
  | 'registration'
  | 'emailConfirmation'
  | 'forgotPassword'

export const useAuthStore = defineStore({
  id: 'auth',
  state: () => ({
    authMode: 'login' as AuthMode,
    // WATCHLIST
    watchlistLoading: false,
    registrationEmail: '',
    // PROFILE
    profile: null as UserProfile | null,
    countryOptions: [] as CountryState[],
    currencyOptions: [] as CurrencyState[],
  }),
  getters: {
    isAuthenticated: (state) => {
      return !!state.profile
    },
  },
  actions: {
    async fetchOptions() {
      try {
        const countryResponse = await axios.get<Country[]>(
          'api/v1/invest/country-options/'
        )
        const currencyResponse = await axios.get<Currency[]>(
          'api/v1/invest/currency-options/'
        )

        this.countryOptions = countryResponse.data.map(
          (c) =>
            ({
              id: c.id,
              key: c.slug,
              translations: c.translations,
              markets: c.markets,
            }) satisfies CountryState
        )
        this.currencyOptions = currencyResponse.data.map(
          (c) =>
            ({
              id: c.id,
              key: c.iso_code,
              translations: c.translations,
              symbol: c.symbol,
            }) satisfies CurrencyState
        )
      } catch (e) {
        console.error(e)
      }
    },
    setUserProfile(loginData: { user: UserProfileResponse }) {
      const user = loginData.user

      const profile: UserProfile = {
        aboutMe: user.bio,
        avatar: user.avatar,
        bannerColor: user.banner_color,
        countryCode: user.country_iso,
        currencyCode: user.currency_iso,
        displayName: user.display_name,
        email: user.email,
        username: user.username,
        familyName: user.last_name,
        firstName: user.first_name,
        id: user.id,
        isStaff: user.is_staff,
        languageCode: user.locale,
        loginMethod: user.auth_provider,
        name: user.name,
        portfolios: user.portfolios,
        registrationDate: user.registration_date,
        stockView: user.stock_view,
        theme: user.theme,
        watchlist: user.watchlist,
        externalLink: user.external_link,
      }
      this.profile = profile
      localStorage.setItem('profile', JSON.stringify(profile))
    },
    async checkAuth() {
      try {
        const response = await axios.get<UserProfileResponse>(
          '/api/v1/auth/user/',
          {
            withCredentials: true,
          }
        )
        this.setUserProfile({ user: response.data })
        return true
      } catch {
        this.clearAuth()
        return false
      }
    },
    clearAuth () {
      this.profile = null
      localStorage.removeItem('profile')
      document.cookie = 'jwt-auth=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;'
      document.cookie = 'jwt-refresh=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;'
    },
    async login(username: string, password: string) {
      try {
        const response = await axios.post<LoginResponse>(
          '/api/v1/auth/login/',
          {
            username,
            password,
          },
          { withCredentials: true }
        )

        this.setUserProfile(response.data)
      } catch (error) {
        console.error(error)
        toast.error(i18n.global.t('toasts.somethingWrong'))
      }
    },
    async logout() {
      try {
        await axios.post('/api/v1/auth/logout/', {}, { withCredentials: true })
      } finally {
        this.clearAuth()
      }
    },
    async refreshToken() {
      try {
        await axios.post(
          '/api/v1/auth/token/refresh/',
          {},
          { withCredentials: true }
        )
        return true
      } catch {
        await this.logout()
        return false
      }
    },
    // WATCHLIST
    async updateWatchlist(company: DetailCompany | CompanyItem) {
      if (!this.profile) return

      const { uid, ticker } = company
      const oldWatchlist = [...this.profile.watchlist]

      try {
        this.watchlistLoading = true
        const action = this.profile.watchlist.includes(uid) ? 'remove' : 'add'

        this.profile.watchlist =
          action === 'add'
            ? [...this.profile.watchlist, uid]
            : this.profile.watchlist.filter((id) => id !== uid)

        await axios.patch<UserProfileResponse>(
          'api/v1/profile/update_watchlist/',
          {
            company_uid: uid,
            action,
          },
          {
            withCredentials: true,
            headers: {
              'Content-Type': 'application/json',
            },
          }
        )

        if (action === 'remove') {
          toast.success(
            i18n.global.t(`toasts.watchlist.removed`, {
              ticker,
            })
          )
        } else {
          toast.success(
            i18n.global.t(`toasts.watchlist.added`, {
              ticker,
            })
          )
        }
      } catch (error) {
        this.profile.watchlist = oldWatchlist
        console.error(error)
        toast.error(i18n.global.t('toasts.somethingWrong'))
      } finally {
        this.watchlistLoading = false
      }
    },
  },
})
