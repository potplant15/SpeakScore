<script setup lang="ts">
import { computed, onBeforeUnmount, ref, watch } from 'vue'
import { useRecorder } from '@/composables/useRecorder'

const props = defineProps<{ disabled?: boolean }>()
const emit = defineEmits<{ recorded: [blob: Blob]; reset: [] }>()
const { isRecording, audioBlob, elapsedSeconds, error, startRecording, stopRecording, resetRecording } = useRecorder()
const timer = computed(() => `0${Math.floor(elapsedSeconds.value / 60)}:${String(elapsedSeconds.value % 60).padStart(2, '0')}`)
const recordedAudioUrl = ref('')

watch(audioBlob, (blob) => {
  if (recordedAudioUrl.value) URL.revokeObjectURL(recordedAudioUrl.value)
  recordedAudioUrl.value = blob ? URL.createObjectURL(blob) : ''
})

async function start() { await startRecording() }
function stop() { stopRecording(); window.setTimeout(() => audioBlob.value && emit('recorded', audioBlob.value), 0) }
function reset() { resetRecording(); emit('reset') }
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
    <button v-if="!isRecording" class="record-button" :disabled="disabled" @click="start">
      <span class="mic-mark">●</span>{{ audioBlob ? 'Record again' : 'Start recording' }}
    </button>
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
