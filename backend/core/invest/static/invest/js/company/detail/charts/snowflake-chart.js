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

const data = {
    companySnowflake: {
        score: 23,
        snowflakeData: [5, 2, 6, 5, 5]
    },
    competitors: {
        VTBR: {
            score: 18,
            snowflakeData: [5, 1, 4, 5, 3]
        },
        CBOM: {
            score: 14,
            snowflakeData: [2, 5, 2, 5, 0]
        },
        ROSB: {
            score: 8,
            snowflakeData: [1, 0, 3, 4, 0]
        },
        AVAN: {
            score: 7,
            snowflakeData: [0, 0, 1, 4, 2]
        },
    }
}

const snowflakeChartOpts = {
    chart: {
        polar: true,
        height: 280,
        backgroundColor: 'transparent',
        style: {
            fontFamily: 'inherit',
        },
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
            pointInterval: 72
        },

    },
}
let snowflakeChartSeriesOpts = {
        series: [{
            type: 'areaspline',
            clip: false,
            enableMouseTracking: true,
            fillColor: snowflakeChartColor5, // Цвет заливки
            lineColor: snowflakeChartBorderColor5, // Цвет границы
            lineWidth: 2, // Толщина границы
            opacity:.75, // Прозрачность фона
            xAxis: 0,
            yAxis: 0,
            marker: {
                enabled: false
            },
            data: data['companySnowflake']['snowflakeData'],
            trackByArea: true,
        }]
    }

// Основной Snowflake
Highcharts.chart('snowflake-chart', {
    ...snowflakeChartOpts,
    ...snowflakeChartSeriesOpts
});

function drawSnowflakeChart(index, companyData) {
    const chartID = `snowflake-chart-${index}`
    let snowflakeChartColor = snowflakeChartColor5
    let snowflakeChartBorderColor = snowflakeChartBorderColor5

    switch (true) {
        case companyData['score']  <= 5:
            snowflakeChartColor = snowflakeChartColor1
            snowflakeChartBorderColor = snowflakeChartBorderColor1
            break
        case companyData['score'] <= 10:
            snowflakeChartColor = snowflakeChartColor2
            snowflakeChartBorderColor = snowflakeChartBorderColor2
            break
        case companyData['score'] <= 15:
            snowflakeChartColor = snowflakeChartColor3
            snowflakeChartBorderColor = snowflakeChartBorderColor3
            break
        case companyData['score'] <= 20:
            snowflakeChartColor = snowflakeChartColor4
            snowflakeChartBorderColor = snowflakeChartBorderColor4
            break
    }

    snowflakeChartSeriesOpts = {
        series: [{
            type: 'areaspline',
            clip: false,
            enableMouseTracking: true,
            fillColor: snowflakeChartColor, // Цвет заливки
            lineColor: snowflakeChartBorderColor, // Цвет границы
            lineWidth: 2, // Толщина границы
            opacity:.75, // Прозрачность фона
            xAxis: 0,
            yAxis: 0,
            marker: {
                enabled: false
            },
            data: companyData['snowflakeData'],
            trackByArea: true,
        }]
    }

    Highcharts.chart(chartID, {
        ...snowflakeChartOpts,
        ...snowflakeChartSeriesOpts
    });


}

snowflakeChartOpts['chart']['height'] = 132
snowflakeChartOpts['xAxis'][0]['gridLineWidth'] = 1
snowflakeChartOpts['yAxis'][0]['gridLineWidth'] = 8

let counter = 0
const competitors = data['competitors']

for (let k in competitors) {
    counter++;
    drawSnowflakeChart(counter, competitors[k])
}