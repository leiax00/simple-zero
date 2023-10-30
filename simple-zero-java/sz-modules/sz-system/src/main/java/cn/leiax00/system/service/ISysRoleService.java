package cn.leiax00.system.service;

import cn.leiax00.system.api.domain.SysRole;

import java.util.List;
import java.util.Set;

public interface ISysRoleService {
    Set<String> getRolePermissionByUserId(Long userId);

    List<SysRole> selectRoleAll();

    List<SysRole> selectRolesByUserId(Long userId);
}
