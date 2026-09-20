<script setup lang="ts">
import { computed, onBeforeUnmount, ref, watch } from 'vue'
import { useRecorder } from '@/composables/useRecorder'

const props = defineProps<{ disabled?: boolean }>()
const emit = defineEmits<{ recorded: [blob: Blob]; reset: [] }>()
const { isRecording, audioBlob, elapsedSeconds, error, startRecording, stopRecording, resetRecording } = useRecorder()
const timer = computed(() => `0${Math.floor(elapsedSeconds.value / 60)}:${String(elapsedSeconds.value % 60).padStart(2, '0')}`)
const recordedAudioUrl = ref('')
const fileInput = ref<HTMLInputElement | null>(null)
const maxAudioSize = 10 * 1024 * 1024
const minAudioDuration = 0.5

watch(audioBlob, (blob) => {
  if (recordedAudioUrl.value) URL.revokeObjectURL(recordedAudioUrl.value)
  recordedAudioUrl.value = blob ? URL.createObjectURL(blob) : ''
})

async function start() {
  if (fileInput.value) fileInput.value.value = ''
  await startRecording()
}
function stop() { stopRecording(); window.setTimeout(() => audioBlob.value && emit('recorded', audioBlob.value), 0) }
function getAudioDuration(file: File): Promise<number> {
  return new Promise((resolve, reject) => {
    const audio = document.createElement('audio')
    const url = URL.createObjectURL(file)
    audio.preload = 'metadata'
    audio.onloadedmetadata = () => {
      URL.revokeObjectURL(url)
      resolve(audio.duration)
    }
    audio.onerror = () => {
      URL.revokeObjectURL(url)
      reject(new Error('decode'))
    }
    audio.src = url
  })
}

async function handleFileChange(event: Event) {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]
  if (!file) return

  error.value = ''
  const extension = file.name.slice(file.name.lastIndexOf('.')).toLowerCase()
  const supportedExtension = ['.mp3', '.wav', '.webm', '.m4a'].includes(extension)
  if ((!file.type.startsWith('audio/') && !supportedExtension) || file.size > maxAudioSize) {
    error.value = file.size > maxAudioSize
      ? 'Audio file is too large. Choose a file smaller than 10 MB.'
      : 'Unsupported audio format. Use MP3, WAV, WEBM, or M4A.'
    input.value = ''
    return
  }

  try {
    const duration = await getAudioDuration(file)
    if (!Number.isFinite(duration) || duration < minAudioDuration) {
      error.value = 'Audio is too short. Record or upload at least half a second of speech.'
      input.value = ''
      return
    }
  } catch {
    error.value = 'Audio could not be recognized. Try another MP3, WAV, WEBM, or M4A file.'
    input.value = ''
    return
  }

  audioBlob.value = file
  elapsedSeconds.value = 0
  emit('recorded', file)
}
function reset() {
  resetRecording()
  if (fileInput.value) fileInput.value.value = ''
  emit('reset')
}
onBeforeUnmount(() => { if (recordedAudioUrl.value) URL.revokeObjectURL(recordedAudioUrl.value) })
</script>

<template>
  <section class="recorder-card" :class="{ recording: isRecording, ready: audioBlob }">
    <div class="recording-orbit" aria-hidden="true"><span /><span /><span /></div>
    <div class="recorder-copy">
      <span class="eyebrow">Your turn</span>
      <strong>{{ isRecording ? 'Speak naturally' : audioBlob ? 'Nice take.' : 'Say it out loud' }}</strong>
      <small>{{ isRecording ? timer : audioBlob ? 'Your recording is ready to review.' : 'Take a breath, then press the microphone.' }}</small>
    </div>
    <input ref="fileInput" type="file" accept="audio/*,.mp3,.wav,.webm,.m4a" hidden @change="handleFileChange" />
    <div v-if="!isRecording" class="recorder-actions">
      <button class="record-button" :disabled="disabled" @click="start">
        <span class="mic-mark">●</span>{{ audioBlob ? 'Record again' : 'Start recording' }}
      </button>
      <button type="button" class="upload-button" :disabled="disabled" @click="fileInput?.click()">Upload audio</button>
    </div>
    <button v-else class="record-button stop" @click="stop"><span class="stop-mark" /> Stop recording</button>
    <button v-if="audioBlob && !isRecording" class="text-button" @click="reset">Clear take</button>
    <div v-if="error" class="recording-help" role="alert">
      <p class="inline-error">{{ error }}</p>
      <small>Try checking the browser microphone icon, system input volume, and whether another app is using the microphone.</small>
    </div>
    <div v-if="recordedAudioUrl && !isRecording" class="recorded-playback">
      <div><span class="eyebrow">Your recording</span><small>Listen back before submitting</small></div>
      <audio :src="recordedAudioUrl" controls preload="metadata" />
    </div>
  </section>
</template>
