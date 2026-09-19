<script setup lang="ts">
import type { EvaluationResult } from '@/types/practice'
defineProps<{ result: EvaluationResult }>()
</script>

<template>
  <section class="results-card">
    <div class="result-heading">
      <div><span class="eyebrow">Your speaking note</span><h2>That sounded like progress.</h2></div>
      <div class="score-ring"><strong>{{ Math.round(result.overallScore) }}</strong><span>/ 100</span></div>
    </div>
    <div class="metric-row">
      <div><span>Pronunciation</span><strong>{{ result.pronunciationScore.toFixed(1) }}</strong></div>
      <div><span>Content</span><strong>{{ result.contentAccuracy.toFixed(0) }}</strong></div>
      <div><span>Fluency</span><strong>{{ result.fluency.toFixed(1) }}</strong></div>
    </div>
    <div class="heard-line"><span class="eyebrow">We heard</span><p>{{ result.recognizedText || 'No speech detected' }}</p></div>
    <div v-if="result.details?.pronunciation_errors?.length" class="coaching-note">
      <span class="note-pin">!</span>
      <p><strong>One sound to revisit:</strong> {{ result.details.pronunciation_errors[0].word }} — heard <b>{{ result.details.pronunciation_errors[0].heard }}</b>, expected <b>{{ result.details.pronunciation_errors[0].expected }}</b>.</p>
    </div>
  </section>
</template>
