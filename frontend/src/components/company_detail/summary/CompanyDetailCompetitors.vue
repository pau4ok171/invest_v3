<script lang="ts">
import {defineComponent} from 'vue'
import CompanyDetailSection from "@/components/company_detail/CompanyDetailSection.vue";
import CompanyDetailSnowflakeTable from "@/components/company_detail/summary/CompanyDetailSnowflakeTable.vue";
import SnowflakeChart from "@/components/charts/SnowflakeChart.vue";
import DetailSectionTitle from "@/components/UI/text/DetailSectionTitle.vue";
import {mapState} from "vuex";

export default defineComponent({
  name: "CompanyDetailCompetitors",
  components: {DetailSectionTitle, SnowflakeChart, CompanyDetailSnowflakeTable, CompanyDetailSection},
  computed: {
    ...mapState({
      company: state => state.companyDetail.company,
    }),
  },
})
</script>

<template>
  <CompanyDetailSection>

    <DetailSectionTitle>{{ company.slug.toUpperCase() }} Competitors</DetailSectionTitle>

    <div class="detail-competitors">

      <section class="detail-competitors__item">
        <a class="detail-competitors__link" href="#">
          <div class="detail-competitors__inner">
            <div class="competitors__snowflake">
              <CompanyDetailSnowflakeTable v-if="false"/>
              <SnowflakeChart v-else :chartData="[5, 1, 4, 5, 3]" :isSmall="true"/>
              </div>

              <div class="detail-competitors__info">
                <p class="detail-competitors__info-text">VTB Bank</p>
                <p class="detail-competitors__info-text detail-competitors__info-text--medium">MOEX:VTBR</p>
                <p class="detail-competitors__info-text detail-competitors__info-text--medium detail-competitors__info-text--grey">P244.0b</p>
              </div>
          </div>
        </a>
      </section>

      <section class="detail-competitors__item">
        <a class="detail-competitors__link" href="#">
          <div class="detail-competitors__inner">
            <div class="competitors__snowflake">
              <CompanyDetailSnowflakeTable v-if="false"/>
              <SnowflakeChart v-else :chartData="[2, 5, 2, 5, 0]" :isSmall="true"/>
              </div>

              <div class="detail-competitors__info">
                <p class="detail-competitors__info-text">Credit Bank of Moscow</p>
                <p class="detail-competitors__info-text detail-competitors__info-text--medium">MOEX:CBOM</p>
                <p class="detail-competitors__info-text detail-competitors__info-text--medium detail-competitors__info-text--grey">P164.3b</p>
              </div>
          </div>
        </a>
      </section>

      <section class="detail-competitors__item">
        <a class="detail-competitors__link" href="#">
          <div class="detail-competitors__inner">
            <div class="competitors__snowflake">
              <CompanyDetailSnowflakeTable v-if="false"/>
              <SnowflakeChart v-else :chartData="[1, 0, 3, 4, 0]" :isSmall="true"/>
              </div>

              <div class="detail-competitors__info">
                <p class="detail-competitors__info-text">Rosbank</p>
                <p class="detail-competitors__info-text detail-competitors__info-text--medium">MOEX:ROSB</p>
                <p class="detail-competitors__info-text detail-competitors__info-text--medium detail-competitors__info-text--grey">P172.5b</p>
              </div>
          </div>
        </a>
      </section>

      <section class="detail-competitors__item">
        <a class="detail-competitors__link" href="#">
          <div class="detail-competitors__inner">
            <div class="competitors__snowflake">
              <CompanyDetailSnowflakeTable v-if="false"/>
              <SnowflakeChart v-else :chartData="[0, 0, 1, 4, 2]" :isSmall="true"/>
              </div>

              <div class="detail-competitors__info">
                <p class="detail-competitors__info-text">Avangard Bank</p>
                <p class="detail-competitors__info-text detail-competitors__info-text--medium">MOEX:AVAN</p>
                <p class="detail-competitors__info-text detail-competitors__info-text--medium detail-competitors__info-text--grey">P69.0b</p>
              </div>
          </div>
        </a>
      </section>

    </div>

  </CompanyDetailSection>
</template>

<style scoped>
  .detail-competitors {
    display: flex;
    flex-direction: row;
    flex-wrap: nowrap;
    justify-content: space-between;
    font-size: 1.2rem;
  }
  .detail-competitors__item {
    width: 164px;
    margin-right: 16px;
    text-align: center;
    border-radius: 8px;
    cursor: pointer;
    flex-shrink: 0;
  }
  .detail-competitors__item:hover {
    background-color: #262e3a;
  }
  .detail-competitors__inner {
    padding: 16px;
  }
  .detail-competitors__info {
    padding-right: 10px;
    margin-top: 8px;
  }
  .detail-competitors__info-text {
    font-size: 1.6rem;
    line-height: 1.5;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .detail-competitors__info-text--medium {
    font-size: 1.4rem;
  }
  .detail-competitors__info-text--grey {
    color: rgba(255, 255, 255, .5);
  }

</style>