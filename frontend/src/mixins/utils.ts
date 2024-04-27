export default {
    methods: {
        humanize_financial_val(val: number, currency_symbol: string): string  {
            if (val === 0) return 'n/a'
            for (const unit of ["", "t", "M", "B", "T"]) {
              if (Math.abs(val) < 1000) return currency_symbol + val.toFixed(2) + unit
              val /= 1000
            }
            return '₽' + val.toFixed(2) + 'Q'
        }
    }
}