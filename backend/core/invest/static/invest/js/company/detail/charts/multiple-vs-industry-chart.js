import { MVIChartOpts } from "./chart_opts/_multiple-vs-industry-chart-opts.js";

const averagesMI = {
    0: {
        labelTextX: 'PE',
        industryValue: 7.4,
        companyValue: 2.6,
        maxY: 48,
        intervalX: 1.5,
    },
    1: {
        labelTextX: 'PS',
        industryValue: 2.1,
        companyValue: 1.2,
        maxY: 34,
        intervalX: 0.3,
    },
    2: {
        labelTextX: 'PB',
        industryValue: 0.7,
        companyValue: 0.5,
        maxY: 33,
        intervalX: 0.2,
    },
}

// Draw Chart
class BaseLabel {
    plotBox = chart.plotBox
    pointWidth = chart.options.plotOptions.series.pointWidth
    plotStartX = this.plotBox.x
    plotStartY = this.plotBox.y
    plotBoxHeight= this.plotBox.height
    averageLineWidth = 2
    polygonHeight = 19
    polygonWidth = 11
    labelHeight = 25
    averageValue = null
    averageFullPosX = null
    isReversed = null

    textLabelName = null
    textColor = null
    elementColor = null

    averagePosX= null
    labelWidth = null
    key = null
    middleBG = null

    polygonOffsetX = this.polygonWidth
    polygonScaleX = -1
    textBoxOffsetX = 0
    textBoxOffsetY = -17
    textOffsetX = 9
    axisOffsetX = 36

    redraw(key, isReversed) {
        this._destroy()
        this.draw(key, isReversed)
    }

    draw () {

    }

    _destroy() {
        if (this.middleBG) {this.middleBG.destroy()}
        this.averageLabelGroup.destroy()
    }

    _drawAverageLabel() {
        this.averageLabelGroup = chart.renderer.g().attr({overflow: 'visible'}).add()
        this._drawAverageMiddleLine()
        this._drawAverageLabelBox()
    }

    _drawAverageMiddleLine() {
        chart.renderer.rect(
            this.averageFullPosX,
            0,
            this.averageLineWidth,
            this.plotBoxHeight
        ).attr({translateX: this.plotStartX, translateY: this.plotStartY, fill: this.elementColor}).add(this.averageLabelGroup)
    }

    _drawAverageLabelBox() {
        const averageGroup = chart.renderer.g().attr({translateX: this.plotStartX, translateY: -this.polygonHeight}).add(this.averageLabelGroup)

        const averagePolygonGroup = chart.renderer.g().attr({translateX: this.averageFullPosX,translateY: this.plotStartY}).add(averageGroup)
        const averageTextLabelGroup = chart.renderer.g().attr({translateX: this.averageFullPosX,translateY: this.plotStartY}).add(averageGroup)

        if (!this.isReversed) {
            this.polygonOffsetX = -this.polygonWidth + this.averageLineWidth
            this.polygonScaleX = 1
            this.textBoxOffsetX = -this.labelWidth + this.averageLineWidth
            this.textOffsetX = 9 - this.labelWidth

        }

        // Polygon
        chart.renderer.path(["M", 0, 0, 11, 0, 11, 19, 9, 19, 0, 0, "Z"])
            .attr({fill: this.elementColor, translateX: this.polygonOffsetX, scaleX: this.polygonScaleX}).add(averagePolygonGroup)

        // TextBox
        chart.renderer.rect(0, 0, this.labelWidth, this.labelHeight)
            .attr({
                fill: this.elementColor,
                rx: 2,
                translateX: this.textBoxOffsetX,
                translateY: this.textBoxOffsetY,
            })
            .add(averageTextLabelGroup)

        // Text
        const textFormat = `<tspan>${this.textLabelName} ${this.averageValue}x</tspan>`
        chart.renderer.text(textFormat).attr({
            fill: this.textColor,
            'font-size': 13,
            translateX: this.textOffsetX,

        }).add(averageTextLabelGroup)
    }

}

