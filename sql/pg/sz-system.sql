-- --------------------------------- 部门表 -----------------------------------------
-- 删除表，如果存在
DROP TABLE IF EXISTS sys_dept;

-- 创建表
CREATE TABLE sys_dept
(
    dept_id     bigserial PRIMARY KEY NOT NULL,
    parent_id   bigint      DEFAULT 0,
    ancestors   VARCHAR(50) DEFAULT '',
    dept_name   VARCHAR(30) DEFAULT '',
    order_num   INT         DEFAULT 0,
    leader      VARCHAR(20) DEFAULT NULL,
    phone       VARCHAR(11) DEFAULT NULL,
    email       VARCHAR(50) DEFAULT NULL,
    status      CHAR(1)     DEFAULT '0',
    del_flag    CHAR(1)     DEFAULT '0',
    create_by   VARCHAR(64) DEFAULT '',
    create_time timestamptz,
    update_by   VARCHAR(64) DEFAULT '',
    update_time timestamptz
);

-- 添加注释
COMMENT ON COLUMN sys_dept.dept_id IS '部门id';
COMMENT ON COLUMN sys_dept.parent_id IS '父部门id';
COMMENT ON COLUMN sys_dept.ancestors IS '祖级列表';
COMMENT ON COLUMN sys_dept.dept_name IS '部门名称';
COMMENT ON COLUMN sys_dept.order_num IS '显示顺序';
COMMENT ON COLUMN sys_dept.leader IS '负责人';
COMMENT ON COLUMN sys_dept.phone IS '联系电话';
COMMENT ON COLUMN sys_dept.email IS '邮箱';
COMMENT ON COLUMN sys_dept.status IS '部门状态（0正常 1停用）';
COMMENT ON COLUMN sys_dept.del_flag IS '删除标志（0代表存在 2代表删除）';
COMMENT ON COLUMN sys_dept.create_by IS '创建者';
COMMENT ON COLUMN sys_dept.create_time IS '创建时间';
COMMENT ON COLUMN sys_dept.update_by IS '更新者';
COMMENT ON COLUMN sys_dept.update_time IS '更新时间';

-- ----------------------------
-- 初始化-部门表数据
insert into sys_dept
values (100, 0, '0', 'Simple Zero', 0, 'leiax00', '18200118152', 'leiax00@outlook.com', '0', '0', 'leiax00', NOW(), '',
        null);

-- ----------------------------

-- --------------------------------- 用户信息表 -----------------------------------------
-- 删除表，如果存在
DROP TABLE IF EXISTS sys_user;

-- 创建表
CREATE TABLE sys_user
(
    user_id      bigserial PRIMARY KEY NOT NULL,
    dept_id      bigint       DEFAULT NULL,
    user_name    varchar(30)           NOT NULL,
    nick_name    varchar(30)           NOT NULL,
    user_type    varchar(2)   DEFAULT '00',
    email        varchar(50)  DEFAULT '',
    phone_number varchar(11)  DEFAULT '',
    sex          char(1)      DEFAULT '0',
    avatar       varchar(100) DEFAULT '',
    password     varchar(100) DEFAULT '',
    status       char(1)      DEFAULT '0',
    del_flag     char(1)      DEFAULT '0',
    login_ip     varchar(128) DEFAULT '',
    login_date   timestamptz,
    create_by    varchar(64)  DEFAULT '',
    create_time  timestamptz,
    update_by    varchar(64)  DEFAULT '',
    update_time  timestamptz,
    remark       varchar(500) DEFAULT NULL
);

-- 为表的列添加注释
COMMENT ON COLUMN sys_user.user_id IS '用户ID';
COMMENT ON COLUMN sys_user.dept_id IS '部门ID';
COMMENT ON COLUMN sys_user.user_name IS '用户账号';
COMMENT ON COLUMN sys_user.nick_name IS '用户昵称';
COMMENT ON COLUMN sys_user.user_type IS '用户类型（00系统用户）';
COMMENT ON COLUMN sys_user.email IS '用户邮箱';
COMMENT ON COLUMN sys_user.phone_number IS '手机号码';
COMMENT ON COLUMN sys_user.sex IS '用户性别（0男 1女 2未知）';
COMMENT ON COLUMN sys_user.avatar IS '头像地址';
COMMENT ON COLUMN sys_user.password IS '密码';
COMMENT ON COLUMN sys_user.status IS '帐号状态（0正常 1停用）';
COMMENT ON COLUMN sys_user.del_flag IS '删除标志（0代表存在 2代表删除）';
COMMENT ON COLUMN sys_user.login_ip IS '最后登录IP';
COMMENT ON COLUMN sys_user.login_date IS '最后登录时间';
COMMENT ON COLUMN sys_user.create_by IS '创建者';
COMMENT ON COLUMN sys_user.create_time IS '创建时间';
COMMENT ON COLUMN sys_user.update_by IS '更新者';
COMMENT ON COLUMN sys_user.update_time IS '更新时间';
COMMENT ON COLUMN sys_user.remark IS '备注';

