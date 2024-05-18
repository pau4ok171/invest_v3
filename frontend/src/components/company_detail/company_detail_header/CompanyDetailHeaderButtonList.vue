<script lang="ts">
import {defineComponent} from 'vue'
import DotsIcon from "@/components/icons/DotsIcon.vue";
import RoundedWhiteButton from "@/components/UI/buttons/RoundedWhiteButton.vue";
import PenIcon from "@/components/icons/PenIcon.vue";
import OutlineStarIcon from "@/components/icons/OutlineStarIcon.vue";
import SolidStarIcon from "@/components/icons/SolidStarIcon.vue";
import RoundedBlueButton from "@/components/UI/buttons/RoundedBlueButton.vue";
import {mapActions, mapGetters, mapMutations, mapState} from "vuex";
import CompanyDetailPortfolioModalMenu
  from "@/components/company_detail/summary/portfolio/CompanyDetailPortfolioModalMenu.vue";
import MiniLoader from "@/components/UI/MiniLoader.vue";
import BaseModalMenuContainer from "@/components/UI/modal_menu/BaseModalMenuContainer.vue";
import TheCompanyDetailHeaderMoreDropDownMenu
  from "@/components/company_detail/company_detail_header/TheCompanyDetailHeaderMoreDropDownMenu.vue";
import DropDownMenuBox from "@/components/UI/DropDownMenuBox.vue";


export default defineComponent({
  name: "CompanyDetailHeaderButtonList",
  components: {
    DropDownMenuBox,
    TheCompanyDetailHeaderMoreDropDownMenu,
    BaseModalMenuContainer,
    MiniLoader,
    CompanyDetailPortfolioModalMenu,
    RoundedBlueButton,
    SolidStarIcon,
    OutlineStarIcon,
    PenIcon,
    RoundedWhiteButton,
    DotsIcon
  },
  methods: {
    ...mapActions({
      toggleToWatchlist: dispatch => dispatch('companyDetail/toggleToWatchlist')
    }),
    ...mapMutations({
      setNotesModalMenuIsOpen: "companyDetail/setNotesModalMenuIsOpen",
      setPortfolioModalMenuIsOpen: "companyDetail/setPortfolioModalMenuIsOpen",
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
  computed: {
    ...mapState({
      isAuthenticated: 'authModule/isAuthenticated',
    }),
    ...mapGetters({
      company: 'companyDetail/getCompany',
      portfolioModalMenuIsOpen: "companyDetail/getPortfolioModalMenuIsOpen",
      watchlistIsLoading: "companyDetail/getWatchlistIsLoading",
      portfolioIsLoading: "companyDetail/getPortfolioIsLoading",
    }),
  },
})
</script>

<template>
<div class="detail-header__button-list">

  <template v-if="company.is_watchlisted">
    <RoundedBlueButton :disabled="!isAuthenticated || watchlistIsLoading" @click="toggleToWatchlist">
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

  <BaseModalMenuContainer>
    <template #button>
      <RoundedWhiteButton :disabled="!isAuthenticated" @click="setPortfolioModalMenuIsOpen(true)">
        <span>Add to portfolio</span>
      </RoundedWhiteButton>
    </template>

    <template #menu="menuProps">
      <CompanyDetailPortfolioModalMenu @closeMenu="menuProps.close()" v-if="isAuthenticated"/>
    </template>
  </BaseModalMenuContainer>

  <DropDownMenuBox>
    <template #button>
      <RoundedWhiteButton><DotsIcon/></RoundedWhiteButton>
    </template>
    <template #menu>
      <TheCompanyDetailHeaderMoreDropDownMenu/>
    </template>
  </DropDownMenuBox>

</div>
</template>

<style scoped>
.detail-header__button-list {
  width: 100%;
  display: flex;
  gap: 4px;
  justify-content: flex-end;
  text-align: right;
  margin-top: -30px;
  height: 32px;
}
</style>