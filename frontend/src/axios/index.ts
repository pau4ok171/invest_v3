// Composables
import { usePageStore } from '@/store/page'

// Utilities
import axios from 'axios'

axios.defaults.baseURL = 'http://localhost:8000'

axios.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    if (axios.isCancel(error)) {
      return Promise.reject(error)
    }

    if (axios.isAxiosError(error)) {
      if (error.response?.status === 404) {
        const pageStore = usePageStore()
        pageStore.notFound = true
      }
    }
    return Promise.reject(error)
  }
)

export default axios
