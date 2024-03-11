import { FRRatioChartOpts } from "./chart_opts/fair-ratio-chart-opts.js";

const fairPE = 4.3
const currentPE = 5.6 // 2.6
const maxY = fairPE * 2


const chart = Highcharts.chart('fair-ratio-chart', FRRatioChartOpts)

class BaseLabel {
    // Base Opts
    paneOffsetX = (chart.chartWidth - chart.pane[0].center[2]) / 2
    plotBox = chart.plotBox
    elementColor = '#eeb219'
    textColor = '#1b222d'
    w = 2 // Vertical Line Width
    h = chart.pane[0].center[2] / 2 // 240 / 2=120
    x = (chart.chartWidth / 2)// 406/2=203
    y = chart.pane[0].center[1] + this.plotBox.x - this.h // 173.25 + 10

    // Polygon Opts
    polygonWidth = 11
    polygonHeight = 19
    polygonOffsetX = this.x + this.polygonWidth
    polygonOffsetY = this.y - this.polygonHeight
    polygonScaleX = -1

    // TextBox Opts
    textBoxHeight = 25
    textBoxWidth = 80
    textBoxOffsetX = this.x
    textBoxOffsetY = this.polygonOffsetY - this.textBoxHeight + 1

    // Text Opts
    textLabelName = 'Fair'
    textLabelValue = fairPE
    textFormat = `<tspan>${this.textLabelName} PE ${this.textLabelValue}x</tspan>`
    textWidth = 72.03
    textOffsetX = this.x + ((this.textBoxWidth - this.textWidth) / 2) // TextWidth = 72.3
    textOffsetY = this.polygonOffsetY - ((this.textBoxHeight - 15) / 2) - 3 // TextHeight = 15, MarginTextBottom = 3

    averageLabelGroup = chart.renderer.g().add()

    draw () {
        this.checkIfReversed()
        this.resetOpts()

        // Vertical average line
        chart.renderer.rect(this.x, this.y, this.w, this.h).attr({fill: this.elementColor, zIndex: 1}).add()

        // Polygon
        chart.renderer.path(["M", 0, 0, 11, 0, 11, 19, 9, 19, 0, 0, "Z"])
            .attr({fill: this.elementColor, translateX: this.polygonOffsetX, translateY: this.polygonOffsetY, scaleX: this.polygonScaleX})
            .add(this.averageLabelGroup)

        // TextBox
        chart.renderer.rect(this.textBoxOffsetX, this.textBoxOffsetY, this.textBoxWidth, this.textBoxHeight)
            .attr({
                fill: this.elementColor,
                rx: 2,
            })
            .add(this.averageLabelGroup)

        // Text
        chart.renderer.text(this.textFormat, this.textOffsetX, this.textOffsetY).attr({
                fill: this.textColor,
                'font-size': 13,
            }).add(this.averageLabelGroup)
    }

    checkIfReversed() {

    }

    resetOpts () {

    }

    setReversedOpts() {
        this.polygonOffsetX = this.x - this.polygonWidth + this.w
        this.polygonScaleX = 1
        this.textBoxOffsetX = this.x - this.textBoxWidth + this.w
        this.textOffsetX = this.textBoxOffsetX + ((this.textBoxWidth - this.textWidth) / 2)
    }
}

class FairLabel extends BaseLabel {
    checkIfReversed () {
        if (fairPE < currentPE) {this.setReversedOpts()}
    }
}

class CurrentLabel extends BaseLabel {

    elementColor = '#2394df'
    textColor = '#fff'

    textLabelName = 'Current'
    textLabelValue = currentPE
    textBoxWidth = 110
    textWidth = 92.99
    textFormat = `<tspan>${this.textLabelName} PE ${this.textLabelValue}x</tspan>`

    checkIfReversed () {
        if (currentPE <= fairPE) {
            this.setReversedOpts()
        }
    }

    resetOpts() {
        const degree = (180 - 180 / maxY * currentPE) * (Math.PI/180)
        const xPos = Math.cos(degree) * this.h + this.h
        this.x = this.paneOffsetX + xPos

        this.polygonOffsetX = this.x + this.polygonWidth
        this.textBoxOffsetX = this.x
        this.textOffsetX = this.x + ((this.textBoxWidth - this.textWidth) / 2)

        const boxH = chart.pane[0].center[2] / 2
        const diffX = (this.plotBox.width / 2) + this.plotBox.x - this.x
        this.h = boxH - Math.sqrt(Math.abs(Math.pow(boxH, 2) - Math.pow(diffX, 2)))
    }
}

const fair = new FairLabel()
const current = new CurrentLabel()
fair.draw()
current.draw()