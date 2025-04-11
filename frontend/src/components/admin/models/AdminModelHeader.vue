<script setup lang="ts">
// Components
import AdminModelIndicator from '@/components/admin/models/AdminModelIndicator.vue'
import BaseFlag from '@/components/UI/BaseFlag/BaseFlag.vue'

// Composables
import { useAdminModelStore } from '@/store/admin/admin'
import { useAuthStore } from '@/store/auth'
import { useRouter } from 'vue-router'

// Utilities
import { computed, ref, shallowRef, watchEffect } from 'vue'
import { DateTime } from 'luxon'
import { toast } from 'vue3-toastify'

// Types
import type { IFormattedDetailCompany } from '@/types/admin.types'

const store = useAdminModelStore()
const authStore = useAuthStore()
const state = computed<IFormattedDetailCompany>(() => store.formState)
const router = useRouter()

const dialog = shallowRef(false)
const logoURL = ref()

const subtitle = computed(
  () =>
    `${state.value.market.slug?.toUpperCase() || 'Market'}:${state.value.ticker || 'Ticker'}`
)

const createdAt = computed(() =>
  state.value.created
    ? DateTime.fromISO(state.value.created).toFormat('dd LLL yyyy TT')
    : '0000-0000-0000-0000'
)

const updatedAt = computed(() =>
  state.value.updated
    ? DateTime.fromISO(state.value.updated).toFormat('dd LLL yyyy TT')
    : '0000-0000-0000-0000'
)

function addToClipboard(e: MouseEvent) {
  const target = e.target as HTMLElement
  navigator.clipboard
    .writeText(target.innerText)
    .then(() => toast.success('Value is copied'))
    .catch((e) => console.log(e))
}

watchEffect(() => {
  logoURL.value = state.value.logo?.type.startsWith('image')
    ? URL.createObjectURL(state.value.logo)
    : undefined
})
</script>

<template>
  <v-card>
    <v-container>
      <v-row>
        <v-col>
          <v-card-item>
            <v-breadcrumbs
              class="px-0"
              :items="[
                { title: state.sector.name || 'Sector' },
                { title: state.industry.name || 'Industry' },
              ]"
            />
          </v-card-item>
          <v-card-item
            :title="state.companyName || 'Company Name'"
            :subtitle="subtitle"
          >
            <template #prepend>
              <v-avatar
                :image="logoURL"
                text="Logo"
                color="surface-bright"
                size="64"
                rounded="lg"
              />
            </template>
          </v-card-item>
          <v-card-text>
            <span
              v-tippy="{
                content: 'Click to copy UID',
                theme: 'tooltip-theme-paper',
                appendTo: 'parent',
                arrow: false,
              }"
              @click="addToClipboard"
              class="border-0 border-opacity-75 border-b-sm border-dotted border-info cursor-pointer"
            >
              {{ state.uid || '0000-0000-0000-0000' }}
            </span>
          </v-card-text>
          <v-card-text class="py-0">
            <span>
              <base-flag size="24" :code="state.country.slug" />
              {{ state.country.name || 'Country' }}
            </span>
          </v-card-text>
          <v-card-text>
            {{
              `${state.country.currency.name || 'Currency'} (${state.country.currency.symbol || 'Symbol'})`
            }}
          </v-card-text>
        </v-col>
        <v-col>
          <v-card-item class="justify-end">
            <div
              class="d-flex justify-center align-center"
              style="width: 20px; height: 20px"
            >
              <admin-model-indicator :is-active="state.isVisible" />
            </div>
          </v-card-item>
          <v-card-text class="d-flex justify-end">
            <span class="opacity-50 mr-1">Created</span>{{ createdAt }}
          </v-card-text>
          <v-card-text class="d-flex justify-end py-0">
            <span class="opacity-50 mr-1">Updated</span>{{ updatedAt }}
          </v-card-text>
          <v-card-text class="d-flex justify-end">
            <span class="admin-model-company__author px-2 py-3">
              <div class="text-subtitle-2 text-disabled">
                {{ store.companyUID ? 'Modified by: ' : 'Created by: ' }}
              </div>
              <div>
                {{
                  !state.createdBy.lastName
                    ? `${authStore.userInfo.first_name} ${authStore.userInfo.last_name}`
                    : state.updatedBy.lastName
                      ? `${state.updatedBy.lastName} ${state.updatedBy.firstName}`
                      : `${state.createdBy.lastName} ${state.createdBy.firstName}`
                }}
              </div>
            </span>
          </v-card-text>
          <v-card-item v-if="!store.editMode" class="justify-end">
            <v-btn
              class="mr-2"
              color="info"
              variant="tonal"
              text="edit"
              @click="store.openEditMode()"
            />
            <v-btn
              color="error"
              prepend-icon="$iDelete"
              :disabled="store.isNew"
            >
              <v-dialog activator="parent" max-width="500">
                <v-card>
                  <v-card-title>Deletion {{ state.companyName }}</v-card-title>
                  <v-card-text>
                    Are you sure to definitely delete the current model?
                  </v-card-text>
                  <v-card-actions>
                    <v-btn
                      text="yes"
                      color="error"
                      variant="text"
                      @click="store.deleteModel(router)"
                    />
                    <v-btn text="no" variant="text" @click="dialog = false" />
                  </v-card-actions>
                </v-card>
              </v-dialog>

              delete
            </v-btn>
          </v-card-item>
          <v-card-item v-else class="justify-end">
            <v-btn
              prepend-icon="$iReset"
              text="Close Without Saving"
              color="info"
              size="small"
              @click="store.closeEditMode(router)"
            />
          </v-card-item>
        </v-col>
      </v-row>
    </v-container>
  </v-card>
</template>

<style scoped lang="scss">
.admin-model-company__author {
  border: 2px solid transparent;
  background-image:
    linear-gradient(rgb(var(--v-theme-surface)), rgb(var(--v-theme-surface))),
    linear-gradient(315deg, #ee4297, #9176c6);
  background-origin: border-box;
  background-clip: padding-box, border-box;
  text-align: center;
  border-radius: 8px;
}
</style>
