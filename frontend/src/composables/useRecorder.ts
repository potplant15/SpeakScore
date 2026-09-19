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
      recorder.onstop = () => {
        audioBlob.value = new Blob(chunks, { type: recorder?.mimeType || 'audio/webm' })
        stream?.getTracks().forEach((track) => track.stop())
        stream = null
      }
      recorder.start()
      isRecording.value = true
      timer = window.setInterval(() => elapsedSeconds.value += 1, 1000)
    } catch {
      error.value = 'Microphone permission was not granted.'
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
