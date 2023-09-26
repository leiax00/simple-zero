package cn.leiax00.system.api.service;

import cn.leiax00.api.system.v1.Simple;
import cn.leiax00.api.system.v1.SimpleServiceGrpc;
import net.devh.boot.grpc.client.inject.GrpcClient;
import org.springframework.stereotype.Component;

@Component
public class SimpleServiceClient {
    @GrpcClient("sz-system")
    private SimpleServiceGrpc.SimpleServiceBlockingStub stub;

    public Simple.HelloReply sayHello(Simple.HelloRequest request) {
        return stub.sayHello(request);
    }
}
