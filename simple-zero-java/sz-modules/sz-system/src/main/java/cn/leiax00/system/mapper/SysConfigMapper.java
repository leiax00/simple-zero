package cn.leiax00.system.mapper;

import cn.leiax00.system.api.domain.SysConfig;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface SysConfigMapper extends BaseMapper<SysConfig> {
    List<SysConfig> selectConfigList(SysConfig sysConfig);

    SysConfig checkConfigKeyUnique(String configKey);

    SysConfig selectConfig(SysConfig config);
}
