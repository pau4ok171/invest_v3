// Composables
import { usePageStore } from '@/store/page'
import { useAuthStore } from '@/store/auth'

// Utilities
import axios from 'axios'

axios.defaults.baseURL = 'http://localhost:8000'
axios.defaults.withCredentials = true

let isRefreshing = false
let failedQueue: any[] = []

const processQueue = (error: any | null, token: string | null = null) => {
  failedQueue.forEach((prom) => {
    if (error) {
      prom.reject(error)
    } else {
      prom.resolve(token)
    }
  })
  failedQueue = []
}

axios.interceptors.response.use(
  (response) => {
    return response
  },
  async (error) => {
    const originalRequest = error.config

    if (axios.isCancel(error)) {
      return Promise.reject(error)
    }

    if (axios.isAxiosError(error)) {
      if (error.response?.status === 404) {
        const pageStore = usePageStore()
        pageStore.notFound = true
        return Promise.reject(error)
      }

      if (error.response?.status === 401 && !originalRequest._retry) {
        if (isRefreshing) {
          return new Promise((resolve, reject) => {
            failedQueue.push({ resolve, reject })
          })
            .then(() => {
              return axios(originalRequest)
            })
            .catch((e) => {
              return Promise.reject(e)
            })
        }

        originalRequest._retry = true
        isRefreshing = true
        const authStore = useAuthStore()

        try {
          const refreshed = await authStore.refreshToken()

          if (refreshed) {
            processQueue(null)
            return axios(originalRequest)
          } else {
            await authStore.logout()
            processQueue(new Error('Refresh failed'))
            return Promise.reject(error)
          }
        } catch (refreshError) {
          await authStore.logout()
          processQueue(refreshError)
          return Promise.reject(refreshError)
        } finally {
          isRefreshing = false
        }
      }
    }

    return Promise.reject(error)
  }
)

export default axios
