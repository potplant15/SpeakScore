package com.speakscore.practice.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "ecdict")
public class DictionaryEntry {
    @Id
    @Column(length = 128)
    private String word;

    @Column(length = 128)
    private String phonetic;

    @Column(columnDefinition = "TEXT")
    private String translation;

    @Column(length = 64)
    private String pos;

    private Integer bnc;
    private Integer frq;

    protected DictionaryEntry() {}

    public String getWord() { return word; }
    public String getPhonetic() { return phonetic; }
    public String getTranslation() { return translation; }
    public String getPos() { return pos; }
    public Integer getBnc() { return bnc; }
    public Integer getFrq() { return frq; }
}
