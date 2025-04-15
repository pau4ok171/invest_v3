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
  Snowflake,
  SnowflakeKey,
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
  peers: Competitor[]
}

function genDefaultCompany(): DetailCompany {
  return {
    absolute_url: '',
    analyst_ideas: [] as AnalystIdea[],
    average_weekly_mouvement: 0,
    company_news: [] as News[],
    country: {
      currency: {
        id: -1,
        name: '',
        name_iso: '',
        symbol: '',
      },
      id: -1,
      markets: [],
      slug: '',
      title: '',
    },
    description: '',
    formatting: {
      primaryCurrencyISO: '',
      primaryCurrencySymbol: '',
      reportCurrencyISO: '',
      reportCurrencySymbol: '',
      tradingCurrencyISO: '',
      tradingCurrencySymbol: '',
    },
    id: -1,
    is_watchlisted: false,
    last_reported_earnings: '',
    logo_url: '',
    market: {
      country: -1,
      id: -1,
      slug: '',
      title: '',
      return_7d: 0,
      return_30d: 0,
      return_90d: 0,
      return_1y: 0,
      return_3y: 0,
      return_5y: 0,
      average_weekly_mouvement: 0,
      volatility_10p: 0,
      volatility_90p: 0,
    },
    next_dividend: {
      currency: {
        id: -1,
        name: '',
        name_iso: '',
        symbol: '',
      },
      declared_date: '',
      dividend_amount: 0,
      dividend_yield: 0,
      ex_dividend_date: '',
      pay_date: '',
      scale: '',
      scale_unit: 0,
    },
    next_earnings: '',
    price_data: {
      capitalisation: 0,
      last_price: 0,
    },
    reports: [] as Report[],
    return_1y: 0,
    return_30d: 0,
    return_3y: 0,
    return_5y: 0,
    return_7d: 0,
    return_90d: 0,
    sector: {
      id: -1,
      main_header: '',
      slug: '',
      title: '',
      countries: [],
    },
    sector_market: {
      average_weekly_mouvement: 0,
      return_1y: 0,
      return_30d: 0,
      return_3y: 0,
      return_5y: 0,
      return_7d: 0,
      return_90d: 0,
    },
    short_description: '',
    slug: '',
    ticker: '',
    title: '',
    uid: '',
    website: '',
    year_founded: 0,
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
    snowflake: {
      value: [],
      future: [],
      past: [],
      health: [],
      dividends: [],
    } as Snowflake,
    competitors: [] as Competitor[],
    note: {} as Note,
    noteSavedContent: '',
    notesEditorIsActive: false,
    fetchingPriceData: false,
    fetchingCompany: false,
    watchlistLoading: false,
    lateralMenuComponentName: null as 'notes' | 'news' | null,
  }),
  getters: {
    chartPriceData(state) {
      return state.priceData.map((F) => [F['time'], F['close']])
    },
  },
  actions: {
    async createPortfolio(portfolioName: string): Promise<'success' | 'error'> {
      const formData = new FormData()
      const formDataFields: Object = {
        portfolio_name: portfolioName,
      }
      Object.entries(formDataFields).forEach(([key, val]) =>
        formData.append(key, val)
      )

      try {
        const response = await axios.post(
          'portfolio/api/v1/portfolios/portfolios/',
          formData
        )

        this.portfolios.push(response.data)
        toast.success(`Portfolio ${response.data.name} was created`)
        return 'success'
      } catch (error) {
        console.log(error)
        toast.error('Something was wrong...')
        return 'error'
      }
    },
    async updatePortfolio(action: 'include' | 'exclude', portfolio: Portfolio) {
      const formData = new FormData()
      Object.entries({
        action: action,
        company_id: this.company.id,
      }).forEach(([key, val]: [string, any]) => formData.append(key, val))

      await axios
        .put(
          `portfolio/api/v1/portfolios/portfolios/${portfolio.id}/`,
          formData
        )
        .then((response) => {
          this.updatePortfolios(response.data)
          if (action === 'include') {
            toast.success(
              `${this.company.slug?.toUpperCase()} was added to ${portfolio.name}`
            )
          } else {
            toast.success(
              `${this.company.slug?.toUpperCase()} was remove from ${portfolio.name}`
            )
          }
        })
        .catch((error) => {
          console.log(error)
          toast.error('Something was wrong...')
        })
    },
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
      this.snowflake = data.statements
        .filter(
          (s) =>
            ['VALUE', 'FUTURE', 'PAST', 'HEALTH', 'DIVIDENDS'].includes(
              s.area
            ) && s.outcome === 1002
        )
        .reduce((acc, s) => {
          const key = s.area.toLowerCase() as SnowflakeKey

          if (!acc[key]) {
            acc[key] = []
          }

          acc[key].push(s)
          return acc
        }, {} as Snowflake)

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
          await axios.delete('/api/v1/invest/toggle_to_watchlist/', {
            data: formData,
          })
        } else {
          status = 'added'
          await axios.patch('/api/v1/invest/toggle_to_watchlist/', formData)
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
        await axios.delete(`/notes/api/v1/notes/${note.id}`)

        this.notes = this.notes.filter((n) => n.id !== note.id)
        toast.success('Note was successfully deleted')
      } catch (error) {
        console.log(error)
        toast.error('Something was wrong... Try again')
      }
    },
  },
})
