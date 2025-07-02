// Utilities
import { defineStore } from 'pinia'
import axios from 'axios'
import { toast } from 'vue3-toastify'
import { i18n } from '@/i18n/i18n'

// Types
import type { Portfolio } from '@/types/portfolios'
import type { DetailCompany } from '@/types/invest'
import type { CompanyItem } from '@/store/companyList/types'

export interface UserProfile {
  id: string
  name: string
  email: string
  first_name: string
  last_name: string
  avatar: string | null
  locale: string
  register_date: number
  country_iso: string | null
  currency: string | null
  auth_provider: string
  display_name: string | null
  portfolios: Portfolio[]
  watchlist: string[]
  stock_view: string
  is_staff: boolean
}

export interface LoginResponse {
  access: string
  refresh: string
  user: UserProfile
}

export type AuthMode =
  | 'login'
  | 'registration'
  | 'emailConfirmation'
  | 'forgotPassword'

export const useAuthStore = defineStore({
  id: 'auth',
  state: () => ({
    token: '',
    authMode: 'login' as AuthMode,
    profile: null as UserProfile | null,
    // WATCHLIST
    watchlistLoading: false,
    registrationEmail: '',
  }),
  getters: {
    isAuthenticated: (state) => {
      return !!state.profile
    },
  },
  actions: {
    setUserProfile(loginData: LoginResponse) {
      this.profile = loginData.user
      localStorage.setItem('profile', JSON.stringify(loginData.user))
    },
    async checkAuth() {
      try {
        const response = await axios.get<UserProfile>('/api/v1/auth/user/', {
          withCredentials: true,
        })
        this.profile = response.data
        return true
      } catch {
        this.profile = null
        return false
      }
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
        this.profile = null
        localStorage.removeItem('profile')
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

        await axios.patch<UserProfile>(
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
