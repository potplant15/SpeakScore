package com.speakscore.practice.repository;
import com.speakscore.practice.entity.EvaluationResult;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.Optional;
public interface EvaluationResultRepository extends JpaRepository<EvaluationResult, Long> { Optional<EvaluationResult> findByPracticeId(Long practiceId); }
