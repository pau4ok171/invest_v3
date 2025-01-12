/* eslint-disable no-console */

// Utilities
import { warn } from "vue";

export function consoleWarn (message: string): void {
  warn(`Base: ${message}`)
}