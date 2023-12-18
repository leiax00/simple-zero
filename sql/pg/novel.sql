-- =========================== 作者表 ===========================
drop table if exists novel.author;
create table novel.author
(
    id              bigserial           not null
        constraint author_pk primary key,
    platform        int8,
    author_id       varchar(64),
    platform_status char(1),
    author_name     varchar(64),
    status          char(1) default '0' not null,
    create_time     timestamptz,
    create_by       varchar(64),
    update_time     timestamptz,
    update_by       varchar(64)
);

comment on table novel.author is '作者表';
comment on column novel.author.id is '主键ID';
comment on column novel.author.platform is '所属平台';
comment on column novel.author.author_id is '平台作者ID';
comment on column novel.author.platform_status is '平台上状态: 0未签约, 1签约';
comment on column novel.author.author_name is '笔名/昵称';
comment on column novel.author.status is '状态: 0正常, 1封禁';
comment on column novel.author.create_time is '创建时间';
comment on column novel.author.create_by is '创建者';
comment on column novel.author.update_time is '更新时间';
comment on column novel.author.update_by is '更新者';

alter sequence novel.author_id_seq start with 1000;

insert into novel.author (id, platform, author_id, platform_status, author_name, status, create_time, create_by)
VALUES (1, 1, 3886666, '1', '小菜清粥', '0', now(), 'admin');

-- =========================== 平台表 ===========================
drop table if exists novel.platform;
create table novel.platform
(
    id            bigserial           not null
        constraint platform_pk primary key,
    platform_name varchar(64),
    nick_name     varchar(64),
    status        char(1) default '0' not null,
    create_time   timestamptz,
    create_by     varchar(64),
    update_time   timestamptz,
    update_by     varchar(64)
);

comment on table novel.platform is '平台表';
comment on column novel.platform.id is '主键ID';
comment on column novel.platform.platform_name is '平台名称';
comment on column novel.platform.nick_name is '平台别名';
comment on column novel.platform.status is '状态: 0正常, 1封禁';
comment on column novel.platform.create_time is '创建时间';
comment on column novel.platform.create_by is '创建者';
comment on column novel.platform.update_time is '更新时间';
comment on column novel.platform.update_by is '更新者';

alter sequence novel.platform_id_seq start with 1000;

insert into novel.platform (id, platform_name, nick_name, create_time, create_by)
values (1, '晋江', '晋江', now(), 'admin');

-- =========================== 小说表 ===========================
drop table if exists novel.book;
create table novel.book
(
    id                bigserial           not null
        constraint book_pk primary key,
    book_id            varchar(24),
    book_type          varchar(64),
    cover             varchar(255),
    book_name         varchar(64),
    author_id         int8,
    author_name       varchar(64),
    book_desc         text,
    finished          char(1) default 'N',
    score             varchar(32),
    count             int8,
    word_count        int8,
    comment_count     int4,
    last_chapter_id   int8,
    last_chapter_name varchar(64),
    last_chapter_time timestamptz,
    sign_status       char(1) default 'N',
    book_status       char(1),
    status            char    default '0' not null,
    create_time       timestamptz default now(),
    create_by         varchar(64),
    update_time       timestamptz,
    update_by         varchar(64)

);
create unique index book_pk2 on novel.book using btree (book_id);

comment on table novel.book is '小说表';
comment on column novel.book.id is '主键ID';
comment on column novel.book.book_id is '书籍原始ID';
comment on column novel.book.book_type is '分类名';
comment on column novel.book.cover is '小说封面url';
comment on column novel.book.book_name is '书籍名称';
comment on column novel.book.author_id is '作者id';
comment on column novel.book.author_name is '作者名';
comment on column novel.book.book_desc is '书籍描述';
comment on column novel.book.finished is '完结状态: N连载中, Y已完结';
comment on column novel.book.score is '评分';
comment on column novel.book.count is '收藏数/点击量等';
comment on column novel.book.word_count is '总字数';
comment on column novel.book.comment_count is '评论数';
comment on column novel.book.last_chapter_id is '最新章节ID';
comment on column novel.book.last_chapter_name is '最新章节名称';
comment on column novel.book.last_chapter_time is '最新更新时间';
comment on column novel.book.sign_status is '签约状态: N未签约, Y已签约';
comment on column novel.book.book_status is '状态，0：入库，1：上架';
comment on column novel.book.status is '本站状态: 0:可用, 1不可用, 2已删除';
comment on column novel.book.create_time is '创建时间';
comment on column novel.book.create_by is '创建者';
comment on column novel.book.update_time is '更新时间';
comment on column novel.book.update_by is '更新者';

