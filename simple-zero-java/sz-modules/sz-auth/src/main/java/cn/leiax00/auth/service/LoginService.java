package cn.leiax00.auth.service;

import cn.leiax00.common.core.constant.CacheConstants;
import cn.leiax00.common.core.constant.SecurityConstants;
import cn.leiax00.common.core.constant.UserConstants;
import cn.leiax00.common.core.enums.UserStatus;
import cn.leiax00.common.core.exception.ServiceException;
import cn.leiax00.common.core.text.Convert;
import cn.leiax00.common.core.utils.StringUtils;
import cn.leiax00.common.core.utils.ip.IpUtils;
import cn.leiax00.common.core.web.domain.R;
import cn.leiax00.common.redis.service.RedisService;
import cn.leiax00.common.security.utils.SecurityUtils;
import cn.leiax00.system.api.domain.SysUser;
import cn.leiax00.system.api.model.LoginUser;
import cn.leiax00.system.api.service.RemoteUserService;
import cn.leiax00.system.api.service.SimpleServiceClient;
import com.google.protobuf.InvalidProtocolBufferException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class LoginService {

    @Autowired
    private SimpleServiceClient client;

    @Autowired
    private SysPasswordService passwordService;

    @Autowired
    private RedisService redisService;

    @SuppressWarnings("SpringJavaInjectionPointsAutowiringInspection")
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
        if (StringUtils.isNull(userResult) || StringUtils.isNull(userResult.getData())) {
            throw new ServiceException("登录用户：" + username + " 不存在");
        }
        if (R.FAIL == userResult.getCode()) {
            throw new ServiceException(userResult.getMsg());
        }
        LoginUser userInfo = userResult.getData();
        SysUser user = userResult.getData().getSysUser();
        if (UserStatus.DELETED.getCode().equals(user.getDelFlag())) {
            throw new ServiceException("对不起，您的账号：" + username + " 已被删除");
        }
        if (UserStatus.DISABLE.getCode().equals(user.getStatus())) {
            throw new ServiceException("对不起，您的账号：" + username + " 已停用");
        }
        passwordService.validate(user, password);
        return userInfo;
    }

    public void logout(String username) {

    }

    public void register(String username, String password) {
        // 用户名或密码为空 错误
        if (StringUtils.isAnyBlank(username, password)) {
            throw new ServiceException("用户/密码必须填写");
        }
        if (username.length() < UserConstants.USERNAME_MIN_LENGTH
                || username.length() > UserConstants.USERNAME_MAX_LENGTH) {
            throw new ServiceException("账户长度必须在2到20个字符之间");
        }
        if (password.length() < UserConstants.PASSWORD_MIN_LENGTH
                || password.length() > UserConstants.PASSWORD_MAX_LENGTH) {
            throw new ServiceException("密码长度必须在5到20个字符之间");
        }

        // 注册用户信息
        SysUser sysUser = new SysUser();
        sysUser.setUserName(username);
        sysUser.setNickName(username);
        sysUser.setPassword(SecurityUtils.encryptPassword(password));
        R<?> registerResult = remoteUserService.registerUserInfo(sysUser, SecurityConstants.INNER);

        if (R.FAIL == registerResult.getCode()) {
            throw new ServiceException(registerResult.getMsg());
        }
    }
}
