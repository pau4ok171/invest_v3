// Locals
import { en } from '@/i18n/locales/en'
import { ru } from '@/i18n/locales/ru'
import { fr } from '@/i18n/locales/fr'
import { de } from '@/i18n/locales/de'
import { es } from '@/i18n/locales/es'
import { pl } from '@/i18n/locales/pl'
import { it } from '@/i18n/locales/it'

export const messages = {
  en,
  ru,
  fr,
  de,
  es,
  pl,
  it,
}

export interface Locale {
  buttons: {
    addToWatchlist: string
    addToPortfolio: string
    addNote: string
    aboutTheCompany: string
    seeAllRisksChecks: string
    seeMore: string
    seeLess: string
    close: string
    max: string
    seeMoreUpdates: string
    seeFullShareholderReturns: string
    add: string
    added: string
    newPortfolio: string
    others: string
    shortMonth: string
    shortYear: string
    advancedFilters: string
    login: string
    registration: string
    forgotPassword: string
    create: string
    edit: string
    delete: string
    closeWithoutSaving: string
    save: string
    yes: string
    no: string
    search: string
    analysts: string
    resentEmail: string
    sendPasswordResetRequest: string
    resetPassword: string
    loginWithGoogle: string
    loginWithYandex: string
    loginWithGithub: string
    reset: string
    saveModifications: string
    deleteAvatar: string
    editProfile: string
  },
  toasts: {
    valueIsCopied: string
    noteSaved: string
    linkCopied: string
    portfolioCreated: string
    somethingWrong: string
    addedToPortfolio: string
    removedFromPortfolio: string
    watchlist: {
      added: string
      removed: string
    },
    noteDeleted: string
    emailConfirmed: string
    emailYetConfirmed: string
    sendPasswordResetRequest: string
    passwordResetSuccess: string
    emailConfirmationResent: string
    profileSaved: string
  },
  header: {
    searchPlaceholder: string
    searchEmpty: string
    dashboard: string
    portfolio: string
    articles: string
    markets: string
    watchlist: string
    screener: string
    translations: string
    adminPanel: string
    profile: string
    planAndPricing: string
    notifications: string
    helpCenter: string
    logout: string
    aboutUs: string
  },
  footer: {
    disclaimer: string
    rights: string
  },
  common: {
    updated: string
    created: string
    or: string
  },
  finance: {
    market: string
    industry: string
    company: string
    ratio: string
    eps: string
    grossMargin: string
    netProfitMargin: string
    debtEquityRatio: string
    currentDivYield: string
    payoutRatio: string
    pe: string
    pb: string
    ps: string
  },
  date: {
    shortDays: string
    shortMonths: string
    shortYears: string
    days: string
    months: string
    years: string
    max: string
  },
  pageTitles: {
    default: string
    companyDetail: string
    companyList: string
    admin: {
      main: string
      dashboard: string
      models: string
      staff: string
      settings: string
    },
    home: string
    page404: string
  },
  loader: {
    defaultText: string
    defaultProgress: string
  },
  companyList: {
    header: {
      companies: string
      marketDescription: {
        global: string
        country: string
      },
      marketTitle: string
      global: string
      any: string
    },
    dataTable: {
      headers: {
        company: string
        lastPrice: string
        return7d: string
        return1y: string
        marketCap: string
        analystsTarget: string
        valuation: string
        growth: string
        dividendYield: string
        industry: string
      },
    },
    dataTile: {
      return7d: string
      return1y: string
      growth: string
      analystsTarget: string
    },
  },
  labels: {
    username: string
    password: string
    passwordConfirmation: string
    email: string
    displayName: string
    avatar: string
    bannerColor: string
    aboutMe: string
    language: string
    country: string
    currency: string
    loginMethod: string
    registrationDate: string
    firstName: string
    familyName: string
  },
  auth: {
    dontHaveAccount: string
    haveYetAccount: string
    disclaimer: {
      prefix: string
      terms: string
      suffix: string
    },
    emailConfirmation: {
      thankYou: string
      confirmationSent: string
      verificationWarning: string
      spamNotice: string
      resentPrompt: string
    },
    passwordReset: {
      emailAsking: string
      resetInstruction: string
    },
  },
  profile: {
    profile: string
    communityProfile: string
    preview: string
    preferences: string
    accountDetails: string
    saveText: string
    preventText: string
  },
  validations: {
    required: string
    minLengthValue: string
    passwordMismatch: string
    usernameYetTaken: string
    emailField: string
  },
  admin: {
    dashboard: string
    models: string
    staff: string
    settings: string
  },
  snowflake: {
    analysisChecks: string
    tooltip: {
      valuation: string
      future: string
      past: string
      health: string
      dividends: string
    },
  },
  highcharts: {
    dataNotAvailable: string
  },
  companyDetail: {
    header: {
      stockReport: string
      lastPrice: string
      marketCap: string
      shortMarketCap: string
      return7d: string
      return1y: string
      data: string
      companyFinancials: string
    },
    sections: {
      overview: string
      valuation: string
      future: string
      past: string
      health: string
      dividend: string
      management: string
      ownership: string
      other: string
      overviewShort: string
      valuationShort: string
      futureShort: string
      pastShort: string
      healthShort: string
      dividendShort: string
      managementShort: string
      ownershipShort: string
      otherShort: string
    },
    portfolio: {
      title: string
      placeholder: string
      holdings: string
    },
    analysts: {
      title: string
      subtitle: string
      table: {
        institution: string
        target: string
        score: string
      },
    },
    overview: {
      stockOverview: {
        header: string
        rewards: string
        risks: string
        riskChecks: string
        riskChecksDesc: string
        pass: string
        fail: string
      },
      notes: {
        header: string
        placeholder: string
        saved: string
        saving: string
      },
      competitors: {
        header: string
      },
      historyPerformance: {
        header: string
      },
      updates: {
        header: string
        emptyNews: string
      },
      shareholderReturns: {
        header: string
      },
      priceVolatility: {
        header: string
        low: string
        high: string
        marketLabel: string
        marketTooltip: string
        companyTooltip: string
        industryTooltip: string
      },
      aboutCompany: {
        header: string
        founded: string
        employees: string
        ceo: string
        website: string
      },
      fundamentalSummary: {
        header: string
        ratio: string
        inducement: {
          question: string
          response: string
        },
      },
      earningsAndRevenue: {
        header: string
        lastReportedEarnings: string
        nextEarnings: string
        inducement: {
          question: string
          response: string
        },
      },
      dividends: {
        header: string
        inducement: {
          question: string
          response: string
        }
      },
    },
    valuation: {
      title: string
      subtitle: string
      score: string
      shareFairValue: {
        title: string
        subtitle: string
        currentPrice: string
        fairPrice: string
        undervalued: string
        aboutRight: string
        overvalued: string
      },
      keyValuationMetric: {
        title: string
        subtitle: string
        keyMetric: string
        keyStatistics: string
        peMetric: string
        pbMetric: string
        psMetric: string
        otherMetric: string
        evToRevenue: string
        evToEBITDA: string
        pegRatio: string
        caption: string
      },
      peVsPeers: {
        title: string
        subtitle: string
        peerAvg: string
        earningsGrowth: string
        salesGrowth: string
      },
      historicalPE: {
        title: string
        subtitle: string
      },
      peVsIndustry: {
        title: string
        subtitle: string
        nombreOfCompanies: string
      },
      peVsFair: {
        title: string
        subtitle: string
      },
      analystsPriceTargets: {
        title: string
        subtitle: string
        past: string
        forecast: string
        tooltip: {
          sharePrice: string
          avgTarget: string
          agreement: {
            title: string
            status: {
              good: string
              low: string
            },
            desc: {
              good: string
              low: string
            },
          },
          analysts: string
        },
        legend: {
          sharePrice: string
          avgTarget: string
        },
      },
    },
    future: {
      title: string
      subtitle: string
      score: string
      earningsAndRevenueGrowth: {
        title: string
        chart: {
          tooltip: {
            analysts: string
            lastUpdated: string
            year: string
            revenue: string
            earnings: string
            fcf: string
            cfo: string
          },
          legends: {
            revenue: string
            earnings: string
            fcf: string
            cfo: string
          },
          past: string
          analystsForecasts: string
        },
      },
      analystFutureGrowth: {
        title: string
        earningsGrowthTitle: string
        revenueGrowthTitle: string
      },
      epsGrowth: {
        title: string
        chart: {
          tooltip: {
            eps: string
            analystsEps: string
            analystsNombre: string
            lastUpdated: string
          },
          legends: {
            eps: string
            analystsEpsRange: string
          },
          actual: string
          analystsForecasts: string
        },
      },
      futureROE: {
        title: string
        chart: {
          title: string
        },
      },
    },
    past: {
      title: string
      subtitle: string
      score: string
      revenueExpensesBreakdown: {
        title: string
        subtitle: string
      },
      earningsRevenueHistory: {
        title: string
        chart: {
          actual: string
          tooltip: {
            revenue: string
            earnings: string
            year: string
            profitMargin: string
            fcf: string
            cfo: string
            opex: string
          },
          legends: {
            revenue: string
            earnings: string
            fcf: string
            cfo: string
            opex: string
          },
        },
      },
      fcfVsEarnings: {
        title: string
      },
      pastEarningsGrowth: {
        title: string
        y5GrowthChart: {
          title: string
        },
        y1GrowthChart: {
          title: string
        },
      },
      roe: {
        title: string
      },
      roa: {
        title: string
      },
      roce: {
        title: string
        lastYear: string
        years3Ago: string
      },
    },
    health: {
      title: string
      subtitle: string
      score: string
      financialPosition: {
        title: string
        shortTerm: string
        longTerm: string
        assets: string
        liabilities: string
      },
      deHistory: {
        title: string
        chart: {
          tooltip: {
            debt: string
            equity: string
            deRatio: string
            cashAndEq: string
          },
          legends: {
            debt: string
            equity: string
            cashAndEq: string
          },
        },
      },
      balanceSheet: {
        title: string
        assets: string
        liabilities: string
        equity: string
      },
    },
    dividend: {
      title: string
      subtitle: string
      score: string
      upcomingPayment: {
        title: string
        chart: {
          today: string
          exDividendDate: string
          dividendPayDate: string
          tooltip: string
        },
      },
      stabilityAndGrowth: {
        title: string
        past: string
        analystsForecasts: string
        tooltip: {
          dividendPayments: string
          annualAmount: string
          eps: string
          dividendYield: string
          quarterly: string
          year: string
        },
        legends: {
          dividendYield: string
          dividendPayments: string
          annualAmount: string
          eps: string
        },
      },
      yieldVsMarket: {
        title: string
        chart: {
          title: string
          marketBottom: string
          marketTop: string
          industryAverage: string
          forecast: string
        },
      },
      earningsPayout: {
        title: string
        chart: {
          current: string
          paidAsDividend: string
          earningsRetained: string
        },
      },
      cashPayout: {
        title: string
        chart: {
          paidAsDividend: string
          earningsRetained: string
        },
      },
    },
  },
}
