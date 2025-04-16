<script setup lang="ts">
// Components
import SnowflakeChart from '@/components/charts/SnowflakeChart.vue'

// Composables
import { useCompanyListStore } from '@/store/companyList/companyList'
import { useAuthStore } from '@/store/auth'

// Utilities
import { inject } from 'vue'

// Types
import type { PropType } from 'vue'
import type { CompanyItem } from '@/store/companyList/types'
import type { ActiveAnimations } from '@/composables/priceUpdater'

const props = defineProps({
  items: {
    type: Object as PropType<CompanyItem[]>,
  },
})

const store = useCompanyListStore()
const authStore = useAuthStore()

const activeAnimations = inject<ActiveAnimations>('activeAnimations') || {}
</script>

<template>
  <v-row style="max-width: 1200px">
    <v-col v-for="item in items" :key="item.uid" cols="3">
      <v-hover #="{ isHovering, props }">
        <v-card v-bind="props" :to="item.to" rounded="lg">
          <div class="company-list-tile-content" v-show="!isHovering">
            <v-card-item
              style="height: 70px"
              :title="item.companyName"
              :subtitle="item.marketCap"
            >
              <template #append>
                <v-btn
                  :icon="item.watchlisted ? '$ratingFull' : '$ratingEmpty'"
                  variant="text"
                  size="small"
                  rounded="lg"
                  :color="item.watchlisted ? 'info': undefined"
                  :disabled="!authStore.isAuthenticated"
                  @click.prevent.stop="store.toggleWatchlisted(item)"
                />
              </template>
            </v-card-item>

            <v-card-item style="height: 185px"
              ><snowflake-chart
                class="company-list-tile-content__snowflake"
                :data="item.snowflake"
                size="154"
                :interactive="false"
            /></v-card-item>

            <v-card-item style="height: 65px">
              <v-row no-gutters>
                <v-col
                  ><div
                    class="d-flex justify-center text-caption text-medium-emphasis"
                  >
                    {{ item.ticker }}
                  </div></v-col
                >
                <v-col
                  ><div
                    class="d-flex justify-center text-caption text-medium-emphasis"
                  >
                    7D
                  </div></v-col
                >
                <v-col
                  ><div
                    class="d-flex justify-center text-caption text-medium-emphasis"
                  >
                    1Y
                  </div></v-col
                >
              </v-row>
              <v-row no-gutters>
                <v-col
                  ><div class="d-flex justify-center">
                    <v-chip
                      label
                      class="price"
                      size="small"
                      :color="
                        activeAnimations[item.uid]
                          ? activeAnimations[item.uid] === 'up'
                            ? 'success'
                            : 'error'
                          : undefined
                      "
                    >
                      {{ item.lastPrice }}
                    </v-chip>
                  </div></v-col
                >
                <v-col
                  ><div class="d-flex justify-center">
                    <v-chip
                      :color="
                        !item.return7D.startsWith('-') ? 'success' : 'error'
                      "
                      label
                      size="small"
                      >{{ item.return7D }}</v-chip
                    >
                  </div></v-col
                >
                <v-col
                  ><div class="d-flex justify-center">
                    <v-chip
                      :color="
                        !item.return1Y.startsWith('-') ? 'success' : 'error'
                      "
                      label
                      size="small"
                      >{{ item.return1Y }}</v-chip
                    >
                  </div></v-col
                >
              </v-row>
            </v-card-item>
          </div>
          <div class="company-list-tile-content" v-show="isHovering">
            <v-card-item style="height: 70px">
              <template #prepend>
                <v-avatar
                  :image="item.companyLogo"
                  variant="tonal"
                  size="small"
                  rounded="lg"
                />
              </template>
              <template #append>
                <v-chip
                  class="mr-2"
                  color="info"
                  label
                  size="x-small"
                  :text="item.sector"
                />
                <v-btn
                  :icon="item.watchlisted ? '$ratingFull' : '$ratingEmpty'"
                  variant="text"
                  size="small"
                  rounded="lg"
                  :color="item.watchlisted ? 'info': undefined"
                  :disabled="!authStore.isAuthenticated"
                  @click.prevent.stop="store.toggleWatchlisted(item)"
                />
              </template>
            </v-card-item>
            <v-card-text style="height: 185px" class="text-caption">
              <span class="company-list-tile-content__description">{{
                item.description
              }}</span>
            </v-card-text>

            <v-card-item style="height: 65px; font-size: 0.625rem">
              <v-row no-gutters>
                <v-col
                  ><div
                    class="d-flex justify-center text-caption text-medium-emphasis"
                  >
                    P/E
                  </div></v-col
                >
                <v-col
                  ><div
                    class="d-flex justify-center text-caption text-medium-emphasis"
                  >
                    Growth
                  </div></v-col
                >
                <v-col
                  ><div
                    class="d-flex justify-center text-caption text-medium-emphasis"
                  >
                    Target
                  </div></v-col
                >
              </v-row>
              <v-row no-gutters>
                <v-col
                  ><div class="d-flex justify-center">
                    <v-chip label size="small">10.0x</v-chip>
                  </div></v-col
                >
                <v-col
                  ><div class="d-flex justify-center">
                    <v-chip label size="small">10.0%</v-chip>
                  </div></v-col
                >
                <v-col
                  ><div class="d-flex justify-center">
                    <v-chip label size="small">RUB2500</v-chip>
                  </div></v-col
                >
              </v-row>
            </v-card-item>
          </div>
        </v-card>
      </v-hover>
    </v-col>
    <v-col
      v-if="store.fetching"
      v-for="i in 20"
      :key="`tile-item-skeleton-${i}`"
    >
      <v-card width="276" height="320" rounded="lg">
        <v-skeleton-loader
          loading
          type="article@2"
          width="100%"
          height="100%"
          color="surface"
        />
      </v-card>
    </v-col>
  </v-row>
</template>

<style scoped lang="scss">
.company-list-tile-content {
  .company-list-tile-content__description {
    display: -webkit-box;
    -webkit-line-clamp: 8;
    -webkit-box-orient: vertical;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .company-list-tile-content__snowflake {
    animation: 700ms cubic-bezier(0.34, 1.56, 0.64, 1) 0s 1 normal forwards
      running snowflake-entry;
  }
  .price {
    color: inherit;
    transition:
      color 0.6s ease-in,
      background-color 0.6s ease-in;
    background-color: transparent;
  }
}

@keyframes snowflake-entry {
  0% {
    opacity: 0;
    transform: scale(0.8);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}
</style>
