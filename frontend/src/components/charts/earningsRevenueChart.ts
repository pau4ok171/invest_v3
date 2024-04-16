export const chartOpts = {
  chart: {
    type: 'waterfall',
    backgroundColor: "#1b222d",
    height: 280,
  },
  accessibility: {
    enabled: false
  },
  title: {
    text: ""
  },
  credits: {
    enabled: false
  },
  xAxis: {
    visible: true,
    type: 'category',
    lineColor: "#fff",
    labels: {
      style: {
        fontSize: '1.2rem',
        fontWeight: 500,
        lineHeight: 1.5,
        color: '#fff',
        whiteSpace: 'normal',
      },
      useHTML: true,
      format: '<tspan class="earnings-revenue-chart__middle-label">{value}</tspan>',
      rotation: 0,
    }
  },
  yAxis: {
    visible: false
  },
  legend: {
    enabled: false
  },
  tooltip: {
    enabled: false
  },
  plotOptions: {
    series: {
      borderWidth: 0
    }
  },
  series: [{
    data: [{
      name: 'Revenue',
      color: "#2394DF",
      y: 2430
    }, {
      name: 'Cost of Revenue',
      color: "rgba(230,65,65,.5)",
      y: -47.50
    }, {
      name: 'Gross Profit',
      color: "#2DC97E",
      isIntermediateSum: true,
    }, {
      name: 'Other Expenses',
      color: "rgba(230,65,65,.5)",
      y: -1200
    }, {
      name: 'Earnings',
      color: "#71E7D6",
      isSum: true,
    }],
    dataLabels: {
      enabled: true,
      color: "#fff",
      style: {
        fontSize: "1.2rem",
        lineHeight: 1.5,
        fontWeight: 500,
      },
      format: '{(abs y):,.f}B',
      verticalAlign: 'top',
      y: -25
    },
    pointPadding: 0,
    groupPadding: .025,
    enableMouseTracking: false,
  }]
}