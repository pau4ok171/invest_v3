/* eslint-disable no-console */

// Utilities
import { warn } from "vue";

export function consoleWarn (message: string): void {
  warn(`Visagiste: ${message}`)
}

export function consoleError (message: string): void {
  warn(`Visagiste error: ${message}`)
}