package com.speakscore.practice.repository;

import com.speakscore.practice.entity.DictionaryEntry;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface DictionaryRepository extends JpaRepository<DictionaryEntry, String> {
    @Query("""
            SELECT entry FROM DictionaryEntry entry
            WHERE entry.word LIKE CONCAT(:prefix, '%')
            ORDER BY
              CASE WHEN entry.frq IS NULL OR entry.frq = 0 THEN 1 ELSE 0 END,
              entry.frq ASC,
              entry.word ASC
            """)
    List<DictionaryEntry> findByPrefix(@Param("prefix") String prefix, Pageable pageable);
}
