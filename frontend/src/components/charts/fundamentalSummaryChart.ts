const eData = {
  market_cap: {
    value: 1000,
    unit: 'Млрд',
    currency_iso: '₽',
    ratio: 100
  },
  revenue: {
    value: 800,
    unit: 'Млрд',
    currency_iso: '₽',
    ratio: 80
  },
  earnings: {
    value: 200,
    unit: 'Млрд',
    currency_iso: '₽',
    ratio: 20
  },
}

export const chartOpts = {
  chart: {
    backgroundColor: '#1b222d',
    type: 'solidgauge',
    height: '80%',
    spacingTop: 80,
    events: {
      load: drawDataLabel
    }
  },
  accessibility: {
    enabled: false
  },
  title: {
   text: ''
  },
  credits: {
   enabled: false,
  },
  yAxis: {
    min: 0,
    max: 100,
    lineWidth: 0,
    tickPositions: []
  },
  pane: {
   background: {
     backgroundColor: '#1b222d',
     borderWidth: 0,
   }
  },
  plotOptions: {
    solidgauge: {
      stickyTracking: false, // stickyTracking
    }
  },
  series: [
    {
      name: 'Market Cap',
      enableMouseTracking: false,
      data: [{
        color: 'rgb(62, 72, 85)',
        radius: '65%',
        innerRadius: '100%',
        y: eData.market_cap.ratio,
        label: `${eData.market_cap.value} ${eData.market_cap.unit} ${eData.market_cap.currency_iso}`,
        dataLabels: {
          align: 'center',
          verticalAlign: 'middle',
          position: 'center',
          borderWidth: 0,
          format: '<tspan class="fundamental-summary-chart__middle-label">{series.name}</tspan><br><tspan class="fundamental-summary-chart__middle-value">{point.label}</tspan>',
          style: {
            fontSize: '12px',
            textAnchor: 'middle',
          },
          x: 36,
        },
      }]
    },
    {
      name: 'Revenue',
      enableMouseTracking: false,
      data: [{
        color: 'rgb(35, 148, 223)',
        radius: '85%',
        innerRadius: '100%',
        y: eData.revenue.ratio,
        label: `${eData.revenue.value} ${eData.revenue.unit} ${eData.revenue.currency_iso}`,
        dataLabels: {
          allowOverlap: true,
          crop: false,
          overflow: 'allow',
          align: 'center',
          verticalAlign: 'middle',
          position: 'center',
          borderWidth: 0,
          format: '<tspan class="fundamental-summary-chart__middle-label">{series.name}</tspan><br><tspan class="fundamental-summary-chart__middle-value">{point.label}</tspan>',
          style: {
            fontSize: '12px',
            textAnchor: 'middle',
          },
          x: 130,
          y: -110
        },
      }]
    },
    {
      name: 'Earnings',
      enableMouseTracking: false,
      data: [{
        color: 'rgb(113, 231, 214)',
        radius: '65%',
        innerRadius: '85%',
        y: eData.earnings.ratio,
        label: `${eData.earnings.value} ${eData.earnings.unit} ${eData.earnings.currency_iso}`,
        dataLabels: {
          allowOverlap: true,
          crop: false,
          overflow: 'allow',
          align: 'center',
          verticalAlign: 'middle',
          position: 'center',
          borderWidth: 0,
          format: '<tspan class="fundamental-summary-chart__middle-label">{series.name}</tspan><br><tspan class="fundamental-summary-chart__middle-value">{point.label}</tspan>',
          style: {
            fontSize: '12px',
            textAnchor: 'middle',
          },
          x: 30,
          y: -160
        },
      }]
    }
  ]
}

function drawDataLabel() {
  const rDiffX = 10
  const rDiffY = 17
  const rOffsetY = -67
  const rData = this.series[1].data

  const rStartX = rData[0].plotX+rDiffX
  const rStartY = rData[0].plotY+rDiffY
  const rFinishX = rStartX
  const rFinishY = rStartY+rOffsetY


  this.renderer.path(['M', rStartX, rStartY, 'L', rFinishX, rFinishY]).attr({'stroke-width': 1, stroke: '#71E7D6', fill:'transparent', zIndex: 6}).add()
  this.renderer.circle().attr({cx:rFinishX, cy:rFinishY, fill: '#71E7D6', r: 2.5}).add()


  const eData = this.series[2].data
  const eStartX = eData[0].plotX + 15
  const eStartY = eData[0].plotY - 15
  const eMiddleX = eStartX + 18
  const eMiddleY = eStartY - 18

  const eFinishX = eMiddleX + 27
  const eFinishY = eMiddleY


  this.renderer.path(['M', eStartX, eStartY, 'L', eMiddleX, eMiddleY, 'L', eFinishX, eFinishY]).attr({'stroke-width': 1, stroke: '#2394DF', fill:'transparent', zIndex: 6}).add()
  this.renderer.circle().attr({cx:eFinishX, cy:eFinishY, fill: '#2394DF', r: 2.5}).add()

}