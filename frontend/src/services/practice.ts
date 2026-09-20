import { api } from './api'
import type { CreatePracticeRequest, EvaluationResult, Practice, PronunciationReference, Suggestion } from '@/types/practice'

export async function createPractice(request: CreatePracticeRequest): Promise<Practice> {
  const response = await api.post<Practice>('/practices', request)
  return response.data
}

export async function getReferenceAudio(practiceId: number): Promise<Blob> {
  const response = await api.get<Blob>(`/practices/${practiceId}/audio`, {
    responseType: 'blob',
  })
  return response.data
}

export async function getPronunciationReference(practiceId: number): Promise<PronunciationReference> {
  const response = await api.get<PronunciationReference>(`/practices/${practiceId}/reference`)
  return response.data
}

export async function getSuggestions(prefix: string): Promise<Suggestion[]> {
  const response = await api.get<Suggestion[]>('/suggestions', { params: { prefix } })
  return response.data
}

export async function evaluatePractice(
  practiceId: number,
  audio: Blob,
): Promise<EvaluationResult> {
  const formData = new FormData()
  const extension = audio.type.includes('mpeg') ? 'mp3'
    : audio.type.includes('wav') ? 'wav'
      : audio.type.includes('mp4') || audio.type.includes('m4a') ? 'm4a'
        : 'webm'
  formData.append('audio', audio, `recording.${extension}`)
  const response = await api.post<EvaluationResult>(`/practices/${practiceId}/evaluate`, formData)
  return response.data
}
