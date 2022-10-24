export interface BookBase {
  bid: string
  name: string
  type: string
  icon: string
  author: string
  desc: string
  latest_chapter: string
  update_time: string
  pinyin_name: string
}

export interface CatalogBase {
  bid: string
  cid: string
  name: string
}

export interface BookInfo {
  book: BookBase
  catalogs: Array<CatalogBase>
}
