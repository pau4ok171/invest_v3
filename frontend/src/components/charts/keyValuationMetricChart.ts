export const chartOpts = {
  chart: {
    type: 'solidgauge',
    height: 280,
    backgroundColor: 'rgb(var(--v-theme-surface-light))',
    spacingTop: 80,
    events: {},
  },
  pane: {
    size: 184,
    background: {
      backgroundColor: 'rgb(var(--v-theme-on-surface-light))',
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