import type {Module} from "vuex";
import type {
  FetchedDetailCompany,
  FormattedCountry,
  FormattedDetailCompany,
  FormattedIndustry,
  FormattedMarket,
  FormattedSector,
} from "@/types/admin";
import axios from "axios";
import getSlug from "speakingurl";
import _ from "lodash";

export const adminModule = {
  state: () => ({
      companyUID: '',
  }),
  getters: {},
  mutations: {
      setCompanyUID(state, payload: string) {
        state.companyUID = payload
      },
  },
  actions: {},
  namespaced: true,
} as Module<any, any>