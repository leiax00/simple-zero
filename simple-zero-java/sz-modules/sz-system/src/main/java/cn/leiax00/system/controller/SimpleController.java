package cn.leiax00.system.controller;

import cn.leiax00.system.service.ISimpleService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.HashMap;

@RestController
@RequestMapping("/simple")
public class SimpleController {
    private final ISimpleService simpleService;

    public SimpleController(ISimpleService simpleService) {
        this.simpleService = simpleService;
    }

    @GetMapping("/say")
    public HashMap<String, String> sayHello() {
        HashMap<String, String> map = new HashMap<>();
        map.put("message", this.simpleService.sayHello("Hello World"));
        return map;
    }


}
