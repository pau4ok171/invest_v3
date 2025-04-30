export type FinUnit = '' | 'K' | 'M' | 'B' | 'T'

export interface FinancialData {
  currency: string
  value: number
  finUnit: FinUnit
}

export function useFinancialFormatter() {
  /**
   * Конвертирует финансовые данные в удобочитаемый формат
   * Примеры:
   * { currency: 'US$', value: 16456, finUnit: 'M' } → "US$16.456B"
   * { currency: '€', value: -2500, finUnit: 'M' } → "-€2.5B"
   */
  const fin = (data: FinancialData): string => {
    const units = [
      { threshold: 1e12, suffix: 'T', divisor: 1e12 },
      { threshold: 1e9, suffix: 'B', divisor: 1e9 },
      { threshold: 1e6, suffix: 'M', divisor: 1e6 },
      { threshold: 1e3, suffix: 'K', divisor: 1e3 },
      { threshold: 0, suffix: '', divisor: 1 },
    ]

    // Обрабатываем отрицательные значения
    const isNegative = data.value < 0
    const absoluteValue = Math.abs(data.value)
    const baseValue = absoluteValue * getUnitMultiplier(data.finUnit)

    // Находим подходящую единицу (используем абсолютное значение)
    const unit =
      units.find((u) => baseValue >= u.threshold) || units[units.length - 1]
    const humanizedValue = baseValue / unit.divisor

    // Форматируем с учетом знака
    const formattedValue = formatHumanizedValue(humanizedValue)
    const signPrefix = isNegative ? '-' : ''

    return `${signPrefix}${data.currency}${formattedValue}${unit.suffix}`
  }

  const getUnitMultiplier = (unit: FinUnit): number => {
    switch (unit) {
      case 'K':
        return 1e3
      case 'M':
        return 1e6
      case 'B':
        return 1e9
      case 'T':
        return 1e12
      default:
        return 1
    }
  }

  const formatHumanizedValue = (value: number): string => {
    const absoluteValue = Math.abs(value)
    let formattedValue: string

    if (absoluteValue >= 1000) {
      formattedValue = value.toFixed(0)
    } else if (absoluteValue >= 100) {
      formattedValue = value.toFixed(1)
    } else if (absoluteValue >= 10) {
      formattedValue = value.toFixed(2)
    } else {
      formattedValue = value.toFixed(3)
    }

    return formattedValue.replace(/(\.\d*?[1-9])0+$/, '$1').replace(/\.$/, '')
  }

  return {
    fin,
    // Можно добавить дополнительные функции при необходимости
    formatCurrency: (value: number, currency: string) => {
      return fin({ currency, value, finUnit: '' })
    },
  }
}
