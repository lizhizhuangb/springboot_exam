package com.zj.examsystem;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;
import org.springframework.cloud.openfeign.EnableFeignClients;

@MapperScan("com.zj.examsystem.mapper")
@SpringBootApplication
@EnableDiscoveryClient
public class ExamsystemApplication {
    public static void main(String[] args) {
        //        String filePath = new File("").getAbsolutePath() + "\\src\\main\\resources\\python\\textSimilarity.py";
        //        Process process;
        //        try {
        //            process = Runtime.getRuntime().exec(new String[]{"python", filePath});
        //            process.waitFor();
        //        } catch (IOException | InterruptedException e) {
        //            e.printStackTrace();
        //        }

        SpringApplication.run(ExamsystemApplication.class, args);
    }
}
