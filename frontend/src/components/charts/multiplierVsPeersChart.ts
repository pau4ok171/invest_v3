const dataMP = {
  0: {
    name: 'ROSBANK',
    pe: 9.8,
    pb: 0.9,
    ps: 3,
    earningsGrowth: 'n/a',
    salesGrowth: 'n/a',
  },
  1: {
    name: 'Credit Bank of Moscow',
    pe: 6.3,
    pb: 0.6,
    ps: 2.6,
    earningsGrowth: '26.9%',
    salesGrowth: '28.3%',
  },
  2: {
    name: 'Sberbank of Russia',
    pe: 9.8,
    pb: 0.5,
    ps: 1.2,
    earningsGrowth: '8.2%',
    salesGrowth: '12.5%',
  },
  3: {
    name: 'Gazprom',
    pe: 2.2,
    pb: 0.3,
    ps: 0.5,
    earningsGrowth: 'n/a',
    salesGrowth: 'n/a',
  },
  4: {
    name: 'VTB Bank',
    pe: 9.8,
    pb: 0.1,
    ps: 0.3,
    earningsGrowth: '-2.1%',
    salesGrowth: '10.2%',
  },
}

const averagesMP = {
  0: {
    averageValue: 4.8,
    maxValue: 9.8,
    max: 10,
  },
  2: {
    averageValue: 0.5,
    maxValue: 0.9,
    max: 1.2,
  },
  1: {
    averageValue: 1.6,
    maxValue: 3,
    max: 3.2
  },
}

let chartMiddleEls = {}
let chartXAxisEls = {}

function setDataSeriesTextFormat() {
  const key = this.key
  const selected = key === 2 ? ' multiple-vs-peers-chart__data-label-name--selected' : ''
  return `` +
  `<text class='multiple-vs-peers-chart__data-label-value'>${this.y}x</text>` +
  `<br>` +
  `<text class='multiple-vs-peers-chart__data-label-name${selected}'>${dataMP[key].name}</text>`
}

export const chartOpts = {
  chart: {
    type: 'bar',
    height: 362,
    style: {
        fontFamily: 'inherit',
    },
    events: {
        load: drawAdditionalElements
    },
    backgroundColor: '#1b222d',
    spacingTop: 45,
    spacingRight: 45,
    plotBackgroundColor: 'url(#Chart_Fail_Pattern)',
    plotBorderWidth: 0,
  },
  plotOptions: {
    bar: {
      enableMouseTracking: false,
      groupPadding: .1,
      borderWidth: 0,
      borderRadius: 0,
      pointWidth: 50, // Высота бары
    }
  },
  series: [
    {
      name: 'PE',
      visible: true,
      color: 'url(#BarGradient)',
      dataLabels: {
        useHTML: true,
        enabled: true,
        inside: true,
        align: 'left',
        x: 10,
        formatter: setDataSeriesTextFormat,
      },
        data: [{y: 9.8,}, {y: 6.3,}, {y: 2.6, color: '#1b222d'}, {y: 2.2,}, {y: 0.8,}]
      }, {
        name: 'PS',
        visible: false,
        color: 'url(#BarGradient)',
        dataLabels: {
          useHTML: true,
          enabled: true,
          inside: true,
          align: 'left',
          x: 10,
          formatter: setDataSeriesTextFormat,
        },
        data: [{y: 3,}, {y: 2.6,}, {y: 1.2, color: '#1b222d'}, {y: 0.5,}, {y: 0.3,}]
      }, {
        name: 'PB',
        visible: false,
        color: 'url(#BarGradient)',
        dataLabels: {
          useHTML: true,
          enabled: true,
          inside: true,
          align: 'left',
          x: 10,
          formatter: setDataSeriesTextFormat,
          },
          data: [{
            y: 0.9,
          }, {
            y: 0.6,
          }, {
            y: 0.5,
            color: '#1b222d'
          }, {
            y: 0.3,
          }, {
            y: 0.1,
          }]
      }
    ],
    // Горизонтальная ось
    yAxis: {
      firstEl: 'PE',
      gridLineWidth: 0,
      lineWidth: 1,
      lineColor: 'rgba(255, 255, 255, .2)',
      tickInterval: 2.5, // Расстояние между чертами
      tickColor: 'rgba(255, 255, 255, .2)',
      tickWidth: 1,
      title: {
        enabled: false
      },
      labels: {
        style: {
          fontSize: '1.2rem',
          color: '#fff',
        },
        formatter: function () {return this.isFirst ? this.chart.yAxis[0].options.firstEl : this.value}},
      max: 10, // Макс значение по оси
    },
    xAxis: {
      currentSeries: 0,
      opposite: true,
      lineWidth: 0,
      tickWidth: 0,
      labels: {
        style: {
          fontSize: '1.2rem',
          color: '#fff',
        },
        formatter: function () {
          const index = Number(this.value)
          if (this.chart.xAxis[0].options.currentSeries === 1) return dataMP[index].salesGrowth
          return dataMP[index].earningsGrowth
        },
      }
    },
    title: {
      text: ''
    },
    credits: {
      enabled: false
    },
    legend: {
      enabled: false
    }
}

