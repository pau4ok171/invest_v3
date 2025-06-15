// Utilities
import { defineStore } from 'pinia'
import axios from 'axios'
import { toast } from 'vue3-toastify'
import { i18n } from '@/i18n/i18n'

// Types
import type { Portfolio } from '@/types/portfolios'
import type { DetailCompany } from '@/types/invest'
import type { CompanyItem } from '@/store/companyList/types'

export interface Profile {
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

export type AuthMode = 'login' | 'registration' | 'emailConfirmation' | 'forgotPassword'

export const useAuthStore = defineStore({
  id: 'auth',
  state: () => ({
    token: '',
    authMode: 'login' as AuthMode,
    profile: {} as Profile,
    // WATCHLIST
    watchlistLoading: false,
    registrationEmail: '',
  }),
  getters: {
    isAuthenticated: (state) => {
      return !!state.token
    },
  },
  actions: {
    setToken(newToken: string | null = null) {
      if (newToken) {
        this.token = newToken
        localStorage.setItem('token', newToken)
      } else {
        this.token = localStorage.getItem('token') || ''
      }

      // Всегда устанавливаем заголовок с текущим токеном
      if (this.token) {
        axios.defaults.headers.common['Authorization'] = `Token ${this.token}`
      } else {
        delete axios.defaults.headers.common['Authorization']
      }
    },
    async fetchUserProfile() {
      if (!this.token) return

      try {
        // Добавляем завершающий слеш и правильный префикс URL
        const response = await axios.get('/api/v1/profile/me/')
        this.profile = response.data
      } catch (error) {
        console.error('Profile fetch error:', error)
        // При ошибке 403 сбрасываем токен
        if (axios.isAxiosError(error) && error.response?.status === 403) {
          this.logout()
        }
      }
    },
    async login(token: string) {
      this.setToken(token)
      await this.fetchUserProfile()
    },
    logout() {
      axios.defaults.headers.common['Authorization'] = ''

      localStorage.removeItem('token')

      this.token = ''
      this.profile = {} as Profile
    },
    // WATCHLIST
    async updateWatchlist(company: DetailCompany | CompanyItem) {
      if (!this.profile.watchlist) return

      const { uid, ticker } = company
      const isCurrentlyWatchlisted = this.profile.watchlist.includes(uid)
      const action = isCurrentlyWatchlisted ? 'remove' : 'add'

      try {
        this.watchlistLoading = true

        if (action === 'add') {
          this.profile.watchlist.push(uid)
        } else {
          this.profile.watchlist = this.profile.watchlist.filter(
            (company_uid) => company_uid !== uid
          )
        }

        const response = await axios.patch<Profile>(
          'api/v1/profile/update_watchlist/',
          {
            company_uid: uid,
            action,
          },
          {
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
        if (action === 'add') {
          this.profile.watchlist = this.profile.watchlist.filter(
            (company_uid) => company_uid !== uid
          )
        } else {
          this.profile.watchlist.push(uid)
        }

        console.log(error)
        toast.error(i18n.global.t('toasts.somethingWrong'))
      } finally {
        this.watchlistLoading = false
      }
    },
  },
})
