// Utilities
import { defineStore } from 'pinia'
import axios from 'axios'
import { toast } from 'vue3-toastify'
import { kebabCase, isEqual } from 'lodash'
import getSlug from 'speakingurl'
import {
  formatCompanyData,
  getInitFormState,
  prepareRequestData,
} from '@/store/admin/helpers'

// Types
import type { AxiosError } from 'axios'
import type {
  ICompanyDataToRequest,
  IFetchedDetailCompany,
  IFormattedDetailCompany,
} from '@/types/admin.types'
import type {
  DependentFieldMap,
  FormState,
  PreviousFormState,
} from '@/store/admin/types'
import type { Router } from 'vue-router'

export const useAdminModelStore = defineStore('admin', {
  state: () => ({
    companyUID: null as string | null,
    formState: {} as FormState,
    previousFormState: {} as PreviousFormState,
    isSaving: false,
    editMode: false,
    isDirty: false,
  }),
  getters: {
    anyDirty(state) {
      return Object.values(state.previousFormState).some((f) => f.isDirty)
    },
    isNew(state) {
      return !state.companyUID
    },
  },
  actions: {
    async _createModel(formData: ICompanyDataToRequest) {
      return await axios.post('api/v1/admin/companies/', formData)
    },
    _getAllPreviousValues(): IFormattedDetailCompany {
      return Object.entries(this.previousFormState).reduce(
        (acc, [key, fieldState]) => ({
          ...acc,
          [key]: fieldState.value,
        }),
        {} as IFormattedDetailCompany
      )
    },
    _handleError(error: AxiosError, context: string) {
      console.log(`[AdminStore] Error in ${context}:`, error)
    },
    async _handleSaveSuccess(data: IFetchedDetailCompany) {
      const companyFormData = await formatCompanyData(data)

      this.closeEditMode()
      this.formState = companyFormData
      this.companyUID = data.uid
      this._initPreviousState()
      toast.success('Company is successfully saved')
      window.scrollTo({ top: 0, behavior: 'smooth' })
    },
    _initPreviousState() {
      this.previousFormState = Object.entries(this.formState).reduce(
        (acc, [key, value]) => ({
          ...acc,
          [key]: {
            value,
            isDirty: false,
          },
        }),
        {} as PreviousFormState
      )
    },
    _navigateToParent(router: Router) {
      router.push({
        name: 'adminModelsCompanies',
      })
    },
    _resetDependentFields(key: keyof IFormattedDetailCompany) {
      const dependentFieldMap: DependentFieldMap = {
        country: ['market'],
        market: ['country'],
        sector: ['industry'],
        industry: ['sector'],
        ticker: ['slug'],
      } as const

      const fieldToReset = (dependentFieldMap[key] ||
        []) as (keyof IFormattedDetailCompany)[]
      fieldToReset.forEach((field) => {
        this.formState[field] = this.previousFormState[field].value as never
        this.previousFormState[key].isDirty = false
      })
    },
    _updateDependentFields(key: keyof IFormattedDetailCompany) {
      const dependencies: Record<string, (keyof IFormattedDetailCompany)[]> = {
        sector: ['industry'],
        country: ['market'],
        ticker: ['slug'],
      }

      const resetStrategies: Record<string, any> = {
        industry: { name: '', slug: '', key: 0 },
        market: { name: '', slug: '', key: 0 },
        slug: getSlug(kebabCase(this.formState.ticker)),
      }

      this.formState =
        dependencies[key]?.reduce(
          (state, field) => ({
            ...state,
            [field]: resetStrategies[field],
          }),
          this.formState
        ) || this.formState
    },
    async _updateModel(formData: ICompanyDataToRequest) {
      return await axios.patch(
        `api/v1/admin/companies/${this.companyUID}/`,
        formData
      )
    },
    closeEditMode(router?: Router) {
      this.resetField('__all__')
      this.editMode = false
      if (this.isNew && !!router) {
        this._navigateToParent(router)
      }
    },
    async deleteModel(router: Router) {
      try {
        await axios.delete(`api/v1/admin/companies/${this.companyUID}/`)

        toast.success(`Company ${this.companyUID} was successfully deleted`)

        this._navigateToParent(router)
      } catch (e) {
        if (axios.isAxiosError(e)) {
          this._handleError(e, 'deleteModel')
        }
      }
    },
    async fetchCompany() {
      const uid = this.companyUID

      if (!uid) return

      // Check cache
      // if (this.statesCache.has(uid)) {
      //   this.formState = this.statesCache.get(uid)!
      //   return
      // }

      try {
        const response = await axios.get<IFetchedDetailCompany>(
          `api/v1/admin/companies/${uid}/`
        )
        const formattedData = await formatCompanyData(response.data)

        // Save in cache
        // this.statesCache.set(uid, formattedData)

        this.formState = formattedData
      } catch (e) {
        if (axios.isAxiosError(e)) {
          this._handleError(e, 'fetchCompany')
        }
        throw e
      }
    },
    async initStore(uid: string, router: Router) {
      this.companyUID = uid || null
      this.formState = getInitFormState()

      if (this.isNew) {
        this.openEditMode()
      } else {
        this.closeEditMode(router)
        await this.fetchCompany()
      }
    },
    openEditMode() {
      this._initPreviousState()
      this.editMode = true
    },
    async postModel() {
      if (this.isSaving) return

      this.isSaving = true

      try {
        const formData = await prepareRequestData(
          this.formState,
          this.previousFormState
        )

        const response = this.isNew
          ? await this._createModel(formData)
          : await this._updateModel(formData)

        await this._handleSaveSuccess(response.data)
      } catch (e) {
        if (axios.isAxiosError(e)) {
          this._handleError(e, 'saveModelForm')
        }
        throw e
      } finally {
        this.isSaving = false
      }
    },
    resetField(key: keyof IFormattedDetailCompany | '__all__') {
      if (key === '__all__') {
        this.formState = this._getAllPreviousValues()
        this._initPreviousState()
        return
      }

      this.formState[key] = this.previousFormState[key].value as never
      this.previousFormState[key].isDirty = false

      this._resetDependentFields(key)
    },
    resetStore() {
      this.companyUID = null
      this.formState = {} as FormState
      this.previousFormState = {} as PreviousFormState
      this.editMode = false
      this.isDirty = false
    },
    updateField(key: keyof IFormattedDetailCompany, val: any) {
      this.formState = { ...this.formState, [key]: val }

      this.previousFormState[key].isDirty = !isEqual(val, this.previousFormState[key].value);

      this._updateDependentFields(key)
    },
  },
})
