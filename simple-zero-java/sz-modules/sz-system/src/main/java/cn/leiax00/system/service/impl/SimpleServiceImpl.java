package cn.leiax00.system.service.impl;

import cn.leiax00.system.service.ISimpleService;
import org.springframework.stereotype.Service;

@Service
public class SimpleServiceImpl implements ISimpleService {
    public String sayHello(String word) {
        System.out.println("Hello, this is service receive: " + word);
        return "request success";
    }
}
