<script lang="ts">
import {defineComponent} from 'vue'
import DotsIcon from "@/components/icons/DotsIcon.vue";
import RoundedWhiteButton from "@/components/UI/buttons/RoundedWhiteButton.vue";
import PenIcon from "@/components/icons/PenIcon.vue";
import OutlineStarIcon from "@/components/icons/OutlineStarIcon.vue";
import SolidStarIcon from "@/components/icons/SolidStarIcon.vue";
import RoundedBlueButton from "@/components/UI/buttons/RoundedBlueButton.vue";
import axios from "axios";
import {mapActions, mapMutations, mapState} from "vuex";

export default defineComponent({
  name: "CompanyDetailHeaderButtonList",
  components: {RoundedBlueButton, SolidStarIcon, OutlineStarIcon, PenIcon, RoundedWhiteButton, DotsIcon},
  methods: {
    ...mapActions({
      toggleToWatchlist: dispatch => dispatch('companyDetail/toggleToWatchlist')
    }),
    ...mapMutations({
      setNotesModalMenuIsOpen: "companyDetail/setNotesModalMenuIsOpen",
    }),
  },
  computed: {
    ...mapState({
      company: state => state.companyDetail.company,
    }),
  },
})
</script>

<template>
  <div class="detail-header__button-list">

    <template v-if="company.is_watchlisted">
      <RoundedBlueButton @click="toggleToWatchlist">
        <SolidStarIcon/>
      </RoundedBlueButton>

      <RoundedBlueButton @click="setNotesModalMenuIsOpen(true)">
        <PenIcon/>
        <span>Add note</span>
      </RoundedBlueButton>
    </template>

    <template v-else>
      <RoundedBlueButton @click="toggleToWatchlist">
        <OutlineStarIcon/>
        <span>Add to watchlist</span>
      </RoundedBlueButton>
    </template>

    <RoundedWhiteButton><span>Add to portfolio</span></RoundedWhiteButton>

    <RoundedWhiteButton><DotsIcon/></RoundedWhiteButton>

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