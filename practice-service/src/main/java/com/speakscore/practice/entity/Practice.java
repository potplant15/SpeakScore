package com.speakscore.practice.entity;

import jakarta.persistence.*;
import java.time.Instant;

@Entity
@Table(name = "practice")
public class Practice {
    public enum Status { CREATED, EVALUATING, EVALUATED, EVALUATION_FAILED }
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY) private Long id;
    @Column(name="reference_text", nullable=false, length=1000) private String referenceText;
    @Column(nullable=false, length=10) private String accent;
    @Column(nullable=false, length=10) private String gender;
    @Enumerated(EnumType.STRING) @Column(nullable=false, length=24) private Status status = Status.CREATED;
    @Column(nullable=false, updatable=false) private Instant createdAt;
    @Column(nullable=false) private Instant updatedAt;
    protected Practice() {}
    public Practice(String text, String accent, String gender) { this.referenceText=text; this.accent=accent; this.gender=gender; }
    @PrePersist void onCreate(){ createdAt=updatedAt=Instant.now(); }
    @PreUpdate void onUpdate(){ updatedAt=Instant.now(); }
    public Long getId(){return id;} public String getReferenceText(){return referenceText;} public String getAccent(){return accent;}
    public String getGender(){return gender;} public Status getStatus(){return status;} public Instant getCreatedAt(){return createdAt;} public Instant getUpdatedAt(){return updatedAt;}
    public void setStatus(Status status){this.status=status;}
}
