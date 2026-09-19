<script setup lang="ts">
import { computed, ref } from 'vue'

const props = defineProps<{ audioUrl: string; accent: string; ipa?: string; loading?: boolean }>()
const audio = ref<HTMLAudioElement | null>(null)
const playing = ref(false)
const progress = ref(0)
const label = computed(() => props.accent === 'en-US' ? 'American English' : 'British English')

function toggle() {
  if (!audio.value) return
  if (playing.value) audio.value.pause()
  else void audio.value.play()
}
function updateProgress() {
  if (audio.value?.duration) progress.value = (audio.value.currentTime / audio.value.duration) * 100
}
</script>

<template>
  <section class="reference-card">
    <div class="reference-topline">
      <span class="eyebrow">Listen first</span>
      <span class="voice-note"><i class="dot" /> {{ label }}</span>
    </div>
    <div v-if="ipa" class="ipa-line"><span class="eyebrow">Learner IPA</span><strong>/{{ ipa }}/</strong></div>
    <div class="reference-content">
      <button class="play-button" :disabled="loading" aria-label="Play reference" @click="toggle">
        <span v-if="!playing">▶</span><span v-else>Ⅱ</span>
      </button>
      <div class="waveform" :class="{ active: playing }" aria-hidden="true">
        <i v-for="n in 22" :key="n" :style="{ '--height': `${20 + ((n * 17) % 45)}%` }" />
      </div>
      <span class="listen-label">{{ playing ? 'Playing...' : 'Hear the rhythm' }}</span>
    </div>
    <div class="progress-line"><span :style="{ width: `${progress}%` }" /></div>
    <audio ref="audio" :src="audioUrl" @play="playing = true" @pause="playing = false" @ended="playing = false" @timeupdate="updateProgress" />
  </section>
</template>
