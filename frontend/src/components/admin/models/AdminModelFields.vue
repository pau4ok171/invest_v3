<script setup lang="ts">
// Composables
import { useAdminModelStore } from '@/store/admin/admin'

// Utilities
import { computed, ref, watch, watchEffect } from 'vue'

// Composables
import { useVuelidate } from '@vuelidate/core'

// Types
import type { PropType } from 'vue'
import type {
  EnrichedFormField,
  SelectorItem,
} from '@/components/admin/models/types'
import type { ErrorObject } from '@vuelidate/core'
import type { IFormattedDetailCompany } from '@/types/admin.types'

const props = defineProps({
  items: {
    type: Object as PropType<EnrichedFormField[]>,
    required: true,
  },
})

const rules = computed(() => {
  return props.items.reduce(
    (acc, item) => ({
      ...acc,
      [item.key]: item.validators,
    }),
    {}
  )
})
const store = useAdminModelStore()
const state = computed(() => store.formState)

const v$ = useVuelidate(rules, state, { $rewardEarly: true })
const isReadonly = computed(() => !store.editMode)

const preview = ref()

function resetField(key: keyof IFormattedDetailCompany | '__all__') {
  store.resetField(key)

  if (key === '__all__') {
    v$.value.$reset
  } else {
    v$.value[key].$reset
  }
}

async function save() {
  const isValid = await v$.value.$validate

  if (!isValid) return

  await store.postModel()
}

const getBaseColor = (key: keyof IFormattedDetailCompany) => {
  if (v$.value[key].$invalid && v$.value[key].$dirty) {
    return 'error'
  }

  if (!v$.value[key].$invalid && v$.value[key].$dirty) {
    return 'success'
  }
  return undefined
}

watch(
  () => store.editMode,
  (value: boolean) => {
    if (value) {
      v$.value.$commit
    } else {
      store.resetField('__all__')
      v$.value.$reset
    }
  }
)

watchEffect(() => {
  preview.value = state.value.logo?.type.startsWith('image')
    ? URL.createObjectURL(state.value.logo)
    : undefined
})
</script>

