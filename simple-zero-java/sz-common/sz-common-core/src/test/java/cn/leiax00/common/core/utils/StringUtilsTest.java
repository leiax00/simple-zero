package cn.leiax00.common.core.utils;

import org.junit.jupiter.api.Test;
import org.springframework.util.Assert;

class StringUtilsTest {

    @Test
    public void test_isMatch() {
        String url = "/api/novel/v1/list/a";
        String pattern = "/api/novel/v1/**";
        boolean match = StringUtils.isMatch(pattern, url);
        Assert.isTrue(match, "error happen");
    }
}