-- ----------------------------
-- 初始化-用户信息表数据
insert into sys_user
values (1, 100, 'leiax00', 'leiax00', '00', 'leiax00@outlook.com', '18200118152', '0', '',
        '$2a$10$JlgGhrb4Rfyz1Ja/0Y20UuucVxha5mOsggVoV3voU82fXQjXDkpJi', '0', '0', '127.0.0.1', now(), 'leiax00', now(),
        '', null, '管理员');
-- ----------------------------

-- --------------------------------- 角色信息表 -----------------------------------------
-- 删除表，如果存在
DROP TABLE IF EXISTS sys_role;

-- 创建表
CREATE TABLE sys_role
(
    role_id             bigserial PRIMARY KEY NOT NULL,
    role_name           varchar(30)           NOT NULL,
    role_key            varchar(100)          NOT NULL,
    role_sort           int                   NOT NULL,
    data_scope          char(1)     DEFAULT '1',
    menu_check_strictly smallint    DEFAULT 1,
    dept_check_strictly smallint    DEFAULT 1,
    status              char(1)               NOT NULL,
    del_flag            char(1)     DEFAULT '0',
    create_by           varchar(64) DEFAULT '',
    create_time         timestamptz,
    update_by           varchar(64) DEFAULT '',
    update_time         timestamptz,
    remark              varchar(500)
);

-- 为表添加注释
COMMENT ON TABLE sys_role IS '角色信息表';
COMMENT ON COLUMN sys_role.role_id IS '角色ID';
COMMENT ON COLUMN sys_role.role_name IS '角色名称';
COMMENT ON COLUMN sys_role.role_key IS '角色权限字符串';
COMMENT ON COLUMN sys_role.role_sort IS '显示顺序';
COMMENT ON COLUMN sys_role.data_scope IS '数据范围（1：全部数据权限 2：自定数据权限 3：本部门数据权限 4：本部门及以下数据权限）';
COMMENT ON COLUMN sys_role.menu_check_strictly IS '菜单树选择项是否关联显示';
COMMENT ON COLUMN sys_role.dept_check_strictly IS '部门树选择项是否关联显示';
COMMENT ON COLUMN sys_role.status IS '角色状态（0正常 1停用）';
COMMENT ON COLUMN sys_role.del_flag IS '删除标志（0代表存在 2代表删除）';
COMMENT ON COLUMN sys_role.create_by IS '创建者';
COMMENT ON COLUMN sys_role.create_time IS '创建时间';
COMMENT ON COLUMN sys_role.update_by IS '更新者';
COMMENT ON COLUMN sys_role.update_time IS '更新时间';
COMMENT ON COLUMN sys_role.remark IS '备注';

-- ----------------------------
-- 初始化-角色信息表数据
insert into sys_role
values ('1', '超级管理员', 'admin', 1, 1, 1, 1, '0', '0', 'leiax00', now(), '', null, '超级管理员');
insert into sys_role
values ('2', '普通角色', 'common', 2, 2, 1, 1, '0', '0', 'leiax00', now(), '', null, '普通角色');
-- ----------------------------

-- --------------------------------- 菜单权限信息表 -----------------------------------------
-- 删除表，如果存在
DROP TABLE IF EXISTS sys_menu;

