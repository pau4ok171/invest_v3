import {helpers, numeric, required, url} from "@vuelidate/validators";
import {isImageValidator, isYearValidator, maxVolumeValidator} from "@/components/admin/models/validators";

export const defaultModelFieldData = {
  field: '',
  isDisabled: false,
  isRequired: false,
  label: '',
  helpText: '',
  validators: {},
  options: null,
  hasSearch: null,
  wasModifiedIsNeeded: true,
}

export const companyModel = {
  isVisible: {
    field: 'AdminCheckBoxField',
    isDisabled: '!editModeActivated',
    label: 'Company is publicly visible',
  },
  ticker: {
    field: 'AdminCharField',
    isDisabled: '!editModeActivated',
    label: 'Ticker',
    validators: { required },
  },
  slug: {
    field: 'AdminCharField',
    isDisabled: true,
    label: 'Slug',
    wasModifiedIsNeeded: false,
  },
  uid: {
    field: 'AdminCharField',
    isDisabled: '!editModeActivated',
    label: 'UID',
    helpText: 'UID of type 00000000-0000-0000-0000-000000000000',
    validators: { required },
  },
  companyName: {
    field: 'AdminCharField',
    isDisabled: '!editModeActivated',
    label: 'Company Name',
    validators: { required },
  },
  shortCompanyName: {
    field: 'AdminCharField',
    isDisabled: '!editModeActivated',
    label: 'Short Company Name',
  },
  shortCompanyNameGenitive: {
    field: 'AdminCharField',
    isDisabled: '!editModeActivated',
    label: 'Short Company Name Genitive',
  },
  description: {
    field: 'AdminTextField',
    isDisabled: '!editModeActivated',
    label: 'Description',
  },
  shortDescription: {
    field: 'AdminTextField',
    isDisabled: '!editModeActivated',
    label: 'Short Description',
  },
  country: {
    field: 'AdminSelectorField',
    isDisabled: '!editModeActivated',
    label: 'Country',
    validators: { slug: { required } },
    options: 'countries',
  },
  market: {
    field: 'AdminSelectorField',
    isDisabled: '!editModeActivated',
    label: 'Market',
    helpText: 'Is unblocked after filling the country field',
    validators: { slug: { required } },
    options: 'filteredMarkets',
  },
  sector: {
    field: 'AdminSelectorField',
    isDisabled: '!editModeActivated',
    label: 'Sector',
    validators: { slug: { required } },
    options: 'sectors',
  },
  industry: {
    field: 'AdminSelectorField',
    isDisabled: '!editModeActivated',
    label: 'Industry',
    helpText: 'Is unblocked after filling the sector field',
    validators: { slug: { required } },
    options: 'filteredIndustries'
  },
  logo: {
    field: 'AdminImageField',
    isDisabled: '!editModeActivated',
    label: 'Logo',
    helpText: 'Drag the photo into the input zone or click there to chose the photo',
    validators: {
      isImageValidator: helpers.withMessage('Field must be an image', isImageValidator),
      maxVolumeValidator: helpers.withMessage('Field must be 100Kb max', maxVolumeValidator),
    },
  },
  isFund: {
    field: 'AdminCheckBoxField',
    isDisabled: '!editModeActivated',
    label: 'Company is a fund',
  },
  city: {
    field: 'AdminCharField',
    isDisabled: '!editModeActivated',
    label: 'City',
  },
  website: {
    field: 'AdminCharField',
    isDisabled: '!editModeActivated',
    label: 'Website',
    validators: { url },
  },
  founded: {
    field: 'AdminCharField',
    isDisabled: '!editModeActivated',
    label: 'Founded',
    helpText: 'Year of company foundation',
    validators: {
      numeric,
      isYearValidator: helpers.withMessage('Field must be an year without text', isYearValidator),
    }
  },
}