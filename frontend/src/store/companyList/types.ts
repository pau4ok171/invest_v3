// Types
import type { ListCompany, Market } from '@/types/invest'

export interface BaseState {
  id: number
  key: string
  title: string
}

export interface CountryState extends BaseState {
  markets: Market[]
}

export interface DependentState extends BaseState {
  parentKeys: number[]
}

export interface CompaniesOptions {
  side?: InfiniteScrollSide
  done: (status: InfiniteScrollStatus) => void
}

export interface CompaniesResponse {
  results: ListCompany[]
  next: string | null
  count: number
}

export interface WatchlistItem {
  watchlisted: boolean
  uid: string
  ticker: string
}

export type InfiniteScrollSide = 'start' | 'end' | 'both'
export type InfiniteScrollStatus = 'ok' | 'empty' | 'loading' | 'error'
