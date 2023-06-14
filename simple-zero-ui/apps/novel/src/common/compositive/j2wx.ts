export type J2Rank = {
  rankId: string
  channelKey: string
  rankName: string
  type: string
}

export type J2Book = {
  id: string
  name: string
  authorId: string
  authorName: string
  cover: string
  size: string
  tags: string
  type: string
}

export type J2Stat = {
  time: number
  score: number
  favoriteCount: number
  ticketCount: number
}

export type J2RankBook = {
  book: J2Book
  statList: J2Stat[]
}

export type CustomRank = {
  id: number
  name: string
  password: string
  desc?: string
  bookIdList: string[]
}

/**
 * 格式化排行榜
 * @param {J2RankBook} rankItem 后端返回的原始值
 * @param {boolean} withDelta 是否显示今日增长排名
 * @return 排名字符串 或 排名(今日增量)
 */
export function formatRank(rankItem: J2RankBook, withDelta = true): string {
  const statLen = rankItem.statList.length
  if (statLen === 0) {
    return '0'
  }
  const score = rankItem.statList[statLen - 1].score
  if (!withDelta) {
    return `${score}`
  }
  const prevScore = rankItem.statList[0].score
  // 时间正序, 因此今早凌晨 - 当前排名 = delta
  // 凌晨排名 100, 当前排名 99, 则 delta = 100 - 99 = +1
  // 凌晨排名 100, 当前排名 101, 则 delta = 100 - 101 = -1
  return `${score}(${prevScore - score})`
}

/**
 * 格式化收藏数量
 * @param {J2RankBook} rankItem 后端返回的原始值
 * @param {boolean} withDelta 是否显示今日增长收藏
 * @return
 */
export function formatFavoriteCount(rankItem: J2RankBook, withDelta = true): string {
  const statLen = rankItem.statList.length
  if (statLen === 0) {
    return '0'
  }
  const score = rankItem.statList[statLen - 1].favoriteCount
  if (!withDelta) {
    return `${score}`
  }
  const prevScore = rankItem.statList[0].favoriteCount
  return `${score}(${score - prevScore})`
}

/**
 * 转换为chart数据, 为画图做基础数据
 * @param rankItem
 * @param isIncrement
 */
export function toChartData(rankItem: any[], isIncrement = false) {
  function parseItem(item: J2RankBook) {
    const rst: any = []
    item.statList.forEach((t: J2Stat, i) => {
      let favoriteCount = t.favoriteCount
      let ticketCount = t.ticketCount
      if (isIncrement) {
        favoriteCount = i === 0 ? 0 : t.favoriteCount - item.statList[i - 1].favoriteCount
        ticketCount = i === 0 ? 0 : t.ticketCount - item.statList[i - 1].favoriteCount
      }
      rst.push([t.time, item.book.id, item.book.name, t.score, favoriteCount, ticketCount])
    })
    return rst
  }

  const tmp: any = [['time', 'id', 'name', 'rank', 'favoriteCount', 'ticketCount']]
  rankItem.forEach((v) => {
    tmp.push(...parseItem(v))
  })

  return tmp
}
