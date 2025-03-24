// Utilities
import { defineStore } from 'pinia'
import axios from 'axios'
import { toast } from 'vue3-toastify'

// Types
import type { ListCompany } from '@/types/invest'
import type {
  InfiniteScrollSide,
  InfiniteScrollStatus,
} from '@/apps/visagiste/components/BaseInfiniteScroll/BaseInfiniteScroll.vue'

const defaultCurrency = {
  id: 0,
  name: '',
  name_iso: '',
  symbol: '',
}
const defaultCountry = {
  id: 0,
  title: '',
  slug: '',
  currency: defaultCurrency,
  markets: [],
}
const defaultSector = {
  main_header: '',
  slug: '',
  title: '',
}

interface FetchCompaniesOptions {
  side?: InfiniteScrollSide
  done: (status: InfiniteScrollStatus) => void
}

interface CompaniesResponse {
  results: ListCompany[]
  next: string | null
  count: number
}

interface FilterOptions {
  filterName: 'country' | 'sector'
  item: { title: string; slug: string }
}

export const useCompanyListStore = defineStore({
  id: 'companyList',
  state: () => ({
    companiesAbortController: null as AbortController | null,
    companies: [] as ListCompany[],
    filters: {
      country: [],
      sector: [],
    },
    activeFilters: {
      country: defaultCountry,
      sector: defaultSector,
    },
    nextUrl: '/api/v1/invest/companies?_limit=20' as string | null,
    totalCompanyLength: 0,
    fetching: false,
  }),
  getters: {
    lastUpdate(state) {
      if (!this.companies.length) return undefined
      if (this.companies.length === 1) return this.companies[0].updated
      return state.companies.reduce((prev: ListCompany, cur: ListCompany) => prev.updated > cur.updated ? prev : cur).updated
    },
  },
  actions: {
    async fetchCompanies(
      { done }: FetchCompaniesOptions,
      clear: boolean = false
    ) {

      try {
        //
        if (this.companiesAbortController) {
          this.companiesAbortController.abort()
        }
        this.companiesAbortController = new AbortController()

        // 1. Reset state if necessary
        if (clear) {
          this.resetCompaniesState()
        }

        // 2. Check if nextUrl is valid
        if (!this.hasValidNextUrl(this.nextUrl)) {
          return done('empty')
        }

        // 3. Execute request
        this.fetching = true
        const response = await axios.get<CompaniesResponse>(this.nextUrl, {
          signal: this.companiesAbortController.signal
        })

        // 4. Success response process
        this.handleSuccessResponse(response.data)

        // 5. Notify of success response
        done('ok')
      } catch (error) {
        if (!axios.isCancel(error)) {
          done('error')
          this.handleError(error)
        }

        // 6. Error response process
        this.handleError(error)
        done('error')
        throw error
      } finally {
        // 7. Reset loading state
        this.companiesAbortController = null
        this.fetching = false
      }
    },
    resetCompaniesState() {
      this.nextUrl = this.buildInitUrl()
      this.companies = []
      this.totalCompanyLength = 0
    },
    buildInitUrl() {
      return `api/v1/invest/companies/?${new URLSearchParams({
        country: this.activeFilters.country.slug,
        sector: this.activeFilters.sector.slug,
        _limit: '20',
      })}`
    },
    hasValidNextUrl(nextUrl: string | null): nextUrl is string {
      return !!nextUrl && nextUrl.trim() !== ''
    },
    handleSuccessResponse(data: CompaniesResponse) {
      this.companies = [...this.companies, ...data.results]
      this.nextUrl = data.next
      this.totalCompanyLength = data.count
    },
    handleError(error: unknown) {
      console.log(error)
      // It's possible to send error to a system of monitoring
      // Sentry.captureException(error)
    },
    async fetchFilters() {
      await axios
        .get('/api/v1/invest/filters')
        .then((response) => {
          this.filters.country = [
            {
              title: 'Global',
              slug: 'global',
              required: true,
            },
            ...response.data.filters.country,
          ]
          this.filters.sector = [
            { title: 'Any', slug: 'any', required: true },
            ...response.data.filters.sector,
          ]
          this.activeFilters.country = this.filters.country[0]
          this.activeFilters.sector = this.filters.sector[0]
        })
        .catch((error) => console.log(error))
    },
    async fetchFiltersByCountry() {
      await axios
        .get(`api/v1/invest/filters/sector/${this.activeFilters.country.slug}`)
        .then((response) => {
          this.filters.sector = [
            { title: 'Any', slug: 'any', required: true },
            ...response.data.filters.sector,
          ]
        })
        .catch((error) => console.log(error))
    },
    async changeFilter(options: FilterOptions) {
      if (options.filterName === 'country') {
        this.activeFilters.sector = this.filters.sector[0]
      }
      this.activeFilters[options.filterName] = options.item
      await this.fetchFiltersByCountry()
      await this.fetchCompanies({ done: (status: string) => status }, true)
    },
    async toggleWatchlisted(
      item: {
        watchlisted: boolean
        uid: string
        ticker: string
      }
    ) {
      const formData = new FormData()
      const formDataPayload: Object = {
        uid: item.uid,
      }
      Object.entries(formDataPayload).forEach(([key, val]) =>
        formData.append(key, val)
      )

      let isSuccess = false

      if (item.watchlisted) {
        await axios
          .delete('/api/v1/invest/toggle_to_watchlist/', { data: formData })
          .then(() => {
            isSuccess = true
            toast.success(
              `Company ${item.ticker.toUpperCase()} was removed from watchlist`
            )
          })
          .catch((error) => {
            isSuccess = false
            console.log(error)
            toast.error('Something was wrong...')
          })
      } else {
        await axios
          .patch('/api/v1/invest/toggle_to_watchlist/', formData)
          .then(() => {
            isSuccess = true
            toast.success(
              `Company ${item.ticker.toUpperCase()} was added to watchlist`
            )
          })
          .catch((error) => {
            isSuccess = false
            console.log(error)
            toast.error('Something was wrong...')
          })
      }

      if (!isSuccess) return

      const company = this.companies.find((c) => c.uid === item.uid)
      if (company) company.is_watchlisted = !company.is_watchlisted
    },
  },
})
