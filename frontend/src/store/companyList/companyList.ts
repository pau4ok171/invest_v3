// Utilities
import { defineStore } from 'pinia'
import axios from 'axios'
import { toast } from 'vue3-toastify'

// Types
import type { Country, ListCompany, Sector } from '@/types/invest'
import type {
  CompaniesOptions,
  CompaniesResponse,
  CountryState,
  DependentState,
  WatchlistItem,
} from './types'

const defaultCountry: CountryState = {
  id: -1,
  key: 'global',
  title: 'Global',
  markets: [],
}
const defaultSector: DependentState = {
  id: -1,
  key: 'any',
  title: 'Any',
  parentKeys: [],
}

export const useCompanyListStore = defineStore('companyList', {
  state: () => ({
    companiesAbortController: null as AbortController | null,
    companies: [] as ListCompany[],
    countries: [] as CountryState[],
    sectors: [] as DependentState[],
    countryState: defaultCountry as CountryState,
    sectorState: defaultSector as DependentState,
    nextUrl: '/api/v1/invest/companies?_limit=20' as string | null,
    totalCompanyLength: 0,
    fetching: false,
    contentMode: 'table' as 'table' | 'tile',
  }),
  getters: {
    lastUpdate(state): string | undefined {
      if (!this.companies.length) return undefined
      if (this.companies.length === 1) return this.companies[0].updated
      return state.companies.reduce((prev: ListCompany, cur: ListCompany) =>
        prev.updated > cur.updated ? prev : cur
      ).updated
    },
    filteredSectors(state) {
      if (state.countryState.key === 'global') return state.sectors

      return state.sectors.filter(
        (s) => s.parentKeys.includes(state.countryState.id) || s.key === 'any'
      )
    },
  },
  actions: {
    async initFilters() {
      this.countryState = defaultCountry
      this.sectorState = defaultSector
      await this.fetchCountries()
      await this.fetchSectors()
    },
    async fetchCountries() {
      try {
        const response = await axios.get<Country[]>('/api/v1/invest/countries')

        const countries = response.data.map((c) => ({
          id: c.id,
          key: c.slug,
          title: c.title,
          markets: c.markets,
        })) satisfies CountryState[]

        this.countries = [
          { id: -1, title: 'Global', key: 'global', markets: [] },
          ...countries,
        ] satisfies CountryState[]
      } catch (e) {
        this._handleError(e)
      }
    },
    async fetchSectors() {
      try {
        const response = await axios.get<Sector[]>('/api/v1/invest/sectors')

        const sectors = response.data.map((s) => ({
          id: s.id,
          key: s.slug,
          title: s.title,
          parentKeys: s.countries.map((c) => c.id),
        })) satisfies DependentState[]

        this.sectors = [
          { id: -1, title: 'Any', key: 'any', parentKeys: [] },
          ...sectors,
        ] satisfies DependentState[]
      } catch (e) {
        this._handleError(e)
      }
    },
    resetSectorState() {
      this.sectorState = defaultSector
    },
    async fetchCompanies({ done }: CompaniesOptions, clear: boolean = false) {
      try {
        //
        if (this.companiesAbortController) {
          this.companiesAbortController.abort()
        }
        this.companiesAbortController = new AbortController()

        // 1. Reset state if necessary
        if (clear) {
          this._resetCompaniesState()
        }

        // 2. Check if nextUrl is valid
        if (!this._hasValidNextUrl(this.nextUrl)) {
          return done('empty')
        }

        // 3. Execute request
        this.fetching = true
        const response = await axios.get<CompaniesResponse>(this.nextUrl, {
          signal: this.companiesAbortController.signal,
        })

        // 4. Success response process
        this._handleSuccessResponse(response.data)

        // 5. Notify of success response
        done('ok')
      } catch (error) {
        if (!axios.isCancel(error)) {
          done('error')
          this._handleError(error)
        }

        // 6. Error response process
        this._handleError(error)
        done('error')
        throw error
      } finally {
        // 7. Reset loading state
        this.companiesAbortController = null
        this.fetching = false
      }
    },
    _resetCompaniesState() {
      this.nextUrl = this._buildInitUrl()
      this.companies = []
      this.totalCompanyLength = 0
    },
    _buildInitUrl() {
      return `api/v1/invest/companies/?${new URLSearchParams({
        country: this.countryState.key,
        sector: this.sectorState.key,
        _limit: '20',
      })}`
    },
    _handleError(error: unknown) {
      console.log(error)
      // It's possible to send error to a system of monitoring
      // Sentry.captureException(error)
    },
    _handleSuccessResponse(data: CompaniesResponse) {
      this.companies = [...this.companies, ...data.results]
      this.nextUrl = data.next
      this.totalCompanyLength = data.count
    },
    _hasValidNextUrl(nextUrl: string | null): nextUrl is string {
      return !!nextUrl && nextUrl.trim() !== ''
    },
    async toggleWatchlisted(item: WatchlistItem) {
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
