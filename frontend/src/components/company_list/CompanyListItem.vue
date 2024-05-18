<template>
  <tr>
    <td>
      <RouterLink :to="object.absolute_url" class="company-list__company-link">
        <div class="company-list__company-logo">
            <img
              :src="object.logo_url"
              class="company-list__logo"
              alt="Logo"
            >
        </div>
      </RouterLink>
    </td>
    <td>
       <RouterLink :to="object.absolute_url" class="company-list__company-link">
        <b>{{ object.ticker }}</b>
        <span>{{ object.title }}</span>
      </RouterLink>
    </td>
    <td>
       <RouterLink :to="object.absolute_url" class="company-list__company-link">
         {{ object.formatting.primaryCurrencySymbol }}{{ object.price_data.last_price.toFixed(2) }}
      </RouterLink>
    </td>
    <td :class="[object.price_data.return_7d > 0 ? 'company-list__success-color' : 'company-list__error-color']">
       <RouterLink :to="object.absolute_url" class="company-list__company-link">
        {{ object.price_data.return_7d.toFixed(2) }}%
      </RouterLink>
    </td>
    <td :class="[object.price_data.return_1y > 0 ? 'company-list__success-color' : 'company-list__error-color']">
       <RouterLink :to="object.absolute_url" class="company-list__company-link">
        {{ object.price_data.return_1y.toFixed(2) }}%
      </RouterLink>
    </td>
    <td>
       <RouterLink :to="object.absolute_url" class="company-list__company-link">
        {{ humanize_financial_val(object.price_data.capitalisation, object.formatting.primaryCurrencySymbol) }}
      </RouterLink>
    </td>
    <td>
      <RouterLink :to="object.absolute_url" class="company-list__company-link">
        US$199.23
      </RouterLink>
    </td>
    <td>
       <RouterLink :to="object.absolute_url" class="company-list__company-link">
        PE 28.7x
      </RouterLink>
    </td>
    <td>
       <RouterLink :to="object.absolute_url" class="company-list__company-link">
        E 6.1%
      </RouterLink>
    </td>
    <td>
       <RouterLink :to="object.absolute_url" class="company-list__company-link">
        0.6%
      </RouterLink>

    </td>
    <td class="company-list__sector-cell">
       <RouterLink :to="object.absolute_url" class="company-list__company-link">
         {{ object.sector.title }}
      </RouterLink>
    </td>
    <td>
      <CircledButton
          :disabled="!isAuthenticated"
          @click="toggleToWatchlist(object)"
      >
        <SolidStarIcon :style="{fill: '#fff'}" v-if="object.is_watchlisted"/>
        <OutlineStarIcon v-else/>
      </CircledButton>
    </td>
  </tr>
</template>

<script>
import OutlineStarIcon from "@/components/icons/OutlineStarIcon.vue";
import SolidStarIcon from "@/components/icons/SolidStarIcon.vue";
import CircledButton from "@/components/UI/buttons/CircledButton.vue";
import utils from "@/mixins/utils";
import {mapActions, mapGetters} from "vuex";

export default {
  name: 'CompanyListItem',
  computed: {
    ...mapGetters({
      isAuthenticated: "authModule/getIsAuthenticated"
    }),
  },
  components: {CircledButton, SolidStarIcon, OutlineStarIcon},
  props: {
    object: {
      type: Object,
      required: true,
      sector: Object,
      price_data: Object,
      absolute_url: String,
      logo_url: String,
    }
  },
  methods: {
    ...mapActions({
      toggleToWatchlist: "companyList/toggleToWatchlist",
    }),
  },
  mixins: [utils,],
}
</script>

<style scoped>
.company-list-table tbody tr  {
  font-size: 1.4rem;
  font-weight: normal;
  line-height: 1.5;
  transition: background-color .2s cubic-bezier(.23, 1, .32, 1) 0s;
}
.company-list-table tbody tr:hover {
  background-color: rgba(255, 255, 255, 0.05);
}
.company-list-table td {
  background-color: transparent;
  font-size: 1.4rem;
  height: 64px;
  border-top: none;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  vertical-align: middle;
  padding: 10px 8px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  cursor: pointer;
}
.company-list__error-color {
  color: var(--color-error);
}
.company-list__success-color {
  color: var(--color-success);
}
.company-list__sector-cell {
  width: 64px;
  font-size: 1.4rem;
  color: rgb(35, 148, 223);
}
.company-list__company-logo {
  background-color: #fff;
  border-radius: 100%;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-left: 4px;
}
.company-list__company-logo img {
  height: 100%;
  width: 100%;
}
.company-list__company-link {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
}
.company-list__company-link b {
  color: var(--blue);
}
.company-list__company-link span {
  width: auto;
  max-width: 100%;
  font-size: 1.2rem;
  min-height: 16px;
  user-select: none;
  color: rgba(255, 255, 255, .5);
  border-bottom: 1px dotted rgb(35, 148, 223);
  padding-right: 10px;
}
</style>>