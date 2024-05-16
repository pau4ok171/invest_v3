export const chartOpts = {
  series: [{
    data: [],
    threshold: null,
    tooltip: {
      valueDecimals: 2
    },
    marker: {
      radius: 2,
      fillColor: '#fff',
    }
  }],
  chart: {
    backgroundColor: "#1b222d",
    style: {
      fontFamily: 'inherit',
      fontSize: '1.6rem',
      fontWeight: 'normal'
    },
    zooming: {
      mouseWheel: {
        enabled: false
      }
    }
  },
  xAxis: [{
    visible: true,
    crosshair: {
      color: '#5C6874',
      dashStyle: 'dash',
    },
    labels: {
      style: {
        color: '#fff',
        opacity: 1,
      }
    }
  }],
  yAxis: [{
    visible: false,
    crosshair: {
      color: '#5C6874',
      dashStyle : 'dash',
    }
  }],
  scrollbar: {
    enabled: false
  },
  rangeSelector: {
    enabled: false,
  },
  navigator: {
    xAxis: {
      labels: {
        style: {
          color: '#fff',
          opacity: 1,
        }
      }
    }
  },
  tooltip: {
    backgroundColor: '#000',
    borderRadius: '8',
    headerFormat: '',
    xDateFormat: '%a, %e %b, %Y',
    pointFormat: '<tspan class="price-history-chart-point-box__date">{point.key}</tspan><br><tspan class="price-history-chart-point-box__price">P{point.y}</tspan>',
    footerFormat: ''
  }
}
