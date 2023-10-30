package cn.leiax00.auth;

import cn.leiax00.common.security.annotation.EnableSzFeignClients;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.jdbc.DataSourceAutoConfiguration;

/**
 * 网关启动程序
 */
@EnableSzFeignClients
@SpringBootApplication(exclude = {DataSourceAutoConfiguration.class})
public class SzAuthApplication {
    public static void main(String[] args) {
        SpringApplication.run(SzAuthApplication.class, args);
        // font: slant -- SZ-Gateway -- https://tools.kalvinbg.cn/txt/ascii
        System.out.println("                  (♥◠‿    ◠)ﾉﾞ  鉴权服务启动成功   ლ(´ڡ`ლ)ﾞ              \n" +
                "     ____ _____       _   _   _ _____ _   _     \n" +
                "    / ___|__  /      / \\ | | | |_   _| | | |    \n" +
                "    \\___ \\ / /_____ / _ \\| | | | | | | |_| |    \n" +
                "     ___) / /|_____/ ___ \\ |_| | | | |  _  |    \n" +
                "    |____/____|   /_/   \\_\\___/  |_| |_| |_|    \n" +
                "         \n"
        );
    }
}