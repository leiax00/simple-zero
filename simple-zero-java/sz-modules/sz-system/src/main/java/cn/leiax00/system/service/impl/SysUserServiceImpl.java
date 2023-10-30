package cn.leiax00.system.service.impl;

import cn.leiax00.common.core.exception.ServiceException;
import cn.leiax00.common.core.utils.SpringUtils;
import cn.leiax00.common.core.utils.StringUtils;
import cn.leiax00.common.datascope.annotation.DataScope;
import cn.leiax00.common.security.utils.SecurityUtils;
import cn.leiax00.system.api.domain.SysUser;
import cn.leiax00.system.api.domain.SysUserRole;
import cn.leiax00.system.mapper.SysUserMapper;
import cn.leiax00.system.mapper.SysUserRoleMapper;
import cn.leiax00.system.service.ISysUserService;
import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.core.metadata.TableFieldInfo;
import com.baomidou.mybatisplus.core.toolkit.Wrappers;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.ArrayList;
import java.util.List;
import java.util.function.Predicate;

@Service
public class SysUserServiceImpl implements ISysUserService {

    @Autowired
    private SysUserMapper userMapper;

    @Autowired
    private SysUserRoleMapper userRoleMapper;

    @Override
    @DataScope(deptAlias = "d", userAlias = "u")
    public List<SysUser> selectUserList(SysUser user) {
        return userMapper.selectUserList(user);
    }

    @Override
    public SysUser selectUserById(Long userId) {
        return userMapper.selectUserById(userId);
    }

    @Override
    public void checkUserDataScope(Long userId) {
        if (!SysUser.isAdmin(SecurityUtils.getUserId())) {
            SysUser user = new SysUser();
            user.setUserId(userId);
            List<SysUser> users = SpringUtils.getAopProxy(this).selectUserList(user);
            if (StringUtils.isEmpty(users)) {
                throw new ServiceException("没有权限访问用户数据！");
            }
        }
    }

    @Override
    public boolean checkUserNameUnique(SysUser user) {
        long userId = StringUtils.isNull(user.getUserId()) ? -1L : user.getUserId();
        return userMapper.selectCount(
                Wrappers.lambdaQuery(SysUser.class)
                        .eq(SysUser::getUserName, user.getUserName())
                        .ne(SysUser::getUserId, userId)
        ) <= 0;
    }

    @Override
    public boolean checkPhoneUnique(SysUser user) {
        long userId = StringUtils.isNull(user.getUserId()) ? -1L : user.getUserId();
        return userMapper.selectCount(
                Wrappers.lambdaQuery(SysUser.class)
                        .eq(SysUser::getPhoneNumber, user.getPhoneNumber())
                        .ne(SysUser::getUserId, userId)
        ) <= 0;
    }

    @Override
    public boolean checkEmailUnique(SysUser user) {
        long userId = StringUtils.isNull(user.getUserId()) ? -1L : user.getUserId();
        return userMapper.selectCount(
                Wrappers.lambdaQuery(SysUser.class)
                        .eq(SysUser::getEmail, user.getEmail())
                        .ne(SysUser::getUserId, userId)
        ) <= 0;
    }

    @Override
    public void checkUserAllowed(SysUser user) {
        if (StringUtils.isNotNull(user.getUserId()) && user.isAdmin()) {
            throw new ServiceException("不允许操作超级管理员用户");
        }
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public int insertUser(SysUser user) {
        int rows = userMapper.insertUser(user);
        insertUserRole(user);
        return rows;
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public int deleteUserByIds(Long[] userIds) {
        for (Long userId : userIds) {
            checkUserAllowed(new SysUser(userId));
            checkUserDataScope(userId);
        }
        // 删除用户与角色关联
        userRoleMapper.deleteUserRole(userIds);
        return userMapper.deleteUserByIds(userIds);
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public int updateUser(SysUser user) {
        Long userId = user.getUserId();
        // 删除用户与角色关联
        userRoleMapper.deleteUserRoleByUserId(userId);
        // 新增用户与角色管理
        insertUserRole(user);
        return userMapper.updateUser(user);
    }

    @Override
    public void insertUserAuth(Long userId, Long[] roleIds) {
        userRoleMapper.deleteUserRoleByUserId(userId);
        insertUserRole(userId, roleIds);
    }

    @Override
    public int resetPwd(SysUser user) {
        return userMapper.updateUser(user);
    }

    @Override
    public int updateUserStatus(SysUser user)
    {
        return userMapper.updateUser(user);
    }

    @Override
    public SysUser selectUserByUserName(String username) {
        return userMapper.selectUserByUserName(username);
    }

    public void insertUserRole(SysUser user) {
        this.insertUserRole(user.getUserId(), user.getRoleIds());
    }

    public void insertUserRole(Long userId, Long[] roleIds) {
        if (StringUtils.isNotEmpty(roleIds)) {
            // 新增用户与角色管理
            List<SysUserRole> list = new ArrayList<SysUserRole>();
            for (Long roleId : roleIds) {
                SysUserRole ur = new SysUserRole();
                ur.setUserId(userId);
                ur.setRoleId(roleId);
                list.add(ur);
            }
            this.userRoleMapper.batchUserRole(list);
        }
    }

    public List<SysUser> selectList(SysUser user) {
        QueryWrapper<SysUser> queryWrapper = Wrappers.query(user);

        queryWrapper.select(SysUser.class, this.getSysUserPlusField(false));
        return userMapper.selectList(queryWrapper);
    }

    /**
     * 做一些字段过滤, 过滤的字段不会查询
     *
     * @param showPwd 是否显示密码字段
     */
    private Predicate<TableFieldInfo> getSysUserPlusField(boolean showPwd) {
        return info -> {
            List<String> fieldList = new ArrayList<>();
            if (!showPwd) {
                fieldList.add("password");
            }
            for (String field : fieldList) {
                if (info.getProperty().equals(field)) {
                    return false;
                }
            }
            return true;
        };
    }

}
