import Components from './component'
import Plugins from './plugin'
import { makeInstaller } from './make-installer'

export default makeInstaller([...Components, ...Plugins])
