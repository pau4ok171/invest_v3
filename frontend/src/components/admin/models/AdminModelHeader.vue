<script setup lang="ts">
// Components
import AdminModelIndicator from '@/components/admin/models/AdminModelIndicator.vue'
import { BaseButton } from '@/apps/visagiste/components/BaseButton'
import { BaseDialog } from '@/apps/visagiste/components/BaseDialog'
import { BaseCardTitle } from '@/apps/visagiste/components/BaseCard'
import { BaseCardText } from '@/apps/visagiste/components/BaseCard'
import { BaseCardActions } from '@/apps/visagiste/components/BaseCard'
import { BaseCard } from '@/apps/visagiste/components/BaseCard'

// Composables
import { useAdminStore } from '@/store/admin'
import { useAuthStore } from '@/store/auth'

// Utilities
import { computed, shallowRef } from 'vue'
import { DateTime } from 'luxon'
import { toast } from 'vue3-toastify'

const adminStore = useAdminStore()
const authStore = useAuthStore()

const dialog = shallowRef(false)

function getURLFromFile(image: File): string {
  try {
    return URL.createObjectURL(image)
  } catch {
    return ''
  }
}

function getFormattedDate(isoDateTime: string) {
  return DateTime.fromISO(isoDateTime).toFormat('dd LLL yyyy TT')
}

function copyValue(e: MouseEvent) {
  const target = e.target as HTMLHtmlElement
  navigator.clipboard
    .writeText(target.innerText)
    .then(() => toast.success('Value Copied'))
    .catch((err) => console.log(err))
}

const moderFullName = computed(() => {
  if (adminStore.companyFormData.updatedBy.lastName.length) {
    return `${adminStore.companyFormData.updatedBy.lastName} ${adminStore.companyFormData.updatedBy.firstName}`
  }
  if (adminStore.companyFormData.createdBy.lastName.length) {
    return `${adminStore.companyFormData.createdBy.lastName} ${adminStore.companyFormData.createdBy.firstName}`
  }
  return `${authStore.userInfo.last_name} ${authStore.userInfo.first_name}`
})

const nameOfModification = computed(() => {
  if (!adminStore.companyUID.length) {
    return 'Creating by:'
  }
  if (adminStore.companyFormData.updatedBy.lastName.length) {
    return 'Modified by:'
  }
  return 'Created by:'
})
</script>

