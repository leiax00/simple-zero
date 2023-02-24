export type J2Rank = {
  id: string
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
  return `${score}(${score - prevScore})`
}

/**
 * 格式化收藏数量
 * @param {J2RankBook} rankItem 后端返回的原始值
 * @param {boolean} withDelta 是否显示今日增长收藏
 * @return
 */
export function formatFavoriteCount(
  rankItem: J2RankBook,
  withDelta = true
): string {
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
 */
export function toChartData(rankItem: any[]) {
  function parseItem(item: J2RankBook) {
    const rst: any = []
    item.statList.forEach((t: J2Stat) => {
      rst.push([
        t.time,
        item.book.id,
        item.book.name,
        t.score,
        t.favoriteCount,
        t.ticketCount,
      ])
    })
    return rst
  }

  const tmp: any = [
    ['time', 'id', 'name', 'rank', 'favoriteCount', 'ticketCount'],
  ]
  rankItem.forEach((v) => {
    tmp.push(...parseItem(v))
  })

  return tmp
}