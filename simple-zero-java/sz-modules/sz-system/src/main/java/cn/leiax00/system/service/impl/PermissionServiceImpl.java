package cn.leiax00.system.service.impl;

import cn.leiax00.system.api.domain.SysRole;
import cn.leiax00.system.api.domain.SysUser;
import cn.leiax00.system.service.IPermissionService;
import cn.leiax00.system.service.ISysMenuService;
import cn.leiax00.system.service.ISysRoleService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.util.CollectionUtils;

import java.util.HashSet;
import java.util.List;
import java.util.Set;

@Service
public class PermissionServiceImpl implements IPermissionService {
    @Autowired
    private ISysRoleService roleService;

    @Autowired
    private ISysMenuService menuService;

    @Override
    public Set<String> getRolePermission(SysUser user) {
        Set<String> permissionSet = new HashSet<>();
        if (user.isAdmin()) {
            permissionSet.add("admin");
        } else {
            permissionSet.addAll(roleService.getRolePermissionByUserId(user.getUserId()));
        }
        return permissionSet;
    }

    @Override
    public Set<String> getMenuPermission(SysUser user) {
        Set<String> permissionSet = new HashSet<>();
        if (user.isAdmin()) {
            permissionSet.add("*:*:*");
        } else {
            List<SysRole> roles = user.getRoles();
            if (!CollectionUtils.isEmpty(roles)) {
                // 多角色设置permissions属性，以便数据权限匹配权限
                for (SysRole role : roles) {
                    Set<String> rolePerms = menuService.selectMenuPermsByRoleId(role.getRoleId());
                    role.setPermissions(rolePerms);
                    permissionSet.addAll(rolePerms);
                }
            } else {
                permissionSet.addAll(menuService.selectMenuPermsByUserId(user.getUserId()));
            }
        }
        return permissionSet;
    }
}
