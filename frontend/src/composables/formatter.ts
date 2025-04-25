export type FinUnit = '' | 'K' | 'M' | 'B' | 'T'

export interface FinancialData {
  currency: string
  value: number
  finUnit: FinUnit
}

export function useFinancialFormatter() {
  /**
   * Конвертирует финансовые данные в удобочитаемый формат
   * Пример: { currency: 'US$', value: 16456, finUnit: 'm' } → "US$16.456B"
   */
  const fin = (data: FinancialData): string => {
    const units = [
      { threshold: 1e12, suffix: 'T', divisor: 1e12 }, // триллионы
      { threshold: 1e9, suffix: 'B', divisor: 1e9 },    // миллиарды
      { threshold: 1e6, suffix: 'M', divisor: 1e6 },     // миллионы
      { threshold: 1e3, suffix: 'K', divisor: 1e3 },     // тысячи
      { threshold: 1, suffix: '', divisor: 1 }           // единицы
    ]

    // Конвертируем в базовые единицы (без множителя)
    const baseValue = data.value * getUnitMultiplier(data.finUnit)

    // Находим подходящую единицу измерения
    const unit = units.find(u => baseValue >= u.threshold) || units[units.length - 1]

    // Вычисляем "гуманизированное" значение
    const humanizedValue = baseValue / unit.divisor

    // Форматируем число
    const formattedValue = formatHumanizedValue(humanizedValue)

    return `${data.currency}${formattedValue}${unit.suffix}`
  }

  /** Вспомогательная функция: множитель для единиц измерения */
  const getUnitMultiplier = (unit: FinUnit): number => {
    switch (unit) {
      case 'K': return 1e3    // thousand → ×1000
      case 'M': return 1e6    // million → ×1,000,000
      case 'B': return 1e9    // billion → ×1,000,000,000
      case 'T': return 1e12   // trillion → ×1,000,000,000,000
      default: return 1       // единицы
    }
  }

  /** Форматирует число с интеллектуальным округлением */
  const formatHumanizedValue = (value: number): string => {
    let formattedValue: string

    if (value >= 1000) {
      formattedValue = value.toFixed(0)
    } else if (value >= 100) {
      formattedValue = value.toFixed(1)
    } else if (value >= 10) {
      formattedValue = value.toFixed(2)
    } else {
      formattedValue = value.toFixed(3)
    }

    // Удаляем лишние нули после запятой (если они есть)
    return formattedValue.replace(/(\.\d*?[1-9])0+$/, '$1').replace(/\.$/, '')
  }

  return {
    fin,
  }
}