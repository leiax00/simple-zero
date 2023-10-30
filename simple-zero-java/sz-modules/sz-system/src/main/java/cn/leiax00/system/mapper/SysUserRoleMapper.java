package cn.leiax00.system.mapper;

import cn.leiax00.system.api.domain.SysUserRole;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface SysUserRoleMapper extends BaseMapper<SysUserRole> {
    int batchUserRole(List<SysUserRole> list);

    int deleteUserRole(Long[] userIds);

    int deleteUserRoleByUserId(Long userId);
}
