<template>
  <header class="detail-header">

    <picture class="detail-header__picture">
      <div class="detail-header__cover"></div>
      <img
        :src="this.company.sector.main_header"
        alt="Company background image"
      >
    </picture>

    <div class="detail-header__element">

      <div class="detail-header__breadcrumbs">
        <ul>
          <li>
            <RouterLink to="/">Stocks</RouterLink>
          </li>
          <li>
            <RouterLink to="/">{{ this.company.sector.title }}</RouterLink>
          </li>
        </ul>
      </div>

      <div class="detail-header__logo">
        <img :src="this.company.logo_url" alt="{{ this.company.slug }}">
      </div>

      <div>
        <h1 class="detail-header__company-title">
          {{ this.company.title }}
          <span class="detail-header__company-desc">{{ this.company.market.title }}:{{ this.company.slug.toUpperCase() }} Stock Report</span>
        </h1>
      </div>

    </div>

    <div class="detail-header__element">
      <div class="detail-header__button-list">
        <template v-if="company.is_watchlisted">
          <RoundedBlueButton>
            <SolidStarIcon/>
          </RoundedBlueButton>

          <RoundedBlueButton>
            <PenIcon/>
            <span>Add note</span>
          </RoundedBlueButton>
        </template>

        <template v-else>
          <RoundedBlueButton>
            <OutlineStarIcon/>
            <span>Add to watchlist</span>
          </RoundedBlueButton>
        </template>

        <RoundedWhiteButton>
          <span>Add to portfolio</span>
        </RoundedWhiteButton>

        <RoundedWhiteButton>
          <DotsIcon/>
        </RoundedWhiteButton>
      </div>
    </div>

    <div class="detail-header__element">
      <div class="detail-header__info-grid">

        <CompanyDetailHeaderInfoItem>
          <template v-slot:title>
            <p>Last price</p>
          </template>
          <template v-slot:value>
            <span>₽{{ this.company.price_data.last_price.toFixed(2) }}</span>
          </template>
        </CompanyDetailHeaderInfoItem>

        <CompanyDetailHeaderInfoItem>
          <template v-slot:title>
            <p>Market cap</p>
          </template>
          <template v-slot:value>
            <span>{{ this.humanize_financial_val(this.company.price_data.capitalisation) }}</span>
          </template>
        </CompanyDetailHeaderInfoItem>

        <CompanyDetailHeaderInfoItem>
          <template v-slot:title>
            <p>7D</p>
          </template>
          <template v-slot:value>
            <span :class="[this.company.price_data.return_7d > 0 ? 'detail-header__success-color' : 'detail-header__error-color']">
              {{ this.company.price_data.return_7d.toFixed(2)}}%
            </span>
          </template>
        </CompanyDetailHeaderInfoItem>

        <CompanyDetailHeaderInfoItem>
          <template v-slot:title>
            <p>1Y</p>
          </template>
          <template v-slot:value>
            <span :class="[this.company.price_data.return_1y > 0 ? 'detail-header__success-color' : 'detail-header__error-color']">
              {{ this.company.price_data.return_1y.toFixed(2)}}%
            </span>
          </template>
        </CompanyDetailHeaderInfoItem>

        <SmallPriceChart class="detail-header__info-item">

        </SmallPriceChart>

        <CompanyDetailHeaderInfoItem class="detail-header__info-item--nowrap">
          <template v-slot:title>
            <p>Updated</p>
          </template>
          <template v-slot:value>
            <span class="detail-header__info-item-value--small">
              <template v-if="company.reports.length">
                {{ this.company.reports[0].updated}}
              </template>
              <template v-else>
                n/a
              </template>
            </span>
          </template>
        </CompanyDetailHeaderInfoItem>

        <CompanyDetailHeaderInfoItem class="detail-header__info-item--nowrap">
          <template v-slot:title>
            <p>Data</p>
          </template>
          <template v-slot:value>
            <span class="detail-header__info-item-value--small detail-header__info-item-value--on-row">
              <span>Financials Company</span>
                <template v-if="company.analyst_ideas">
                  <span> + </span>
                  <TextButton>
                    {{ this.totalIdeas }} Analysts
                  </TextButton>
                </template>
            </span>
          </template>
        </CompanyDetailHeaderInfoItem>
      </div>

    </div>
  </header>
