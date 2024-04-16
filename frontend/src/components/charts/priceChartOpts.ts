export const chartOpts = {
  series: [{
    data: [],
    threshold: null,
    tooltip: {
      valueDecimals: 2
    },
  }],
  chart: {
    backgroundColor: "#1b222d",
    style: {
      fontFamily: 'inherit',
      fontSize: '1.6rem',
      fontWeight: 'normal'
    }
  },
  accessibility: {
    enabled: false,
  },
  xAxis: [{
    visible: true,
    labels: {
      style: {
        color: '#fff',
        opacity: 1,
      }
    }
  }],
  yAxis: [{
    visible: false
  }],
  scrollbar: {
    enabled: false
  },
  credits: {
    enabled: false
  },
  rangeSelector: {
    floating: true,
    inputEnabled: false,
    selected: 2,
    buttons: [
      {
        type: 'month',
        count: 1,
        text: '1M',
      }, {
        type: 'month',
        count: 3,
        text: '3M',
      }, {
        type: 'year',
        count: 1,
        text: '1Y',
      }, {
        type: 'year',
        count: 3,
        text: '3Y',
      }, {
        type: 'year',
        count: 5,
        text: '5Y',
      }, {
        type: 'all',
        text: 'Max'
    }],
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
