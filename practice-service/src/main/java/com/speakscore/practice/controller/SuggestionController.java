package com.speakscore.practice.controller;

import com.speakscore.practice.dto.SuggestionDtos.SuggestionResponse;
import com.speakscore.practice.service.SuggestionService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/v1/suggestions")
public class SuggestionController {
    private final SuggestionService suggestions;

    public SuggestionController(SuggestionService suggestions) {
        this.suggestions = suggestions;
    }

    @GetMapping
    public List<SuggestionResponse> suggest(@RequestParam(defaultValue = "") String prefix) {
        return suggestions.suggest(prefix);
    }
}
