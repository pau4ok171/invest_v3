export const defChartOpts = {
  chart: {
    backgroundColor: 'transparent',
    height: 40,
    width: 300,
    spacing: [5, 0, 5, 0],
  },
  series: [
    {
      name: 'price_candles',
      data: [],
      turboThreshold: 10000,
      marker: {
        enabled: false,
        states: {
          hover: {
            enabled: false,
          },
        },
      },
    },
  ],
  xAxis: {
    visible: false,
    crosshair: {
      width: 0,
    },
  },
  yAxis: {
    visible: false,
    crosshair: {
      width: 0,
    },
  },
  scrollbar: {
    enabled: false,
  },
  navigator: {
    enabled: false,
  },
  title: {
    text: null,
  },
  rangeSelector: {
    enabled: false,
  },
  tooltip: {
    enabled: false,
  },
}
