package com.zj.examsystem.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

/**
 * 解决跨域问题
 */
@Configuration
public class VueConfig implements WebMvcConfigurer {
    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/**")//对所有路径的请求都适用该CORS配置
                .allowedOriginPatterns("*")//允许所有来源（Origin）的请求访问资源
                .allowedMethods("GET", "POST", "HEAD", "PUT", "DELETE", "OPTIONS")//允许使用的HTTP方法。
                .allowCredentials(true)//允许请求发送凭据（如Cookie、HTTP认证信息）
                .maxAge(3600)//设置预检请求（OPTIONS请求）的有效期为3600秒（即1小时），减少浏览器发送预检请求的频率。 预检请求即检查头部信息等是否符合请求
                .allowedHeaders("*");//允许所有的请求头
    }
}
