package cn.leiax00.system.service;

import cn.leiax00.system.api.domain.SysUser;

import java.util.Set;

public interface IPermissionService {
    Set<String> getRolePermission(SysUser user);

    Set<String> getMenuPermission(SysUser user);
}
