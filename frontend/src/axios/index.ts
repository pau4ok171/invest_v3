// Utilities
import axios from 'axios'
import { usePageStore } from '@/store/page'

axios.defaults.baseURL = 'http://localhost:8000'

axios.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    if (error.response.status === 404) {
      const pageStore = usePageStore()

      pageStore.notFound = true
    }
    return Promise.reject(error)
  }
)

export default axios
