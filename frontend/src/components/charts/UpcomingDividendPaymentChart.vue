<script setup lang="ts">
// Utilities
import { computed } from 'vue'
import { DateTime } from 'ts-luxon'

// Types
import type { Chart, Options, SVGElement } from 'highcharts'

// Consts
const BAR_WIDTH = 40
const LINE_WIDTH = 2
const LINE_HEIGHT = 56

const today = DateTime.now()
const chartElements = [] as SVGElement[]

const data = {
  exDividendDate: 1749168000,
  dividendPayDate: 1750982400,
}

// Получаем разницу в днях
const daysToDividend =
  Math.round(
    DateTime.fromSeconds(data.exDividendDate).diff(today, 'days').days
  ) + 1
const daysToPayment =
  Math.round(
    DateTime.fromSeconds(data.dividendPayDate).diff(
      DateTime.fromSeconds(data.exDividendDate),
      'days'
    ).days
  ) + 1

const drawItems = (chart: Chart) => {
  // Delete previous elements
  deleteElements()

  const todayData = chart.series[0].data[0]
  const exDividendData = chart.series[1].data[0]
  const fromX = chart.plotLeft
  const fromY = chart.plotTop + (todayData.shapeArgs?.x || 0) + BAR_WIDTH

  const exDivFromX = fromX + (exDividendData.shapeArgs?.height || 0)
  const divPayFromX = fromX + (todayData.shapeArgs?.height || 0) - LINE_WIDTH

  // Today Elements
  const todayLine = chart.renderer
    .rect(fromX, fromY, LINE_WIDTH, LINE_HEIGHT)
    .attr({
      fill: 'rgb(var(--v-theme-hc-series1-color))',
      zIndex: 4,
    })
    .add()

  const todayText = chart.renderer
    .text(
      `Today<br/>${today.toFormat('MMM dd yyyy')}`,
      fromX,
      fromY + LINE_HEIGHT + 20
    )
    .css({
      color: 'rgb(var(--v-theme-on-surface))',
      fontSize: '0.875rem',
      fontWeight: '500',
    })
    .add()

  // Ex Dividend Data Elements
  const exDividendLine = chart.renderer
    .rect(
      exDivFromX,
      fromY - LINE_HEIGHT - BAR_WIDTH + 20,
      LINE_WIDTH,
      LINE_HEIGHT - 20
    )
    .attr({
      fill: 'rgb(var(--v-theme-hc-series3-color))',
      zIndex: 4,
    })
    .add()

  const exDividendText = chart.renderer
    .text(
      `Ex Dividend Date<br/>${DateTime.fromSeconds(data.exDividendDate).toFormat('MMM dd yyyy')}`,
      exDivFromX,
      fromY - LINE_HEIGHT - 50
    )
    .css({
      color: 'rgb(var(--v-theme-on-surface))',
      fontSize: '0.875rem',
      fontWeight: '500',
    })
    .add()

  // Dividend Pay Date Elements
  const dividendPayLine = chart.renderer
    .rect(divPayFromX, fromY, LINE_WIDTH, LINE_HEIGHT)
    .attr({
      fill: 'rgb(var(--v-theme-hc-series3-color))',
      zIndex: 4,
    })
    .add()

  const dividendPayText = chart.renderer
    .text(
      `<div class="text-hc-series3-color">Dividend Pay Date</div><div>${DateTime.fromSeconds(data.dividendPayDate).toFormat('MMM dd yyyy')}</div>`,
      divPayFromX - 115,
      fromY + LINE_HEIGHT + 20,
      true
    )
    .css({
      color: 'rgb(var(--v-theme-on-surface))',
      fontSize: '0.875rem',
      fontWeight: '500',
    })
    .add()

  chartElements.push(todayLine)
  chartElements.push(todayText)
  chartElements.push(exDividendLine)
  chartElements.push(exDividendText)
  chartElements.push(dividendPayLine)
  chartElements.push(dividendPayText)
}

const deleteElements = () => {
  chartElements.forEach((el) => {
    el.destroy()
  })
}

const options = computed<Options>(() => {
  const todaySeconds = today.toSeconds()
  const totalDuration = data.dividendPayDate - todaySeconds
  const exDividendPosition =
    (data.exDividendDate - todaySeconds) / totalDuration

  return {
    chart: {
      type: 'bar',
      height: 227,
      backgroundColor: 'transparent',
      spacingRight: 0,
      events: {
        load: function () {
          drawItems(this)
        },
        redraw: function () {
          drawItems(this)
        },
      },
    },
    title: { text: undefined },
    legend: { enabled: false },
    xAxis: {
      visible: false,
    },
    yAxis: {
      visible: false,
      min: 0,
      max: 1,
    },
    tooltip: {
      format: `Buy in the next ${daysToDividend} days to receive the upcoming dividend`,
      backgroundColor: 'rgb(var(--v-theme-surface))',
      style: {
        color: 'rgb(var(--v-theme-on-surface))',
      },
      positioner: function (labelWidth, labelHeight) {
        const chart = this.chart
        return {
          x: chart.plotLeft + chart.plotWidth / 2 - labelWidth / 2,
          y: chart.plotTop + chart.plotHeight / 2 - labelHeight / 2,
        }
      },
    },
    plotOptions: {
      bar: {
        borderRadius: 0,
        grouping: false,
        pointWidth: BAR_WIDTH,
        borderWidth: 0,
        states: {
          inactive: { enabled: false },
          hover: { enabled: false },
        },
      },
    },
    series: [
      // Основная полоса (прогресс)
      {
        type: 'bar',
        dataLabels: {
          enabled: true,
          format: `${daysToPayment} days`,
          align: 'left',
          verticalAlign: 'center',
          style: {
            color: 'rgb(var(--v-theme-on-surface))',
            fontSize: '0.875rem',
            fontWeight: '500',
            textOutline: 'none',
            stroke: 'none',
          },
        },
        data: [
          {
            x: 0,
            y: 1,
            color: 'rgb(var(--v-theme-hc-series3-color))',
          },
        ],
      },
      // Зона Ex-Dividend
      {
        type: 'bar',
        dataLabels: {
          enabled: true,
          format: `${daysToDividend} days`,
          align: 'right',
          verticalAlign: 'center',
          style: {
            color: 'rgb(var(--v-theme-on-surface))',
            fontSize: '0.875rem',
            fontWeight: '500',
            textOutline: 'none',
            stroke: 'none',
          },
        },
        data: [
          {
            x: 0,
            y: exDividendPosition,
            color: 'rgb(var(--v-theme-hc-series1-color))',
          },
        ],
      },
    ],
  }
})
</script>

<template>
  <div class="upcoming-dividend-payment-chart">
    <charts
      class="upcoming-dividend-payment-chart__chart"
      constructorType="chart"
      :options="options"
    />
  </div>
</template>

<style scoped lang="scss"></style>