function drawAdditionalElements() {
  const chart = this
  drawVAxisEls(chart)
  drawMiddleEls(chart)
}

function drawVAxisEls(chart) {
  const offsetX = 8
  const boxW = 60
  const plotBox = chart.plotBox

  const boxX = plotBox.x + plotBox.width + offsetX // Dynamic
  const boxY = plotBox.y // Dynamic
  const boxH = plotBox.height // Dynamic

  chart.renderer.rect(boxX, boxY, boxW, boxH)
    .attr({
      fill: '#262e3a',
      'rx': 4, // BorderRadius
    })
    .add()

    drawXAxisLabel(chart)

}

function drawXAxisLabel (chart, key=0) {
  const plotBox = chart.plotBox
  const textOffsetX = 8
  const textOffsetY = 18
  const textX = plotBox.x + plotBox.width + textOffsetX
  const textY = plotBox.y - textOffsetY
  const textValueType = key === 1 ? 'Sales' : 'Earnings'
  const textFormat = `` +
    `<tspan class='multiple-vs-peers-chart__v-axis-name'>${textValueType}</tspan>` +
    `<br>` +
    `<tspan class=\'multiple-vs-peers-chart__v-axis-name\'>Growth</tspan>`

  chartXAxisEls.xAxisLabel = chart.renderer.text(textFormat, textX, textY).add()
}

function drawMiddleEls(chart, key=0) {
  const plotBox = chart.plotBox
  const averageValue = averagesMP[key].averageValue
  const yMax = averagesMP[key].max
  const pointWidth = plotBox.width / yMax
  const averagePosX = pointWidth * averageValue

  const bgX = plotBox.x// Dynamic
  const bgY = plotBox.y // Dynamic
  const bgH = plotBox.height // Dynamic
  const bgW = averagePosX

  // Background after Vertical Middle Line
  const middleBG = chart.renderer.rect(bgX, bgY, bgW, bgH)
    .attr({
        fill: '#2dc97e',
    })
    .add()

  const lineX = plotBox.x + averagePosX // Dynamic
  const lineY = plotBox.y // Dynamic
  const lineH = plotBox.height // Dynamic
  const lineW = 2

  // Vertical Middle Line
  const middleLine = chart.renderer.rect(lineX, lineY, lineW, lineH)
    .attr({
        fill: '#eeb219',
    })
    .add()
  const polygonH = 19
  const labelPosX = averagePosX+1
  const labelPosY = plotBox.y - polygonH

  const middlePolygon = chart.renderer.path(["M", 0, 0, 11, 0, 11, 19, 9, 19, 0, 0, "Z"])
    .attr({
        transform: `translate(${labelPosX}, ${labelPosY})`,
        fill: '#eeb219',
    })
    .add()

  const labelW = 100
  const labelH = 25
  const labelX = averagePosX + 1 - labelW + 11
  const labelY = plotBox.y - labelH - polygonH + 1


  const middleLabel = chart.renderer.rect(labelX, labelY, labelW, labelH)
    .attr({
        fill: '#eeb219',
        rx: 2,
    })
    .add()

  const textBoxX = 30
  const textBoxY = 5
  const textX = averagePosX - (labelW / 2) - textBoxX
  const textY = plotBox.y - polygonH - (labelH / 2) + textBoxY
  const textFormat = `<tspan class=\'multiple-vs-peers-chart__middle-label-name\'>Peer Avg ${averageValue}x</tspan>`

  const middleText = chart.renderer.text(textFormat, textX, textY)
    .attr({

    })
    .add()

  chartMiddleEls.middleBG = middleBG
  chartMiddleEls.middleLine = middleLine
  chartMiddleEls.middlePolygon = middlePolygon
  chartMiddleEls.middleLabel = middleLabel
  chartMiddleEls.middleText = middleText
}







