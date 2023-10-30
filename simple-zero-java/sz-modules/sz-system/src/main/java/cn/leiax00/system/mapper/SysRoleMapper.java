package cn.leiax00.system.mapper;

import cn.leiax00.system.api.domain.SysRole;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface SysRoleMapper extends BaseMapper<SysRole> {
    List<SysRole> getRolePermissionByUserId(Long userId);

    List<SysRole> selectRolePermissionByUserId(Long userId);
}