<template>
  <div class="admin-model__admin-model-header">
    <div>
      <div class="admin-model-header__breadcrumbs">
        {{
          adminStore.companyFormData.sector.slug
            ? adminStore.companyFormData.sector.name
            : 'Sector'
        }}
        /
        {{
          adminStore.companyFormData.industry.slug
            ? adminStore.companyFormData.industry.name
            : 'Industry'
        }}
      </div>
      <div class="admin-model-header__block-company-name">
        <div class="admin-header__logo-wrapper">
          <img
            class="admin-header__logo"
            :src="getURLFromFile(adminStore.companyFormData.logo)"
            alt="LOGO"
            v-if="adminStore.companyFormData.logo?.size"
          />
          <span class="admin-header__logo-text" v-else>Logo</span>
        </div>
        <div>
          <div class="admin-model-header__company-name">
            {{
              adminStore.companyFormData.companyName
                ? adminStore.companyFormData.companyName
                : 'Company Name'
            }}
          </div>
          <div class="admin-model-header__ticker">
            <span>{{
              adminStore.companyFormData.market.slug
                ? adminStore.companyFormData.market.slug.toUpperCase()
                : 'Market'
            }}</span>
            <span>:</span>
            <span>{{
              adminStore.companyFormData.ticker
                ? adminStore.companyFormData.ticker
                : 'Ticker'
            }}</span>
          </div>
        </div>
      </div>

      <div
        v-tippy="{
          content: 'Click to copy UID',
          theme: 'tooltip-theme-paper',
          appendTo: 'parent',
          arrow: false,
        }"
        class="admin-model-header__item admin-model-header__item--tooltip"
        @click="copyValue"
      >
        {{
          adminStore.companyFormData.uid
            ? adminStore.companyFormData.uid
            : '0000-0000-0000-0000'
        }}
      </div>
      <div class="admin-model-header__item">
        <img
          class="admin-model-header__country-flag-icon"
          :src="adminStore.companyFormData.country.flagURL"
          alt="Country"
          v-if="adminStore.companyFormData.country.flagURL"
        />
        {{
          adminStore.companyFormData.country.slug
            ? adminStore.companyFormData.country.name
            : 'Country'
        }}
      </div>
      <div class="admin-model-header__item">
        {{
          adminStore.companyFormData.country.currency?.name
            ? `${adminStore.companyFormData.country.currency.name} (${adminStore.companyFormData.country.currency.symbol})`
            : 'Currency Symbol'
        }}
      </div>
    </div>
    <div class="admin-model-header__last-column">
      <div class="admin-model-header__indicator">
        <AdminModelIndicator
          :is-active="adminStore.companyFormData.isVisible"
        />
      </div>

      <div class="admin-model-header__last-column-info">
        <div class="admin-model-header__item">
          Created:
          {{
            adminStore.companyFormData.created
              ? getFormattedDate(adminStore.companyFormData.created)
              : '00.00.0000 00:00:00'
          }}
        </div>
        <div class="admin-model-header__item">
          Updated:
          {{
            adminStore.companyFormData.updated
              ? getFormattedDate(adminStore.companyFormData.updated)
              : '00.00.0000 00:00:00'
          }}
        </div>
        <div class="admin-model-header__item">
          <div class="admin-model-header__item-modified-by">
            <div
              class="admin-model-header__item-modified-by-title"
              v-text="nameOfModification"
            ></div>
            <div
              class="admin-model-header__item-modified-by-value"
              v-text="moderFullName"
            ></div>
          </div>
        </div>
      </div>

      <div class="admin-model-header__action-list">
        <template v-if="!adminStore.editModeActivated">
          <div class="admin-model-header__item">
            <base-button
              color="info"
              prepend-icon="$iEdit"
              text="edit"
              rounded="large"
              @click="adminStore.activateEditMode()"
            />
          </div>

          <base-dialog v-model="dialog" max-width="500">
            <template #activator="{ props: activatorProps }">
              <base-button
                v-bind="activatorProps"
                color="error"
                prepend-icon="$iDelete"
                text="delete"
                rounded="large"
                :disabled="adminStore.isNewModel"
              />
            </template>
            <template #default>
              <base-card>
                <base-card-title
                  >Deletion
                  {{ adminStore.companyFormData.companyName }}</base-card-title
                >
                <base-card-text>
                  Are you sure to definitely delete the current model?
                </base-card-text>
                <base-card-actions>
                  <base-button
                    text="yes"
                    color="error"
                    variant="text"
                    @click="adminStore.deleteModel()"
                  />
                  <base-button
                    text="no"
                    variant="text"
                    @click="dialog = false"
                  />
                </base-card-actions>
              </base-card>
            </template>
          </base-dialog>
        </template>
        <template v-else>
          <div class="admin-model-header__item">
            <base-button
              prepend-icon="$iReset"
              text="Close Edit Mode Without Saving"
              color="info"
              rounded="large"
              size="small"
              @click="adminStore.deactivateEditMode()"
            />
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.admin-model__admin-model-header {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 8px;
  background-color: #1b222d;
  width: 100%;
  min-height: 200px;
  border-radius: 8px;
  margin-bottom: 16px;
  padding: 16px 32px;
}
.admin-model-header__breadcrumbs {
  margin-bottom: 1.5rem;
  font-size: 0.875rem;
}
.admin-model-header__block-company-name {
  padding-bottom: 10px;
}
.admin-header__logo-wrapper {
  margin: 4px 12px 0 0;
  float: left;
  background-color: #92969c;
  border-radius: 8px;
  height: 56px;
  width: 56px;
}
.admin-header__logo-text {
  font-size: 0.875rem;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}
.admin-header__logo {
  width: 56px;
  height: 56px;
  min-width: 56px;
  min-height: 56px;
  border: 1px solid #fff;
  background-color: #fff;
  border-radius: 8px;
  object-fit: scale-down;
  vertical-align: text-bottom;
}
.admin-model-header__company-name {
  font-size: 1.75rem;
  line-height: 1.25;
  font-weight: 500;
  overflow: hidden;
}
.admin-model-header__ticker {
  font-size: 1rem;
  line-height: 1.5;
  color: rgba(255, 255, 255, 0.7);
}
.admin-model-header__item {
  font-size: 0.875rem;
  margin-bottom: 5px;

  &--tooltip {
    border-bottom: 1px dotted rgb(35, 148, 223);
    width: max-content;
    cursor: pointer;
  }
}
.admin-model-header__last-column {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
.admin-model-header__last-column-info {
  display: flex;
  flex-direction: column;
  align-items: end;
}
.admin-model-header__action-list {
  display: flex;
  justify-content: end;
  gap: 8px;
}
.admin-model-header__indicator {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: end;
}
.admin-model-header__country-flag-icon {
  height: 10px;
  width: 15px;
}
.admin-model-header__item-modified-by {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 2px;
  min-width: 130px;
  border: 2px solid transparent;
  border-radius: 8px;
  padding: 10px;
  background-image:
    linear-gradient(#1b222d, #1b222d), linear-gradient(315deg, #ee4297, #9176c6);
  background-origin: border-box;
  background-clip: padding-box, border-box;
}
</style>