<template>
  <div>
    <v-btn
      :disabled="!store.anyDirty"
      style="right: 16px"
      position="absolute"
      icon="$iReset"
      color="info"
      variant="tonal"
      density="comfortable"
      rounded="lg"
      @click="resetField('__all__')"
      v-tippy="{ content: 'Click to reset all changes' }"
    />

    <template v-for="item in items">
      <v-switch
        class="my-4"
        v-if="item.type === 'checkbox'"
        :key="item.key"
        inset
        :label="item.label"
        color="success"
        density="compact"
        :disabled="isReadonly"
        :model-value="store.formState[item.key]"
        @update:model-value="(val: any) => store.updateField(item.key, val)"
      >
        <template #append>
          <v-btn
            :disabled="!store.previousFormState[item.key]?.isDirty"
            icon="$iReset"
            @click="resetField(item.key)"
            color="info"
            variant="tonal"
            tabindex="-1"
            size="small"
            density="comfortable"
            v-tippy="{ content: 'Click to reset field changes' }"
          />
        </template>
      </v-switch>

      <v-text-field
        color="info"
        :base-color="getBaseColor(item.key)"
        class="my-4 admin-models-fields__field"
        rounded="xl"
        v-if="item.type === 'text'"
        :key="item.key"
        variant="outlined"
        :label="item.label"
        :messages="item.helpText ? [item.helpText] : ''"
        :disabled="isReadonly"
        :model-value="store.formState[item.key]"
        @update:model-value="(val: any) => store.updateField(item.key, val)"
        :error-messages="
          v$[item.key].$errors.map((e: ErrorObject) => e.$message) as string[]
        "
        @blur="
          () => {
            v$[item.key].$commit()
            v$[item.key].$touch()
          }
        "
      >
        <template #append>
          <v-btn
            :disabled="!store.previousFormState[item.key]?.isDirty"
            icon="$iReset"
            @click="resetField(item.key)"
            color="info"
            variant="tonal"
            tabindex="-1"
            size="small"
            density="comfortable"
            v-tippy="{ content: 'Click to reset field changes' }"
          />
        </template>
      </v-text-field>

      <v-textarea
        color="info"
        class="my-4 admin-models-fields__field"
        :base-color="getBaseColor(item.key)"
        rounded="xl"
        v-if="item.type === 'textarea'"
        :key="item.key"
        variant="outlined"
        :label="item.label"
        :messages="item.helpText ? [item.helpText] : ''"
        :disabled="isReadonly"
        :model-value="store.formState[item.key]"
        @update:model-value="(val: any) => store.updateField(item.key, val)"
        :error-messages="
          v$[item.key].$errors.map((e: ErrorObject) => e.$message) as string[]
        "
        @blur="
          () => {
            v$[item.key].$commit()
            v$[item.key].$touch()
          }
        "
        auto-grow
        rows="2"
      >
        <template #append>
          <v-btn
            :disabled="!store.previousFormState[item.key]?.isDirty"
            icon="$iReset"
            @click="resetField(item.key)"
            color="info"
            variant="tonal"
            tabindex="-1"
            size="small"
            density="comfortable"
            v-tippy="{ content: 'Click to reset field changes' }"
          />
        </template>
      </v-textarea>

      <v-select
        color="info"
        class="my-4 admin-models-fields__field"
        rounded="xl"
        :base-color="getBaseColor(item.key)"
        v-if="item.type === 'selector'"
        :key="item.key"
        variant="outlined"
        :messages="item.helpText ? [item.helpText] : ''"
        :disabled="isReadonly || !item.items.length"
        return-object
        item-title="name"
        item-value="slug"
        :items="item.items"
        :model-value="store.formState[item.key] as SelectorItem"
        @update:model-value="(val: any) => store.updateField(item.key, val)"
        :error-messages="
          v$[item.key].$errors.map((e: ErrorObject) => e.$message) as string[]
        "
        @blur="
          () => {
            v$[item.key].$commit()
            v$[item.key].$touch()
          }
        "
        aria-autocomplete="none"
        autocomplete="new-password"
      >
        <template #append>
          <v-btn
            :disabled="!store.previousFormState[item.key]?.isDirty"
            icon="$iReset"
            @click="resetField(item.key)"
            color="info"
            variant="tonal"
            tabindex="-1"
            size="small"
            density="comfortable"
            v-tippy="{ content: 'Click to reset field changes' }"
          />
        </template>
      </v-select>

      <v-input
        class="my-4 admin-models-fields__field admin-models-fields__image-field"
        :label="item.label"
        v-if="item.type === 'image'"
        :key="item.key"
        :disabled="isReadonly"
        :messages="[
          'Drag the photo into the input zone or click there to chose the photo',
        ]"
        :error-messages="
          v$[item.key].$errors.map((e: ErrorObject) => e.$message) as string[]
        "
      >
        <v-chip
          label
          :text="item.label"
          color="info"
          variant="flat"
          style="position: absolute; z-index: 5; top: 12px; left: 24px"
        />
        <v-file-upload
          width="50%"
          icon="$iUpload"
          clearable
          density="comfortable"
          :model-value="store.formState[item.key] as File | undefined"
          @update:model-value="
            (val: any) => {
              store.updateField(item.key, val)
              v$[item.key].$commit()
              v$[item.key].$touch()
            }
          "
          accept="image/*"
        >
          <template #title>
            <span class="text-subtitle-2 text-disabled"
              >Drag and drop your image here</span
            >
          </template>
          <template #item>
            <v-card
              :border="`${getBaseColor(item.key)} md`"
              flat
              height="100%"
              width="100%"
              style="--v-border-opacity: 0.5"
            >
              <v-btn
                @click="store.updateField(item.key, undefined)"
                position="absolute"
                style="z-index: 5; top: 8px; right: 8px"
                icon="$iDelete"
                density="comfortable"
                rounded="lg"
                color="error"
                variant="flat"
                v-tippy="{ content: 'Click to delete current image' }"
              />
              <v-card-item>
                <v-avatar :image="preview" size="216" rounded="lg" />
              </v-card-item>
            </v-card>
          </template>
        </v-file-upload>
        <template #append>
          <v-btn
            :disabled="!store.previousFormState[item.key]?.isDirty"
            icon="$iReset"
            @click="resetField(item.key)"
            color="info"
            variant="tonal"
            tabindex="-1"
            size="small"
            density="comfortable"
            v-tippy="{ content: 'Click to reset field changes' }"
          />
        </template>
      </v-input>
    </template>

    <v-btn
      text="save"
      color="info"
      block
      variant="tonal"
      :loading="store.isSaving"
      :disabled="v$.$invalid || !store.anyDirty"
      @click="save"
    />
  </div>
</template>

<style lang="scss">
.admin-models-fields__field {
  .v-field__outline {
    --v-field-border-width: 2px;
  }
  &.admin-models-fields__image-field {
    > .v-input__control {
      position: relative;

      > .v-file-upload-items {
        position: absolute;
        top: 0;
        left: 0;
        width: 50%;
        height: 100%;
        margin: 0;
      }
    }
  }
}
</style>
