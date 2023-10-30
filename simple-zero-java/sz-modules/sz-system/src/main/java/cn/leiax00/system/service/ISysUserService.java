package cn.leiax00.system.service;

import cn.leiax00.system.api.domain.SysUser;

import java.util.List;

public interface ISysUserService {
    List<SysUser> selectUserList(SysUser user);

    SysUser selectUserById(Long userId);

    void checkUserDataScope(Long userId);

    boolean checkUserNameUnique(SysUser user);

    boolean checkPhoneUnique(SysUser user);

    boolean checkEmailUnique(SysUser user);

    void checkUserAllowed(SysUser user);

    int insertUser(SysUser user);

    int deleteUserByIds(Long[] userIds);

    int updateUser(SysUser user);

    void insertUserAuth(Long userId, Long[] roleIds);

    int resetPwd(SysUser user);

    int updateUserStatus(SysUser user);

    SysUser selectUserByUserName(String username);
}
