const company_slugEl = document.querySelector('#company_slug');

let company_slug = company_slugEl.innerText
company_slug = JSON.parse(company_slug)
company_slugEl.remove()

export const slug = company_slug
export const priceChartURL = `https://finargo.ru/invest/api/v1/price_chart/${company_slug}/`
