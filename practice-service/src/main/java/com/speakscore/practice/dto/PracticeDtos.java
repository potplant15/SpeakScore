package com.speakscore.practice.dto;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.constraints.*;

public final class PracticeDtos {
    private PracticeDtos() {}
    public record CreateRequest(@NotBlank @Size(max=1000) String text, @NotNull @Pattern(regexp="en-US|en-GB") String accent, @NotNull @Pattern(regexp="female|male") String gender) {}
    public record EvaluationResponse(@JsonProperty("reference_text") String referenceText, @JsonProperty("recognized_text") String recognizedText, String accent, @JsonProperty("content_accuracy") Double contentAccuracy, Double completeness, Pronunciation pronunciation, Double fluency, @JsonProperty("overall_score") Double overallScore, Double wer, @JsonProperty("words_per_minute") Double wordsPerMinute, @JsonProperty("long_pause_count") Integer longPauseCount, @JsonProperty("pronunciation_errors") JsonNode pronunciationErrors) {}
    public record Pronunciation(Double score, @JsonProperty("phoneme_error_rate") Double phonemeErrorRate) {}
    public record ReferenceResponse(String text, String accent, String ipa) {}
    public record PracticeResponse(Long id, String text, String accent, String gender, String status, String audioUrl, EvaluationSummary evaluation, String createdAt) {}
    public record EvaluationSummary(String recognizedText, Double contentAccuracy, Double completeness, Double pronunciationScore, Double phonemeErrorRate, Double fluency, Double overallScore, Double wer, Double wordsPerMinute, Integer longPauseCount, JsonNode details) {}
}
