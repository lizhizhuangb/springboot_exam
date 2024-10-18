package com.zj.examsystem.config.security;

import com.zj.examsystem.entity.User;
import io.jsonwebtoken.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.security.core.Authentication;
import org.springframework.stereotype.Component;

import java.util.Date;
import java.util.HashMap;
import java.util.Map;

@Component
public class JwtUtils {
    private static final Logger logger = LoggerFactory.getLogger(JwtUtils.class);

    //密钥
    @Value("${examsystem.app.jwtSecret}")
    private String jwtSecret;

    // 有效期3h
    @Value("${examsystem.app.jwtExpirationMs}")
    private int jwtExpirationMs;

    public String generateJwtToken(Authentication authentication, Integer identity) {
        //获取当前登录用户的对象
        User userPrincipal = (User) authentication.getPrincipal();
        //claims 是一个包含了 JWT 所需的任何自定义声明的 Map 对象，用于在 JWT 中存储一些自定义的键值对信息。
        Map<String, Object> claims = new HashMap<>();
        claims.put("identity", identity);

        // Header.Payload.Signature
        return Jwts.builder()
                // Payload
                .setClaims(claims)
                .setSubject(userPrincipal.getAccount())
                .setIssuedAt(new Date())
                .setExpiration(new Date((new Date()).getTime() + jwtExpirationMs))
                // Signature: 算法名称 + 密钥
                .signWith(SignatureAlgorithm.HS512, jwtSecret)
                .compact();
    }

    //从jwt中获取用户名
    public String getUserNameFromJwtToken(String token) {
        return Jwts.parser().setSigningKey(jwtSecret).parseClaimsJws(token).getBody().getSubject();
    }

    //从jwt中获取role_id
    public Object getIdentityFromJwtToken(String token) {
        return Jwts.parser().setSigningKey(jwtSecret).parseClaimsJws(token).getBody().get("identity");
    }

    //校验jwt令牌是否有效
    public boolean validateJwtToken(String authToken) {
        try {
            Jwts.parser().setSigningKey(jwtSecret).parseClaimsJws(authToken);
            return true;
        } catch (SignatureException e) {
            logger.error("Invalid JWT signature: {}", e.getMessage());
        } catch (MalformedJwtException e) {
            logger.error("Invalid JWT token: {}", e.getMessage());
        } catch (ExpiredJwtException e) {
            logger.error("JWT token is expired: {}", e.getMessage());
        } catch (UnsupportedJwtException e) {
            logger.error("JWT token is unsupported: {}", e.getMessage());
        } catch (IllegalArgumentException e) {
            logger.error("JWT claims string is empty: {}", e.getMessage());
        }
        return false;
    }
}
