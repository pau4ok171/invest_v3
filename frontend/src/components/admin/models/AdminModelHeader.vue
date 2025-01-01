<script lang="ts">
import {defineComponent} from 'vue'
import AdminModelIndicator from "@/components/admin/models/AdminModelIndicator.vue";
import {mapState} from "vuex";
import {DateTime} from "luxon";
import {toast} from "vue3-toastify";
import BaseModalMenuContainer from "@/components/UI/modal_menu/BaseModalMenuContainer.vue";
import BaseModalMenu from "@/components/UI/base/BaseModalMenu.vue";
import {useAdminStore} from "@/store/admin";
import BaseButton from "@/components/UI/base/components/BaseButton/BaseButton.vue";

export default defineComponent({
  name: "AdminModelHeader",
  components: {
    BaseButton,
    BaseModalMenu,
    BaseModalMenuContainer,
    AdminModelIndicator,
  },
  setup:() => ({store: useAdminStore()}),
  methods: {
    getURLFromFile(image: File): string {
      try {
        return URL.createObjectURL(image)
      } catch {
        return ''
      }
    },
    getFormattedDate(isoDateTime: string) {
      return DateTime.fromISO(isoDateTime).toFormat('dd LLL yyyy TT')
    },
    copyValue(event: MouseEvent) {
      const target = event.target as HTMLHtmlElement
      navigator.clipboard.writeText(target.innerText).then(() => toast.success('Value Copied')).catch(err => console.log(err))
    },
  },
  computed: {
    ...mapState({
      userInfo: (state: any) => state.authModule.userInfo,
    }),
    getModerFullName() {
      if (this.store.companyFormData.updatedBy.lastName.length) {
        return `${this.store.companyFormData.updatedBy.lastName} ${this.store.companyFormData.updatedBy.firstName}`
      }
      if (this.store.companyFormData.createdBy.lastName.length) {
        return `${this.store.companyFormData.createdBy.lastName} ${this.store.companyFormData.createdBy.firstName}`
      }
      return `${this.userInfo.last_name} ${this.userInfo.first_name}`
    },
    getNameOfModification() {
      if (!this.store.companyUID.length) {
        return 'Creating by:'
      }
      if (this.store.companyFormData.updatedBy.lastName.length) {
        return 'Modified by:'
      }
      return 'Created by:'

    },
  },
})
</script>

