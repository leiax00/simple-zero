package cn.leiax00.system.mapper;

import cn.leiax00.system.api.domain.SysMenu;
import cn.leiax00.system.api.domain.SysRole;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface SysMenuMapper extends BaseMapper<SysRole> {
    List<String> selectMenuPermsByUserId(Long userId);

    List<String> selectMenuPermsByRoleId(Long roleId);
}
