import { priceChartURL } from "../consts.js";

// TODO: Добавить тултип

Highcharts.getJSON(priceChartURL, function (response) {
    const data = get_data(response)

    const SPHChartOpts = {
        chart: {
            backgroundColor: 'transparent',
            height: 40,
            width: 300,
            spacing: [0, 0, 0, 0]
        },
        series: [
            {
                name: 'price_candles',
                data: data
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
    const chart = Highcharts.stockChart('small-price-history-chart', SPHChartOpts)
})

function get_data(response) {
    let data = []
    response.forEach(el => {data.push([el['time'], el['close']])})
    return data
}
