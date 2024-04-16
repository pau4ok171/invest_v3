let chartOpts;
export default chartOpts =  {
  chart: {
    backgroundColor: 'transparent',
    height: 40,
    width: 300,
    spacing: [0, 0, 0, 0]
  },
  accessibility: {
    enabled: false,
  },
  series: [
    {
      name: 'price_candles',
      data: [],
      turboThreshold: 10000,
    },
  ],
  xAxis: {
    visible: false
  },
  yAxis: {
    visible: false
  },
  scrollbar: {
    enabled: false
  },
  credits: {
    enabled: false
  },
  navigator: {
    enabled: false
  },
  title: {
    text: null
  },
  rangeSelector: {
    enabled: false,
  },
  tooltip: {
    enabled: false
  }
}