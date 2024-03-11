import { HMChartOpts } from "./chart_opts/_historical-metrics-chart-opts.js";

const chart = Highcharts.stockChart('historical-metrics-chart', HMChartOpts)
changeChartPeriod()

const HMChartContainer = document.querySelector('.historical-metrics-chart')

const HMChartBtns = HMChartContainer.querySelectorAll('.historical-metrics-chart__periodical-tab')

// Добавить прослушку на кнопки смены периода
HMChartBtns.forEach((el) => {el.addEventListener('click', changePeriod)})

function changePeriod(event) {
    const target = event.target
    const value = target.value
    // Сменить кнопку на выбранную
    togglePeriodBtn(target)
    changeChartPeriod(value)
}

function togglePeriodBtn(target) {
    // Удалить атрибут disabled со всех кнопок
    HMChartBtns.forEach((el) => {
        el.removeAttribute('disabled')
    })

    target.setAttribute('disabled', '')
}

function changeChartPeriod(value='3M') {
    const lastDataTs = chart.xAxis[0].dataMax
    const lastData = luxon.DateTime.fromMillis(lastDataTs)

    const diffFormat = {
        '3M': {months: 3},
        '1Y': {years: 1},
        '3Y': {years: 3},
        '5Y': {years: 5},
    }

    const min = lastData.minus(diffFormat[value]).toMillis()

    chart.xAxis[0].options.currentPeriod = value
    chart.xAxis[0].setExtremes(min, lastDataTs)
}

// TODO: Считать мультипликаторы раз в неделю (Создать столбец по трем мультипликатором)

const chartBox = document.querySelector('.historical-metrics-chart')

// CHANGING CHART ACTIONS
const DDLinks = chartBox.querySelectorAll('.chart__dropdown-link')
DDLinks.forEach((el) => {el.addEventListener('click', changeChart)})
const selectedLinkIcon = '' +
    '<span class="chart__dropdown-icon">\n' +
    '<svg height="24" width="24" viewBox="0 0 24 24" fill="#2394df">\n' +
    '<use href="#checked-icon"></use>\n' +
    '</svg>\n' +
    '</span>'

function changeChart(event) {
    const target = event.target
    if (target.classList.contains('chart__dropdown-link--selected')) return
    toggleLink(target)
    changeChartSeries(target)
    changeChartParams(target)
    // Перерисовать серии
    chart.renderSeries()
    chart.redraw()
}

function toggleLink(target) {
    const tabEl = target.closest('.chart__tab')
    const tabButtonText = tabEl.querySelector('.chart__tab-button-text')
    const selectedIcon = tabEl.querySelector('.chart__dropdown-icon')
    selectedIcon.remove()

    const key = Number(target.dataset.value)
    const data = [
        'Price to Earnings',
        'Price to Sales',
        'Price to Book'
    ]
    tabButtonText.innerHTML = data[key]

    DDLinks.forEach((el) => {el.classList.remove('chart__dropdown-link--selected')})
    target.classList.add('chart__dropdown-link--selected')
    target.insertAdjacentHTML('beforeend', selectedLinkIcon)
}

function changeChartSeries(target) {
    const key = Number(target.dataset.value)
    // Проверить что кнопка находится в диапазоне
    if (key<0 || key>3) return

    // Отключить видимость всех серий
    for (let i = 0; i<3; i++) {
        chart.series[i].visible = false
    }
    // Включить видимость выбранной серии
    chart.series[key].visible = true
}

function changeChartParams(target) {
    const key = Number(target.dataset.value)
    const data = {
        0: {yAxis: {max: 40, tickInterval: 40/4}},
        1: {yAxis: {max: 14, tickInterval: 14/4}},
        2: {yAxis: {max: 16, tickInterval: 16/4}},
    }
    const max = data[key].yAxis.max
    const tickInterval = data[key].yAxis.tickInterval

    chart.yAxis[0].update({
        max: max,
        tickInterval: tickInterval
    })
}

// TODO Объединить общие функции в отельный модуль либо создать класс