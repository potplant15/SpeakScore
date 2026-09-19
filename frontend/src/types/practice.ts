export type Accent = 'en-US' | 'en-GB'
export type Gender = 'female' | 'male'

export interface CreatePracticeRequest {
  text: string
  accent: Accent
  gender: Gender
}

export interface Practice {
  id: number
  text: string
  accent: Accent
  gender: Gender
  status: 'CREATED' | 'EVALUATING' | 'EVALUATED' | 'EVALUATION_FAILED'
  audioUrl: string
  createdAt?: string
}

export interface PronunciationReference {
  text: string
  accent: Accent
  ipa: string
}

export interface Suggestion {
  word: string
  translation?: string
  phonetic?: string
  pos?: string
}

export interface EvaluationResult {
  recognizedText: string
  contentAccuracy: number
  completeness: number
  pronunciationScore: number
  phonemeErrorRate: number
  fluency: number
  overallScore: number
  wer: number
  wordsPerMinute: number
  longPauseCount: number
  details?: {
    pronunciation_errors?: Array<{
      word: string
      expected: string
      heard: string
      confidence: number
    }>
  }
}
