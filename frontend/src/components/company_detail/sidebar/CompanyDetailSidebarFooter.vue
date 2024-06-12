<script lang="ts">
import {defineComponent} from 'vue'

interface Section {
 name: string,
 key: string,
}

export default defineComponent({
  name: "CompanyDetailSidebarFooter",
  data() {
    return {
      sections: [
        {key: 'overview', name: 'Company Overview'},
        {key: 'value', name: '1 Valuation'},
        {key: 'future', name: '2 Future Growth'},
        {key: 'past', name: '3 Past Performance'},
        {key: 'health', name: '4 Financial Health'},
        {key: 'dividend', name: '5 Dividend'},
        {key: 'management', name: '6 Management'},
        {key: 'owners', name: '7 Ownership'},
        {key: 'other', name: 'Other Information'},
      ] as Array<Section>,
      activeSection: 'overview',
      previousSection: 'overview',
      nextSection: 'overview',
    }
  },
  methods: {
    changeSection(section: Section) {
      this.activeSection = section.key
      this.previousSection = section.key
      this.nextSection = section.key
      const goTo = (document as any).querySelector(`#${section.key}`).getBoundingClientRect()
      const windowScroll = document.documentElement.scrollTop
      const scrollTop = goTo.top + windowScroll - 80
      window.scrollTo({top: scrollTop})
    },
  },
  mounted() {
    const observer = new IntersectionObserver((entries) => {
      const entry = entries[0]
      if (entry.intersectionRatio > 0) {
        this.previousSection = entry.boundingClientRect.top >= 0 ? this.activeSection: this.previousSection
        this.activeSection = entry.target.getAttribute('id') as string
        this.previousSection = entry.boundingClientRect.top < 0 ? this.activeSection: this.previousSection
        this.nextSection = entry.boundingClientRect.top >= 0 ? this.activeSection : this.nextSection
      } else {
        if (entry.boundingClientRect.top < 0) {
          this.activeSection = this.nextSection
        } else {
          this.activeSection = this.previousSection
        }
      }
    })
    document.querySelectorAll('.section_observer').forEach((section) => {
          observer.observe(section)
        },
        {
          rootMargin: '-50% 0px -50% 0px',
          threshold: [.1],
        }
    )
  },
})
</script>

<template>
<footer class="detail-sidebar__footer">
  <nav class="detail-sidebar__navigation">
    <ul>
      <li
        class="detail-sidebar__list-item"
        :class="{'detail-sidebar__list-item--active': section.key === activeSection}"
        v-for="section in sections"
        :key="section.key"
        @click="changeSection(section)"
      >
        {{ section.name }}
      </li>
    </ul>
  </nav>
</footer>
</template>

<style scoped>
.detail-sidebar__footer {
  position: fixed;
  top: 375px;
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