<template>
<div class="detail-sidebar">
  <section class="detail-sidebar__inner">

    <header ref="sidebar_header" class="detail-sidebar__header">
      <div class="detail-sidebar__snowflake">
        <div class="detail-sidebar__logo">
          <img
            :src="company.logo_url"
            :alt="company.slug"
          >
        </div>
      </div>
    </header>

    <main ref="sidebar_main" class="detail-sidebar__main">
      <p class="detail-sidebar__title">
        {{ company.title }}
          <CopyIcon class="detail-sidebar__copy-icon" @click="addToClipBoard"/>
      </p>
        <h3 class="detail-sidebar__text">{{ company.market.title }}:{{ company.slug.toUpperCase() }} Stock Report</h3>
        <p class="detail-sidebar__text detail-sidebar__text--small">
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

          <RoundedWhiteButton>
            <DotsIcon/>
          </RoundedWhiteButton>
        </section>
    </main>

    <footer class="detail-sidebar__footer">
      <nav class="detail-sidebar__navigation">
        <ul>
          <li
              class="detail-sidebar__list-item"
              :class="{'detail-sidebar__list-item--active': header === activeHeader}"
              v-once
              v-for="header in contentListHeaders"
              :key="header"
          >
            {{ header }}
          </li>
        </ul>
      </nav>
    </footer>

  </section>
</div>
</template>

<script lang="ts">
 import utils from "@/mixins/utils";
 import CopyIcon from "@/components/icons/CopyIcon.vue";
 import PenIcon from "@/components/icons/PenIcon.vue";
 import RoundedWhiteButton from "@/components/UI/buttons/RoundedWhiteButton.vue";
 import RoundedBlueButton from "@/components/UI/buttons/RoundedBlueButton.vue";
 import OutlineStarIcon from "@/components/icons/OutlineStarIcon.vue";
 import SolidStarIcon from "@/components/icons/SolidStarIcon.vue";
 import DotsIcon from "@/components/icons/DotsIcon.vue";
 import {mapActions, mapGetters, mapMutations, mapState} from "vuex";
 import MiniLoader from "@/components/UI/MiniLoader.vue";
 import {toast} from "vue3-toastify";

export default {
  name: 'CompanyDetailSidebar',
  components: {
    MiniLoader,
    DotsIcon,
    SolidStarIcon,
    OutlineStarIcon,
    RoundedBlueButton,
    RoundedWhiteButton,
    PenIcon,
    CopyIcon
  },
  computed: {
    ...mapState({
     company: state => state.companyDetail.company,
     isAuthenticated: state => state.isAuthenticated,
    }),
    ...mapGetters({
     watchlistIsLoading: "companyDetail/getWatchlistIsLoading",
     portfolioIsLoading: "companyDetail/getPortfolioIsLoading",
     sidebarIsVisible: "companyDetail/getSidebarIsVisible",
    })
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
    addToClipBoard() {
      navigator.clipboard.writeText(location.href)
        .then(() => {
            toast.success('Link Copied')
        })
        .catch(err => {console.log(err)})
    },
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
    changeSidebarOpacity() {
      const opacity = this.calculateSidebarOpacity()
      const sidebar_header = this.$refs.sidebar_header
      const sidebar_body = this.$refs.sidebar_main

      sidebar_header.style.setProperty('opacity', opacity)
      sidebar_body.style.setProperty('opacity', opacity)

      if (opacity === 0) {
        sidebar_header.style.setProperty('visibility', 'hidden')
        sidebar_body.style.setProperty('visibility', 'hidden')
      } else {
        sidebar_header.style.setProperty('visibility', 'visible')
        sidebar_body.style.setProperty('visibility', 'visible')
      }
    },
    calculateSidebarOpacity(): Number {
      const scrollVisible = 25
      const scrollHidden = 200
      const scrollY = window.scrollY
      let opacity = 0

      if (scrollY < scrollHidden && scrollY > scrollVisible) {
        opacity = (scrollY - scrollVisible) /  (scrollHidden - scrollVisible)
        return opacity
      }
      if (scrollY <= scrollVisible) {
        opacity = 0
        return opacity
      }
      if (scrollY >= scrollHidden) {
        opacity = 1
        return opacity
      }
      return opacity
    },
  },
  mixins: [utils,],
  data() {
   return {
     activeHeader: 'Company Overview',
     contentListHeaders: [
       'Company Overview',
       '1 Valuation',
       '2 Future Growth',
       '3 Past Performance',
       '4 Financial Health',
       '5 Dividend',
       '6 Management',
       '7 Ownership',
       'Other Information'
    ]
   }
  },
  mounted() {
    window.addEventListener('scroll', this.changeSidebarOpacity)
  },
  unmounted() {
    window.removeEventListener('scroll', this.changeSidebarOpacity)
  },
 }
</script>

<style scoped>
  .detail-sidebar {
    position: relative;
    width: 100%;
    min-height: 0;
    flex: 0 0 25%;
    max-width: 25%;
  }
  .detail-sidebar__inner {
    position: fixed;
    top: 80px;
    width: 298px;
    padding: 8px 24px 0 0;
  }
  .detail-sidebar__header {
    padding-bottom: 8px;
    visibility: hidden;
    opacity: 0;
  }
  .detail-sidebar__snowflake {
    margin: -18px -8px;
    max-width: 160px;
    padding-bottom: 16px;
  }
  .detail-sidebar__logo {
    margin: 4px 12px 0 8px;
    float: left;
    background-color: #fff;
    border-radius: 8px;
  }
  .detail-sidebar__logo img {
    width: 160px;
    height: 160px;
    padding: 11%;
  }
  .detail-sidebar__main {
    padding-bottom: 16px;
    visibility: hidden;
    opacity: 0;
  }
  .detail-sidebar__footer {
    position: fixed;
    top: 375px;
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
  .detail-sidebar__text--small {
    font-size: 1.2rem;
  }
  .detail-sidebar__navigation {
    width: 298px;
    margin: -20px 0 0 -16px;
  }
  .detail-sidebar__list-item {
    cursor: pointer;
    width: 267px;
    position: relative;
    border-radius: 4px;
    color: rgba(255, 255, 255, .5);
    padding: 4px 0 4px 12px;
    margin-left: 14px;
    line-height: 1.5;
    font-size: 1.6rem;
  }
  .detail-sidebar__list-item:hover {
    background-color: #1b222d;
  }
  .detail-sidebar__list-item--active {
    color: #fff;
    background-color: #1b222d;
  }
  .detail-sidebar__list-item--active::before {
    content: "";
    display: block;
    position: absolute;
    width: 4px;
    height: 100%;
    top: 0;
    background-color: var(--blue);
    border-radius: 4px;
    margin-left: -12px;
  }
</style>