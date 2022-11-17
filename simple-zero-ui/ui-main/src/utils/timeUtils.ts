import dayjs from 'dayjs'
import constObj from '@/bean/constObj'

export default {
  parseTime(times: number | Date, pattern = 'YYYY-MM-DDTHH:mm:ss') {
    if (times === 0) {
      return ''
    }
    if (pattern) {
      return dayjs(times).format(pattern).toLocaleString()
    }
    return dayjs(times).format('YYYY-MM-DDTHH:mm:ss').toLocaleString()
  },
  calcTimeDiff(
    startT: number | Date,
    endT = new Date()
  ): {
    day: number
    hour: number
    minute: number
    second: number
    time?: string
  } {
    let diff =
      dayjs(endT).diff(dayjs(startT), 'seconds') * constObj.TIME_UNIT.ONE_SECOND
    const day = Math.floor(diff / constObj.TIME_UNIT.ONE_DAY)
    diff = diff - day * constObj.TIME_UNIT.ONE_DAY
    const hour = Math.floor(diff / constObj.TIME_UNIT.ONE_HOUR)
    diff = diff - hour * constObj.TIME_UNIT.ONE_HOUR
    const minute = Math.floor(diff / constObj.TIME_UNIT.ONE_MINUTE)
    diff = diff - minute * constObj.TIME_UNIT.ONE_MINUTE
    const second = Math.floor(diff / constObj.TIME_UNIT.ONE_SECOND)
    return {
      day,
      hour,
      minute,
      second,
    }
  },
  formatTime(time: number | Date) {
    return dayjs(time).format('YYYY-MM-DD')
  },
}
