package com.speakscore.practice.entity;

import jakarta.persistence.*;
import java.time.Instant;

@Entity
@Table(name="evaluation_result")
public class EvaluationResult {
    @Id @GeneratedValue(strategy=GenerationType.IDENTITY) private Long id;
    @OneToOne(optional=false) @JoinColumn(name="practice_id", nullable=false, unique=true) private Practice practice;
    private String recognizedText; private Double contentAccuracy; private Double completeness; private Double pronunciationScore;
    private Double phonemeErrorRate; private Double fluency; private Double overallScore; private Double wer; private Double wordsPerMinute;
    private Integer longPauseCount;
    @Lob @Column(columnDefinition="LONGTEXT") private String resultJson;
    @Column(nullable=false, updatable=false) private Instant createdAt;
    protected EvaluationResult() {}
    public EvaluationResult(Practice p){practice=p; createdAt=Instant.now();}
    public void update(String recognizedText, Double contentAccuracy, Double completeness, Double pronunciationScore, Double per, Double fluency, Double overall, Double wer, Double wpm, Integer pauses, String json){
        this.recognizedText=recognizedText;this.contentAccuracy=contentAccuracy;this.completeness=completeness;this.pronunciationScore=pronunciationScore;this.phonemeErrorRate=per;this.fluency=fluency;this.overallScore=overall;this.wer=wer;this.wordsPerMinute=wpm;this.longPauseCount=pauses;this.resultJson=json;
    }
    public Long getId(){return id;} public String getRecognizedText(){return recognizedText;} public Double getContentAccuracy(){return contentAccuracy;} public Double getCompleteness(){return completeness;} public Double getPronunciationScore(){return pronunciationScore;} public Double getPhonemeErrorRate(){return phonemeErrorRate;} public Double getFluency(){return fluency;} public Double getOverallScore(){return overallScore;} public Double getWer(){return wer;} public Double getWordsPerMinute(){return wordsPerMinute;} public Integer getLongPauseCount(){return longPauseCount;} public String getResultJson(){return resultJson;}
}
