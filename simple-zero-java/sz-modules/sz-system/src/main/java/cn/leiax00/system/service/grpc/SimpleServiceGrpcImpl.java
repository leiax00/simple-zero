package cn.leiax00.system.service.grpc;


import cn.leiax00.api.system.v1.Simple;
import cn.leiax00.api.system.v1.SimpleServiceGrpc;
import cn.leiax00.system.service.ISimpleService;
import io.grpc.stub.StreamObserver;
import net.devh.boot.grpc.server.service.GrpcService;

@GrpcService
public class SimpleServiceGrpcImpl extends SimpleServiceGrpc.SimpleServiceImplBase {
    private final ISimpleService simpleService;

    public SimpleServiceGrpcImpl(ISimpleService simpleService) {
        this.simpleService = simpleService;
    }

    @Override
    public void sayHello(Simple.HelloRequest request, StreamObserver<Simple.HelloReply> responseObserver) {
        System.out.println("Hello, this is grpc result: " + request.getName());
        String value = this.simpleService.sayHello(request.getName());
        Simple.HelloReply reply = Simple.HelloReply.newBuilder().setMessage(value).build();
        responseObserver.onNext(reply);
        responseObserver.onCompleted();
    }
}
