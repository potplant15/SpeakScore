CREATE TABLE IF NOT EXISTS ecdict (
    word VARCHAR(128) NOT NULL,
    phonetic VARCHAR(128),
    definition TEXT,
    translation TEXT,
    pos VARCHAR(64),
    collins TINYINT,
    oxford TINYINT,
    tag VARCHAR(128),
    bnc INT,
    frq INT,
    exchange VARCHAR(255),
    detail TEXT,
    audio VARCHAR(255),
    PRIMARY KEY (word),
    INDEX idx_ecdict_word_prefix (word),
    INDEX idx_ecdict_frequency (frq, bnc)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
