package com.speakscore.practice.client;

import com.speakscore.practice.dto.PracticeDtos.ReferenceResponse;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatusCode;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

import java.util.List;
import java.util.Map;

@Component
public class ReferenceClient {
    private final String baseUrl;
    private final RestTemplate restTemplate = new RestTemplate();

    public ReferenceClient(@Value("${services.reference.base-url}") String baseUrl) {
        this.baseUrl = baseUrl;
    }

    public byte[] synthesize(String text, String accent, String gender) {
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        headers.setAccept(List.of(MediaType.valueOf("audio/mpeg")));

        Map<String, String> requestBody = Map.of(
                "text", text,
                "accent", accent,
                "gender", gender
        );
        HttpEntity<Map<String, String>> request = new HttpEntity<>(requestBody, headers);

        ResponseEntity<byte[]> response = restTemplate.postForEntity(
                baseUrl + "/api/v1/tts",
                request,
                byte[].class
        );
        HttpStatusCode status = response.getStatusCode();
        if (!status.is2xxSuccessful() || response.getBody() == null) {
            throw new IllegalStateException(
                    "Reference Service returned HTTP " + status.value()
            );
        }
        return response.getBody();
    }

    public ReferenceResponse pronunciationReference(String text, String accent) {
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        HttpEntity<Map<String, String>> request = new HttpEntity<>(
                Map.of("text", text, "accent", accent), headers
        );
        ResponseEntity<ReferenceResponse> response = restTemplate.postForEntity(
                baseUrl + "/api/v1/reference", request, ReferenceResponse.class
        );
        if (!response.getStatusCode().is2xxSuccessful() || response.getBody() == null) {
            throw new IllegalStateException(
                    "Reference Service returned HTTP " + response.getStatusCode().value()
            );
        }
        return response.getBody();
    }
}
