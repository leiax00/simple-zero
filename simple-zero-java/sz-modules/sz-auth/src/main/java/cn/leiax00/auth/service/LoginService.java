package cn.leiax00.auth.service;

import cn.leiax00.api.system.v1.Simple;
import cn.leiax00.common.core.constant.CacheConstants;
import cn.leiax00.common.core.constant.SecurityConstants;
import cn.leiax00.common.core.constant.UserConstants;
import cn.leiax00.common.core.exception.ServiceException;
import cn.leiax00.common.core.text.Convert;
import cn.leiax00.common.core.utils.ProtoUtils;
import cn.leiax00.common.core.utils.StringUtils;
import cn.leiax00.common.core.utils.ip.IpUtils;
import cn.leiax00.common.core.web.domain.R;
import cn.leiax00.common.redis.service.RedisService;
import cn.leiax00.system.api.model.LoginUser;
import cn.leiax00.system.api.service.RemoteUserService;
import cn.leiax00.system.api.service.SimpleServiceClient;
import com.google.protobuf.InvalidProtocolBufferException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Map;

@Service
public class LoginService {

    @Autowired
    private SimpleServiceClient client;

    @Autowired
    private RedisService redisService;

    @Autowired
    private RemoteUserService remoteUserService;

    public LoginUser login(String username, String password) throws InvalidProtocolBufferException {
        if (StringUtils.isAnyBlank(username, password)) {
            throw new ServiceException("用户/密码必须填写");
        }

        if (password.length() < UserConstants.PASSWORD_MIN_LENGTH
                || password.length() > UserConstants.PASSWORD_MAX_LENGTH) {
            throw new ServiceException("用户密码不在指定范围");
        }

        if (username.length() < UserConstants.USERNAME_MIN_LENGTH
                || username.length() > UserConstants.USERNAME_MAX_LENGTH) {
            throw new ServiceException("用户名不在指定范围");
        }

        String blackStr = Convert.toStr(redisService.getCacheObject(CacheConstants.SYS_LOGIN_BLACKIPLIST));
        if (IpUtils.isMatchedIp(blackStr, IpUtils.getIpAddr())) {
            throw new ServiceException("很遗憾，访问IP已被列入系统黑名单");
        }

        R<LoginUser> userResult = this.remoteUserService.getUserInfo(username, SecurityConstants.INNER);
        return userResult.getData();
    }
}
