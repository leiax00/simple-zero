package cn.leiax00.common.core.domain;

import cn.leiax00.common.core.constant.Constants;
import lombok.Data;

import java.io.Serializable;

@Data
public class Resp<T> implements Serializable {
    private static final long serialVersionUID = 1L;

    /**
     * 成功
     */
    public static final int SUCCESS = Constants.SUCCESS;

    /**
     * 失败
     */
    public static final int FAIL = Constants.FAIL;

    private int code;

    private String msg;

    private T data;

    private Resp() {
    }

    public static <T> Resp<T> ok(T data) {
        return restResult(data, SUCCESS, null);
    }

    public static <T> Resp<T> ok(T data, String msg) {
        return restResult(data, SUCCESS, msg);
    }

    public static <T> Resp<T> fail(String msg) {
        return restResult(null, FAIL, msg);
    }

    public static <T> Resp<T> fail(T data) {
        return restResult(data, FAIL, null);
    }

    public static <T> Resp<T> fail(T data, String msg) {
        return restResult(data, FAIL, msg);
    }

    public static <T> Resp<T> fail(T data, int code, String msg) {
        return restResult(data, code, msg);
    }


    private static <T> Resp<T> restResult(T data, int code, String msg) {
        Resp<T> apiResult = new Resp<>();
        apiResult.setCode(code);
        apiResult.setData(data);
        apiResult.setMsg(msg);
        return apiResult;
    }

    public static <T> boolean isOk(Resp<T> resp) {
        return Resp.SUCCESS == resp.code;
    }
}
