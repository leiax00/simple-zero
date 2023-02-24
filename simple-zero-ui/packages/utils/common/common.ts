export const add = (a: number, b: number): number => {
  return a + b
}

export const isEmptyStr = (str: string): boolean =>
  str === null || str === undefined || str.trim() === ''

export const strIntercept = (str: string, maxLen: number): string => {
  if (str.length > maxLen) {
    return `${str.slice(0, maxLen > 3 ? maxLen - 3 : maxLen)}...`
  }
  return str
}
