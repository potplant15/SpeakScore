package com.speakscore.practice.client;

import com.speakscore.practice.dto.PracticeDtos.EvaluationResponse;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Component;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestTemplate;

import java.util.List;

@Component
public class EvaluationClient {
    private final String baseUrl;
    private final RestTemplate restTemplate = new RestTemplate();

    public EvaluationClient(@Value("${services.evaluation.base-url}") String baseUrl) {
        this.baseUrl = baseUrl;
    }

    public EvaluationResponse evaluate(String text, String accent, byte[] audio, String filename) {
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.MULTIPART_FORM_DATA);
        headers.setAccept(List.of(MediaType.APPLICATION_JSON));

        ByteArrayResource audioResource = new ByteArrayResource(audio) {
            @Override
            public String getFilename() {
                return filename;
            }
        };

        MultiValueMap<String, Object> form = new LinkedMultiValueMap<>();
        form.add("reference_text", text);
        form.add("accent", accent);
        form.add("audio", audioResource);

        HttpEntity<MultiValueMap<String, Object>> request = new HttpEntity<>(form, headers);
        ResponseEntity<EvaluationResponse> response = restTemplate.postForEntity(
                baseUrl + "/api/v1/evaluate",
                request,
                EvaluationResponse.class
        );
        if (!response.getStatusCode().is2xxSuccessful() || response.getBody() == null) {
            throw new IllegalStateException(
                    "Evaluation Service returned HTTP " + response.getStatusCode().value()
            );
        }
        return response.getBody();
    }
}
