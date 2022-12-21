export const add = (a: number, b: number): number => {
  return a + b
}

export const isEmptyStr = (str: string): boolean =>
  str === null || str === undefined || str.trim() === ''
