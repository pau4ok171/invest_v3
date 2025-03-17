import { defineStore } from 'pinia'

export const usePageStore = defineStore({
  id: 'page',
  state: () => ({
    notFound: false,
    loading: false,
  }),
})
