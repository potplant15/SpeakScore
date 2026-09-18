package com.speakscore.practice.controller;

import com.speakscore.practice.dto.PracticeDtos.*;
import com.speakscore.practice.entity.*;
import com.speakscore.practice.service.PracticeService;
import jakarta.validation.Valid;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.data.domain.*;
import org.springframework.data.web.PageableDefault;
import org.springframework.http.*;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

@RestController @RequestMapping("/api/v1/practices")
public class PracticeController {
    private final PracticeService service;
    public PracticeController(PracticeService s){service=s;}
    @PostMapping public ResponseEntity<PracticeResponse> create(@Valid @RequestBody CreateRequest req){Practice p=service.create(req);return ResponseEntity.status(HttpStatus.CREATED).body(view(p,null));}
    @GetMapping("/{id}/audio") public ResponseEntity<ByteArrayResource> audio(@PathVariable long id){return ResponseEntity.ok().contentType(MediaType.valueOf("audio/mpeg")).body(new ByteArrayResource(service.audio(id)));}
    @PostMapping("/{id}/evaluate") public EvaluationSummary evaluate(@PathVariable long id,@RequestPart("audio") MultipartFile audio){return summary(service.evaluate(id,audio));}
    @GetMapping("/{id}") public PracticeResponse get(@PathVariable long id){Practice p=service.get(id);return view(p,service.result(id));}
    @GetMapping public Page<PracticeResponse> list(@PageableDefault(size=20,sort="createdAt",direction=Sort.Direction.DESC) Pageable page){return service.list(page).map(p->view(p,service.result(p.getId())));}
    private PracticeResponse view(Practice p,EvaluationResult r){return new PracticeResponse(p.getId(),p.getReferenceText(),p.getAccent(),p.getGender(),p.getStatus().name(),"/api/v1/practices/"+p.getId()+"/audio",r==null?null:summary(r),p.getCreatedAt().toString());}
    private EvaluationSummary summary(EvaluationResult r){try{return new EvaluationSummary(r.getRecognizedText(),r.getContentAccuracy(),r.getCompleteness(),r.getPronunciationScore(),r.getPhonemeErrorRate(),r.getFluency(),r.getOverallScore(),r.getWer(),r.getWordsPerMinute(),r.getLongPauseCount(),new com.fasterxml.jackson.databind.ObjectMapper().readTree(r.getResultJson()));}catch(Exception e){return null;}}
}
