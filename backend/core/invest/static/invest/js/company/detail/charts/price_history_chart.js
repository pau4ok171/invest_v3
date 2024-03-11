import { priceChartURL } from "../consts.js";

Highcharts.setOptions({
    lang: {
        rangeSelectorZoom: ''
    }
});

let chart;

Highcharts.getJSON(priceChartURL, function (response) {
    const data = get_data(response)

    // Create the chart
    chart = Highcharts.stockChart('price-history-chart', {
        series: [{
            data: data,
            threshold: null,
            tooltip: {
                valueDecimals: 2
            },

        }],
        chart: {
            events: {
                load: get_new_price
            },
            backgroundColor: "#1b222d",
            style: {
                fontFamily: 'inherit',
                fontSize: '1.6rem',
                fontWeight: 'normal'
            }
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
    });
});

function get_new_price(){
    setInterval(get_last_price, 1000*60*2.5) // Каждые 2,5 минуты
}

function get_last_price() {
    fetch(priceChartURL)
            .then(response => {return response.json()})
            .then(response => {set_or_update_ponts(response)})
            .catch(err => {console.log(err)})
}

function set_or_update_ponts(response) {
    const data = get_data(response)
    const d1 = data.pop() // Последняя цена
    update_header_data(d1)
    const d2 = data.pop() // Предпоследняя цена
    const length = chart.series[0].points["length"]
    const last_price = chart.series[0].points[length - 1]
    // Если d1 и last_price совпадают по времени
    if (d1[0] === last_price['x']) {
        last_price['y'] = d1[1]
        chart.redraw()
    } else {
        last_price['y'] = d2[1]
        chart.series[0].addPoint(d1, true, false)
    }
}

function get_data(response) {
    let data = []
    response.forEach(el => {
        data.push([el['time'], el['close']])
    })
    return data
}

function update_header_data(last_price) {
    const price_container = document.querySelector('.company-detail-header__last-price')
    price_container.innerText = `P${last_price[1].toFixed(2)}`
}