-- =========================== 小说目录表 ===========================
drop table if exists novel.book_index;
create table novel.book_index
(
    id          bigserial        not null
        constraint book_index_pk primary key,
    book_id     varchar(24),
    index_num   varchar(24),
    index_name  varchar(64),
    word_count  int4 default 0,
    status      char default '0' not null,
    create_time timestamptz default now(),
    create_by   varchar(64),
    update_time timestamptz,
    update_by   varchar(64)
);
create unique index book_index_pk2 on novel.book_index using btree (book_id, index_num);

comment on table novel.book_index is '小说目录表';
comment on column novel.book_index.id is '主键ID';
comment on column novel.book_index.book_id is '书籍原始ID';
comment on column novel.book_index.index_num is '目录号';
comment on column novel.book_index.index_name is '目录名';
comment on column novel.book_index.word_count is '字数';
comment on column novel.book_index.status is '状态: 0免费, 1收费';
comment on column novel.book_index.create_time is '创建时间';
comment on column novel.book_index.create_by is '创建者';
comment on column novel.book_index.update_time is '更新时间';
comment on column novel.book_index.update_by is '更新者';

-- =========================== 小说章节表 ===========================
drop table if exists novel.book_content;
create table novel.book_content
(
    id       bigserial not null
        constraint book_content_pk primary key,
    book_id varchar(24),
    index_num varchar(24),
    content  text,
    create_time timestamptz default now(),
    create_by   varchar(64),
    update_time timestamptz,
    update_by   varchar(64)
);
create unique index book_content_pk2 on novel.book_content using btree (book_id, index_num);

comment on table novel.book_content is '小说章节内容表';
comment on column novel.book_content.id is '主键ID';
comment on column novel.book_content.book_id is '书籍原始ID';
comment on column novel.book_content.index_num is '目录号';
comment on column novel.book_content.content is '章节内容';
comment on column novel.book_index.create_time is '创建时间';
comment on column novel.book_index.create_by is '创建者';
comment on column novel.book_index.update_time is '更新时间';
comment on column novel.book_index.update_by is '更新者';

-- =========================== 小说爬虫源站表 ===========================
drop table if exists novel.crawl_source;
create table novel.crawl_source
(
    id          bigserial not null
        constraint crawl_source_pk primary key,
    source_name varchar(64),
    crawl_rule  jsonb   default '{}'::jsonb,
    status      char(1) default '0',
    remark      text,
    create_time timestamptz,
    create_by   varchar(64),
    update_time timestamptz,
    update_by   varchar(64)
);
comment on table novel.crawl_source is '小说爬虫源站表';
comment on column novel.crawl_source.id is '主键ID';
comment on column novel.crawl_source.source_name is '源站名称';
comment on column novel.crawl_source.crawl_rule is '爬虫规则';
comment on column novel.crawl_source.status is '爬虫状态: 0关闭, 1开启, 2已删除';
comment on column novel.crawl_source.create_time is '创建时间';
comment on column novel.crawl_source.create_by is '创建者';
comment on column novel.crawl_source.update_time is '更新时间';
comment on column novel.crawl_source.update_by is '更新者';

-- =========================== 小说爬虫源与小说映射表 ===========================
drop table if exists novel.crawl_book;
create table novel.crawl_book
(
    id bigserial not null
        constraint crawl_book_pk primary key,
    crawl_id int8,
    book_id varchar(24),
    create_time    timestamptz default now(),
    create_by      varchar(64),
    update_time    timestamptz,
    update_by      varchar(64)
);
comment on table novel.crawl_book is '小说爬虫爬取记录表';
comment on column novel.crawl_book.id is '主键ID';
comment on column novel.crawl_book.crawl_id is '爬虫源ID';
comment on column novel.crawl_book.book_id is '爬取书籍ID';
comment on column novel.crawl_book.create_time is '创建时间';
comment on column novel.crawl_book.create_by is '创建者';
comment on column novel.crawl_book.update_time is '更新时间';
comment on column novel.crawl_book.update_by is '更新者';

-- =========================== 小说爬虫爬取记录表 ===========================
drop table if exists novel.crawl_record;
create table novel.crawl_record
(
    id             bigserial not null
        constraint crawl_record_pk primary key,
    crawl_id      int8,
    book_id int8,
    status         char(1) default '0',
    exec_count     int2,
    index_count    int2,
    create_time    timestamptz default now(),
    create_by      varchar(64),
    update_time    timestamptz,
    update_by      varchar(64)
);

