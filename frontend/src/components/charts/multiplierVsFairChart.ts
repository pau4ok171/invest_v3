const fairPE = 4.3
const currentPE = 5.6 // 2.6
const maxY = fairPE * 2
const tickIntervalY = maxY / 4

export const chartOpts = {
  chart: {
    type: 'gauge',
    plotBorderWidth: 0,
    height: 256,
    backgroundColor: null,
  },
  pane: {
    startAngle: -90,
    endAngle: 90,
    size: 240, // Ширина в px
    background: null,
    center: ['50%', '75%'],
  },
  // the value axis
  yAxis: {
    min: 0,
    max: maxY,
    tickInterval: tickIntervalY,
    tickWidth: 0,
    minorTickInterval: null,
    labels: {
      enabled: true,
      format: '{value:.1f}x',
      distance: 20,
      style: {
        fontSize: '12px',
        color: 'rgb(var(--v-theme-on-surface-light))'
      }
    },
    lineWidth: 0,
    plotBands: [{
      from: 0,
      to: fairPE,
      color: '#1f433d', // green
      thickness: '100%', // Ширина окантовки
    }, {
      from: fairPE,
      to: maxY,
      color: 'url(#Chart_Fail_Pattern)', // red
      thickness: '100%',
    }, {
      from: 0,
      to: fairPE,
      color: '#2dc97e', // green
      thickness: 12, // Ширина окантовки
    }, {
      from: fairPE,
      to: maxY,
      color: '#e64141', // red
      thickness: 12
    }]
  },
  series: [{
    data: [currentPE],
    dataLabels: {
      enabled: false
    },
    // Стрелка
    dial: {
      radius: '100%',
      backgroundColor: '#2394df',
      baseWidth: 10,
      topWidth: 6,
      baseLength: '0%',
      rearLength: '0%'
    },
    // Точка стрелки
    pivot: {
      backgroundColor: '#2394df',
      radius: 6
    },
  }],
  credits: {
    enabled: false
  },
  title: {
    text: null
  },
  tooltip: {
    enabled: false
  }
}