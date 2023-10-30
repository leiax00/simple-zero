package cn.leiax00.system;

import cn.leiax00.common.security.annotation.EnableCustomConfig;

import cn.leiax00.common.security.annotation.EnableSzFeignClients;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@EnableCustomConfig
@EnableSzFeignClients
@SpringBootApplication
public class SzSystemApplication {
    public static void main(String[] args) {
        SpringApplication.run(SzSystemApplication.class, args);
        System.out.println("              (♥◠‿    ◠)ﾉﾞ  系统core启动成功   ლ(´ڡ`ლ)ﾞ          \n" +
                "     ____ _____    ______   ______ _____ _____ __  __           \n" +
                "    / ___|__  /   / ___\\ \\ / / ___|_   _| ____|  \\/  |       \n" +
                "    \\___ \\ / /____\\___ \\ V /\\___ \\  | | |  _| | |\\/| |   \n" +
                "     ___) / /|_____|__) || |  ___) || | | |___| |  | |          \n" +
                "    |____/____|   |____/ |_| |____/ |_| |_____|_|  |_|          \n" +
                "                                                                \n" +
                "         \n"
        );
    }
}
