package cn.leiax00.system.mapper;

import cn.leiax00.system.api.domain.SysUser;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface SysUserMapper extends BaseMapper<SysUser> {
    List<SysUser> selectUserList(SysUser user);

    SysUser selectUserById(Long userId);

    int deleteUserByIds(Long[] userIds);

    int insertUser(SysUser user);

    int updateUser(SysUser user);

    SysUser selectUserByUserName(String username);
}
