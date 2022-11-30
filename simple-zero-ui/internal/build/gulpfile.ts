import { parallel, series } from 'gulp'
export const clean = () => {
  console.log('clean.....')
}

export default series(clean)
