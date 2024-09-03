export const isImageValidator = (file: File) => {
  if (!file?.size) return true
  return file.type.startsWith('image')
}
export const maxVolumeValidator = (file: File|Object) => {
  if (file instanceof File && file.type.startsWith('image')) {
    return file.size < 100 * 1024
  }
  return true
}
export const isYearValidator = (val: string) => {
  if (val.length === 0) return true

  return val.length === 4 && Number(val) >= 1000 && Number(val) <= new Date().getFullYear()
}