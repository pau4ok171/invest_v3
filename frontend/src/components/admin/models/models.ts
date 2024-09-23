import {helpers, numeric, required, url} from "@vuelidate/validators";
import {isImageValidator, isYearValidator, maxVolumeValidator} from "@/components/admin/models/validators";
import {AdminFieldType} from "@/types/admin.types";
import type {IAdminModelDeclared, IDefaultField} from "@/types/admin.types";


export const defaultModelFieldData: IDefaultField = {
  modelValue: undefined,
  isDisabled: false,
  isRequired: false,
  label: '',
  helpText: '',
  validators: {},
  options: undefined,
  hasSearch: undefined,
  wasModifiedIsNeeded: true,
}

export const companyModel: IAdminModelDeclared = {
  isVisible: {
    field: AdminFieldType.CHECKBOX,
    isDisabled: 'editModeActivated',
    label: 'Company is publicly visible',
  },
  ticker: {
    field: AdminFieldType.CHAR,
    isDisabled: 'editModeActivated',
    label: 'Ticker',
    validators: { required },
  },
  slug: {
    field: AdminFieldType.CHAR,
    isDisabled: true,
    label: 'Slug',
    wasModifiedIsNeeded: false,
  },
  uid: {
    field: AdminFieldType.CHAR,
    isDisabled: 'editModeActivated',
    label: 'UID',
    helpText: 'UID of type 00000000-0000-0000-0000-000000000000',
    validators: { required },
  },
  companyName: {
    field: AdminFieldType.CHAR,
    isDisabled: 'editModeActivated',
    label: 'Company Name',
    validators: { required },
  },
  shortCompanyName: {
    field: AdminFieldType.CHAR,
    isDisabled: 'editModeActivated',
    label: 'Short Company Name',
  },
  shortCompanyNameGenitive: {
    field: AdminFieldType.CHAR,
    isDisabled: 'editModeActivated',
    label: 'Short Company Name Genitive',
  },
  description: {
    field: AdminFieldType.TEXT,
    isDisabled: 'editModeActivated',
    label: 'Description',
  },
  shortDescription: {
    field: AdminFieldType.TEXT,
    isDisabled: 'editModeActivated',
    label: 'Short Description',
  },
  country: {
    field: AdminFieldType.SELECTOR,
    isDisabled: 'editModeActivated',
    label: 'Country',
    validators: { slug: { required } },
    options: 'countries',
  },
  market: {
    field: AdminFieldType.SELECTOR,
    isDisabled: 'editModeActivated',
    label: 'Market',
    helpText: 'Is unblocked after filling the country field',
    validators: { slug: { required } },
    options: 'filteredMarkets',
  },
  sector: {
    field: AdminFieldType.SELECTOR,
    isDisabled: 'editModeActivated',
    label: 'Sector',
    validators: { slug: { required } },
    options: 'sectors',
  },
  industry: {
    field: AdminFieldType.SELECTOR,
    isDisabled: 'editModeActivated',
    label: 'Industry',
    helpText: 'Is unblocked after filling the sector field',
    validators: { slug: { required } },
    options: 'filteredIndustries'
  },
  logo: {
    field: AdminFieldType.IMAGE,
    isDisabled: 'editModeActivated',
    label: 'Logo',
    helpText: 'Drag the photo into the input zone or click there to chose the photo',
    validators: {
      isImageValidator: helpers.withMessage('Field must be an image', isImageValidator),
      maxVolumeValidator: helpers.withMessage('Field must be 100Kb max', maxVolumeValidator),
    },
  },
  isFund: {
    field: AdminFieldType.CHECKBOX,
    isDisabled: 'editModeActivated',
    label: 'Company is a fund',
  },
  city: {
    field: AdminFieldType.CHAR,
    isDisabled: 'editModeActivated',
    label: 'City',
  },
  website: {
    field: AdminFieldType.CHAR,
    isDisabled: 'editModeActivated',
    label: 'Website',
    validators: { url },
  },
  founded: {
    field: AdminFieldType.YEAR,
    isDisabled: 'editModeActivated',
    label: 'Founded',
    helpText: 'Year of company foundation',
    validators: {
      numeric,
      isYearValidator: helpers.withMessage(`Field must be an year between 1000 and ${new Date().getFullYear()}`, isYearValidator),
    }
  },
}