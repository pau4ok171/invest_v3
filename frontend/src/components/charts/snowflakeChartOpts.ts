let chartOpts;

const snowflakeChartColor5 = '#6bc51a'
const snowflakeChartBorderColor5 = '#79ee04'

const snowflakeChartColor4 = '#b2c319'
const snowflakeChartBorderColor4 = '#def30b'

const snowflakeChartColor3 = '#c7a028'
const snowflakeChartBorderColor3 = '#ffc413'

const snowflakeChartColor2 = '#c75633'
const snowflakeChartBorderColor2 = '#ff5a23'

const snowflakeChartColor1 = '#c74a35'
const snowflakeChartBorderColor1 = '#fb4a27'

export default chartOpts =  {
  chart: {
    polar: true,
    height: 280,
    backgroundColor: 'transparent',
    style: {
      fontFamily: 'inherit',
    },
  },
  accessibility: {
    enabled: false,
  },
  title: {
    text: ''
  },
  legend: {
    enabled: false
  },
  credits: {
    enabled: false
  },
  pane: [{
    startAngle: 0,
    size: '80%',
    endAngle: 360,
    background: {
      backgroundColor: '#4b5966',
      borderWidth: 0,
      outerRadius: '108%',
    }
  }],
  xAxis: [{
    pane: 0,
    tickInterval: 72,
    min: 0,
    max: 360,
    lineColor: 'transparent',
    gridLineColor: '#4b5966',
    gridLineWidth: 3,
    gridZIndex: 2,
    labels: {
      enabled: false
    },
  }],
  yAxis: [{
    pane: 0,
    tickInterval: 2,
    min: 0,
    max: 6,
    gridLineColor: "#283440",
    gridLineWidth: 18,
    gridLineInterpolation: 'circle',
    labels: {
      enabled: false
    },
  }],
  plotOptions: {
    series: {
      pointStart: 0,
      pointInterval: 72,
    },

  },
  series: [{
    type: 'areaspline',
    clip: false,
    enableMouseTracking: false,
    fillColor: snowflakeChartColor5, // Цвет заливки
    lineColor: snowflakeChartBorderColor5, // Цвет границы
    lineWidth: 2, // Толщина границы
    opacity:.75, // Прозрачность фона
    xAxis: 0,
    yAxis: 0,
    marker: {
      enabled: false,
      states: {
        hover: {
          enabled: false
        }
      }
    },
    data: [],
    trackByArea: false,
  }],
  tooltip: {
    enabled: false,
  },
}



