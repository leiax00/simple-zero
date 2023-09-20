package cn.leiax00.common.core.utils;


import com.alibaba.fastjson2.JSON;
import com.alibaba.fastjson2.TypeReference;
import com.google.protobuf.InvalidProtocolBufferException;
import com.google.protobuf.Message;
import com.google.protobuf.MessageOrBuilder;
import com.google.protobuf.util.JsonFormat;

import java.util.Map;

public class ProtoUtils {

    /**
     * proto对象转换为json字符串
     */
    public static <T extends MessageOrBuilder> String proto2JsonStr(T t) throws InvalidProtocolBufferException {
        return JsonFormat.printer().print(t);
    }

    /**
     * proto对象转换为Map
     */
    public static <T extends MessageOrBuilder> Map<String, Object> proto2Map(T t) throws InvalidProtocolBufferException {
        return JSON.parseObject(proto2JsonStr(t), new TypeReference<Map<String, Object>>() {});
    }

    /**
     * json字符串转换为proto对象
     */
    public static <T extends Message.Builder> Message jsonStr2Proto(String jsonStr, T t) throws InvalidProtocolBufferException {
        JsonFormat.parser().merge(jsonStr, t);
        return t.build();
    }
}
