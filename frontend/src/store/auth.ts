import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore({
  id: 'auth',
  state: () => ({
    userInfo: {} as {
      first_name: string
      is_anonymous: boolean
      is_staff: boolean
      last_name: string
      stage_in_days: number
    },
    token: '',
    hasAccount: true,
  }),
  getters: {
    isAuthenticated: (state) => {
      return !!state.token
    },
  },
  actions: {
    init() {
      const token = localStorage.getItem('token')
      if (token) {
        this.token = token
      } else {
        this.token = ''
      }
    },
    async fetchUserInfo() {
      await axios
        .get('api/v1/admin/users/')
        .then((r) => (this.userInfo = r.data))
        .catch((e) => console.log(e))
    },
  },
})
