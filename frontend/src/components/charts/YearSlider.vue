<script setup lang="ts">
// Utilities
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { indexOf, debounce } from 'lodash'

const props = defineProps({
  maxYear: {
    type: Number,
    required: true,
  },
  minYear: {
    type: Number,
    required: true,
  },
  modelValue: {
    type: Number,
    required: true,
  },
})

const emit = defineEmits(['update:modelValue'])

const trackRef = ref<HTMLElement | null>(null)
const thumbRef = ref<HTMLElement | null>(null)
const selectedYear = ref<number>(props.modelValue)
const isDragging = ref(false)
const trackWidth = ref(0)

const values: number[] = []
for (let i = props.minYear; i <= props.maxYear; i++) {
  values.push(i)
}

// Обновляем ширину трека при изменении размеров
const updateTrackWidth = () => {
  if (trackRef.value) {
    trackWidth.value = trackRef.value.clientWidth
  }
}

// Дебаунсим обработчик ресайза
const handleResize = debounce(() => {
  updateTrackWidth()
}, 100)

const left = computed(() => {
  const index = indexOf(values, selectedYear.value)
  const step = trackWidth.value / values.length
  return `${index * step}px`
})

const handleClick = (year: number) => {
  selectedYear.value = year
  emit('update:modelValue', selectedYear.value)
}

const startDrag = (e: MouseEvent) => {
  isDragging.value = true
  document.addEventListener('mousemove', handleDrag)
  document.addEventListener('mouseup', stopDrag)
  handleDrag(e)
}

const handleDrag = (e: MouseEvent) => {
  if (!isDragging.value || !trackRef.value) return

  const trackRect = trackRef.value.getBoundingClientRect()
  const clientX = e.clientX
  let position = (clientX - trackRect.left) / trackRect.width

  position = Math.max(0, Math.min(1, position))

  const index = Math.round(position * (values.length - 1))
  const newYear = values[index]

  if (newYear !== selectedYear.value) {
    selectedYear.value = newYear
    emit('update:modelValue', newYear)
  }
}

const stopDrag = () => {
  isDragging.value = false
  document.removeEventListener('mousemove', handleDrag)
  document.removeEventListener('mouseup', stopDrag)
}

// Инициализация и подписка на события
onMounted(() => {
  updateTrackWidth()
  window.addEventListener('resize', handleResize)

  // Наблюдаем за изменениями размеров трека
  const resizeObserver = new ResizeObserver(handleResize)
  if (trackRef.value) {
    resizeObserver.observe(trackRef.value)
  }

  onUnmounted(() => {
    window.removeEventListener('resize', handleResize)
    resizeObserver.disconnect()
    document.removeEventListener('mousemove', handleDrag)
    document.removeEventListener('mouseup', stopDrag)
  })
})
</script>

<template>
  <div class="year-slider">
    <div ref="trackRef" class="year-slider__track">
      <div class="year-slider__track-chart"></div>
      <div
        v-for="(year, i) in values"
        :key="`year-${year}`"
        class="w-100 h-100 d-flex align-center justify-center"
        @click="handleClick(year)"
      >
        <p
          :class="[
            'year-slider__track-year',
            {
              'year-slider__track-year--active': selectedYear === year,
            },
          ]"
        >
          {{ i % 2 === 0 || selectedYear === year ? year : '' }}
        </p>
      </div>
    </div>
    <div
      ref="thumbRef"
      class="year-slider__thumb"
      :style="{ left: left }"
      @mousedown="startDrag"
    />
  </div>
</template>

<style scoped lang="scss">
.year-slider {
  position: relative;
  height: 40px;
  user-select: none;
  cursor: pointer;
  appearance: none;
  -moz-appearance: none;

  &__track {
    position: absolute;
    left: 0;
    right: 0;
    display: grid;
    width: 100%;
    height: 40px;
    background-color: rgb(var(--v-theme-surface-bright));
    border-radius: 8px;
    grid-template-columns: repeat(12, 1fr);
    place-items: center;
    -webkit-box-align: center;
  }
  &__track-chart {
    position: absolute;
    width: 100%;
  }
  &__track-year {
    font-size: 0.75rem;
    margin: 0;
    line-height: 1.5;
    color: rgb(var(--v-theme-on-surface-bright));

    &--active {
      font-weight: bold;
      font-size: 0.875rem;
    }
  }
  &__thumb {
    position: absolute;
    touch-action: none;
    z-index: 1;
    will-change: left;
    cursor: grab;
    width: calc(8.33333%);
    height: 50px;
    top: -5px;
    border-radius: 6px;
    background-color: rgba(var(--v-theme-hc-series1-color), 0.2);
  }
}
</style>