<template>
<div class="admin-model__admin-model-header">
  <div>
    <div class="admin-model-header__breadcrumbs">
      {{ store.companyFormData.sector.slug?store.companyFormData.sector.name:'Sector'  }}
      /
      {{ store.companyFormData.industry.slug?store.companyFormData.industry.name:'Industry' }}
    </div>
    <div class="admin-model-header__block-company-name">
      <div class="admin-header__logo-wrapper">
        <img class="admin-header__logo" :src="getURLFromFile(store.companyFormData.logo)" alt="LOGO" v-if="store.companyFormData.logo?.size">
        <span class="admin-header__logo-text" v-else>Logo</span>
      </div>
      <div>
        <div class="admin-model-header__company-name">{{ store.companyFormData.companyName?store.companyFormData.companyName:'Company Name' }}</div>
        <div class="admin-model-header__ticker">
          <span>{{ store.companyFormData.market.slug?store.companyFormData.market.slug.toUpperCase():'Market' }}</span>
          <span>:</span>
          <span>{{ store.companyFormData.ticker?store.companyFormData.ticker:'Ticker' }}</span>
        </div>
      </div>
    </div>

    <div
        v-tippy="{content: 'Click to copy UID', theme: 'tooltip-theme-paper', appendTo: 'parent', arrow: false}"
        class="admin-model-header__item admin-model-header__item--tooltip"
        @click="copyValue"
    >
      {{ store.companyFormData.uid?store.companyFormData.uid:'0000-0000-0000-0000' }}
    </div>
    <div class="admin-model-header__item">
      <img class="admin-model-header__country-flag-icon" :src="store.companyFormData.country.flagURL" alt="Country" v-if="store.companyFormData.country.flagURL">
      {{ store.companyFormData.country.slug?store.companyFormData.country.name:'Country' }}
    </div>
    <div class="admin-model-header__item">{{ store.companyFormData.country.currency?.name?`${store.companyFormData.country.currency.name} (${store.companyFormData.country.currency.symbol})`:'Currency Symbol' }}</div>
  </div>
  <div class="admin-model-header__last-column">
    <div class="admin-model-header__indicator">
      <AdminModelIndicator :is-active="store.companyFormData.isVisible"/>
    </div>

    <div class="admin-model-header__last-column-info">
      <div class="admin-model-header__item">Created: {{ store.companyFormData.created?getFormattedDate(store.companyFormData.created):'00.00.0000 00:00:00' }}</div>
      <div class="admin-model-header__item">Updated: {{ store.companyFormData.updated?getFormattedDate(store.companyFormData.updated):'00.00.0000 00:00:00' }}</div>
      <div class="admin-model-header__item">
        <div class="admin-model-header__item-modified-by">
          <div class="admin-model-header__item-modified-by-title" v-text="getNameOfModification"></div>
          <div class="admin-model-header__item-modified-by-value" v-text="getModerFullName"></div>
        </div>
      </div>
    </div>

    <div class="admin-model-header__action-list">
      <template v-if="!store.editModeActivated">
        <div class="admin-model-header__item">
          <base-button
            theme="dark-blue"
            prepend-icon="EditIcon"
            text="edit"
            rounded="large"
            @click="store.activateEditMode()"
          />
        </div>
        <BaseModalMenuContainer>
          <template #button>
          <div class="admin-model-header__item">
            <base-button
              theme="error"
              prepend-icon="DeleteIcon"
              text="delete"
              rounded="large"
              :disabled="store.isNewModel"
            />
          </div>
          </template>
          <template #menu="menuProps">
            <BaseModalMenu @closeMenu="menuProps.close()">
              <template #title>Confirm the action</template>
              <template #content>
                <div class="admin-model-modal-menu__content">
                  <div class="admin-model-modal-menu__description">
                    Are you sure to definitely delete the current model?
                  </div>
                  <div class="admin-model-modal-menu__actions">
                    <base-button
                        text="Yes, I want to delete"
                        theme="error"
                        size="small"
                        rounded="large"
                        @click="store.deleteModel()"
                    />
                    <base-button
                        text="No"
                        theme="dark-blue"
                        size="small"
                        rounded="large"
                        @click="menuProps.close()"
                    />
                  </div>
                </div>
              </template>
            </BaseModalMenu>
          </template>
        </BaseModalMenuContainer>
      </template>
      <template v-else>
        <div class="admin-model-header__item">
          <base-button
            prepend-icon="ResetIcon"
            text="Close Edit Mode Without Saving"
            theme="dark-blue"
            rounded="large"
            size="small"
            @click="store.deactivateEditMode()"
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
  margin-bottom: 2.4rem;
  font-size: 1.4rem;
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
  font-size: 1.4rem;
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
  font-size: 2.8rem;
  line-height: 1.25;
  font-weight: 500;
  overflow: hidden;
}
.admin-model-header__ticker {
  font-size: 1.6rem;
  line-height: 1.5;
  color: rgba(255, 255, 255, .7);
}
.admin-model-header__item {
  font-size: 1.4rem;
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
  background-image: linear-gradient(#1b222d, #1b222d), linear-gradient(315deg, #ee4297, #9176c6);
  background-origin: border-box;
  background-clip: padding-box, border-box;
}
.admin-model-modal-menu__content {
  padding: 16px;
}
.admin-model-modal-menu__description {
  font-size: 1.6rem;
  line-height: 1.7;
  margin-bottom: 24px;
}
.admin-model-modal-menu__actions {
  display: flex;
  justify-content: end;
  gap: 4px;
  margin-right: 20px;
}
</style>