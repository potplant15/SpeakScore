package com.speakscore.practice.client;

import com.speakscore.practice.dto.PracticeDtos.EvaluationResponse;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.http.*;
import org.springframework.stereotype.Component;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestClient;

@Component
public class EvaluationClient {
    private final RestClient client;
    public EvaluationClient(@Value("${services.evaluation.base-url}") String url){client=RestClient.builder().baseUrl(url).build();}
    public EvaluationResponse evaluate(String text,String accent,byte[] audio,String filename){
        MultiValueMap<String,Object> form=new LinkedMultiValueMap<>(); form.add("reference_text",text); form.add("accent",accent);
        form.add("audio",new ByteArrayResource(audio){@Override public String getFilename(){return filename;}});
        return client.post().uri("/api/v1/evaluate").contentType(MediaType.MULTIPART_FORM_DATA).body(form).retrieve().body(EvaluationResponse.class);
    }
}
