<script lang="ts">
import {defineComponent} from 'vue'
import OutlineStarIcon from "@/components/icons/OutlineStarIcon.vue";
import SolidStarIcon from "@/components/icons/SolidStarIcon.vue";
import RoundedBlueButton from "@/components/UI/buttons/RoundedBlueButton.vue";
import MiniLoader from "@/components/UI/MiniLoader.vue";
import PenIcon from "@/components/icons/PenIcon.vue";
import {mapActions, mapGetters, mapMutations} from "vuex";

export default defineComponent({
  name: "CompanyDetailHeaderToggleToWatchlist",
  components: {PenIcon, MiniLoader, RoundedBlueButton, SolidStarIcon, OutlineStarIcon},
  computed: {
    ...mapGetters({
      isAuthenticated: 'authModule/getIsAuthenticated',
      company: 'companyDetail/getCompany',
      watchlistIsLoading: "companyDetail/getWatchlistIsLoading",
    }),
  },
  methods: {
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
})
</script>

<template>
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
</template>
