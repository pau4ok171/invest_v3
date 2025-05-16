<script setup lang="ts">
// Components
import BaseFlag from '@/components/UI/BaseFlag/BaseFlag.vue'

// Composables
import { useI18n } from 'vue-i18n'

// Utilities
import { onMounted, onUnmounted, ref, shallowRef, watch } from 'vue'
import axios from 'axios'

// Types
import type { SearchCompany } from '@/types/invest'

const searchResponse = ref<SearchCompany[]>([])
const model = shallowRef(false)
const timeoutId = shallowRef(-1)
const { t } = useI18n()

function onUpdate(v: string) {
  clearTimeout(timeoutId.value)

  timeoutId.value = setTimeout(() => getSearchResults(v), 600)
}

function onKeydown(e: KeyboardEvent) {
  if (e.key === 'k' && e.ctrlKey && !e.altKey && !e.shiftKey && !e.metaKey) {
    e.stopPropagation()
    e.preventDefault()

    model.value = !model.value
  }
}

async function getSearchResults(v: string) {
  if (!v.length) {
    searchResponse.value = []
    return
  }

  await axios
    .get('/api/v1/invest/search_query/', {
      params: { query: v },
    })
    .then((response) => {
      searchResponse.value = highlightSearchResponse(response.data, v)
    })
    .catch((err) => {
      console.log(err)
    })
}

function highlightSearchResponse(
  searchResponse: SearchCompany[],
  query: string
) {
  const regex = new RegExp(query, 'gi')
  return searchResponse.map((c) => {
    c.title = c.title.replace(regex, `<span class="mask__highlight">$&</span>`)
    c.ticker = c.ticker.replace(
      regex,
      `<span class="mask__highlight">$&</span>`
    )
    return c
  })
}

watch(model, (val) => {
  if (!val) {
    searchResponse.value = []
  }
})

onMounted(() => {
  document.addEventListener('keydown', onKeydown)
})

onUnmounted(() => {
  document.removeEventListener('keydown', onKeydown)
})
</script>

<template>
  <v-dialog v-model="model" width="600">
    <template #activator="{ props: activatorProps }">
      <v-btn
        v-bind="activatorProps"
        prepend-icon="$iSearch"
        variant="text"
        class="text-body-2 text-capitalize px-3"
      >
        <span class="me-n1">
          <span>{{ t('buttons.search') }}</span>
          <span class="py-1 px-2 ms-2 border rounded text-disabled text-caption"
            >Ctrl+K</span
          >
        </span>
      </v-btn>
    </template>
    <template #default>
      <v-card>
        <v-text-field
          prepend-inner-icon="$iSearch"
          placeholder="Looking for..."
          single-line
          persistent-placeholder
          hide-details
          @update:modelValue="onUpdate"
          :autofocus="true"
        >
          <template #append-inner>
            <v-btn
              size="small"
              border
              class="text-medium-emphasis text-body-2 text-capitalize px-3"
              variant="text"
              @click="model = false"
            >
              <span class="text-caption text-disabled">Esc</span>
            </v-btn>
          </template>
        </v-text-field>

        <v-card-text
          v-if="!searchResponse.length"
          class="px-4 py-0 my-4 d-flex flex-wrap justify-center align-center"
        >
          <div class="text-center">
            <v-icon
              class="text-disabled mb-6 mx-auto"
              size="150"
              icon="$iSearchList"
            />
            <v-list-subheader title="Your search results will appear here" />
          </div>
        </v-card-text>
        <v-card-item v-else class="px-2">
          <v-list slim>
            <v-list-item
              v-for="item in searchResponse"
              :key="item.uid"
              :to="item.absolute_url"
              @click="model = false"
            >
              <template #prepend>
                <base-flag :code="item.country.slug" />
              </template>
              <template #default>
                <v-list-item-title v-html="item.title" />
                <v-list-item-subtitle v-html="item.ticker" />
              </template>
              <template #append>
                <v-chip
                  :text="item.sector.title"
                  label
                  color="info"
                  size="small"
                />
              </template>
            </v-list-item>
          </v-list>
        </v-card-item>
      </v-card>
    </template>
  </v-dialog>
</template>

<style>
.mask__highlight {
  background-color: yellow;
  color: black;
}
</style>