-- 创建表
CREATE TABLE sys_menu
(
    menu_id     bigserial PRIMARY KEY NOT NULL,
    menu_name   varchar(50)           NOT NULL,
    parent_id   bigint       DEFAULT 0,
    order_num   int          DEFAULT 0,
    path        varchar(200) DEFAULT '',
    component   varchar(255),
    query       varchar(255),
    is_frame    int          DEFAULT 1,
    is_cache    int          DEFAULT 0,
    menu_type   char(1)      DEFAULT '',
    visible     char(1)      DEFAULT '0',
    status      char(1)      DEFAULT '0',
    perms       varchar(100),
    icon        varchar(100) DEFAULT '#',
    create_by   varchar(64)  DEFAULT '',
    create_time timestamptz,
    update_by   varchar(64)  DEFAULT '',
    update_time timestamptz,
    remark      varchar(500) DEFAULT ''
);

-- 设置序列起始值
SELECT setval('sys_menu_menu_id_seq', 5000);

-- 添加注释
COMMENT ON TABLE sys_menu IS '菜单权限表';
COMMENT ON COLUMN sys_menu.menu_id IS '菜单ID';
COMMENT ON COLUMN sys_menu.menu_name IS '菜单名称';
COMMENT ON COLUMN sys_menu.parent_id IS '父菜单ID';
COMMENT ON COLUMN sys_menu.order_num IS '显示顺序';
COMMENT ON COLUMN sys_menu.path IS '路由地址';
COMMENT ON COLUMN sys_menu.component IS '组件路径';
COMMENT ON COLUMN sys_menu.query IS '路由参数';
COMMENT ON COLUMN sys_menu.is_frame IS '是否为外链（0是 1否）';
COMMENT ON COLUMN sys_menu.is_cache IS '是否缓存（0缓存 1不缓存）';
COMMENT ON COLUMN sys_menu.menu_type IS '菜单类型（M目录 C菜单 F按钮）';
COMMENT ON COLUMN sys_menu.visible IS '菜单状态（0显示 1隐藏）';
COMMENT ON COLUMN sys_menu.status IS '菜单状态（0正常 1停用）';
COMMENT ON COLUMN sys_menu.perms IS '权限标识';
COMMENT ON COLUMN sys_menu.icon IS '菜单图标';
COMMENT ON COLUMN sys_menu.create_by IS '创建者';
COMMENT ON COLUMN sys_menu.create_time IS '创建时间';
COMMENT ON COLUMN sys_menu.update_by IS '更新者';
COMMENT ON COLUMN sys_menu.update_time IS '更新时间';
COMMENT ON COLUMN sys_menu.remark IS '备注';

-- ----------------------------
-- 初始化-菜单信息表数据
-- ----------------------------

-- --------------------------------- 用户和角色关联表  用户N-1角色 -----------------------------------------
-- 删除表，如果存在
DROP TABLE IF EXISTS sys_user_role;

-- 创建表
CREATE TABLE sys_user_role
(
    user_id bigint NOT NULL,
    role_id bigint NOT NULL,
    PRIMARY KEY (user_id, role_id)
);

-- 添加注释
COMMENT ON TABLE sys_user_role IS '用户和角色关联表';
COMMENT ON COLUMN sys_user_role.user_id IS '用户ID';
COMMENT ON COLUMN sys_user_role.role_id IS '角色ID';

-- ----------------------------
-- 初始化-用户和角色关联表数据
insert into sys_user_role
values ('1', '1');
-- ----------------------------

-- --------------------------------- 角色和菜单关联表  角色1-N菜单 -----------------------------------------
drop table if exists sys_role_menu;
create table sys_role_menu
(
    role_id bigint NOT NULL,
    menu_id bigint NOT NULL,
    PRIMARY KEY (role_id, menu_id)
);

-- 添加注释
COMMENT ON TABLE sys_role_menu IS '角色和菜单关联表';
COMMENT ON COLUMN sys_role_menu.role_id IS '角色ID';
COMMENT ON COLUMN sys_role_menu.menu_id IS '菜单ID';

-- ----------------------------
-- 初始化-用户和角色关联表数据
-- ----------------------------

-- --------------------------------- 角色和部门关联表  角色1-N部门 -----------------------------------------
drop table if exists sys_role_dept;
create table sys_role_dept
(
    role_id bigint not null,
    dept_id bigint not null,
    primary key (role_id, dept_id)
);

-- 添加注释
COMMENT ON TABLE sys_role_dept IS '角色和部门关联表';
COMMENT ON COLUMN sys_role_dept.role_id IS '角色ID';
COMMENT ON COLUMN sys_role_dept.dept_id IS '部门ID';
-- ----------------------------
-- 初始化-角色和部门关联表数据
-- ----------------------------

