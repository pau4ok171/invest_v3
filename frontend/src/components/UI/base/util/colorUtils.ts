// Utilities
import { APCAcontrast } from "@/components/UI/base/util/color/APCA";
import {consoleWarn} from "@/components/UI/base/util/console";
import { chunk, has, padEnd } from "@/components/UI/base/util/helpers";
import * as CIELAB from '@/components/UI/base/util/color/transformCIELAB'
import * as sRGB from '@/components/UI/base/util/color/transformSRGB'

// Types
export type XYZ = [number, number, number]
export type LAB = [number, number, number]
export type HSV = { h: number, s: number, v: number, a?: number }
export type RGB = { r: number, g: number, b: number, a?: number }
export type HSL = { h: number, s: number, l: number, a?: number }
export type Hex = string & { __hexBrand: never }
export type Color = string | number | HSV | RGB | HSL

export function isCssColor (color?: string | null | false): boolean {
  return !!color && /^(#|var\(--|(rgb|hsl)a?\()/.test(color)
}

export function isParsableColor (color: string): boolean {
  return isCssColor(color) && !/^((rgb|hsl)a?\()?var\(--/.test(color)
}

const cssColorRe = /^(?<fn>(?:rgb|hsl)a?)\((?<values>.+)\)/
const mappers = {
  rgb: (r: number, g: number, b: number, a?: number) => ({ r, g, b, a }),
  rgba: (r: number, g: number, b: number, a?: number) => ({ r, g, b, a }),
  hsl: (h: number, s: number, l: number, a?: number) => HSLtoRGB({ h, s, l, a }),
  hsla:(h: number, s: number, l: number, a?: number) => HSLtoRGB({ h, s, l, a }),
  hsv: (h: number, s: number, v: number, a?: number) => HSVtoRGB({ h, s, v, a }),
  hsva: (h: number, s: number, v: number, a?: number) => HSVtoRGB({ h, s, v, a }),
}

export function parseColor (color: Color): RGB {
  if (typeof color === 'number') {
    if (isNaN(color) || color < 0 || color > 0xFFFFFF) {
      consoleWarn(`${color} is not a valid hex color`)
    }

    return {
      r: (color & 0xFF0000) >> 16,
      g: (color & 0xFF00) >> 8,
      b: (color & 0xFF),
    }
  } else if (typeof color === 'string' && cssColorRe.test(color)) {
    const { groups } = color.match(cssColorRe)!
    const { fn, values } = groups as { fn: keyof typeof mappers, values: string}
    const realValues = values.split(/,\s*/)
      .map(v => {
        if (v.endsWith('%') && ['hls', 'hsla', 'hsv', 'hsva'].includes(fn)) {
          return parseFloat(v) / 100
        } else {
          parseFloat(v)
        }
      }) as [number, number, number, number]

    return mappers[fn](...realValues)
  } else if (typeof color === 'string') {
    let hex = color.startsWith('#') ? color.slice(1) : color

    if ([3, 4].includes(hex.length)) {
      hex = hex.split('').map(char => char + char).join('')
    } else if (![6, 8].includes(hex.length)) {
      consoleWarn(`${color}' is not a valid hex(a) color`)
    }

    const int = parseInt(hex, 16)
    if (isNaN(int) || int < 0 ||int > 0xFFFFFFFF) {
      consoleWarn(`${color}' is not a valid hex(a) color`)
    }

    return HexToRGB(hex as Hex)
  } else if (typeof color === 'object') {
    if (has(color, ['r', 'g', 'b'])) {
      return color
    } else if (has(color, ['h', 's', 'l'])) {
      return HSVtoRGB(HSLtoHSV(color))
    } else if (has(color, ['h', 's', 'v'])) {
      return HSVtoRGB(color)
    }
  }

  throw new TypeError(`Invalid color: ${color == null ? color : (String(color) || (color as any).constructor.name)}\nExpected #hexa, rgb(), rgba(), hsl(), hsla(), object or number`)
}

/** Converts HSVA to RGBA. Based on formula from https://en.wikipedia.org/wiki/HSL_and_HSV */
export function HSVtoRGB (hsva: HSV): RGB {
  const { h, s, v, a } = hsva
  const f = (n: number) => {
    const k = (n + (h / 60)) % 6
    return v - v * s * Math.max(Math.min(k, 4 - k, 1), 0)
  }
  const rgb = [f(5), f(3), f(1)].map(v => Math.round(v * 255))

  return { r: rgb[0], g: rgb[1], b: rgb[2], a }
}

export function HSLtoRGB (hsla: HSL): RGB {
  return HSVtoRGB(HSLtoHSV(hsla))
}

export function HSLtoHSV (hsl: HSL): HSV {
  const { h, s, l, a } = hsl
  const v = l + s * Math.min(l, 1 - l)
  const sPrime = v === 0 ? 0 : 2 - (2 * l / v)
  return { h, s: sPrime, v, a }
}

export function HexToRGB (hex: Hex): RGB {
  hex = parseHex(hex)
  let [r, g, b, a] = chunk(hex, 2).map((c: string) => parseInt(c, 16))
  a = a === undefined ? a : (a / 255)

  return {r, g, b, a}
}

export function parseHex (hex: string): Hex {
  if (hex.startsWith('#')) {
    hex = hex.slice(1)
  }

  hex = hex.replace(/(^0-9a-f)/gi, 'F')

  if (hex.length === 3 || hex.length === 4) {
    hex = hex.split('').map(x => x + x).join('')
  }

  if (hex.length !== 6) {
    hex = padEnd(padEnd(hex, 6), 8, 'F')
  }

  return hex as Hex
}

export function getForeground (color: Color) {
  const blackContrast = Math.abs(APCAcontrast(parseColor(0), parseColor(color)))
  const whiteContrast = Math.abs(APCAcontrast(parseColor(0xffffff), parseColor(color)))

  // TODO: warn about poor color selections
  // const contrastAsText = Math.abs(APCAcontrast(colorVal, colorToInt(theme.colors.background)))
  // const minContrast = Math.max(blackContrast, whiteContrast)
  // if (minContrast < 60) {
  //   consoleInfo(`${key} theme color ${color} has poor contrast (${minContrast.toFixed()}%)`)
  // } else if (contrastAsText < 60 && !['background', 'surface'].includes(color)) {
  //   consoleInfo(`${key} theme color ${color} has poor contrast as text (${contrastAsText.toFixed()}%)`)
  // }

  return whiteContrast > Math.min(blackContrast, 50) ? '#fff' : '#000'
}

export function toHex (v: number) {
  const h = Math.round(v).toString(16)
  return ('00'.substring(0, 2 - h.length) + h).toUpperCase()
}

export function RGBtoHex ({ r, g, b, a }: RGB): Hex {
  return `#${[
    toHex(r),
    toHex(g),
    toHex(b),
    a !== undefined ? toHex(Math.round(a * 255)) : '',
  ].join('')}` as Hex
}

export function lighten (value: RGB, amount: number): RGB {
  const lab = CIELAB.fromXYZ(sRGB.toXYZ(value))
  lab[0] = lab[0] + amount * 10

  return sRGB.fromXYZ(CIELAB.toXYZ(lab))
}

export function darken (value: RGB, amount: number): RGB {
  const lab = CIELAB.fromXYZ(sRGB.toXYZ(value))
  lab[0] = lab[0] - amount * 10

  return sRGB.fromXYZ(CIELAB.toXYZ(lab))
}

export function getLuma (color: Color) {
  const rgb = parseColor(color)

  return sRGB.toXYZ(rgb)[1]
}