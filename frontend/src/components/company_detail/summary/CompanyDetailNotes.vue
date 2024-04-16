<script lang="ts">
import {defineComponent} from 'vue'
import CompanyDetailSection from "@/components/company_detail/CompanyDetailSection.vue";
import CompanyDetailContentGroup from "@/components/company_detail/CompanyDetailContentGroup.vue";
import BookIcon from "@/components/icons/BookIcon.vue";
import RoundedDarkBlueButton from "@/components/UI/buttons/RoundedDarkBlueButton.vue";
import PenIcon from "@/components/icons/PenIcon.vue";
import DetailSectionTitle from "@/components/UI/text/DetailSectionTitle.vue";
import DetailSectionText from "@/components/UI/text/DetailSectionText.vue";

export default defineComponent({
  name: "CompanyDetailNotes",
  components: {
    DetailSectionText,
    DetailSectionTitle,
    PenIcon, RoundedDarkBlueButton, BookIcon, CompanyDetailContentGroup, CompanyDetailSection}
})
</script>

<template>
  <CompanyDetailSection>
    <CompanyDetailContentGroup>

      <header class="detail-notes">
        <DetailSectionTitle>My Notes</DetailSectionTitle>
        <mark class="detail-notes__mark">0</mark>
      </header>

      <div class="detail-notes__empty">
        <BookIcon class="detail-notes__empty-image"/>
        <DetailSectionText>Capture your thoughts, links and company narrative</DetailSectionText>
        <RoundedDarkBlueButton>
          <PenIcon/>
          <span>Add note</span>
        </RoundedDarkBlueButton>
      </div>

    </CompanyDetailContentGroup>
  </CompanyDetailSection>
</template>

<style scoped>
  .detail-notes {
    display: grid;
    gap: 8px;
    grid-template-columns: auto auto 1fr;
    justify-content: start;
    align-items: center;
    margin-bottom: 8px;
  }
  .detail-notes__mark {
    font-size: 1.4rem;
    border-radius: 8px;
    background-color: #262e3a;
    margin: 0 4px 8px;
    padding: 2px 8px;
    color: inherit;
    white-space: nowrap;
  }
  .detail-notes__empty {
    display: grid;
    gap: 8px;
    grid-template-columns: repeat(1, 1fr);
    grid-template-rows: auto auto auto;
    justify-items: center;
    align-content: center;
    max-height: 164px;
    margin-bottom: 8px;
  }
  .detail-notes__empty-image {
    width: 64px;
    height: 66px;
    fill: none;
    transform: translateY(4px);
  }
</style>