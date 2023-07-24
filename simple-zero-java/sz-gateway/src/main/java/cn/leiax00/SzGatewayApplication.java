package cn.leiax00;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.jdbc.DataSourceAutoConfiguration;

/**
 * 网关启动程序
 */
@SpringBootApplication(exclude = {DataSourceAutoConfiguration.class})
public class SzGatewayApplication {
    public static void main(String[] args) {
        SpringApplication.run(SzGatewayApplication.class, args);
        // font: slant -- SZ-Gateway -- https://tools.kalvinbg.cn/txt/ascii
        System.out.println("                  (♥◠‿    ◠)ﾉﾞ  网关启动成功   ლ(´ڡ`ლ)ﾞ              \n" +
                "       __________        ______      __                                        \n" +
                "      / ___/__  /       / ____/___ _/ /____ _      ______ ___  __              \n" +
                "      \\__ \\  / / ______/ / __/ __ `/ __/ _ \\ | /| / / __ `/ / / /           \n" +
                "     ___/ / / /_/_____/ /_/ / /_/ / /_/  __/ |/ |/ / /_/ / /_/ /               \n" +
                "    /____/ /____/     \\____/\\__,_/\\__/\\___/|__/|__/\\__,_/\\__, /          \n" +
                "                                                        /____/                 \n" +
                "         \n"
        );
    }
}