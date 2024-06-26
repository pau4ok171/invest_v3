export const chartOpts = {
  chart: {
    type: 'solidgauge',
    height: 280,
    backgroundColor: '#1b222d',
    spacingTop: 80,
    events: {},
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
  series: [],
  yAxis: {},
  title: {
    text: null
  },
}