export const chartOpts = {
  chart: {
    type: 'bar',
    height: 358,
    styledMode: true,
    borderWidth: 0,
    spacingTop: 69,
    spacingBottom: 80,
    className: 'dcf-chart__container',
    events: {},
    plotBackgroundColor: {
      linearGradient: []
    }
  },
  title: {
    text: null,
  },
  xAxis: {
    visible: false,
  },
  yAxis: {},
  legend: {
    enabled: false
  },
  plotOptions: {
    bar: {
      groupPadding: .1,
      borderWidth: 0,
      borderRadius: 0,
      pointWidth: 72, // Высота бары
    }
  },
  series: []
}