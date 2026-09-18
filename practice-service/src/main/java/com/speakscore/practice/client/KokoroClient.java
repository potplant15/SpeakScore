package com.speakscore.practice.client;

import com.fasterxml.jackson.databind.JsonNode;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.http.*;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestClient;
import java.util.Map;

@Component
public class KokoroClient {
    private final RestClient client;
    public KokoroClient(@Value("${services.kokoro.base-url}") String url){client=RestClient.builder().baseUrl(url).build();}
    public byte[] synthesize(String text,String accent,String gender){
        byte[] body=client.post().uri("/api/v1/tts").contentType(MediaType.APPLICATION_JSON).body(Map.of("text",text,"accent",accent,"gender",gender)).retrieve().body(byte[].class);
        if(body==null) throw new IllegalStateException("Kokoro returned an empty audio response"); return body;
    }
}
