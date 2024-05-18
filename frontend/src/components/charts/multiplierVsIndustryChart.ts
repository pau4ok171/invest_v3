const dataPE = [1,9,12,48,39,31,26,13,9,10,2,2,0,2,2,0,0,1,0,0,6]
const dataPS = [0,6,8,18,34,18,22,22,18,14,9,13,5,10,4,1,3,2,1,1,8]
const dataPB = [5,25,28,28,33,32,16,17,5,9,7,3,1,1,2,1,2,1,1,1,1]
export const chartOpts = {
  chart: {
    spacingTop: 40,
    height: 324,
    backgroundColor: '#1b222d',
    plotBackgroundColor: 'url(#Chart_Fail_Pattern)',
    style: {
      fontFamily: 'inherit',
      fontSize: '1.6rem',
      fontWeight: 'normal'
    },
    type: 'column',
  },
  xAxis: {
    tickInterval: 1.5,
    showLastLabel: true,
    lineColor: '#494e57',
    tickLength: 4,
    tickColor: '#494e57',
    labels: {
      step: 4,
      distance: 10,
      formatter: function (this: any) {
        return this.isLast ? `${this.value}+` : this.value
      },
      style: {
        color: '#fff',
        fontSize: 11,
      }
    },
    left: '1.25%',
    width: '97.5%',
    title: {
      text: 'PE',
      align: 'low',
      offset: 10,
      x: -5,
      style: {
        color: '#fff',
        fontSize: 10,
        fontWeight: 'normal',
      }
    }
  },
  yAxis: {
    min: 0,
    max: 48,
    gridLineWidth: 1,
    gridLineColor: 'rgba(255,255,255,.1)',
    tickInterval: 48/4,
    lineColor: '#494e57',
    top: '3.0%',
    height: '97,5%',
    labels: {
      step: 4,
      style: {
        color: '#fff',
        fontSize: 11,
      },
      x: 20,
      y: 15,
    },
    showFirstLabel: false,
    showLastLabel: true,
    title: {
      text: 'No. of Companies',
      align: 'low',
      offset: -15,
      y: -9,
      style: {
        color: '#fff',
        fontSize: 11,
        fontWeight: 'normal',
      }
    }
  },
  plotOptions: {
    column: {
      borderWidth: 0
    },
    series: {
      borderRadius: 0,
      color: 'url(#Noir_Gradient_01)',
      pointPlacement: 0.5,
      pointWidth: 34,
    }
  },
  series: [
    {
      visible: true,
      name: 'PE',
      pointInterval: 1.5,
      data: dataPE
    }, {
      visible: false,
      name: 'PS',
      pointInterval: 0.3,
      data: dataPS
    }, {
      visible: false,
      name: 'PB',
      pointInterval: 0.2,
      data: dataPB
    },
  ],
  legend: {
    enabled: false
  },
  credits: {
    enabled: false
  },
  title: {
    text: null,
  },
  tooltip: {
    enabled: false
  }
}

const averagesMI = {
  0: {
    labelTextX: 'PE',
    industryValue: 7.4,
    companyValue: 2.6,
    maxY: 48,
    intervalX: 1.5,
  },
  1: {
    labelTextX: 'PS',
    industryValue: 2.1,
    companyValue: 1.2,
    maxY: 34,
    intervalX: 0.3,
  },
  2: {
    labelTextX: 'PB',
    industryValue: 0.7,
    companyValue: 0.5,
    maxY: 33,
    intervalX: 0.2,
  },
}
