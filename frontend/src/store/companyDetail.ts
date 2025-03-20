// Utilities
import { defineStore } from 'pinia'
import axios from 'axios'
import { toast } from 'vue3-toastify'

// Types
import type {
  AnalystIdea,
  Candle,
  Competitor,
  DetailCompany,
  News,
  Report,
} from '@/types/invest'
import type { Portfolio } from '@/types/portfolios'
import type { Note } from '@/types/notes'
import type { Statement } from '@/types/statements'

interface PriceDataResponse extends Array<Candle> {}

interface CompanyResponse {
  company: DetailCompany
  portfolios: Portfolio[]
  notes: Note[]
  statements: Statement[]
  snowflake: number[]
  peers: Competitor[]
}

function genDefaultCompany(): DetailCompany {
  return {
    absolute_url: undefined,
    analyst_ideas: [] as AnalystIdea[],
    average_weekly_mouvement: undefined,
    company_news: [] as News[],
    country: {
      currency: {
        id: undefined,
        name: undefined,
        name_iso: undefined,
        symbol: undefined,
      },
      id: undefined,
      markets: [],
      slug: undefined,
      title: undefined,
    },
    description: undefined,
    formatting: {
      primaryCurrencyISO: undefined,
      primaryCurrencySymbol: undefined,
      reportCurrencyISO: undefined,
      reportCurrencySymbol: undefined,
      tradingCurrencyISO: undefined,
      tradingCurrencySymbol: undefined,
    },
    id: undefined,
    is_watchlisted: undefined,
    last_reported_earnings: undefined,
    logo_url: undefined,
    market: {
      country: undefined,
      id: undefined,
      slug: undefined,
      title: undefined,
      return_7d: undefined,
      return_30d: undefined,
      return_90d: undefined,
      return_1y: undefined,
      return_3y: undefined,
      return_5y: undefined,
      average_weekly_mouvement: undefined,
      volatility_10p: undefined,
      volatility_90p: undefined,
    },
    next_dividend: {
      currency: {
        id: undefined,
        name: undefined,
        name_iso: undefined,
        symbol: undefined,
      },
      declared_date: undefined,
      dividend_amount: undefined,
      dividend_yield: undefined,
      ex_dividend_date: undefined,
      pay_date: undefined,
      scale: undefined,
      scale_unit: undefined,
    },
    next_earnings: undefined,
    price_data: {
      capitalisation: undefined,
      last_price: undefined,
    },
    reports: [] as Report[],
    return_1y: undefined,
    return_30d: undefined,
    return_3y: undefined,
    return_5y: undefined,
    return_7d: undefined,
    return_90d: undefined,
    sector: {
      main_header: undefined,
      slug: undefined,
      title: undefined,
    },
    sector_market: {
      average_weekly_mouvement: undefined,
      return_1y: undefined,
      return_30d: undefined,
      return_3y: undefined,
      return_5y: undefined,
      return_7d: undefined,
      return_90d: undefined,
    },
    short_description: undefined,
    slug: undefined,
    ticker: undefined,
    title: undefined,
    uid: undefined,
    website: undefined,
    year_founded: undefined,
  }
}

export const useCompanyDetailStore = defineStore({
  id: 'companyDetail',
  state: () => ({
    priceData: [] as Candle[],
    company: genDefaultCompany() as DetailCompany,
    portfolios: [] as Portfolio[],
    notes: [] as Note[],
    statements: {} as Record<string, Statement>,
    snowflake: [] as Number[],
    competitors: [] as Competitor[],
    note: {} as Note,
    noteSavedContent: '',
    notesEditorIsActive: false,
    fetchingPriceData: false,
    fetchingCompany: false,
    watchlistLoading: false,
  }),
  getters: {
    chartPriceData(state) {
      return state.priceData.map((F) => [F['time'], F['close']])
    },
  },
  actions: {
    updatePortfolios(portfolio: Portfolio) {
      let portfolios: Portfolio[] = []

      this.portfolios.forEach((p: Portfolio) => {
        if (p.id === portfolio.id) {
          portfolios.push(portfolio)
        } else {
          portfolios.push(p)
        }
      })

      this.portfolios = portfolios
    },
    addNote(note: Note) {
      this.notes.push(note)
    },
    updateNotes(note: Note) {
      let _notes: Note[] = []
      this.notes.forEach((n: Note) => {
        if (n.id === note.id) {
          _notes.push(note)
        } else {
          _notes.push(n)
        }
        this.notes = _notes
      })
    },
    async fetchPriceData(companySlug: string) {
      try {
        this.fetchingPriceData = true

        const response = await axios.get<PriceDataResponse>(
          `api/v1/invest/price_data/${companySlug}`
        )
        this.priceData = [...response.data]
      } catch (error) {
        console.log(error)
      } finally {
        this.fetchingPriceData = false
      }
    },
    async fetchCompany(companySlug: string) {
      try {
        this.fetchingCompany = true

        const response = await axios.get<CompanyResponse>(
          `api/v1/invest/companies/${companySlug}`
        )

        this.handleCompanyResponse(response.data)
      } catch (error) {
        console.log(error)
      } finally {
        this.fetchingCompany = false
      }
    },
    handleCompanyResponse(data: CompanyResponse) {
      this.company = data.company
      this.portfolios = data.portfolios
      this.notes = data.notes
      this.statements = data.statements.reduce(
        (res: Record<string, Statement>, item: Statement) => {
          res[item.name] = item
          return res
        },
        {}
      )
      this.snowflake = Object.values(data.snowflake)
      this.competitors = data.peers
    },
    async toggleWatchlisted() {
      const formData = new FormData()
      Object.entries({ uid: this.company.uid }).forEach(
        ([key, val]: [string, any]) => {
          formData.append(key, val)
        }
      )

      let status = 'start' as 'start' | 'added' | 'deleted'

      try {
        this.watchlistLoading = true

        if (this.company.is_watchlisted) {
          status = 'deleted'
          const _ = await axios.delete('/api/v1/invest/toggle_to_watchlist/', {
            data: formData,
          })
        } else {
          status = 'added'
          const _ = await axios.patch(
            '/api/v1/invest/toggle_to_watchlist/',
            formData
          )
        }

        this.company.is_watchlisted = status === 'added'
        toast.success(
          `${this.company.ticker} was successfully ${status === 'added' ? 'added to' : 'remove from'} watchlist`
        )
      } catch (error) {
        console.log(error)
        toast.error('Something was wrong... Try again')
      } finally {
        this.watchlistLoading = false
      }
    },
    async deleteNote(note: Note) {
      try {
        const _ = await axios.delete(`/notes/api/v1/notes/${note.id}`)

        this.notes = this.notes.filter((n) => n.id !== note.id)
        toast.success('Note was successfully deleted')
      } catch (error) {
        console.log(error)
        toast.error('Something was wrong... Try again')
      }
    },
  },
})
