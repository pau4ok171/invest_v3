// Composables
import { useAuthStore } from '@/store/auth'

// Utilities
import { defineStore } from 'pinia'
import axios from 'axios'
import { toast } from 'vue3-toastify'
import { i18n } from '@/i18n/i18n'

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
    company_news: [] as News[],
    translations: {
      en: {
        title: '',
        short_title: '',
        short_title_genitive: '',
        description: '',
        short_description: '',
        city: '',
      },
    },
    country: {
      currency: {
        id: -1,
        translations: {
          en: {
            name: '',
          },
        },
        iso_code: '',
        symbol: '',
      },
      id: -1,
      markets: [],
      slug: '',
      translations: {
        en: {
          name: '',
          name_genitive: '',
        },
      },
    },
    formatting: {
      primaryCurrencyISO: '',
      primaryCurrencySymbol: '',
      reportCurrencyISO: '',
      reportCurrencySymbol: '',
      tradingCurrencyISO: '',
      tradingCurrencySymbol: '',
    },
    id: -1,
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
        translations: {
          en: {
            name: '',
          },
        },
        iso_code: '',
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

    price_data: {
      capitalisation: 0,
      last_price: 0,
    },
    reports: [] as Report[],
    performance: {
      return_1y: 0,
      return_30d: 0,
      return_3y: 0,
      return_5y: 0,
      return_7d: 0,
      return_90d: 0,
      next_earnings: 0,
      average_weekly_movement: 0,
      last_reported_earnings: 0,
    },
    sector: {
      id: -1,
      main_header: '',
      slug: '',
      translations: {
        en: {
          title: '',
          description: '',
        },
      },
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
    slug: '',
    ticker: '',
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
    lateralMenuComponentName: null as 'notes' | 'news' | null,
  }),
  getters: {
    chartPriceData(state) {
      return state.priceData.map((F) => [F['time'], F['close']])
    },
  },
  actions: {
    async createPortfolio(portfolioName: string) {
      const authStore = useAuthStore()
      try {
        const response = await axios.post('api/v1/portfolios/', {
          name: portfolioName,
        })

        await authStore.requestUserProfile()
        toast.success(
          i18n.global.t('toasts.portfolioCreated', { name: response.data.name })
        )
      } catch (error) {
        toast.error(i18n.global.t('toasts.somethingWrong'))
        throw error
      }
    },
    async updatePortfolio(portfolio: Portfolio) {
      const authStore = useAuthStore()
      const profile = authStore.profile

      if (!profile) return

      const company_id = this.company.id
      const action = portfolio.positions.includes(company_id) ? 'remove' : 'add'

      const positions =
        action === 'add'
          ? [...portfolio.positions, company_id]
          : portfolio.positions.filter((id) => id !== company_id)

      try {
        await axios.patch(`api/v1/portfolios/${portfolio.id}/`, { positions })

        await authStore.requestUserProfile()

        if (action === 'add') {
          toast.success(
            i18n.global.t('toasts.addedToPortfolio', {
              ticker: this.company.ticker,
              portfolioName: portfolio.name,
            })
          )
        } else {
          toast.success(
            i18n.global.t('toasts.removedFromPortfolio', {
              ticker: this.company.ticker,
              portfolioName: portfolio.name,
            })
          )
        }
      } catch (error) {
        console.log(error)
        toast.error(i18n.global.t('toasts.somethingWrong'))
      }
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
          `api/v1/invest/candles/${companySlug}`
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
    async deleteNote(note: Note) {
      try {
        await axios.delete(`/notes/api/v1/notes/${note.id}`)

        this.notes = this.notes.filter((n) => n.id !== note.id)
        toast.success(i18n.global.t('toasts.noteDeleted'))
      } catch (error) {
        console.log(error)
        toast.error(i18n.global.t('toasts.somethingWrong'))
      }
    },
  },
})
