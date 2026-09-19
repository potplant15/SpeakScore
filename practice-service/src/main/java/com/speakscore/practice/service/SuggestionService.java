package com.speakscore.practice.service;

import com.speakscore.practice.dto.SuggestionDtos.SuggestionResponse;
import com.speakscore.practice.entity.DictionaryEntry;
import com.speakscore.practice.repository.DictionaryRepository;
import org.springframework.data.domain.PageRequest;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class SuggestionService {
    private static final int MAX_SUGGESTIONS = 8;
    private final DictionaryRepository dictionary;

    public SuggestionService(DictionaryRepository dictionary) {
        this.dictionary = dictionary;
    }

    public List<SuggestionResponse> suggest(String prefix) {
        String normalized = prefix == null ? "" : prefix.trim();
        if (normalized.length() < 1 || normalized.length() > 32) {
            return List.of();
        }
        return dictionary.findByPrefix(normalized, PageRequest.of(0, MAX_SUGGESTIONS))
                .stream()
                .map(this::toResponse)
                .toList();
    }

    private SuggestionResponse toResponse(DictionaryEntry entry) {
        return new SuggestionResponse(
                entry.getWord(),
                entry.getTranslation(),
                entry.getPhonetic(),
                entry.getPos()
        );
    }
}
