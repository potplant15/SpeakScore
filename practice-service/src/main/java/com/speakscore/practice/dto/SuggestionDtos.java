package com.speakscore.practice.dto;

public final class SuggestionDtos {
    private SuggestionDtos() {}

    public record SuggestionResponse(
            String word,
            String translation,
            String phonetic,
            String pos
    ) {}
}
