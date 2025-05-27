// Utilities
import { defineStore } from 'pinia'
import axios from 'axios'

// Types
import type { Portfolio } from '@/types/portfolios'

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

export type AuthMode = 'login' | 'registration'

export const useAuthStore = defineStore({
  id: 'auth',
  state: () => ({
    token: '',
    authMode: 'login' as AuthMode,
    profile: {} as Profile,
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
  },
})
