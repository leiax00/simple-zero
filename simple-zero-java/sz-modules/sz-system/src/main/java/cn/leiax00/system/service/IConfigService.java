package cn.leiax00.system.service;

import cn.leiax00.system.api.domain.SysConfig;

public interface IConfigService {
    String selectConfigByKey(String configKey);

    boolean checkConfigKeyUnique(SysConfig config);
}
