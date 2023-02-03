/*
 Navicat Premium Data Transfer

 Source Server         : pgsql@10.1.0.3
 Source Server Type    : PostgreSQL
 Source Server Version : 120013 (120013)
 Source Host           : 10.1.0.3:5432
 Source Catalog        : simple-zero
 Source Schema         : novel

 Target Server Type    : PostgreSQL
 Target Server Version : 120013 (120013)
 File Encoding         : 65001

 Date: 06/01/2023 18:12:44
*/

CREATE SCHEMA IF NOT EXISTS "novel" AUTHORIZATION "postgres";
CREATE SEQUENCE IF NOT EXISTS "novel"."serial"
    INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 10
CYCLE;

SELECT setval('"novel"."serial"', 10, true);

ALTER SEQUENCE "novel"."serial" OWNER TO "postgres";


-- ----------------------------
-- Table structure for book
-- ----------------------------
DROP TABLE IF EXISTS "novel"."book";
CREATE TABLE "novel"."book"
(
    "bid"         varchar(64)  NOT NULL,
    "name"        varchar(128) NOT NULL,
    "author"      varchar(128),
    "type"        varchar(32),
    "icon"        varchar(255),
    "desc"        text,
    "update_time" varchar(64),
    "group_name"  varchar(255) NOT NULL DEFAULT 'default':: character varying
)
;

-- ----------------------------
-- Primary Key structure for table book
-- ----------------------------
ALTER TABLE "novel"."book"
    ADD CONSTRAINT "book_pkey" PRIMARY KEY ("bid");

-- ----------------------------
-- Table structure for book_record
-- ----------------------------
DROP TABLE IF EXISTS "novel"."book_record";
CREATE TABLE "novel"."book_record"
(
    "bid"        varchar(64)  NOT NULL,
    "group_name" varchar(255) NOT NULL,
    "cid"        varchar(64)  NOT NULL,
    "c_name"     varchar(255),
    "percent"    int4 DEFAULT 0
)
;

-- ----------------------------
-- Primary Key structure for table book_record
-- ----------------------------
ALTER TABLE "novel"."book_record"
    ADD CONSTRAINT "book_record_pkey" PRIMARY KEY ("bid", "group_name");


DROP TABLE IF EXISTS "novel"."book_catalog";
CREATE TABLE "novel"."book_catalog"
(
    "id"       int4        NOT NULL DEFAULT nextval('"novel".serial'::regclass),
    "bid"      varchar(64) NOT NULL,
    "cid"      varchar(64) NOT NULL,
    "name"     varchar(255),
    "prev_cid" varchar(64),
    "next_cid" varchar(64)
)
;

-- ----------------------------
-- Indexes structure for table book_catalog
-- ----------------------------
CREATE INDEX "book_catalog_bid_cid_idx" ON "novel"."book_catalog" USING btree (
    "bid" "pg_catalog"."text_ops" ASC NULLS LAST,
    "cid" "pg_catalog"."text_ops" ASC NULLS LAST
    );

-- ----------------------------
-- Primary Key structure for table book_catalog
-- ----------------------------
ALTER TABLE "novel"."book_catalog"
    ADD CONSTRAINT "book_catalog_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Table structure for book_chapter
-- ----------------------------
DROP TABLE IF EXISTS "novel"."book_chapter";
CREATE TABLE "novel"."book_chapter"
(
    "id"      int4 NOT NULL,
    "content" text
)
;

-- ----------------------------
-- Primary Key structure for table book_chapter
-- ----------------------------
ALTER TABLE "novel"."book_chapter"
    ADD CONSTRAINT "book_chapter_pkey" PRIMARY KEY ("id");
