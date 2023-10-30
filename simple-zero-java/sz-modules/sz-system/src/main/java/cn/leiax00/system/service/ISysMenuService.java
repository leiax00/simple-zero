package cn.leiax00.system.service;

import java.util.Set;

public interface ISysMenuService {
    Set<String> selectMenuPermsByRoleId(Long roleId);

    Set<String> selectMenuPermsByUserId(Long userId);
}
