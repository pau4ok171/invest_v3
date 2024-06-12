<script lang="ts">
import {defineComponent} from 'vue'
import OutlineStarIcon from "@/components/icons/OutlineStarIcon.vue";
import SolidStarIcon from "@/components/icons/SolidStarIcon.vue";
import TheCompanyDetailHeaderMoreDropDownMenu
  from "@/components/company_detail/header/TheCompanyDetailHeaderMoreDropDownMenu.vue";
import DropDownMenuBox from "@/components/UI/DropDownMenuBox.vue";
import RoundedBlueButton from "@/components/UI/buttons/RoundedBlueButton.vue";
import RoundedWhiteButton from "@/components/UI/buttons/RoundedWhiteButton.vue";
import DotsIcon from "@/components/icons/DotsIcon.vue";
import MiniLoader from "@/components/UI/MiniLoader.vue";
import CopyIcon from "@/components/icons/CopyIcon.vue";
import PenIcon from "@/components/icons/PenIcon.vue";
import {mapActions, mapGetters, mapMutations} from "vuex";
import {toast} from "vue3-toastify";
import utils from "@/mixins/utils";

export default defineComponent({
  name: "CompanyDetailSidebarMain",
  components: {
    PenIcon,
    CopyIcon,
    MiniLoader,
    DotsIcon,
    RoundedWhiteButton,
    RoundedBlueButton,
    DropDownMenuBox,
    TheCompanyDetailHeaderMoreDropDownMenu,
    SolidStarIcon,
    OutlineStarIcon
  },
  computed: {
    ...mapGetters({
      company: 'companyDetail/getCompany',
      watchlistIsLoading: "companyDetail/getWatchlistIsLoading",
      isAuthenticated: 'authModule/getIsAuthenticated',
    }),
  },
  methods: {
    addToClipBoard() {
      navigator.clipboard.writeText(location.href)
        .then(() => {
            toast.success('Link Copied')
        })
        .catch(err => {console.log(err)})
    },
    ...mapActions({
      toggleToWatchlist: dispatch => dispatch('companyDetail/toggleToWatchlist')
    }),
    ...mapMutations({
      setNotesModalMenuIsOpen: "companyDetail/setNotesModalMenuIsOpen",
      setNote: 'companyDetail/setNote',
      setNoteSavedContent: "companyDetail/setNoteSavedContent",
    }),
    createNewNote() {
      this.setNote({
        id: null,
        body: null,
        created: null,
        updated: null,
        company: this.company.id,
      })
      this.setNoteSavedContent('')
      this.setNotesModalMenuIsOpen(true)
    },
  },
  mixins: [utils],
})
</script>

<template>
<main class="detail-sidebar__main">
  <p class="detail-sidebar__title">
    {{ company.title }}
      <CopyIcon class="detail-sidebar__copy-icon" @click="addToClipBoard"/>
  </p>
    <h3 v-if="company.market" class="detail-sidebar__text">{{ company.market.title }}:{{ company.slug.toUpperCase() }} Stock Report</h3>
    <p v-if="company.price_data" class="detail-sidebar__text detail-sidebar__text--small">
      Mkt Cap: {{ humanize_financial_val(company.price_data.capitalisation, company.formatting.primaryCurrencySymbol) }}
    </p>

    <section class="detail-sidebar__button-list">
      <template v-if="company.is_watchlisted">
        <RoundedBlueButton :disabled="!isAuthenticated || watchlistIsLoading"  @click="toggleToWatchlist">
          <MiniLoader v-if="watchlistIsLoading"/>
          <SolidStarIcon v-else/>
        </RoundedBlueButton>

        <RoundedBlueButton @click="createNewNote">
          <PenIcon/>
          <span>Add note</span>
        </RoundedBlueButton>
      </template>

      <template v-else>
        <RoundedBlueButton :disabled="!isAuthenticated || watchlistIsLoading" @click="toggleToWatchlist">
          <MiniLoader v-if="watchlistIsLoading"/>
          <OutlineStarIcon v-else/>
          <span>Add to watchlist</span>
        </RoundedBlueButton>
      </template>

      <DropDownMenuBox>
        <template #button>
          <RoundedWhiteButton><DotsIcon/></RoundedWhiteButton>
        </template>
        <template #menu>
          <TheCompanyDetailHeaderMoreDropDownMenu/>
        </template>
      </DropDownMenuBox>
    </section>
</main>
</template>

<style scoped>
.detail-sidebar__main {
  padding-bottom: 16px;
  visibility: hidden;
  opacity: 0;
}
.detail-sidebar__title {
  width: 100%;
  font-size: 1.6rem;
  line-height: 1.5;
  font-weight: 500;
  overflow: hidden;
  text-overflow: ellipsis;
}
.detail-sidebar__copy-icon {
  fill: #fff;
  width: 24px;
  height: 24px;
  cursor: pointer;
  margin-left: 8px;
  transform: translate(0, 6px);
  fill: rgba(140, 146, 155, .5);
}
.detail-sidebar__copy-icon:hover {
  fill: rgb(140, 146, 155);
}
.detail-sidebar__text {
  width: 100%;
  font-size: 1.4rem;
  line-height: 1.5;
  font-weight: 500;
  overflow: hidden;
  text-overflow: ellipsis;
  color: rgba(255, 255, 255, .7);
}
.detail-sidebar__button-list {
  display: flex;
  gap: 4px;
  margin-bottom: 35px;
  margin-top: 12px;
  min-height: 32px;
  position: relative;
  z-index: 1;
}
.detail-sidebar__text--small {
  font-size: 1.2rem;
}
</style>