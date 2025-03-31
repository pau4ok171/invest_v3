export const chartOpts = {
  series: [
    {
      data: [],
      threshold: null,
      tooltip: {
        valueDecimals: 2,
      },
      marker: {
        radius: 2,
        fillColor: 'rgb(var(--v-theme-on-surface-light))',
      },
    },
  ],
  chart: {
    marginTop: 40,
    style: {
      fontFamily: 'inherit',
      fontSize: '1rem',
      fontWeight: 'normal',
    },
    zooming: {
      mouseWheel: {
        enabled: false,
      },
    },
  },
  xAxis: [
    {
      visible: true,
      crosshair: {
        color: '#5C6874',
        dashStyle: 'dash',
      },
      labels: {
        style: {
          color: 'rgb(var(--v-theme-on-surface-light))',
          opacity: 1,
        },
      },
    },
  ],
  yAxis: [
    {
      visible: false,
      crosshair: {
        color: '#5C6874',
        dashStyle: 'dash',
      },
    },
  ],
  scrollbar: {
    enabled: false,
  },
  rangeSelector: {
    enabled: false,
  },
  navigator: {
    height: 32,
    top: 4,
    outlineWidth: 0,
    maskFill: 'rgba(35, 148, 223, 0.2)',
    handles: {
      enabled: false,
    },
    xAxis: {
      enabled: false,
      gridLineWidth: 0,
      labels: {
        overflow: 'allow',
        y: -10,
        align: 'center',
        style: {
          color: 'rgb(var(--v-theme-on-surface-light))',
          opacity: 1,
          fontSize: '.75rem',
        },
      },
    },
  },
  tooltip: {
    backgroundColor: 'rgb(var(--v-theme-surface-bright))',
    borderRadius: '3',
    padding: 8,
    borderWidth: 0,
    headerFormat: '',
    xDateFormat: '%a, %e %b %Y',
    pointFormat:
      '<tspan class="price-history-chart-point-box__date">{point.key}</tspan><br><tspan class="price-history-chart-point-box__price">₽{point.y}</tspan>',
    footerFormat: '',
    style: {
      fontSize: '.875rem',
    },
  },
}