class AvgLabel extends BaseLabel {
    labelWidth = 120
    averageValue = null
    averagePosX = null
    averageLabelGroup = null
    middleBG = null
    key = null
    isReversed = null

    textLabelName = 'Industry Avg'
    elementColor = '#eeb219'
    textColor = '#1b222d'

    draw(key=0, isReversed=false) {
        this.key=key
        this.isReversed=isReversed
        this._setOptions()
        this._drawBackground()
        this._drawAverageLabel()
    }

    _setOptions () {
        this.averageValue = averagesMI[this.key].industryValue
        this.intervalX = averagesMI[this.key].intervalX
        this.averagePosX = this.pointWidth * this.averageValue / this.intervalX
        this.averageFullPosX = this.averagePosX + this.axisOffsetX
    }

    // Draw Background after Vertical Middle Line
    _drawBackground () {
        this.middleBG = chart.renderer.rect(
            this.plotStartX,
            this.plotStartY,
            this.averageFullPosX,
            this.plotBoxHeight
        ).attr({fill:'#2dc97e'}).add()
    }
}

class CompanyLabel extends BaseLabel {
    labelWidth = 80
    averageValue = null
    averagePosX = null
    averageLabelGroup = null
    key = null

    isReversed = null

    textLabelName = 'SBER'
    textColor = '#fff'
    elementColor = '#2394df'

    draw(key=0, isReversed=false) {
        this.key=key
        this.isReversed = isReversed
        this._setOptions()
        this._drawAverageLabel()
    }

    _setOptions () {
        this.averageValue = averagesMI[this.key].companyValue
        this.intervalX = averagesMI[this.key].intervalX
        this.averagePosX = this.pointWidth * this.averageValue / this.intervalX
        this.averageFullPosX = this.averagePosX + this.axisOffsetX
    }
}

const chart = Highcharts.chart('multiple-vs-industry-chart', MVIChartOpts)
const avg = new AvgLabel()
const company = new CompanyLabel()

let industryIsReversed = true
let companyIsReversed = false

if (averagesMI[0].industryValue < averagesMI[0].companyValue) {
    industryIsReversed = false
    companyIsReversed = true
}

avg.draw(0, industryIsReversed)
company.draw(0, companyIsReversed)

// Redraw Chart
const chartBox = document.querySelector('.multiple-vs-industry-chart')

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
    changeChartSeriesMI(target)
    changeChartParams(target)
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

function changeChartSeriesMI(target) {
    const key = Number(target.dataset.value)
    // Проверить что кнопка находится в диапазоне
    if (key<0 || key>3) return
    // Отключить видимость всех серий
    for (let i = 0; i<3; i++) {
        chart.series[i].visible = false
    }
    // Включить видимость выбранной серии
    chart.series[key].visible = true

    // Перерисовать серии
    chart.renderSeries()
}

function changeChartParams(target) {
    const key = Number(target.dataset.value)

    const currentSeries = averagesMI[key]
    const labelTextX = currentSeries.labelTextX
    const yAxisMax = currentSeries.maxY
    const xAxisTickInterval = currentSeries.intervalX

    const labelY = chartBox.querySelector('.highcharts-xaxis .highcharts-axis-title')
    labelY.textContent = labelTextX

    chart.xAxis[0].update({
        tickInterval: xAxisTickInterval,
    }, false)
    chart.yAxis[0].update({
        max: yAxisMax,
        tickInterval: yAxisMax/4
    }, false)

    redrawMiddleEls(key)

    chart.redraw()
}

function redrawMiddleEls(key) {
    industryIsReversed = true
    companyIsReversed = false

    if (averagesMI[key].industryValue < averagesMI[key].companyValue) {
        industryIsReversed = false
        companyIsReversed = true
    }
    avg.redraw(key, industryIsReversed)
    company.redraw(key, companyIsReversed)
}
