export const chartOpts = {
  chart: {
    backgroundColor: '#1b222d',
    type: 'solidgauge',
    height: '80%',
    spacingTop: 80,
    events: {}
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
  series: []
}