</template>

<script lang="ts">
  import TextButton from "@/components/UI/buttons/TextButton.vue";
  import OutlineStarIcon from "@/components/icons/OutlineStarIcon.vue";
  import SolidStarIcon from "@/components/icons/SolidStarIcon.vue";
  import PenIcon from "@/components/icons/PenIcon.vue";
  import DotsIcon from "@/components/icons/DotsIcon.vue";
  import CompanyDetailHeaderInfoItem from "@/components/company_detail/CompanyDetailHeaderInfoItem.vue";
  import RoundedButton from "@/components/UI/buttons/RoundedButton.vue";
  import RoundedBlueButton from "@/components/UI/buttons/RoundedBlueButton.vue";
  import RoundedWhiteButton from "@/components/UI/buttons/RoundedWhiteButton.vue";
  import utils from "@/mixins/utils";
  import SmallPriceChart from "@/components/charts/SmallPriceChart.vue";

  export default {
    name: 'CompanyDetailHeader',
    components: {
      SmallPriceChart,
      RoundedWhiteButton,
      RoundedBlueButton,
      RoundedButton,
      CompanyDetailHeaderInfoItem,
      DotsIcon,
      PenIcon,
      SolidStarIcon,
      OutlineStarIcon,
      TextButton
    },
    props: {
      company: {
        type: Object,
        required: true,
      },
    },
    methods: {
    },
    computed: {
      totalIdeas() {
        return this.company.analyst_ideas.length
      }
    },
    mixins: [utils,],
  }
</script>

<style scoped>
  .detail-header {
    border-radius: 0 0 8px 8px;
    margin-bottom: 16px;
    padding: 16px 32px;
    background-color: #1b222d;
    background-position: center;
    background-size: cover;
    position: relative;
    z-index: 1;
    min-height: 166px;
    display: flex;
    flex-flow: wrap;
    justify-content: left;
  }
  .detail-header__picture {
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 0;
  }
  .detail-header__cover {
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 1;
    background: rgba(21, 27, 36, .7);
  }
  .detail-header__picture img {
    border-radius: 0 0 8px 8px;
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  .detail-header__element {
    position: relative;
    width: 100%;
    max-width: 100%;
    flex: 0 0 100%;
  }
  .detail-header__breadcrumbs {
    margin-bottom: 2.4rem;
  }
  .detail-header__breadcrumbs ul {
    font-size: 1.6rem;
  }
  .detail-header__breadcrumbs li {
    position: relative;
    display: inline-block;
    padding-right: .8rem;
  }
  .detail-header__breadcrumbs li:nth-child(2n)::before {
    content: '/';
    padding-right: .8rem;
  }
  .detail-header__breadcrumbs a {
    font-size: 1.4rem;
    text-decoration: underline;
    line-height: 1.5;
  }
  .detail-header__logo {
    margin: 4px 12px 0 8px;
    float: left;
    background-color: #fff;
    border-radius: 8px;
  }
  .detail-header__logo img {
    width: 56px;
    height: 56px;
    min-width: 56px;
    min-height: 56px;
    border: 1px solid #fff;
    border-radius: 8px;
    object-fit: scale-down;
    vertical-align: text-bottom;
  }
  .detail-header__company-title {
    font-size: 3.6rem;
    line-height: 1.25;
    font-weight: 500;
    margin: 0 0 14px;
    overflow: hidden;
  }
  .detail-header__company-desc {
    display: block;
    font-size: 1.6rem;
    line-height: 1.5;
    color: rgba(255, 255, 255, .7);
  }
  .detail-header__button-list {
    width: 100%;
    display: flex;
    gap: 4px;
    justify-content: flex-end;
    text-align: right;
    margin-top: -30px;
    height: 32px;
  }
  .detail-header__info-grid {
    padding-left: 76px;
    display: grid;
    grid-template: 52px / repeat(4, min-content) 2fr 1fr 1fr;
  }
</style>
