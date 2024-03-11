const data =  {
    currentValue: 133.3,
    fairValue: 329.48,
}

data['diff'] = +((data['fairValue'] - data['currentValue']) / data['fairValue'] * 100).toFixed(2)
data['highest'] = Math.max(data['currentValue'], data['fairValue'])

let diffType;
let diffClass;
let diffColor;

switch (true) {
    case data['diff'] >= 20:
        diffType = 'Undervalued'
        diffClass = 'dcf-chart__data-label-diff--undervalued'
        diffColor = '#2dc97e'
        break
    case data['diff'] <= -20:
        diffType = 'Overvalued'
        diffClass = 'dcf-chart__data-label-diff--overvalued'
        diffColor = '#e64141'
        break
    default:
        diffType = 'Overvalued'
        diffClass = 'dcf-chart__data-label-diff--about-right'
        diffColor = '#eeb219'
}

data['diffType'] = diffType
data['diffClass'] = diffClass
data['diffColor'] = diffColor

const dataLabelFormat = "" +
    "<tspan class='dcf-chart__data-label-name'>{series.name}</tspan>" +
    "<br>" +
    "<tspan class='dcf-chart__data-label-value'>{series.yData}RUB</tspan>"

const dataDiffLabelFormat = `` +
    `<tspan class=\"dcf-chart__data-label-diff-value\">${data['diff']}%</tspan>` +
    `<br>` +
    `<tspan class=\"dcf-chart__data-label-diff-type\">${data['diffType']}</tspan>`

Highcharts.chart('dcf-chart', {
    chart: {
        type: 'bar',
        height: 358,
        styledMode: true,
        borderWidth: 0,
        spacingTop: 69,
        spacingBottom: 80,
        className: 'dcf-chart__container',
        events: {
            load: drawMultipleBgC,
        }
    },
    title: {
        text: null,
    },
    xAxis: {
        visible: false,
    },
    yAxis: {
        visible: false,
        max: data['highest'] * 1.5 // Максимальное значение по ширине [ЗАВИСИТ ОТ МАКСИМАЛЬНОГО ЗНАЧЕНИЯ СТОИМОСТИ]
    },
    legend: {
        enabled: false
    },
    plotOptions: {
        bar: {
            groupPadding: .1,
            borderWidth: 0,
            borderRadius: 0,
            pointWidth: 72, // Высота бары
        }
    },
    credits: {
        enabled: false
    },
    series: [{
        name: 'Current Price',
        data: [data['currentValue']],
        enableMouseTracking: false,
        dataLabels: {
            align: 'right',
            enabled: true,
            format: dataLabelFormat,
        }
    }, {
        name: 'Fair Price',
        data: [data['fairValue']],
        enableMouseTracking: false,
        dataLabels: {
            align: 'right',
            enabled: true,
            format: dataLabelFormat
        }
    }]
});

function drawMultipleBgC() {
    // BACKGROUND
    const plotBox = this.plotBox
    const x1 = plotBox.x
    const y1 = plotBox.y
    const w = this.series[1].data[0].tooltipPos[2]
    const h = plotBox.height
    this.renderer.rect(x1, y1, w*1.2, h)
        .attr({
            fill: '#eeb219'
        })
        .add()

    this.renderer.rect(x1, y1, w*0.8, h)
        .attr({
            fill: '#2dc97e'
        })
        .add()

    // LINES
    const OUTLINE_OFFSET = 24
    const point2XOffset = this.series[0].pointXOffset
    const client2X = this.series[0].points[0].clientX

    const line1X = this.series[1].data[0].tooltipPos[2] + plotBox.x -1
    const line1Y = plotBox.y + 0.5 - OUTLINE_OFFSET
    const line1H = plotBox.height - 1 + OUTLINE_OFFSET

    const line2X = this.series[0].data[0].tooltipPos[2] + plotBox.x - 1
    const line2Y = plotBox.y + 0.5 - OUTLINE_OFFSET
    const line2H = plotBox.height - 1 + OUTLINE_OFFSET - client2X - point2XOffset

    const line3X = line2X < line1X ? line2X + 0.5 : line1X + 0.5
    const line3Y = plotBox.y + 0.5 - OUTLINE_OFFSET
    const line3W = Math.abs(line2X - line1X) - 0.5
    // FAIR PRICE LINE
    this.renderer.rect(line1X, line1Y, .5, line1H)
        .attr({
            fill: '#fff',
            opacity: .7,
            zIndex: 10,
        })
        .add()

    // CURRENT PRICE LINE
    this.renderer.rect(line2X, line2Y, .5, line2H)
        .attr({
            fill: '#fff',
            opacity: .7,
        })
        .add()

    // CONNECTING LINE
    this.renderer.rect(line3X, line3Y, line3W, 2)
        .attr({
            fill: data['diffColor'], // [ЗАВИСИТ ОТ ОТНОШЕНИЯ СПРАВЕДЛИВОЙ ОЦЕНКИ: ПЕРЕОЦЕНЕН, НЕДООЦЕНЕН]
        })
        .add()

    // CONNECTING LINE LABEL
    this.renderer.text(
        dataDiffLabelFormat,
        line3X,
        line3Y-22
    )
        .attr({
            class: data['diffClass']
        })
        .add()

    // TEXT
    const textY = plotBox.y + plotBox.height
    const textYOffset = 12
    const textXOffset = 12
    this.renderer.text(
        "<tspan class='dcf-chart__label-level-name'>20% Undervalued</tspan>",
        w * 0.8 + textXOffset,
        textY + textYOffset
    )
        .attr({
            rotation: -35,
            class: 'dcf-chart__data-label-diff--undervalued'
        })
        .add()

    this.renderer.text(
        "<tspan class='dcf-chart__label-level-name'>About Right</tspan>",
        w + textXOffset,
        textY + textYOffset
    )
        .attr({
            rotation: -35,
            class: 'dcf-chart__data-label-diff--about-right'
        })
        .add()

    this.renderer.text(
        "<tspan class='dcf-chart__label-level-name'>20% Overvalued</tspan>",
        w * 1.2 + textXOffset,
        textY + textYOffset
    )
        .attr({
            rotation: -35,
            class: 'dcf-chart__data-label-diff--overvalued'
        })
        .add()
}

