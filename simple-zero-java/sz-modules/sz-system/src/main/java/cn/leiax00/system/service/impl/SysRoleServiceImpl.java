package cn.leiax00.system.service.impl;

import cn.leiax00.common.core.utils.StringUtils;
import cn.leiax00.system.api.domain.SysRole;
import cn.leiax00.system.mapper.SysRoleMapper;
import cn.leiax00.system.service.ISysRoleService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

@Service
public class SysRoleServiceImpl implements ISysRoleService {
    @Autowired
    private SysRoleMapper sysRoleMapper;

    @Override
    public Set<String> getRolePermissionByUserId(Long userId) {
        List<SysRole> roleList = sysRoleMapper.getRolePermissionByUserId(userId);
        Set<String> rolePermissionSet = new HashSet<>();
        roleList.forEach(item -> {
            if (StringUtils.isNotNull(item)) {
                rolePermissionSet.addAll(Arrays.asList(item.getRoleKey().trim().split(",")));
            }
        });
        return rolePermissionSet;
    }

    @Override
    public List<SysRole> selectRoleAll() {
        return sysRoleMapper.selectList(null);
    }

    @Override
    public List<SysRole> selectRolesByUserId(Long userId) {
        List<SysRole> userRoles = sysRoleMapper.selectRolePermissionByUserId(userId);
        List<SysRole> roles = selectRoleAll();
        for (SysRole role : roles) {
            for (SysRole userRole : userRoles) {
                if (role.getRoleId().longValue() == userRole.getRoleId().longValue()) {
                    role.setFlag(true);
                    break;
                }
            }
        }
        return roles;
    }
}
