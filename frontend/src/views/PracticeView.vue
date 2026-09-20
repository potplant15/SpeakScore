<script setup lang="ts">
import { computed, onBeforeUnmount, ref } from 'vue'
import { isAxiosError } from 'axios'
import AccentSelector from '@/components/AccentSelector.vue'
import Recorder from '@/components/Recorder.vue'
import ReferencePlayer from '@/components/ReferencePlayer.vue'
import ScoreResult from '@/components/ScoreResult.vue'
import SentenceInput from '@/components/SentenceInput.vue'
import { createPractice, evaluatePractice, getPronunciationReference, getReferenceAudio } from '@/services/practice'
import type { Accent, EvaluationResult, Gender, Practice } from '@/types/practice'

const sentence = ref('I would like some water.')
const accent = ref<Accent>('en-US')
const gender = ref<Gender>('female')
const practice = ref<Practice | null>(null)
const result = ref<EvaluationResult | null>(null)
const referenceAudioUrl = ref('')
const referenceIpa = ref('')
const loading = ref(false)
const evaluating = ref(false)
const error = ref('')
const stage = computed(() => result.value ? 4 : practice.value ? 3 : 1)
const canStart = computed(() => sentence.value.trim().length > 0 && !loading.value)

async function startPractice() {
  if (!canStart.value) return
  loading.value = true
  error.value = ''
  result.value = null
  try {
    practice.value = await createPractice({ text: sentence.value.trim(), accent: accent.value, gender: gender.value })
    const [audio, reference] = await Promise.all([
      getReferenceAudio(practice.value.id),
      getPronunciationReference(practice.value.id),
    ])
    if (referenceAudioUrl.value) URL.revokeObjectURL(referenceAudioUrl.value)
    referenceAudioUrl.value = URL.createObjectURL(audio)
    referenceIpa.value = reference.ipa
  } catch {
    error.value = 'Could not start this practice. Is Practice Service running on port 8080?'
    practice.value = null
  } finally { loading.value = false }
}

async function submitRecording(audio: Blob) {
  if (!practice.value) return
  evaluating.value = true
  error.value = ''
  try {
    result.value = await evaluatePractice(practice.value.id, audio)
    practice.value.status = 'EVALUATED'
  } catch (cause) {
    if (isAxiosError(cause)) {
      const status = cause.response?.status
      const detail = cause.response?.data?.detail
      if (status === 413) error.value = 'Audio file is too large. Choose a file smaller than 10 MB.'
      else if (status === 422 && /speech|recogn/i.test(String(detail))) error.value = 'Audio could not be recognized. Try a clearer recording or another audio file.'
      else if (status === 503) error.value = 'The scoring service is temporarily unavailable. Please try again in a moment.'
      else error.value = 'The score could not be generated. Please try the recording again.'
    } else {
      error.value = 'The scoring service is temporarily unavailable. Please try again in a moment.'
    }
  }
  finally { evaluating.value = false }
}

function resetPractice() {
  practice.value = null
  result.value = null
  error.value = ''
  if (referenceAudioUrl.value) URL.revokeObjectURL(referenceAudioUrl.value)
  referenceAudioUrl.value = ''
  referenceIpa.value = ''
}

onBeforeUnmount(() => { if (referenceAudioUrl.value) URL.revokeObjectURL(referenceAudioUrl.value) })
</script>

<template>
  <main class="app-shell">
    <header class="topbar">
      <a class="brand" href="#"><span class="brand-mark">ss</span><span>SpeakScore</span></a>
      <div class="session-chip"><span class="spark">✦</span> one good sentence at a time</div>
    </header>

    <div class="page-grid">
      <aside class="side-note">
        <div class="vertical-word">PRONUNCIATION PRACTICE</div>
        <div class="side-bottom"><span class="page-number">01</span><span class="side-rule" /><span>quiet focus</span></div>
      </aside>

      <section class="practice-page">
        <div class="intro-row">
          <div><p class="kicker">A small speaking ritual</p><h1>Find the shape<br /><em>of your voice.</em></h1></div>
          <div class="progress-track"><span v-for="n in 4" :key="n" :class="{ current: stage === n, done: stage > n }" /><small>{{ stage }}/4</small></div>
        </div>

        <div v-if="!practice" class="setup-area">
          <div class="setup-card paper-card">
            <span class="card-number">01</span>
            <SentenceInput v-model="sentence" />
            <AccentSelector v-model:accent="accent" v-model:gender="gender" />
            <button class="primary-button" :disabled="!canStart" @click="startPractice">
              {{ loading ? 'Preparing your practice...' : 'Begin this practice' }} <span>↗</span>
            </button>
          </div>
          <p class="small-hint"><span>⌁</span> Tip: choose a sentence you would actually say today.</p>
        </div>

        <div v-else class="practice-area">
          <div class="sentence-display paper-card"><span class="eyebrow">Say this</span><p>{{ practice.text }}</p><button class="change-button" @click="resetPractice">Change sentence</button></div>
          <ReferencePlayer v-if="referenceAudioUrl" :audio-url="referenceAudioUrl" :accent="practice.accent" :ipa="referenceIpa" :loading="loading" />
          <Recorder :disabled="evaluating" @recorded="submitRecording" />
          <p v-if="evaluating" class="processing"><span class="loader" /> Listening for the details...</p>
          <ScoreResult v-if="result" :result="result" />
        </div>
        <p v-if="error" class="error-banner">{{ error }}</p>
      </section>
    </div>
    <footer><span>SpeakScore / practice desk</span><span>English pronunciation, made personal.</span></footer>
  </main>
</template>
