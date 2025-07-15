export interface Language {
  id: string
  title: string
  iso: string
}
export type Languages = Language[]

export const LANGUAGES: Languages = [
  { id: 'en', title: 'English', iso: 'gb' },
  { id: 'ru', title: 'Русский', iso: 'ru' },
  { id: 'fr', title: 'Français', iso: 'fr' },
  { id: 'es', title: 'Español', iso: 'es' },
  { id: 'de', title: 'Deutsch', iso: 'de' },
  { id: 'pl', title: 'Polski', iso: 'pl' },
  { id: 'it', title: 'Italiano', iso: 'it' },
]