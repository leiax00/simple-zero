package cn.leiax00.auth.service;

import cn.leiax00.api.system.v1.Simple;
import cn.leiax00.auth.domain.dto.LoginBody;
import cn.leiax00.common.core.utils.ProtoUtils;
import cn.leiax00.system.api.service.SimpleServiceClient;
import com.google.protobuf.InvalidProtocolBufferException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Map;

@Service
public class LoginService {

    @Autowired
    private SimpleServiceClient client;

    public Map<String, Object> login(LoginBody form) throws InvalidProtocolBufferException {
        Simple.HelloRequest request = Simple.HelloRequest.newBuilder().setName(form.getUsername()).build();
        Simple.HelloReply reply = client.sayHello(request);
        return ProtoUtils.proto2Map(reply);
    }
}
