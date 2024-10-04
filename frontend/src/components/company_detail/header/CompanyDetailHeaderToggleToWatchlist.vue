<script lang="ts">
import {defineComponent} from 'vue'
import {mapActions, mapGetters, mapMutations} from "vuex";
import BaseButton from "@/components/UI/base/BaseButton/BaseButton.vue";

export default defineComponent({
  name: "CompanyDetailHeaderToggleToWatchlist",
  components: {BaseButton},
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
  <base-button
    icon="SolidStarIcon"
    theme="blue"
    rounded="x-small"
    density="compact"
    :loading="watchlistIsLoading"
    :disabled="!isAuthenticated"
    @click="toggleToWatchlist"
  />

  <base-button
    prepend-icon="PenIcon"
    text="Add Note"
    theme="blue"
    rounded="large"
    size="small"
    lower
    @click="createNewNote"
  />
</template>

<template v-else>
  <base-button
    prepend-icon="OutlineStarIcon"
    text="Add to watchlist"
    theme="blue"
    rounded="large"
    size="small"
    lower
    :loading="watchlistIsLoading"
    :disabled="!isAuthenticated"
    @click="toggleToWatchlist"
  />
</template>
</template>
