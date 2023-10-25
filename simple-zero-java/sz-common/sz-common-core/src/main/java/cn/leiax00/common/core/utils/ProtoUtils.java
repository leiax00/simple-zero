package cn.leiax00.common.core.utils;


import com.alibaba.fastjson2.JSON;
import com.alibaba.fastjson2.TypeReference;
import com.google.protobuf.Descriptors;
import com.google.protobuf.InvalidProtocolBufferException;
import com.google.protobuf.Message;
import com.google.protobuf.MessageOrBuilder;
import com.google.protobuf.util.JsonFormat;

import java.util.Map;

public class ProtoUtils {

    /**
     * proto对象转换为json字符串
     */
    public static <T extends MessageOrBuilder> String proto2JsonStr(T t, Descriptors.Descriptor descriptor) throws InvalidProtocolBufferException {
        JsonFormat.Printer printer = JsonFormat.printer();
        if (descriptor != null) {
            JsonFormat.TypeRegistry typeRegistry = JsonFormat.TypeRegistry.newBuilder()
                .add(descriptor)
                .build();
            printer.usingTypeRegistry(typeRegistry);
        }

        return printer.print(t);
    }

    public static <T extends MessageOrBuilder> String proto2JsonStr(T t) throws InvalidProtocolBufferException {
        return proto2JsonStr(t, null);
    }

    /**
     * proto对象转换为Map
     */
    public static <T extends MessageOrBuilder> Map<String, Object> proto2Map(T t) throws InvalidProtocolBufferException {
        return JSON.parseObject(proto2JsonStr(t), new TypeReference<Map<String, Object>>() {
        });
    }

    /**
     * proto对象转pojo对象
     */
    public static <T extends MessageOrBuilder, V> T proto2Obj(T t, TypeReference<T> typeReference) throws InvalidProtocolBufferException {
        return JSON.parseObject(proto2JsonStr(t), typeReference);
    }

    /**
     * json字符串转换为proto对象
     */
    public static <T extends Message.Builder> Message jsonStr2Proto(String jsonStr, T t) throws InvalidProtocolBufferException {
        JsonFormat.parser().merge(jsonStr, t);
        return t.build();
    }

    /**
     * proto对象转pojo对象
     */
    public static <T extends Message.Builder, V> Message obj2Proto(V v, T t) throws InvalidProtocolBufferException {
        JsonFormat.parser().merge(JSON.toJSONString(v), t);
        return t.build();
    }
}