-- --------------------------------- 字典类型表 -----------------------------------------
drop table if exists sys_dict_type;
create table sys_dict_type
(
    dict_id     bigserial not null,
    dict_name   varchar(100) default '',
    dict_type   varchar(100) default '',
    status      char(1)      default '0',
    create_by   varchar(64)  default '',
    create_time timestamptz,
    update_by   varchar(64)  default '',
    update_time timestamptz,
    remark      varchar(500) default null,
    primary key (dict_id),
    unique (dict_type)
);

-- 添加注释
COMMENT ON TABLE sys_dict_type IS '字典类型表';
COMMENT ON COLUMN sys_dict_type.dict_id IS '字典主键';
COMMENT ON COLUMN sys_dict_type.dict_name IS '字典名称';
COMMENT ON COLUMN sys_dict_type.dict_type IS '字典类型';
COMMENT ON COLUMN sys_dict_type.status IS '状态（0正常 1停用）';
COMMENT ON COLUMN sys_dict_type.create_by IS '创建者';
COMMENT ON COLUMN sys_dict_type.create_time IS '创建时间';
COMMENT ON COLUMN sys_dict_type.update_by IS '更新者';
COMMENT ON COLUMN sys_dict_type.update_time IS '更新时间';
COMMENT ON COLUMN sys_dict_type.remark IS '备注';

-- ----------------------------
-- 初始化-字典类型表数据
insert into sys_dict_type
values (1, '用户性别', 'sys_user_sex', '0', 'leiax00', now(), '', null, '用户性别列表');
-- ----------------------------

-- --------------------------------- 字典数据表 -----------------------------------------
-- 删除表，如果存在
DROP TABLE IF EXISTS sys_dict_data;

-- 创建表
CREATE TABLE sys_dict_data
(
    dict_code   bigserial NOT NULL PRIMARY KEY,
    dict_sort   int          DEFAULT 0,
    dict_label  varchar(100) DEFAULT '',
    dict_value  varchar(100) DEFAULT '',
    dict_type   varchar(100) DEFAULT '',
    css_class   varchar(100),
    list_class  varchar(100),
    is_default  char(1)      DEFAULT 'N',
    status      char(1)      DEFAULT '0',
    create_by   varchar(64)  DEFAULT '',
    create_time timestamptz,
    update_by   varchar(64)  DEFAULT '',
    update_time timestamptz,
    remark      varchar(500)
);

-- 为表的列添加注释
COMMENT ON COLUMN sys_dict_data.dict_code IS '字典编码';
COMMENT ON COLUMN sys_dict_data.dict_sort IS '字典排序';
COMMENT ON COLUMN sys_dict_data.dict_label IS '字典标签';
COMMENT ON COLUMN sys_dict_data.dict_value IS '字典键值';
COMMENT ON COLUMN sys_dict_data.dict_type IS '字典类型';
COMMENT ON COLUMN sys_dict_data.css_class IS '样式属性（其他样式扩展）';
COMMENT ON COLUMN sys_dict_data.list_class IS '表格回显样式';
COMMENT ON COLUMN sys_dict_data.is_default IS '是否默认（Y是 N否）';
COMMENT ON COLUMN sys_dict_data.status IS '状态（0正常 1停用）';
COMMENT ON COLUMN sys_dict_data.create_by IS '创建者';
COMMENT ON COLUMN sys_dict_data.create_time IS '创建时间';
COMMENT ON COLUMN sys_dict_data.update_by IS '更新者';
COMMENT ON COLUMN sys_dict_data.update_time IS '更新时间';
COMMENT ON COLUMN sys_dict_data.remark IS '备注';

-- 为表添加注释
COMMENT ON TABLE sys_dict_data IS '字典数据表';

-- ----------------------------
-- 初始化-字典数据表数据
insert into sys_dict_data
values (1, 1, '男', '0', 'sys_user_sex', '', '', 'Y', '0', 'leiax00', now(), '', null, '性别男');
insert into sys_dict_data
values (2, 2, '女', '1', 'sys_user_sex', '', '', 'N', '0', 'leiax00', now(), '', null, '性别女');
insert into sys_dict_data
values (3, 3, '未知', '2', 'sys_user_sex', '', '', 'N', '0', 'leiax00', now(), '', null, '性别未知');
-- ----------------------------