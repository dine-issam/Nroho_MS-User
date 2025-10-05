package com.example.gateway_api.auth.config;


import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpStatus;
import org.springframework.security.config.annotation.web.reactive.EnableWebFluxSecurity;
import org.springframework.security.config.web.server.SecurityWebFiltersOrder;
import org.springframework.security.config.web.server.ServerHttpSecurity;
import org.springframework.security.web.server.SecurityWebFilterChain;
import org.springframework.security.web.server.context.NoOpServerSecurityContextRepository;

import com.example.gateway_api.auth.filter.JwtAuthenticationFilter;

@Configuration
@EnableWebFluxSecurity
public class ReactiveSecurityConfig {
    private final JwtAuthenticationFilter jwtAuthenticationFilter;

    public ReactiveSecurityConfig(JwtAuthenticationFilter jwtAuthenticationFilter) {
        this.jwtAuthenticationFilter = jwtAuthenticationFilter;
    }

    @Bean
    public SecurityWebFilterChain securityWebFilterChain(ServerHttpSecurity http){
        return http.csrf(ServerHttpSecurity.CsrfSpec::disable)
        .authorizeExchange(exchanges -> exchanges
        .pathMatchers("/ms-user/auth/signup/","/ms-user/auth/signin/").permitAll()
        .anyExchange().authenticated()
        ).securityContextRepository(NoOpServerSecurityContextRepository.getInstance())
        .exceptionHandling(exceptions -> exceptions
        .authenticationEntryPoint((exchange,__)->{
            exchange.getResponse().setStatusCode(HttpStatus.UNAUTHORIZED);
                        return exchange.getResponse().setComplete();
        }))
        .addFilterBefore(jwtAuthenticationFilter, SecurityWebFiltersOrder.AUTHENTICATION)
        .build();
    }

    
}
