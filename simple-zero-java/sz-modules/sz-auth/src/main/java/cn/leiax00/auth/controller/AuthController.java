package cn.leiax00.auth.controller;

import cn.leiax00.auth.domain.dto.LoginBody;
import cn.leiax00.auth.domain.dto.RegisterBody;
import cn.leiax00.auth.service.LoginService;
import cn.leiax00.common.core.web.domain.R;
import cn.leiax00.common.security.service.TokenService;
import cn.leiax00.system.api.model.LoginUser;
import com.google.protobuf.InvalidProtocolBufferException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import javax.servlet.http.HttpServletRequest;
import java.util.Map;

@RestController
public class AuthController {
    @Autowired
    private LoginService loginService;

    @Autowired
    private TokenService tokenService;

    @PostMapping("login")
    public R<?> login(@RequestBody LoginBody form) throws InvalidProtocolBufferException {
        LoginUser login = loginService.login(form.getUsername(), form.getPassword());
        return R.ok(login);
    }

    @DeleteMapping("logout")
    public R<?> logout(HttpServletRequest request) {
        return null;
    }

    @PostMapping("refresh")
    public R<?> refresh(HttpServletRequest request) {
        return null;
    }

    @PostMapping("register")
    public R<?> register(@RequestBody RegisterBody registerBody) {
        return null;
    }
}
