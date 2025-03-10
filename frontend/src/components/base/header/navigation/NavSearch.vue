<script lang="ts">
import axios from "axios";
import { defineComponent } from "vue";
import type { SearchCompany } from "@/types/invest";
import { BaseIcon } from "@/apps/visagiste/components/BaseIcon";
import BaseButton from "@/apps/visagiste/components/BaseButton/BaseButton.vue";
import BaseDialog from "@/apps/visagiste/components/BaseDialog/BaseDialog.vue";
import BaseCard from "@/apps/visagiste/components/BaseCard/BaseCard.vue";
import BaseTextField from "@/apps/visagiste/components/BaseTextField/BaseTextField.vue";
import BaseCardText from "@/apps/visagiste/components/BaseCard/BaseCardText.vue";
import BaseListItemSubheader from "@/apps/visagiste/components/BaseList/BaseListItemSubheader.vue";
import BaseList from "@/apps/visagiste/components/BaseList/BaseList.vue";
import BaseListItem from "@/apps/visagiste/components/BaseList/BaseListItem.vue";
import BaseListItemTitle from "@/apps/visagiste/components/BaseList/BaseListItemTitle.vue";
import BaseListItemSubtitle from "@/apps/visagiste/components/BaseList/BaseListItemSubtitle.vue";
import BaseFlag from "@/apps/visagiste/components/BaseFlag/BaseFlag.vue";
import BaseChip from "@/apps/visagiste/components/BaseChip/BaseChip.vue";

export default defineComponent({
  name: "NavSearch",
  components: {
    BaseChip,
    BaseFlag,
    BaseListItemSubtitle,
    BaseListItemTitle,
    BaseListItem,
    BaseList,
    BaseListItemSubheader,
    BaseCardText,
    BaseTextField,
    BaseCard,
    BaseDialog,
    BaseButton,
    BaseIcon,
  },
  data() {
    return {
      searchResponse: [] as SearchCompany[],
      model: false,
      timeoutId: -1
    };
  },
  methods: {
    onUpdate(v: string) {
      clearTimeout(this.timeoutId)

      this.timeoutId = setTimeout(() => this.getSearchResults(v), 600)
    },
    onKeydown(e: KeyboardEvent) {
      if (e.key === 'k' && e.ctrlKey && !e.altKey && !e.shiftKey &&!e.metaKey) {
        e.stopPropagation()
        e.preventDefault()

        this.model = !this.model
      }
    },
    async getSearchResults (v: string) {
      if (!v.length) {
        this.searchResponse = []
        return
      }

      await axios
        .get('/api/v1/invest/search_query/', {
          params: { query: v }
        })
        .then((response) => {
          this.searchResponse = this.highlightSearchResponse(response.data, v)
        })
        .catch((err) => {
          console.log(err);
        })
    },
    highlightSearchResponse(searchResponse: SearchCompany[], query: string) {
      const regex = new RegExp(query, "gi");
      return searchResponse.map((c) => {
        c.title = c.title.replace(
          regex,
          `<span class="mask__highlight">$&</span>`,
        );
        c.ticker = c.ticker.replace(
          regex,
          `<span class="mask__highlight">$&</span>`,
        );
        return c;
      });
    },
  },
  watch: {
    model(val) {
      if (val === false) {
        this.searchResponse = []
      }
    }
  },
  mounted () {
    document.addEventListener('keydown', this.onKeydown)
  },
  unmounted () {
    document.removeEventListener('keydown', this.onKeydown)
  }
});
</script>

<template>
  <base-dialog v-model="model" width="600">
    <template #activator="{ props: activatorProps }">
      <base-button
        v-bind="activatorProps"
        prepend-icon="$iSearch"
        variant="text"
        class="text-body-2 text-capitalize px-3"
      >
        <span class="me-n1">
          <span>Search</span>
          <span class="py-1 px-2 ms-2 border rounded text-disabled text-caption">Ctrl+K</span>
        </span>
      </base-button>
    </template>
    <template #default>
      <base-card>
        <base-text-field
          class="mb-4"
          prepend-inner-icon="$iSearch"
          placeholder="Looking for..."
          single-line
          persistent-placeholder
          hide-details
          @update:modelValue="onUpdate"
          :autofocus="true"
        >
          <template #append-inner>
            <base-button
              size="small"
              border
              class="text-medium-emphasis text-body-2 text-capitalize px-3"
              variant="text"
              @click="model = false"
            >
              <span class="text-caption text-disabled">Esc</span>
            </base-button>
          </template>
        </base-text-field>

        <base-card-text
          v-if="!searchResponse.length"
          class="px-4 py-0 mb-4 d-flex flex-wrap justify-center align-center"
        >
          <div class="text-center">
            <base-icon
              class="text-disabled mb-6 mx-auto"
              size="150"
              icon="$iSearchList"
            />
            <base-list-item-subheader
              title="Your search results will appear here"
            />
          </div>
        </base-card-text>

        <base-list v-else>
          <base-list-item
            v-for="item in searchResponse"
            :key="item.uid"
            :to="item.absolute_url"
            @click="model = false"
          >
            <template #prepend>
              <base-flag :code="item.country.slug"/>
            </template>
            <template #default>
              <base-list-item-title v-html="item.title"/>
              <base-list-item-subtitle v-html="item.ticker"/>
            </template>
            <template #append>
              <base-chip :text="item.sector.title" label color="info" size="small" />
            </template>
          </base-list-item>
        </base-list>
      </base-card>
    </template>
  </base-dialog>
</template>

<style>
.mask__highlight {
  background-color: yellow;
  color: black;
}
</style>