comment on table novel.crawl_record is '小说爬虫爬取记录表';
comment on column novel.crawl_record.id is '主键ID';
comment on column novel.crawl_record.crawl_id is '爬虫源ID';
comment on column novel.crawl_record.book_id is '爬取书籍ID';
comment on column novel.crawl_record.status is '状态: 0失败, 1成功, 2未执行';
comment on column novel.crawl_record.exec_count is '执行次数';
comment on column novel.crawl_record.index_count is '获取的章节数';
comment on column novel.crawl_record.create_time is '创建时间';
comment on column novel.crawl_record.create_by is '创建者';
comment on column novel.crawl_record.update_time is '更新时间';
comment on column novel.crawl_record.update_by is '更新者';

-- =========================== 小说与爬虫爬取记录关联表 ===========================
-- 书籍关联最新的一条爬虫爬取记录
drop table if exists novel.book_crawl_record;
create table novel.book_crawl_record
(
    book_id   int8,
    record_id int8
);

comment on table novel.book_crawl_record is '小说爬虫爬取记录表';
comment on column novel.book_crawl_record.book_id is '书籍ID';
comment on column novel.book_crawl_record.record_id is '爬取记录ID';

-- =========================== 小说字典类型表 ===========================
drop table if exists novel.book_dict_type;
create table novel.book_dict_type
(
    id          bigserial not null
        constraint book_dict_type_pk primary key,
    dict_name   varchar(64),
    dict_type   varchar(64),
    status      char(1),
    create_time timestamptz,
    create_by   varchar(64),
    update_time timestamptz,
    update_by   varchar(64),
    remark      text
);

comment on table novel.book_dict_type is '小说字典类型表';
comment on column novel.book_dict_type.id is '主键ID';
comment on column novel.book_dict_type.dict_name is '字典名称';
comment on column novel.book_dict_type.dict_type is '字典类型';
comment on column novel.book_dict_type.status is '状态: 0正常, 1禁用';
comment on column novel.book_dict_type.create_time is '创建时间';
comment on column novel.book_dict_type.create_by is '创建者';
comment on column novel.book_dict_type.update_time is '更新时间';
comment on column novel.book_dict_type.update_by is '更新者';
comment on column novel.book_dict_type.remark is '备注';

insert into novel.book_dict_type (dict_name, dict_type, status, create_time, create_by, remark)
values ('小说类别', 'book_type', '0', now(), 'admin', ''),
       ('小说tags', 'book_tags', '0', now(), 'admin', '小说tag列表')
;

-- =========================== 小说字典数据表 ===========================
drop table if exists novel.book_dict_data;
create table novel.book_dict_data
(
    id          bigserial                not null
        constraint book_dict_data_pk primary key,
    dict_label  varchar(128) default ''  not null,
    dict_value  varchar(128) default ''  not null,
    dict_type   varchar(64)  default ''  not null,
    is_default  char(1)      default 'N' not null,
    status      char(1)      default '0' not null,
    create_time timestamptz,
    create_by   varchar(64),
    update_time timestamptz,
    update_by   varchar(64),
    remark      varchar(500)
);

comment on table novel.book_dict_data is '小说字典数据表';
comment on column novel.book_dict_data.id is '主键ID';
comment on column novel.book_dict_data.dict_label is '字典标签名';
comment on column novel.book_dict_data.dict_value is '字典值';
comment on column novel.book_dict_data.dict_type is '字典类型';
comment on column novel.book_dict_data.is_default is '默认值: Y是, N不是';
comment on column novel.book_dict_data.status is '状态: 0正常, 1禁用';
comment on column novel.book_dict_data.create_time is '创建时间';
comment on column novel.book_dict_data.create_by is '创建者';
comment on column novel.book_dict_data.update_time is '更新时间';
comment on column novel.book_dict_data.update_by is '更新者';
comment on column novel.book_dict_data.remark is '备注';

insert into novel.book_dict_data (dict_label, dict_value, dict_type, is_default, status, create_time, create_by, remark)
values ('原创-言情-古色古香-爱情', '1', 'book_type', 'Y', '0', now(), 'admin', ''),
       ('宫廷侯爵', '1', 'book_tags', 'N', '0', now(), 'admin', ''),
       ('天作之合', '2', 'book_tags', 'N', '0', now(), 'admin', ''),
       ('种田文', '3', 'book_tags', 'N', '0', now(), 'admin', ''),
       ('重生', '4', 'book_tags', 'N', '0', now(), 'admin', ''),
       ('打脸', '5', 'book_tags', 'N', '0', now(), 'admin', ''),
       ('正剧', '6', 'book_tags', 'N', '0', now(), 'admin', '')
;