package com.speakscore.practice.repository;
import com.speakscore.practice.entity.Practice;
import org.springframework.data.jpa.repository.JpaRepository;
public interface PracticeRepository extends JpaRepository<Practice, Long> {}
