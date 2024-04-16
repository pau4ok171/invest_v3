const data = {
  sales: {
    name: 'Sales',
    value: 2430,
    unit: 'Млрд',
    currency_iso: '₽',
    mult: 1.2,
    isKeyMetric: true,
    keyMetricDesc: 'As SBER is a bank we don’t use its Price-To-Sales Ratio as the key metric for relative valuation analysis',
  },
  book: {
    name: 'Book',
    value: 5640,
    unit: 'Млрд',
    currency_iso: '₽',
    mult: 0.5,
  },
  earnings: {
    name: 'Earnings',
    value: 1160,
    unit: 'Млрд',
    currency_iso: '₽',
    mult: 2.6,
  },
  marketCap: {
    name: 'Market Cap',
    value: 2990,
    unit: 'Млрд',
    currency_iso: '₽'
  }
}

export const chartOpts = {
  chart: {
    type: 'solidgauge',
    height: 280,
    backgroundColor: '#1b222d',
    spacingTop: 80,
    events: {
      load: drawLines
    }
  },
  pane: {
    size: 184,
    background: {
      backgroundColor: '#1b222d',
      borderWidth: 0,
    }
  },
  plotOptions: {
    solidgauge: {
      enableMouseTracking: false,
      stickyTracking: false,
      dataLabels: {
        enabled: true
      }
    }

  },
  series: [{
    name: 'Market Cap',
    data: [{
      name: 'Market Cap',
      y: 2990,
      color: 'rgb(62, 72, 85)',
      radius: '65%',
      innerRadius: '100%',
      label: `${data.marketCap.value} ${data.marketCap.unit} ${data.marketCap.currency_iso}`,
      dataLabels: {
        align: 'center',
        verticalAlign: 'middle',
        position: 'center',
        borderWidth: 0,
        format: '<tspan class="fundamental-summary-chart__middle-label">{point.name}</tspan><br><tspan class="fundamental-summary-chart__middle-value">{point.label}</tspan>',
        style: {
          fontSize: '12px',
          textAnchor: 'middle',
        },
        x: 36,
      },
    }]
  }, {
    name: 'Earnings',
    visible: true,
    data: [{
      name: 'Earnings',
      y: 1160,
      color: 'rgb(35, 148, 223)',
      radius: '65%',
      innerRadius: '100%',
      label: `${data.earnings.value} ${data.earnings.unit} ${data.earnings.currency_iso}`,
      dataLabels: {
        allowOverlap: true,
        // crop: true,
        overflow: 'allow',
        align: 'center',
        verticalAlign: 'middle',
        position: 'center',
        borderWidth: 0,
        format: '<tspan class="fundamental-summary-chart__middle-label">{point.name}</tspan><br><tspan class="fundamental-summary-chart__middle-value">{point.label}</tspan>',
        style: {
          fontSize: '12px',
          textAnchor: 'middle',
        },
        x: 0, // 153.5
        y: -184 / 2 - 64
      },
    }]
  }, {
    name: 'Book',
    visible: false,
    data: [{
      name: 'Book',
      y: 5640,
      color: 'rgb(35, 148, 223)',
      radius: '65%',
      innerRadius: '100%',
      label: `${data.book.value} ${data.book.unit} ${data.book.currency_iso}`,
      dataLabels: {
        allowOverlap: true,
        // crop: true,
        overflow: 'allow',
        align: 'center',
        verticalAlign: 'middle',
        position: 'center',
        borderWidth: 0,
        format: '<tspan class="fundamental-summary-chart__middle-label">{point.name}</tspan><br><tspan class="fundamental-summary-chart__middle-value">{point.label}</tspan>',
        style: {
          fontSize: '12px',
          textAnchor: 'middle',
        },
        x: 0, // 153.5
        y: -184 / 2 - 64
      },
    }]
  }, {
    name: 'Sales',
    visible: false,
    data: [{
      name: 'Sales',
      y: 2430,
      color: 'rgb(35, 148, 223)',
      radius: '65%',
      innerRadius: '100%',
      label: `${data.sales.value} ${data.sales.unit} ${data.sales.currency_iso}`,
      dataLabels: {
        allowOverlap: true,
        // crop: true,
        overflow: 'allow',
        align: 'center',
        verticalAlign: 'middle',
        position: 'center',
        borderWidth: 0,
        format: '<tspan class="fundamental-summary-chart__middle-label">{point.name}</tspan><br><tspan class="fundamental-summary-chart__middle-value">{point.label}</tspan>',
        style: {
          fontSize: '12px',
          textAnchor: 'middle',
        },
        x: 0, // 153.5
        y: -184 / 2 - 64
      },
    }]
  }],
  yAxis: {
    min: 0,
    max: 2990,
    lineWidth: 0,
    tickPositions: []
  },
  title: {
    text: null
  },
  credits: {
    enabled: false
  },
}

function drawLines() {
  const plotOffsetX = this.plotBox.x
  const plotOffsetY = this.plotBox.y
  const lineH = 64
  const lineX = plotOffsetX + this.series[0].data[0].graphic.pathArray[0][1]
  const lineY = plotOffsetY + this.series[0].data[0].graphic.pathArray[0][2] - lineH
  const lineW = .5

  this.renderer.rect(lineX, lineY, lineW, lineH)
    .attr({
      fill: '#2394df',
      zIndex: 10,
    })
    .add()

  this.renderer.circle()
    .attr({
      cx: lineX,
      cy: lineY,
      fill: '#2394df',
      r: 2.5,
      zIndex: 10,
    })
    .add()
}