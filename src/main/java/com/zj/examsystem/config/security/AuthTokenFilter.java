package com.zj.examsystem.config.security;

import org.jetbrains.annotations.NotNull;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.web.authentication.WebAuthenticationDetailsSource;
import org.springframework.util.StringUtils;
import org.springframework.web.filter.OncePerRequestFilter;

import javax.servlet.FilterChain;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
//处理身份验证的过滤器  在每个http请求中执行一次过滤操作
public class AuthTokenFilter extends OncePerRequestFilter {
    //处理jwt的工具类，解析、验证、生成jwt
    @Autowired
    private JwtUtils jwtUtils;

    //自定义的用户详情服务
    @Autowired
    private CustomUserDetailsService userDetailsService;

    //静态的日志记录器
    private static final Logger logger = LoggerFactory.getLogger(AuthTokenFilter.class);

    @Override
    protected void doFilterInternal(@NotNull HttpServletRequest request, @NotNull HttpServletResponse response, @NotNull FilterChain filterChain)
            throws ServletException, IOException {
        try {
            //从请求中获取jwt
            String jwt = parseJwt(request);
            if (jwt != null && jwtUtils.validateJwtToken(jwt)) {
                // 从jwt中拿到username
                String account = jwtUtils.getUserNameFromJwtToken(jwt);
                Integer identity = (Integer) jwtUtils.getIdentityFromJwtToken(jwt);
                account = identity + " " + account;
                // 根据username拿到userDetails
                UserDetails userDetails = userDetailsService.loadUserByUsername(account);
                UsernamePasswordAuthenticationToken authentication = new UsernamePasswordAuthenticationToken(
                        userDetails, null, userDetails.getAuthorities());
                // 将当前请求包中的内容存入Authentication中
                authentication.setDetails(new WebAuthenticationDetailsSource().buildDetails(request));

                // 将authentication存入到SecurityContext中，便于之后调用
                // 以下代码将存在SecurityContext中的authentication中的整个用户信息取出
                // UserDetails userDetails = (UserDetails) SecurityContextHolder.getContext().getAuthentication().getPrincipal();
                SecurityContextHolder.getContext().setAuthentication(authentication);
            }
        } catch (Exception e) {
            logger.error("Cannot set user authentication: {0}", e);
        }

        filterChain.doFilter(request, response);
    }

    // 从请求包中拿到JWT
    private String parseJwt(HttpServletRequest request) {
        String headerAuth = request.getHeader("Authorization");

        // 如果authorization中有内容且是以本项目中设定好的字符串为前缀，则将该jwt返回
        if (StringUtils.hasText(headerAuth) && headerAuth.startsWith("Bearer ")) {
            // 移除Bearer前缀
            return headerAuth.substring(7);
        }

        return null;
    }
}