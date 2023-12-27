import { writeFile } from 'node:fs/promises'
import * as path from 'node:path'
import log from 'consola'
// @ts-ignore
import pkg from '../../zero-ui/package.json' // need to be checked
import { uiPath } from './pkgPath'

function getVersion() {
  const tagVer = process.env.TAG_VERSION
  if (tagVer) {
    return tagVer.startsWith('v') ? tagVer.slice(1) : tagVer
  } else {
    return pkg.version
  }
}

const version = getVersion()

async function main() {
  log.info(`Version: ${version}`)
  await writeFile(
    path.resolve(uiPath, 'version.ts'),
    `export const version = '${version}'
export const name = '${pkg.name}'
`
  )
}

main()
