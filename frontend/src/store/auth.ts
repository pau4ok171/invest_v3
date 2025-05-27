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
        axios.defaults.headers.common['Authorization'] = `Token ${newToken}`
        localStorage.setItem('token', newToken)
      } else {
        const token = localStorage.getItem('token')
        this.token = token || ''
        axios.defaults.headers.common['Authorization'] = `Token ${this.token}`
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
    async fetchUserProfile() {
      if (!this.token) return

      try {
        const response = await axios.get('api/v1/profile/me/')

        this.profile = response.data
      } catch (error) {
        console.log(error)
      }
    },
  },
})
