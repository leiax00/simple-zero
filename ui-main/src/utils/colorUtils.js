export function hex2Rgb(hexStr) {
  return 'RGB(' + getRgbNumList(hexStr).join(', ') + ')'
}

export function rgb2hex(rgbStr) {
  // RGB颜色值的正则
  const reg = /^(rgb|RGB)/
  const color = rgbStr
  if (reg.test(color)) {
    let strHex = '#'
    // 把RGB的3个数值变成数组
    const colorArr = color.replace(/(?:\(|\)|rgb|RGB)*/g, '').split(',')
    // 转成16进制
    for (let i = 0; i < colorArr.length; i++) {
      let hex = Number(colorArr[i]).toString(16)
      if (hex === '0') {
        hex += hex
      }
      strHex += hex
    }
    return strHex
  } else {
    return String(color)
  }
}

export function getRgbNumList(color) {
  let colorChange = []
  if (/^#([0-9a-fA-f]{3}|[0-9a-fA-f]{6})$/.test(color)) {
    color = color.toLowerCase()
    if (color.length === 4) {
      let colorNew = '#'
      for (let i = 1; i < 4; i += 1) {
        colorNew += color.slice(i, i + 1).concat(color.slice(i, i + 1))
      }
      color = colorNew
    }
    // 处理六位的颜色值，转为RGB
    for (let i = 1; i < 7; i += 2) {
      colorChange.push(parseInt('0x' + color.slice(i, i + 2)))
    }
  } else {
    colorChange = color.substring(color.indexOf('('), color.indexOf(')')).split(',').map(item => item.trim())
  }
  return colorChange
}

export function hex2Rgba(hex, transparency = 1) {
  return `rgba(${getRgbNumList(hex).join(',')},${transparency})`
}
