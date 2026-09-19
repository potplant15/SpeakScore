import { onBeforeUnmount, ref } from 'vue'

export function useRecorder() {
  const isRecording = ref(false)
  const audioBlob = ref<Blob | null>(null)
  const elapsedSeconds = ref(0)
  const error = ref('')

  let recorder: MediaRecorder | null = null
  let stream: MediaStream | null = null
  let chunks: Blob[] = []
  let timer: number | undefined

  async function startRecording() {
    error.value = ''
    if (!navigator.mediaDevices?.getUserMedia) {
      error.value = 'Microphone recording is not supported in this browser.'
      return
    }

    try {
      stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      chunks = []
      audioBlob.value = null
      elapsedSeconds.value = 0
      recorder = new MediaRecorder(stream)
      recorder.ondataavailable = (event) => {
        if (event.data.size > 0) chunks.push(event.data)
      }
      recorder.onerror = () => {
        error.value = 'Recording failed while capturing audio. Check that your microphone is connected and try again.'
        isRecording.value = false
        if (timer) window.clearInterval(timer)
        timer = undefined
      }
      recorder.onstop = () => {
        const blob = new Blob(chunks, { type: recorder?.mimeType || 'audio/webm' })
        audioBlob.value = blob.size > 0 ? blob : null
        if (blob.size === 0) error.value = 'No audio was captured. Speak for a moment before stopping, then try again.'
        stream?.getTracks().forEach((track) => track.stop())
        stream = null
      }
      recorder.start()
      isRecording.value = true
      timer = window.setInterval(() => elapsedSeconds.value += 1, 1000)
    } catch (cause) {
      const name = cause instanceof DOMException ? cause.name : ''
      if (name === 'NotAllowedError' || name === 'SecurityError') error.value = 'Microphone access was blocked. Allow microphone permission for this site, then try again.'
      else if (name === 'NotFoundError' || name === 'DevicesNotFoundError') error.value = 'No microphone was found. Connect a microphone and check your system input settings.'
      else if (name === 'NotReadableError' || name === 'TrackStartError') error.value = 'Your microphone is busy or unavailable. Close other apps using it, then try again.'
      else error.value = 'Could not start the microphone. Check your browser, site permissions, and input device.'
    }
  }

  function stopRecording() {
    if (!recorder || recorder.state === 'inactive') return
    recorder.stop()
    isRecording.value = false
    if (timer) window.clearInterval(timer)
    timer = undefined
  }

  function resetRecording() {
    if (isRecording.value) stopRecording()
    audioBlob.value = null
    elapsedSeconds.value = 0
    error.value = ''
  }

  onBeforeUnmount(() => {
    if (isRecording.value) stopRecording()
    stream?.getTracks().forEach((track) => track.stop())
  })

  return { isRecording, audioBlob, elapsedSeconds, error, startRecording, stopRecording, resetRecording }
}
