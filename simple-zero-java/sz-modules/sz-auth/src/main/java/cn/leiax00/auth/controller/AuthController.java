package cn.leiax00.auth.controller;

import cn.leiax00.auth.domain.dto.LoginBody;
import cn.leiax00.auth.domain.dto.RegisterBody;
import cn.leiax00.auth.service.LoginService;
import cn.leiax00.common.core.utils.JwtUtils;
import cn.leiax00.common.core.utils.StringUtils;
import cn.leiax00.common.core.web.domain.R;
import cn.leiax00.common.security.auth.AuthUtil;
import cn.leiax00.common.security.service.TokenService;
import cn.leiax00.common.security.utils.SecurityUtils;
import cn.leiax00.system.api.model.LoginUser;
import com.google.protobuf.InvalidProtocolBufferException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import javax.servlet.http.HttpServletRequest;

@RestController
public class AuthController {
    @Autowired
    private LoginService loginService;

    @Autowired
    private TokenService tokenService;

    @PostMapping("login")
    public R<?> login(@RequestBody LoginBody form) throws InvalidProtocolBufferException {
        LoginUser userInfo = loginService.login(form.getUsername(), form.getPassword());
        return R.ok(tokenService.createToken(userInfo));
    }

    @DeleteMapping("logout")
    public R<?> logout(HttpServletRequest request) {
        String token = SecurityUtils.getToken(request);
        if (StringUtils.isNotEmpty(token)) {
            String username = JwtUtils.getUserName(token);
            // 删除用户缓存记录
            AuthUtil.logoutByToken(token);
            // 记录用户退出日志
            loginService.logout(username);
        }
        return R.ok();
    }

    @PostMapping("refresh")
    public R<?> refresh(HttpServletRequest request) {
        LoginUser loginUser = tokenService.getLoginUser(request);
        if (StringUtils.isNotNull(loginUser)) {
            // 刷新令牌有效期
            tokenService.refreshToken(loginUser);
            return R.ok();
        }
        return R.ok();
    }

    @PostMapping("register")
    public R<?> register(@RequestBody RegisterBody registerBody) {
        // 用户注册
        loginService.register(registerBody.getUsername(), registerBody.getPassword());
        return R.ok();
    }
}
